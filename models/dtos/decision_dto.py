"""DecisionDTO — Pydantic v2 contract for the decision surface (framework base).

Vertical forks subclass and add the verdict shape (grade / treatment /
hire-decision / ...).
"""
from pydantic import BaseModel


class DecisionDTO(BaseModel):
    """TODO: fill in fields per the framework paper §5."""

    pass
