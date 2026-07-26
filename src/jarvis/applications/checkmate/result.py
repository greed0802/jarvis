"""CheckMate Application Execution Result.

Represents the output of a successful application execution.
Does NOT contain reports, Presentation Models, or recommendations.
Simply represents successful application execution.

Authority:
  - EQ-0021 (Permanently Frozen)
  - Application Architecture Principles v1.0
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from jarvis.applications.checkmate.state import CheckMateRuntimeState


@dataclass(frozen=True)
class CheckMateResult:
    """Immutable result of a CheckMate application execution.

    This is the public output of the application. It represents
    successful execution — not reports, not Presentation Models,
    not recommendations.

    Attributes:
        success: Whether the application executed successfully.
        state: Snapshot of the runtime state at completion.
        execution_timestamp: UTC timestamp of when execution completed.
    """

    success: bool
    state: CheckMateRuntimeState
    execution_timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )