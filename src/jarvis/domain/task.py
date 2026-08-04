"""Task Domain Model."""
from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class Task:
    """Discrete unit of work within a Workflow."""
    task_id: str
    workflow_id: str
    capability_name: str
    status: str
    inputs: dict[str, Any] = field(default_factory=dict)
