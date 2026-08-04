"""Capability Domain Model."""
from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class CapabilityDefinition:
    """Defines what the platform can do."""
    name: str
    description: str
    input_schema: dict[str, Any] = field(default_factory=dict)
    output_schema: dict[str, Any] = field(default_factory=dict)
    supported_intents: tuple[str, ...] = field(default_factory=tuple)
    priority: int = 0
