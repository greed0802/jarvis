# verify_all.py Investigation Report

**Date:** 2026-07-22
**Classification:** Resolved (fix applied in M10, re-verified)
**Root Cause:** Subprocess timeout (120s) insufficient for full pytest suite
**Fix:** Timeout increased to 600s. Summary capture added for passing runs.

---

## Original Symptom

verify_all.py reported:
```json
{
  "pytest": {"pass": false, "error": "Timeout"}
}
```

While direct pytest execution:
```
150 passed, 8 skipped in 258.43s
```

The orchestrator claimed pytest FAIL when pytest actually PASSED. This was a **false negative** caused by insufficient subprocess timeout.

---

## Root Cause Analysis

### Option A — verify_all.py bug
**FALSE.** No code logic error. The tool correctly captured `TimeoutExpired` and reported failure — but the timeout was too short.

### Option B — pytest invocation bug
**FALSE.** The subprocess invocation is correct:
```python
proc = subprocess.run(
    [sys.executable, "-m", "pytest", "tests/", "-q", "--tb=short", "--no-header"],
    capture_output=True, text=True, timeout=600,
    cwd=str(PROJECT_ROOT),
)
```

### Option C — environment issue
**FALSE.** The virtual environment is healthy. Python and pytest are correctly installed.

### Option D — report generation bug
**FALSE.** Reports are generated correctly when subprocess completes.

### Option E — false positive (actually: timeout value too low)
**TRUE (primary cause).** The original timeout of 120 seconds was lower than the actual test suite duration of ~258 seconds (150 tests across 3 domains: BOQ extraction, workbook parsing, lifecycle, BOQ intelligence, validation engine).

### Additional Finding: verify_tests.py skip counting discrepancy
`verify_tests.py` reports `total_skipped: 0` while pytest reports 8 skipped. This is a **design limitation**, not a bug:

- The 8 skipped tests in `test_workbook_observe_historical.py` use `pytest.skip()` as a **function body call**, not as a decorator
- verify_tests.py uses AST parsing which can detect `@pytest.mark.skip` decorators but cannot detect runtime `pytest.skip()` calls inside function bodies
- This is inherent to static analysis — runtime behavior is not visible to AST

**No fix needed.** The orchestrator's subprocess-based pytest execution correctly captures skip counts in the summary. The static analysis tool's skip count is approximate by design (decorator-scoped skips only).

---

## Resolution

### Applied Fixes (M10, re-verified)

| File | Change | Line(s) |
|------|--------|---------|
| `tools/quality/verify_all.py` | `timeout=120` → `timeout=600` | Line 80 |
| `tools/quality/verify_all.py` | Added `else` branch to capture passing pytest summary | Lines 86-88 |
| `tools/quality/verify_all.py` | Improved timeout error message to `"Timeout (600s exceeded)"` | Line 90 |

### Current State

The orchestrator correctly reports:

```json
{
  "tool": "verify_all",
  "overall_pass": true,
  "quality_tools": { "total": 6, "passed": 6, "failed": 0 },
  "pytest": {
    "pass": true,
    "returncode": 0,
    "summary": "150 passed, 8 skipped in 196.01s (0:03:16)"
  },
  "results": {
    "verify_contracts": {"pass": true, "returncode": 0},
    "verify_documentation": {"pass": true, "returncode": 0},
    "verify_imports": {"pass": true, "returncode": 0},
    "verify_registry": {"pass": true, "returncode": 0},
    "verify_tests": {"pass": true, "returncode": 0},
    "verify_versions": {"pass": true, "returncode": 0}
  }
}
```

---

## Regression Verification

### verify_all.py
```
overall_pass: true
quality_tools: 6/6 passed
pytest: PASS (150 passed, 8 skipped)
```

### Pytest (direct)
```
150 passed, 8 skipped in ~196s
FAILED: 0
```

### Both results agree
- verify_all.py reports pytest = **PASS**
- pytest direct run = **PASS**
- Both show 150 passed, 8 skipped
- **No false PASS, no false FAIL**

---

## Known Limitations (Not Bugs)

| Limitation | Impact | Mitigation |
|------------|--------|------------|
| verify_tests.py skip count = 0, actual = 8 | Low. Static analysis limitation | Pytest execution in verify_all.py provides actual skip count |
| 600s timeout may still be exceeded if test suite grows | Potential future issue | Monitor, adjust if test count significantly increases |
| Network/file system latency not accounted for | Minor variance in test duration | pytest -q flag minimizes I/O, ~3-min baseline is stable |

---

## Conclusion

The verify_all.py false failure was caused by a subprocess timeout that was too short for the test suite duration. The fix (600s timeout) has been applied and verified. The orchestrator now correctly reports pytest status in agreement with direct pytest execution.

A secondary discrepancy (verify_tests.py skip counting) is a static analysis design limitation, not a bug. The orchestrator's runtime pytest execution provides authoritative skip counts.

**Classification: Resolved.** No further action required.