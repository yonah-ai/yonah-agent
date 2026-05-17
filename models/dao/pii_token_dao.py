"""PiiTokenDao — PynamoDB model (framework-canonical).

KMS-wrapped mapping from opaque code to the original identifying field
of the second-audience party. TTL-bound; the delete_my_data tool purges
this row to render the residual envelope chain anonymous.

See the framework paper §5 and DEPLOY.md for the schema.
"""
import os

from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute
from pynamodb.models import Model

_PREFIX = os.environ.get("NAME_PREFIX", "yonah")


class PiiTokenDao(Model):
    class Meta:
        table_name = f"{_PREFIX}-pii_token-TODO"
        region = os.environ.get("AWS_REGION", "us-east-1")

    decision_id = UnicodeAttribute(hash_key=True)
    code = UnicodeAttribute(range_key=True)
    created_at = UTCDateTimeAttribute()

    # TODO: domain-specific attributes; soft-delete flag where applicable
