from fastapi import APIRouter
from app.models import WordEntry, PracticeSession

router = APIRouter()

@router.get("/")
async def language_home():
    return {"message": "Language Learning Module"}

@router.get("/words")
async def get_words():
    return {"words": ["hello", "world", "test"]}

@router.post("/add-word")
async def add_word(word: WordEntry):
    return {"message": "Word added", "word": word}

@router.post("/practice")
async def practice_session(session: PracticeSession):
    return {"message": "Practice completed", "session": session}
