"""
verify_documentation.py — Documentation Synchronization Audit

Checks structural integrity of key documentation files:
README.md, Knowledge Index, Implementation Status, AGENTS.md.

Authority: Quality Gate 5 (Release Readiness)
Consumer: verify_all.py, CI
"""

import argparse
import json
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

EXIT_PASS = 0
EXIT_FAIL = 1
EXIT_ERROR = 2

AGENTS_REQUIRED_SECTIONS = [
    "# Repository Purpose",
    "# Project Authority",
    "# Source of Truth",
    "# Required Repository Reading",
    "# Evidence Hierarchy",
    "# Engineering Philosophy",
    "# Architecture Rules",
    "# Engineering Workflow",
    "# Capability Lifecycle",
    "# Implementation Rules",
    "# Deterministic Engineering",
    "# Multi-Agent Collaboration",
    "# Documentation Responsibilities",
    "# Code Reviews",
    "# Repository Workflow",
    "# Prohibited Without Approval",
    "# Communication Guidelines",
    "# Engineering Principles",
]

def check_readme(path: Path) -> list[str]:
    findings = []
    if not path.exists():
        findings.append("ERROR: README.md not found")
        return findings
    text = path.read_text(encoding="utf-8")
    if not re.search(r"v?\d+\.\d+\.\d+", text):
        findings.append("WARN: No version string found in README.md")
    if "## Repository Structure" not in text and "Repository Structure" not in text:
        findings.append("WARN: README.md missing Repository Structure section")
    return findings

def check_knowledge_index(path: Path) -> list[str]:
    findings = []
    if not path.exists():
        findings.append("ERROR: docs/knowledge/00_Knowledge_Index.md not found")
        return findings
    text = path.read_text(encoding="utf-8")
    if "Knowledge Hierarchy" not in text:
        findings.append("WARN: 00_Knowledge_Index.md missing Knowledge Hierarchy section")
    return findings

def check_implementation_status(path: Path) -> list[str]:
    findings = []
    if not path.exists():
        findings.append("ERROR: docs/26_Implementation_Status.md not found")
        return findings
    text = path.read_text(encoding="utf-8")
    if not re.search(r"v?\d+\.\d+\.\d+", text):
        findings.append("WARN: No version in Implementation Status")
    return findings

def check_agents(path: Path) -> list[str]:
    findings = []
    if not path.exists():
        findings.append("ERROR: AGENTS.md not found")
        return findings
    text = path.read_text(encoding="utf-8")
    for section in AGENTS_REQUIRED_SECTIONS:
        if section not in text:
            findings.append(f"WARN: AGENTS.md missing section: {section}")
    return findings

def main():
    parser = argparse.ArgumentParser(description="Documentation Synchronization Audit")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--output", type=str)
    args = parser.parse_args()

    checks = {
        "README.md": check_readme(PROJECT_ROOT / "README.md"),
        "00_Knowledge_Index.md": check_knowledge_index(PROJECT_ROOT / "docs" / "knowledge" / "00_Knowledge_Index.md"),
        "26_Implementation_Status.md": check_implementation_status(PROJECT_ROOT / "docs" / "26_Implementation_Status.md"),
        "AGENTS.md": check_agents(PROJECT_ROOT / "AGENTS.md"),
    }

    all_pass = all(len(v) == 0 or all("WARN" in f for f in v) for v in checks.values())
    report = {
        "tool": "verify_documentation",
        "overall_pass": all_pass,
        "documents": {k: {"findings": v} for k, v in checks.items()},
    }

    if args.json:
        print(json.dumps(report, indent=2))
    if args.output:
        out = Path(args.output)
        if out.suffix == ".json":
            out.write_text(json.dumps(report, indent=2), encoding="utf-8")
        else:
            lines = [f"# verify_documentation Report", f"", f"**Overall:** {'PASS' if all_pass else 'FAIL'}", ""]
            for doc, result in checks.items():
                lines.append(f"## {doc}: {'PASS' if not result else 'FINDINGS'}")
                for f in result:
                    lines.append(f"- {f}")
                lines.append("")
            out.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"Report written to: {out}")

    has_errors = any("ERROR" in f for findings in checks.values() for f in findings)
    sys.exit(EXIT_FAIL if has_errors else EXIT_PASS)

if __name__ == "__main__":
    main()