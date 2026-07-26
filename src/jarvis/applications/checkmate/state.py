"""CheckMate Application Runtime State.

Contains application status, input references, configuration,
diagnostics, and timestamps. No Presentation Model, no review state.

Authority:
  - EQ-0021 (Permanently Frozen)
  - Application Architecture Principles v1.0
"""

from __future__ import annotations

import enum
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from jarvis.applications.checkmate.config import CheckMateConfig


class CheckMateStatus(enum.Enum):
    """Deterministic application lifecycle status.

    Transitions follow a strict linear order:
        UNINITIALIZED → INITIALIZED → INPUT_READY → RUNNING → COMPLETE
        UNINITIALIZED → INITIALIZED → INPUT_READY → RUNNING → FAILED
    """

    UNINITIALIZED = "UNINITIALIZED"
    INITIALIZED = "INITIALIZED"
    INPUT_READY = "INPUT_READY"
    RUNNING = "RUNNING"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"

    def can_transition_to(self, target: CheckMateStatus) -> bool:
        """Check if a transition to the target status is valid.

        Args:
            target: The target status to transition to.

        Returns:
            True if the transition is valid.
        """
        valid_transitions: dict[CheckMateStatus, set[CheckMateStatus]] = {
            CheckMateStatus.UNINITIALIZED: {CheckMateStatus.INITIALIZED},
            CheckMateStatus.INITIALIZED: {CheckMateStatus.INPUT_READY, CheckMateStatus.FAILED},
            CheckMateStatus.INPUT_READY: {CheckMateStatus.RUNNING, CheckMateStatus.FAILED},
            CheckMateStatus.RUNNING: {CheckMateStatus.COMPLETE, CheckMateStatus.FAILED},
            CheckMateStatus.COMPLETE: set(),
            CheckMateStatus.FAILED: set(),
        }
        return target in valid_transitions.get(self, set())


@dataclass(frozen=False)
class CheckMateRuntimeState:
    """Mutable runtime state for the CheckMate application.

    Tracks the current execution state deterministically.
    Not frozen because state transitions are part of the lifecycle.

    No Presentation Model data, no review state, no report data.
    """

    status: CheckMateStatus = CheckMateStatus.UNINITIALIZED
    config: CheckMateConfig = field(default_factory=CheckMateConfig)
    has_evidence: bool = False
    has_findings: bool = False
    has_interpretation: bool = False
    started_at: datetime | None = None
    completed_at: datetime | None = None
    diagnostics: dict[str, Any] = field(default_factory=dict)
    error_count: int = 0
    errors: list[str] = field(default_factory=list)

    def transition_to(self, target: CheckMateStatus) -> None:
        """Transition to a new status, validating the transition.

        Args:
            target: The target status.

        Raises:
            RuntimeError: If the transition is invalid.
        """
        if not self.status.can_transition_to(target):
            raise RuntimeError(
                f"Invalid status transition: {self.status.value} → {target.value}"
            )
        self.status = target

    def record_error(self, message: str) -> None:
        """Record a non-fatal error.

        Args:
            message: Error description.
        """
        self.error_count += 1
        self.errors.append(message)

    @property
    def elapsed_seconds(self) -> float | None:
        """Get elapsed execution time in seconds.

        Returns:
            Elapsed time if execution has started, None otherwise.
        """
        if self.started_at is None:
            return None
        end = self.completed_at or datetime.now(timezone.utc)
        return (end - self.started_at).total_seconds()