"""
Integration tests for verify_links.py using the shared_governance library.

Tests ensure the refactored link validator correctly discovers,
validates, and reports findings for all markdown links,
Engineering Register links, and cross-document references.
"""

import pytest
import subprocess
import json
import sys
from pathlib import Path

TOOLS_ROOT = Path(__file__).resolve().parent.parent.parent / "tools"
VERIFY_LINKS = TOOLS_ROOT / "quality" / "verify_links.py"

def run_tool(*args):
    result = subprocess.run(
        [sys.executable, str(VERIFY_LINKS), *args],
        capture_output=True,
        text=True,
        cwd=TOOLS_ROOT.parent
    )
    return result


class TestVerifyLinksDiscoverability:
    """Integration tests for tool import and execution."""

    def test_tool_runs_without_error(self):
        """Tool should execute and exit cleanly."""
        result = run_tool("--json")
        assert result.returncode in (0, 1), f"Tool failed: {result.stderr}"
        report = json.loads(result.stdout)
        assert report["tool"] == "verify_links"

    def test_all_checks_are_executed(self):
        """All defined checks should be executed and reported."""
        result = run_tool("--json")
        report = json.loads(result.stdout)
        assert report["summary"]["total_checks"] > 0
        # Should cover markdown links, register links, evidence links, etc.
        assert "markdown_links" in report["results"]
        assert "engineering_register_links" in report["results"]
        assert "evidence_package_links" in report["results"]
        assert "readme_references" in report["results"]
        assert "cross_document_references" in report["results"]

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
        output_path = TOOLS_ROOT / "quality" / "test_links_report.md"
        result = run_tool("--output", str(output_path))
        assert output_path.exists(), f"Report was not created at {output_path}"
        content = output_path.read_text(encoding="utf-8")
        assert "Verify Links Validation Report" in content
        output_path.unlink(missing_ok=True)


class TestVerifyLinksContent:
    """Integration tests for link validation content."""

    def test_tool_detects_missing_directory(self, tmp_path):
        """Tool should fail gracefully in a non-existent project structure."""
        result = subprocess.run(
            [sys.executable, str(VERIFY_LINKS), "--json"],
            capture_output=True, text=True,
            cwd=tmp_path
        )
        if result.returncode == 0:
            report = json.loads(result.stdout)
            assert not report["overall_pass"], "Should fail on empty directory"
        else:
            assert result.returncode == 1

    def test_link_count_as_expected(self):
        """Link validation should identify a reasonable number of links."""
        result = run_tool("--json")
        report = json.loads(result.stdout)
        links_check = report["results"]["markdown_links"]
        info_findings = [f for f in links_check["findings"]
                         if f.startswith("INFO:")]
        # There should be at least one INFO line with link counts
        assert len(info_findings) > 0

    def test_evidence_package_links_validated(self):
        """Evidence package links should be checked."""
        result = run_tool("--json")
        report = json.loads(result.stdout)
        evidence_links = report["results"]["evidence_package_links"]
        # The check should at least execute (pass or fail)
        assert "pass" in evidence_links


class TestVerifyLinksIntegration:
    """Integration tests with other quality tools."""

    def test_output_matches_verify_all_format(self):
        """Tool output should be consumable by verify_all.py."""
        result = run_tool("--json")
        report = json.loads(result.stdout)
        for name, check in report["results"].items():
            assert "pass" in check
            assert "findings" in check
            assert isinstance(check["findings"], list)