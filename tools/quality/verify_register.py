"""
verify_register.py — Engineering Register Validation

Specialized validation of the Engineering Register for
unique EQ numbers, authority document existence, evidence
package existence, valid repository paths, and status values.

Authority: Quality Gate 3 (Consumer Readiness)
Consumers: verify_all.py, CI, Pull Request validation
"""

import argparse
import json
import sys
import os
from pathlib import Path
from typing import Tuple, List, Dict

# Add the tools/quality directory to the Python path so we can import shared_governance
sys.path.append(str(Path(__file__).parent))

from shared_governance import (
    EngineeringRegisterParser,
    EngineeringQuestion,
    FileValidator,
    ValidationResult,
    RepositoryPath,
    generate_validation_report,
    write_markdown_report,
    count_findings_by_severity
)

EXIT_PASS = 0
EXIT_FAIL = 1
EXIT_ERROR = 2

def validate_register_structure() -> ValidationResult:
    """Validate Engineering Register file structure."""
    success, findings = EngineeringRegisterParser.validate_register_structure()
    return ValidationResult(success, findings)

def validate_unique_eq_numbers() -> ValidationResult:
    """Validate that all EQ numbers are unique."""
    findings = []

    # Parse the register to get all EQ entries
    success, parse_findings, eq_entries = EngineeringRegisterParser.parse_register()
    findings.extend(parse_findings)

    if not success:
        return ValidationResult(False, findings)

    if not eq_entries:
        findings.append("ERROR: No EQ entries found in Engineering Register")
        return ValidationResult(False, findings)

    # Check for duplicates
    eq_numbers = [eq.eq_number for eq in eq_entries]
    unique_eq_numbers = set(eq_numbers)

    if len(eq_numbers) != len(unique_eq_numbers):
        duplicates = [eq for eq in unique_eq_numbers if eq_numbers.count(eq) > 1]
        findings.append(f"ERROR: Duplicate EQ numbers found: {', '.join(sorted(duplicates))}")

    return ValidationResult(len(findings) == 0, findings)

def validate_authority_documents_exist() -> ValidationResult:
    """Validate that all authority documents referenced in the register exist."""
    findings = []

    # Parse the register to get all EQ entries
    success, parse_findings, eq_entries = EngineeringRegisterParser.parse_register()
    findings.extend(parse_findings)

    if not success:
        return ValidationResult(False, findings)

    # Validate questions directory exists
    questions_dir_success, questions_dir_findings = FileValidator.validate_directory_exists(
        RepositoryPath.ENGINEERING_QUESTIONS.value,
        "questions directory not found"
    )
    findings.extend(questions_dir_findings)
    if not questions_dir_success:
        return ValidationResult(False, findings)

    for eq in eq_entries:
        # Validate authority document path format
        if not eq.validate_authority_document_path():
            findings.append(f"ERROR: EQ {eq.eq_number} authority document has invalid path format: {eq.authority_document_path}")
            continue

        # Check if authority document exists
        auth_doc_path = eq.get_authority_document_full_path()
        file_success, file_findings = FileValidator.validate_file_exists(
            auth_doc_path,
            f"EQ {eq.eq_number} authority document not found: {eq.authority_document_path}"
        )
        findings.extend(file_findings)
        if not file_success:
            continue

        # Validate authority document naming
        # The filename should match the link text in the register (which is the descriptive filename)
        expected_name = eq.authority_document_text
        if auth_doc_path.name != expected_name:
            findings.append(f"ERROR: EQ {eq.eq_number} authority document has incorrect naming: {auth_doc_path.name} (expected: {expected_name}")

    return ValidationResult(len(findings) == 0, findings)

def validate_evidence_packages_exist() -> ValidationResult:
    """Validate that all evidence packages referenced in the register exist."""
    findings = []

    # Parse the register to get all EQ entries
    success, parse_findings, eq_entries = EngineeringRegisterParser.parse_register()
    findings.extend(parse_findings)

    if not success:
        return ValidationResult(False, findings)

    # Validate evidence directory exists
    evidence_dir_success, evidence_dir_findings = FileValidator.validate_directory_exists(
        RepositoryPath.ENGINEERING_EVIDENCE.value,
        "evidence directory not found"
    )
    findings.extend(evidence_dir_findings)
    if not evidence_dir_success:
        return ValidationResult(False, findings)

    for eq in eq_entries:
        # Validate evidence package path format
        if not eq.validate_evidence_path():
            findings.append(f"ERROR: EQ {eq.eq_number} evidence package has invalid path format: {eq.evidence_path}")
            continue

        # Check if evidence package exists
        evidence_path = eq.get_evidence_package_full_path()
        dir_success, dir_findings = FileValidator.validate_directory_exists(
            evidence_path,
            f"EQ {eq.eq_number} evidence package not found: {eq.evidence_path}"
        )
        findings.extend(dir_findings)
        if not dir_success:
            continue

        # Validate evidence package naming
        # The directory name is the last component of the evidence_path (e.g., '../evidence/EQ_0010/' -> 'EQ_0010')
        expected_name = eq.evidence_path.rstrip("/").split("/")[-1]
        if evidence_path.name != expected_name:
            findings.append(f"ERROR: EQ {eq.eq_number} evidence package has incorrect naming: {evidence_path.name} (expected: {expected_name}")

    return ValidationResult(len(findings) == 0, findings)

def validate_repository_paths() -> ValidationResult:
    """Validate repository location paths in the register."""
    findings = []

    # Parse the register to get all EQ entries
    success, parse_findings, eq_entries = EngineeringRegisterParser.parse_register()
    findings.extend(parse_findings)

    if not success:
        return ValidationResult(False, findings)

    for eq in eq_entries:
        # Validate repository location
        if not eq.validate_repository_location():
            findings.append(f"ERROR: EQ {eq.eq_number} has non-standard repository location: {eq.repository_location}")

    return ValidationResult(len(findings) == 0, findings)

def validate_status_values() -> ValidationResult:
    """Validate that all EQ status values are valid."""
    findings = []

    # Parse the register to get all EQ entries
    success, parse_findings, eq_entries = EngineeringRegisterParser.parse_register()
    findings.extend(parse_findings)

    if not success:
        return ValidationResult(False, findings)

    for eq in eq_entries:
        # Validate status
        if not eq.validate_status():
            valid_statuses = ["Completed", "Active", "Draft", "Frozen"]
            findings.append(f"ERROR: EQ {eq.eq_number} has invalid status: {eq.status} (valid: {', '.join(valid_statuses)})")

    return ValidationResult(len(findings) == 0, findings)

def validate_no_duplicate_registrations() -> ValidationResult:
    """Validate that no EQ is registered multiple times."""
    findings = []

    # Parse the register to get all EQ entries
    success, parse_findings, eq_entries = EngineeringRegisterParser.parse_register()
    findings.extend(parse_findings)

    if not success:
        return ValidationResult(False, findings)

    # Check for exact duplicates (same EQ number, auth doc path, evidence path)
    eq_entries_tuples = [(eq.eq_number, eq.authority_document_path, eq.evidence_path) for eq in eq_entries]

    seen = set()
    duplicates = []
    for entry in eq_entries_tuples:
        if entry in seen:
            duplicates.append(entry[0])
        else:
            seen.add(entry)

    if duplicates:
        findings.append(f"ERROR: Duplicate EQ registrations found: {', '.join(sorted(set(duplicates)))}")

    return ValidationResult(len(findings) == 0, findings)

def validate_register_completeness() -> ValidationResult:
    """Validate that the register is complete with all required fields."""
    findings = []

    # Parse the register to get all EQ entries
    success, parse_findings, eq_entries = EngineeringRegisterParser.parse_register()
    findings.extend(parse_findings)

    if not success:
        return ValidationResult(False, findings)

    for eq in eq_entries:
        # Check for empty fields
        if not eq.title.strip():
            findings.append(f"ERROR: EQ {eq.eq_number} has empty title")

        if not eq.status.strip():
            findings.append(f"ERROR: EQ {eq.eq_number} has empty status")

        if not eq.authority_document_text.strip():
            findings.append(f"ERROR: EQ {eq.eq_number} has empty authority document text")

        if not eq.authority_document_path.strip():
            findings.append(f"ERROR: EQ {eq.eq_number} has empty authority document path")

        if not eq.evidence_text.strip():
            findings.append(f"ERROR: EQ {eq.eq_number} has empty evidence package text")

        if not eq.evidence_path.strip():
            findings.append(f"ERROR: EQ {eq.eq_number} has empty evidence package path")

        if not eq.outcome.strip():
            findings.append(f"ERROR: EQ {eq.eq_number} has empty outcome")

        if not eq.repository_location.strip():
            findings.append(f"ERROR: EQ {eq.eq_number} has empty repository location")

    return ValidationResult(len(findings) == 0, findings)

def main():
    parser = argparse.ArgumentParser(description="Engineering Register Validation")
    parser.add_argument("--json", action="store_true", help="Output JSON to stdout")
    parser.add_argument("--strict", action="store_true", help="Exit 1 on any finding")
    parser.add_argument("--output", type=str, help="Write report to file (.json or .md)")
    args = parser.parse_args()

    # Define validation checks
    checks = [
        ("register_structure", validate_register_structure),
        ("unique_eq_numbers", validate_unique_eq_numbers),
        ("authority_documents_exist", validate_authority_documents_exist),
        ("evidence_packages_exist", validate_evidence_packages_exist),
        ("repository_paths", validate_repository_paths),
        ("status_values", validate_status_values),
        ("no_duplicate_registrations", validate_no_duplicate_registrations),
        ("register_completeness", validate_register_completeness),
    ]

    # Execute all checks using shared validation result structure
    validation_results = []
    for name, fn in checks:
        try:
            result = fn()
            validation_results.append((name, result))
        except Exception as e:
            validation_results.append((name, ValidationResult(False, [f"ERROR: Validation failed with exception: {e}"])))

    # Generate report using shared function
    report = generate_validation_report("verify_register", validation_results)

    # Output results
    if args.json:
        print(json.dumps(report, indent=2))

    if args.output:
        output_path = Path(args.output)
        if output_path.suffix == ".json":
            output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
        elif output_path.suffix == ".md":
            write_markdown_report(report, output_path)
        print(f"Report written to: {output_path}")

    # Exit with appropriate code
    if not report["overall_pass"]:
        sys.exit(EXIT_FAIL if args.strict else EXIT_FAIL)
    sys.exit(EXIT_PASS)

if __name__ == "__main__":
    main()
