"""submit_draft tool — second-audience side (framework base class).

API contract (vertical-invariant):

    Input fields:
        artefact_id: str           # active artefact version to evaluate against
        draft: bytes | str         # the second-audience party's submitted work

    Output fields:
        decision_id: str           # ULID for the new in-flight decision
        envelope_hash: str         # content-hash of the submission envelope

    Contract semantics:
        - Runs the personally identifiable information (PII) detacher
          across the draft before any LLM call; persists a KMS-wrapped
          mapping in PiiTokenDao.
        - Emits a `wasGeneratedBy` activity attributed to the second
          audience, with the PII detacher's tokenisation as an
          intermediate `wasInformedBy`.
        - The downstream EvaluatorCrew is invoked by the SQS worker, not
          inline; this tool only enqueues.

Override hooks (verticals override exactly these):
    - input-schema override: bind `draft` to the vertical's concrete
      submission shape (essay / case-study / application packet / ...).
    - output-schema override: rare.
    - regulatory-mapping override: declare which articles this discharges.

Reference education implementation: yonah-edu-agent.
"""
from abc import ABC, abstractmethod


class SubmitDraftTool(ABC):
    """Framework base class for the submit_draft tool. Audience: second_audience."""

    tool_name = "submit_draft"
    audience = "second_audience"

    input_schema = None  # Override hook
    output_schema = None  # Override hook
    regulatory_anchors: list[str] = []  # Override hook

    @abstractmethod
    def run(self, **kwargs):
        """Submit a draft for identity-blind evaluation.

        Verticals override this with their domain-specific implementation.
        See yonah-edu-agent for the education reference.
        """
        raise NotImplementedError(
            "Verticals override this with their domain-specific implementation. "
            "See yonah-edu-agent for the education reference."
        )
