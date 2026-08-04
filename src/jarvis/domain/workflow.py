"""Workflow Domain Model."""
from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class Workflow:
    """Consumes Intent. State machine for execution."""
    workflow_id: str
    intent_id: str
    status: str  # e.g. PENDING, RUNNING, COMPLETED
    metadata: dict[str, Any] = field(default_factory=dict)
