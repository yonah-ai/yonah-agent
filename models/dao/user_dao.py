"""UserDao — PynamoDB model (framework-canonical).

Table name follows the `{vertical}-yonah-<entity>` pattern. The vertical
prefix is supplied at deploy time via the `NAME_PREFIX` environment
variable; the framework default is `yonah`.

See the framework paper §5 and DEPLOY.md for the schema.
"""
import os

from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute
from pynamodb.models import Model

_PREFIX = os.environ.get("NAME_PREFIX", "yonah")


class UserDao(Model):
    class Meta:
        table_name = f"{_PREFIX}-user-TODO"
        region = os.environ.get("AWS_REGION", "us-east-1")

    user_id = UnicodeAttribute(hash_key=True)
    created_at = UTCDateTimeAttribute()

    # TODO: domain-specific attributes; soft-delete flag where applicable
