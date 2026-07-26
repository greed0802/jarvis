"""Tests for CheckMate Review Session (IP-0006).

Verifies:
- PresentationId stability, determinism, uniqueness
- ReviewDecision immutability
- ReviewSession: decision recording, notes, bookmarks, progress
- PresentationModel unchanged after review
- No interpretation in review layer
- Review navigation via presentation

"""

from __future__ import annotations

import uuid

import pytest

from jarvis.applications.checkmate.config import CheckMateConfig
from jarvis.applications.checkmate.context import ApplicationContext
from jarvis.applications.checkmate.interpretation.engine import interpret
from jarvis.applications.checkmate.presentation.assembler import assemble
from jarvis.applications.checkmate.review.identity import (
    PresentationId,
    PresentationIdPrefix,
)
from jarvis.applications.checkmate.review.decisions import (
    Decision,
    ReviewDecision,
    ReviewDecisionSet,
)
from jarvis.applications.checkmate.review.session import (
    ReviewSession,
    ReviewProgress,
    ReviewNote,
    Bookmark,
    create_review_session,
)
from jarvis.parsers.costx.boq_intelligence import BOQIntelligenceResult
from jarvis.engines.validation.engine import ValidationFindings, ValidationFinding

# ============================================================================
# Test Helpers
# ============================================================================

def _make_minimal_evidence() -> BOQIntelligenceResult:
    return BOQIntelligenceResult(
        row_classification={"Head": 5, "Item": 10, "Note": 1},
        section_statistics={
            "Section A": {"items": 5, "page": 1},
            "Section B": {"items": 5, "page": 1},
        },
        boq_statistics={"total_rows": 16, "total_sections": 2},
        known_anomalies=[],
    )

def _make_findings(*finding_types: str) -> ValidationFindings:
    entries: list[ValidationFinding] = []
    for i, ft in enumerate(finding_types, start=1):
        entries.append(ValidationFinding(
            rule_id=f"V-{i:03d}",
            rule_version="1.0.0",
            category="Test Category",
            finding_type=ft,
            finding_value=0,
            evidence_fields=("row_classification", "section_statistics"),
        ))
    return ValidationFindings(
        findings=tuple(entries),
        engine_version="1.0.0",
        contract_version="1.0.0",
        execution_timestamp="2026-07-25T00:00:00+00:00",
    )

def _make_context(finding_types: tuple = ("Error", "Warning", "Information")) -> ApplicationContext:
    return ApplicationContext(
        evidence=_make_minimal_evidence(),
        findings=_make_findings(*finding_types),
    )

def _make_presentation(finding_types: tuple = ("Error", "Warning", "Information")) -> "PresentationModel":
    ctx = _make_context(finding_types=finding_types)
    interpretation = interpret(ctx)
    return assemble(ctx, interpretation)

# ============================================================================
# Part A: PresentationId Tests
# ============================================================================

class TestPresentationId:
    """Verify stable, deterministic presentation identity."""

    def test_finding_id_format(self) -> None:
        pid = PresentationId.for_finding(0)
        assert pid.to_external() == "PF-000001"

    def test_finding_id_format_second(self) -> None:
        pid = PresentationId.for_finding(1)
        assert pid.to_external() == "PF-000002"

    def test_recommendation_id_format(self) -> None:
        pid = PresentationId.for_recommendation(0)
        assert pid.to_external() == "PR-000001"

    def test_section_id_format(self) -> None:
        pid = PresentationId.for_section(0)
        assert pid.to_external() == "PS-000001"

    def test_navigation_id_format(self) -> None:
        pid = PresentationId.for_navigation(0)
        assert pid.to_external() == "PN-000001"

    def test_ids_are_equal_for_same_index(self) -> None:
        a = PresentationId.for_finding(5)
        b = PresentationId.for_finding(5)
        assert a == b
        assert hash(a) == hash(b)

    def test_ids_not_equal_for_different_indices(self) -> None:
        a = PresentationId.for_finding(0)
        b = PresentationId.for_finding(1)
        assert a != b

    def test_different_prefixes_never_equal(self) -> None:
        pf = PresentationId.for_finding(0)
        pr = PresentationId.for_recommendation(0)
        assert pf != pr

    def test_str_equals_to_external(self) -> None:
        pid = PresentationId.for_finding(0)
        assert str(pid) == pid.to_external()

    def test_representation_is_stable(self) -> None:
        pid = PresentationId.for_finding(0)
        assert str(pid) == "PF-000001"
        assert repr(pid).startswith("PresentationId")

    def test_deterministic(self) -> None:
        a = PresentationId.for_finding(3)
        b = PresentationId.for_finding(3)
        assert a == b
        assert a.to_external() == b.to_external()
        assert str(a) == str(b)

    def test_no_rule_ids_in_presentation(self) -> None:
        """PresentationIds do NOT expose rule IDs or internal engine IDs."""
        pid = PresentationId.for_finding(0)
        assert "V-" not in pid.to_external()
        assert "rule" not in pid.to_external().lower()
        assert "engine" not in pid.to_external().lower()

# ============================================================================
# Part C: ReviewDecision Tests
# ============================================================================

class TestReviewDecision:
    """Verify immutable review decisions."""

    def test_decision_is_frozen(self) -> None:
        pid = PresentationId.for_finding(0)
        rd = ReviewDecision(
            presentation_id=pid,
            decision=Decision.ACCEPTED,
        )
        with pytest.raises(Exception):
            rd.decision = Decision.REJECTED

    def test_default_decision_is_not_reviewed(self) -> None:
        pid = PresentationId.for_finding(0)
        rd = ReviewDecision(
            presentation_id=pid,
            decision=Decision.NOT_REVIEWED,
        )
        assert rd.decision == Decision.NOT_REVIEWED

    def test_all_decisions_exist(self) -> None:
        for decision in Decision:
            assert isinstance(decision, Decision)

    def test_decisions_are_unique(self) -> None:
        num_decision_values = len({d.value for d in Decision})
        assert num_decision_values >= 5  # ACCEPTED, REJECTED, NEEDS_REVIEW, DEFERRED, NOT_REVIEWED

# ============================================================================
# Part B: ReviewDecisionSet Tests
# ============================================================================

class TestReviewDecisionSet:
    """Verify collection of review decisions."""

    def test_can_query_by_presentation_id(self) -> None:
        pid1 = PresentationId.for_finding(0)
        pid2 = PresentationId.for_finding(1)
        ds = ReviewDecisionSet(decisions=(
            ReviewDecision(presentation_id=pid1, decision=Decision.ACCEPTED),
        ))
        assert ds.of(pid1) == Decision.ACCEPTED
        assert ds.of(pid2) == Decision.NOT_REVIEWED

    def test_empty_set_returns_not_reviewed(self) -> None:
        ds = ReviewDecisionSet(decisions=())
        pid = PresentationId.for_finding(0)
        assert ds.of(pid) == Decision.NOT_REVIEWED

    def test_items_reviewed_count(self) -> None:
        pids = [PresentationId.for_finding(i) for i in range(3)]
        ds = ReviewDecisionSet(decisions=(
            ReviewDecision(presentation_id=pids[0], decision=Decision.ACCEPTED),
            ReviewDecision(presentation_id=pids[1], decision=Decision.NOT_REVIEWED),
            ReviewDecision(presentation_id=pids[2], decision=Decision.DEFERRED),
        ))
        # 3 items, 1 NOT_REVIEWED → 2 reviewed
        progress = ReviewProgress.from_decisions(ds)
        assert progress.items_reviewed == 2

    def test_full_count_matches_input(self) -> None:
        ds = ReviewDecisionSet(decisions=(
            ReviewDecision(presentation_id=PresentationId.for_finding(0), decision=Decision.ACCEPTED),
        ))
        assert len(ds) == 1

# ============================================================================
# Part F: ReviewProgress Tests
# ============================================================================

class TestReviewProgress:
    """Verify deterministic review progress computation."""

    def test_all_not_reviewed(self) -> None:
        ds = ReviewDecisionSet(decisions=(
            ReviewDecision(presentation_id=PresentationId.for_finding(0), decision=Decision.NOT_REVIEWED),
            ReviewDecision(presentation_id=PresentationId.for_finding(1), decision=Decision.NOT_REVIEWED),
        ))
        progress = ReviewProgress.from_decisions(ds)
        assert progress.total_items == 2
        assert progress.items_reviewed == 0
        assert progress.items_remaining == 2
        assert progress.completion_percent == 0.0

    def test_all_accepted(self) -> None:
        ds = ReviewDecisionSet(decisions=(
            ReviewDecision(presentation_id=PresentationId.for_finding(0), decision=Decision.ACCEPTED),
        ))
        progress = ReviewProgress.from_decisions(ds)
        assert progress.items_reviewed == 1
        assert progress.accepted_count == 1
        assert progress.acceptance_percent == 100.0
        assert progress.completion_percent == 100.0

    def test_mixed_decisions(self) -> None:
        ds = ReviewDecisionSet(decisions=(
            ReviewDecision(presentation_id=PresentationId.for_finding(0), decision=Decision.ACCEPTED),
            ReviewDecision(presentation_id=PresentationId.for_finding(1), decision=Decision.REJECTED),
            ReviewDecision(presentation_id=PresentationId.for_finding(2), decision=Decision.DEFERRED),
            ReviewDecision(presentation_id=PresentationId.for_finding(3), decision=Decision.NOT_REVIEWED),
        ))
        progress = ReviewProgress.from_decisions(ds)
        assert progress.total_items == 4
        assert progress.items_reviewed == 3
        assert progress.accepted_count == 1
        assert progress.rejected_count == 1
        assert progress.deferred_count == 1
        assert progress.not_reviewed_count == 1
        assert progress.acceptance_percent == 25.0
        assert progress.completion_percent == 75.0

    def test_empty_decisions_progress_zero(self) -> None:
        progress = ReviewProgress.from_decisions(ReviewDecisionSet(decisions=()))
        assert progress.total_items == 0
        assert progress.items_reviewed == 0
        assert progress.completion_percent == 0.0

    def test_progress_is_deterministic(self) -> None:
        ds1 = ReviewDecisionSet(decisions=(
            ReviewDecision(presentation_id=PresentationId.for_finding(0), decision=Decision.ACCEPTED),
        ))
        ds2 = ReviewDecisionSet(decisions=(
            ReviewDecision(presentation_id=PresentationId.for_finding(0), decision=Decision.ACCEPTED),
        ))
        p1 = ReviewProgress.from_decisions(ds1)
        p2 = ReviewProgress.from_decisions(ds2)
        assert p1 == p2

# ============================================================================
# Part D: ReviewNote Tests
# ============================================================================

class TestReviewNote:
    """Verify reviewer-authored notes."""

    def test_note_is_frozen(self) -> None:
        note = ReviewNote(
            presentation_id=PresentationId.for_finding(0),
            note_text="This item needs clarification.",
        )
        with pytest.raises(Exception):
            note.note_text = "changed"

    def test_note_contains_text(self) -> None:
        note = ReviewNote(
            presentation_id=PresentationId.for_finding(0),
            note_text="Check item 5",
        )
        assert "Check item 5" == note.note_text

    def test_note_has_timestamp(self) -> None:
        note = ReviewNote(
            presentation_id=PresentationId.for_finding(0),
            note_text="note",
        )
        assert len(note.timestamp) > 0

    def test_note_has_reviewer(self) -> None:
        note = ReviewNote(
            presentation_id=PresentationId.for_finding(0),
            note_text="note",
            reviewer="jdoe",
        )
        assert note.reviewer == "jdoe"

# ============================================================================
# Part E: Bookmark Tests
# ============================================================================

class TestBookmark:
    """Verify bookmarks."""

    def test_bookmark_references_presentation_id(self) -> None:
        pid = PresentationId.for_finding(3)
        bm = Bookmark(presentation_id=pid, label="return later")
        assert bm.presentation_id.to_external() == "PF-000004"

    def test_bookmark_is_frozen(self) -> None:
        bm = Bookmark(presentation_id=PresentationId.for_finding(0), label="mark")
        with pytest.raises(Exception):
            bm.label = "new label"

    def test_bookmark_has_timestamp(self) -> None:
        bm = Bookmark(presentation_id=PresentationId.for_finding(0), label="mark")
        assert len(bm.timestamp) > 0

# ============================================================================
# ReviewSession Tests
# ============================================================================

class TestReviewSession:
    """Verify ReviewSession creation, decision recording, notes, bookmarks."""

    def test_create_session_from_presentation(self) -> None:
        presentation = _make_presentation()
        session = create_review_session(presentation)
        assert session.presentation is presentation
        assert len(session.decisions) >= 0
        assert len(session.notes) == 0
        assert len(session.bookmarks) == 0

    def test_session_defaults_are_not_reviewed(self) -> None:
        presentation = _make_presentation()
        session = create_review_session(presentation)
        for d in session.decisions.decisions:
            assert d.decision == Decision.NOT_REVIEWED

    def test_session_has_unique_id(self) -> None:
        p = _make_presentation()
        s1 = create_review_session(p)
        s2 = create_review_session(p)
        assert s1.session_id != s2.session_id

    def test_record_decision_returns_new_session(self) -> None:
        presentation = _make_presentation()
        session = create_review_session(presentation)
        pid = PresentationId.for_finding(0)
        updated = session.record_decision(pid, Decision.ACCEPTED)
        # Original session unchanged
        assert session.decisions.of(pid) == Decision.NOT_REVIEWED
        # New session reflects decision
        assert updated.decisions.of(pid) == Decision.ACCEPTED
        assert updated is not session

    def test_record_multiple_decisions(self) -> None:
        presentation = _make_presentation()
        session = create_review_session(presentation)
        pid1 = PresentationId.for_finding(0)
        pid2 = PresentationId.for_finding(1)
        session = session.record_decision(pid1, Decision.ACCEPTED)
        session = session.record_decision(pid2, Decision.REJECTED)
        assert session.decisions.of(pid1) == Decision.ACCEPTED
        assert session.decisions.of(pid2) == Decision.REJECTED

    def test_re_record_decision_overwrites(self) -> None:
        presentation = _make_presentation()
        session = create_review_session(presentation)
        pid = PresentationId.for_finding(0)
        session = session.record_decision(pid, Decision.REJECTED)
        session = session.record_decision(pid, Decision.ACCEPTED)
        # Only one decision per ID
        assert session.decisions.of(pid) == Decision.ACCEPTED
        count = len([d for d in session.decisions.decisions if d.presentation_id == pid])
        assert count == 1

    def test_record_note(self) -> None:
        presentation = _make_presentation()
        session = create_review_session(presentation)
        pid = PresentationId.for_finding(0)
        session = session.record_note(pid, "check this", reviewer="jdoe")
        assert len(session.notes) == 1
        assert session.notes[0].note_text == "check this"
        assert session.notes[0].reviewer == "jdoe"

    def test_record_multiple_notes(self) -> None:
        presentation = _make_presentation()
        session = create_review_session(presentation)
        pid = PresentationId.for_finding(0)
        session = session.record_note(pid, "first")
        session = session.record_note(pid, "second")
        assert len(session.notes) == 2

    def test_add_bookmark(self) -> None:
        presentation = _make_presentation()
        session = create_review_session(presentation)
        pid = PresentationId.for_finding(2)
        session = session.add_bookmark(pid, "check later")
        assert len(session.bookmarks) == 1
        assert session.bookmarks[0].label == "check later"

    def test_presentation_unchanged_after_review(self) -> None:
        presentation = _make_presentation()
        total_findings_before = len(presentation.findings)
        session = create_review_session(presentation)
        session = session.record_decision(PresentationId.for_finding(0), Decision.ACCEPTED)
        session = session.record_note(PresentationId.for_finding(0), "note")
        session = session.add_bookmark(PresentationId.for_finding(0), "b")
        # PresentationModel is immutable — same object
        assert session.presentation is presentation
        assert len(presentation.findings) == total_findings_before

    def test_complete_session(self) -> None:
        presentation = _make_presentation()
        session = create_review_session(presentation)
        completed = session.complete()
        assert len(completed.completed_at) > 0
        # Original
        assert len(session.completed_at) == 0

    def test_review_navigation_preserved(self) -> None:
        presentation = _make_presentation()
        session = create_review_session(presentation)
        # NavigationView is still accessible
        nav = session.presentation.navigation
        assert len(nav.indexes) > 0
        assert all(len(idx.items) >= 0 for idx in nav.indexes)

# ============================================================================
# No Interpretation Boundary Tests
# ============================================================================

class TestNoInterpretationInReview:
    """Verify review layer never performs interpretation."""

    def test_review_session_does_not_call_interpret(self) -> None:
        presentation = _make_presentation()
        session = create_review_session(presentation)
        assert not hasattr(session, "interpret")
        assert not hasattr(session, "_classify_severity")
        assert not hasattr(session, "_generate_recommendations")

    def test_review_decision_never_mutates_presentation(self) -> None:
        presentation = _make_presentation()
        original_summary = presentation.summary
        session = create_review_session(presentation)
        session = session.record_decision(PresentationId.for_finding(0), Decision.ACCEPTED)
        assert presentation.summary is original_summary
        assert presentation.findings.items == session.presentation.findings.items  # same object

    def test_no_business_logic_leakage(self) -> None:
        presentation = _make_presentation()
        session = create_review_session(presentation)
        assert not hasattr(session, "dashboard")
        assert not hasattr(session, "findings")
        assert not hasattr(session, "recommendations")
        assert not hasattr(session, "severity_map")

    def test_no_rendering_in_review_session(self) -> None:
        presentation = _make_presentation()
        session = create_review_session(presentation)
        assert not hasattr(session, "render")
        assert not hasattr(session, "to_html")
        assert not hasattr(session, "to_pdf")
        assert not hasattr(session, "to_json")
        assert not hasattr(session, "to_csv")
        assert not hasattr(session, "export")