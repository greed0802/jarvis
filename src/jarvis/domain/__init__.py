"""Domain Rule Foundation for BOQ Intelligence.

This package provides deterministic rule representation for all
BOQ domain rules — both Engineering-derived and Domain-derived.

It is the foundation that future capabilities (CheckMate, Formatter,
Validation Reports, SDK/API, AI consumers) will depend upon.

Authority:
  - CB-0002 — BOQ Intelligence Domain Rule Foundation
  - Capability Baseline (docs/planning/Capability_Baseline.md)
  - Capability Register (docs/planning/Capability_Register.md)

Constraints:
  - Pure Python. No runtime registration framework.
  - Immutable after loading. Deterministic ordering.
  - No reflection. No plugins. No dynamic imports.
  - No architecture drift. No speculative implementation.
"""

from jarvis.domain.models import (
    RuleAuthority,
    RuleCategory,
    RuleSeverity,
    RuleStatus,
    DomainRule,
    RuleRegistry,
)

from jarvis.domain.registry import load_registry, get_registry

__all__ = [
    "RuleAuthority",
    "RuleCategory",
    "RuleSeverity",
    "RuleStatus",
    "DomainRule",
    "RuleRegistry",
    "load_registry",
    "get_registry",
]

# Jarvis Domain Models
from .workspace import Workspace
from .project import Project
from .knowledge import KnowledgeItem
from .context import Context
from .memory import Memory
from .intent import Intent
from .workflow import Workflow
from .task import Task
from .capability import CapabilityDefinition
from .planner import Plan
from .session import Session

__all__.extend([
    "Workspace",
    "Project",
    "KnowledgeItem",
    "Context",
    "Memory",
    "Intent",
    "Workflow",
    "Task",
    "CapabilityDefinition",
    "Plan",
    "Session"
])
