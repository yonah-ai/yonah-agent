"""ArtefactDao — PynamoDB model (framework-canonical).

The shared-contract artefact's storage shape. Vertical forks bind the
artefact's body via their `chalicelib/vertical/artefact_schema.py`; the
storage row schema is invariant.

See the framework paper §5 and DEPLOY.md for the schema.
"""
import os

from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute
from pynamodb.models import Model

_PREFIX = os.environ.get("NAME_PREFIX", "yonah")


class ArtefactDao(Model):
    class Meta:
        table_name = f"{_PREFIX}-artefact-TODO"
        region = os.environ.get("AWS_REGION", "us-east-1")

    user_id = UnicodeAttribute(hash_key=True)
    artefact_id = UnicodeAttribute(range_key=True)
    created_at = UTCDateTimeAttribute()

    # TODO: domain-specific attributes; soft-delete flag where applicable
