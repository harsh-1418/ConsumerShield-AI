# backend/app/agents/document_generation_agent.py

from app.agents.base_agent import BaseAgent
from app.prompts.document_prompts import (
    LEGAL_NOTICE_SYSTEM_PROMPT,
    COMPLAINT_DRAFT_SYSTEM_PROMPT,
    DOCUMENT_FEW_SHOT_EXAMPLES,
    DOCUMENT_USER_TEMPLATE,
)


class DocumentGenerationAgent(BaseAgent):
    """
    Assembles legal notice / complaint draft markdown documents.

    Can be used in two ways:
      1. As part of the main analysis workflow (optional, lightweight legal_notice_preview)
      2. As a standalone agent invoked by the /api/v1/documents/generate endpoint

    Writes to state (when used standalone): document (dict matching document schema)
    """

    def __init__(self):
        super().__init__(temperature=0.3)

    def generate_document(
        self,
        document_type: str,
        complainant_name: str,
        respondent_name: str,
        amount_involved: float,
        facts: str,
        reliefs_sought: str,
    ) -> dict:
        """
        Standalone entry point for the document generation endpoint.

        document_type: "legal_notice" | "complaint"
        Returns dict matching:
        {
          "document_type": str,
          "content_markdown": str,
          "content_plain": str,
          "recommended_next_steps": [str, ...]
        }
        """
        self.logger.info("DocumentGenerationAgent generating type: %s", document_type)

        if document_type == "complaint":
            system_prompt = COMPLAINT_DRAFT_SYSTEM_PROMPT
        else:
            system_prompt = LEGAL_NOTICE_SYSTEM_PROMPT
            document_type = "legal_notice"

        user_message = DOCUMENT_USER_TEMPLATE.format(
            document_type=document_type,
            complainant_name=complainant_name,
            respondent_name=respondent_name,
            amount_involved=amount_involved,
            facts=facts,
            reliefs_sought=reliefs_sought,
        )

        try:
            result = self._invoke_and_parse(
                system_prompt=system_prompt,
                user_message=user_message,
                few_shot_examples=DOCUMENT_FEW_SHOT_EXAMPLES,
            )
        except Exception as e:
            self.logger.warning("DocumentGenerationAgent LLM failed (%s), using fallback template.", e)
            result = _fallback_document(
                document_type, complainant_name, respondent_name, amount_involved, facts, reliefs_sought
            )

        return {
            "document_type": result.get("document_type", document_type),
            "content_markdown": result.get("content_markdown", ""),
            "content_plain": result.get("content_plain", ""),
            "recommended_next_steps": result.get("recommended_next_steps", []),
        }

    def run(self, state: dict) -> dict:
        """
        Optional node for the LangGraph workflow: generates a short legal notice
        preview based on the complaint analysis so far. This is NOT the full
        /documents/generate response, but a lightweight preview embedded in the
        complaint analysis output if needed by the frontend.

        Reads from state: intent, summary, category, amount_involved, rights
        Writes to state: legal_notice_preview (dict)
        """
        self.logger.info("DocumentGenerationAgent generating legal notice preview.")

        rights_text = "; ".join(r.get("name", "") for r in state.get("rights", []))
        facts = state.get("summary", "")
        reliefs_sought = (
            f"Resolution of the {state.get('intent', 'issue')} including refund/compensation "
            f"of ₹{state.get('amount_involved', 0.0):,.2f} where applicable, "
            f"in line with: {rights_text}."
        )

        result = self.generate_document(
            document_type="legal_notice",
            complainant_name="[COMPLAINANT NAME]",
            respondent_name="[RESPONDENT NAME]",
            amount_involved=state.get("amount_involved", 0.0),
            facts=facts,
            reliefs_sought=reliefs_sought,
        )

        return {"legal_notice_preview": result}


def _fallback_document(
    document_type: str,
    complainant_name: str,
    respondent_name: str,
    amount_involved: float,
    facts: str,
    reliefs_sought: str,
) -> dict:
    """Static fallback template if the LLM call fails."""
    content_markdown = f"""## {'LEGAL NOTICE' if document_type == 'legal_notice' else 'CONSUMER COMPLAINT'}

**Date:** [DATE]

**From:** {complainant_name}
**To:** {respondent_name}

---

**FACTS OF THE CASE:**

{facts}

**RELIEF SOUGHT:**

{reliefs_sought}

Amount Involved: ₹{amount_involved:,.2f}

---

Yours sincerely,
**{complainant_name}**
"""
    content_plain = content_markdown.replace("##", "").replace("**", "").replace("---", "")

    return {
        "document_type": document_type,
        "content_markdown": content_markdown,
        "content_plain": content_plain,
        "recommended_next_steps": [
            "Review the document and fill in placeholder fields.",
            "Send via Registered Post with Acknowledgement Due.",
            "Retain proof of dispatch and delivery.",
        ],
    }
