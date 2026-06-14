from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import sys, os, time
from pathlib import Path
from datetime import datetime
from google import genai

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent / "rag"))
from retrieve import retrieve

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from db.mongo import complaints_col

router = APIRouter()

class ComplaintRequest(BaseModel):
    text: str
    title: Optional[str] = None
    category: Optional[str] = "others"
    amount_involved: Optional[float] = 0.0

@router.post("/analyze")
def analyze_complaint(body: ComplaintRequest):
    try:
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

        # Use text as both title and description if title not provided
        title = body.title or body.text[:80]
        description = body.text

        laws = retrieve(description, top_k=5)
        context = "\n\n".join([f"[{r['source']}]\n{r['text']}" for r in laws])

        prompt = f"""You are a consumer rights expert in India.

A user has submitted this complaint:
Title: "{title}"
Description: "{description}"
Category: {body.category}

Relevant legal provisions from Indian law:
{context}

Provide:
1. Which laws apply and how
2. Strength of their case (Weak / Moderate / Strong) with reason
3. Key rights violated
4. Recommended next steps (3-5 actionable steps)

Be concise and practical."""

        # Retry on quota error
        response = None
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model="models/gemini-2.5-flash",
                    contents=prompt
                )
                break
            except Exception as e:
                if "429" in str(e) and attempt < 2:
                    time.sleep(5)
                else:
                    raise e

        # Save to MongoDB
        try:
            complaints_col.insert_one({
                "title": title,
                "text": description,
                "category": body.category,
                "ai_analysis": response.text,
                "timestamp": datetime.utcnow()
            })
        except Exception:
            pass

        return {
            "complaint": description,
            "title": title,
            "ai_analysis": response.text,
            "relevant_laws": laws,
            "status": "analyzed"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))