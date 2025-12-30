import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# Database configuration
DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'myjournal_user',
    'password': 'SecurePass123!',
    'database': 'myjournal_db',
    'port': 3306
}

# Security
SECRET_KEY = "myjournal-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours

# Application settings
UPLOAD_FOLDER = BASE_DIR / "app" / "static" / "uploads"
ALLOWED_EXTENSIONS = {'csv', 'pdf', 'xlsx', 'xls'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

# Daily limits
DAILY_PMP_QUESTIONS = 20
DAILY_LANGUAGE_SENTENCES = 5

# Create uploads directory
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
