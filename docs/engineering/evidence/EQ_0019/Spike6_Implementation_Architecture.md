# Spike 6 — Implementation Architecture

## EQ-0019 BOQ Semantic Intelligence Increment 1

### Purpose
Determine production module location, public API, internal responsibilities, testing strategy, and performance expectations. No runtime redesign.

### Authority
- BOQ Intelligence current location: `src/jarvis/parsers/costx/boq_intelligence.py`
- Current public API: `analyze_boq(rows, include_hierarchy, include_detection) -> BOQIntelligenceResult`
- Current module: ~476 lines, 20+ functions
- Architecture pattern: Pure functions over `list[BOQRow]`

---

## 1. Module Location

**Decision:** Extend existing `boq_intelligence.py` module.

**Rationale:**
1. All new capabilities operate over `list[BOQRow]` — same input as existing functions
2. All new capabilities produce evidence for `BOQIntelligenceResult` — same output contract
3. No architectural boundary justifies a new module
4. Reuse analysis (per Increment 2 design pattern) confirms: existing module can accommodate

**Module Location:**
```
src/jarvis/parsers/costx/boq_intelligence.py  (extend existing)
```

**Discarded Option:** New module `boq_semantic.py`
- Rationale for discarding: Would create unnecessary module boundary, increase import complexity, and duplicate existing patterns. Rule of Three does not apply — this is extension, not new architecture.

---

## 2. Public API Changes

### Current API
```python
def analyze_boq(
    rows: list[BOQRow],
    *,
    include_hierarchy: bool = False,
    include_detection: bool = False,
) -> BOQIntelligenceResult:
```

### Proposed API
```python
def analyze_boq(
    rows: list[BOQRow],
    *,
    include_hierarchy: bool = False,
    include_detection: bool = False,
    include_semantic: bool = False,  # NEW — enables Increment 4 semantic capabilities
) -> BOQIntelligenceResult:
```

**Backward Compatibility:** The new `include_semantic` parameter has default `False`, preserving all existing behavior. Existing callers are unaffected.

---

## 3. Internal Responsibility Changes

### New Internal Functions

| Function | Responsibility | Input | Output | Capability |
|---|---|---|---|---|
| `_extract_vocabulary(rows, max_terms=50)` | Count term frequencies in item descriptions | `list[BOQRow]` | `dict[str, int]` | SEM-PROD-01 |
| `_categorize_head1(rows)` | Classify Head1 as admin or trade | `list[BOQRow]` | `dict[str, list]` | SEM-PROD-02 |
| `_detect_administrative_patterns(hierarchy)` | Detect boilerplate patterns in hierarchy | `tuple[BOQHeaderNode]` | `dict[str, list]` | SEM-PROD-04 |
| `_enumerate_sections(rows)` | Enumerate sections with code + name | `list[BOQRow]` | `tuple[dict]` | SEM-PROD-05 |
| `_compute_uom_distribution(rows)` | Compute UOM frequency distribution | `list[BOQRow]` | `dict[str, int]` | SEM-PROD-06 |
| `_compute_header_distribution(rows)` | Count Head1-Head4 frequency | `list[BOQRow]` | `dict[str, int]` | SEM-PROD-07 |
| `_detect_header_quantity_violations(rows)` | Check header rows for non-NULL quantities | `list[BOQRow]` | `tuple[dict]` | SEM-PROD-09 |
| `_detect_admin_template_matches(rows)` | Detect administrative sub-template sequences | `list[BOQRow]` | `dict[str, list]` | SEM-PROD-12 |

### Extended Internal Functions

| Function | Change | Capability |
|---|---|---|
| `_compute_section_stats(rows)` | Add `section_code` and `section_name` keys to output dict | SEM-PROD-05 (partial) |
| `_count_row_types(rows)` | Add `Head1`, `Head2`, `Head3`, `Head4` keys to output dict | SEM-PROD-07 (partial) |

### BOQIntelligenceResult Changes

**New optional fields:**

```python
@dataclass(frozen=True)
class BOQIntelligenceResult:
    # Existing fields (unchanged)
    row_classification: dict[str, int]
    section_statistics: dict[str, dict[str, int]]
    boq_statistics: dict[str, int | float]
    known_anomalies: list[dict[str, int | str | float]]
    hierarchy: tuple[BOQHeaderNode, ...] | None = None
    hierarchy_statistics: dict[str, int | float] | None = None
    detected_level_skips: tuple[dict[str, int], ...] | None = None
    zero_quantity_items: tuple[dict[str, int | str | float | None], ...] | None = None
    structural_containment_findings: tuple[dict[str, int], ...] | None = None
    completeness_findings: tuple[dict[str, int | str], ...] | None = None
    
    # NEW — Increment 4 semantic fields (all optional, None when include_semantic=False)
    vocabulary: dict[str, int] | None = None  # SEM-PROD-01
    head1_categorization: dict[str, list[dict]] | None = None  # SEM-PROD-02
    administrative_patterns: dict[str, list[dict]] | None = None  # SEM-PROD-04
    section_enumeration: tuple[dict[str, str | int], ...] | None = None  # SEM-PROD-05
    uom_distribution: dict[str, int] | None = None  # SEM-PROD-06
    uom_percentages: dict[str, float] | None = None  # SEM-PROD-06
    header_distribution: dict[str, int] | None = None  # SEM-PROD-07
    header_quantity_violations: tuple[dict[str, int | str | float | None], ...] | None = None  # SEM-PROD-09
    admin_template_matches: dict[str, list[dict]] | None = None  # SEM-PROD-12
```

**Total fields:** 10 existing + 9 new = 19 fields (all existing fields unchanged)

---

## 4. Testing Strategy

### Test Location

```
tests/test_boq_intelligence.py  (extend existing test file)
```

### New Test Cases

| Test | Capability | Evidence Reference | Type |
|---|---|---|---|
| Test vocabulary extraction counts | SEM-PROD-01 | EQ-0018 §6 | Determinism |
| Test vocabulary empty input | SEM-PROD-01 | — | Edge case |
| Test vocabulary max_terms limit | SEM-PROD-01 | Spike 3 Rule | Determinism |
| Test Head1 categorization (admin) | SEM-PROD-02 | Spike 3 Rule | Pattern matching |
| Test Head1 categorization (trade) | SEM-PROD-02 | Spike 3 Rule | Pattern matching |
| Test admin pattern detection present | SEM-PROD-04 | EQ-0018 §7 | Pattern matching |
| Test admin pattern detection missing | SEM-PROD-04 | Spike 3 Rule | Edge case |
| Test section enumeration ordering | SEM-PROD-05 | EQ-0018 §3 | Determinism |
| Test section enumeration fields | SEM-PROD-05 | Spike 3 Rule | Completeness |
| Test UOM distribution counts | SEM-PROD-06 | EQ-0018 §5 | Determinism |
| Test UOM distribution percentages | SEM-PROD-06 | Spike 3 Rule | Percentage sum |
| Test header distribution counts | SEM-PROD-07 | EQ-0018 §4 | Determinism |
| Test header distribution consistency | SEM-PROD-07 | Spike 3 Rule | Consistency |
| Test header quantity invariant passes | SEM-PROD-09 | EQ-0018 §4, §10 | Invariant |
| Test header quantity invariant fails | SEM-PROD-09 | — | Edge case |
| Test admin template detection | SEM-PROD-12 | EQ-0018 §7 | Pattern matching |
| Test template sequence order | SEM-PROD-12 | Spike 3 Rule | Sequence matching |
| Test include_semantic flag | ALL | Spike 4 Contract | Backward compat |
| Test production fixture | ALL | Full BOQ | Integration |

### Test Fixtures

- Current fixture: `tests/fixtures/costx/full_boq.xlsx` (primary)
- All tests should pass with production data
- No new fixture required for Increment 4 (existing fixture sufficient)

---

## 5. Performance Expectations

| Capability | Complexity | Expected Cost (3606 items) |
|---|---|---|
| SEM-PROD-01 (Vocabulary) | O(n × avg_words) | ~5ms — word splitting over 3606 descriptions |
| SEM-PROD-02 (Head1 Categorization) | O(h) where h = Head1 count | <1ms — 294 Head1 entries |
| SEM-PROD-04 (Admin Patterns) | O(s × h_avg) where s = sections | <1ms — hierarchy traversal |
| SEM-PROD-05 (Section Enumeration) | O(s) where s = sections | <1ms — 61 sections |
| SEM-PROD-06 (UOM Distribution) | O(i) where i = items | <1ms — 3606 UOM values |
| SEM-PROD-07 (Header Distribution) | O(h) where h = headers | <1ms — 2037 headers |
| SEM-PROD-09 (Items Always Quantify) | O(h_h) where h_h = Head rows | <1ms — 2037 headers |
| SEM-PROD-12 (Template Recognition) | O(s × h1_avg) | <1ms — pattern match |

**Total incremental cost:** <10ms for full BOQ with 3606 items, 2037 headers, 26 sections

**Performance invariant:** Increment 4 does NOT significantly increase `analyze_boq()` runtime.

---

## 6. Architecture Verification

| Principle | Verification |
|---|---|
| Pure functions | ✅ All 8 new functions are pure (identical inputs → identical outputs) |
| No side effects | ✅ All functions return new data, never modify inputs |
| No architecture changes | ✅ Same module, same pattern, same output contract |
| No parser changes | ✅ Operates over existing `BOQRow` only |
| No runtime changes | ✅ No new runtime modules, no new entry points |
| No kernel changes | ✅ BOQ Intelligence is not part of Kernel |
| Evidence/Assessment boundary | ✅ All capabilities produce evidence only |
| Consumer independence | ✅ All capabilities opt-in via `include_semantic` flag |
| YAGNI | ✅ Only capabilities with confirmed consumer value included |
| Determinism | ✅ All capabilities produce deterministic output |

---

## 7. Implementation Sequence

1. Extend `BOQIntelligenceResult` dataclass with new fields
2. Implement `_enumerate_sections()` (SEM-PROD-05) — simplest, most foundational
3. Implement `_compute_header_distribution()` (SEM-PROD-07) — extension of existing `_count_row_types()`
4. Implement `_categorize_head1()` (SEM-PROD-02) — pattern matching
5. Implement `_detect_administrative_patterns()` (SEM-PROD-04) — hierarchy traversal
6. Implement `_detect_admin_template_matches()` (SEM-PROD-12) — sequence matching
7. Implement `_extract_vocabulary()` (SEM-PROD-01) — word frequency
8. Implement `_compute_uom_distribution()` (SEM-PROD-06) — UOM frequency
9. Implement `_detect_header_quantity_violations()` (SEM-PROD-09) — invariant check
10. Add `include_semantic` parameter to `analyze_boq()`
11. Wire all new functions into `analyze_boq()` main logic
12. Write all new tests
13. Run full test suite
14. Verify against production fixture
15. Document new capabilities

---

## Document Control

**Version:** 1.0
**Spike:** 6 of 7
**EQ:** EQ-0019
**Status:** Complete
**Last Updated:** 2026-07-25
**Owner:** Project Owner