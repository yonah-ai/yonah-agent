"""Smoke test of the role guard against the published personality.md.

Per the personality contract: the guard's AUTHORITY_TOOLS +
SECOND_AUDIENCE_TOOLS + UNIVERSAL_TOOLS must cover every tool mentioned
in personality.md, and no more.
"""
import re
from pathlib import Path

from agent.yonah.role_guard import RoleGuard


def test_guard_covers_personality_tools():
    md = Path("agent/yonah/personality.md").read_text(encoding="utf-8")
    # Tool names appear as `tool_name` in backticks in the markdown
    declared = set(re.findall(r"`([a-z_]+)`", md))
    guard_known = (
        RoleGuard.AUTHORITY_TOOLS
        | RoleGuard.SECOND_AUDIENCE_TOOLS
        | RoleGuard.UNIVERSAL_TOOLS
    )
    # Tools listed in personality.md MUST all be in the guard
    overlap = declared & guard_known
    assert overlap == guard_known, (
        f"personality.md mentions tools not enforced by RoleGuard: "
        f"{guard_known - overlap}"
    )


def test_guard_allows_authority_for_authority_tools():
    g = RoleGuard()
    from agent.yonah.role_guard import Decision
    assert g.check(user_role="authority", intended_tool="build_artefact") == Decision.ALLOW
    assert g.check(user_role="second_audience", intended_tool="build_artefact") == Decision.REFUSE


def test_guard_universal_always_allows():
    g = RoleGuard()
    from agent.yonah.role_guard import Decision
    assert g.check(user_role="authority", intended_tool="delete_my_data") == Decision.ALLOW
    assert g.check(user_role="second_audience", intended_tool="delete_my_data") == Decision.ALLOW
