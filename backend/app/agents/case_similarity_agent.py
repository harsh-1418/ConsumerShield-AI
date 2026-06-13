# backend/app/agents/case_similarity_agent.py

import logging
from app.agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Case Similarity Interface – Member 2's RAG (cases_vectors collection) and/or
# Member 3's prediction module may eventually back this. A clean hook is
# provided with mock fallback so this agent works standalone.
# ---------------------------------------------------------------------------
def _case_similarity_search(query: str, category: str, top_k: int = 3) -> list[dict]:
    """
    Interface hook for retrieving similar historical cases.
    Attempts to use Member 2's RAG retriever against the cases_vectors collection.
    Falls back to structured mock data if unavailable.

    Returns a list of dicts matching the similar_cases schema:
    [
      {"case_id": str, "title": str, "similarity_score": float}
    ]
    """
    try:
        from app.rag.retriever import search_cases  # type: ignore
        results = search_cases(query=query, top_k=top_k)
        logger.info("Case retriever returned %d results", len(results))
        return results
    except ImportError:
        logger.warning("Case retrieval module not available — using mock fallback.")
        return _mock_similar_cases(category)


def _mock_similar_cases(category: str) -> list[dict]:
    """Structured mock historical case data, keyed by category."""
    mock_db = {
        "ecommerce": [
            {"case_id": "case_ec_101", "title": "Refund denied for damaged electronics - Amazon", "similarity_score": 0.86},
            {"case_id": "case_ec_204", "title": "Replacement refused despite manufacturing defect - Flipkart", "similarity_score": 0.81},
            {"case_id": "case_ec_309", "title": "Wrong product delivered, return window expired - Myntra", "similarity_score": 0.74},
        ],
        "banking": [
            {"case_id": "case_bk_055", "title": "Unauthorized EMI deduction not refunded - HDFC Bank", "similarity_score": 0.88},
            {"case_id": "case_bk_112", "title": "Double charge on credit card reversed after Ombudsman complaint - ICICI", "similarity_score": 0.83},
            {"case_id": "case_bk_180", "title": "Loan foreclosure charges disputed - Axis Bank", "similarity_score": 0.70},
        ],
        "telecom": [
            {"case_id": "case_tc_022", "title": "Service disconnected without notice - Airtel", "similarity_score": 0.79},
            {"case_id": "case_tc_058", "title": "Overcharging on data plan - Jio", "similarity_score": 0.75},
        ],
        "insurance": [
            {"case_id": "case_in_011", "title": "Health insurance claim rejected on technical ground", "similarity_score": 0.82},
            {"case_id": "case_in_044", "title": "Delay in claim settlement beyond IRDAI timeline", "similarity_score": 0.77},
        ],
        "real_estate": [
            {"case_id": "case_re_009", "title": "Builder delayed possession beyond RERA timeline", "similarity_score": 0.80},
        ],
        "others": [
            {"case_id": "case_ot_001", "title": "Service deficiency complaint resolved via DCDRC", "similarity_score": 0.68},
        ],
    }
    return mock_db.get(category, mock_db["others"])


class CaseSimilarityAgent(BaseAgent):
    """
    Finds historically similar consumer cases to help establish precedent
    and inform case strength assessment.

    Writes to state: similar_cases (list)
    """

    def __init__(self):
        super().__init__(temperature=0.0)

    def run(self, state: dict) -> dict:
        """
        Reads from state: summary, category, intent
        Writes to state: similar_cases
        """
        self.logger.info("CaseSimilarityAgent running for category: %s", state.get("category", "others"))

        query = f"{state.get('intent', '')} {state.get('summary', '')[:200]}"
        category = state.get("category", "others")

        results = _case_similarity_search(query=query, category=category, top_k=3)

        similar_cases = [
            {
                "case_id": r.get("case_id", ""),
                "title": r.get("title", ""),
                "similarity_score": round(float(r.get("similarity_score", 0.0)), 2),
            }
            for r in results
        ]

        return {"similar_cases": similar_cases}
