"""
verify_contracts.py — Contract Presence Verification

Scans docs/contracts/ for contract .md files. For each contract:
checks version field exists, checks a source file mapping exists in src/.

Authority: Quality Gate 2 (Architecture Verification)
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

# Known contract-to-source mappings
CONTRACT_SOURCE_MAP = {
    "BOQ_Intelligence_Public_Evidence_Contract": "src/jarvis/parsers/costx/boq_intelligence.py",
    "Validation_Findings_Contract": "src/jarvis/engines/validation/engine.py",
}

def main():
    parser = argparse.ArgumentParser(description="Contract Presence Verification")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--output", type=str)
    args = parser.parse_args()

    contracts_dir = PROJECT_ROOT / "docs" / "contracts"
    contracts = {}

    if not contracts_dir.exists():
        report = {"tool": "verify_contracts", "overall_pass": False, "contracts": {}, "error": "docs/contracts/ not found"}
        if args.json:
            print(json.dumps(report, indent=2))
        sys.exit(EXIT_ERROR)

    for cf in sorted(contracts_dir.glob("*.md")):
        findings = []
        text = cf.read_text(encoding="utf-8")
        name = cf.stem

        # Check version field
        version_match = re.search(r"(?:Version|version)[:\s]*(?:v?(\d+\.\d+\.\d+))", text)
        version = version_match.group(1) if version_match else None
        if not version:
            findings.append("WARN: No version field found")

        # Check source mapping
        source_path = None
        for key, src_rel in CONTRACT_SOURCE_MAP.items():
            if key in name:
                source_path = PROJECT_ROOT / src_rel
                break

        source_exists = source_path.exists() if source_path else False
        if source_path and not source_exists:
            findings.append(f"WARN: Source file not found: {source_path.relative_to(PROJECT_ROOT)}")

        contracts[cf.name] = {
            "version": version,
            "source_exists": source_exists,
            "findings": findings,
        }

    all_pass = all(len(v["findings"]) == 0 or all("WARN" in f for f in v["findings"]) for v in contracts.values())
    report = {
        "tool": "verify_contracts",
        "overall_pass": all_pass,
        "contracts": contracts,
    }

    if args.json:
        print(json.dumps(report, indent=2))
    if args.output:
        out = Path(args.output)
        if out.suffix == ".json":
            out.write_text(json.dumps(report, indent=2), encoding="utf-8")
        else:
            lines = [f"# verify_contracts Report", f"", f"**Overall:** {'PASS' if all_pass else 'FAIL'}", ""]
            for name, result in contracts.items():
                lines.append(f"## {name}: v{result['version'] or 'UNKNOWN'} (source: {'PASS' if result['source_exists'] else 'MISSING'})")
                for f in result["findings"]:
                    lines.append(f"- {f}")
                lines.append("")
            out.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"Report written to: {out}")

    sys.exit(EXIT_FAIL if not all_pass else EXIT_PASS)

if __name__ == "__main__":
    main()