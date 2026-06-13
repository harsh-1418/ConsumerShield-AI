# backend/app/agents/base_agent.py

import os
import json
import logging
from abc import ABC, abstractmethod
from typing import Any

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

logger = logging.getLogger(__name__)

GEMINI_MODEL = "gemini-2.5-flash"


def get_llm(temperature: float = 0.2) -> ChatGoogleGenerativeAI:
    """Initialize and return a Gemini 2.5 Flash LLM instance."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError("GEMINI_API_KEY environment variable is not set.")
    return ChatGoogleGenerativeAI(
        model=GEMINI_MODEL,
        google_api_key=api_key,
        temperature=temperature,
        convert_system_message_to_human=False,
    )


def safe_parse_json(raw: str) -> dict:
    """Safely parse JSON from an LLM response, stripping markdown fences if present."""
    text = raw.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        # Remove opening fence (```json or ```)
        lines = lines[1:] if lines[0].startswith("```") else lines
        # Remove closing fence
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        logger.error("JSON parse error: %s | Raw text: %s", e, raw[:300])
        raise ValueError(f"Agent returned invalid JSON: {e}") from e


class BaseAgent(ABC):
    """
    Abstract base class for all ConsumerShield agents.
    All agents must implement the `run` method and return a dict.
    """

    def __init__(self, temperature: float = 0.2):
        self.llm = get_llm(temperature=temperature)
        self.logger = logging.getLogger(self.__class__.__name__)

    def _invoke(
        self,
        system_prompt: str,
        user_message: str,
        few_shot_examples: list[dict] | None = None,
    ) -> str:
        """
        Build the message list and call the LLM.
        Returns the raw string content of the model's response.
        """
        messages: list = [SystemMessage(content=system_prompt)]

        if few_shot_examples:
            for example in few_shot_examples:
                if example["role"] == "user":
                    messages.append(HumanMessage(content=example["content"]))
                elif example["role"] == "assistant":
                    messages.append(AIMessage(content=example["content"]))

        messages.append(HumanMessage(content=user_message))

        self.logger.debug("Invoking LLM with %d messages", len(messages))
        response = self.llm.invoke(messages)
        return response.content

    def _invoke_and_parse(
        self,
        system_prompt: str,
        user_message: str,
        few_shot_examples: list[dict] | None = None,
    ) -> dict:
        """Invoke the LLM and parse the JSON response."""
        raw = self._invoke(system_prompt, user_message, few_shot_examples)
        return safe_parse_json(raw)

    @abstractmethod
    def run(self, state: dict) -> dict:
        """
        Execute the agent's task given the current workflow state.
        Must return a dict with the keys this agent is responsible for updating.
        """
        ...
