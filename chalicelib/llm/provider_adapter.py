"""Multi-provider LLM adapter (framework-canonical).

Discriminates by user-supplied key prefix:
  - sk-ant-*    → Anthropic provider
  - sk-*        → OpenAI provider
  - AIza*       → Google Gemini provider

Per-call cost + latency are captured into envelope metadata so the
record-keeping and robustness obligations under the regulation have
the underlying data they need at audit time. See the framework paper §5.
"""
from typing import Protocol


class LLMProvider(Protocol):
    """CrewAI-compatible BaseLLM-ish surface."""

    def complete(self, prompt: str, **kwargs) -> str: ...

    @classmethod
    def from_user_key(cls, key: str) -> "LLMProvider":
        """Route by key prefix — see module docstring."""
        # TODO: implement prefix dispatch
        raise NotImplementedError
