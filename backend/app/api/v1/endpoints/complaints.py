from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
import sys, os
from pathlib import Path
from google import genai

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent / "rag"))
from retrieve import retrieve

router = APIRouter()

class ComplaintRequest(BaseModel):
    text: str
    category: Optional[str] = None

@router.post("/analyze")
def analyze_complaint(body: ComplaintRequest):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    
    laws = retrieve(body.text, top_k=5)
    context = "\n\n".join([f"[{r['source']}]\n{r['text']}" for r in laws])
    
    prompt = f"""You are a consumer rights expert in India.

A user has submitted this complaint:
"{body.text}"

Relevant legal provisions:
{context}

Provide:
1. Which laws apply and how
2. Strength of their case (Weak / Moderate / Strong)
3. Recommended next steps (3-5 actionable steps)

Be concise and practical."""

    response = client.models.generate_content(
    model="models/gemini-2.5-flash",
    contents=prompt
)
    
    return {
        "complaint": body.text,
        "ai_analysis": response.text,
        "relevant_laws": laws,
        "status": "analyzed"
    }