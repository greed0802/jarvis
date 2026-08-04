"""Session Domain Model."""
from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class Session:
    """Runtime interaction boundary, belongs to Workspace."""
    session_id: str
    workspace_id: str
    created_at: datetime
    active_project_id: str | None = None
    current_context_id: str | None = None
