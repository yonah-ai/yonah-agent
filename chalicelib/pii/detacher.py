"""PII detacher middleware (framework-canonical).

Runs at /eval ingress (submit_draft path). Extracts identifying fields
from the request body, mints a ULID code, encrypts the identity under
the per-tenant Key Management Service (KMS) data key, persists the
mapping to PiiTokenDao, and rewrites the request body so the downstream
pipeline sees only the opaque code.

This is framework-canonical and does not require vertical overrides.
Vertical-specific identifying-field lists are declared in
`chalicelib/vertical/vertical_config.py` and read at detacher init.
"""
from typing import Any

# TODO: implement detach(request_body: dict) -> (rewritten_body, decision_id, code)
# TODO: integrate as Chalice middleware on submit_draft route
