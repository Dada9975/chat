import openai
from typing import List, Dict


class LLMClient:
    """Wrapper around an LLM API (e.g., OpenAI)."""

    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        openai.api_key = api_key
        self.model = model

    def generate_reply(self, conversation: List[Dict[str, str]]) -> str:
        """Return the assistant's reply given the conversation history."""
        response = openai.ChatCompletion.create(model=self.model, messages=conversation)
        return response["choices"][0]["message"]["content"].strip()
