"""Context Domain Model."""
from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class Context:
    """Derives from Knowledge. Current working context for Intents."""
    context_id: str
    knowledge_references: tuple[str, ...] = field(default_factory=tuple)
    active_elements: dict[str, Any] = field(default_factory=dict)
