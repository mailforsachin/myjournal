from fastapi import APIRouter, Depends
from app.auth.deps import get_current_user
import json
import os

router = APIRouter()

# Path to language data file
LANGUAGE_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "french_vocab.json")

@router.get("/words")
async def get_words(user_id: int = Depends(get_current_user)):
    """Get vocabulary words"""
    try:
        with open(LANGUAGE_DATA_PATH, 'r') as f:
            data = json.load(f)
        return {"words": data}
    except Exception as e:
        print(f"Error loading words: {e}")
        # Return sample data
        return {"words": [
            {
                "id": 1,
                "title": "Bonjour – Hello",
                "fr": "Bonjour, comment allez-vous?",
                "en": "Hello, how are you?"
            },
            {
                "id": 2,
                "title": "Merci – Thank you",
                "fr": "Merci beaucoup pour votre aide.",
                "en": "Thank you very much for your help."
            }
        ]}

@router.post("/add-word")
async def add_word(word_data: dict, user_id: int = Depends(get_current_user)):
    """Add a new word"""
    return {"message": "Word added successfully", "word": word_data}

@router.get("/practice")
async def get_practice(user_id: int = Depends(get_current_user)):
    """Get practice questions"""
    return {
        "questions": [
            {
                "id": 1,
                "question": "Translate: Bonjour",
                "options": ["Hello", "Goodbye", "Thank you", "Please"],
                "answer": "Hello"
            }
        ]
    }
