"""Tests for CheckMate Export & Delivery Layer (IP-0008).

Verifies:
- ExportRequest / ExportResult immutability
- Exporter protocol conformance for all 4 exporters
- Determinism: identical inputs → identical outputs
- Content preserved exactly (byte-for-byte)
- Correct MIME handling
- Checksum stability
- Filename generation
- No rendering, no interpretation, no mutation
- All exporters consume only RenderedDocument
"""

from __future__ import annotations

import json

import pytest

from jarvis.applications.checkmate.rendering.context import RenderedDocument
from jarvis.applications.checkmate.export.request import (
    ExportRequest,
    ExportOptions,
    ExportMetadata,
    ExportResult,
    OutputPolicy,
    _compute_checksum,
)
from jarvis.applications.checkmate.export.protocol import Exporter
from jarvis.applications.checkmate.export.markdown import MarkdownExporter
from jarvis.applications.checkmate.export.html import HTMLExporter
from jarvis.applications.checkmate.export.json_exporter import JSONExporter
from jarvis.applications.checkmate.export.text import TextExporter

# ============================================================================
# Test Fixtures
# ============================================================================

@pytest.fixture
def markdown_document() -> RenderedDocument:
    return RenderedDocument(
        mime_type="text/markdown",
        content="# Test Report\n\nHello world.\n",
        title="Test Report",
        metadata=(("renderer", "MarkdownRenderer"),),
    )

@pytest.fixture
def html_document() -> RenderedDocument:
    return RenderedDocument(
        mime_type="text/html",
        content="<!DOCTYPE html><html><body><h1>Test</h1></body></html>",
        title="Test Report",
        metadata=(("renderer", "HTMLRenderer"),),
    )

@pytest.fixture
def json_document() -> RenderedDocument:
    return RenderedDocument(
        mime_type="application/json",
        content='{"title":"Test","count":3}\n',
        title="Test Report",
        metadata=(("renderer", "JSONRenderer"),),
    )

@pytest.fixture
def text_document() -> RenderedDocument:
    return RenderedDocument(
        mime_type="text/plain",
        content="TEST REPORT\n===========\nHello world.\n",
        title="Test Report",
        metadata=(("renderer", "TerminalRenderer"),),
    )

ALL_EXPORTERS = [MarkdownExporter, HTMLExporter, JSONExporter, TextExporter]

# ============================================================================
# Part A & B: ExportRequest and ExportResult
# ============================================================================

class TestExportRequest:
    """Verify immutable ExportRequest."""

    def test_request_is_frozen(self, markdown_document) -> None:
        req = ExportRequest(document=markdown_document)
        with pytest.raises(Exception):
            req.document = None

    def test_recommended_filename_default(self, markdown_document) -> None:
        req = ExportRequest(document=markdown_document)
        assert req.recommended_filename == "test_report"

    def test_recommended_filename_with_format(self, markdown_document) -> None:
        opts = ExportOptions(target_format="md")
        req = ExportRequest(document=markdown_document, options=opts)
        assert req.recommended_filename == "test_report.md"

    def test_recommended_filename_with_base(self, markdown_document) -> None:
        opts = ExportOptions(target_format="md", filename_base="my_report")
        req = ExportRequest(document=markdown_document, options=opts)
        assert req.recommended_filename == "my_report.md"

    def test_default_options(self, markdown_document) -> None:
        req = ExportRequest(document=markdown_document)
        assert req.options.target_format == ""
        assert req.options.filename_base == ""

class TestExportResult:
    """Verify immutable ExportResult."""

    def test_result_is_frozen(self) -> None:
        result = ExportResult(
            format="md",
            media_type="text/markdown",
            filename="report.md",
            content_bytes=b"hello",
            size_bytes=5,
            checksum="abc123",
        )
        with pytest.raises(Exception):
            result.content_bytes = b"changed"

    def test_result_has_all_fields(self) -> None:
        result = ExportResult(
            format="md",
            media_type="text/markdown",
            filename="report.md",
            content_bytes=b"hello",
            size_bytes=5,
            checksum="abc123",
            warnings=("test warning",),
        )
        assert result.format == "md"
        assert result.media_type == "text/markdown"
        assert result.filename == "report.md"
        assert result.content_bytes == b"hello"
        assert result.size_bytes == 5
        assert result.checksum == "abc123"
        assert result.warnings == ("test warning",)

    def test_result_default_warnings(self) -> None:
        result = ExportResult(
            format="md",
            media_type="text/markdown",
            filename="report.md",
            content_bytes=b"hello",
            size_bytes=5,
            checksum="abc123",
        )
        assert result.warnings == ()

# ============================================================================
# Part C: Exporter Protocol Conformance
# ============================================================================

class TestExporterProtocol:
    """Verify all exporters conform to the Exporter protocol."""

    @pytest.mark.parametrize("exporter_cls", ALL_EXPORTERS)
    def test_has_export_method(self, exporter_cls) -> None:
        e = exporter_cls()
        assert hasattr(e, "export")
        assert callable(e.export)

    @pytest.mark.parametrize("exporter_cls", ALL_EXPORTERS)
    def test_returns_export_result(self, exporter_cls, markdown_document) -> None:
        req = ExportRequest(document=markdown_document)
        result = exporter_cls().export(req)
        assert isinstance(result, ExportResult)

    @pytest.mark.parametrize("exporter_cls", ALL_EXPORTERS)
    def test_returns_non_empty_bytes(self, exporter_cls, markdown_document) -> None:
        req = ExportRequest(document=markdown_document)
        result = exporter_cls().export(req)
        assert len(result.content_bytes) > 0
        assert result.size_bytes > 0

    @pytest.mark.parametrize("exporter_cls", ALL_EXPORTERS)
    def test_returns_checksum(self, exporter_cls, markdown_document) -> None:
        req = ExportRequest(document=markdown_document)
        result = exporter_cls().export(req)
        assert len(result.checksum) > 0
        assert result.checksum == _compute_checksum(result.content_bytes)

# ============================================================================
# Determinism Tests
# ============================================================================

class TestDeterminism:
    """All exporters produce identical output for identical input."""

    @pytest.mark.parametrize("exporter_cls", ALL_EXPORTERS)
    def test_identical_input_identical_output(self, exporter_cls, markdown_document) -> None:
        req = ExportRequest(document=markdown_document)
        r1 = exporter_cls().export(req)
        r2 = exporter_cls().export(req)
        assert r1.content_bytes == r2.content_bytes
        assert r1.filename == r2.filename
        assert r1.checksum == r2.checksum

# ============================================================================
# Content Preservation Tests
# ============================================================================

class TestContentPreservation:
    """Exporters preserve content byte-for-byte from RenderedDocument."""

    @pytest.mark.parametrize("exporter_cls,fixture_name", [
        (MarkdownExporter, "markdown_document"),
        (HTMLExporter, "html_document"),
        (JSONExporter, "json_document"),
        (TextExporter, "text_document"),
    ])
    def test_content_preserved_exactly(self, exporter_cls, fixture_name, request) -> None:
        doc = request.getfixturevalue(fixture_name)
        req = ExportRequest(document=doc)
        result = exporter_cls().export(req)
        expected_bytes = doc.content.encode("utf-8")
        assert result.content_bytes == expected_bytes
        assert result.size_bytes == len(expected_bytes)

    @pytest.mark.parametrize("exporter_cls,fixture_name", [
        (MarkdownExporter, "markdown_document"),
        (HTMLExporter, "html_document"),
        (JSONExporter, "json_document"),
        (TextExporter, "text_document"),
    ])
    def test_content_matches_document(self, exporter_cls, fixture_name, request) -> None:
        doc = request.getfixturevalue(fixture_name)
        req = ExportRequest(document=doc)
        result = exporter_cls().export(req)
        decoded = result.content_bytes.decode("utf-8")
        assert decoded == doc.content

# ============================================================================
# MIME Handling Tests
# ============================================================================

class TestMimeHandling:
    """Exporters handle MIME types correctly."""

    def test_markdown_exporter_mime(self, markdown_document) -> None:
        req = ExportRequest(document=markdown_document)
        result = MarkdownExporter().export(req)
        assert result.media_type == "text/markdown"
        assert result.format == "md"

    def test_html_exporter_mime(self, html_document) -> None:
        req = ExportRequest(document=html_document)
        result = HTMLExporter().export(req)
        assert result.media_type == "text/html"
        assert result.format == "html"

    def test_json_exporter_mime(self, json_document) -> None:
        req = ExportRequest(document=json_document)
        result = JSONExporter().export(req)
        assert result.media_type == "application/json"
        assert result.format == "json"

    def test_text_exporter_mime(self, text_document) -> None:
        req = ExportRequest(document=text_document)
        result = TextExporter().export(req)
        assert result.media_type == "text/plain"
        assert result.format == "txt"

# ============================================================================
# Checksum Stability Tests
# ============================================================================

class TestChecksumStability:
    """Checksums are deterministic and match content."""

    @pytest.mark.parametrize("exporter_cls,fixture_name", [
        (MarkdownExporter, "markdown_document"),
        (HTMLExporter, "html_document"),
        (JSONExporter, "json_document"),
        (TextExporter, "text_document"),
    ])
    def test_checksum_matches_content(self, exporter_cls, fixture_name, request) -> None:
        doc = request.getfixturevalue(fixture_name)
        req = ExportRequest(document=doc)
        result = exporter_cls().export(req)
        expected = _compute_checksum(result.content_bytes)
        assert result.checksum == expected

    @pytest.mark.parametrize("exporter_cls,fixture_name", [
        (MarkdownExporter, "markdown_document"),
        (HTMLExporter, "html_document"),
        (JSONExporter, "json_document"),
        (TextExporter, "text_document"),
    ])
    def test_checksum_stable(self, exporter_cls, fixture_name, request) -> None:
        doc = request.getfixturevalue(fixture_name)
        req = ExportRequest(document=doc)
        r1 = exporter_cls().export(req)
        r2 = exporter_cls().export(req)
        assert r1.checksum == r2.checksum

# ============================================================================
# No Rendering / No Interpretation / No Mutation Tests
# ============================================================================

class TestNoRendering:
    """Exporters never perform rendering, interpretation, or mutation."""

    @pytest.mark.parametrize("exporter_cls", ALL_EXPORTERS)
    def test_document_unchanged_after_export(self, exporter_cls, markdown_document) -> None:
        req = ExportRequest(document=markdown_document)
        content_before = markdown_document.content
        exporter_cls().export(req)
        assert markdown_document.content == content_before

    @pytest.mark.parametrize("exporter_cls", ALL_EXPORTERS)
    def test_no_render_methods(self, exporter_cls) -> None:
        e = exporter_cls()
        assert not hasattr(e, "render")
        assert not hasattr(e, "interpret")
        assert not hasattr(e, "validate")
        assert not hasattr(e, "review")

    @pytest.mark.parametrize("exporter_cls", ALL_EXPORTERS)
    def test_no_filesystem_methods(self, exporter_cls) -> None:
        e = exporter_cls()
        assert not hasattr(e, "save")
        assert not hasattr(e, "write_file")
        assert not hasattr(e, "open")

    @pytest.mark.parametrize("exporter_cls", ALL_EXPORTERS)
    def test_no_application_state_access(self, exporter_cls) -> None:
        e = exporter_cls()
        assert not hasattr(e, "presentation")
        assert not hasattr(e, "review")
        assert not hasattr(e, "context")

# ============================================================================
# Filename Tests
# ============================================================================

class TestFilename:
    """Exporters generate correct filenames."""

    def test_markdown_filename(self, markdown_document) -> None:
        opts = ExportOptions(target_format="md")
        req = ExportRequest(document=markdown_document, options=opts)
        result = MarkdownExporter().export(req)
        assert result.filename == "test_report.md"

    def test_html_filename(self, html_document) -> None:
        opts = ExportOptions(target_format="html")
        req = ExportRequest(document=html_document, options=opts)
        result = HTMLExporter().export(req)
        assert result.filename == "test_report.html"

    def test_json_filename(self, json_document) -> None:
        opts = ExportOptions(target_format="json")
        req = ExportRequest(document=json_document, options=opts)
        result = JSONExporter().export(req)
        assert result.filename == "test_report.json"

    def test_text_filename(self, text_document) -> None:
        opts = ExportOptions(target_format="txt")
        req = ExportRequest(document=text_document, options=opts)
        result = TextExporter().export(req)
        assert result.filename == "test_report.txt"

    def test_custom_filename_base(self, markdown_document) -> None:
        opts = ExportOptions(target_format="md", filename_base="my_custom_name")
        req = ExportRequest(document=markdown_document, options=opts)
        result = MarkdownExporter().export(req)
        assert result.filename == "my_custom_name.md"

# ============================================================================
# OutputPolicy Tests
# ============================================================================

class TestOutputPolicy:
    """OutputPolicy handles output configuration."""

    def test_default_policy(self) -> None:
        p = OutputPolicy()
        assert p.directory == "."
        assert p.create_directory is True
        assert p.overwrite is True

    def test_custom_policy(self) -> None:
        p = OutputPolicy(directory="/tmp/output", create_directory=False, overwrite=False)
        assert p.directory == "/tmp/output"
        assert p.create_directory is False
        assert p.overwrite is False

# ============================================================================
# Cross-Exporter Consistency Tests
# ============================================================================

class TestCrossExporterConsistency:
    """Verify all exporters represent the same RenderedDocument."""

    def test_all_exporters_same_content(self, markdown_document) -> None:
        """Different exporters on same doc should preserve content bytes."""
        for cls in ALL_EXPORTERS:
            req = ExportRequest(document=markdown_document)
            result = cls().export(req)
            assert result.content_bytes == markdown_document.content.encode("utf-8")

    def test_all_exporters_unique_formats(self) -> None:
        doc = RenderedDocument(mime_type="text/plain", content="x", title="test")
        req = ExportRequest(document=doc)
        formats = set()
        for cls in ALL_EXPORTERS:
            result = cls().export(req)
            formats.add(result.format)
        assert len(formats) == len(ALL_EXPORTERS)

    def test_all_exporters_produce_checksums(self, markdown_document) -> None:
        for cls in ALL_EXPORTERS:
            req = ExportRequest(document=markdown_document)
            result = cls().export(req)
            assert len(result.checksum) == 64  # SHA-256 hex length