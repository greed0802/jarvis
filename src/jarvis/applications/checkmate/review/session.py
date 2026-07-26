"""Review Session — Human interaction layer (IP-0006, Part B-F).

Provides the ReviewSession composition root that captures reviewer
interaction with the immutable PresentationModel. Consumes ONLY
PresentationModel. Records decisions, notes, bookmarks, and progress.

No rendering. No interpretation. No reports.

Authority:
  - EQ-0021 (Permanently Frozen)
  - Application Architecture Principles v1.0
  - IP-0006 — CheckMate Review Session & Human Workflow
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import uuid

from jarvis.applications.checkmate.presentation.models import (
    PresentationModel,
    NavigationIndex,
)
from jarvis.applications.checkmate.review.identity import PresentationId, PresentationIdPrefix
from jarvis.applications.checkmate.review.decisions import Decision, ReviewDecision, ReviewDecisionSet

# ============================================================================
# Review Note (Part D)
# ============================================================================

@dataclass(frozen=True)
class ReviewNote:
    """Reviewer-authored annotation for a presentation item.

    PresentationModel remains read-only. Notes are reviewer-authored only.

    Attributes:
        presentation_id: Stable presentation identity.
        note_text: Freeform reviewer text.
        timestamp: UTC timestamp.
        reviewer: Reviewer identifier.
    """

    presentation_id: PresentationId
    note_text: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    reviewer: str = ""

# ============================================================================
# Bookmark (Part E)
# ============================================================================

@dataclass(frozen=True)
class Bookmark:
    """A return-later bookmark referencing a presentation item.

    Attributes:
        presentation_id: Stable presentation identity.
        label: Short reviewer label.
        timestamp: UTC timestamp.
    """

    presentation_id: PresentationId
    label: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

# ============================================================================
# Review Progress (Part F)
# ============================================================================

@dataclass(frozen=True)
class ReviewProgress:
    """Deterministic review progress computed from a ReviewDecisionSet.

    Progress is read-only and computed deterministically at the time
    of inspection. No caching or mutable state.
    """

    total_items: int
    items_reviewed: int
    items_remaining: int
    accepted_count: int
    rejected_count: int
    deferred_count: int
    not_reviewed_count: int
    acceptance_percent: float
    completion_percent: float

    @classmethod
    def from_decisions(cls, decisions: ReviewDecisionSet) -> ReviewProgress:
        """Compute progress from current decisions."""
        total = len(decisions)
        accepted = sum(1 for d in decisions.decisions if d.decision == Decision.ACCEPTED)
        rejected = sum(1 for d in decisions.decisions if d.decision == Decision.REJECTED)
        deferred = sum(1 for d in decisions.decisions if d.decision == Decision.DEFERRED)
        not_reviewed = sum(1 for d in decisions.decisions if d.decision == Decision.NOT_REVIEWED)
        reviewed = accepted + rejected + deferred  # NOT_REVIEWED is not yet reviewed
        return cls(
            total_items=total,
            items_reviewed=reviewed,
            items_remaining=total - reviewed,
            accepted_count=accepted,
            rejected_count=rejected,
            deferred_count=deferred,
            not_reviewed_count=not_reviewed,
            acceptance_percent=(accepted / total * 100.0) if total > 0 else 0.0,
            completion_percent=(reviewed / total * 100.0) if total > 0 else 0.0,
        )

# ============================================================================
# Review Session (Part B)
# ============================================================================

@dataclass(frozen=True)
class ReviewSession:
    """Human review session consuming only the immutable PresentationModel.

    Captures human decisions, notes, bookmarks, and progress for the
    reviewer's session. The PresentationModel is NEVER modified. This is
    the only review state in the pipeline.

    Attributes:
        session_id: Unique review session ID.
        presentation: The immutable PresentationModel consumed for review.
        decisions: All reviewer decisions (immutable collection).
        notes: All reviewer-authored notes.
        bookmarks: All return-later bookmarks.
        progress: Computed review progress.
        started_at: UTC start timestamp.
        completed_at: UTC completion timestamp (None if in progress).
    """

    presentation: PresentationModel
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    decisions: ReviewDecisionSet = field(default_factory=lambda: ReviewDecisionSet(decisions=()))
    notes: tuple[ReviewNote, ...] = ()
    bookmarks: tuple[Bookmark, ...] = ()
    started_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    completed_at: str = ""

    def __post_init__(self) -> None:
        progress = ReviewProgress.from_decisions(self.decisions)
        object.__setattr__(self, "progress", progress)

    def record_decision(
        self, presentation_id: PresentationId, decision: Decision
    ) -> ReviewSession:
        """Return a new ReviewSession with one additional decision.

        The original session is not mutated. Returns a new session
        reflecting the new decision.

        Args:
            presentation_id: Stable presentation identity.
            decision: Reviewer's decision.

        Returns:
            New ReviewSession with updated decisions.
        """
        updated = list(self.decisions.decisions)
        # Remove any prior decision for same ID
        updated = [d for d in updated if d.presentation_id != presentation_id]
        # Add new decision
        updated.append(ReviewDecision(
            presentation_id=presentation_id,
            decision=decision,
        ))
        new_set = ReviewDecisionSet(decisions=tuple(updated))
        return ReviewSession(
            session_id=self.session_id,
            presentation=self.presentation,
            decisions=new_set,
            notes=self.notes,
            bookmarks=self.bookmarks,
            started_at=self.started_at,
            completed_at=self.completed_at,
        )

    def record_note(
        self, presentation_id: PresentationId, note_text: str, reviewer: str = ""
    ) -> ReviewSession:
        """Return a new ReviewSession with an additional note.

        Args:
            presentation_id: Stable presentation identity.
            note_text: Reviewer-authored text.
            reviewer: Optional reviewer identifier.

        Returns:
            New ReviewSession with note recorded.
        """
        new_note = ReviewNote(
            presentation_id=presentation_id,
            note_text=note_text,
            reviewer=reviewer,
        )
        return ReviewSession(
            session_id=self.session_id,
            presentation=self.presentation,
            decisions=self.decisions,
            notes=self.notes + (new_note,),
            bookmarks=self.bookmarks,
            started_at=self.started_at,
            completed_at=self.completed_at,
        )

    def add_bookmark(self, presentation_id: PresentationId, label: str) -> ReviewSession:
        """Return a new ReviewSession with a bookmark added.

        Args:
            presentation_id: Stable presentation identity.
            label: Reviewer-label for the bookmark.

        Returns:
            New ReviewSession with bookmark added.
        """
        bookmark = Bookmark(
            presentation_id=presentation_id,
            label=label,
        )
        return ReviewSession(
            session_id=self.session_id,
            presentation=self.presentation,
            decisions=self.decisions,
            notes=self.notes,
            bookmarks=self.bookmarks + (bookmark,),
            started_at=self.started_at,
            completed_at=self.completed_at,
        )

    def complete(self) -> ReviewSession:
        """Return a completed session with timestamp set."""
        return ReviewSession(
            session_id=self.session_id,
            presentation=self.presentation,
            decisions=self.decisions,
            notes=self.notes,
            bookmarks=self.bookmarks,
            started_at=self.started_at,
            completed_at=datetime.now(timezone.utc).isoformat(),
        )

# ============================================================================
# Factory function
# ============================================================================

def create_review_session(
    presentation: PresentationModel,
    initialize_all_as: Decision = Decision.NOT_REVIEWED,
) -> ReviewSession:
    """Create a ReviewSession with initial decisions for all presentation items.

    Every finding and recommendation in the PresentationModel gets
    an initial decision (default NOT_REVIEWED).

    Args:
        presentation: Immutable PresentationModel.
        initialize_all_as: Default decision for all items.

    Returns:
        New ReviewSession with initial decision set.
    """
    decisions: list[ReviewDecision] = []
    # Findings
    for i, _ in enumerate(presentation.findings.items):
        pid = PresentationId.for_finding(i)
        decisions.append(ReviewDecision(
            presentation_id=pid,
            decision=initialize_all_as,
        ))
    # Recommendations
    for i, _ in enumerate(presentation.recommendations.items):
        pid = PresentationId.for_recommendation(i)
        decisions.append(ReviewDecision(
            presentation_id=pid,
            decision=initialize_all_as,
        ))
    # Sections
    for i, _ in enumerate(presentation.sections.items):
        pid = PresentationId.for_section(i)
        decisions.append(ReviewDecision(
            presentation_id=pid,
            decision=initialize_all_as,
        ))
    return ReviewSession(
        presentation=presentation,
        decisions=ReviewDecisionSet(decisions=tuple(decisions)),
    )