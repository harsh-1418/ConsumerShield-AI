from fastapi import APIRouter
from app.workflows.resolution_flow import run_document_generation
from pydantic import BaseModel
from typing import Dict, Any

router = APIRouter()

class DocumentPayload(BaseModel):
    pass

@router.post("/generate")
def generate_document(payload: DocumentPayload):
    return run_document_generation(payload.model_dump())
