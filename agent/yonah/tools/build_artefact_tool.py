"""build_artefact tool — authority-audience side (framework base class).

API contract (vertical-invariant):

    Input fields:
        artefact_type: str   # vertical taxonomy of artefact shapes
        criteria: list       # criterion-level structure of the artefact
        metadata: dict       # vertical-specific metadata

    Output fields:
        artefact_id: str     # ULID for the new artefact
        artefact_version: str
        envelope_hash: str   # content-hash of the build envelope

    Contract semantics:
        - Produces a `wasGeneratedBy` PROV activity attributed to the
          authority audience.
        - Emits a content-hashed signed envelope persisted to the
          provenance graph BEFORE returning the artefact_id.
        - Refuses if the caller's role does not normalise to "authority".

Override hooks (verticals override exactly these):
    - input-schema override: bind `criteria` to the vertical's concrete
      artefact schema (Rubric / CareProtocol / JobCriteria / ...).
    - output-schema override: extend output envelope with vertical-specific
      fields if needed (rare).
    - regulatory-mapping override: declare which regulation articles this
      tool discharges in the vertical's regulatory map.

Reference education implementation: yonah-edu-agent.
"""
from abc import ABC, abstractmethod


class BuildArtefactTool(ABC):
    """Framework base class for the build_artefact tool. Audience: authority."""

    tool_name = "build_artefact"
    audience = "authority"

    # Override hook: vertical declares its concrete input schema.
    input_schema = None  # vertical Pydantic model

    # Override hook: vertical declares its concrete output schema.
    output_schema = None  # vertical Pydantic model

    # Override hook: vertical regulatory mapping, e.g. ["eu_ai_act.art_13"].
    regulatory_anchors: list[str] = []

    @abstractmethod
    def run(self, **kwargs):
        """Build a shared-contract artefact.

        Verticals override this with their domain-specific implementation.
        See yonah-edu-agent for the education reference.
        """
        raise NotImplementedError(
            "Verticals override this with their domain-specific implementation. "
            "See yonah-edu-agent for the education reference."
        )
