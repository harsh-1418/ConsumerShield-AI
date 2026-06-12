# backend/app/api/v1/endpoints/insights.py
# Member 3 - FastAPI endpoints: case insights, analytics, knowledge graph

import sys
import os
from datetime import datetime
from typing import List, Optional

# ── Add backend/ to path so all Member 3 modules resolve ──────────────
_backend_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../../..")
)
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from prediction.case_strength import score_case_strength
from prediction.risk_scoring import get_risk_profile, get_resolution_roadmap
from analytics.metrics import get_platform_metrics, get_category_breakdown
from analytics.usage_events import log_event, get_event_counts
from knowledge_graph.graph_builder import build_consumer_graph
from knowledge_graph.graph_queries import (
    get_rights_of_consumer,
    get_authorities_for_complaint,
    get_laws_protecting_right,
    get_connections_of_node,
)

router = APIRouter()

# ── Try to import Member 2's MongoDB collections ───────────────────────
try:
    from db.mongo import complaints_col, authorities_col
    _MONGO_AVAILABLE = True
except ImportError:
    _MONGO_AVAILABLE = False
    complaints_col = None
    authorities_col = None


# ─── REQUEST MODELS ───────────────────────────────────────────────────

class InsightRequest(BaseModel):
    complaint: str
    relevant_laws: Optional[List[str]] = []
    complaint_value_lakh: Optional[float] = 5.0


# ─── CASE STRENGTH ────────────────────────────────────────────────────

@router.post("/insights/case-strength")
async def case_strength(request: InsightRequest):
    try:
        strength = score_case_strength(
            complaint=request.complaint,
            relevant_laws=request.relevant_laws,
        )
        risk = get_risk_profile(strength["score"])
        roadmap = get_resolution_roadmap(
            strength["score"],
            strength.get("recommended_forum", "District Forum"),
        )

        if _MONGO_AVAILABLE:
            try:
                from db.mongo import db as _db
                log_event(_db, "complaint_analyzed", {
                    "score": strength["score"],
                    "label": strength["label"],
                })
            except Exception:
                pass

        return {
            "success": True,
            "score": strength["score"],
            "label": strength["label"],
            "reason": strength["reason"],
            "winning_chances": strength["winning_chances"],
            "key_rights_violated": strength.get("key_rights_violated", []),
            "applicable_sections": strength.get("applicable_sections", []),
            "recommended_forum": strength.get("recommended_forum", "NCH Helpline"),
            "risk_profile": risk,
            "resolution_roadmap": roadmap,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ─── FULL INSIGHT PACKAGE (for Member 1's agent pipeline) ─────────────

@router.post("/case/insights")
async def get_case_insights(request: InsightRequest):
    try:
        strength = score_case_strength(request.complaint, request.relevant_laws)
        risk = get_risk_profile(strength["score"])
        roadmap = get_resolution_roadmap(
            strength["score"],
            strength.get("recommended_forum", "District Forum"),
        )
        authority = get_authorities_for_complaint(request.complaint_value_lakh)

        return {
            "success": True,
            "strength": strength,
            "risk_profile": risk,
            "resolution_roadmap": roadmap,
            "authority_recommendation": authority,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ─── RESOLUTION ROADMAP ───────────────────────────────────────────────

@router.post("/insights/roadmap")
async def resolution_roadmap(request: InsightRequest):
    try:
        strength = score_case_strength(request.complaint, request.relevant_laws)
        roadmap = get_resolution_roadmap(
            strength["score"],
            strength.get("recommended_forum", "District Forum"),
        )
        return {
            "success": True,
            "score": strength["score"],
            "label": strength["label"],
            "roadmap": roadmap,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ─── AUTHORITY RECOMMENDATION ─────────────────────────────────────────

@router.post("/insights/authorities")
async def recommend_authorities(request: InsightRequest):
    try:
        kg_authority = get_authorities_for_complaint(request.complaint_value_lakh)

        db_authorities = []
        if _MONGO_AVAILABLE and authorities_col is not None:
            try:
                db_authorities = list(authorities_col.find({}, {"_id": 0}))
            except Exception:
                pass

        complaint_lower = request.complaint.lower()
        keyword_matches = []

        keyword_map = {
            "bank":      "RBI Banking Ombudsman",
            "payment":   "RBI Banking Ombudsman",
            "upi":       "RBI Banking Ombudsman",
            "loan":      "RBI Banking Ombudsman",
            "telecom":   "TRAI",
            "internet":  "TRAI",
            "broadband": "TRAI",
            "insurance": "IRDAI Ombudsman",
            "policy":    "IRDAI Ombudsman",
            "ad":        "ASCI",
            "mislead":   "ASCI (Advertising Standards Council of India)",
            "ecommerce": "District Consumer Forum + NCH Helpline",
            "amazon":    "District Consumer Forum + NCH Helpline",
            "flipkart":  "District Consumer Forum + NCH Helpline",
        }
        for keyword, authority_name in keyword_map.items():
            if keyword in complaint_lower and authority_name not in keyword_matches:
                keyword_matches.append(authority_name)

        return {
            "success": True,
            "recommended_authorities": keyword_matches or [kg_authority["primary"]],
            "primary_forum": kg_authority["primary"],
            "appeal_to": kg_authority.get("appeal_to", ""),
            "claim_limit": kg_authority["limit"],
            "all_authorities": db_authorities,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ─── ANALYTICS ────────────────────────────────────────────────────────

@router.get("/analytics/metrics")
async def platform_metrics():
    if _MONGO_AVAILABLE and complaints_col is not None:
        try:
            from db.mongo import db as _db
            return get_platform_metrics(_db)
        except Exception:
            pass

    return {
        "total_complaints": 0,
        "strong_cases": 0,
        "moderate_cases": 0,
        "weak_cases": 0,
        "strong_cases_pct": 0,
        "moderate_cases_pct": 0,
        "weak_cases_pct": 0,
        "average_strength_score": 0,
        "last_updated": datetime.utcnow().isoformat(),
        "note": "MongoDB not connected yet",
    }


@router.get("/analytics/events")
async def recent_events():
    if _MONGO_AVAILABLE:
        try:
            from db.mongo import db as _db
            return get_event_counts(_db)
        except Exception:
            pass
    return {"event_counts": [], "message": "MongoDB not connected yet"}


@router.get("/analytics/categories")
async def category_breakdown():
    if _MONGO_AVAILABLE and complaints_col is not None:
        try:
            from db.mongo import db as _db
            return get_category_breakdown(_db)
        except Exception:
            pass
    return {"categories": [], "message": "MongoDB not connected yet"}


# ─── KNOWLEDGE GRAPH ──────────────────────────────────────────────────

@router.get("/knowledge-graph")
async def knowledge_graph():
    return build_consumer_graph()


@router.get("/knowledge-graph/rights")
async def consumer_rights():
    return {"rights": get_rights_of_consumer()}


@router.get("/knowledge-graph/node/{node_id}")
async def node_detail(node_id: str):
    return get_connections_of_node(node_id)


@router.get("/knowledge-graph/laws/{right_id}")
async def laws_for_right(right_id: str):
    return {"laws": get_laws_protecting_right(right_id)}


@router.get("/authority/recommend")
async def recommend_authority(complaint_value_lakh: float = 5.0):
    return get_authorities_for_complaint(complaint_value_lakh)