from fastapi import APIRouter, Query
from app.database import get_db

router = APIRouter()

@router.get("/events")
async def list_events(
    module: str | None = None,
    action: str | None = None,
    limit: int = Query(50, le=200)
):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT
            id,
            event_time,
            user,
            module,
            action,
            entity_type,
            entity_id,
            payload,
            ip_address
        FROM system_events
        WHERE 1=1
    """
    params = []

    if module:
        query += " AND module = %s"
        params.append(module)

    if action:
        query += " AND action = %s"
        params.append(action)

    query += " ORDER BY id DESC LIMIT %s"
    params.append(limit)

    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    return rows
