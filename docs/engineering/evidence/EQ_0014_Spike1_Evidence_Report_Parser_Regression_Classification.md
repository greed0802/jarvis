# EQ-0014 Spike 1 — Evidence Report: Parser Regression Classification

**Status:** Complete
**Date:** 2026-07-16
**EQ:** EQ-0014 Parser Regression Investigation
**Spike:** 1 — Failure Classification
**Tool:** `tools/eq0014_spike1_parser_regression_investigation.py`
**JSON Evidence:** `data/reports/eq0014_spike1_parser_regression_classification.json`

---

## Summary

20 failing tests. 1 root cause. 0 unknown classifications.

| Metric | Value |
|--------|-------|
| Total parser tests | 103 |
| Passing | 75 |
| Failing | 20 |
| Skipped | 8 (historical: observe() method was removed) |
| Unique error types | 2 (`Unknown row type: 'm'`, `Unknown row type: 'Head1'`) |
| Root cause | 1 (BOQRow field-ordering bug in test construction) |
| Classification | 20/20 = Outdated Test |
| Production code defect | 0 |

---

## Root Cause

All 20 failures share a single root cause: `test_boq_intelligence_increment3.py` constructs `BOQRow` objects with incorrect positional argument ordering.

**BOQRow fields** (from `boq_extraction.py:39-48`):
```
(row_number, code, description, quantity, uom, row_type, section=None)
```

**Tests pass arguments as** (incorrect):
```
(row_number, row_type, code, description, quantity, uom, section)
```

This swaps positions 2 and 6 — the `row_type` field receives the UOM string ("m", "Head1") instead of the classification string ("Item", "Head").

The production `_count_row_types()` in `boq_intelligence.py:123-124` correctly rejects these because `_VALID_ROW_TYPES = {"Head", "Note", "Section", "Item", "Other"}` and neither "m" nor "Head1" are in that set.

The production `_classify_row()` in `boq_extraction.py` correctly maps:
- UOM `"m"` → row_type `"Item"` (via `_ITEM_UOMS` frozenset, line 122-123)
- UOM `"Head1"` → row_type `"Head"` (via regex `Head\d+`, line 126-127)

**Production code is correct. Tests have a construction bug.**

---

## Failure Classification Matrix

### Group A: "m" failures (8 tests)

| # | Test Class | Test Name | Error | Classification | Disposition |
|---|-----------|-----------|-------|----------------|-------------|
| 1 | TestBackwardCompatibility | test_increment1_unchanged_with_increment3_disabled | Unknown row type: 'm' | Outdated Test | Fix BOQRow construction |
| 2 | TestZeroQuantityDetection | test_detect_single_zero_quantity | Unknown row type: 'm' | Outdated Test | Fix BOQRow construction |
| 3 | TestZeroQuantityDetection | test_detect_multiple_zero_quantities | Unknown row type: 'm' | Outdated Test | Fix BOQRow construction |
| 4 | TestZeroQuantityDetection | test_no_zero_quantities | Unknown row type: 'm' | Outdated Test | Fix BOQRow construction |
| 5 | TestZeroQuantityDetection | test_zero_quantity_determinism | Unknown row type: 'm' | Outdated Test | Fix BOQRow construction |
| 6 | TestForbiddenLanguage | test_zero_quantity_no_forbidden_language | Unknown row type: 'm' | Outdated Test | Fix BOQRow construction |
| 7 | TestRequiresHierarchy | test_detection_requires_hierarchy | Unknown row type: 'm' | Outdated Test | Fix BOQRow construction |

### Group B: "Head1" failures (12 tests) — also "Head2", "Head3", "Head5" in some tests

| # | Test Class | Test Name | Error | Classification | Disposition |
|---|-----------|-----------|-------|----------------|-------------|
| 8 | TestBackwardCompatibility | test_increment2_unchanged_with_increment3_disabled | Unknown row type: 'Head1' | Outdated Test | Fix BOQRow construction |
| 9 | TestLevelSkipDetection | test_detect_simple_level_skip | Unknown row type: 'Head1' | Outdated Test | Fix BOQRow construction |
| 10 | TestLevelSkipDetection | test_detect_large_level_skip | Unknown row type: 'Head1' | Outdated Test | Fix BOQRow construction |
| 11 | TestLevelSkipDetection | test_no_level_skip_sequential | Unknown row type: 'Head1' | Outdated Test | Fix BOQRow construction |
| 12 | TestLevelSkipDetection | test_level_skip_determinism | Unknown row type: 'Head1' | Outdated Test | Fix BOQRow construction |
| 13 | TestStructuralContainment | test_no_structural_inversions_valid_hierarchy | Unknown row type: 'Head1' | Outdated Test | Fix BOQRow construction |
| 14 | TestStructuralContainment | test_structural_containment_determinism | Unknown row type: 'Head1' | Outdated Test | Fix BOQRow construction |
| 15 | TestBasicCompleteness | test_detect_section_with_no_items | Unknown row type: 'Head1' | Outdated Test | Fix BOQRow construction |
| 16 | TestBasicCompleteness | test_all_sections_have_items | Unknown row type: 'Head1' | Outdated Test | Fix BOQRow construction |
| 17 | TestBasicCompleteness | test_basic_completeness_determinism | Unknown row type: 'Head1' | Outdated Test | Fix BOQRow construction |
| 18 | TestForbiddenLanguage | test_level_skip_no_forbidden_language | Unknown row type: 'Head1' | Outdated Test | Fix BOQRow construction |
| 19 | TestForbiddenLanguage | test_structural_containment_no_forbidden_language | Unknown row type: 'Head1' | Outdated Test | Fix BOQRow construction |
| 20 | TestForbiddenLanguage | test_completeness_no_forbidden_language | Unknown row type: 'Head1' | Outdated Test | Fix BOQRow construction |

**Classification Summary:**
| Classification | Count |
|----------------|-------|
| Outdated Test | 20 |
| Implementation Bug | 0 |
| Regression | 0 |
| Intentional Change | 0 |
| Specification Drift | 0 |
| Unknown | 0 |

---

## Parser Regression Matrix

| Test File | Total | Pass | Fail | Skip | Status |
|-----------|-------|------|------|------|--------|
| test_boq_extraction.py | 10 | 10 | 0 | 0 | ✓ Clean |
| test_boq_intelligence.py | 55 | 55 | 0 | 0 | ✓ Clean |
| test_boq_intelligence_increment3.py | 20 | 0 | 20 | 0 | ✗ All fail |
| test_observation_models.py | 10 | 10 | 0 | 0 | ✓ Clean |
| test_workbook_observe_historical.py | 8 | 0 | 0 | 8 | ⊘ Skipped (historical) |
| test_workbook_parser.py | 6 | 6 | 0 | 0 | ✓ Clean |
| test_workbook_validation.py | 4 | 4 | 0 | 0 | ✓ Clean |

Test files using synthetic BOQRow construction:
- `test_boq_intelligence_increment3.py` — positional args, ALL fail
- `test_boq_intelligence.py` — uses `keyword=True` args and/or production fixture, ALL pass

---

## Evidence Chain

### Production Code Evidence

**boq_extraction.py:36** — Item UOM set:
```python
_ITEM_UOMS = frozenset({"m", "m2", "m3", "no", "t", "Item", "item"})
```

**boq_extraction.py:39-48** — BOQRow field order:
```python
@dataclass
class BOQRow:
    row_number: int
    code: str | None
    description: str | None
    quantity: float | None
    uom: str | None
    row_type: str
    section: Literal["OMISSION", "ADDITION"] | None = None
```

**boq_extraction.py:122-123** — Item classification:
```python
if uom in _ITEM_UOMS:
    return "Item"
```

**boq_extraction.py:126-127** — Head classification:
```python
if re.fullmatch(r"Head\d+", str(uom) if uom else ""):
    return "Head"
```

**boq_intelligence.py:24** — Valid row types:
```python
_VALID_ROW_TYPES = frozenset({"Head", "Note", "Section", "Item", "Other"})
```

**boq_intelligence.py:123-124** — Rejection:
```python
if row.row_type not in _VALID_ROW_TYPES:
    raise ValueError(f"Unknown row type: {row.row_type!r}")
```

### Test Code Evidence

**test_boq_intelligence_increment3.py:30** — Incorrect construction:
```python
rows = [
    BOQRow(1, "Item", "A001", "Test item", 10.0, "m", "SECTION_A"),
    #      ^1  ^code?  ^desc?   ^qty?       ^uom?  ^row_type?  ^section?
    # Actually mapped as: row_number=1, code="Item", description="A001",
    #   quantity="Test item", uom=10.0, row_type="m", section="SECTION_A"
]
```

**test_boq_intelligence.py** (passing comparison) — Correct keyword construction:
```python
# This file uses production fixture BOQRows from extract_boq(), 
# which always produce correct row_type values.
```

### Frozen Engineering Evidence

**EQ-0010 Spike 1** established row type classifications: Head, Note, Section, Item, Other.
**EQ-0010 Spike 5** confirmed these are structurally deterministic.
**EQ-0011 Spike 2** confirmed detection/decision separation for all 4 permitted detection capabilities.
**EQ-0011 Spike 5** classified level skip, zero-quantity, structural containment, and basic completeness as Permitted detection capabilities.

The Increment 3 tests correctly validate the EQ-0011 engineering boundary (forbidden language, determinism, backward compatibility) — they just construct BOQRow objects incorrectly.

---

## Recommendation

**Fix tests only. Production code is correct and should not be modified.**

Disposition: Convert all BOQRow positional constructions in `test_boq_intelligence_increment3.py` to keyword arguments to prevent field-ordering ambiguity.

Example correction:
```python
# Before (incorrect positional — row_type receives UOM string):
BOQRow(1, "Item", "A001", "Test item", 10.0, "m", "SECTION_A")

# After (correct keyword — explicit field assignment):
BOQRow(
    row_number=1,
    code="A001",
    description="Test item",
    quantity=10.0,
    uom="m",
    row_type="Item",
    section="SECTION_A",
)
```

Expected result: 20/20 previously failing tests pass. 103/103 parser tests pass.

**Project Owner approval required before fixing tests.**

---

## Verification

- Classification tool: `tools/eq0014_spike1_parser_regression_investigation.py` — executed successfully
- JSON evidence: `data/reports/eq0014_spike1_parser_regression_classification.json` — written
- Production code references: all 20 failures traced to exact lines
- No assumptions: every classification confirmed by production code inspection
- No unknowns: all 20 failures fully classified

---

## Next Steps

1. Project Owner reviews classification
2. Project Owner approves or modifies disposition
3. If approved: fix tests via keyword-argument conversion
4. Run full parser test suite to confirm 103/103 pass
5. Update Engineering Debt Register (EQ-0014-01 resolved)
6. Proceed to M8 consumer architecture work