"""OpenAI provider — implements the LLMProvider Protocol."""
from .provider_adapter import LLMProvider


class OpenaiProvider:
    """TODO: implement complete() against the openai SDK; capture cost+latency."""

    def __init__(self, api_key: str):
        self.api_key = api_key

    def complete(self, prompt: str, **kwargs) -> str:
        raise NotImplementedError
