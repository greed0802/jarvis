"""Tests for CheckMate CLI entry point (CP-0001).

Verifies:
- CLIRunner handles all commands
- Version command returns success
- Analyze command with real inputs
- Exit codes are correct
- Error handling returns appropriate codes
- CLI consumes frozen architecture (no new layers)
"""

from __future__ import annotations

import json
import os
import tempfile

import pytest

from jarvis.applications.checkmate.cli.main import (
    CLIRunner,
    main,
    EXIT_SUCCESS,
    EXIT_APPLICATION_ERROR,
    EXIT_INVALID_ARGS,
    EXIT_INPUT_MISSING,
    EXIT_CONFIG_ERROR,
    EXIT_INTERNAL_ERROR,
)
from jarvis.applications.checkmate.cli.parser import (
    CLIOptions,
    APPLICATION_VERSION,
    ARCHITECTURE_VERSION,
)
from jarvis.applications.checkmate.cli.pipeline import PipelineRunner
from jarvis.parsers.costx.boq_intelligence import BOQIntelligenceResult
from jarvis.engines.validation.engine import ValidationFindings, ValidationFinding
from jarvis.applications.checkmate.export.request import ExportResult

# ============================================================================
# Test Fixtures
# ============================================================================

def make_minimal_evidence() -> BOQIntelligenceResult:
    return BOQIntelligenceResult(
        row_classification={"Head": 5, "Item": 10, "Note": 1, "Section": 2, "Other": 0},
        section_statistics={"Section A": {"items": 10, "headers": 2}},
        boq_statistics={"total_items": 10, "total_headers": 5},
        known_anomalies=[],
    )

def make_minimal_findings() -> ValidationFindings:
    return ValidationFindings(
        findings=(),
        engine_version="1.0.0",
        contract_version="1.0.0",
        execution_timestamp="2026-07-26T00:00:00",
    )

def make_input_json(evidence: BOQIntelligenceResult | None = None, findings: ValidationFindings | None = None) -> str:
    """Create a temporary JSON input file and return its path."""
    e = evidence or make_minimal_evidence()
    f = findings or make_minimal_findings()
    data = {
        "evidence": {k: v for k, v in e.__dict__.items() if not k.startswith("_")},
        "findings": {
            "findings": [
                {
                    "rule_id": _.rule_id,
                    "rule_version": _.rule_version or "1.0.0",
                    "category": _.category,
                    "finding_type": _.finding_type,
                    "finding_value": _.finding_value or "",
                    "evidence_fields": list(_.evidence_fields or ()),
                }
                for _ in f.findings
            ],
            "engine_version": f.engine_version,
            "contract_version": f.contract_version,
            "execution_timestamp": f.execution_timestamp,
        },
    }
    return json.dumps(data)

def create_temp_input_file() -> str:
    """Create a real temp file with pipeline-compatible JSON and return the path."""
    import tempfile
    fd, path = tempfile.mkstemp(suffix=".json", prefix="checkmate_test_")
    os.close(fd)
    content = make_input_json()
    with open(path, "w") as f:
        f.write(content)
    return path

# ============================================================================
# Test: CLIRunner
# ============================================================================

class TestCLIRunner:
    def test_runner_instantiation(self) -> None:
        runner = CLIRunner()
        assert runner is not None
        assert isinstance(runner.pipeline, PipelineRunner)

    def test_version_command(self) -> None:
        runner = CLIRunner()
        opts = CLIOptions(command="version")
        exit_code = runner.run(opts)
        assert exit_code == EXIT_SUCCESS

    def test_analyze_with_valid_input(self) -> None:
        path = create_temp_input_file()
        try:
            runner = CLIRunner()
            opts = CLIOptions(
                command="analyze",
                input_path=path,
                renderer="terminal",
                exporter="txt",
                quiet=True,
            )
            exit_code = runner.run(opts)
            assert exit_code == EXIT_SUCCESS
        finally:
            os.unlink(path)

    def test_analyze_with_markdown_renderer(self) -> None:
        path = create_temp_input_file()
        try:
            runner = CLIRunner()
            opts = CLIOptions(
                command="analyze",
                input_path=path,
                renderer="markdown",
                exporter="md",
                quiet=True,
            )
            exit_code = runner.run(opts)
            assert exit_code == EXIT_SUCCESS
        finally:
            os.unlink(path)

    def test_analyze_with_review_enabled(self) -> None:
        path = create_temp_input_file()
        try:
            runner = CLIRunner()
            opts = CLIOptions(
                command="analyze",
                input_path=path,
                renderer="terminal",
                exporter="txt",
                enable_review=True,
                quiet=True,
            )
            exit_code = runner.run(opts)
            assert exit_code == EXIT_SUCCESS
        finally:
            os.unlink(path)

    def test_analyze_with_output_file(self) -> None:
        path = create_temp_input_file()
        try:
            with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as out_f:
                out_path = out_f.name
            try:
                runner = CLIRunner()
                opts = CLIOptions(
                    command="analyze",
                    input_path=path,
                    output_path=out_path,
                    renderer="terminal",
                    exporter="txt",
                    quiet=True,
                )
                exit_code = runner.run(opts)
                assert exit_code == EXIT_SUCCESS
                assert os.path.exists(out_path)
                assert os.path.getsize(out_path) > 0
            finally:
                os.unlink(out_path)
        finally:
            os.unlink(path)

    def test_analyze_missing_file(self) -> None:
        runner = CLIRunner()
        opts = CLIOptions(
            command="analyze",
            input_path="/nonexistent/file.xlsx",
            quiet=True,
        )
        exit_code = runner.run(opts)
        assert exit_code == EXIT_INPUT_MISSING

    def test_render_command_is_stub(self) -> None:
        runner = CLIRunner()
        opts = CLIOptions(command="render", input_path="model.json")
        exit_code = runner.run(opts)
        assert exit_code == EXIT_SUCCESS

    def test_export_command_is_stub(self) -> None:
        runner = CLIRunner()
        opts = CLIOptions(command="export", input_path="document.md")
        exit_code = runner.run(opts)
        assert exit_code == EXIT_SUCCESS

# ============================================================================
# Test: Exit Codes
# ============================================================================

class TestExitCodes:
    def test_success_code(self) -> None:
        assert EXIT_SUCCESS == 0

    def test_app_error_code(self) -> None:
        assert EXIT_APPLICATION_ERROR == 1

    def test_invalid_args_code(self) -> None:
        assert EXIT_INVALID_ARGS == 2

    def test_input_missing_code(self) -> None:
        assert EXIT_INPUT_MISSING == 3

    def test_config_error_code(self) -> None:
        assert EXIT_CONFIG_ERROR == 4

    def test_internal_error_code(self) -> None:
        assert EXIT_INTERNAL_ERROR == 5

# ============================================================================
# Test: main() entry point
# ============================================================================

class TestMainEntryPoint:
    def test_main_with_version(self) -> None:
        exit_code = main(["version"])
        assert exit_code == EXIT_SUCCESS

    def test_main_with_no_args(self) -> None:
        """main() with empty argv should yield SystemExit (no subcommand)."""
        exit_code = main([])
        assert exit_code == EXIT_INVALID_ARGS


# ============================================================================
# Test: No Architecture Violation
# ============================================================================

class TestNoArchitectureViolation:
    def test_cli_runner_is_not_renderer(self) -> None:
        """CLIRunner is a consumer, not a renderer."""
        runner = CLIRunner()
        assert not hasattr(runner, "render")  # still can scaffold ops
        assert not hasattr(runner, "interpret")
        assert not hasattr(runner, "validate")

    def test_cli_runner_uses_existing_architecture(self) -> None:
        """CLIRunner wires existing components — does not modify them."""
        runner = CLIRunner()
        assert isinstance(runner.pipeline, PipelineRunner)
        # pipeline is from IP-0007/IP-0008 — no new architecture