"""Yonah — the conversational autonomous agent (framework upstream).

Loads its identity contract from personality.md (see that file for the
published refusal scope). The agent itself is a thin orchestrator: it
classifies user intent, calls the role guard, dispatches to one of the
seven tools, and returns the result wrapped in a provenance envelope.

This is the framework upstream. Vertical forks supply concrete tool
implementations via the override surface at `agent/yonah/tools/` and
override personality.md with vertical-specific voice.
"""
from pathlib import Path


class YonahAgent:
    """The named conversational agent — framework base class."""

    PERSONALITY_PATH = Path(__file__).parent / "personality.md"

    def __init__(self, *, llm, role_guard, tools: dict):
        self.llm = llm
        self.role_guard = role_guard
        self.tools = tools  # {tool_name: ToolImpl}
        self.system_prompt = self._load_personality()

    def _load_personality(self) -> str:
        return self.PERSONALITY_PATH.read_text(encoding="utf-8")

    def handle(self, *, user_role: str, user_msg: str, session_state: dict):
        """One turn: classify intent -> role-guard check -> tool dispatch."""
        # TODO: implement intent classification (LLM call)
        # TODO: invoke self.role_guard.check(user_role, intended_tool)
        # TODO: dispatch to self.tools[intended_tool]
        # TODO: wrap response in a provenance envelope and persist
        raise NotImplementedError
