from fastapi import APIRouter, Depends
from app.database import get_db
from app.auth.deps import get_current_user

router = APIRouter()

@router.get("/")
async def finance_home():
    return {"message": "Finance module OK"}

@router.get("/transactions")
async def get_transactions(user_id: int = Depends(get_current_user)):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *
        FROM transactions
        WHERE user_id = %s
        ORDER BY transaction_date DESC
        LIMIT 10
        """,
        (user_id,)
    )

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return {"transactions": rows}
