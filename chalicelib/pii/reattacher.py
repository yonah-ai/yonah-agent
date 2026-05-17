"""PII reattacher (framework-canonical).

Allowed at exactly two endpoints:
  - second-audience query_my_provenance (the party may see their own
    identifying information on their own decision)
  - authority commit_decision (the authority audience may see the
    identity of whom they are committing a decision against)

Refuses everywhere else by design. See agent/yonah/role_guard.py.
"""
from typing import Literal

# TODO: implement reattach(decision_id, code, *, allowed_for: Literal["second_audience_self", "authority_commit"])
