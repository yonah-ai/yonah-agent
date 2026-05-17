"""Gemini provider — implements the LLMProvider Protocol."""
from .provider_adapter import LLMProvider


class GeminiProvider:
    """TODO: implement complete() against the gemini SDK; capture cost+latency."""

    def __init__(self, api_key: str):
        self.api_key = api_key

    def complete(self, prompt: str, **kwargs) -> str:
        raise NotImplementedError
