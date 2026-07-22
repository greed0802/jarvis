"""
verify_all.py — Full Repository Verification Pipeline Orchestrator

Reads tools/manifest.json to discover quality tools dynamically.
Executes each tool, aggregates results, produces consolidated report.
Exit code reflects aggregate: non-zero if any tool fails.

Authority: Quality Gate 5 (Release Readiness)
Consumer: CI, Release Candidate check
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

EXIT_PASS = 0
EXIT_FAIL = 1
EXIT_ERROR = 2

def main():
    parser = argparse.ArgumentParser(description="Full Repository Verification Pipeline")
    parser.add_argument("--json", action="store_true", help="Output JSON to stdout")
    parser.add_argument("--output", type=str, help="Write consolidated report")
    args = parser.parse_args()

    manifest_path = PROJECT_ROOT / "tools" / "manifest.json"
    if not manifest_path.exists():
        print(json.dumps({"tool": "verify_all", "overall_pass": False, "error": "tools/manifest.json not found"}))
        sys.exit(EXIT_ERROR)

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    quality_dir = PROJECT_ROOT / "tools" / "quality"

    results = {}
    all_pass = True
    total_tools = 0
    passed_tools = 0

    for tool_name in sorted(manifest.keys()):
        total_tools += 1
        tool_path = quality_dir / f"{tool_name}.py"
        if not tool_path.exists():
            results[tool_name] = {"pass": False, "error": "Tool file not found"}
            all_pass = False
            continue

        try:
            proc = subprocess.run(
                [sys.executable, str(tool_path), "--json"],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(PROJECT_ROOT),
            )
            if proc.returncode == 0:
                passed_tools += 1
                results[tool_name] = {"pass": True, "returncode": 0}
            else:
                all_pass = False
                try:
                    detail = json.loads(proc.stdout)
                except json.JSONDecodeError:
                    detail = {"raw_stdout": proc.stdout[:500], "raw_stderr": proc.stderr[:500]}
                results[tool_name] = {"pass": False, "returncode": proc.returncode, "detail": detail}
        except subprocess.TimeoutExpired:
            all_pass = False
            results[tool_name] = {"pass": False, "error": "Timeout"}

    # Also run pytest
    pytest_result = {"pass": True, "returncode": 0}
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/", "-q", "--tb=short", "--no-header"],
            capture_output=True,
            text=True,
            timeout=600,
            cwd=str(PROJECT_ROOT),
        )
        if proc.returncode != 0:
            pytest_result = {"pass": False, "returncode": proc.returncode, "summary": proc.stdout[-500:] + proc.stderr[-200:]}
            all_pass = False
        else:
            # Capture summary for passing runs too
            pytest_result["summary"] = proc.stdout[-300:]
    except subprocess.TimeoutExpired:
        pytest_result = {"pass": False, "error": "Timeout (600s exceeded)"}
        all_pass = False

    report = {
        "tool": "verify_all",
        "overall_pass": all_pass,
        "quality_tools": {
            "total": total_tools,
            "passed": passed_tools,
            "failed": total_tools - passed_tools,
        },
        "pytest": pytest_result,
        "results": results,
    }

    if args.json:
        print(json.dumps(report, indent=2))
    if args.output:
        out = Path(args.output)
        if out.suffix == ".json":
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(report, indent=2), encoding="utf-8")
        else:
            lines = [f"# Repository Quality Report", f"", f"**Overall:** {'PASS' if all_pass else 'FAIL'}",
                     f"", f"## Quality Tools: {passed_tools}/{total_tools} passed", ""]
            for name, result in results.items():
                status = "PASS" if result.get("pass") else "FAIL"
                lines.append(f"- {name}: {status}")
            lines.append("")
            lines.append(f"## Pytest: {'PASS' if pytest_result.get('pass') else 'FAIL'}")
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"Report written to: {out}")

    sys.exit(EXIT_PASS if all_pass else EXIT_FAIL)

if __name__ == "__main__":
    main()