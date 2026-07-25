"""
verify_links.py — Markdown Link Validation

Automated verification of all markdown links in the repository.
Validates internal references, relative paths, cross-document links,
and Engineering Question references.

Authority: Quality Gate 1 (Mechanical Verification)
Consumers: verify_all.py, CI, Pull Request validation
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Tuple, List, Dict, Set
from urllib.parse import urlparse

from shared_governance import (
    PROJECT_ROOT, RepositoryPath, EngineeringQuestion, EngineeringRegisterParser,
    RepositoryModel, FileValidator, MarkdownParser, ValidationResult,
    generate_validation_report, write_markdown_report
)

EXIT_PASS = 0
EXIT_FAIL = 1
EXIT_ERROR = 2

def is_external_link(url: str) -> bool:
    """Check if a URL is external (http/https)."""
    return url.startswith(('http://', 'https://', 'ftp://'))

def is_anchor_link(url: str) -> bool:
    """Check if a URL is an anchor link (#...)."""
    return url.startswith('#')

def validate_markdown_links() -> ValidationResult:
    """Validate all markdown links in the repository."""
    findings = []
    markdown_files = MarkdownParser.find_all_markdown_files(PROJECT_ROOT)

    if not markdown_files:
        findings.append("WARN: No markdown files found in repository")
        return ValidationResult(True, findings)

    total_links = 0
    broken_links = 0
    external_links = 0
    anchor_links = 0

    for file_path in markdown_files:
        relative_path = file_path.relative_to(PROJECT_ROOT)
        links = MarkdownParser.extract_markdown_links(file_path)

        for line_num, link_text, url in links:
            total_links += 1

            # Skip external links
            if is_external_link(url):
                external_links += 1
                continue

            # Skip anchor links
            if is_anchor_link(url):
                anchor_links += 1
                continue

            # Resolve relative paths
            if url.startswith('/') and not url.startswith('//'): # Absolute path within repo
                target_path = PROJECT_ROOT / url.lstrip('/')
                if not target_path.exists():
                    findings.append(f"ERROR: {relative_path}:{line_num} - Broken absolute link: [{link_text}]({url})")
                    broken_links += 1
            else: # Relative path
                base_dir = file_path.parent
                target_path = FileValidator.normalize_and_resolve_path(url, base_dir)

                if target_path is None:
                    findings.append(f"ERROR: {relative_path}:{line_num} - Invalid path resolution for: [{link_text}]({url})")
                    broken_links += 1
                    continue
                
                # Check if target exists
                if not target_path.exists():
                    findings.append(f"ERROR: {relative_path}:{line_num} - Broken relative link: [{link_text}]({url}) -> {target_path}")
                    broken_links += 1
    
    if broken_links == 0:
        findings.append(f"INFO: All {total_links} links validated successfully ({external_links} external, {anchor_links} anchor links)")
    else:
        findings.insert(0, f"INFO: Link validation completed - {total_links} total links, {broken_links} broken, {external_links} external, {anchor_links} anchor links")

    return ValidationResult(broken_links == 0, findings)

def validate_engineering_register_links() -> ValidationResult:
    """Validate links specifically in the Engineering Register."""
    findings = []
    register_path = RepositoryPath.ENGINEERING_REGISTER.value

    ok_register_exists, exists_findings = FileValidator.validate_file_exists(register_path, "Engineering_Register.md not found")
    findings.extend(exists_findings)
    if not ok_register_exists:
        return ValidationResult(False, findings)

    ok_parse, parse_findings, eq_entries = EngineeringRegisterParser.parse_register()
    findings.extend(parse_findings)
    if not ok_parse:
        return ValidationResult(False, findings)

    for eq in eq_entries:
        auth_doc_full = eq.get_authority_document_full_path()
        if not auth_doc_full.exists():
            findings.append(f"ERROR: EQ {eq.eq_number} authority document link broken: {eq.authority_document_path}")

        evidence_full = eq.get_evidence_package_full_path()
        if not evidence_full.exists():
            findings.append(f"ERROR: EQ {eq.eq_number} evidence package link broken: {eq.evidence_path}")
    
    if not findings:
        findings.append("INFO: All Engineering Register links validated successfully")

    return ValidationResult(len(findings) == 0, findings)

def validate_evidence_package_links() -> ValidationResult:
    """Validate links in all evidence package README files."""
    findings = []
    evidence_dir = RepositoryPath.ENGINEERING_EVIDENCE.value

    ok_dir, dir_findings = FileValidator.validate_directory_exists(evidence_dir, "evidence directory not found")
    findings.extend(dir_findings)
    if not ok_dir:
        return ValidationResult(False, findings)

    eq_packages = [d for d in evidence_dir.iterdir() if d.is_dir() and d.name.startswith("EQ_")]
    if not eq_packages:
        findings.append("WARN: No evidence packages found")
        return ValidationResult(True, findings)

    for package in eq_packages:
        readme_path = package / "README.md"
        ok_readme_exists, readme_exists_findings = FileValidator.validate_file_exists(readme_path, f"Evidence package {package.name} missing README.md")
        findings.extend(readme_exists_findings)
        if not ok_readme_exists:
            continue

        links = MarkdownParser.extract_markdown_links(readme_path)
        found_auth_doc_link = False
        for _, link_text, url in links:
            if "Authority Document:" in link_text: # crude check, improve if needed
                found_auth_doc_link = True
                base_dir = readme_path.parent
                target_path = FileValidator.normalize_and_resolve_path(url, base_dir)

                if target_path is None or not target_path.exists():
                    findings.append(f"ERROR: {package.name}/README.md - Broken authority document link: [{link_text}]({url})")
                
                # Check for relative link format (../questions/EQ_XXXX.md)
                if not (url.startswith('../questions/') and url.endswith('.md')):
                     findings.append(f"WARN: {package.name}/README.md - Authority document link has non-standard format: [{link_text}]({url})")
                break
        
        if not found_auth_doc_link:
            findings.append(f"ERROR: {package.name}/README.md missing authority document link (or improperly formatted link text)")

    if not findings:
        findings.append("INFO: All evidence package README links validated successfully")
    return ValidationResult(len(findings) == 0, findings)

def validate_readme_references() -> ValidationResult:
    """Validate references in key README files."""
    findings = []
    readme_paths = [
        PROJECT_ROOT / "README.md",
        RepositoryPath.DOCS_ROOT.value / "README.md",
        RepositoryPath.DOCS_ROOT.value / "engineering" / "README.md"
    ]

    for readme_path in readme_paths:
        relative_path_str = readme_path.relative_to(PROJECT_ROOT)
        ok_exists, exists_findings = FileValidator.validate_file_exists(readme_path, f"README file not found: {relative_path_str}")
        findings.extend(exists_findings)
        if not ok_exists:
            continue

        links = MarkdownParser.extract_markdown_links(readme_path)

        for line_num, link_text, url in links:
            if is_external_link(url) or is_anchor_link(url):
                continue
            
            # Resolve relative paths
            if url.startswith('/') and not url.startswith('//'): # Absolute path within repo
                target_path = PROJECT_ROOT / url.lstrip('/')
                if not target_path.exists():
                    findings.append(f"ERROR: {relative_path_str}:{line_num} - Broken absolute link: [{link_text}]({url})")
            else: # Relative path
                base_dir = readme_path.parent
                target_path = FileValidator.normalize_and_resolve_path(url, base_dir)

                if target_path is None or not target_path.exists():
                    findings.append(f"ERROR: {relative_path_str}:{line_num} - Broken relative link: [{link_text}]({url})")

    if not findings:
        findings.append("INFO: All README references validated successfully")
    return ValidationResult(len(findings) == 0, findings)

def validate_cross_document_references() -> ValidationResult:
    """Validate cross-references between governance documents."""
    findings = []

    # Define key governance documents and their expected locations
    governance_docs = [
        RepositoryPath.ENGINEERING_REGISTER.value,
        RepositoryPath.DOCS_ROOT.value / "engineering" / "Engineering_Governance.md",
        RepositoryPath.DOCS_ROOT.value / "engineering" / "Engineering_Authority.md",
        RepositoryPath.DOCS_ROOT.value / "engineering" / "Quality_Assurance_Constitution.md",
        RepositoryPath.DOCS_ROOT.value / "engineering" / "Engineering_Question_Freeze_Checklist.md",
        PROJECT_ROOT / "AGENTS.md" # Special case, not in docs/engineering
    ]

    for doc_path in governance_docs:
        doc_name = doc_path.name
        relative_path_str = doc_path.relative_to(PROJECT_ROOT)

        ok_exists, exists_findings = FileValidator.validate_file_exists(doc_path, f"Missing governance document: {relative_path_str}")
        findings.extend(exists_findings)
        if not ok_exists:
            continue

        links = MarkdownParser.extract_markdown_links(doc_path)

        for line_num, link_text, url in links:
            if is_external_link(url) or is_anchor_link(url):
                continue
            
            # Resolve relative paths
            if url.startswith('/') and not url.startswith('//'): # Absolute path within repo
                target_path = PROJECT_ROOT / url.lstrip('/')
                if not target_path.exists():
                    findings.append(f"ERROR: {relative_path_str}:{line_num} - Broken absolute link: [{link_text}]({url})")
            else: # Relative path
                base_dir = doc_path.parent
                target_path = FileValidator.normalize_and_resolve_path(url, base_dir)

                if target_path is None or not target_path.exists():
                    findings.append(f"ERROR: {relative_path_str}:{line_num} - Broken relative link: [{link_text}]({url})")

    if not findings:
        findings.append("INFO: All cross-document references validated successfully")
    return ValidationResult(len(findings) == 0, findings)

def main():
    parser = argparse.ArgumentParser(description="Markdown Link Validation")
    parser.add_argument("--json", action="store_true", help="Output JSON to stdout")
    parser.add_argument("--strict", action="store_true", help="Exit 1 on any finding")
    parser.add_argument("--output", type=str, help="Write report to file (.json or .md)")
    args = parser.parse_args()

    checks_to_run = [
        ("markdown_links", validate_markdown_links),
        ("engineering_register_links", validate_engineering_register_links),
        ("evidence_package_links", validate_evidence_package_links),
        ("readme_references", validate_readme_references),
        ("cross_document_references", validate_cross_document_references),
    ]

    all_check_results = []
    for name, fn in checks_to_run:
        try:
            result = fn()
            all_check_results.append((name, result))
        except Exception as e:
            all_check_results.append((name, ValidationResult(False, [f"ERROR: Validation failed with exception: {e}"])))
            
    report = generate_validation_report("verify_links", all_check_results)
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
