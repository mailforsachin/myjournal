from fastapi import APIRouter, HTTPException, UploadFile, File, Depends, Query
import csv, io, json
from datetime import datetime
from app.database import get_db
from app.auth.deps import get_current_user
from app.finance.categorizer import categorize
from app.utils.events import log_event
import os

RULES_PATH = os.path.join(os.path.dirname(__file__), "rules.json")

router = APIRouter()

# -------------------------
# HEALTH / HOME
# -------------------------
@router.get("/")
async def finance_home():
    return {"message": "Finance module OK"}

# -------------------------
# TRANSACTIONS (pagination + filters)
# -------------------------
@router.get("/transactions")
async def get_transactions(
    user_id: int = Depends(get_current_user),
    page: int = Query(1, ge=1),
    limit: int = Query(20, le=100),
    type: str | None = None,
    confirmed: bool | None = None,
    search: str | None = None,
):
    offset = (page - 1) * limit

    clauses = ["user_id=%s"]
    params = [user_id]

    if type:
        clauses.append("type=%s")
        params.append(type)

    if confirmed is not None:
        clauses.append("confirmed=%s")
        params.append(int(confirmed))

    if search:
        clauses.append("description LIKE %s")
        params.append(f"%{search}%")

    where = " AND ".join(clauses)

    conn = get_db()
    cur = conn.cursor(dictionary=True)

    cur.execute(
        f"""
        SELECT *
        FROM transactions
        WHERE {where}
        ORDER BY transaction_date DESC, id DESC
        LIMIT %s OFFSET %s
        """,
        (*params, limit, offset),
    )
    rows = cur.fetchall()

    cur.execute(
        f"SELECT COUNT(*) AS total FROM transactions WHERE {where}",
        params,
    )
    total = cur.fetchone()["total"]

    cur.close()
    conn.close()

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "transactions": rows,
    }

# -------------------------
# CSV UPLOAD
# -------------------------
@router.post("/upload-csv")
async def upload_csv(
    file: UploadFile = File(...),
    user_id: int = Depends(get_current_user),
):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(400, "Only CSV files allowed")

    content = await file.read()
    reader = csv.DictReader(io.StringIO(content.decode("utf-8-sig")))

    conn = get_db()
    cur = conn.cursor()
    inserted = 0

    for row in reader:
        raw_date = row.get("Transaction Date") or row.get("Date")
        amount_raw = row.get("CAD$") or row.get("Amount")

        if not raw_date or not amount_raw:
            continue

        try:
            txn_date = datetime.strptime(raw_date.strip(), "%m/%d/%Y").date()
            amount = float(amount_raw)
        except Exception:
            continue

        description = " ".join(
            filter(None, [row.get("Description 1"), row.get("Description 2")])
        ).strip()

        txn_type = "expense" if amount < 0 else "income"
        auto_category = categorize(description)

        cur.execute(
            """
            INSERT INTO transactions
            (user_id, transaction_date, description, amount, type, auto_category, raw_data, source_file)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                user_id,
                txn_date,
                description,
                amount,
                txn_type,
                auto_category,
                json.dumps(row),
                file.filename,
            ),
        )
        inserted += 1

    conn.commit()
    cur.close()
    conn.close()

    log_event(
        user="sachin",
        module="finance",
        action="finance.csv.import",
        entity_type="csv",
        payload={"file": file.filename, "inserted": inserted},
    )

    return {"file": file.filename, "inserted": inserted}

# -------------------------
# CSV REPLAY (STEP 5)
# -------------------------
@router.post("/replay/{event_id}")
async def replay_csv(
    event_id: int,
    user_id: int = Depends(get_current_user),
):
    conn = get_db()
    cur = conn.cursor(dictionary=True)

    # 1. Fetch event
    cur.execute(
        """
        SELECT payload
        FROM system_events
        WHERE id=%s AND module='finance' AND action='finance.csv.import'
        """,
        (event_id,)
    )
    event = cur.fetchone()
    if not event:
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Event not found")

    # 2. Payload is stored as JSON STRING → decode it
    try:
        payload = json.loads(event["payload"])
    except Exception:
        cur.close()
        conn.close()
        raise HTTPException(status_code=500, detail="Invalid event payload")

    file = payload.get("file")
    if not file:
        cur.close()
        conn.close()
        raise HTTPException(status_code=400, detail="No file in event payload")

    # 3. Delete previous imports for that file & user
    cur.execute(
        """
        DELETE FROM transactions
        WHERE user_id=%s AND source_file=%s
        """,
        (user_id, file)
    )
    deleted = cur.rowcount

    conn.commit()
    cur.close()
    conn.close()

    return {
        "status": "ready-for-reimport",
        "file": file,
        "deleted_rows": deleted
    }

# -------------------------
# MANUAL CATEGORY OVERRIDE
# -------------------------
@router.patch("/transactions/{tx_id}/category")
async def override_category(
    tx_id: int,
    payload: dict,
    user_id: int = Depends(get_current_user),
):
    category = payload.get("manual_category")
    if not category:
        raise HTTPException(400, "manual_category required")

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE transactions
        SET manual_category=%s, confirmed=1
        WHERE id=%s AND user_id=%s
        """,
        (category, tx_id, user_id),
    )
    conn.commit()

    cur.close()
    conn.close()

    return {
        "status": "updated",
        "transaction_id": tx_id,
        "manual_category": category,
    }

# -------------------------
# SUMMARY (STEP 6 backend)
# -------------------------
@router.get("/summary")
async def finance_summary(user_id: int = Depends(get_current_user)):
    conn = get_db()
    cur = conn.cursor(dictionary=True)

    cur.execute(
        "SELECT SUM(amount) AS total FROM transactions WHERE user_id=%s AND amount>0",
        (user_id,),
    )
    income = cur.fetchone()["total"] or 0

    cur.execute(
        "SELECT SUM(amount) AS total FROM transactions WHERE user_id=%s AND amount<0",
        (user_id,),
    )
    expense = abs(cur.fetchone()["total"] or 0)

    cur.execute(
        """
        SELECT
            COALESCE(manual_category, auto_category) AS category,
            SUM(amount) AS total
        FROM transactions
        WHERE user_id=%s
        GROUP BY COALESCE(manual_category, auto_category)
        ORDER BY ABS(SUM(amount)) DESC
        """,
        (user_id,),
    )
    categories = cur.fetchall()

    cur.execute(
        """
        SELECT confirmed, COUNT(*) AS count
        FROM transactions
        WHERE user_id=%s
        GROUP BY confirmed
        """,
        (user_id,),
    )
    confirmed = cur.fetchall()

    cur.close()
    conn.close()

    return {
        "income": round(income, 2),
        "expense": round(expense, 2),
        "net": round(income - expense, 2),
        "by_category": categories,
        "confirmed": confirmed,
    }
@router.get("/rules")
async def get_rules(user_id: int = Depends(get_current_user)):
    with open(RULES_PATH) as f:
        return json.load(f)

@router.put("/rules")
async def update_rules(
    payload: dict,
    user_id: int = Depends(get_current_user),
):
    with open(RULES_PATH, "w") as f:
        json.dump(payload, f, indent=2)

    return {"status": "updated"}
