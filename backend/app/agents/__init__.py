# backend/app/agents/__init__.py

from app.agents.base_agent import BaseAgent
from app.agents.intent_agent import IntentAgent
from app.agents.legal_retrieval_agent import LegalRetrievalAgent
from app.agents.case_similarity_agent import CaseSimilarityAgent
from app.agents.rights_agent import RightsAgent
from app.agents.action_planning_agent import ActionPlanningAgent
from app.agents.document_generation_agent import DocumentGenerationAgent
from app.agents.evidence_agent import EvidenceAgent
from app.agents.authority_agent import AuthorityAgent

__all__ = [
    "BaseAgent",
    "IntentAgent",
    "LegalRetrievalAgent",
    "CaseSimilarityAgent",
    "RightsAgent",
    "ActionPlanningAgent",
    "DocumentGenerationAgent",
    "EvidenceAgent",
    "AuthorityAgent",
]
