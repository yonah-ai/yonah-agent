"""DecisionDao — PynamoDB model (framework-canonical).

The committed-decision storage shape. Vertical forks bind the verdict's
body via their `chalicelib/vertical/`; the storage row schema is
invariant.

See the framework paper §5 and DEPLOY.md for the schema.
"""
import os

from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute
from pynamodb.models import Model

_PREFIX = os.environ.get("NAME_PREFIX", "yonah")


class DecisionDao(Model):
    class Meta:
        table_name = f"{_PREFIX}-decision-TODO"
        region = os.environ.get("AWS_REGION", "us-east-1")

    user_id = UnicodeAttribute(hash_key=True)
    decision_id = UnicodeAttribute(range_key=True)
    created_at = UTCDateTimeAttribute()

    # TODO: domain-specific attributes; soft-delete flag where applicable
