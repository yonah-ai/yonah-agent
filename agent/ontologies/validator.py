"""Generic structural validators shared across crews (framework-canonical).

The framework ships:
  - verify_integrity        — envelope hash chain re-derives.
  - verify_temporal_oversight — required `used` activities precede `wasGeneratedBy`.
  - verify_role_gate        — every tool invocation was role-allowed.
  - verify_artefact_grounding — every formative turn grounded in an artefact criterion.

Vertical forks add their own verifiers in
`chalicelib/vertical/regulatory_map.py`; the framework runs both layers
in sequence.
"""
# TODO: structural verifier implementations
