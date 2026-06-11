from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class InsightRequest(BaseModel):
    complaint: str
    relevant_laws: list = []

@router.post("/case-strength")
def case_strength(body: InsightRequest):
    # Stub — Member 3 will implement real scoring
    return {
        "score": 72,
        "label": "Strong",
        "explanation": "Your complaint aligns with multiple Consumer Protection Act provisions."
    }

@router.post("/roadmap")
def resolution_roadmap(body: InsightRequest):
    # Stub — Member 1 will implement via agents
    return {
        "steps": [
            "File complaint with seller formally via email",
            "Escalate to National Consumer Helpline (1800-11-4000)",
            "File case at District Consumer Commission"
        ]
    }

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from db.mongo import authorities_col

@router.post("/authorities")
def recommend_authorities(body: InsightRequest):
    # Simple keyword match for now
    complaint_lower = body.complaint.lower()
    keywords = {
        "bank": "banking", "upi": "UPI", "loan": "loan",
        "phone": "product defect", "amazon": "ecommerce",
        "flipkart": "ecommerce", "ad": "misleading ads",
        "telecom": "telecom", "internet": "broadband"
    }
    
    matched_type = "product defect"  # default
    for word, category in keywords.items():
        if word in complaint_lower:
            matched_type = category
            break
    
    results = list(authorities_col.find(
        {"handles": matched_type},
        {"_id": 0}
    ))
    
    if not results:
        results = list(authorities_col.find({}, {"_id": 0}).limit(2))
    
    return {"recommended_authorities": results}