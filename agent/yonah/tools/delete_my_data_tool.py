"""delete_my_data tool — universal-audience side (framework base class).

API contract (vertical-invariant):

    Input fields:
        confirm: bool              # explicit caller confirmation

    Output fields:
        deleted_envelopes: int     # count of envelopes scrubbed
        deleted_pii_tokens: int    # count of PiiToken rows deleted
        retention_residue: dict    # what was kept on legal-basis grounds

    Contract semantics:
        - Universal: every caller may invoke this against their own data.
        - The envelope chain itself is NOT deleted (append-only); instead
          the personally identifiable information (PII) reattachment
          mapping is purged so the residual chain becomes anonymous.
        - Some envelopes may be retained on legal-basis grounds
          (regulatory record-keeping); the residue is itemised in
          retention_residue with the article cited as basis.
        - Discharges the caller's right to erasure where the regulation
          provides one (vertical specifies exact article).

Override hooks (verticals override exactly these):
    - input-schema override: usually none; confirm flag is invariant.
    - output-schema override: extend retention_residue with vertical-specific
      legal-basis citations.
    - regulatory-mapping override: name the article that grounds erasure
      (GDPR Art. 17 + the vertical's domain-specific retention basis).

Reference education implementation: yonah-edu-agent.
"""
from abc import ABC, abstractmethod


class DeleteMyDataTool(ABC):
    """Framework base class for the delete_my_data tool. Audience: universal."""

    tool_name = "delete_my_data"
    audience = "universal"

    input_schema = None  # Override hook
    output_schema = None  # Override hook
    regulatory_anchors: list[str] = []  # Override hook

    @abstractmethod
    def run(self, **kwargs):
        """Scrub the caller's PII reattachment mapping; keep envelopes anonymous.

        Verticals override this with their domain-specific implementation.
        See yonah-edu-agent for the education reference.
        """
        raise NotImplementedError(
            "Verticals override this with their domain-specific implementation. "
            "See yonah-edu-agent for the education reference."
        )
