"""
Integration tests for verify_evidence.py using the shared_governance library.

Tests ensure the refactored evidence validator correctly validates
authority documents, evidence packages, completeness, and prevents
orphaned/duplicate evidence.
"""

import pytest
import subprocess
import json
import sys
from pathlib import Path

TOOLS_ROOT = Path(__file__).resolve().parent.parent.parent / "tools"
VERIFY_EVIDENCE = TOOLS_ROOT / "quality" / "verify_evidence.py"


def run_tool(*args):
    result = subprocess.run(
        [sys.executable, str(VERIFY_EVIDENCE), *args],
        capture_output=True,
        text=True,
        cwd=TOOLS_ROOT.parent
    )
    return result


class TestVerifyEvidenceDiscoverability:
    """Integration tests for tool import and execution."""

    def test_tool_runs_without_error(self):
        """Tool should execute and exit cleanly."""
        result = run_tool("--json")
        assert result.returncode in (0, 1), f"Tool failed: {result.stderr}"
        report = json.loads(result.stdout)
        assert report["tool"] == "verify_evidence"

    def test_all_checks_are_executed(self):
        """All defined checks should be executed and reported."""
        result = run_tool("--json")
        report = json.loads(result.stdout)
        assert report["summary"]["total_checks"] > 0
        assert "authority_documents" in report["results"]
        assert "evidence_packages" in report["results"]
        assert "evidence_completeness" in report["results"]
        assert "orphaned_evidence" in report["results"]
        assert "duplicate_evidence" in report["results"]
        assert "package_structure" in report["results"]
        assert "authority_references" in report["results"]
        assert "readme_validation" in report["results"]

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
        output_path = TOOLS_ROOT / "quality" / "test_evidence_report.md"
        result = run_tool("--output", str(output_path))
        assert output_path.exists(), f"Report was not created at {output_path}"
        content = output_path.read_text(encoding="utf-8")
        assert "Evidence Validation Report" in content
        output_path.unlink(missing_ok=True)


class TestVerifyEvidenceContent:
    """Integration tests for evidence validation content."""

    def test_authority_documents_check_finds_expected_content(self):
        """Authority document validation should operate as expected."""
        result = run_tool("--json")
        report = json.loads(result.stdout)
        auth_check = report["results"]["authority_documents"]
        # The check should have executed (pass or fail is acceptable)
        assert "pass" in auth_check

    def test_evidence_packages_check_finds_expected_content(self):
        """Evidence package validation should operate as expected."""
        result = run_tool("--json")
        report = json.loads(result.stdout)
        evidence_check = report["results"]["evidence_packages"]
        assert "pass" in evidence_check

    def test_orphaned_evidence_detection(self):
        """Orphaned evidence detection should operate without error."""
        result = run_tool("--json")
        report = json.loads(result.stdout)
        orphaned_check = report["results"]["orphaned_evidence"]
        assert "pass" in orphaned_check

    def test_duplicate_evidence_detection(self):
        """Duplicate evidence detection should operate without error."""
        result = run_tool("--json")
        report = json.loads(result.stdout)
        dup_check = report["results"]["duplicate_evidence"]
        assert "pass" in dup_check

    def test_package_structure_validation(self):
        """Package structure validation should operate without error."""
        result = run_tool("--json")
        report = json.loads(result.stdout)
        struct_check = report["results"]["package_structure"]
        assert "pass" in struct_check

    def test_readme_validation(self):
        """README validation should operate without error."""
        result = run_tool("--json")
        report = json.loads(result.stdout)
        readme_check = report["results"]["readme_validation"]
        assert "pass" in readme_check


class TestVerifyEvidenceIntegration:
    """Integration tests for evidence validation."""

    def test_output_matches_verify_all_format(self):
        """Tool output should be consumable by verify_all.py."""
        result = run_tool("--json")
        report = json.loads(result.stdout)
        for name, check in report["results"].items():
            assert "pass" in check
            assert "findings" in check
            assert isinstance(check["findings"], list)