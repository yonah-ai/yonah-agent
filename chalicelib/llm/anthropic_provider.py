"""Anthropic provider — implements the LLMProvider Protocol."""
from .provider_adapter import LLMProvider


class AnthropicProvider:
    """TODO: implement complete() against the anthropic SDK; capture cost+latency."""

    def __init__(self, api_key: str):
        self.api_key = api_key

    def complete(self, prompt: str, **kwargs) -> str:
        raise NotImplementedError
