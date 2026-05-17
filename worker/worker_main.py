"""SQS-triggered Lambda worker entry point (framework-canonical).

Parses incoming SQS records, routes by action code (BUILD_ARTEFACT,
TUTOR_TURN, EVAL_DRAFT, COMMIT_DECISION, ...) to the appropriate handler
in this package.
"""
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """Dispatch each SQS record to the right handler."""
    for record in event.get("Records", []):
        body = json.loads(record["body"])
        action = body.get("action")
        logger.info("worker received action=%s decision_id=%s", action, body.get("decision_id"))
        # TODO: dispatch by action to handler_artefact_build / handler_tutor /
        # handler_evaluator
    return {"statusCode": 200}
