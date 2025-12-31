from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth.jwt import create_access_token, verify_token
from pydantic import BaseModel

router = APIRouter()
security = HTTPBearer()

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest):
    """Login endpoint that returns JWT token"""
    # Simple hardcoded authentication
    if data.username == "sachin" and data.password == "Welcome@2026!":
        token = create_access_token(1)
        return {"access_token": token, "token_type": "bearer"}
    
    raise HTTPException(
        status_code=401,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

@router.get("/verify")
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify if token is valid"""
    token = credentials.credentials
    try:
        payload = verify_token(token)
        return {"valid": True, "user_id": payload["sub"]}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/me")
async def get_current_user_info(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current user information"""
    token = credentials.credentials
    try:
        payload = verify_token(token)
        return {
            "user_id": payload["sub"],
            "username": "sachin"  # Hardcoded for now
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")
