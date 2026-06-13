# backend/app/agents/action_planning_agent.py

import logging
from app.agents.base_agent import BaseAgent
from app.prompts.roadmap_prompts import (
    ROADMAP_SYSTEM_PROMPT,
    ROADMAP_FEW_SHOT_EXAMPLES,
    ROADMAP_USER_TEMPLATE,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Case Strength Interface – Member 3 owns backend/app/prediction/case_strength.py
# This hook attempts to use Member 3's scorer; falls back to a clean local
# heuristic so the workflow remains fully functional without Member 3's module.
# ---------------------------------------------------------------------------
def _compute_case_strength(state: dict) -> dict:
    """
    Returns dict matching the case_strength schema:
    {"score": float, "label": str, "reasons": [str, ...]}
    """
    try:
        from app.prediction.case_strength import compute_case_strength  # type: ignore
        return compute_case_strength(state)
    except ImportError:
        logger.warning("Prediction module not available — using local heuristic for case_strength.")
        return _heuristic_case_strength(state)


def _heuristic_case_strength(state: dict) -> dict:
    """
    Simple, explainable heuristic combining:
      - evidence strength (from EvidenceAgent)
      - number of rights identified
      - number of similar precedent cases with high similarity
      - amount involved (very high amounts slightly reduce confidence without strong evidence)
    """
    score = 0.5
    reasons = []

    evidence_assessment = state.get("evidence_assessment", {})
    evidence_strength = evidence_assessment.get("evidence_strength", "moderate")

    if evidence_strength == "strong":
        score += 0.2
        reasons.append("Strong documentary evidence supports the claim.")
    elif evidence_strength == "weak":
        score -= 0.15
        reasons.append("Evidence provided is weak; consider gathering more documentation.")
    else:
        score += 0.05
        reasons.append("Moderate evidence supports the claim.")

    rights = state.get("rights", [])
    if len(rights) >= 2:
        score += 0.15
        reasons.append(f"Multiple consumer rights ({len(rights)}) identified as applicable.")
    elif len(rights) == 1:
        score += 0.07
        reasons.append("One clear consumer right identified as applicable.")

    similar_cases = state.get("similar_cases", [])
    high_sim = [c for c in similar_cases if c.get("similarity_score", 0) >= 0.8]
    if high_sim:
        score += 0.1
        reasons.append(f"{len(high_sim)} similar precedent case(s) with high relevance found.")

    amount_involved = state.get("amount_involved", 0.0) or 0.0
    if amount_involved > 0:
        reasons.append(f"Claim amount of ₹{amount_involved:,.2f} is well within Consumer Commission jurisdictional limits.")

    score = max(0.0, min(1.0, round(score, 2)))

    if score >= 0.7:
        label = "Strong"
    elif score >= 0.45:
        label = "Moderate"
    else:
        label = "Weak"

    return {"score": score, "label": label, "reasons": reasons}


class ActionPlanningAgent(BaseAgent):
    """
    Generates the step-by-step resolution roadmap and computes case strength.

    Writes to state: resolution_roadmap (dict), case_strength (dict)
    """

    def __init__(self):
        super().__init__(temperature=0.2)

    def run(self, state: dict) -> dict:
        """
        Reads from state: intent, category, summary, amount_involved, rights,
                          authorities, evidence_assessment, similar_cases
        Writes to state: resolution_roadmap, case_strength
        """
        self.logger.info("ActionPlanningAgent running for intent: %s", state.get("intent", "unknown"))

        rights_summary = "; ".join(
            r.get("name", "") for r in state.get("rights", [])
        ) or "General consumer protection rights"

        authorities_summary = "; ".join(
            f"{a.get('name', '')} ({a.get('jurisdiction', '')})"
            for a in state.get("authorities", [])
        ) or "District Consumer Disputes Redressal Commission"

        user_message = ROADMAP_USER_TEMPLATE.format(
            intent=state.get("intent", ""),
            category=state.get("category", "others"),
            summary=state.get("summary", ""),
            amount_involved=state.get("amount_involved", 0.0),
            rights_summary=rights_summary,
            authorities_summary=authorities_summary,
        )

        try:
            result = self._invoke_and_parse(
                system_prompt=ROADMAP_SYSTEM_PROMPT,
                user_message=user_message,
                few_shot_examples=ROADMAP_FEW_SHOT_EXAMPLES,
            )
            steps = result.get("steps", [])
            if not steps:
                raise ValueError("Empty steps list from LLM")
        except Exception as e:
            self.logger.warning("ActionPlanningAgent LLM failed (%s), using default roadmap.", e)
            steps = _default_roadmap_steps(state)

        # Normalize and re-sequence step ordering
        normalized_steps = []
        for idx, step in enumerate(steps, start=1):
            normalized_steps.append({
                "order": idx,
                "title": step.get("title", f"Step {idx}"),
                "description": step.get("description", ""),
                "expected_time_days": int(step.get("expected_time_days", 7)),
            })

        resolution_roadmap = {"steps": normalized_steps}
        case_strength = _compute_case_strength(state)

        return {
            "resolution_roadmap": resolution_roadmap,
            "case_strength": case_strength,
        }


def _default_roadmap_steps(state: dict) -> list[dict]:
    """Fallback roadmap if the LLM call fails entirely."""
    authorities = state.get("authorities", [])
    primary_authority = authorities[0]["name"] if authorities else "the appropriate Consumer Commission"

    return [
        {
            "order": 1,
            "title": "Contact the Seller/Service Provider Directly",
            "description": "Send a written communication (email/support ticket) to the seller or service provider clearly describing the issue and the resolution you are seeking. Keep a copy for your records.",
            "expected_time_days": 3,
        },
        {
            "order": 2,
            "title": "Send a Formal Legal Notice",
            "description": "If the seller does not respond satisfactorily, send a formal legal notice citing the relevant consumer protection provisions and demanding resolution within 15 days.",
            "expected_time_days": 15,
        },
        {
            "order": 3,
            "title": "Register Complaint on National Consumer Helpline",
            "description": "File your complaint on the National Consumer Helpline (consumerhelpline.gov.in or call 1915) to create an official record and seek mediation assistance.",
            "expected_time_days": 7,
        },
        {
            "order": 4,
            "title": f"File a Formal Complaint with {primary_authority}",
            "description": f"If the issue remains unresolved, file a formal complaint with {primary_authority}, attaching all evidence, correspondence, and the legal notice copy.",
            "expected_time_days": 90,
        },
    ]
