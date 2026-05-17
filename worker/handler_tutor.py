"""SQS handler for tutor actions (framework base).

See agent/crews/tutor/. Vertical forks override the concrete crew it
dispatches to.
"""


def handle(message: dict):
    """TODO: instantiate the relevant crew + run + persist envelopes."""
    raise NotImplementedError
