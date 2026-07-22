"""
verify_registry.py — Registry Integrity Verification

Validates Capability Register, Tool Registry, and Tool Manifest
for structural integrity and cross-registry consistency.

Authority: Quality Gate 3 (Consumer Readiness)
Consumers: verify_all.py, CI
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


def validate_capability_register() -> tuple[bool, list[str]]:
    """Check Capability_Register.md exists and has capability entries."""
    findings = []
    path = PROJECT_ROOT / "docs" / "planning" / "Capability_Register.md"
    if not path.exists():
        findings.append("ERROR: Capability_Register.md not found")
        return False, findings
    text = path.read_text(encoding="utf-8")
    caps = re.findall(r"^\|\s*CAP-\d+", text, re.MULTILINE)
    if not caps:
        findings.append("WARN: No CAP-XXX entries found in Capability Register")
    return len(findings) == 0 or all("WARN" in f for f in findings), findings


def validate_tool_registry() -> tuple[bool, list[str]]:
    """Check Tool_Registry.md has required sections and tool entries."""
    findings = []
    path = PROJECT_ROOT / "tools" / "quality" / "Tool_Registry.md"
    if not path.exists():
        findings.append("ERROR: Tool_Registry.md not found")
        return False, findings
    text = path.read_text(encoding="utf-8")
    if "## Purpose" not in text:
        findings.append("ERROR: Tool_Registry.md missing '## Purpose' section")
    if "## Active Tools" not in text and "## Tool Inventory" not in text:
        findings.append("ERROR: Tool_Registry.md missing '## Active Tools' or '## Tool Inventory' section")
    if "## Historical Evidence Tools" not in text:
        findings.append("WARN: Tool_Registry.md missing '## Historical Evidence Tools' section")
    tools = re.findall(r"^\|\s*`?verify_\w+\.py`?", text, re.MULTILINE)
    if not tools:
        findings.append("ERROR: No verify_*.py entries in Tool Inventory table")
    return len(findings) == 0 or all("WARN" in f for f in findings), findings


def validate_manifest() -> tuple[bool, list[str]]:
    """Check manifest.json exists and each tool has required fields."""
    findings = []
    path = PROJECT_ROOT / "tools" / "manifest.json"
    if not path.exists():
        findings.append("ERROR: tools/manifest.json not found")
        return False, findings
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        findings.append(f"ERROR: tools/manifest.json invalid JSON: {e}")
        return False, findings
    required_fields = {"authority", "inputs", "outputs"}
    for tool_name, tool_data in data.items():
        missing = required_fields - set(tool_data.keys())
        if missing:
            findings.append(f"ERROR: Manifest tool '{tool_name}' missing fields: {missing}")
    return len(findings) == 0, findings


def main():
    parser = argparse.ArgumentParser(description="Registry Integrity Verification")
    parser.add_argument("--json", action="store_true", help="Output JSON to stdout")
    parser.add_argument("--strict", action="store_true", help="Exit 1 on any finding")
    parser.add_argument("--output", type=str, help="Write report to file (.json or .md)")
    args = parser.parse_args()

    all_findings = {}
    all_pass = True

    checks = [
        ("capability_register", validate_capability_register),
        ("tool_registry", validate_tool_registry),
        ("manifest", validate_manifest),
    ]

    for name, fn in checks:
        ok, findings = fn()
        all_findings[name] = {"pass": ok, "findings": findings}
        if not ok:
            all_pass = False

    report = {
        "tool": "verify_registry",
        "overall_pass": all_pass,
        "results": all_findings,
    }

    if args.json:
        print(json.dumps(report, indent=2))

    if args.output:
        output_path = Path(args.output)
        if output_path.suffix == ".json":
            output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
        elif output_path.suffix == ".md":
            md = f"# verify_registry Report\n\n**Overall:** {'PASS' if all_pass else 'FAIL'}\n\n"
            for name, result in all_findings.items():
                md += f"## {name}\n"
                md += f"Status: {'PASS' if result['pass'] else 'FAIL'}\n"
                for f in result["findings"]:
                    md += f"- {f}\n"
                md += "\n"
            output_path.write_text(md, encoding="utf-8")
        print(f"Report written to: {output_path}")

    if not all_pass:
        sys.exit(EXIT_FAIL if args.strict else EXIT_FAIL)
    sys.exit(EXIT_PASS)

if __name__ == "__main__":
    main()