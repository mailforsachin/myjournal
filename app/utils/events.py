import json
from app.database import get_db

def log_event(
    *,
    user: str,
    module: str,
    action: str,
    entity_type: str | None = None,
    entity_id: str | None = None,
    payload: dict | None = None,
    ip: str | None = None
):
    conn = get_db()              # ✅ MISSING LINE
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO system_events
        (user, module, action, entity_type, entity_id, payload, ip_address)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        """,
        (
            user,
            module,
            action,
            entity_type,
            entity_id,
            json.dumps(payload) if payload else None,
            ip
        )
    )

    conn.commit()
    cursor.close()
    conn.close()
