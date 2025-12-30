# MyJournal Application

A personal journal and finance tracking application built with FastAPI.

## Features

- **Finance Tracking**: Upload CSV transactions, categorize expenses
- **PMP Study**: Project management learning resources
- **Language Learning**: Track language progress
- **Quotes Database**: Store and retrieve inspirational quotes
- **System Monitoring**: Log events and monitor system health

## Tech Stack

- **Backend**: FastAPI, Python 3.12
- **Database**: MySQL
- **Authentication**: JWT tokens
- **Deployment**: Uvicorn, Systemd
- **Frontend**: Jinja2 templates, HTML/CSS

## Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/myjournal.git
cd myjournal

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your database credentials

# Run the application
python -m app.main
