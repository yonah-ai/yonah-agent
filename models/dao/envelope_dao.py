"""EnvelopeDao — PynamoDB model (framework-canonical).

The append-only provenance envelope store. Vertical forks do not
override this; the envelope shape is the framework's structural
invariant.

See the framework paper §5 and DEPLOY.md for the schema.
"""
import os

from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute
from pynamodb.models import Model

_PREFIX = os.environ.get("NAME_PREFIX", "yonah")


class EnvelopeDao(Model):
    class Meta:
        table_name = f"{_PREFIX}-envelope-TODO"
        region = os.environ.get("AWS_REGION", "us-east-1")

    decision_id = UnicodeAttribute(hash_key=True)
    seq_step_id = UnicodeAttribute(range_key=True)
    created_at = UTCDateTimeAttribute()

    # TODO: domain-specific attributes; soft-delete flag where applicable
