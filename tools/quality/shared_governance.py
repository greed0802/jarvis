"""
shared_governance.py — Shared Governance Library

Reusable components for repository governance validation.
Provides shared functionality for Engineering Register parsing,
repository model, path resolution, and common validation utilities.

Authority: Repository Governance Automation Framework
Consumers: All governance validators
"""

import re
import sys
from pathlib import Path
from typing import Tuple, List, Dict, Set, Optional, Any
from dataclasses import dataclass
from enum import Enum

# Repository Constants
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

class RepositoryPath(Enum):
    """Standard repository paths."""
    ENGINEERING_REGISTER = PROJECT_ROOT / "docs" / "engineering" / "Engineering_Register.md"
    ENGINEERING_QUESTIONS = PROJECT_ROOT / "docs" / "engineering" / "questions"
    ENGINEERING_EVIDENCE = PROJECT_ROOT / "docs" / "engineering" / "evidence"
    DOCS_ROOT = PROJECT_ROOT / "docs"
    TOOLS_ROOT = PROJECT_ROOT / "tools"
    TOOLS_QUALITY = PROJECT_ROOT / "tools" / "quality"
    TESTS_ROOT = PROJECT_ROOT / "tests"
    SRC_ROOT = PROJECT_ROOT / "src"

@dataclass
class EngineeringQuestion:
    """Data model for Engineering Question entries."""
    eq_number: str
    title: str
    status: str
    authority_document_text: str
    authority_document_path: str
    evidence_text: str
    evidence_path: str
    outcome: str
    repository_location: str

    def get_authority_document_full_path(self) -> Path:
        """Get the full path to the authority document.

        Authority document paths in the Engineering Register use paths like
        '../questions/EQ_0010.md' which are markdown-relative from the register
        location (docs/engineering/). The '../' prefix goes up from engineering/
        into docs/, then into a 'questions/' directory that mirrors the actual
        docs/engineering/questions/ location.

        Resolve by stripping '../questions/' and joining with the
        ENGINEERING_QUESTIONS directory.
        """
        prefix = "../questions/"
        if self.authority_document_path.startswith(prefix):
            filename = self.authority_document_path[len(prefix):]
            return (RepositoryPath.ENGINEERING_QUESTIONS.value / filename).resolve()
        # Fallback: resolve relative to register directory
        register_dir = RepositoryPath.ENGINEERING_REGISTER.value.parent
        return (register_dir / self.authority_document_path).resolve()

    def get_evidence_package_full_path(self) -> Path:
        """Get the full path to the evidence package.

        Evidence paths in the Engineering Register use paths like
        '../evidence/EQ_0010/' which are markdown-relative from the register
        location (docs/engineering/). The '../' prefix goes up from engineering/
        into docs/, then into an 'evidence/' directory that mirrors the actual
        docs/engineering/evidence/ location.

        Resolve by stripping '../evidence/' and joining with the
        ENGINEERING_EVIDENCE directory.
        """
        prefix = "../evidence/"
        if self.evidence_path.startswith(prefix):
            dirname = self.evidence_path[len(prefix):].rstrip("/")
            return (RepositoryPath.ENGINEERING_EVIDENCE.value / dirname).resolve()
        # Fallback: resolve relative to register directory
        register_dir = RepositoryPath.ENGINEERING_REGISTER.value.parent
        return (register_dir / self.evidence_path).resolve()

    def validate_authority_document_path(self) -> bool:
        """Validate the authority document path format.

        Valid paths start with '../questions/' (markdown-relative from
        docs/engineering/) and end with '.md'.
        """
        return (self.authority_document_path.startswith("../questions/")
                and self.authority_document_path.endswith(".md"))

    def validate_evidence_path(self) -> bool:
        """Validate the evidence package path format.

        Valid paths start with '../evidence/' (markdown-relative from
        docs/engineering/) and end with '/'.
        """
        return (self.evidence_path.startswith("../evidence/")
                and self.evidence_path.endswith("/"))

    def validate_status(self) -> bool:
        """Validate the EQ status."""
        valid_statuses = ["Completed", "Active", "Draft", "Frozen"]
        return self.status.strip() in valid_statuses

    def validate_repository_location(self) -> bool:
        """Validate the repository location."""
        return self.repository_location.strip() == "docs/engineering/"

class RepositoryModel:
    """Shared repository structure model."""

    @staticmethod
    def get_required_directories() -> List[Path]:
        """Get all required repository directories."""
        return [
            RepositoryPath.DOCS_ROOT.value,
            RepositoryPath.SRC_ROOT.value,
            RepositoryPath.TESTS_ROOT.value,
            RepositoryPath.TOOLS_ROOT.value,
            RepositoryPath.ENGINEERING_QUESTIONS.value,
            RepositoryPath.ENGINEERING_EVIDENCE.value,
        ]

    @staticmethod
    def get_required_documentation_files() -> List[Path]:
        """Get all required main documentation files."""
        return [
            PROJECT_ROOT / "README.md",
            PROJECT_ROOT / "docs" / "00_Vision.md",
            PROJECT_ROOT / "docs" / "01_Principles.md",
            PROJECT_ROOT / "docs" / "02_System_Blueprint.md",
            RepositoryPath.ENGINEERING_REGISTER.value,
        ]

    @staticmethod
    def get_quality_tool_locations() -> Dict[str, Path]:
        """Get expected locations for quality tools."""
        return {
            "verify_all.py": RepositoryPath.TOOLS_QUALITY.value,
            "verify_governance.py": RepositoryPath.TOOLS_QUALITY.value,
            "verify_links.py": RepositoryPath.TOOLS_QUALITY.value,
            "verify_evidence.py": RepositoryPath.TOOLS_QUALITY.value,
            "verify_tools.py": RepositoryPath.TOOLS_QUALITY.value,
            "verify_register.py": RepositoryPath.TOOLS_QUALITY.value,
        }

class EngineeringRegisterParser:
    """Parser for Engineering Register."""

    @staticmethod
    def parse_register() -> Tuple[bool, List[str], List[EngineeringQuestion]]:
        """
        Parse the Engineering Register and return EQ entries.

        Returns:
            tuple: (success, findings, eq_entries)
        """
        findings = []
        eq_entries = []

        register_path = RepositoryPath.ENGINEERING_REGISTER.value

        if not register_path.exists():
            findings.append("ERROR: Engineering_Register.md not found")
            return False, findings, eq_entries

        try:
            content = register_path.read_text(encoding="utf-8")

            # Extract EQ entries using comprehensive regex pattern
            eq_pattern = r"\| (EQ-\d+)\s*\|\s*([^\|]+)\s*\|\s*([^\|]+)\s*\|\s*\[([^\]]+)\]\(([^\)]+)\)\s*\|\s*\[([^\]]+)\]\(([^\)]+)\)\s*\|\s*([^\|]+)\s*\|\s*([^\|]+)"
            eq_matches = re.findall(eq_pattern, content)

            if not eq_matches:
                findings.append("ERROR: No EQ entries found in Engineering Register")
                return False, findings, eq_entries

            # Convert matches to EngineeringQuestion objects
            for match in eq_matches:
                eq_number, title, status, auth_doc_text, auth_doc_path, evidence_text, evidence_path, outcome, repo_location = match
                eq_entries.append(EngineeringQuestion(
                    eq_number=eq_number.strip(),
                    title=title.strip(),
                    status=status.strip(),
                    authority_document_text=auth_doc_text.strip(),
                    authority_document_path=auth_doc_path.strip(),
                    evidence_text=evidence_text.strip(),
                    evidence_path=evidence_path.strip(),
                    outcome=outcome.strip(),
                    repository_location=repo_location.strip()
                ))

        except Exception as e:
            findings.append(f"ERROR: Could not parse Engineering Register: {e}")
            return False, findings, eq_entries

        return True, findings, eq_entries

    @staticmethod
    def validate_register_structure() -> Tuple[bool, List[str]]:
        """Validate Engineering Register file structure."""
        findings = []
        register_path = RepositoryPath.ENGINEERING_REGISTER.value

        if not register_path.exists():
            findings.append("ERROR: Engineering_Register.md not found")
            return False, findings

        try:
            content = register_path.read_text(encoding="utf-8")

            # Check for required sections
            required_sections = [
                "# Engineering Register",
                "## Active Engineering Questions",
                "## Archive",
                "## Governance Model Compliance"
            ]

            for section in required_sections:
                if section not in content:
                    findings.append(f"ERROR: Engineering Register missing required section: {section}")

            # Check for table structure
            if "| EQ Number |" not in content:
                findings.append("ERROR: Engineering Register missing table header")

            if "|-----------|" not in content:
                findings.append("ERROR: Engineering Register missing table separator")

        except Exception as e:
            findings.append(f"ERROR: Could not read Engineering Register: {e}")
            return False, findings

        return len(findings) == 0, findings

class FileValidator:
    """Utilities for file and directory validation."""

    @staticmethod
    def validate_file_exists(file_path: Path, error_message: str) -> Tuple[bool, List[str]]:
        """Validate that a file exists."""
        findings = []
        if not file_path.exists():
            findings.append(f"ERROR: {error_message}")
            return False, findings
        return True, findings

    @staticmethod
    def validate_directory_exists(directory_path: Path, error_message: str) -> Tuple[bool, List[str]]:
        """Validate that a directory exists."""
        findings = []
        if not directory_path.exists():
            findings.append(f"ERROR: {error_message}")
            return False, findings
        if not directory_path.is_dir():
            findings.append(f"ERROR: {error_message} (not a directory)")
            return False, findings
        return True, findings

    @staticmethod
    def validate_file_content_contains(file_path: Path, required_content: List[str], error_prefix: str) -> Tuple[bool, List[str]]:
        """Validate that a file contains required content."""
        findings = []

        if not file_path.exists():
            findings.append(f"ERROR: {error_prefix} - file not found")
            return False, findings

        try:
            content = file_path.read_text(encoding="utf-8")
            missing_sections = [section for section in required_content if section not in content]

            if missing_sections:
                findings.append(f"ERROR: {error_prefix} - missing sections: {', '.join(missing_sections)}")
                return False, findings

        except Exception as e:
            findings.append(f"ERROR: {error_prefix} - could not read file: {e}")
            return False, findings

        return True, findings

    @staticmethod
    def normalize_and_resolve_path(path_str: str, base_dir: Path) -> Optional[Path]:
        """Normalize a relative path string and resolve it against a base directory."""
        try:
            # Handle relative paths starting with ./
            if path_str.startswith('./'):
                path_str = path_str[2:]
            
            # pathlib.Path handles '..' and absolute paths correctly when joining
            resolved_path = (base_dir / path_str).resolve()
            return resolved_path
        except Exception:
            # Return None if path resolution fails (e.g., malformed path)
            return None

class MarkdownParser:
    """Utilities for parsing markdown files."""

    @staticmethod
    def extract_markdown_links(file_path: Path) -> List[Tuple[int, str, str]]:
        """Extract all markdown links from a file with line numbers."""
        links = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    # Match markdown links: [text](url)
                    matches = re.finditer(r'\[([^\]]+)\]\(([^\)]+)\)', line)
                    for match in matches:
                        text = match.group(1)
                        url = match.group(2)
                        links.append((line_num, text, url))
        except Exception as e:
            print(f"ERROR: Could not read {file_path}: {e}")
        return links

    @staticmethod
    def find_all_markdown_files(root_path: Path = PROJECT_ROOT) -> List[Path]:
        """Find all markdown files in the repository."""
        markdown_files = []
        for ext in ['*.md', '*.MD']:
            markdown_files.extend(root_path.rglob(ext))
        return [f for f in markdown_files if not any(part.startswith('.') for part in f.parts)]

class ValidationResult:
    """Standard validation result structure."""

    def __init__(self, success: bool, findings: List[str]):
        self.success = success
        self.findings = findings

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "success": self.success,
            "findings": self.findings
        }

def count_findings_by_severity(findings: List[str]) -> Dict[str, int]:
    """Count findings by severity level."""
    error_count = 0
    warn_count = 0
    info_count = 0

    for finding in findings:
        if finding.startswith("ERROR:"):
            error_count += 1
        elif finding.startswith("WARN:"):
            warn_count += 1
        elif finding.startswith("INFO:"):
            info_count += 1

    return {
        "error_count": error_count,
        "warning_count": warn_count,
        "info_count": info_count
    }

def generate_validation_report(
    tool_name: str,
    checks: List[Tuple[str, ValidationResult]]
) -> Dict[str, Any]:
    """Generate a standard validation report."""
    all_pass = all(result.success for _, result in checks)

    report = {
        "tool": tool_name,
        "overall_pass": all_pass,
        "summary": {
            "total_checks": len(checks),
            "passed_checks": sum(1 for _, result in checks if result.success),
            "failed_checks": sum(1 for _, result in checks if not result.success),
        },
        "results": {name: {"pass": result.success, "findings": result.findings}
                   for name, result in checks}
    }

    # Count findings by severity across all checks
    total_errors = 0
    total_warnings = 0
    total_info = 0

    for _, result in checks:
        counts = count_findings_by_severity(result.findings)
        total_errors += counts["error_count"]
        total_warnings += counts["warning_count"]
        total_info += counts["info_count"]

    report["summary"]["error_count"] = total_errors
    report["summary"]["warning_count"] = total_warnings
    report["summary"]["info_count"] = total_info

    return report

def write_markdown_report(report: Dict[str, Any], output_path: Path) -> None:
    """Write a validation report in markdown format."""
    summary = report["summary"]
    results = report["results"]

    md = f"# {report['tool'].replace('_', ' ').title()} Validation Report\n\n"
    md += f"**Overall Status:** {'PASS' if report['overall_pass'] else 'FAIL'}\n\n"
    md += f"**Summary:** {summary['passed_checks']}/{summary['total_checks']} checks passed | "
    md += f"{summary['error_count']} errors | {summary['warning_count']} warnings | {summary['info_count']} info\n\n"

    for name, result in results.items():
        status = "PASS" if result["pass"] else "FAIL"
        md += f"## {name.replace('_', ' ').title()}\n"
        md += f"**Status:** {status}\n\n"

        if result["findings"]:
            for finding in result["findings"]:
                severity = "❌" if finding.startswith("ERROR:") else "⚠️" if finding.startswith("WARN:") else "ℹ️"
                md += f"- {severity} {finding[6:] if finding.startswith(('ERROR:', 'WARN:', 'INFO:')) else finding}\n"
        else:
            md += "- No findings\n"
        md += "\n"

    output_path.write_text(md, encoding="utf-8")