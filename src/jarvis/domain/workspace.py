"""Workspace Domain Model."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

@dataclass(frozen=True)
class Workspace:
    """Highest-level business object. Owns projects and sessions."""
    workspace_id: str
    name: str
    created_at: datetime
    metadata: dict[str, Any] = field(default_factory=dict)
