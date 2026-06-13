# backend/app/workflows/resolution_flow.py

import logging
from typing import TypedDict, Optional, Any

from langgraph.graph import StateGraph, END

from app.agents.document_generation_agent import DocumentGenerationAgent
from app.agents.action_planning_agent import ActionPlanningAgent
from app.agents.authority_agent import AuthorityAgent

logger = logging.getLogger(__name__)


class ResolutionState(TypedDict, total=False):
    """
    Shared state for the resolution/document-generation workflow.
    Used by POST /api/v1/documents/generate and as a secondary flow that can
    re-derive a roadmap + authorities + document for an existing complaint
    (e.g. for the /api/v1/cases/{case_id}/insights endpoint's "roadmap" field).
    """

    # ---- Input fields ----
    document_type: str  # "complaint" | "legal_notice"
    complainant_name: str
    respondent_name: str
    amount_involved: float
    facts: str
    reliefs_sought: str

    # Optional context carried over from a prior complaint analysis, used to
    # refresh / regenerate roadmap and authorities for the resolution flow.
    intent: Optional[str]
    category: Optional[str]
    summary: Optional[str]
    rights: Optional[list[dict[str, Any]]]
    evidence_assessment: Optional[dict[str, Any]]
    similar_cases: Optional[list[dict[str, Any]]]
    location: Optional[str]

    # ---- Output fields ----
    document: dict[str, Any]
    authorities: list[dict[str, Any]]
    resolution_roadmap: dict[str, Any]
    case_strength: dict[str, Any]


_document_generation_agent = DocumentGenerationAgent()
_authority_agent = AuthorityAgent()
_action_planning_agent = ActionPlanningAgent()


def authority_node(state: ResolutionState) -> dict:
    """
    Recomputes / confirms the recommended authorities for this resolution,
    in case the caller did not pass them through from the analysis stage.
    """
    logger.info("Executing node: authority_node (resolution_flow)")
    if state.get("category"):
        return _authority_agent.run(dict(state))
    # No category context available — skip authority recomputation gracefully.
    return {"authorities": state.get("authorities", [])}


def action_planning_node(state: ResolutionState) -> dict:
    """
    Recomputes the resolution roadmap and case strength for this resolution,
    using whatever context (rights, evidence, similar_cases) is available.
    """
    logger.info("Executing node: action_planning_node (resolution_flow)")
    if state.get("category") and state.get("intent"):
        merged_state = dict(state)
        return _action_planning_agent.run(merged_state)
    # Insufficient context — return empty placeholders rather than failing.
    return {
        "resolution_roadmap": state.get("resolution_roadmap", {"steps": []}),
        "case_strength": state.get("case_strength", {"score": 0.0, "label": "Unknown", "reasons": []}),
    }


def document_generation_node(state: ResolutionState) -> dict:
    """
    Generates the final legal_notice or complaint document.
    """
    logger.info("Executing node: document_generation_node")
    result = _document_generation_agent.generate_document(
        document_type=state.get("document_type", "legal_notice"),
        complainant_name=state.get("complainant_name", "[COMPLAINANT NAME]"),
        respondent_name=state.get("respondent_name", "[RESPONDENT NAME]"),
        amount_involved=state.get("amount_involved", 0.0),
        facts=state.get("facts", ""),
        reliefs_sought=state.get("reliefs_sought", ""),
    )
    return {"document": result}


def build_resolution_graph() -> StateGraph:
    """
    Builds and returns the StateGraph for the resolution workflow.

    Flow:
      authority -> action_planning -> document_generation -> END

    This ordering ensures the generated document's "Relief Sought" and
    "Legal Basis" sections can (in future iterations) be cross-referenced
    against the freshly computed roadmap/authorities, while keeping each
    node independently invocable.
    """
    graph = StateGraph(ResolutionState)

    graph.add_node("authority", authority_node)
    graph.add_node("action_planning", action_planning_node)
    graph.add_node("document_generation", document_generation_node)

    graph.set_entry_point("authority")
    graph.add_edge("authority", "action_planning")
    graph.add_edge("action_planning", "document_generation")
    graph.add_edge("document_generation", END)

    return graph


def get_compiled_resolution_workflow():
    """Returns the compiled, runnable resolution workflow."""
    graph = build_resolution_graph()
    return graph.compile()


# Module-level compiled workflow instance, ready for import by API endpoints.
resolution_workflow = get_compiled_resolution_workflow()


def run_document_generation(payload: dict) -> dict:
    """
    Main entry point for the /api/v1/documents/generate endpoint.

    payload: dict matching the request schema:
        {
          "type": "complaint" | "legal_notice",
          "complaint_id": str | None,
          "inputs": {
            "complainant_name": str,
            "respondent_name": str,
            "amount_involved": float,
            "facts": str,
            "reliefs_sought": str
          }
        }

    Returns: dict matching the response schema:
        {
          "document_type": str,
          "content_markdown": str,
          "content_plain": str,
          "recommended_next_steps": [str, ...]
        }
    """
    inputs = payload.get("inputs", {})

    initial_state: ResolutionState = {
        "document_type": payload.get("type", "legal_notice"),
        "complainant_name": inputs.get("complainant_name", "[COMPLAINANT NAME]"),
        "respondent_name": inputs.get("respondent_name", "[RESPONDENT NAME]"),
        "amount_involved": float(inputs.get("amount_involved", 0.0)),
        "facts": inputs.get("facts", ""),
        "reliefs_sought": inputs.get("reliefs_sought", ""),
    }

    final_state = resolution_workflow.invoke(initial_state)
    document = final_state.get("document", {})

    return {
        "document_type": document.get("document_type", initial_state["document_type"]),
        "content_markdown": document.get("content_markdown", ""),
        "content_plain": document.get("content_plain", ""),
        "recommended_next_steps": document.get("recommended_next_steps", []),
    }


def run_resolution_refresh(payload: dict) -> dict:
    """
    Secondary entry point: refreshes roadmap + authorities + case_strength
    for an existing complaint context (used by case insights / resolution refresh).

    payload: dict that should include at minimum:
        {
          "intent": str,
          "category": str,
          "summary": str,
          "amount_involved": float,
          "rights": list[dict],
          "evidence_assessment": dict,
          "similar_cases": list[dict],
          "location": str | None
        }

    Returns: dict with keys: authorities, resolution_roadmap, case_strength
    """
    initial_state: ResolutionState = {
        "document_type": "legal_notice",
        "complainant_name": "[COMPLAINANT NAME]",
        "respondent_name": "[RESPONDENT NAME]",
        "amount_involved": float(payload.get("amount_involved", 0.0)),
        "facts": payload.get("summary", ""),
        "reliefs_sought": "Resolution as per identified consumer rights.",
        "intent": payload.get("intent"),
        "category": payload.get("category"),
        "summary": payload.get("summary"),
        "rights": payload.get("rights", []),
        "evidence_assessment": payload.get("evidence_assessment", {}),
        "similar_cases": payload.get("similar_cases", []),
        "location": payload.get("location"),
    }

    final_state = resolution_workflow.invoke(initial_state)

    return {
        "authorities": final_state.get("authorities", []),
        "resolution_roadmap": final_state.get("resolution_roadmap", {"steps": []}),
        "case_strength": final_state.get("case_strength", {}),
    }
