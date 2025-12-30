from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from app.system.router import router as system_router
from pathlib import Path
import uvicorn
import time
from datetime import datetime
from app.database import get_db
from app.auth.jwt import create_access_token
from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

# Import routers
try:
    from app.finance.router import router as finance_router
except ImportError:
    # Create dummy router if import fails
    from fastapi import APIRouter
    finance_router = APIRouter()
    @finance_router.get("/")
    async def dummy():
        return {"message": "Finance module not fully implemented"}

try:
    from app.pmp.router import router as pmp_router
except ImportError:
    from fastapi import APIRouter
    pmp_router = APIRouter()
    @pmp_router.get("/")
    async def dummy():
        return {"message": "PMP module not fully implemented"}

try:
    from app.language.router import router as language_router
except ImportError:
    from fastapi import APIRouter
    language_router = APIRouter()
    @language_router.get("/")
    async def dummy():
        return {"message": "Language module not fully implemented"}

try:
    from app.quotes.router import router as quotes_router
except ImportError:
    from fastapi import APIRouter
    quotes_router = APIRouter()
    @quotes_router.get("/")
    async def dummy():
        return {"message": "Quotes module not fully implemented"}

app = FastAPI(title="MyJournal", version="1.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files only if directory exists
static_dir = Path(__file__).parent.parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    print(f"✅ Static files mounted from {static_dir}")
else:
    print(f"⚠️  Static directory not found: {static_dir}")

# Templates
templates_dir = Path("templates")
if templates_dir.exists():
    templates = Jinja2Templates(directory=templates_dir)
else:
    print("⚠️  Templates directory not found: templates")
    templates = None

# Include routers
app.include_router(finance_router, prefix="/api/finance", tags=["finance"])
app.include_router(pmp_router, prefix="/api/pmp", tags=["pmp"])
app.include_router(language_router, prefix="/api/language", tags=["language"])
app.include_router(quotes_router, prefix="/api/quotes", tags=["quotes"])
app.include_router(system_router, prefix="/api/system", tags=["system"])

# Health check endpoint
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "MyJournal"}

# Home page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    if templates:
        return templates.TemplateResponse("index.html", {"request": request})
    else:
        return HTMLResponse("""
        <html>
            <body>
                <h1>MyJournal</h1>
                <p>Welcome to MyJournal API!</p>
                <p>API is running. Access documentation at <a href="/docs">/docs</a></p>
                <p>Test login: username: sachin, password: ~~</p>
            </body>
        </html>
        """)

# Simple login endpoint
@app.post("/api/login")
async def login(data: LoginRequest):
    if data.username == "sachin" and data.password == "Welcome@2026!":
        token = create_access_token(1)
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

# Test database connection
@app.get("/api/test-db")
async def test_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT 1")
    return {"ok": True}

@app.middleware("http")
async def request_logger(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = round((time.time() - start) * 1000, 2)

    print({
        "time": datetime.utcnow().isoformat(),
        "method": request.method,
        "path": request.url.path,
        "ip": request.client.host if request.client else None,
        "status": response.status_code,
        "duration_ms": duration,
        "user_agent": request.headers.get("user-agent")
    })

    return response

@app.get("/transactions-ui", response_class=HTMLResponse)
async def transactions_ui(request: Request):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM transactions ORDER BY transaction_date DESC LIMIT 50"
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return templates.TemplateResponse(
        "transactions.html",
        {"request": request, "transactions": rows}
    )


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8011, reload=True)
