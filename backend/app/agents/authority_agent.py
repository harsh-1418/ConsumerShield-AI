# backend/app/agents/authority_agent.py

from app.agents.base_agent import BaseAgent
from app.prompts.roadmap_prompts import (
    AUTHORITY_SYSTEM_PROMPT,
    AUTHORITY_USER_TEMPLATE,
)


# Default authority fallback per category (used if LLM output is malformed)
_DEFAULT_AUTHORITIES = {
    "ecommerce": [
        {
            "name": "District Consumer Disputes Redressal Commission",
            "jurisdiction": "Hyderabad",
            "contact": {
                "email": None,
                "phone": "1915",
                "website": "https://consumerhelpline.gov.in",
            },
        },
    ],
    "banking": [
        {
            "name": "RBI Banking Ombudsman",
            "jurisdiction": "Hyderabad",
            "contact": {
                "email": None,
                "phone": None,
                "website": "https://cms.rbi.org.in",
            },
        },
    ],
    "telecom": [
        {
            "name": "TRAI - Telecom Regulatory Authority of India",
            "jurisdiction": "National",
            "contact": {
                "email": None,
                "phone": "1800-110-420",
                "website": "https://trai.gov.in",
            },
        },
    ],
    "insurance": [
        {
            "name": "IRDAI Grievance Cell",
            "jurisdiction": "National",
            "contact": {
                "email": None,
                "phone": "155255",
                "website": "https://igms.irda.gov.in",
            },
        },
    ],
    "others": [
        {
            "name": "District Consumer Disputes Redressal Commission",
            "jurisdiction": "Hyderabad",
            "contact": {
                "email": None,
                "phone": "1915",
                "website": "https://consumerhelpline.gov.in",
            },
        },
    ],
}


class AuthorityAgent(BaseAgent):
    """
    Determines the correct legal jurisdiction(s)/authorities the consumer
    should approach for redressal.

    Writes to state: authorities (list)
    """

    def __init__(self):
        super().__init__(temperature=0.1)

    def run(self, state: dict) -> dict:
        """
        Reads from state: intent, category, amount_involved, location (optional)
        Writes to state: authorities
        """
        self.logger.info("AuthorityAgent running for category: %s", state.get("category", "others"))

        user_message = AUTHORITY_USER_TEMPLATE.format(
            intent=state.get("intent", ""),
            category=state.get("category", "others"),
            amount_involved=state.get("amount_involved", 0.0),
            location=state.get("location", "Hyderabad, Telangana"),
        )

        try:
            result = self._invoke_and_parse(
                system_prompt=AUTHORITY_SYSTEM_PROMPT,
                user_message=user_message,
            )
            authorities = result.get("authorities", [])
            if not authorities:
                raise ValueError("Empty authorities list")
        except Exception as e:
            self.logger.warning("AuthorityAgent LLM failed (%s), using default fallback.", e)
            category = state.get("category", "others")
            authorities = _DEFAULT_AUTHORITIES.get(category, _DEFAULT_AUTHORITIES["others"])

        # Normalize schema
        normalized = []
        for a in authorities:
            contact = a.get("contact", {}) or {}
            normalized.append({
                "name": a.get("name", "Consumer Affairs Department"),
                "jurisdiction": a.get("jurisdiction", "Hyderabad"),
                "contact": {
                    "email": contact.get("email"),
                    "phone": contact.get("phone"),
                    "website": contact.get("website", "https://consumerhelpline.gov.in"),
                },
            })

        return {"authorities": normalized}
