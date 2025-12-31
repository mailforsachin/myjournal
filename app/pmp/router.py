from fastapi import APIRouter, Depends
from app.auth.deps import get_current_user

router = APIRouter()

@router.get("/questions")
async def get_questions(user_id: int = Depends(get_current_user)):
    return {
        "questions": [
            {
                "id": 1,
                "question_text": "What is PMP?",
                "options": ["A", "B", "C", "D"],
                "correct_answer": 0
            }
        ]
    }

@router.get("/progress")
async def get_progress(user_id: int = Depends(get_current_user)):
    return {
        "progress": {
            "total": 10,
            "completed": 3,
            "score": 75
        }
    }
