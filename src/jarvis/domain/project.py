"""Project Domain Model."""
from dataclasses import dataclass, field
from datetime import datetime

@dataclass(frozen=True)
class Project:
    """Belongs to Workspace, owns knowledge."""
    project_id: str
    workspace_id: str
    name: str
    created_at: datetime
    status: str = "active"
