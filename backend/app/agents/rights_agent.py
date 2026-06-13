# backend/app/agents/rights_agent.py

from app.agents.base_agent import BaseAgent
from app.prompts.rights_prompts import (
    RIGHTS_SYSTEM_PROMPT,
    RIGHTS_FEW_SHOT_EXAMPLES,
    RIGHTS_USER_TEMPLATE,
)


class RightsAgent(BaseAgent):
    """
    Maps the complaint to specific Indian consumer rights violations,
    citing relevant legal provisions retrieved by the LegalRetrievalAgent.

    Writes to state: rights (list)
    """

    def __init__(self):
        super().__init__(temperature=0.2)

    def run(self, state: dict) -> dict:
        """
        Reads from state: intent, category, summary, amount_involved, rag_context
        Writes to state: rights
        """
        self.logger.info("RightsAgent running for intent: %s", state.get("intent", "unknown"))

        rag_context = state.get("rag_context", "") or "No specific legal context retrieved."

        user_message = RIGHTS_USER_TEMPLATE.format(
            intent=state.get("intent", ""),
            category=state.get("category", "others"),
            summary=state.get("summary", ""),
            amount_involved=state.get("amount_involved", 0.0),
            rag_context=rag_context,
        )

        result = self._invoke_and_parse(
            system_prompt=RIGHTS_SYSTEM_PROMPT,
            user_message=user_message,
            few_shot_examples=RIGHTS_FEW_SHOT_EXAMPLES,
        )

        rights = result.get("rights", [])

        # Defensive normalization to guarantee schema compliance
        normalized_rights = []
        for r in rights:
            normalized_rights.append({
                "name": r.get("name", "Consumer Right"),
                "description": r.get("description", ""),
                "law_refs": [
                    {
                        "section": ref.get("section", ""),
                        "snippet": ref.get("snippet", ""),
                    }
                    for ref in r.get("law_refs", [])
                ],
            })

        return {"rights": normalized_rights}
