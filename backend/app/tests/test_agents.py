# backend/app/tests/test_agents.py

"""
Unit tests for Member 1's agents and workflows.

These tests focus on schema correctness and deterministic fallback logic
(mock RAG, mock case similarity, default authorities, heuristic case strength,
default roadmap). They do NOT require a live GEMINI_API_KEY for the
non-LLM code paths tested here.

LLM-dependent tests (marked with @pytest.mark.llm) require GEMINI_API_KEY
to be set and will make real API calls — run separately with:
    pytest -m llm
"""

import os
import pytest

os.environ.setdefault("GEMINI_API_KEY", "test_dummy_key_for_init_only")

from app.agents.legal_retrieval_agent import _mock_legal_results, LegalRetrievalAgent
from app.agents.case_similarity_agent import _mock_similar_cases, CaseSimilarityAgent
from app.agents.authority_agent import _DEFAULT_AUTHORITIES, AuthorityAgent
from app.agents.action_planning_agent import (
    _heuristic_case_strength,
    _default_roadmap_steps,
    ActionPlanningAgent,
)
from app.agents.evidence_agent import EvidenceAgent
from app.agents.intent_agent import IntentAgent
from app.agents.rights_agent import RightsAgent
from app.agents.document_generation_agent import DocumentGenerationAgent, _fallback_document
from app.workflows.complaint_analysis_flow import (
    build_complaint_analysis_graph,
    get_compiled_complaint_analysis_workflow,
)
from app.workflows.resolution_flow import (
    build_resolution_graph,
    get_compiled_resolution_workflow,
)


# ---------------------------------------------------------------------------
# Agent instantiation tests (verify Gemini client initializes without error)
# ---------------------------------------------------------------------------

def test_all_agents_instantiate():
    assert IntentAgent() is not None
    assert LegalRetrievalAgent() is not None
    assert CaseSimilarityAgent() is not None
    assert RightsAgent() is not None
    assert EvidenceAgent() is not None
    assert AuthorityAgent() is not None
    assert ActionPlanningAgent() is not None
    assert DocumentGenerationAgent() is not None


# ---------------------------------------------------------------------------
# Mock RAG retrieval fallback
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("query,expected_min", [
    ("refund ecommerce defective product", 1),
    ("bank emi double charge", 1),
    ("telecom mobile network disconnection", 1),
    ("insurance claim rejected irdai", 1),
    ("something completely unrelated", 1),
])
def test_mock_legal_results_non_empty(query, expected_min):
    results = _mock_legal_results(query)
    assert len(results) >= expected_min
    for r in results:
        assert set(["id", "title", "section", "snippet", "score", "source_url"]).issubset(r.keys())


# ---------------------------------------------------------------------------
# Mock case similarity fallback
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("category", ["ecommerce", "banking", "telecom", "insurance", "real_estate", "others", "unknown_cat"])
def test_mock_similar_cases_schema(category):
    results = _mock_similar_cases(category)
    assert len(results) >= 1
    for r in results:
        assert "case_id" in r
        assert "title" in r
        assert "similarity_score" in r
        assert 0.0 <= r["similarity_score"] <= 1.0


# ---------------------------------------------------------------------------
# Default authorities fallback
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("category", ["ecommerce", "banking", "telecom", "insurance", "others"])
def test_default_authorities_schema(category):
    authorities = _DEFAULT_AUTHORITIES[category]
    assert len(authorities) >= 1
    for a in authorities:
        assert "name" in a
        assert "jurisdiction" in a
        assert "contact" in a
        assert set(["email", "phone", "website"]).issubset(a["contact"].keys())


# ---------------------------------------------------------------------------
# Heuristic case strength
# ---------------------------------------------------------------------------

def test_heuristic_case_strength_strong_case():
    state = {
        "amount_involved": 65000.0,
        "evidence_assessment": {"evidence_strength": "strong"},
        "rights": [{"name": "Right A"}, {"name": "Right B"}],
        "similar_cases": [{"similarity_score": 0.86}],
    }
    result = _heuristic_case_strength(state)
    assert 0.0 <= result["score"] <= 1.0
    assert result["label"] in ("Strong", "Moderate", "Weak")
    assert result["score"] >= 0.7
    assert result["label"] == "Strong"
    assert len(result["reasons"]) >= 1


def test_heuristic_case_strength_weak_case():
    state = {
        "amount_involved": 0.0,
        "evidence_assessment": {"evidence_strength": "weak"},
        "rights": [],
        "similar_cases": [],
    }
    result = _heuristic_case_strength(state)
    assert result["label"] in ("Strong", "Moderate", "Weak")
    assert result["score"] <= 0.45


# ---------------------------------------------------------------------------
# Default roadmap fallback
# ---------------------------------------------------------------------------

def test_default_roadmap_steps_schema():
    steps = _default_roadmap_steps({"authorities": [{"name": "DCDRC Hyderabad"}]})
    assert len(steps) == 4
    for i, step in enumerate(steps, start=1):
        assert step["order"] == i
        assert "title" in step
        assert "description" in step
        assert isinstance(step["expected_time_days"], int)
        assert step["expected_time_days"] > 0


def test_default_roadmap_steps_no_authorities():
    steps = _default_roadmap_steps({"authorities": []})
    assert len(steps) == 4
    assert "appropriate Consumer Commission" in steps[-1]["title"] or "Consumer Commission" in steps[-1]["title"]


# ---------------------------------------------------------------------------
# Document fallback template
# ---------------------------------------------------------------------------

def test_fallback_document_legal_notice():
    doc = _fallback_document(
        document_type="legal_notice",
        complainant_name="Ravi Kumar",
        respondent_name="Flipkart Internet Private Limited",
        amount_involved=65000.0,
        facts="Laptop arrived damaged.",
        reliefs_sought="Full refund of amount.",
    )
    assert doc["document_type"] == "legal_notice"
    assert "Ravi Kumar" in doc["content_markdown"]
    assert "65,000.00" in doc["content_markdown"]
    assert len(doc["recommended_next_steps"]) >= 1


# ---------------------------------------------------------------------------
# Workflow graph structure tests
# ---------------------------------------------------------------------------

def test_complaint_analysis_graph_structure():
    graph = build_complaint_analysis_graph()
    compiled = graph.compile()
    nodes = set(compiled.get_graph().nodes.keys())
    expected_nodes = {
        "__start__", "intent", "legal_retrieval", "case_similarity",
        "evidence", "rights", "authority", "action_planning", "__end__",
    }
    assert expected_nodes.issubset(nodes)


def test_resolution_graph_structure():
    graph = build_resolution_graph()
    compiled = graph.compile()
    nodes = set(compiled.get_graph().nodes.keys())
    expected_nodes = {"__start__", "authority", "action_planning", "document_generation", "__end__"}
    assert expected_nodes.issubset(nodes)


def test_workflows_compile_without_error():
    assert get_compiled_complaint_analysis_workflow() is not None
    assert get_compiled_resolution_workflow() is not None


# ---------------------------------------------------------------------------
# LLM-dependent integration tests (require real GEMINI_API_KEY)
# ---------------------------------------------------------------------------

@pytest.mark.llm
def test_full_complaint_analysis_pipeline():
    from app.workflows.complaint_analysis_flow import run_complaint_analysis

    payload = {
        "user_id": None,
        "title": "Flipkart refused refund on broken laptop",
        "description": (
            "I ordered a laptop from Flipkart on 12th March 2024. It arrived with a cracked screen. "
            "I raised a return request within 24 hours but they rejected it saying the damage was user-caused. "
            "I have unboxing video proof."
        ),
        "category": "ecommerce",
        "amount_involved": 65000.0,
        "evidence_texts": [
            "Unboxing video showing cracked screen on delivery",
            "Email from Flipkart support rejecting return request",
        ],
    }

    result = run_complaint_analysis(payload)

    required_keys = {
        "intent", "summary", "rights", "relevant_laws", "similar_cases",
        "case_strength", "authorities", "resolution_roadmap",
    }
    assert required_keys.issubset(result.keys())
    assert result["intent"] != ""
    assert isinstance(result["rights"], list)
    assert isinstance(result["resolution_roadmap"].get("steps"), list)


@pytest.mark.llm
def test_document_generation_endpoint():
    from app.workflows.resolution_flow import run_document_generation

    payload = {
        "type": "legal_notice",
        "complaint_id": None,
        "inputs": {
            "complainant_name": "Ravi Kumar",
            "respondent_name": "Flipkart Internet Private Limited",
            "amount_involved": 65000.0,
            "facts": "Laptop arrived with a cracked screen; return request rejected.",
            "reliefs_sought": "Full refund of ₹65,000 and compensation of ₹10,000.",
        },
    }

    result = run_document_generation(payload)
    assert result["document_type"] == "legal_notice"
    assert "content_markdown" in result
    assert len(result["content_markdown"]) > 0
    assert isinstance(result["recommended_next_steps"], list)
