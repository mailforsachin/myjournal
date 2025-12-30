from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

# User Models
class UserLogin(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    username: str
    password: str
    email: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

# PMP Models
class PMPAnswer(BaseModel):
    question_id: int
    answer: str
    is_correct: Optional[bool] = None

class PMPConfirm(BaseModel):
    answer_id: int
    confirmed: bool
    notes: Optional[str] = None

class PMPQuestion(BaseModel):
    question_text: str
    options: List[str]
    correct_answer: int
    category: Optional[str] = None
    difficulty: Optional[str] = None

# Finance Models
class Transaction(BaseModel):
    amount: float
    description: str
    category: str
    date: Optional[datetime] = None
    type: Optional[str] = "expense"  # or "income"

class Budget(BaseModel):
    category: str
    limit: float
    period: str  # "monthly", "weekly", "yearly"

# Language Models
class WordEntry(BaseModel):
    word: str
    translation: str
    language: str
    notes: Optional[str] = None

class PracticeSession(BaseModel):
    words: List[str]
    score: float
    date: Optional[datetime] = None

# Quotes Models
class Quote(BaseModel):
    text: str
    author: str
    category: Optional[str] = None
    tags: Optional[List[str]] = None
