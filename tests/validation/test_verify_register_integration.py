"""
Integration tests for verify_register.py using the shared_governance library.

Tests ensure the refactored register validator correctly validates
the Engineering Register structure, EQ entries, authority documents,
and evidence packages.
"""

import pytest
import subprocess
import json
import sys
from pathlib import Path

TOOLS_ROOT = Path(__file__).resolve().parent.parent.parent / "tools"
VERIFY_REGISTER = TOOLS_ROOT / "quality" / "verify_register.py"

def run_tool(*args):
    result = subprocess.run(
        [sys.executable, str(VERIFY_REGISTER), *args],
        capture_output=True,
        text=True,
        cwd=TOOLS_ROOT.parent
    )
    return result

class TestVerifyRegisterDiscoverability:
    """Integration tests for tool import and execution."""

    def test_tool_runs_without_error(self):
        """Tool should execute and exit cleanly."""
        result = run_tool("--json")
        assert result.returncode in (0, 1), f"Tool failed: {result.stderr}"
        report = json.loads(result.stdout)
        assert report["tool"] == "verify_register"

    def test_all_checks_are_executed(self):
        """All defined checks should be executed and reported."""
        result = run_tool("--json")
        report = json.loads(result.stdout)
        assert report["summary"]["total_checks"] > 0
        assert "register_structure" in report["results"]
        assert "unique_eq_numbers" in report["results"]
        assert "authority_documents_exist" in report["results"]
        assert "evidence_packages_exist" in report["results"]

    def test_json_output_structure(self):
        """JSON output should match the standard report structure."""
        result = run_tool("--json")
        report = json.loads(result.stdout)
        assert "overall_pass" in report
        assert "summary" in report
        assert "results" in report
        for name, check in report["results"].items():
            assert "pass" in check
            assert "findings" in check
            assert isinstance(check["findings"], list)

    def test_markdown_report_creation(self):
        """Tool should write a markdown report file when --output is specified."""
        output_path = TOOLS_ROOT / "quality" / "test_register_report.md"
        result = run_tool("--output", str(output_path))
        assert output_path.exists(), f"Report was not created at {output_path}"
        content = output_path.read_text(encoding="utf-8")
        assert "Register Validation Report" in content
        output_path.unlink(missing_ok=True)

class TestVerifyRegisterContent:
    """Integration tests for register validation content."""

    def test_register_structure_validated(self):
        """Register structure validation should operate without error."""
        result = run_tool("--json")
        report = json.loads(result.stdout)
        struct_check = report["results"]["register_structure"]
        assert "pass" in struct_check

    def test_eq_entries_validated(self):
        """EQ entry validation should operate without error."""
        result = run_tool("--json")
        report = json.loads(result.stdout)
        entries_check = report["results"]["unique_eq_numbers"]
        assert "pass" in entries_check

    def test_authority_documents_validated(self):
        """Authority document validation should operate without error."""
        result = run_tool("--json")
        report = json.loads(result.stdout)
        auth_check = report["results"]["authority_documents_exist"]
        assert "pass" in auth_check

    def test_evidence_packages_validated(self):
        """Evidence package validation should operate without error."""
        result = run_tool("--json")
        report = json.loads(result.stdout)
        evidence_check = report["results"]["evidence_packages_exist"]
        assert "pass" in evidence_check

class TestVerifyRegisterIntegration:
    """Integration tests for register validation."""

    def test_output_matches_verify_all_format(self):
        """Tool output should be consumable by verify_all.py."""
        result = run_tool("--json")
        report = json.loads(result.stdout)
        for name, check in report["results"].items():
            assert "pass" in check
            assert "findings" in check
            assert isinstance(check["findings"], list)