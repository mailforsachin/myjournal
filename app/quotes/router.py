from fastapi import APIRouter
from app.models import Quote

router = APIRouter()

@router.get("/")
async def quotes_home():
    return {"message": "Quotes Collection Module"}

@router.get("/random")
async def random_quote():
    return {
        "quote": {
            "text": "The only way to do great work is to love what you do.",
            "author": "Steve Jobs",
            "category": "Motivation"
        }
    }

@router.post("/add-quote")
async def add_quote(quote: Quote):
    return {"message": "Quote added", "quote": quote}

@router.get("/daily")
async def daily_quote():
    return {
        "daily_quote": {
            "text": "Today is a new day!",
            "author": "Anonymous",
            "date": "2025-12-30"
        }
    }
