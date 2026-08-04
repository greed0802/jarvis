"""Capability Manifests and Contracts."""
from dataclasses import dataclass, field
from typing import Any, Dict

from jarvis.domain.capability import CapabilityDefinition

@dataclass(frozen=True)
class CapabilityInput:
    parameters: dict[str, Any]

@dataclass(frozen=True)
class CapabilityResult:
    status: str
    output: Any
    evidence: list[Any] = field(default_factory=list)

@dataclass(frozen=True)
class ExecutionContext:
    workspace_id: str
    session_id: str
    inputs: CapabilityInput
