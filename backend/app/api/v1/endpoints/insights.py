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