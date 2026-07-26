"""Tests for CheckMate CLI argument parser (CP-0001).

Verifies:
- Argument parsing for all commands
- Valid and invalid renderer/exporter selections
- Default values
- Help and version output
"""

from __future__ import annotations

import pytest

from jarvis.applications.checkmate.cli.parser import (
    build_parser,
    parse_args,
    CLIOptions,
    VALID_RENDERERS,
    VALID_EXPORTERS,
    APPLICATION_VERSION,
    ARCHITECTURE_VERSION,
)

# ============================================================================
# Test: Parser Construction
# ============================================================================

class TestParserConstruction:
    """Verify parser is constructed correctly."""

    def test_build_parser_returns_parser(self) -> None:
        parser = build_parser()
        assert parser is not None
        assert parser.prog == "checkmate"

    def test_parser_has_analyze_subcommand(self) -> None:
        parser = build_parser()
        opts = parse_args(["analyze", "test.xlsx"])
        assert opts.command == "analyze"

    def test_parser_has_render_subcommand(self) -> None:
        opts = parse_args(["render", "test.json"])
        assert opts.command == "render"

    def test_parser_has_export_subcommand(self) -> None:
        opts = parse_args(["export", "test.md"])
        assert opts.command == "export"

    def test_parser_has_version_subcommand(self) -> None:
        opts = parse_args(["version"])
        assert opts.command == "version"

# ============================================================================
# Test: analyze command
# ============================================================================

class TestAnalyzeCommand:
    def test_analyze_with_input_path(self) -> None:
        opts = parse_args(["analyze", "workbook.xlsx"])
        assert opts.command == "analyze"
        assert opts.input_path == "workbook.xlsx"

    def test_analyze_with_renderer(self) -> None:
        opts = parse_args(["analyze", "workbook.xlsx", "--renderer", "markdown"])
        assert opts.renderer == "markdown"

    def test_analyze_with_exporter(self) -> None:
        opts = parse_args(["analyze", "workbook.xlsx", "--export", "json"])
        assert opts.exporter == "json"

    def test_analyze_with_review(self) -> None:
        opts = parse_args(["analyze", "workbook.xlsx", "--review"])
        assert opts.enable_review is True

    def test_analyze_with_no_review(self) -> None:
        opts = parse_args(["analyze", "workbook.xlsx", "--no-review"])
        assert opts.enable_review is False

    def test_analyze_review_disabled_by_default(self) -> None:
        opts = parse_args(["analyze", "workbook.xlsx"])
        assert opts.enable_review is False

    def test_analyze_with_output(self) -> None:
        opts = parse_args(["analyze", "workbook.xlsx", "--output", "/tmp/report.txt"])
        assert opts.output_path == "/tmp/report.txt"

    def test_analyze_with_short_options(self) -> None:
        opts = parse_args(["analyze", "workbook.xlsx", "-r", "html", "-e", "html", "-o", "/tmp/report.html"])
        assert opts.renderer == "html"
        assert opts.exporter == "html"
        assert opts.output_path == "/tmp/report.html"

    def test_analyze_with_quiet(self) -> None:
        opts = parse_args(["analyze", "workbook.xlsx", "--quiet"])
        assert opts.quiet is True

    def test_analyze_with_verbose(self) -> None:
        opts = parse_args(["analyze", "workbook.xlsx", "--verbose"])
        assert opts.verbose is True

    def test_analyze_default_renderer_terminal(self) -> None:
        opts = parse_args(["analyze", "workbook.xlsx"])
        assert opts.renderer == "terminal"

    def test_analyze_default_exporter_txt(self) -> None:
        opts = parse_args(["analyze", "workbook.xlsx"])
        assert opts.exporter == "txt"

# ============================================================================
# Test: render command
# ============================================================================

class TestRenderCommand:
    def test_render_with_defaults(self) -> None:
        opts = parse_args(["render", "model.json"])
        assert opts.command == "render"
        assert opts.input_path == "model.json"
        assert opts.renderer == "terminal"

    def test_render_with_specific_renderer(self) -> None:
        opts = parse_args(["render", "model.json", "--renderer", "json"])
        assert opts.renderer == "json"

# ============================================================================
# Test: export command
# ============================================================================

class TestExportCommand:
    def test_export_with_defaults(self) -> None:
        opts = parse_args(["export", "document.md"])
        assert opts.command == "export"
        assert opts.input_path == "document.md"
        assert opts.exporter == "txt"

    def test_export_with_specific_exporter(self) -> None:
        opts = parse_args(["export", "doc.html", "--exporter", "html"])
        assert opts.exporter == "html"

# ============================================================================
# Test: version command
# ============================================================================

class TestVersionCommand:
    def test_version_returns_empty_input_path(self) -> None:
        opts = parse_args(["version"])
        assert opts.command == "version"
        assert opts.input_path == ""

# ============================================================================
# Test: Invalid Inputs
# ============================================================================

class TestInvalidInputs:
    def test_invalid_renderer_raises_exit(self) -> None:
        with pytest.raises(SystemExit):
            parse_args(["analyze", "workbook.xlsx", "--renderer", "invalid"])

    def test_invalid_exporter_raises_exit(self) -> None:
        with pytest.raises(SystemExit):
            parse_args(["analyze", "workbook.xlsx", "--export", "invalid"])

    def test_no_subcommand_raises_exit(self) -> None:
        with pytest.raises(SystemExit):
            parse_args([])

    def test_unknown_command_raises_exit(self) -> None:
        with pytest.raises(SystemExit):
            parse_args(["unknown", "arg"])

# ============================================================================
# Test: Constants
# ============================================================================

class TestConstants:
    def test_valid_renderers(self) -> None:
        assert "markdown" in VALID_RENDERERS
        assert "html" in VALID_RENDERERS
        assert "json" in VALID_RENDERERS
        assert "terminal" in VALID_RENDERERS

    def test_valid_exporters(self) -> None:
        assert "md" in VALID_EXPORTERS
        assert "html" in VALID_EXPORTERS
        assert "json" in VALID_EXPORTERS
        assert "txt" in VALID_EXPORTERS

    def test_application_version(self) -> None:
        assert APPLICATION_VERSION.startswith("0.")

    def test_architecture_version(self) -> None:
        assert ARCHITECTURE_VERSION == "1.0"

# ============================================================================
# Test: CLIOptions Data Object
# ============================================================================

class TestCLIOptions:
    def test_cli_options_defaults(self) -> None:
        opts = CLIOptions(command="version")
        assert opts.command == "version"
        assert opts.input_path == ""
        assert opts.output_path == ""
        assert opts.renderer == "terminal"
        assert opts.exporter == "txt"
        assert opts.enable_review is False
        assert opts.quiet is False
        assert opts.verbose is False

    def test_cli_options_analyze(self) -> None:
        opts = CLIOptions(
            command="analyze",
            input_path="workbook.xlsx",
            renderer="html",
            exporter="html",
            enable_review=True,
            verbose=True,
        )
        assert opts.command == "analyze"
        assert opts.input_path == "workbook.xlsx"
        assert opts.renderer == "html"
        assert opts.exporter == "html"
        assert opts.enable_review is True
        assert opts.verbose is True