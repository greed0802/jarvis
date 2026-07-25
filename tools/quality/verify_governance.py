"""
verify_governance.py — Repository Governance Validation

Comprehensive validator for repository governance compliance.
Verifies Engineering Register, EQ packages, authority documents,
evidence structure, tool placement, and documentation hierarchy.

Authority: Quality Gate 2 (Architecture Verification)
Consumers: verify_all.py, CI, Pull Request validation
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Tuple, List, Dict, Any

from shared_governance import (
    PROJECT_ROOT, RepositoryPath, EngineeringQuestion, EngineeringRegisterParser,
    RepositoryModel, FileValidator, MarkdownParser, ValidationResult,
    generate_validation_report, write_markdown_report
)

EXIT_PASS = 0
EXIT_FAIL = 1
EXIT_ERROR = 2

def validate_engineering_register() -> ValidationResult:
    """Validate Engineering Register structure and content."""
    findings = []
    
    # Use shared parser for structural validation
    ok_structure, structural_findings = EngineeringRegisterParser.validate_register_structure()
    findings.extend(structural_findings)

    # Use shared parser to get EQ entries
    ok_parse, parse_findings, eq_entries = EngineeringRegisterParser.parse_register()
    findings.extend(parse_findings)

    if not ok_parse:
        return ValidationResult(False, findings)

    # Validate each EQ entry
    eq_numbers_found = []
    for eq in eq_entries:
        eq_numbers_found.append(eq.eq_number)

        # Check authority document path format and existence
        if not eq.validate_authority_document_path():
            findings.append(f"ERROR: EQ {eq.eq_number} authority document path format invalid: {eq.authority_document_path}")
        else:
            auth_doc_full_path = eq.get_authority_document_full_path()
            if not auth_doc_full_path.exists():
                findings.append(f"ERROR: EQ {eq.eq_number} authority document not found: {auth_doc_full_path}")

        # Check evidence package path format and existence
        if not eq.validate_evidence_path():
            findings.append(f"ERROR: EQ {eq.eq_number} evidence package path format invalid: {eq.evidence_path}")
        else:
            evidence_full_path = eq.get_evidence_package_full_path()
            if not evidence_full_path.exists():
                findings.append(f"ERROR: EQ {eq.eq_number} evidence package not found: {evidence_full_path}")

        # Check status is valid
        if not eq.validate_status():
            findings.append(f"ERROR: EQ {eq.eq_number} has invalid status: {eq.status}")

        # Check repository location is consistent
        if not eq.validate_repository_location():
            findings.append(f"WARN: EQ {eq.eq_number} has non-standard repository location: {eq.repository_location}")

    # Check for duplicate EQ numbers
    if len(eq_numbers_found) != len(set(eq_numbers_found)):
        duplicates = [eq for eq in eq_numbers_found if eq_numbers_found.count(eq) > 1]
        findings.append(f"ERROR: Duplicate EQ numbers found in register: {', '.join(duplicates)}")
    
    return ValidationResult(len(findings) == 0 and ok_structure and ok_parse, findings)

def validate_authority_documents() -> ValidationResult:
    """Validate all Engineering Question authority documents."""
    findings = []
    questions_dir = RepositoryPath.ENGINEERING_QUESTIONS.value

    ok_dir, dir_findings = FileValidator.validate_directory_exists(questions_dir, "questions directory not found")
    findings.extend(dir_findings)
    if not ok_dir:
        return ValidationResult(False, findings)

    eq_files = list(questions_dir.glob("EQ_*.md"))
    if not eq_files:
        findings.append("WARN: No EQ authority documents found in questions directory")
        return ValidationResult(True, findings) # Warning, not error

    required_sections = [
        "## Status",
        "## Purpose",
        "## Engineering Question",
        "## Investigation Scope",
        "## Methodology",
        "## Deliverables",
        "## Success Criteria",
        "## Out of Scope",
        "## Conclusion"
    ]

    for eq_file in eq_files:
        file_ok, file_findings = FileValidator.validate_file_content_contains(
            eq_file, required_sections, f"{eq_file.name}"
        )
        findings.extend(file_findings)
        
        if not file_ok:
            # Continue to other checks for this file, just report content issue
            pass

        try:
            content = eq_file.read_text(encoding="utf-8")
            status_match = re.search(r"## Status\n([^\n]+)", content)
            if not status_match:
                findings.append(f"ERROR: {eq_file.name} missing status definition under '## Status'")
            else:
                status = status_match.group(1).strip()
                if status not in ["COMPLETED", "ACTIVE", "DRAFT", "FROZEN"]:
                    findings.append(f"ERROR: {eq_file.name} has invalid status: {status}")
        except Exception as e:
            findings.append(f"ERROR: Could not read {eq_file.name} for status check: {e}")

    return ValidationResult(len(findings) == 0, findings)

def validate_evidence_packages() -> ValidationResult:
    """Validate evidence package structure and completeness."""
    findings = []
    evidence_dir = RepositoryPath.ENGINEERING_EVIDENCE.value

    ok_dir, dir_findings = FileValidator.validate_directory_exists(evidence_dir, "evidence directory not found")
    findings.extend(dir_findings)
    if not ok_dir:
        return ValidationResult(False, findings)

    eq_packages = [d for d in evidence_dir.iterdir() if d.is_dir() and d.name.startswith("EQ_")]
    if not eq_packages:
        findings.append("WARN: No evidence packages found in evidence directory")
        return ValidationResult(True, findings) # Warning, not error

    required_readme_sections = [
        "## Engineering Question",
        "## Package Contents",
        "## Governance Compliance"
    ]

    for package in eq_packages:
        readme_path = package / "README.md"
        
        ok_readme_exists, readme_exists_findings = FileValidator.validate_file_exists(
            readme_path, f"Evidence package {package.name} missing README.md"
        )
        findings.extend(readme_exists_findings)
        if not ok_readme_exists:
            continue # Can't validate content if README doesn't exist

        ok_readme_content, readme_content_findings = FileValidator.validate_file_content_contains(
            readme_path, required_readme_sections, f"{package.name}/README.md"
        )
        findings.extend(readme_content_findings)

        try:
            readme_content = readme_path.read_text(encoding="utf-8")
            if "Authority Document:" not in readme_content:
                findings.append(f"ERROR: {package.name}/README.md missing authority document reference")
        except Exception as e:
            findings.append(f"ERROR: Could not read {package.name}/README.md for reference check: {e}")

    return ValidationResult(len(findings) == 0, findings)

def validate_repository_organization() -> ValidationResult:
    """Validate overall repository structure and organization."""
    findings = []

    # Check for repository root pollution (existing logic, not in shared library yet)
    root_files = [f.name for f in PROJECT_ROOT.iterdir() if f.is_file()]
    expected_root_files = {
        ".gitignore", "AGENTS.md", "app.py", "LICENSE", "pytest.ini",
        "README.md", "requirements.txt"
    }
    unexpected_files = set(root_files) - expected_root_files
    if unexpected_files:
        findings.append(f"WARN: Unexpected files in repository root: {', '.join(unexpected_files)}")

    # Check main required directories
    for req_dir_path in RepositoryModel.get_required_directories():
        ok, dir_findings = FileValidator.validate_directory_exists(req_dir_path, f"Required directory missing: {req_dir_path.relative_to(PROJECT_ROOT)}")
        findings.extend(dir_findings)
    
    # Additional docs structure checks (not yet in shared model, kept local)
    docs_dir = RepositoryPath.DOCS_ROOT.value
    required_docs_subdirs = [
        "engineering", "decisions", "contracts", "knowledge", "architecture"
    ]
    for sub_dir in required_docs_subdirs:
        sub_path = docs_dir / sub_dir
        ok, sub_dir_findings = FileValidator.validate_directory_exists(sub_path, f"Required docs directory missing: {sub_path.relative_to(PROJECT_ROOT)}")
        findings.extend(sub_dir_findings)

    # Additional engineering structure checks (not yet in shared model, kept local)
    engineering_dir = RepositoryPath.ENGINEERING_QUESTIONS.value.parent # docs/engineering
    required_engineering_subdirs = [
        "evidence", "questions"
    ]
    for sub_dir in required_engineering_subdirs:
        sub_path = engineering_dir / sub_dir
        ok, sub_dir_findings = FileValidator.validate_directory_exists(sub_path, f"Required engineering directory missing: {sub_path.relative_to(PROJECT_ROOT)}")
        findings.extend(sub_dir_findings)

    # Additional tools structure checks (not yet in shared model, kept local)
    tools_dir = RepositoryPath.TOOLS_ROOT.value
    required_tools_subdirs = [
        "quality"
    ]
    for sub_dir in required_tools_subdirs:
        sub_path = tools_dir / sub_dir
        ok, sub_dir_findings = FileValidator.validate_directory_exists(sub_path, f"Required tools directory missing: {sub_path.relative_to(PROJECT_ROOT)}")
        findings.extend(sub_dir_findings)

    return ValidationResult(len(findings) == 0, findings)

def validate_freeze_checklist() -> ValidationResult:
    """Validate freeze checklist presence and structure."""
    findings = []
    checklist_path = PROJECT_ROOT / "docs" / "engineering" / "Engineering_Question_Freeze_Checklist.md"

    ok_exists, exists_findings = FileValidator.validate_file_exists(checklist_path, "Engineering_Question_Freeze_Checklist.md not found")
    findings.extend(exists_findings)
    if not ok_exists:
        return ValidationResult(False, findings)

    required_sections = [
        "## Freeze Checklist",
        "## Freeze Process",
        "## Checklist Version History",
        "## Relationship to Governance"
    ]
    ok_sections, sections_findings = FileValidator.validate_file_content_contains(
        checklist_path, required_sections, "Freeze checklist"
    )
    findings.extend(sections_findings)

    try:
        content = checklist_path.read_text(encoding="utf-8")
        # Check for checklist items (specific content)
        if "Authority Document Complete" not in content:
            findings.append("ERROR: Freeze checklist missing 'Authority Document Complete' item")
        if "Evidence Package Complete" not in content:
            findings.append("ERROR: Freeze checklist missing 'Evidence Package Complete' item")
        if "Project Owner Approval Recorded" not in content:
            findings.append("ERROR: Freeze checklist missing 'Project Owner Approval Recorded' item")

    except Exception as e:
        findings.append(f"ERROR: Could not read freeze checklist for item checks: {e}")
        return ValidationResult(False, findings) # if we can't read it, all checks fail

    return ValidationResult(len(findings) == 0, findings)

def validate_tool_placement() -> ValidationResult:
    """Validate tool organization and placement."""
    findings = []
    tools_dir = RepositoryPath.TOOLS_ROOT.value
    quality_dir = RepositoryPath.TOOLS_QUALITY.value

    ok_quality_dir, quality_dir_findings = FileValidator.validate_directory_exists(quality_dir, "tools/quality directory not found")
    findings.extend(quality_dir_findings)
    if not ok_quality_dir:
        return ValidationResult(False, findings)

    # Check for quality tools based on shared model
    expected_quality_tools = RepositoryModel.get_quality_tool_locations()
    for tool_name, expected_path in expected_quality_tools.items():
        tool_full_path = expected_path / tool_name
        ok, tool_findings = FileValidator.validate_file_exists(tool_full_path, f"Quality tool {tool_name} not found at {expected_path.relative_to(PROJECT_ROOT)}")
        findings.extend(tool_findings)
        
        if ok and not tool_full_path.name.startswith("verify_"):
             findings.append(f"ERROR: Quality tool has incorrect naming: {tool_full_path.name}")

    # Check for manifest.json (existing logic)
    manifest_path = tools_dir / "manifest.json"
    ok_manifest, manifest_exists_findings = FileValidator.validate_file_exists(manifest_path, "tools/manifest.json not found")
    findings.extend(manifest_exists_findings)

    if ok_manifest:
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            if not isinstance(manifest, dict):
                findings.append("ERROR: tools/manifest.json is not a valid JSON object")

            # Check that all tools in manifest exist
            for tool_name in manifest.keys():
                tool_path = quality_dir / f"{tool_name}.py"
                if not tool_path.exists():
                    findings.append(f"ERROR: Tool in manifest but not found: {tool_name}.py")
        except json.JSONDecodeError:
            findings.append("ERROR: tools/manifest.json is not valid JSON")
        except Exception as e:
            findings.append(f"ERROR: Could not read tools/manifest.json: {e}")

    # Check for historical tools (should be preserved) (existing logic)
    historical_tools = list(tools_dir.glob("eq*.py"))
    if historical_tools:
        findings.append(f"INFO: Found {len(historical_tools)} historical tools in tools/ root (preserved as evidence)")

    return ValidationResult(len(findings) == 0, findings)

def validate_documentation_hierarchy() -> ValidationResult:
    """Validate documentation structure and cross-references."""
    findings = []
    docs_dir = RepositoryPath.DOCS_ROOT.value

    # Check main documentation files using shared model
    for doc_path in RepositoryModel.get_required_documentation_files():
        ok, doc_findings = FileValidator.validate_file_exists(doc_path, f"Missing main documentation file: {doc_path.name}")
        findings.extend(doc_findings)

    # Check engineering documentation (existing logic, some parts may be added to shared model later)
    engineering_dir = docs_dir / "engineering"
    engineering_docs = [
        "Engineering_Authority.md",
        "Engineering_Governance.md",
        "Engineering_Register.md",
        "Quality_Assurance_Constitution.md",
        "Engineering_Question_Freeze_Checklist.md"
    ]
    for doc in engineering_docs:
        doc_path = engineering_dir / doc
        ok, doc_findings = FileValidator.validate_file_exists(doc_path, f"Missing engineering documentation: {doc}")
        findings.extend(doc_findings)

    # Check decisions directory and ADR numbering consistency (existing logic)
    decisions_dir = docs_dir / "decisions"
    if decisions_dir.exists():
        adr_files = list(decisions_dir.glob("ADR_*.md"))
        if not adr_files:
            findings.append("WARN: No ADR files found in docs/decisions/")
        else:
            adr_numbers = []
            for adr in adr_files:
                match = re.match(r"ADR_(\d+)_", adr.name)
                if match:
                    adr_numbers.append(int(match.group(1)))

            if adr_numbers:
                expected_numbers = set(range(1, max(adr_numbers) + 1))
                actual_numbers = set(adr_numbers)
                missing_numbers = expected_numbers - actual_numbers
                if missing_numbers:
                    findings.append(f"WARN: Missing ADR numbers: {', '.join(map(str, sorted(missing_numbers)))}")
    else:
        findings.append("ERROR: docs/decisions directory not found.") # Should be caught by validate_repository_organization but good to have here too

    return ValidationResult(len(findings) == 0, findings)

def validate_generated_artifacts() -> ValidationResult:
    """Validate placement of generated artifacts and reports."""
    findings = []

    # Check data/reports directory (existing logic, may be added to shared model later)
    reports_dir = PROJECT_ROOT / "data" / "reports"
    if not reports_dir.exists():
        findings.append("WARN: data/reports directory not found (may be created on demand)")
    else:
        quality_reports = list(reports_dir.glob("*Quality*.md"))
        if quality_reports:
            findings.append(f"INFO: Found {len(quality_reports)} quality reports in data/reports/")

    # Check archive structure (existing logic, may be added to shared model later)
    archive_dir = PROJECT_ROOT / "archive"
    ok_archive_dir, archive_dir_findings = FileValidator.validate_directory_exists(archive_dir, "archive directory not found")
    findings.extend(archive_dir_findings)

    archive_docs = [
        "Archive_Inventory.md",
        "Archive_Policy.md"
    ]
    for doc in archive_docs:
        doc_path = archive_dir / doc
        ok, doc_findings = FileValidator.validate_file_exists(doc_path, f"Missing archive documentation: {doc}")
        findings.extend(doc_findings)

    return ValidationResult(len(findings) == 0, findings)

def main():
    parser = argparse.ArgumentParser(description="Repository Governance Validation")
    parser.add_argument("--json", action="store_true", help="Output JSON to stdout")
    parser.add_argument("--strict", action="store_true", help="Exit 1 on any finding")
    parser.add_argument("--output", type=str, help="Write report to file (.json or .md)")
    args = parser.parse_args()

    # Define validation checks
    checks_to_run = [
        ("engineering_register", validate_engineering_register),
        ("authority_documents", validate_authority_documents),
        ("evidence_packages", validate_evidence_packages),
        ("repository_organization", validate_repository_organization),
        ("freeze_checklist", validate_freeze_checklist),
        ("tool_placement", validate_tool_placement),
        ("documentation_hierarchy", validate_documentation_hierarchy),
        ("generated_artifacts", validate_generated_artifacts),
    ]

    all_check_results = []
    for name, fn in checks_to_run:
        try:
            result = fn()
            all_check_results.append((name, result))
        except Exception as e:
            all_check_results.append((name, ValidationResult(False, [f"ERROR: Validation failed with exception: {e}"])))
            
    # Generate report using shared utility
    report = generate_validation_report("verify_governance", all_check_results)
    all_pass = report["overall_pass"]

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
    if not all_pass:
        sys.exit(EXIT_FAIL if args.strict else EXIT_FAIL)
    sys.exit(EXIT_PASS)

if __name__ == "__main__":
    main()
