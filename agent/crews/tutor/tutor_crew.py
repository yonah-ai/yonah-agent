"""TutorCrew (framework base class).

Invoked by the second-audience party's tutor_me tool. The framework
crew defines the lifecycle stages and the structural-verifier hooks;
each vertical fork supplies the domain content.

Framework lifecycle stages (vertical-invariant):

    1. ArtefactSummariser — render the active shared-contract artefact
                            into a second-audience-facing objective set.
    2. FormativeGuide     — drive the formative dialogue, grounding each
                            hint in a named criterion of the artefact.
    3. ReflectionPrompter — ask the second-audience party to articulate
                            their working interpretation of a criterion.

Every TutorCrew turn produces an envelope persisted to EnvelopeDao.

Override hooks (verticals override exactly these):
    - `agents()`     — return the three concrete agents with vertical
                       voice and grounding rules.
    - `tasks()`      — return the three concrete tasks bound to the
                       vertical's artefact_schema.
    - `regulatory_mapping()` — declare which articles each stage
                       discharges.
    - `structural_verifier_hooks()` — declare which verifiers run on
                       each formative turn.

Reference education implementation: yonah-edu-agent.
"""
from abc import ABC, abstractmethod


class TutorCrew(ABC):
    """Framework base class for the formative (tutor) crew."""

    crew_name = "tutor"

    @abstractmethod
    def agents(self, llm):
        """Return the three concrete agents.

        Verticals override this with their domain-specific implementation.
        See yonah-edu-agent for the education reference.
        """
        raise NotImplementedError(
            "Verticals override this with their domain-specific implementation. "
            "See yonah-edu-agent for the education reference."
        )

    @abstractmethod
    def tasks(self, llm, active_artefact):
        """Return the three concrete tasks for the lifecycle stages."""
        raise NotImplementedError(
            "Verticals override this with their domain-specific implementation. "
            "See yonah-edu-agent for the education reference."
        )

    regulatory_mapping: dict[str, list[str]] = {}  # Override hook
    structural_verifier_hooks: list[str] = []  # Override hook

    def build(self, llm, active_artefact):
        """Assemble the framework Crew from vertical-supplied agents and tasks."""
        raise NotImplementedError
