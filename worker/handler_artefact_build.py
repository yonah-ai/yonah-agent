"""SQS handler for artefact_build actions (framework base).

See agent/crews/artefact_builder/. Vertical forks override the concrete
crew it dispatches to.
"""


def handle(message: dict):
    """TODO: instantiate the relevant crew + run + persist envelopes."""
    raise NotImplementedError
