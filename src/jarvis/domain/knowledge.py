"""Knowledge Domain Model."""
from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class KnowledgeItem:
    """Belongs to a Project. Source of truth documentation or data."""
    knowledge_id: str
    project_id: str
    resource_uri: str
    content_hash: str
    added_at: datetime
