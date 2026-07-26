"""Tests for CheckMate CLI pipeline runner (CP-0001).

Verifies:
- Renderer resolution
- Exporter resolution
- PipelineRunner render, export, and render_and_export methods
- Error cases for unknown renderers/exporters
- Pipeline consumes frozen architecture (no new layers)
"""

from __future__ import annotations

import pytest

from jarvis.applications.checkmate.cli.pipeline import (
    PipelineRunner,
    get_renderer,
    get_exporter,
)
from jarvis.applications.checkmate.rendering.context import RenderedDocument
from jarvis.applications.checkmate.rendering.protocol import Renderer
from jarvis.applications.checkmate.export.protocol import Exporter
from jarvis.applications.checkmate.export.request import ExportResult
from jarvis.applications.checkmate.presentation.models import (
    PresentationModel,
    DashboardView,
    SummaryView,
    FindingView,
    RecommendationView,
    SectionView,
    NavigationView,
    MetadataView,
)
from jarvis.applications.checkmate.review.session import ReviewSession

# ============================================================================
# Test Fixtures
# ============================================================================

@pytest.fixture
def presentation() -> PresentationModel:
    return PresentationModel(
        dashboard=DashboardView(
            total_findings=0,
            total_recommendations=0,
            high_severity_count=0,
            medium_severity_count=0,
            low_severity_count=0,
            total_sections=0,
        ),
        summary=SummaryView(
            application_title="Test CheckMate",
            application_version="0.0.1-test",
            execution_timestamp="2026-07-26T00:00:00",
            finding_summary="No findings.",
            recommendation_summary="No recommendations.",
            overall_severity="LOW",
        ),
        findings=FindingView(items=()),
        recommendations=RecommendationView(items=()),
        sections=SectionView(items=()),
        navigation=NavigationView(indexes=()),
        metadata=MetadataView(
            runtime_id="test-run-id",
            application_name="CheckMate Test",
            application_version="0.0.1-test",
            contract_version="1.0.0",
            engine_version="1.0.0",
            execution_timestamp="2026-07-26T00:00:00",
            diagnostic_flags=(),
        ),
    )

# ============================================================================
# Test: Renderer/Exporter Resolution
# ============================================================================

class TestRendererResolution:
    def test_get_renderer_markdown(self) -> None:
        r = get_renderer("markdown")
        assert r is not None
        assert hasattr(r, "render")

    def test_get_renderer_html(self) -> None:
        r = get_renderer("html")
        assert r is not None
        assert hasattr(r, "render")

    def test_get_renderer_json(self) -> None:
        r = get_renderer("json")
        assert r is not None
        assert hasattr(r, "render")

    def test_get_renderer_terminal(self) -> None:
        r = get_renderer("terminal")
        assert r is not None
        assert hasattr(r, "render")

    def test_get_renderer_unknown_raises(self) -> None:
        with pytest.raises(ValueError, match="Unknown renderer"):
            get_renderer("unknown")

class TestExporterResolution:
    def test_get_exporter_md(self) -> None:
        e = get_exporter("md")
        assert e is not None
        assert hasattr(e, "export")

    def test_get_exporter_html(self) -> None:
        e = get_exporter("html")
        assert e is not None
        assert hasattr(e, "export")

    def test_get_exporter_json(self) -> None:
        e = get_exporter("json")
        assert e is not None
        assert hasattr(e, "export")

    def test_get_exporter_txt(self) -> None:
        e = get_exporter("txt")
        assert e is not None
        assert hasattr(e, "export")

    def test_get_exporter_unknown_raises(self) -> None:
        with pytest.raises(ValueError, match="Unknown exporter"):
            get_exporter("unknown")

# ============================================================================
# Test: PipelineRunner
# ============================================================================

class TestPipelineRunner:
    def test_runner_instantiation(self) -> None:
        runner = PipelineRunner()
        assert runner is not None

    def test_render_returns_rendered_document(self, presentation) -> None:
        runner = PipelineRunner()
        doc = runner.render(presentation, renderer_name="markdown")
        assert isinstance(doc, RenderedDocument)
        assert doc.mime_type == "text/markdown"
        assert len(doc.content) > 0

    def test_render_all_four_renderers(self, presentation) -> None:
        runner = PipelineRunner()
        for name in ("markdown", "html", "json", "terminal"):
            doc = runner.render(presentation, renderer_name=name)
            assert isinstance(doc, RenderedDocument)
            assert len(doc.content) > 0

    def test_render_with_review(self, presentation) -> None:
        from jarvis.applications.checkmate.review.session import create_review_session
        session = create_review_session(presentation)
        runner = PipelineRunner()
        doc = runner.render(presentation, renderer_name="markdown", review=session, include_review=True)
        assert isinstance(doc, RenderedDocument)
        assert len(doc.content) > 0

    def test_export_returns_export_result(self, presentation) -> None:
        runner = PipelineRunner()
        doc = runner.render(presentation, renderer_name="markdown")
        result = runner.export(doc, exporter_name="md")
        assert isinstance(result, ExportResult)
        assert len(result.content_bytes) > 0
        assert result.format == "md"

    def test_export_all_exporters(self, presentation) -> None:
        runner = PipelineRunner()
        doc = runner.render(presentation, renderer_name="markdown")
        for fmt in ("md", "html", "json", "txt"):
            result = runner.export(doc, exporter_name=fmt)
            assert isinstance(result, ExportResult)
            assert len(result.content_bytes) > 0

    def test_render_and_export(self, presentation) -> None:
        runner = PipelineRunner()
        result = runner.render_and_export(
            presentation,
            renderer_name="markdown",
            exporter_name="md",
            filename_base="test",
        )
        assert isinstance(result, ExportResult)
        assert result.format == "md"
        assert len(result.content_bytes) > 0

    def test_render_and_export_with_review(self, presentation) -> None:
        from jarvis.applications.checkmate.review.session import create_review_session
        session = create_review_session(presentation)
        runner = PipelineRunner()
        result = runner.render_and_export(
            presentation,
            renderer_name="terminal",
            exporter_name="txt",
            review=session,
            filename_base="test",
            include_review=True,
        )
        assert isinstance(result, ExportResult)
        assert result.format == "txt"
        assert len(result.content_bytes) > 0

# ============================================================================
# Test: Determinism
# ============================================================================

class TestDeterminism:
    def test_render_deterministic(self, presentation) -> None:
        runner = PipelineRunner()
        doc1 = runner.render(presentation, renderer_name="markdown")
        doc2 = runner.render(presentation, renderer_name="markdown")
        assert doc1.content == doc2.content
        assert doc1.mime_type == doc2.mime_type

    def test_export_deterministic(self, presentation) -> None:
        runner = PipelineRunner()
        doc = runner.render(presentation, renderer_name="markdown")
        r1 = runner.export(doc, exporter_name="md")
        r2 = runner.export(doc, exporter_name="md")
        assert r1.content_bytes == r2.content_bytes
        assert r1.checksum == r2.checksum

# ============================================================================
# Test: No Architecture Violation
# ============================================================================

class TestNoArchitectureViolation:
    def test_pipeline_runner_is_not_a_renderer(self) -> None:
        """PipelineRunner is a consumer, not a renderer."""
        runner = PipelineRunner()
        assert not hasattr(runner, "render_to_pdf")
        assert not hasattr(runner, "interpret")
        assert not hasattr(runner, "validate")

    def test_pipeline_runner_has_no_architecture_access(self) -> None:
        """PipelineRunner doesn't directly access interpretation or evidence."""
        runner = PipelineRunner()
        assert not hasattr(runner, "evidence")
        assert not hasattr(runner, "interpretation")
        assert not hasattr(runner, "context")