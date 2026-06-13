from fastapi import APIRouter
from pydantic import BaseModel
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent / "rag"))
from retrieve import retrieve

router = APIRouter()

class RAGQuery(BaseModel):
    query: str
    top_k: int = 5

@router.post("/search")
def rag_search(body: RAGQuery):
    try:
        results = retrieve(body.query, body.top_k)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))