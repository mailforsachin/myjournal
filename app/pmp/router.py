from fastapi import APIRouter, HTTPException
from typing import List
from app.models import PMPAnswer, PMPConfirm, PMPQuestion

router = APIRouter()

# Mock data for testing
mock_questions = [
    {"id": 1, "question_text": "What is PMP?", "options": ["A", "B", "C", "D"], "correct_answer": 0}
]

@router.get("/")
async def pmp_home():
    return {"message": "PMP Exam Preparation Module"}

@router.get("/questions")
async def get_questions():
    return {"questions": mock_questions}

@router.post("/answer")
async def submit_answer(answer: PMPAnswer):
    return {"message": "Answer submitted", "answer": answer}

@router.post("/confirm")
async def confirm_answer(confirm: PMPConfirm):
    return {"message": "Answer confirmed", "confirm": confirm}

@router.get("/progress")
async def get_progress():
    return {"progress": {"total": 10, "completed": 3, "score": 75}}
