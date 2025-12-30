from datetime import datetime, timedelta
from jose import jwt

SECRET = "CHANGE_ME"
ALGO = "HS256"

def create_access_token(user_id: int):
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(hours=8)
    }
    return jwt.encode(payload, SECRET, algorithm=ALGO)
