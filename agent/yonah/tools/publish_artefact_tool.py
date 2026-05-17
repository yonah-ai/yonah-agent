"""publish_artefact tool — authority-audience side (framework base class).

API contract (vertical-invariant):

    Input fields:
        artefact_id: str
        artefact_version: str
        cohort_id: str       # identifier of the bound second-audience cohort

    Output fields:
        publication_id: str  # ULID for the publication event
        envelope_hash: str   # content-hash of the publication envelope

    Contract semantics:
        - Locks the artefact at the given version; further edits require
          a new build_artefact call producing a new version.
        - Bounds the artefact to a named second-audience cohort.
        - Emits a `wasInformedBy` PROV activity linking publication to
          the prior build envelope.
        - Refuses if the caller's role does not normalise to "authority"
          or if the artefact is already published at the given version.

Override hooks (verticals override exactly these):
    - input-schema override: bind `cohort_id` to the vertical's grouping
      concept (class / case-cohort / req / ...).
    - output-schema override: extend with vertical-specific bookkeeping.
    - regulatory-mapping override: declare which articles this discharges.

Reference education implementation: yonah-edu-agent.
"""
from abc import ABC, abstractmethod


class PublishArtefactTool(ABC):
    """Framework base class for the publish_artefact tool. Audience: authority."""

    tool_name = "publish_artefact"
    audience = "authority"

    input_schema = None  # Override hook
    output_schema = None  # Override hook
    regulatory_anchors: list[str] = []  # Override hook

    @abstractmethod
    def run(self, **kwargs):
        """Publish a shared-contract artefact to a bound cohort.

        Verticals override this with their domain-specific implementation.
        See yonah-edu-agent for the education reference.
        """
        raise NotImplementedError(
            "Verticals override this with their domain-specific implementation. "
            "See yonah-edu-agent for the education reference."
        )
