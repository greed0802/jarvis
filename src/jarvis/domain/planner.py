"""Planner Domain Model."""
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Plan:
    """Generates Workflows from Intents."""
    plan_id: str
    intent_id: str
    workflow_id: str
    strategy: str
