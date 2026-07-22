"""
verify_imports.py — Import Boundary Verification

Scans all .py files under src/ for import boundary violations.
Production code SHALL NOT import from docs/, tools/, data/reports/
(per AGENTS.md Quality Gate 1).

Authority: Quality Gate 1 (Architecture Integrity)
Consumer: verify_all.py, CI
"""

import argparse
import ast
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

EXIT_PASS = 0
EXIT_FAIL = 1
EXIT_ERROR = 2

FORBIDDEN_ROOTS = {"docs", "tools", "data/reports"}

def _is_forbidden(import_path: str) -> bool:
    for root in FORBIDDEN_ROOTS:
        if import_path == root or import_path.startswith(root + "."):
            return True
    return False

def main():
    parser = argparse.ArgumentParser(description="Import Boundary Verification")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--output", type=str)
    args = parser.parse_args()

    src_dir = PROJECT_ROOT / "src"
    violations = []

    for py_file in sorted(src_dir.rglob("*.py")):
        try:
            tree = ast.parse(py_file.read_text(encoding="utf-8"))
        except SyntaxError:
            continue

        rel_path = str(py_file.relative_to(PROJECT_ROOT))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if _is_forbidden(alias.name):
                        violations.append({
                            "file": rel_path,
                            "line": node.lineno,
                            "import": alias.name,
                            "type": "import",
                        })
            elif isinstance(node, ast.ImportFrom):
                if node.module and _is_forbidden(node.module):
                    violations.append({
                        "file": rel_path,
                        "line": node.lineno,
                        "import": node.module,
                        "type": "importfrom",
                    })

    report = {
        "tool": "verify_imports",
        "overall_pass": len(violations) == 0,
        "violations": violations,
    }

    if args.json:
        print(json.dumps(report, indent=2))
    if args.output:
        out = Path(args.output)
        if out.suffix == ".json":
            out.write_text(json.dumps(report, indent=2), encoding="utf-8")
        else:
            lines = [f"# verify_imports Report", f"", f"**Overall:** {'PASS' if report['overall_pass'] else 'FAIL'}",
                     f"", f"**Violations:** {len(violations)}"]
            for v in violations:
                lines.append(f"- {v['file']}:{v['line']} — imports `{v['import']}` ({v['type']})")
            out.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"Report written to: {out}")

    sys.exit(EXIT_FAIL if violations else EXIT_PASS)

if __name__ == "__main__":
    main()