"""ArtefactBuilderCrew (framework base class).

Invoked by the authority audience's build_artefact tool. The framework
crew defines the lifecycle stages and the structural-verifier hooks;
each vertical fork supplies the domain content (concrete agent
personalities, prompts, regulatory-mapping table).

Framework lifecycle stages (vertical-invariant):

    1. TypeAdvisor   — recommend a concrete shape of the shared-contract
                       artefact from the vertical's taxonomy.
    2. CriteriaElicitor — multi-turn dialogue to draft the artefact's
                       criterion-level structure.
    3. Validator     — coverage + measurability check against the
                       vertical's structural-verifier hooks.

Override hooks (verticals override exactly these):
    - `agents()`     — return the three concrete CrewAI Agents with
                       vertical-specific roles, goals, and backstories.
    - `tasks()`      — return the three concrete Tasks for the lifecycle
                       stages above, bound to the vertical's
                       artefact_schema.
    - `regulatory_mapping()` — declare which regulation articles each
                       stage discharges.
    - `structural_verifier_hooks()` — declare which verifiers the
                       framework should call on the artefact (coverage,
                       measurability, monotonicity, ...).

Reference education implementation: yonah-edu-agent.
"""
from abc import ABC, abstractmethod


class ArtefactBuilderCrew(ABC):
    """Framework base class for the artefact-builder crew."""

    crew_name = "artefact_builder"

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
    def tasks(self, llm, artefact_schema):
        """Return the three concrete tasks for the lifecycle stages."""
        raise NotImplementedError(
            "Verticals override this with their domain-specific implementation. "
            "See yonah-edu-agent for the education reference."
        )

    # Override hook: regulatory mapping for this crew.
    regulatory_mapping: dict[str, list[str]] = {}

    # Override hook: which structural verifiers to invoke at end-of-crew.
    structural_verifier_hooks: list[str] = []

    def build(self, llm, artefact_schema):
        """Assemble the framework Crew from vertical-supplied agents and tasks.

        TODO: instantiate CrewAI Crew(agents=self.agents(llm),
              tasks=self.tasks(llm, artefact_schema)) and return it.
        """
        raise NotImplementedError
