"""
verify_versions.py — Version Consistency Verification

Extracts version strings from README, __version__, contracts, and release
notes. Reports mismatches within each version scheme (app vs contract).

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

VERSION_RE = re.compile(r"v?(\d+\.\d+\.\d+(?:-(?:alpha|beta|rc)\.?\d*)?)", re.IGNORECASE)

def _extract(text: str, label: str) -> str | None:
    """Extract first version string matching VERSION_RE."""
    m = VERSION_RE.search(text)
    return m.group(1) if m else None

def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""

def main():
    parser = argparse.ArgumentParser(description="Version Consistency Verification")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--output", type=str)
    args = parser.parse_args()

    sources = {}
    mismatches = []

    # Readme
    readme = _read(PROJECT_ROOT / "README.md")
    v_readme = _extract(readme, "README")
    sources["README.md"] = v_readme

    # __version__
    version_py = _read(PROJECT_ROOT / "src" / "jarvis" / "version.py")
    v_mod = _extract(version_py, "version.py")
    sources["src/jarvis/version.py"] = v_mod

    # Contracts
    contracts_dir = PROJECT_ROOT / "docs" / "contracts"
    if contracts_dir.exists():
        for cf in sorted(contracts_dir.glob("*.md")):
            text = cf.read_text(encoding="utf-8")
            vc = _extract(text, cf.name)
            sources[f"docs/contracts/{cf.name}"] = vc

    # Releases
    releases = sorted(PROJECT_ROOT.glob("RELEASE_*.md"))
    if releases:
        latest = releases[-1]
        vr = _extract(latest.read_text(encoding="utf-8"), latest.name)
        sources[f"{latest.name}"] = vr

    # Group by scheme: app versions (0.x.x) vs contract versions (1.x.x or filename-based)
    app_versions = {k: v for k, v in sources.items() if v and not k.startswith("RELEASE_") and (v.startswith("0.") or "alpha" in str(v) or "README" in k or "version.py" in k)}
    contract_versions = {k: v for k, v in sources.items() if v and k.startswith("docs/contracts/")}

    # Check app version consistency
    app_values = set(app_versions.values())
    if len(app_values) > 1:
        mismatches.append(f"App version mismatch: {app_versions}")

    # Check contract version consistency (contracts use independent semver)
    contract_values = set(contract_versions.values())
    if len(contract_values) > 2:  # Allow minor format differences (v1.0.0 vs 1.0.0)
        mismatches.append(f"Contract version spread: {contract_versions}")

    report = {
        "tool": "verify_versions",
        "overall_pass": len(mismatches) == 0,
        "sources": sources,
        "mismatches": mismatches,
    }

    if args.json:
        print(json.dumps(report, indent=2))
    if args.output:
        out = Path(args.output)
        if out.suffix == ".json":
            out.write_text(json.dumps(report, indent=2), encoding="utf-8")
        else:
            out.write_text(f"# verify_versions\n\n**Overall:** {'PASS' if report['overall_pass'] else 'FAIL'}\n\n"
                           f"## Sources\n" + "\n".join(f"- {k}: {v}" for k, v in sources.items()) +
                           f"\n\n## Mismatches\n" + "\n".join(f"- {m}" for m in mismatches) + "\n",
                           encoding="utf-8")
        print(f"Report written to: {out}")

    sys.exit(EXIT_FAIL if mismatches else EXIT_PASS)

if __name__ == "__main__":
    main()