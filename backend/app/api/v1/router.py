from fastapi import APIRouter
from api.v1.endpoints import rag, complaints, insights, documents

router = APIRouter()

router.include_router(rag.router,        prefix="/rag",        tags=["RAG"])
router.include_router(complaints.router, prefix="/complaints",  tags=["Complaints"])
router.include_router(insights.router,   prefix="",            tags=["Insights"])
router.include_router(documents.router,  prefix="/documents",  tags=["Documents"])