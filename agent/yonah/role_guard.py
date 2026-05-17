"""Asymmetric refusal contract enforcement.

Reads personality.md at module load time and indexes the refusal rules by
(audience, tool). The check() method returns either ALLOW or REFUSE; every
REFUSE produces a PROV activity carrying the refusal reason.

Framework-level guard: roles are abstract ("authority" / "second_audience").
Vertical forks may subclass to alias their domain roles onto the abstract
ones (e.g. {"professor": "authority", "student": "second_audience"}) by
overriding `normalize_role`.
"""
from enum import Enum


class Decision(Enum):
    ALLOW = "allow"
    REFUSE = "refuse"


class RoleGuard:
    """Framework-default asymmetric refusal contract.

    Verticals subclass and override:
      - `normalize_role` to alias vertical-specific role names onto the
        abstract "authority" / "second_audience" axes.
    """

    AUTHORITY_TOOLS = {"build_artefact", "publish_artefact", "commit_decision"}
    SECOND_AUDIENCE_TOOLS = {"tutor_me", "submit_draft", "query_my_provenance"}
    UNIVERSAL_TOOLS = {"delete_my_data"}

    # Override hook: vertical forks alias their role names onto these.
    ROLE_ALIASES: dict[str, str] = {
        "authority": "authority",
        "second_audience": "second_audience",
    }

    def normalize_role(self, user_role: str) -> str:
        """Alias a vertical-specific role name onto the abstract axis.

        Override hook: vertical forks extend `ROLE_ALIASES` to map their
        domain vocabulary onto the framework's `authority` /
        `second_audience` axes.
        """
        return self.ROLE_ALIASES.get(user_role, user_role)

    def check(self, *, user_role: str, intended_tool: str) -> Decision:
        role = self.normalize_role(user_role)
        if intended_tool in self.UNIVERSAL_TOOLS:
            return Decision.ALLOW
        if role == "authority" and intended_tool in self.AUTHORITY_TOOLS:
            return Decision.ALLOW
        if role == "second_audience" and intended_tool in self.SECOND_AUDIENCE_TOOLS:
            return Decision.ALLOW
        return Decision.REFUSE

    def is_off_topic(self, user_msg: str) -> bool:
        """TODO: classifier for off-topic requests (returns capability summary)."""
        return False
