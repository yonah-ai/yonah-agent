"""CohortDao — PynamoDB model (framework-canonical).

The "cohort" is the framework-level abstraction of the grouping concept
each vertical binds an artefact to (class enrolment in education, case
cohort in health, requisition in hire). Vertical forks may rename the
table at the `vertical_config.toml` level but the schema is invariant.

See the framework paper §5 and DEPLOY.md for the schema.
"""
import os

from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute
from pynamodb.models import Model

_PREFIX = os.environ.get("NAME_PREFIX", "yonah")


class CohortDao(Model):
    class Meta:
        table_name = f"{_PREFIX}-cohort-TODO"
        region = os.environ.get("AWS_REGION", "us-east-1")

    cohort_id = UnicodeAttribute(hash_key=True)
    user_id = UnicodeAttribute(range_key=True)
    created_at = UTCDateTimeAttribute()

    # TODO: domain-specific attributes; soft-delete flag where applicable
