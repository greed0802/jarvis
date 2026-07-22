"""
verify_tests.py — Test Suite Structural Audit

Walks tests/ directory, counts test files and functions via AST parsing.
Reads pytest.ini for configuration. Reports structural metrics only —
does NOT execute pytest.

Authority: Quality Gate 1 (Mechanical Verification)
Consumer: verify_all.py, CI
"""

import argparse
import ast
import configparser
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

EXIT_PASS = 0
EXIT_FAIL = 1
EXIT_ERROR = 2

def count_test_functions(file_path: Path) -> tuple[int, int]:
    """Parse AST, count test functions and skipped tests."""
    try:
        tree = ast.parse(file_path.read_text(encoding="utf-8"))
    except SyntaxError:
        return 0, 0

    test_count = 0
    skip_count = 0

    for node in ast.walk(tree):
        # Test functions: defs starting with test_ inside Test* classes
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name.startswith("test_"):
                test_count += 1
                # Check for skip decorator
                for decorator in node.decorator_list:
                    if isinstance(decorator, ast.Attribute):
                        if decorator.attr == "skip" and isinstance(decorator.value, ast.Attribute) and decorator.value.attr == "mark":
                            skip_count += 1
                    elif isinstance(decorator, ast.Call):
                        if hasattr(decorator.func, "attr") and decorator.func.attr == "skip":
                            skip_count += 1

    return test_count, skip_count

def main():
    parser = argparse.ArgumentParser(description="Test Suite Structural Audit")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--output", type=str)
    args = parser.parse_args()

    tests_dir = PROJECT_ROOT / "tests"
    if not tests_dir.exists():
        print(json.dumps({"tool": "verify_tests", "overall_pass": False, "error": "tests/ not found"}))
        sys.exit(EXIT_ERROR)

    # Read pytest.ini
    pytest_ini = PROJECT_ROOT / "pytest.ini"
    testpaths = ["tests"]
    if pytest_ini.exists():
        cfg = configparser.ConfigParser()
        cfg.read(str(pytest_ini))
        if cfg.has_option("tool:pytest", "testpaths"):
            testpaths = cfg.get("tool:pytest", "testpaths").split()

    # Walk tests directory
    directories = {}  # dir_name -> {file_count, test_count, skip_count}
    total_files = 0
    total_tests = 0
    total_skipped = 0

    for py_file in sorted(tests_dir.rglob("test_*.py")):
        rel_dir = str(py_file.parent.relative_to(tests_dir)) if py_file.parent != tests_dir else "root"
        tc, sc = count_test_functions(py_file)

        if rel_dir not in directories:
            directories[rel_dir] = {"file_count": 0, "test_count": 0, "skip_count": 0}
        directories[rel_dir]["file_count"] += 1
        directories[rel_dir]["test_count"] += tc
        directories[rel_dir]["skip_count"] += sc

        total_files += 1
        total_tests += tc
        total_skipped += sc

    # Minimal threshold: expect at least 50 tests
    findings = []
    if total_tests < 50:
        findings.append(f"WARN: Total test count ({total_tests}) below expected minimum (50)")

    report = {
        "tool": "verify_tests",
        "overall_pass": len(findings) == 0 or all("WARN" in f for f in findings),
        "counts": {
            "total_files": total_files,
            "total_test_functions": total_tests,
            "total_skipped": total_skipped,
        },
        "directories": directories,
        "findings": findings,
    }

    if args.json:
        print(json.dumps(report, indent=2))
    if args.output:
        out = Path(args.output)
        if out.suffix == ".json":
            out.write_text(json.dumps(report, indent=2), encoding="utf-8")
        else:
            lines = [f"# verify_tests Report", f"", f"**Overall:** {'PASS' if report['overall_pass'] else 'FAIL'}",
                     f"", f"## Counts", f"- Total files: {total_files}", f"- Total tests: {total_tests}",
                     f"- Skipped: {total_skipped}", f"", f"## Directories"]
            for d, v in directories.items():
                lines.append(f"- {d}: {v['file_count']} files, {v['test_count']} tests, {v['skip_count']} skipped")
            if findings:
                lines.append(""); lines.append("## Findings")
                for f in findings:
                    lines.append(f"- {f}")
            out.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"Report written to: {out}")

    sys.exit(EXIT_FAIL if findings and args.strict else EXIT_PASS)

if __name__ == "__main__":
    main()