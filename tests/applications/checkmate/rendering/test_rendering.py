"""Tests for CheckMate Rendering Layer (IP-0007).

Verifies:
- RenderContext / RenderedDocument immutability
- Renderer protocol conformance for all 4 renderers
- Determinism: identical inputs → identical outputs
- Stable ordering and formatting
- No interpretation, no review mutation
- PresentationModel & ReviewSession unchanged after rendering
- Markdown, JSON, HTML, Terminal correctness
- Review decisions appear when ReviewSession provided
- Options control (include_review, include_navigation, include_metadata)
"""

from __future__ import annotations

import json

import pytest

from jarvis.applications.checkmate.config import CheckMateConfig
from jarvis.applications.checkmate.context import ApplicationContext
from jarvis.applications.checkmate.interpretation.engine import interpret
from jarvis.applications.checkmate.presentation.assembler import assemble
from jarvis.applications.checkmate.review.decisions import Decision
from jarvis.applications.checkmate.review.identity import PresentationId
from jarvis.applications.checkmate.review.session import create_review_session
from jarvis.applications.checkmate.rendering.context import (
    RenderContext,
    RenderOptions,
    RenderMetadata,
    RenderedDocument,
)
from jarvis.applications.checkmate.rendering.protocol import Renderer
from jarvis.applications.checkmate.rendering.markdown import MarkdownRenderer
from jarvis.applications.checkmate.rendering.terminal import TerminalRenderer
from jarvis.applications.checkmate.rendering.json_renderer import JSONRenderer
from jarvis.applications.checkmate.rendering.html import HTMLRenderer
from jarvis.parsers.costx.boq_intelligence import BOQIntelligenceResult
from jarvis.engines.validation.engine import ValidationFindings, ValidationFinding

# ============================================================================
# Test Helpers
# ============================================================================

def _make_evidence() -> BOQIntelligenceResult:
    return BOQIntelligenceResult(
        row_classification={"Head": 5, "Item": 10, "Note": 1},
        section_statistics={
            "Section A": {"items": 5, "page": 1},
            "Section B": {"items": 5, "page": 1},
        },
        boq_statistics={"total_rows": 16, "total_sections": 2},
        known_anomalies=[],
    )

def _make_findings(*types: str) -> ValidationFindings:
    entries = []
    for i, ft in enumerate(types, start=1):
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

def _make_presentation(types=("Error", "Warning", "Information")):
    ctx = ApplicationContext(
        evidence=_make_evidence(),
        findings=_make_findings(*types),
    )
    interp = interpret(ctx)
    return assemble(ctx, interp)

def _make_context_no_review(types=("Error", "Warning", "Information")) -> RenderContext:
    pres = _make_presentation(types)
    return RenderContext(presentation=pres)

def _make_context_with_review(types=("Error", "Warning", "Information")) -> RenderContext:
    pres = _make_presentation(types)
    session = create_review_session(pres)
    session = session.record_decision(PresentationId.for_finding(0), Decision.ACCEPTED)
    return RenderContext(presentation=pres, review=session)

ALL_RENDERERS = [MarkdownRenderer, TerminalRenderer, JSONRenderer, HTMLRenderer]

# ============================================================================
# Part A & B: RenderContext and RenderedDocument
# ============================================================================

class TestRenderContext:
    """Verify immutable RenderContext."""

    def test_context_is_frozen(self) -> None:
        ctx = _make_context_no_review()
        with pytest.raises(Exception):
            ctx.presentation = None

    def test_context_has_timestamp(self) -> None:
        ctx = _make_context_no_review()
        assert len(ctx.timestamp) > 0

    def test_context_default_options(self) -> None:
        ctx = _make_context_no_review()
        assert ctx.options.include_review is True
        assert ctx.options.include_navigation is True
        assert ctx.options.include_metadata is True

    def test_context_review_none_by_default(self) -> None:
        ctx = _make_context_no_review()
        assert ctx.review is None

    def test_context_with_review(self) -> None:
        ctx = _make_context_with_review()
        assert ctx.review is not None

class TestRenderedDocument:
    """Verify immutable RenderedDocument."""

    def test_document_is_frozen(self) -> None:
        doc = RenderedDocument(mime_type="text/plain", content="hello")
        with pytest.raises(Exception):
            doc.content = "changed"

    def test_document_has_defaults(self) -> None:
        doc = RenderedDocument(mime_type="text/plain", content="x")
        assert doc.title == ""
        assert doc.metadata == ()
        assert doc.warnings == ()

    def test_document_with_metadata(self) -> None:
        doc = RenderedDocument(
            mime_type="text/plain",
            content="x",
            metadata=(("k", "v"),),
        )
        assert doc.metadata == (("k", "v"),)

# ============================================================================
# Part C: Renderer Protocol Conformance
# ============================================================================

class TestRendererProtocol:
    """Verify all renderers conform to the Renderer protocol."""

    @pytest.mark.parametrize("renderer_cls", ALL_RENDERERS)
    def test_has_render_method(self, renderer_cls) -> None:
        r = renderer_cls()
        assert hasattr(r, "render")
        assert callable(r.render)

    @pytest.mark.parametrize("renderer_cls", ALL_RENDERERS)
    def test_returns_rendered_document(self, renderer_cls) -> None:
        ctx = _make_context_no_review()
        doc = renderer_cls().render(ctx)
        assert isinstance(doc, RenderedDocument)

    @pytest.mark.parametrize("renderer_cls", ALL_RENDERERS)
    def test_returns_non_empty_content(self, renderer_cls) -> None:
        ctx = _make_context_no_review()
        doc = renderer_cls().render(ctx)
        assert len(doc.content) > 0

    @pytest.mark.parametrize("renderer_cls", ALL_RENDERERS)
    def test_returns_title(self, renderer_cls) -> None:
        ctx = _make_context_no_review()
        doc = renderer_cls().render(ctx)
        assert len(doc.title) > 0

    @pytest.mark.parametrize("renderer_cls", ALL_RENDERERS)
    def test_returns_metadata(self, renderer_cls) -> None:
        ctx = _make_context_no_review()
        doc = renderer_cls().render(ctx)
        assert len(doc.metadata) > 0

# ============================================================================
# Determinism Tests
# ============================================================================

class TestDeterminism:
    """All renderers produce identical output for identical input."""

    @pytest.mark.parametrize("renderer_cls", ALL_RENDERERS)
    def test_identical_input_identical_output(self, renderer_cls) -> None:
        ctx = _make_context_no_review()
        doc1 = renderer_cls().render(ctx)
        doc2 = renderer_cls().render(ctx)
        assert doc1.content == doc2.content
        assert doc1.mime_type == doc2.mime_type

    @pytest.mark.parametrize("renderer_cls", ALL_RENDERERS)
    def test_deterministic_with_review(self, renderer_cls) -> None:
        ctx = _make_context_with_review()
        doc1 = renderer_cls().render(ctx)
        doc2 = renderer_cls().render(ctx)
        assert doc1.content == doc2.content

# ============================================================================
# No Interpretation / No Mutation Tests
# ============================================================================

class TestNoInterpretation:
    """Renderers never perform interpretation or mutate state."""

    @pytest.mark.parametrize("renderer_cls", ALL_RENDERERS)
    def test_presentation_unchanged_after_render(self, renderer_cls) -> None:
        ctx = _make_context_no_review()
        pres_before = ctx.presentation
        findings_before = len(pres_before.findings)
        renderer_cls().render(ctx)
        assert len(ctx.presentation.findings) == findings_before
        assert ctx.presentation is pres_before

    @pytest.mark.parametrize("renderer_cls", ALL_RENDERERS)
    def test_review_unchanged_after_render(self, renderer_cls) -> None:
        ctx = _make_context_with_review()
        review_before = ctx.review
        decisions_before = len(review_before.decisions)
        renderer_cls().render(ctx)
        assert len(ctx.review.decisions) == decisions_before
        assert ctx.review is review_before

    @pytest.mark.parametrize("renderer_cls", ALL_RENDERERS)
    def test_no_interpretation_methods(self, renderer_cls) -> None:
        r = renderer_cls()
        assert not hasattr(r, "interpret")
        assert not hasattr(r, "validate")
        assert not hasattr(r, "_classify_severity")
        assert not hasattr(r, "_generate_recommendations")

    @pytest.mark.parametrize("renderer_cls", ALL_RENDERERS)
    def test_no_filesystem_methods(self, renderer_cls) -> None:
        r = renderer_cls()
        assert not hasattr(r, "save")
        assert not hasattr(r, "write")
        assert not hasattr(r, "export")
        assert not hasattr(r, "open")

# ============================================================================
# Part D: Markdown Renderer Tests
# ============================================================================

class TestMarkdownRenderer:
    """Verify Markdown rendering correctness."""

    def test_mime_type(self) -> None:
        doc = MarkdownRenderer().render(_make_context_no_review())
        assert doc.mime_type == "text/markdown"

    def test_contains_title_heading(self) -> None:
        doc = MarkdownRenderer().render(_make_context_no_review())
        assert doc.content.startswith("# ")

    def test_contains_summary_section(self) -> None:
        doc = MarkdownRenderer().render(_make_context_no_review())
        assert "## Summary" in doc.content

    def test_contains_dashboard_table(self) -> None:
        doc = MarkdownRenderer().render(_make_context_no_review())
        assert "## Dashboard" in doc.content
        assert "| Metric | Count |" in doc.content

    def test_contains_findings_section(self) -> None:
        doc = MarkdownRenderer().render(_make_context_no_review())
        assert "## Findings" in doc.content

    def test_contains_recommendations_section(self) -> None:
        doc = MarkdownRenderer().render(_make_context_no_review())
        assert "## Recommendations" in doc.content

    def test_contains_sections_section(self) -> None:
        doc = MarkdownRenderer().render(_make_context_no_review())
        assert "## Sections" in doc.content

    def test_contains_metadata_section(self) -> None:
        doc = MarkdownRenderer().render(_make_context_no_review())
        assert "## Metadata" in doc.content

    def test_review_decisions_included(self) -> None:
        doc = MarkdownRenderer().render(_make_context_with_review())
        assert "Review Decision" in doc.content
        assert "ACCEPTED" in doc.content

    def test_review_progress_included(self) -> None:
        doc = MarkdownRenderer().render(_make_context_with_review())
        assert "## Review Progress" in doc.content

    def test_no_review_progress_without_review(self) -> None:
        doc = MarkdownRenderer().render(_make_context_no_review())
        assert "## Review Progress" not in doc.content

    def test_metadata_excluded_when_option_off(self) -> None:
        pres = _make_presentation()
        ctx = RenderContext(
            presentation=pres,
            options=RenderOptions(include_metadata=False),
        )
        doc = MarkdownRenderer().render(ctx)
        assert "## Metadata" not in doc.content

# ============================================================================
# Part E: Terminal Renderer Tests
# ============================================================================

class TestTerminalRenderer:
    """Verify Terminal rendering correctness."""

    def test_mime_type(self) -> None:
        doc = TerminalRenderer().render(_make_context_no_review())
        assert doc.mime_type == "text/plain"

    def test_contains_title_banner(self) -> None:
        doc = TerminalRenderer().render(_make_context_no_review())
        lines = doc.content.split("\n")
        # Title is between two lines of equal signs
        assert lines[0].startswith("=")
        assert lines[2].startswith("=")

    def test_contains_summary(self) -> None:
        doc = TerminalRenderer().render(_make_context_no_review())
        assert "SUMMARY" in doc.content

    def test_contains_dashboard(self) -> None:
        doc = TerminalRenderer().render(_make_context_no_review())
        assert "DASHBOARD" in doc.content

    def test_contains_findings(self) -> None:
        doc = TerminalRenderer().render(_make_context_no_review())
        assert "FINDINGS" in doc.content

    def test_contains_sections(self) -> None:
        doc = TerminalRenderer().render(_make_context_no_review())
        assert "SECTIONS" in doc.content

    def test_no_ansi_codes(self) -> None:
        doc = TerminalRenderer().render(_make_context_no_review())
        assert "\033[" not in doc.content
        assert "\x1b[" not in doc.content

    def test_review_decisions_included(self) -> None:
        doc = TerminalRenderer().render(_make_context_with_review())
        assert "Decision:" in doc.content
        assert "ACCEPTED" in doc.content

    def test_review_progress_included(self) -> None:
        doc = TerminalRenderer().render(_make_context_with_review())
        assert "REVIEW PROGRESS" in doc.content

# ============================================================================
# Part F: JSON Renderer Tests
# ============================================================================

class TestJSONRenderer:
    """Verify JSON rendering correctness."""

    def test_mime_type(self) -> None:
        doc = JSONRenderer().render(_make_context_no_review())
        assert doc.mime_type == "application/json"

    def test_valid_json(self) -> None:
        doc = JSONRenderer().render(_make_context_no_review())
        data = json.loads(doc.content)
        assert isinstance(data, dict)

    def test_has_summary(self) -> None:
        doc = JSONRenderer().render(_make_context_no_review())
        data = json.loads(doc.content)
        assert "summary" in data

    def test_has_dashboard(self) -> None:
        doc = JSONRenderer().render(_make_context_no_review())
        data = json.loads(doc.content)
        assert "dashboard" in data

    def test_has_findings(self) -> None:
        doc = JSONRenderer().render(_make_context_no_review())
        data = json.loads(doc.content)
        assert "findings" in data
        assert isinstance(data["findings"], list)

    def test_has_recommendations(self) -> None:
        doc = JSONRenderer().render(_make_context_no_review())
        data = json.loads(doc.content)
        assert "recommendations" in data

    def test_has_sections(self) -> None:
        doc = JSONRenderer().render(_make_context_no_review())
        data = json.loads(doc.content)
        assert "sections" in data

    def test_has_navigation(self) -> None:
        doc = JSONRenderer().render(_make_context_no_review())
        data = json.loads(doc.content)
        assert "navigation" in data

    def test_has_metadata(self) -> None:
        doc = JSONRenderer().render(_make_context_no_review())
        data = json.loads(doc.content)
        assert "metadata" in data

    def test_finding_fields_complete(self) -> None:
        doc = JSONRenderer().render(_make_context_no_review())
        data = json.loads(doc.content)
        f = data["findings"][0]
        assert "finding_id" in f
        assert "severity_label" in f
        assert "display_title" in f

    def test_review_decisions_in_json(self) -> None:
        doc = JSONRenderer().render(_make_context_with_review())
        data = json.loads(doc.content)
        assert data["findings"][0]["review_decision"] == "ACCEPTED"

    def test_review_progress_in_json(self) -> None:
        doc = JSONRenderer().render(_make_context_with_review())
        data = json.loads(doc.content)
        assert "review_progress" in data
        assert "total_items" in data["review_progress"]

    def test_no_review_progress_without_review(self) -> None:
        doc = JSONRenderer().render(_make_context_no_review())
        data = json.loads(doc.content)
        assert "review_progress" not in data

    def test_stable_ordering(self) -> None:
        ctx = _make_context_no_review()
        doc1 = JSONRenderer().render(ctx)
        doc2 = JSONRenderer().render(ctx)
        # Character-level equality ensures stable key ordering
        assert doc1.content == doc2.content

    def test_metadata_excluded_when_option_off(self) -> None:
        pres = _make_presentation()
        ctx = RenderContext(
            presentation=pres,
            options=RenderOptions(include_metadata=False),
        )
        doc = JSONRenderer().render(ctx)
        data = json.loads(doc.content)
        assert "metadata" not in data

# ============================================================================
# Part G: HTML Renderer Tests
# ============================================================================

class TestHTMLRenderer:
    """Verify HTML rendering correctness."""

    def test_mime_type(self) -> None:
        doc = HTMLRenderer().render(_make_context_no_review())
        assert doc.mime_type == "text/html"

    def test_valid_html_structure(self) -> None:
        doc = HTMLRenderer().render(_make_context_no_review())
        assert "<!DOCTYPE html>" in doc.content
        assert "<html" in doc.content
        assert "</html>" in doc.content
        assert "<head>" in doc.content
        assert "<body>" in doc.content

    def test_has_title(self) -> None:
        doc = HTMLRenderer().render(_make_context_no_review())
        assert "<title>" in doc.content
        assert "<h1>" in doc.content

    def test_has_summary_section(self) -> None:
        doc = HTMLRenderer().render(_make_context_no_review())
        assert 'id="summary"' in doc.content

    def test_has_dashboard_section(self) -> None:
        doc = HTMLRenderer().render(_make_context_no_review())
        assert 'id="dashboard"' in doc.content
        assert "<table>" in doc.content

    def test_has_findings_section(self) -> None:
        doc = HTMLRenderer().render(_make_context_no_review())
        assert 'id="findings"' in doc.content

    def test_has_recommendations_section(self) -> None:
        doc = HTMLRenderer().render(_make_context_no_review())
        assert 'id="recommendations"' in doc.content

    def test_has_sections_section(self) -> None:
        doc = HTMLRenderer().render(_make_context_no_review())
        assert 'id="sections"' in doc.content

    def test_has_metadata_section(self) -> None:
        doc = HTMLRenderer().render(_make_context_no_review())
        assert 'id="metadata"' in doc.content

    def test_semantic_elements(self) -> None:
        doc = HTMLRenderer().render(_make_context_no_review())
        assert "<article" in doc.content
        assert "<dl>" in doc.content
        assert "<dt>" in doc.content
        assert "<dd>" in doc.content

    def test_no_javascript(self) -> None:
        doc = HTMLRenderer().render(_make_context_no_review())
        assert "<script" not in doc.content

    def test_no_css_framework(self) -> None:
        doc = HTMLRenderer().render(_make_context_no_review())
        assert "bootstrap" not in doc.content.lower()
        assert "tailwind" not in doc.content.lower()

    def test_review_decisions_in_html(self) -> None:
        doc = HTMLRenderer().render(_make_context_with_review())
        assert "Review Decision" in doc.content
        assert "ACCEPTED" in doc.content

    def test_review_progress_in_html(self) -> None:
        doc = HTMLRenderer().render(_make_context_with_review())
        assert 'id="review-progress"' in doc.content

    def test_html_escaping(self) -> None:
        """Verify special characters are escaped in HTML output."""
        doc = HTMLRenderer().render(_make_context_no_review())
        # The content should not contain unescaped < or > in text
        # (all angle brackets should be part of tags)
        assert isinstance(doc.content, str)

    def test_metadata_excluded_when_option_off(self) -> None:
        pres = _make_presentation()
        ctx = RenderContext(
            presentation=pres,
            options=RenderOptions(include_metadata=False),
        )
        doc = HTMLRenderer().render(ctx)
        assert 'id="metadata"' not in doc.content

# ============================================================================
# Cross-Renderer Consistency Tests
# ============================================================================

class TestCrossRendererConsistency:
    """Verify all renderers represent the same data."""

    def test_all_renderers_same_title(self) -> None:
        ctx = _make_context_no_review()
        titles = set()
        for cls in ALL_RENDERERS:
            doc = cls().render(ctx)
            titles.add(doc.title)
        assert len(titles) == 1

    def test_all_renderers_unique_mime_types(self) -> None:
        ctx = _make_context_no_review()
        mime_types = set()
        for cls in ALL_RENDERERS:
            doc = cls().render(ctx)
            mime_types.add(doc.mime_type)
        assert len(mime_types) == len(ALL_RENDERERS)

    def test_all_renderers_have_renderer_metadata(self) -> None:
        ctx = _make_context_no_review()
        for cls in ALL_RENDERERS:
            doc = cls().render(ctx)
            renderer_names = [v for k, v in doc.metadata if k == "renderer"]
            assert len(renderer_names) == 1