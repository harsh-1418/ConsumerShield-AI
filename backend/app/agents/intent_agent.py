# backend/app/agents/intent_agent.py

from app.agents.base_agent import BaseAgent
from app.prompts.intent_prompts import (
    INTENT_SYSTEM_PROMPT,
    INTENT_FEW_SHOT_EXAMPLES,
    INTENT_USER_TEMPLATE,
)


class IntentAgent(BaseAgent):
    """
    Parses the raw complaint and produces:
      - intent: snake_case label of the core issue
      - summary: one-paragraph neutral summary of the complaint
    """

    def __init__(self):
        super().__init__(temperature=0.1)

    def run(self, state: dict) -> dict:
        """
        Reads from state: title, description, category, amount_involved, evidence_texts
        Writes to state: intent, summary
        """
        self.logger.info("IntentAgent running for title: %s", state.get("title", "N/A"))

        evidence_str = "; ".join(state.get("evidence_texts", [])) or "No evidence provided."

        user_message = INTENT_USER_TEMPLATE.format(
            title=state.get("title", ""),
            description=state.get("description", ""),
            category=state.get("category", "others"),
            amount_involved=state.get("amount_involved", 0.0),
            evidence_texts=evidence_str,
        )

        result = self._invoke_and_parse(
            system_prompt=INTENT_SYSTEM_PROMPT,
            user_message=user_message,
            few_shot_examples=INTENT_FEW_SHOT_EXAMPLES,
        )

        return {
            "intent": result.get("intent", "out_of_scope"),
            "summary": result.get("summary", ""),
        }
