# backend/app/agents/legal_retrieval_agent.py

import logging
from app.agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# RAG Interface – Member 2 will replace this with the real implementation.
# This function signature is the agreed contract between Member 1 and Member 2.
# Member 2 implements: backend/app/rag/retriever.py → search(query, top_k) -> list[dict]
# ---------------------------------------------------------------------------
def _rag_search(query: str, top_k: int = 5) -> list[dict]:
    """
    Interface hook for Member 2's RAG retriever.
    Import is attempted first; if unavailable (e.g. during development or RAG not ready),
    falls back to structured mock data.

    Returns a list of dicts matching the relevant_laws schema:
    [
      {
        "id": str,
        "title": str,
        "section": str,
        "snippet": str,
        "score": float,
        "source_url": str
      }
    ]
    """
    try:
        from app.rag.retriever import search as rag_search  # type: ignore
        results = rag_search(query=query, top_k=top_k)
        logger.info("RAG retriever returned %d results for query: %s", len(results), query[:60])
        return results
    except ImportError:
        logger.warning("RAG module not available — using mock fallback for legal retrieval.")
        return _mock_legal_results(query)


def _mock_legal_results(query: str) -> list[dict]:
    """
    Structured mock fallback used when Member 2's RAG is not yet integrated.
    Covers the main complaint categories with real Indian law references.
    """
    q = query.lower()

    if any(kw in q for kw in ["refund", "ecommerce", "online", "defective", "product"]):
        return [
            {
                "id": "mock_cpa_2019_sec2_47",
                "title": "Consumer Protection Act 2019 – Unfair Trade Practice",
                "section": "Section 2(47)",
                "snippet": "Unfair trade practice means a trade practice which adopts any unfair method or deceptive practice for promoting sale or supply of goods or services.",
                "score": 0.92,
                "source_url": "https://consumeraffairs.nic.in/consumer-protection-act-2019",
            },
            {
                "id": "mock_cpa_2019_sec2_34",
                "title": "Consumer Protection Act 2019 – Product Liability",
                "section": "Section 2(34)",
                "snippet": "Product liability means the responsibility of a product manufacturer or product seller to compensate for any harm caused to a consumer by such defective product.",
                "score": 0.89,
                "source_url": "https://consumeraffairs.nic.in/consumer-protection-act-2019",
            },
            {
                "id": "mock_cpa_2019_sec87",
                "title": "Consumer Protection Act 2019 – Product Liability Action",
                "section": "Section 87",
                "snippet": "A product liability action may be brought by a complainant against a product manufacturer, product service provider or a product seller.",
                "score": 0.85,
                "source_url": "https://consumeraffairs.nic.in/consumer-protection-act-2019",
            },
        ]
    elif any(kw in q for kw in ["bank", "emi", "debit", "charge", "account", "loan"]):
        return [
            {
                "id": "mock_rbi_ombudsman_2006",
                "title": "Banking Ombudsman Scheme 2006",
                "section": "Clause 8",
                "snippet": "A complaint can be filed against a bank for charging without prior notice, non-adherence to RBI guidelines, or failure to resolve within 30 days of written complaint.",
                "score": 0.91,
                "source_url": "https://rbi.org.in/Scripts/bs_viewcontent.aspx?Id=159",
            },
            {
                "id": "mock_rbi_fair_practice",
                "title": "RBI Fair Practices Code for Lenders",
                "section": "Para 3(ii)",
                "snippet": "Lenders should give notice to the borrower of any change in terms and conditions including disbursement schedule, interest rates, service charges, prepayment charges etc.",
                "score": 0.87,
                "source_url": "https://rbi.org.in",
            },
        ]
    elif any(kw in q for kw in ["telecom", "mobile", "network", "trai", "recharge"]):
        return [
            {
                "id": "mock_trai_qos_2009",
                "title": "TRAI Quality of Service Regulations 2009",
                "section": "Regulation 4",
                "snippet": "Every service provider shall ensure that the quality of service benchmarks as specified are met and complaints are resolved within prescribed timelines.",
                "score": 0.88,
                "source_url": "https://trai.gov.in",
            },
        ]
    elif any(kw in q for kw in ["insurance", "claim", "policy", "irdai"]):
        return [
            {
                "id": "mock_irdai_grievance",
                "title": "IRDAI Grievance Redressal Guidelines 2010",
                "section": "Circular 014/IRDA/Life/Circular/GRV/01/11",
                "snippet": "Every insurer shall appoint a Grievance Redressal Officer and resolve complaints within 15 days of receipt. Unresolved complaints can be escalated to IRDAI via IGMS portal.",
                "score": 0.90,
                "source_url": "https://igms.irda.gov.in",
            },
        ]
    else:
        return [
            {
                "id": "mock_cpa_2019_general",
                "title": "Consumer Protection Act 2019 – Consumer Rights",
                "section": "Section 2(9)",
                "snippet": "Rights of consumers include right to be protected against marketing of goods and services which are hazardous, right to information, right to choose, right to be heard, and right to seek redressal.",
                "score": 0.80,
                "source_url": "https://consumeraffairs.nic.in/consumer-protection-act-2019",
            },
        ]


class LegalRetrievalAgent(BaseAgent):
    """
    Retrieves relevant legal provisions for the complaint using the RAG pipeline.
    Interfaces with Member 2's retriever via a clean hook with mock fallback.

    Writes to state: relevant_laws (list), rag_context (str for downstream agents)
    """

    def __init__(self):
        super().__init__(temperature=0.0)

    def run(self, state: dict) -> dict:
        """
        Reads from state: summary, intent, category
        Writes to state: relevant_laws, rag_context
        """
        self.logger.info("LegalRetrievalAgent running for intent: %s", state.get("intent", "unknown"))

        # Build a rich query from the complaint context
        query = (
            f"{state.get('intent', '')} {state.get('category', '')} "
            f"{state.get('summary', '')[:200]}"
        ).strip()

        results = _rag_search(query=query, top_k=5)

        # Build a plain-text context string for downstream agents (rights, roadmap)
        rag_context_lines = []
        for r in results:
            rag_context_lines.append(
                f"{r.get('title', '')} {r.get('section', '')}: {r.get('snippet', '')}"
            )
        rag_context = "\n".join(rag_context_lines)

        # Format to match the API contract schema for relevant_laws
        relevant_laws = [
            {
                "id": r.get("id", ""),
                "title": r.get("title", ""),
                "section": r.get("section", ""),
                "snippet": r.get("snippet", ""),
                "source_url": r.get("source_url", ""),
            }
            for r in results
        ]

        return {
            "relevant_laws": relevant_laws,
            "rag_context": rag_context,
        }
