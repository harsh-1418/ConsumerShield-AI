# backend/app/agents/evidence_agent.py

from app.agents.base_agent import BaseAgent

EVIDENCE_SYSTEM_PROMPT = """You are an evidence-review assistant for Indian consumer complaints.
Given a list of textual evidence descriptions provided by the consumer, your task is to:
1. Assess the overall strength of the evidence (strong, moderate, weak)
2. Identify what types of evidence are present (e.g., receipts, screenshots, emails, videos, chat logs)
3. Identify gaps - what additional evidence would strengthen the case

GUARDRAILS:
- Return ONLY valid JSON.
- Do NOT make legal conclusions, only assess evidentiary completeness.
- Base assessment strictly on the text descriptions provided; do not assume content not stated.
- If evidence_texts is empty, set evidence_strength to "weak" and recommend documentation steps.

OUTPUT FORMAT (strict JSON):
{
  "evidence_strength": "strong | moderate | weak",
  "evidence_types_identified": ["<type1>", "<type2>"],
  "evidence_gaps": ["<gap1>", "<gap2>"],
  "evidence_reasons": ["<short reason 1>", "<short reason 2>"]
}
"""

EVIDENCE_USER_TEMPLATE = """Review the following evidence provided for a consumer complaint:

Complaint Summary: {summary}
Category: {category}
Evidence Texts:
{evidence_list}

Return ONLY valid JSON in the required format."""


class EvidenceAgent(BaseAgent):
    """
    Reviews attached textual evidence and produces a strength assessment
    used downstream by the CaseStrengthAgent logic (folded into this agent's
    output for case_strength reasons) and the ActionPlanningAgent.

    Writes to state: evidence_assessment (dict)
    """

    def __init__(self):
        super().__init__(temperature=0.1)

    def run(self, state: dict) -> dict:
        """
        Reads from state: summary, category, evidence_texts
        Writes to state: evidence_assessment
        """
        self.logger.info("EvidenceAgent running with %d evidence items", len(state.get("evidence_texts", [])))

        evidence_texts = state.get("evidence_texts", [])
        if evidence_texts:
            evidence_list = "\n".join(f"- {e}" for e in evidence_texts)
        else:
            evidence_list = "(No evidence provided by the consumer)"

        user_message = EVIDENCE_USER_TEMPLATE.format(
            summary=state.get("summary", ""),
            category=state.get("category", "others"),
            evidence_list=evidence_list,
        )

        try:
            result = self._invoke_and_parse(
                system_prompt=EVIDENCE_SYSTEM_PROMPT,
                user_message=user_message,
            )
        except Exception as e:
            self.logger.warning("EvidenceAgent LLM failed (%s), using default assessment.", e)
            result = {
                "evidence_strength": "weak" if not evidence_texts else "moderate",
                "evidence_types_identified": [],
                "evidence_gaps": ["Unable to automatically assess evidence; manual review recommended."],
                "evidence_reasons": [],
            }

        evidence_assessment = {
            "evidence_strength": result.get("evidence_strength", "moderate"),
            "evidence_types_identified": result.get("evidence_types_identified", []),
            "evidence_gaps": result.get("evidence_gaps", []),
            "evidence_reasons": result.get("evidence_reasons", []),
        }

        return {"evidence_assessment": evidence_assessment}
