"""commit_decision tool — authority-audience side (framework base class).

API contract (vertical-invariant):

    Input fields:
        decision_id: str           # the in-flight decision from submit_draft
        verdict: dict              # vertical-specific outcome shape
        rationale: str             # authority's stated reason for the commit
        override_flags: dict       # if structural verifier failed, named overrides

    Output fields:
        committed_decision_id: str # ULID for the committed decision
        envelope_hash: str         # content-hash of the commit envelope

    Contract semantics:
        - Requires that the authority has accessed (`used`) the artefact,
          the submission, the criterion-level scores, and the evidence
          spans BEFORE this call — enforced via PROV graph queries against
          the same session.
        - If a structural verifier failed on the in-flight decision, the
          commit MUST carry an override_flag for that verifier with the
          authority's stated reason; otherwise the commit is refused.
        - Emits a `wasGeneratedBy` PROV activity attributed to the
          authority; the verdict is the committed decision.

Override hooks (verticals override exactly these):
    - input-schema override: bind `verdict` to the vertical's concrete
      decision shape (grade / treatment / hire-decision / ...).
    - output-schema override: extend with vertical-specific bookkeeping.
    - regulatory-mapping override: declare which articles this discharges.

Reference education implementation: yonah-edu-agent.
"""
from abc import ABC, abstractmethod


class CommitDecisionTool(ABC):
    """Framework base class for the commit_decision tool. Audience: authority."""

    tool_name = "commit_decision"
    audience = "authority"

    input_schema = None  # Override hook
    output_schema = None  # Override hook
    regulatory_anchors: list[str] = []  # Override hook

    @abstractmethod
    def run(self, **kwargs):
        """Commit a final decision against an in-flight evaluation.

        Verticals override this with their domain-specific implementation.
        See yonah-edu-agent for the education reference.
        """
        raise NotImplementedError(
            "Verticals override this with their domain-specific implementation. "
            "See yonah-edu-agent for the education reference."
        )
