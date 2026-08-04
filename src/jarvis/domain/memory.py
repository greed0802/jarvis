"""Memory Domain Model."""
from dataclasses import dataclass, field
from datetime import datetime

@dataclass(frozen=True)
class Memory:
    """References Knowledge and Context. Stores insights and facts."""
    memory_id: str
    context_id: str
    content: str
    created_at: datetime
    knowledge_references: tuple[str, ...] = field(default_factory=tuple)
