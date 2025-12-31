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
from pydantic import BaseModel

app = FastAPI(title="MyJournal", version="1.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
	max_age=3600,
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

# Import and include routers with error handling
print("Loading routers...")

# 1. Auth router
try:
    from app.auth.router import router as auth_router
    app.include_router(auth_router, prefix="/api", tags=["auth"])
    print("✅ Auth router loaded")
except ImportError as e:
    print(f"❌ Auth router failed: {e}")
    from fastapi import APIRouter
    auth_router = APIRouter()
    app.include_router(auth_router, prefix="/api")

# 2. Finance router
try:
    from app.finance.router import router as finance_router
    app.include_router(finance_router, prefix="/api/finance", tags=["finance"])
    print("✅ Finance router loaded")
except ImportError as e:
    print(f"❌ Finance router failed: {e}")

# 3. Language router
try:
    from app.language.router import router as language_router
    app.include_router(language_router, prefix="/api/language", tags=["language"])
    print("✅ Language router loaded")
except ImportError as e:
    print(f"❌ Language router failed: {e}")

# 4. PMP router
try:
    from app.pmp.router import router as pmp_router
    app.include_router(pmp_router, prefix="/api/pmp", tags=["pmp"])
    print("✅ PMP router loaded")
except ImportError as e:
    print(f"❌ PMP router failed: {e}")

# 5. Quotes router
try:
    from app.quotes.router import router as quotes_router
    app.include_router(quotes_router, prefix="/api/quotes", tags=["quotes"])
    print("✅ Quotes router loaded")
except ImportError as e:
    print(f"❌ Quotes router failed: {e}")

# 6. System router
try:
    from app.system.router import router as system_router
    app.include_router(system_router, prefix="/api/system", tags=["system"])
    print("✅ System router loaded")
except ImportError as e:
    print(f"❌ System router failed: {e}")

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
                <p><a href="/transactions-ui">View Transactions UI</a></p>
            </body>
        </html>
        """)

# Keep the existing login endpoint for backward compatibility
class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/api/login")
async def legacy_login(data: LoginRequest):
    """Legacy login endpoint for backward compatibility"""
    try:
        from app.auth.jwt import create_access_token
        # Hardcoded auth
        if data.username == "sachin" and data.password == "Welcome@2026!":
            token = create_access_token(1)
            return {"access_token": token, "token_type": "bearer"}
    except:
        pass
    raise HTTPException(status_code=401, detail="Invalid credentials")

# Test database connection
@app.get("/api/test-db")
async def test_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT 1")
    return {"ok": True}

# Request logging middleware
@app.middleware("http")
async def request_logger(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = round((time.time() - start) * 1000, 2)

    print({
        "time": datetime.utcnow().isoformat(),
        "method": request.method,
        "path": request.url.path,
        "status": response.status_code,
        "duration_ms": duration,
    })

    return response

# Transactions UI endpoint
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
    if templates:
        return templates.TemplateResponse(
            "transactions.html",
            {"request": request, "transactions": rows}
        )
    else:
        return HTMLResponse(f"<pre>{rows}</pre>")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8011, reload=True)
