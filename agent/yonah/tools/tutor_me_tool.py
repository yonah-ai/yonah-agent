"""tutor_me tool — second-audience side (framework base class).

API contract (vertical-invariant):

    Input fields:
        artefact_id: str           # currently active shared-contract artefact
        session_state: dict        # multi-turn conversational state
        message: str               # the second-audience party's turn

    Output fields:
        reply: str                 # the agent's tutoring turn
        session_state: dict        # updated multi-turn state
        envelope_hash: str         # content-hash of the turn envelope

    Contract semantics:
        - Grounds every hint in the artefact at the named version.
        - Never surfaces identifying information about any other
          second-audience party.
        - Emits a `wasInformedBy` PROV activity per turn linking to the
          active artefact's publication envelope.
        - Refuses if the caller's role does not normalise to "second_audience"
          or if no published artefact is bound to the caller's cohort.

Override hooks (verticals override exactly these):
    - input-schema override: extend `session_state` with vertical
      affordances.
    - output-schema override: rare.
    - regulatory-mapping override: declare which articles this discharges.

Reference education implementation: yonah-edu-agent.
"""
from abc import ABC, abstractmethod


class TutorMeTool(ABC):
    """Framework base class for the tutor_me tool. Audience: second_audience."""

    tool_name = "tutor_me"
    audience = "second_audience"

    input_schema = None  # Override hook
    output_schema = None  # Override hook
    regulatory_anchors: list[str] = []  # Override hook

    @abstractmethod
    def run(self, **kwargs):
        """Run one formative turn against the active artefact.

        Verticals override this with their domain-specific implementation.
        See yonah-edu-agent for the education reference.
        """
        raise NotImplementedError(
            "Verticals override this with their domain-specific implementation. "
            "See yonah-edu-agent for the education reference."
        )
