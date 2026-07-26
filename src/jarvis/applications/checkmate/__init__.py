"""CheckMate Application — Quantity Surveying Guidance Platform.

CheckMate is the first production application on the Jarvis Platform.
This package provides the application foundation only — no business
interpretation, no Presentation Model, no review workflow, no reports,
no exports.

IP-0003 — CheckMate Application Foundation

Authority:
  - EQ-0021 (Permanently Frozen)
  - Application Architecture Principles v1.0
  - Implementation Governance

Public API:
    run() — Execute the CheckMate application with given inputs.
"""

from jarvis.applications.checkmate.application import run
from jarvis.applications.checkmate.config import CheckMateConfig
from jarvis.applications.checkmate.state import CheckMateRuntimeState, CheckMateStatus
from jarvis.applications.checkmate.errors import (
    CheckMateError,
    ConfigurationError,
    ContractViolationError,
    ApplicationRuntimeError,
    InternalError,
)
from jarvis.applications.checkmate.result import CheckMateResult

__all__ = [
    "run",
    "CheckMateConfig",
    "CheckMateRuntimeState",
    "CheckMateStatus",
    "CheckMateResult",
    "CheckMateError",
    "ConfigurationError",
    "ContractViolationError",
    "ApplicationRuntimeError",
    "InternalError",
]