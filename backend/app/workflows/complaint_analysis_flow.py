# backend/app/workflows/complaint_analysis_flow.py

import logging
from typing import TypedDict, Optional, Any

from langgraph.graph import StateGraph, END

from app.agents.intent_agent import IntentAgent
from app.agents.legal_retrieval_agent import LegalRetrievalAgent
from app.agents.case_similarity_agent import CaseSimilarityAgent
from app.agents.rights_agent import RightsAgent
from app.agents.evidence_agent import EvidenceAgent
from app.agents.authority_agent import AuthorityAgent
from app.agents.action_planning_agent import ActionPlanningAgent

logger = logging.getLogger(__name__)


class AgentState(TypedDict, total=False):
    """
    Shared state object passed between all nodes of the complaint analysis graph.
    This corresponds directly to the POST /api/v1/complaints/analyze contract
    (input fields + output fields accumulated as the graph executes).
    """

    # ---- Input fields (from request) ----
    user_id: Optional[str]
    title: str
    description: str
    category: str
    amount_involved: float
    evidence_texts: list[str]
    location: Optional[str]

    # ---- Intermediate / shared fields ----
    rag_context: str
    evidence_assessment: dict[str, Any]

    # ---- Output fields (match API contract) ----
    intent: str
    summary: str
    rights: list[dict[str, Any]]
    relevant_laws: list[dict[str, Any]]
    similar_cases: list[dict[str, Any]]
    case_strength: dict[str, Any]
    authorities: list[dict[str, Any]]
    resolution_roadmap: dict[str, Any]
    legal_notice_preview: dict[str, Any]


# ---------------------------------------------------------------------------
# Node wrapper functions
# Each node receives the full AgentState dict, runs its agent, and returns
# a partial dict of updated keys which LangGraph merges into the state.
# ---------------------------------------------------------------------------

_intent_agent = IntentAgent()
_legal_retrieval_agent = LegalRetrievalAgent()
_case_similarity_agent = CaseSimilarityAgent()
_rights_agent = RightsAgent()
_evidence_agent = EvidenceAgent()
_authority_agent = AuthorityAgent()
_action_planning_agent = ActionPlanningAgent()


def intent_node(state: AgentState) -> dict:
    logger.info("Executing node: intent_node")
    return _intent_agent.run(dict(state))


def legal_retrieval_node(state: AgentState) -> dict:
    logger.info("Executing node: legal_retrieval_node")
    return _legal_retrieval_agent.run(dict(state))


def case_similarity_node(state: AgentState) -> dict:
    logger.info("Executing node: case_similarity_node")
    return _case_similarity_agent.run(dict(state))


def evidence_node(state: AgentState) -> dict:
    logger.info("Executing node: evidence_node")
    return _evidence_agent.run(dict(state))


def rights_node(state: AgentState) -> dict:
    logger.info("Executing node: rights_node")
    return _rights_agent.run(dict(state))


def authority_node(state: AgentState) -> dict:
    logger.info("Executing node: authority_node")
    return _authority_agent.run(dict(state))


def action_planning_node(state: AgentState) -> dict:
    logger.info("Executing node: action_planning_node")
    return _action_planning_agent.run(dict(state))


# ---------------------------------------------------------------------------
# Conditional routing
# ---------------------------------------------------------------------------

def route_after_intent(state: AgentState) -> str:
    """
    If the IntentAgent classifies the complaint as out_of_scope, short-circuit
    the graph and route directly to END (skip legal analysis entirely).
    """
    if state.get("intent") == "out_of_scope":
        logger.info("Routing: intent=out_of_scope -> END")
        return "end"
    return "continue"


# ---------------------------------------------------------------------------
# Graph construction
# ---------------------------------------------------------------------------

def build_complaint_analysis_graph() -> StateGraph:
    """
    Builds and returns the compiled LangGraph StateGraph for complaint analysis.

    Flow:
      intent -> [conditional] -> legal_retrieval -> (case_similarity, evidence in parallel-ish sequence)
             -> rights -> authority -> action_planning -> END

    Note: LangGraph executes nodes sequentially in this linear graph definition;
    true parallel fan-out is avoided here for simplicity and determinism,
    which is preferable for a hackathon-grade demo.
    """
    graph = StateGraph(AgentState)

    graph.add_node("intent", intent_node)
    graph.add_node("legal_retrieval", legal_retrieval_node)
    graph.add_node("case_similarity", case_similarity_node)
    graph.add_node("evidence", evidence_node)
    graph.add_node("rights", rights_node)
    graph.add_node("authority", authority_node)
    graph.add_node("action_planning", action_planning_node)

    graph.set_entry_point("intent")

    graph.add_conditional_edges(
        "intent",
        route_after_intent,
        {
            "continue": "legal_retrieval",
            "end": END,
        },
    )

    graph.add_edge("legal_retrieval", "case_similarity")
    graph.add_edge("case_similarity", "evidence")
    graph.add_edge("evidence", "rights")
    graph.add_edge("rights", "authority")
    graph.add_edge("authority", "action_planning")
    graph.add_edge("action_planning", END)

    return graph


def get_compiled_complaint_analysis_workflow():
    """Returns the compiled, runnable complaint analysis workflow."""
    graph = build_complaint_analysis_graph()
    return graph.compile()


# Module-level compiled workflow instance, ready for import by API endpoints.
complaint_analysis_workflow = get_compiled_complaint_analysis_workflow()


def run_complaint_analysis(payload: dict) -> dict:
    """
    Main entry point for the /api/v1/complaints/analyze endpoint.

    payload: dict matching the request schema:
        {
          "user_id": str | None,
          "title": str,
          "description": str,
          "category": str,
          "amount_involved": float,
          "evidence_texts": list[str],
          "location": str | None (optional)
        }

    Returns: dict matching the response schema defined in docs/api_contracts.md
    """
    initial_state: AgentState = {
        "user_id": payload.get("user_id"),
        "title": payload.get("title", ""),
        "description": payload.get("description", ""),
        "category": payload.get("category", "others"),
        "amount_involved": float(payload.get("amount_involved", 0.0)),
        "evidence_texts": payload.get("evidence_texts", []) or [],
        "location": payload.get("location"),
    }

    final_state = complaint_analysis_workflow.invoke(initial_state)

    # Handle out_of_scope short-circuit gracefully
    if final_state.get("intent") == "out_of_scope":
        return {
            "intent": "out_of_scope",
            "summary": final_state.get("summary", "This complaint does not appear to be a consumer rights issue."),
            "rights": [],
            "relevant_laws": [],
            "similar_cases": [],
            "case_strength": {"score": 0.0, "label": "Not Applicable", "reasons": ["Complaint is out of scope for consumer rights analysis."]},
            "authorities": [],
            "resolution_roadmap": {"steps": []},
        }

    return {
        "intent": final_state.get("intent", ""),
        "summary": final_state.get("summary", ""),
        "rights": final_state.get("rights", []),
        "relevant_laws": final_state.get("relevant_laws", []),
        "similar_cases": final_state.get("similar_cases", []),
        "case_strength": final_state.get("case_strength", {}),
        "authorities": final_state.get("authorities", []),
        "resolution_roadmap": final_state.get("resolution_roadmap", {"steps": []}),
    }
