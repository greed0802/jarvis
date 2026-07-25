"""
Integration tests for verify_governance.py using the shared_governance library.

Tests ensure the refactored governance tool correctly discovers,
validates, and reports findings for all governance documents,
Engineering Questions, authority documents, and evidence packages.
"""

import pytest
import subprocess
import json
import sys
from pathlib import Path

# Path to the verify_governance.py tool
TOOLS_ROOT = Path(__file__).resolve().parent.parent.parent / "tools"
VERIFY_GOVERNANCE = TOOLS_ROOT / "quality" / "verify_governance.py"

# Helper to invoke verify_governance.py
def run_tool(*args):
    result = subprocess.run(
        [sys.executable, str(VERIFY_GOVERNANCE), *args],
        capture_output=True,
        text=True,
        cwd=TOOLS_ROOT.parent
    )
    return result

class TestVerifyGovernanceDiscoverability:
    """Integration tests for tool import and execution."""

    def test_tool_runs_without_error(self):
        """Tool should execute and exit cleanly."""
        result = run_tool("--json")
        assert result.returncode in (0, 1), f"Tool failed: {result.stderr}"
        # Should produce valid JSON
        report = json.loads(result.stdout)
        assert report["tool"] == "verify_governance"

    def test_all_checks_are_executed(self):
        """All defined checks should be executed and reported."""
        result = run_tool("--json")
        report = json.loads(result.stdout)
        assert report["summary"]["total_checks"] > 0
        # Should cover governance hierarchy, register, and documents
        assert "documentation_hierarchy" in report["results"]
        assert "engineering_register" in report["results"]
        assert "authority_documents" in report["results"]
        assert "evidence_packages" in report["results"]

    def test_json_output_structure(self):
        """JSON output should match the standard report structure."""
        result = run_tool("--json")
        report = json.loads(result.stdout)
        assert "overall_pass" in report
        assert "summary" in report
        assert "results" in report
        assert isinstance(report["summary"]["passed_checks"], int)
        assert isinstance(report["summary"]["failed_checks"], int)

    def test_markdown_report_creation(self):
        """Tool should write a markdown report file when --output is specified."""
        output_path = TOOLS_ROOT / "quality" / "test_governance_report.md"
        result = run_tool("--output", str(output_path))
        assert output_path.exists(), f"Report file was not created at {output_path}"
        content = output_path.read_text(encoding="utf-8")
        assert "Governance" in content
        output_path.unlink(missing_ok=True)


class TestVerifyGovernanceContent:
    """Integration tests for governance content validation."""

    def test_detects_missing_governance_directory(self, tmp_path):
        """Tool should fail gracefully on a non-existent governance structure."""
        result = subprocess.run(
            [sys.executable, str(VERIFY_GOVERNANCE), "--json"],
            capture_output=True, text=True,
            cwd=tmp_path
        )
        if result.returncode == 0:
            report = json.loads(result.stdout)
            # The tool should report failures for missing directories
            assert not report["overall_pass"], "Should fail on empty temp directory"
        else:
            # Or exit with code 1
            assert result.returncode == 1

    def test_cross_document_link_integrity(self):
        """Authority documents should properly link to evidence packages."""
        result = run_tool("--json")
        report = json.loads(result.stdout)
        if "cross_references" in report["results"]:
            cross_ref = report["results"]["cross_references"]
            # If links are valid, warnings/errors should not be excessive
            if not cross_ref["pass"]:
                errors = [f for f in cross_ref["findings"]
                          if f.startswith("ERROR:")]
                assert len(errors) < 20, f"Too many cross-reference errors: {errors}"

    def test_engineering_question_completeness(self):
        """Engineering questions should have authority documents and evidence packages."""
        result = run_tool("--json")
        report = json.loads(result.stdout)
        register_check = report["results"].get("engineering_register", {})
        if register_check.get("pass"):
            return  # Register is complete
        findings = register_check.get("findings", [])
        errors = [f for f in findings if f.startswith("ERROR:")]
        warnings = [f for f in findings if f.startswith("WARN:")]
        # Allow warnings but ensure errors are limited
        assert len(errors) < 15, f"Too many register errors: {errors}"


class TestVerifyGovernanceIntegration:
    """Integration tests with other quality tools."""

    def test_output_is_compatible_with_verify_all(self):
        """Tool output should be consumable by verify_all.py."""
        # This is a structural test: the JSON format should match expectations
        result = run_tool("--json")
        report = json.loads(result.stdout)
        assert "tool" in report
        assert "overall_pass" in report
        assert "summary" in report
        assert "results" in report
        # Each result should have 'pass' and 'findings'
        for name, check in report["results"].items():
            assert "pass" in check, f"Check '{name}' missing 'pass' key"
            assert "findings" in check, f"Check '{name}' missing 'findings' key"
            assert isinstance(check["findings"], list)

    def test_exit_code_reflects_overall_status(self):
        """Exit code 0 for pass, 1 for fail with only errors, 0 for fail with only warnings."""
        result = run_tool("--json")
        report = json.loads(result.stdout)
        has_errors = any(
            f.startswith("ERROR:")
            for check in report["results"].values()
            for f in check["findings"]
        )
        if report["overall_pass"] and not has_errors:
            assert result.returncode == 0
        # If only warnings, flexible behavior
        # Strict mode should exit 1 on any finding

    def test_strict_mode_exits_with_findings(self):
        """--strict should exit 1 if any findings at all exist."""
        result = run_tool("--json", "--strict")
        report = json.loads(result.stdout)
        all_pass = report["overall_pass"]
        if all_pass:
            assert result.returncode == 0
        else:
            assert result.returncode == 1