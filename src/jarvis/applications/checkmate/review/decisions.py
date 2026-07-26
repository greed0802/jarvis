"""Review Decisions — Immutable human reviewer decisions (IP-0006, Part C).

Supported decisions: Accepted, Rejected, Needs Review, Deferred, Not Reviewed.

Review decisions never modify the PresentationModel. They are pure
annotations of reviewer intent.

Authority:
  - EQ-0021 (Permanently Frozen)
  - Application Architecture Principles v1.0
  - IP-0006 — CheckMate Review Session & Human Workflow
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

import enum
from jarvis.applications.checkmate.review.identity import PresentationId

class Decision(enum.Enum):
    """Deterministic review decision values.

    ACCEPTED — Reviewer confirms the finding/recommendation.
    REJECTED — Reviewer disagrees with the finding/recommendation.
    NEEDS_REVIEW — Explicit reviewer identification of pending work.
    DEFERRED — Postponed for later consideration.
    NOT_REVIEWED — No decision yet recorded (default).
    """
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    NEEDS_REVIEW = "NEEDS_REVIEW"
    DEFERRED = "DEFERRED"
    NOT_REVIEWED = "NOT_REVIEWED"

@dataclass(frozen=True)
class ReviewDecision:
    """A single immutable reviewer decision for one presentation item.

    Attributes:
        presentation_id: Stable presentation identity.
        decision: Human decision.
        timestamp: UTC timestamp when decision was made.
    """
    presentation_id: PresentationId
    decision: Decision
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

@dataclass(frozen=True)
class ReviewDecisionSet:
    """Immutable collection of all reviewer decisions for a session.

    Attributes:
        decisions: Tuple of ReviewDecision.
    """

    decisions: tuple[ReviewDecision, ...]

    def of(self, presentation_id: PresentationId) -> Decision:
        """Return the decision for a presentation ID, or NOT_REVIEWED."""
        for d in self.decisions:
            if d.presentation_id == presentation_id:
                return d.decision
        return Decision.NOT_REVIEWED

    def __len__(self) -> int:
        return len(self.decisions)