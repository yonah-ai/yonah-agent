"""EvaluatorCrew (framework base class).

Invoked by the second-audience party's submit_draft tool (via the SQS
worker, not inline). The framework crew defines the lifecycle stages
and the structural-verifier hooks; each vertical fork supplies the
domain content.

Framework lifecycle stages (vertical-invariant):

    1. IdentityBlindReader — confirms PII detachment is in place, produces
                             a structured reading of the submission.
    2. ArtefactApplier     — per-criterion application of the shared-contract
                             artefact to the structured reading.
    3. EvidenceFinder      — cite submission spans (offset + content hash)
                             grounding each per-criterion outcome.
    4. Calibrator          — cross-criterion consistency check + SPARQL
                             emptiness check against the structural
                             verifier's invariants.
    5. Auditor             — Ed25519-sign the final envelope chain.

Outputs are read by both audiences: the second-audience party via the
result view + query_my_provenance; the authority audience via
commit_decision.

Override hooks (verticals override exactly these):
    - `agents()`     — return the five concrete agents with vertical
                       voice. Verticals may collapse stages (e.g. fold
                       Calibrator into Auditor for short-form decisions)
                       but the framework's stage IDs remain canonical
                       across the family.
    - `tasks()`      — return the five concrete tasks for the lifecycle
                       stages, bound to the vertical's artefact_schema.
    - `regulatory_mapping()` — declare which articles each stage
                       discharges.
    - `structural_verifier_hooks()` — declare which verifiers run.

Reference education implementation: yonah-edu-agent.
"""
from abc import ABC, abstractmethod


class EvaluatorCrew(ABC):
    """Framework base class for the evaluator crew."""

    crew_name = "evaluator"

    @abstractmethod
    def agents(self, llm):
        """Return the five concrete agents.

        Verticals override this with their domain-specific implementation.
        See yonah-edu-agent for the education reference.
        """
        raise NotImplementedError(
            "Verticals override this with their domain-specific implementation. "
            "See yonah-edu-agent for the education reference."
        )

    @abstractmethod
    def tasks(self, llm, artefact_id):
        """Return the five concrete tasks for the lifecycle stages."""
        raise NotImplementedError(
            "Verticals override this with their domain-specific implementation. "
            "See yonah-edu-agent for the education reference."
        )

    regulatory_mapping: dict[str, list[str]] = {}  # Override hook
    structural_verifier_hooks: list[str] = []  # Override hook

    def build(self, llm, artefact_id):
        """Assemble the framework Crew from vertical-supplied agents and tasks."""
        raise NotImplementedError
