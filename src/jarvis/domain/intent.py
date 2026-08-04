"""Intent Domain Model."""
from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class Intent:
    """Consumes Context. Structured understanding of user's objective."""
    intent_id: str
    context_id: str
    goal: str
    parameters: dict[str, Any] = field(default_factory=dict)
