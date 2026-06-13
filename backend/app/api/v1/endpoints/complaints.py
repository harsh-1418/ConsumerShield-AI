
from fastapi import APIRouter
from app.workflows.complaint_analysis_flow import run_complaint_analysis
from pydantic import BaseModel
from typing import Optional
import sys, os
from pathlib import Path
from google import genai

# Add at top of complaints.py
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from db.mongo import complaints_col
from datetime import datetime

# Inside analyze_complaint(), before the return:


sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent / "rag"))
from retrieve import retrieve

router = APIRouter()

class ComplaintRequest(BaseModel):
    text: str
    category: Optional[str] = None

@router.post("/analyze")
def analyze_complaint(payload: ComplaintRequest):
    return run_complaint_analysis(payload.model_dump())