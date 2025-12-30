from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from pydantic import BaseModel
import csv, io, json
from datetime import datetime
from app.database import get_db
from app.auth.deps import get_current_user

router = APIRouter()


# ----------------------------
# MODELS
# ----------------------------

class ManualCategoryUpdate(BaseModel):
    manual_category: str


# ----------------------------
# ROUTES
# ----------------------------

@router.get("/")
async def finance_home():
    return {"message": "Finance module OK"}


@router.get("/transactions")
async def get_transactions(
    user_id: int = Depends(get_current_user),
    limit: int = 10,
    offset: int = 0,
):
    conn = get_db()
    cur = conn.cursor(dictionary=True)

    cur.execute(
        """
        SELECT
            id,
            transaction_date,
            description,
            amount,
            type,
            auto_category,
            manual_category,
            confirmed
        FROM transactions
        WHERE user_id=%s
        ORDER BY transaction_date DESC
        LIMIT %s OFFSET %s
        """,
        (user_id, limit, offset),
    )

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return {
        "limit": limit,
        "offset": offset,
        "count": len(rows),
        "transactions": rows,
    }


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
        raw_date = row.get("Transaction Date")
        amount_raw = row.get("CAD$")

        if not raw_date or not amount_raw:
            continue

        try:
            txn_date = datetime.strptime(raw_date.strip(), "%m/%d/%Y").date()
            amount = float(amount_raw)
        except Exception:
            continue

        description = row.get("Description 1", "").strip()
        txn_type = "expense" if amount < 0 else "income"

        cur.execute(
            """
            INSERT INTO transactions
            (user_id, transaction_date, description, amount, type, raw_data)
            VALUES (%s,%s,%s,%s,%s,%s)
            """,
            (user_id, txn_date, description, amount, txn_type, json.dumps(row)),
        )

        inserted += 1

    conn.commit()
    cur.close()
    conn.close()

    return {
        "file": file.filename,
        "inserted": inserted,
    }


@router.patch("/transactions/{transaction_id}/category")
async def set_manual_category(
    transaction_id: int,
    data: ManualCategoryUpdate,
    user_id: int = Depends(get_current_user),
):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE transactions
        SET manual_category=%s,
            confirmed=1
        WHERE id=%s AND user_id=%s
        """,
        (data.manual_category, transaction_id, user_id),
    )

    if cur.rowcount == 0:
        cur.close()
        conn.close()
        raise HTTPException(404, "Transaction not found")

    conn.commit()
    cur.close()
    conn.close()

    return {
        "status": "updated",
        "transaction_id": transaction_id,
        "manual_category": data.manual_category,
    }
