"""
verify_evidence.py — Engineering Question Evidence Validation

Automated verification of Engineering Question evidence packages.
Validates authority documents, evidence packages, completeness,
and prevents orphaned/duplicate evidence.

Authority: Quality Gate 2 (Architecture Verification)
Consumers: verify_all.py, CI, Pull Request validation
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Tuple, List, Dict

from shared_governance import (
    PROJECT_ROOT, RepositoryPath, EngineeringQuestion, EngineeringRegisterParser,
    RepositoryModel, FileValidator, ValidationResult,
    generate_validation_report, write_markdown_report
)

EXIT_PASS = 0
EXIT_FAIL = 1
EXIT_ERROR = 2

def validate_eq_authority_documents() -> ValidationResult:
    """Validate that every EQ has an authority document."""
    findings = []
    
    ok_parse, parse_findings, eq_entries = EngineeringRegisterParser.parse_register()
    findings.extend(parse_findings)
    if not ok_parse:
        return ValidationResult(False, findings)

    questions_dir = RepositoryPath.ENGINEERING_QUESTIONS.value
    ok_dir, dir_findings = FileValidator.validate_directory_exists(questions_dir, "questions directory not found")
    findings.extend(dir_findings)
    if not ok_dir:
        return ValidationResult(False, findings)

    for eq in eq_entries:
        auth_doc_full_path = eq.get_authority_document_full_path()
        ok_exists, exists_findings = FileValidator.validate_file_exists(
            auth_doc_full_path, f"EQ {eq.eq_number} missing authority document: {eq.authority_document_path}"
        )
        findings.extend(exists_findings)
        
        if ok_exists:
            required_sections = ["## Status", "## Purpose", "## Engineering Question"]
            ok_content, content_findings = FileValidator.validate_file_content_contains(
                auth_doc_full_path, required_sections, f"EQ {eq.eq_number} authority document"
            )
            findings.extend(content_findings)

            try:
                content = auth_doc_full_path.read_text(encoding="utf-8")
                status_match = re.search(r"## Status\n([^\n]+)", content)
                if status_match:
                    doc_status = status_match.group(1).strip()
                    if doc_status not in ["COMPLETED", "ACTIVE", "DRAFT", "FROZEN"]:
                        findings.append(f"ERROR: EQ {eq.eq_number} authority document has invalid status: {doc_status}")
            except Exception as e:
                findings.append(f"ERROR: Could not read EQ {eq.eq_number} authority document for status check: {e}")

    return ValidationResult(len(findings) == 0, findings)

def validate_evidence_packages() -> ValidationResult:
    """Validate that every EQ has a proper evidence package."""
    findings = []
    
    ok_parse, parse_findings, eq_entries = EngineeringRegisterParser.parse_register()
    findings.extend(parse_findings)
    if not ok_parse:
        return ValidationResult(False, findings)

    evidence_dir = RepositoryPath.ENGINEERING_EVIDENCE.value
    ok_dir, dir_findings = FileValidator.validate_directory_exists(evidence_dir, "evidence directory not found")
    findings.extend(dir_findings)
    if not ok_dir:
        return ValidationResult(False, findings)

    for eq in eq_entries:
        evidence_full_path = eq.get_evidence_package_full_path()

        ok_exists, exists_findings = FileValidator.validate_directory_exists(
            evidence_full_path, f"EQ {eq.eq_number} missing evidence package or it's not a directory: {eq.evidence_path}"
        )
        findings.extend(exists_findings)
        if not ok_exists:
            continue

        readme_path = evidence_full_path / "README.md"
        ok_readme_exists, readme_exists_findings = FileValidator.validate_file_exists(
            readme_path, f"EQ {eq.eq_number} evidence package missing README.md"
        )
        findings.extend(readme_exists_findings)
        if not ok_readme_exists:
            continue

        required_sections = ["## Engineering Question", "## Package Contents"]
        ok_content, content_findings = FileValidator.validate_file_content_contains(
            readme_path, required_sections, f"EQ {eq.eq_number} evidence package README"
        )
        findings.extend(content_findings)

        try:
            readme_content = readme_path.read_text(encoding="utf-8")
            if "Authority Document:" not in readme_content:
                findings.append(f"ERROR: EQ {eq.eq_number} evidence package README missing authority document reference")
        except Exception as e:
            findings.append(f"ERROR: Could not read EQ {eq.eq_number} evidence package README for reference check: {e}")

    return ValidationResult(len(findings) == 0, findings)

def validate_evidence_completeness() -> ValidationResult:
    """Validate evidence package completeness."""
    findings = []
    evidence_dir = RepositoryPath.ENGINEERING_EVIDENCE.value

    ok_dir, dir_findings = FileValidator.validate_directory_exists(evidence_dir, "evidence directory not found")
    findings.extend(dir_findings)
    if not ok_dir:
        return ValidationResult(False, findings)

    eq_packages = [d for d in evidence_dir.iterdir() if d.is_dir() and d.name.startswith("EQ_")]

    for package in eq_packages:
        readme_path = package / "README.md"
        ok_readme_exists, readme_exists_findings = FileValidator.validate_file_exists(
            readme_path, f"Evidence package {package.name} missing README.md"
        )
        findings.extend(readme_exists_findings)
        if not ok_readme_exists:
            continue

        reports = list(package.glob("*Report*.md"))
        if not reports:
            findings.append(f"WARN: Evidence package {package.name} has no evidence reports")

        tools = list(package.glob("*.py"))
        if tools:
            findings.append(f"INFO: Evidence package {package.name} contains {len(tools)} investigation tools")

    return ValidationResult(len(findings) == 0, findings)

def detect_orphaned_evidence() -> ValidationResult:
    """Detect evidence that doesn't belong to any registered EQ."""
    findings = []
    
    ok_parse, parse_findings, eq_entries = EngineeringRegisterParser.parse_register()
    findings.extend(parse_findings)
    if not ok_parse:
        return ValidationResult(False, findings)

    evidence_dir = RepositoryPath.ENGINEERING_EVIDENCE.value
    ok_dir, dir_findings = FileValidator.validate_directory_exists(evidence_dir, "evidence directory not found")
    findings.extend(dir_findings)
    if not ok_dir:
        return ValidationResult(False, findings)

    registered_eq_numbers = {eq.eq_number for eq in eq_entries}
    
    eq_packages = [d for d in evidence_dir.iterdir() if d.is_dir() and d.name.startswith("EQ_")]
    evidence_eq_packages = {package.name for package in eq_packages}

    orphaned = evidence_eq_packages - registered_eq_numbers
    if orphaned:
        findings.append(f"ERROR: Orphaned evidence packages found: {', '.join(sorted(orphaned))}")

    missing = registered_eq_numbers - evidence_eq_packages
    if missing:
        findings.append(f"ERROR: Registered EQs missing evidence packages: {', '.join(sorted(missing))}")

    return ValidationResult(len(findings) == 0, findings)

def detect_duplicate_evidence() -> ValidationResult:
    """Detect duplicate evidence files across packages."""
    findings = []
    evidence_dir = RepositoryPath.ENGINEERING_EVIDENCE.value

    ok_dir, dir_findings = FileValidator.validate_directory_exists(evidence_dir, "evidence directory not found")
    findings.extend(dir_findings)
    if not ok_dir:
        return ValidationResult(False, findings)

    evidence_files = {}
    eq_packages = [d for d in evidence_dir.iterdir() if d.is_dir() and d.name.startswith("EQ_")]

    for package in eq_packages:
        for file_path in package.iterdir():
            if file_path.is_file() and file_path.name != "README.md":
                try:
                    file_key = (file_path.name, file_path.stat().st_size)
                    if file_key in evidence_files:
                        existing = evidence_files[file_key]
                        findings.append(f"WARN: Potential duplicate evidence: {existing} and {file_path}")
                    else:
                        evidence_files[file_key] = str(file_path)
                except Exception:
                    continue

    return ValidationResult(len(findings) == 0, findings)

def validate_evidence_package_structure() -> ValidationResult:
    """Validate evidence package directory structure."""
    findings = []
    evidence_dir = RepositoryPath.ENGINEERING_EVIDENCE.value

    ok_dir, dir_findings = FileValidator.validate_directory_exists(evidence_dir, "evidence directory not found")
    findings.extend(dir_findings)
    if not ok_dir:
        return ValidationResult(False, findings)

    eq_packages = [d for d in evidence_dir.iterdir() if d.is_dir() and d.name.startswith("EQ_")]

    for package in eq_packages:
        if not re.match(r"EQ_\d{4}", package.name):
            findings.append(f"ERROR: Evidence package {package.name} has incorrect naming (should be EQ_XXXX)")

        subdirs = [d for d in package.iterdir() if d.is_dir()]
        if subdirs:
            findings.append(f"WARN: Evidence package {package.name} contains unexpected subdirectories: {', '.join(d.name for d in subdirs)}")

    return ValidationResult(len(findings) == 0, findings)

def validate_authority_document_references() -> ValidationResult:
    """Validate that authority documents reference their evidence packages."""
    findings = []
    questions_dir = RepositoryPath.ENGINEERING_QUESTIONS.value
    evidence_dir = RepositoryPath.ENGINEERING_EVIDENCE.value

    ok_questions_dir, questions_dir_findings = FileValidator.validate_directory_exists(questions_dir, "questions directory not found")
    findings.extend(questions_dir_findings)
    if not ok_questions_dir:
        return ValidationResult(False, findings)

    ok_evidence_dir, evidence_dir_findings = FileValidator.validate_directory_exists(evidence_dir, "evidence directory not found")
    findings.extend(evidence_dir_findings)
    if not ok_evidence_dir:
        return ValidationResult(False, findings)

    eq_files = list(questions_dir.glob("EQ_*.md"))

    for eq_file in eq_files:
        eq_number = eq_file.stem
        evidence_package = evidence_dir / eq_number

        ok_package_exists, package_exists_findings = FileValidator.validate_directory_exists(
            evidence_package, f"Authority document {eq_file.name} has no corresponding evidence package"
        )
        findings.extend(package_exists_findings)
        if not ok_package_exists:
            continue

        required_sections = ["## Purpose", "## Engineering Question"]
        ok_content, content_findings = FileValidator.validate_file_content_contains(
            eq_file, required_sections, f"Authority document {eq_file.name}"
        )
        findings.extend(content_findings)

    return ValidationResult(len(findings) == 0, findings)

def validate_evidence_package_readmes() -> ValidationResult:
    """Validate evidence package README content and structure."""
    findings = []
    evidence_dir = RepositoryPath.ENGINEERING_EVIDENCE.value

    ok_dir, dir_findings = FileValidator.validate_directory_exists(evidence_dir, "evidence directory not found")
    findings.extend(dir_findings)
    if not ok_dir:
        return ValidationResult(False, findings)

    eq_packages = [d for d in evidence_dir.iterdir() if d.is_dir() and d.name.startswith("EQ_")]

    for package in eq_packages:
        readme_path = package / "README.md"
        ok_readme_exists, readme_exists_findings = FileValidator.validate_file_exists(
            readme_path, f"Evidence package {package.name} missing README.md"
        )
        findings.extend(readme_exists_findings)
        if not ok_readme_exists:
            continue

        required_sections = ["## Engineering Question"]
        ok_content, content_findings = FileValidator.validate_file_content_contains(
            readme_path, required_sections, f"{package.name}/README.md"
        )
        findings.extend(content_findings)

        try:
            content = readme_path.read_text(encoding="utf-8")
            eq_number = package.name.replace("EQ_", "EQ-")
            auth_pattern = rf"\[.*{eq_number}.*\]\(.*{eq_number}.*\.md\)"
            if not re.search(auth_pattern, content):
                findings.append(f"ERROR: {package.name}/README.md does not properly reference authority document")
        except Exception as e:
            findings.append(f"ERROR: Could not read {package.name}/README.md for reference check: {e}")

    return ValidationResult(len(findings) == 0, findings)

def main():
    parser = argparse.ArgumentParser(description="Engineering Question Evidence Validation")
    parser.add_argument("--json", action="store_true", help="Output JSON to stdout")
    parser.add_argument("--strict", action="store_true", help="Exit 1 on any finding")
    parser.add_argument("--output", type=str, help="Write report to file (.json or .md)")
    args = parser.parse_args()

    checks_to_run = [
        ("authority_documents", validate_eq_authority_documents),
        ("evidence_packages", validate_evidence_packages),
        ("evidence_completeness", validate_evidence_completeness),
        ("orphaned_evidence", detect_orphaned_evidence),
        ("duplicate_evidence", detect_duplicate_evidence),
        ("package_structure", validate_evidence_package_structure),
        ("authority_references", validate_authority_document_references),
        ("readme_validation", validate_evidence_package_readmes),
    ]

    all_check_results = []
    for name, fn in checks_to_run:
        try:
            result = fn()
            all_check_results.append((name, result))
        except Exception as e:
            all_check_results.append((name, ValidationResult(False, [f"ERROR: Validation failed with exception: {e}"])))

    report = generate_validation_report("verify_evidence", all_check_results)
    all_pass = report["overall_pass"]

    if args.json:
        print(json.dumps(report, indent=2))

    if args.output:
        output_path = Path(args.output)
        if output_path.suffix == ".json":
            output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
        elif output_path.suffix == ".md":
            write_markdown_report(report, output_path)
        print(f"Report written to: {output_path}")

    if not all_pass:
        sys.exit(EXIT_FAIL if args.strict else EXIT_FAIL)
    sys.exit(EXIT_PASS)

if __name__ == "__main__":
    main()
