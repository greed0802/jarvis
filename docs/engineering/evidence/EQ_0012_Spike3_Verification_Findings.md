# EQ-0012 Spike 3 — Verification Findings

**Date:** 2026-07-15  
**Status:** Verification Complete  
**Investigation:** EQ-0012 Spike 3 Contract Invariants Verification Audit  
**Auditor:** Automated verification against production implementation  
**Source of Truth:** `src/jarvis/parsers/costx/boq_intelligence.py` (lines 48-64)

---

## Executive Summary

**Verification Result:** All 10 fields have documentation drift (Class A errors).

**Root Cause:** Spike 3 documentation was created from Spike 1 inventory, which used inferred/simplified types rather than exact production types.

**Disposition:** Revise Spike 3 to match production implementation exactly.

**Zero Class B or Class C issues:** No implementation errors, no ambiguities.

---

## Verification Matrix

| Field | Production Type | Spike 3 Type | Status | Classification |
|-------|----------------|--------------|--------|----------------|
| row_classification | `dict[str, int]` | `Dict[int, RowType]` | DOCUMENTATION_DRIFT | Class A |
| section_statistics | `dict[str, dict[str, int]]` | `Dict[str, Any]` | DOCUMENTATION_DRIFT | Class A |
| boq_statistics | `dict[str, int \| float]` | `Dict[str, Any]` | DOCUMENTATION_DRIFT | Class A |
| known_anomalies | `list[dict[str, int \| str \| float]]` | `List[str]` | DOCUMENTATION_DRIFT | Class A |
| hierarchy | `tuple[BOQHeaderNode, ...] \| None` | `Optional[BOQHierarchy]` | DOCUMENTATION_DRIFT | Class A |
| hierarchy_statistics | `dict[str, int \| float] \| None` | `Optional[Dict[str, Any]]` | DOCUMENTATION_DRIFT | Class A |
| detected_level_skips | `tuple[dict[str, int], ...] \| None` | `Optional[List[Dict[str, Any]]]` | DOCUMENTATION_DRIFT | Class A |
| zero_quantity_items | `tuple[dict[str, int \| str \| float \| None], ...] \| None` | `Optional[List[Dict[str, Any]]]` | DOCUMENTATION_DRIFT | Class A |
| structural_containment_findings | `tuple[dict[str, int], ...] \| None` | `Optional[List[Dict[str, Any]]]` | DOCUMENTATION_DRIFT | Class A |
| completeness_findings | `tuple[dict[str, int \| str], ...] \| None` | `Optional[List[Dict[str, Any]]]` | DOCUMENTATION_DRIFT | Class A |

---

## Detailed Findings

### Issue 1: row_classification

**Production Type:** `dict[str, int]` (line 55)  
**Spike 3 Type:** `Dict[int, RowType]`

**Evidence:**
- `BOQIntelligenceResult.row_classification` defined at line 55
- `_count_row_types()` function (lines 120-126) returns `dict[str, int]`
- Keys are row type strings: "Head", "Note", "Section", "Item", "Other"
- Values are integer counts

**RowType enum does not exist in production.**

**Classification:** Class A (Documentation Error)

**Correction Required:** Change documented type from `Dict[int, RowType]` to `dict[str, int]`

**Implications for Invariants:**
- SI-RC-02: Update type verification
- SI-RC-04: Update shape description (keys are strings, not ints)

---

### Issue 2: section_statistics

**Production Type:** `dict[str, dict[str, int]]` (line 56)  
**Spike 3 Type:** `Dict[str, Any]`

**Evidence:**
- `BOQIntelligenceResult.section_statistics` defined at line 56
- `_compute_section_stats()` function (lines 147-161) returns `dict[str, dict[str, int]]`
- Outer dict: section name → section stats
- Inner dict: "negative_qty" and "positive_qty" → counts

**Spike 3 documents `Any` which is less precise than actual production type.**

**Classification:** Class A (Documentation Error)

**Correction Required:** Change documented type from `Dict[str, Any]` to `dict[str, dict[str, int]]`

**Implications for Invariants:**
- SI-SS-02: Update type verification to exact nested dict structure
- SI-SS-03: Document actual keys ("negative_qty", "positive_qty")

---

### Issue 3: boq_statistics

**Production Type:** `dict[str, int | float]` (line 57)  
**Spike 3 Type:** `Dict[str, Any]`

**Evidence:**
- `BOQIntelligenceResult.boq_statistics` defined at line 57
- `_compute_boq_stats()` function (lines 129-144) returns `dict[str, int | float]`
- Keys: "total_rows", "code_rows", "description_rows", "quantity_rows", "uom_rows", "section_rows"
- Values: integer or float

**Spike 3 documents `Any` which is less precise than actual production type.**

**Classification:** Class A (Documentation Error)

**Correction Required:** Change documented type from `Dict[str, Any]` to `dict[str, int | float]`

**Implications for Invariants:**
- SI-BS-02: Update type verification to union type
- SI-BS-03: Document actual keys from lines 137-143

---

### Issue 4: known_anomalies

**Production Type:** `list[dict[str, int | str | float]]` (line 58)  
**Spike 3 Type:** `List[str]`

**Evidence:**
- `BOQIntelligenceResult.known_anomalies` defined at line 58
- `_detect_anomalies()` function (lines 164-178) returns `list[dict[str, int | str | float]]`
- Each anomaly is a dict with keys: "row_number", "code", "quantity", "section"

**Spike 3 documents `List[str]` but production returns list of dicts.**

**Classification:** Class A (Documentation Error)

**Correction Required:** Change documented type from `List[str]` to `list[dict[str, int | str | float]]`

**Implications for Invariants:**
- SI-KA-02: Complete rewrite of type verification
- All semantic invariants remain valid but need updated verification methods

---

### Issue 5: hierarchy

**Production Type:** `tuple[BOQHeaderNode, ...] | None` (line 59)  
**Spike 3 Type:** `Optional[BOQHierarchy]`

**Evidence:**
- `BOQIntelligenceResult.hierarchy` defined at line 59
- `_reconstruct_hierarchy()` function (lines 198-260) returns `tuple[BOQHeaderNode, ...]`
- Returns tuple of root header nodes, not a single BOQHierarchy object

**BOQHierarchy type does not exist in production.**

**Classification:** Class A (Documentation Error)

**Correction Required:** Change documented type from `Optional[BOQHierarchy]` to `tuple[BOQHeaderNode, ...] | None`

**Implications for Invariants:**
- SI-H-02: Update type verification to tuple of BOQHeaderNode
- All invariants reference correct type now

---

### Issue 6: hierarchy_statistics

**Production Type:** `dict[str, int | float] | None` (line 60)  
**Spike 3 Type:** `Optional[Dict[str, Any]]`

**Evidence:**
- `BOQIntelligenceResult.hierarchy_statistics` defined at line 60
- `_compute_hierarchy_statistics()` function (lines 279-330) returns `dict[str, int | float]`
- Keys: "total_headers", "root_headers", "depth_distribution", "items_per_header_by_uom"

**Spike 3 documents `Any` which is less precise than actual production type.**

**Classification:** Class A (Documentation Error)

**Correction Required:** Change documented type from `Optional[Dict[str, Any]]` to `dict[str, int | float] | None`

**Implications for Invariants:**
- SI-HS-02: Update type verification to union type
- SI-HS-03: Keys already correctly documented

---

### Issues 7-10: Detection Fields (tuple vs List)

All four detection fields have the same pattern:

**Production:** Uses `tuple[dict[...], ...] | None` (immutable)  
**Spike 3:** Documents `Optional[List[Dict[str, Any]]]` (mutable)

**Evidence:**
- `detected_level_skips` line 61: `tuple[dict[str, int], ...] | None`
- `zero_quantity_items` line 62: `tuple[dict[str, int | str | float | None], ...] | None`
- `structural_containment_findings` line 63: `tuple[dict[str, int], ...] | None`
- `completeness_findings` line 64: `tuple[dict[str, int | str], ...] | None`

**Semantic difference:** Tuple (immutable) vs List (mutable)

**Classification:** Class A (Documentation Error)

**Correction Required:** 
- Change all from `Optional[List[...]]` to `tuple[...] | None`
- Update inner dict types to match specific production types (not `Any`)

**Implications for Invariants:**
- SI-*-02: Update type verification to tuple
- Immutability invariant (SI-*-03) is now enforced by type system itself

---

## Additional Observations

### Observation 1: Spike 2 Tuple Policy Validation

Spike 2 versioning policy states:
> **Tuples:** Ordered, frozen structures. Future extensible evidence should prefer named structures (dataclasses, dictionaries). If a tuple must grow, explicit append-only semantics required in contract.

**Verification:** Production implementation is consistent with Spike 2 policy:
- All detection evidence uses tuples (immutable)
- `hierarchy` uses tuple of BOQHeaderNode (immutable dataclass)
- This supports the MAJOR version constraint for tuple extension

**Status:** Production implementation validates Spike 2 policy.

---

### Observation 2: Immutability Strategy

**Production implementation immutability:**
1. `BOQIntelligenceResult` is frozen dataclass (line 48: `frozen=True`)
2. Detection evidence uses tuples (immutable sequences)
3. `hierarchy` uses tuple of frozen BOQHeaderNode dataclasses

**Spike 3 documented immutability:**
- SI-*-03 invariants all state "Evidence is immutable after creation"
- Verification method: "Dataclass frozen=True"

**Status:** Immutability invariants are correct, but need to acknowledge tuple immutability.

---

### Observation 3: No Implementation Errors

**Critical finding:** Zero Class B issues.

**Interpretation:** Production implementation correctly follows frozen engineering evidence from:
- EQ-0007 (Increment 1)
- EQ-0010 (Increment 2)
- EQ-0011 (Increment 3)

**Implication:** Implementation is trustworthy. Documentation must conform to implementation.

---

## Required Corrections

### Correction Summary

All 10 fields require type corrections in Spike 3 documentation:

1. **row_classification:** `Dict[int, RowType]` → `dict[str, int]`
2. **section_statistics:** `Dict[str, Any]` → `dict[str, dict[str, int]]`
3. **boq_statistics:** `Dict[str, Any]` → `dict[str, int | float]`
4. **known_anomalies:** `List[str]` → `list[dict[str, int | str | float]]`
5. **hierarchy:** `Optional[BOQHierarchy]` → `tuple[BOQHeaderNode, ...] | None`
6. **hierarchy_statistics:** `Optional[Dict[str, Any]]` → `dict[str, int | float] | None`
7. **detected_level_skips:** `Optional[List[Dict[str, Any]]]` → `tuple[dict[str, int], ...] | None`
8. **zero_quantity_items:** `Optional[List[Dict[str, Any]]]` → `tuple[dict[str, int | str | float | None], ...] | None`
9. **structural_containment_findings:** `Optional[List[Dict[str, Any]]]` → `tuple[dict[str, int], ...] | None`
10. **completeness_findings:** `Optional[List[Dict[str, Any]]]` → `tuple[dict[str, int | str], ...] | None`

### Invariant Updates Required

**Structural Invariants:**
- Update all SI-*-02 (type invariants) with correct production types
- Update SI-RC-04 (shape) to reflect string keys not int keys
- Update SI-SS-03, SI-BS-03 (shape) with verified dictionary keys

**Semantic Invariants:**
- No changes required (semantic invariants remain valid)
- Verification methods remain valid

**Total Invariants Affected:** 34 structural invariants require type specification updates

---

## Root Cause Analysis

**Why did this occur?**

1. Spike 1 inventory used simplified/inferred types
2. Spike 3 tool read from Spike 1 rather than production code
3. No verification step was performed before Spike 3 completion

**Prevention:**
- Future spikes must verify against production before completion
- Evidence inventory must use exact production types
- Verification audit is now mandatory before freeze

---

## Recommendation

**Status:** Revise Spike 3

**Actions Required:**
1. Update all 10 field type specifications in Spike 3 Evidence Report
2. Update corresponding structural invariants (SI-*-02, SI-*-04)
3. Update Spike 3 tool to reflect production types
4. Re-run Spike 3 tool to regenerate JSON report
5. Re-run verification audit to confirm all fields match
6. Update Spike 1 inventory to use exact production types
7. Request freeze approval after corrections

**Timeline:** Single iteration (all corrections are deterministic)

**Gate 2 Impact:** None (corrections completed before Gate 2 submission)

---

## Verification Artifacts

**Tool:** `tools/eq0012_spike3_verification_audit.py`  
**Report:** `data/reports/eq0012_spike3_verification_audit.json`  
**Production Source:** `src/jarvis/parsers/costx/boq_intelligence.py` lines 48-64

---

**End of Verification Findings**