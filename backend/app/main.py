import sys
from pathlib import Path

# Add the app directory to path so 'api' is resolvable
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

from api.v1.router import router

app = FastAPI(title="ConsumerShield AI", version="1.0.0")

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        FRONTEND_URL,
        "http://localhost:5173",
        "http://localhost:3000",
        "https://consumershield.vercel.app"
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router, prefix="/api/v1")

@app.get("/health")
def health():
    return {"status": "ok"}