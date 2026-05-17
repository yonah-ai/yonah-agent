"""query_my_provenance tool — second-audience side (framework base class).

API contract (vertical-invariant):

    Input fields:
        decision_id: str           # a committed decision the caller is bound to

    Output fields:
        provenance_graph: dict     # PROV-O subgraph for this decision
        envelope_chain: list       # ordered envelope hashes
        artefact_versions: list    # artefact(s) referenced at decision time

    Contract semantics:
        - The caller may query only decisions where the second-audience
          party identity in PiiTokenDao matches the caller's session
          identity; everything else is refused.
        - Returns the full PROV-O subgraph + the envelope chain;
          structural verifier outputs are included verbatim.
        - Discharges the caller's right of recourse where the regulation
          provides one (vertical specifies exact article in
          `regulatory_anchors`).

Override hooks (verticals override exactly these):
    - input-schema override: rare; identifier surfaces are framework-invariant.
    - output-schema override: extend with vertical-specific projections of
      the provenance graph (e.g. patient-facing summary; candidate-facing
      summary).
    - regulatory-mapping override: name the article that grounds recourse.

Reference education implementation: yonah-edu-agent.
"""
from abc import ABC, abstractmethod


class QueryMyProvenanceTool(ABC):
    """Framework base class for the query_my_provenance tool. Audience: second_audience."""

    tool_name = "query_my_provenance"
    audience = "second_audience"

    input_schema = None  # Override hook
    output_schema = None  # Override hook
    regulatory_anchors: list[str] = []  # Override hook

    @abstractmethod
    def run(self, **kwargs):
        """Return the PROV subgraph for one of the caller's own decisions.

        Verticals override this with their domain-specific implementation.
        See yonah-edu-agent for the education reference.
        """
        raise NotImplementedError(
            "Verticals override this with their domain-specific implementation. "
            "See yonah-edu-agent for the education reference."
        )
