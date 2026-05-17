"""ApiKeyDao — PynamoDB model (framework-canonical).

Table name follows the `{vertical}-yonah-<entity>` pattern.
See the framework paper §5 and DEPLOY.md for the schema.
"""
import os

from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute
from pynamodb.models import Model

_PREFIX = os.environ.get("NAME_PREFIX", "yonah")


class ApiKeyDao(Model):
    class Meta:
        table_name = f"{_PREFIX}-api_key-TODO"
        region = os.environ.get("AWS_REGION", "us-east-1")

    key_hash = UnicodeAttribute(hash_key=True)
    created_at = UTCDateTimeAttribute()

    # TODO: domain-specific attributes; soft-delete flag where applicable
