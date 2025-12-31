from fastapi import APIRouter, Depends
from app.auth.deps import get_current_user
from datetime import datetime

router = APIRouter()

@router.get("/daily")
async def get_daily_quote(user_id: int = Depends(get_current_user)):
    return {
        "daily_quote": {
            "text": "Today is a new day!",
            "author": "Anonymous",
            "date": datetime.now().strftime("%Y-%m-%d")
        }
    }

@router.get("/random")
async def get_random_quote(user_id: int = Depends(get_current_user)):
    return {
        "quote": {
            "text": "The only way to do great work is to love what you do.",
            "author": "Steve Jobs",
            "category": "Motivation"
        }
    }
