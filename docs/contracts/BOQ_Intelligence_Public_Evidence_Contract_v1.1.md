# BOQ Intelligence Public Evidence Contract v1.1

## Contract Header

**Version:** 1.1.0
**Status:** Frozen
**Date:** 2026-07-25
**Engineering Question:** EQ-0019 (PERMANENTLY FROZEN)
**Governance:** Implementation_Governance.md v1.0
**Principle:** Evidence Before Abstraction
**Source of Truth:** `src/jarvis/parsers/costx/boq_intelligence.py`

---

## Contract Overview

### Purpose

This document defines the Public Evidence Contract between the **BOQ Intelligence** (Evidence Producer) and all **consumers** of deterministic evidence extracted from CostX BOQ workbooks. It is the stable, versioned API that decouples evidence production from consumption.

### Scope

**In scope:**
- 10 evidence fields from Increments 1-3 (v1.0 — unchanged)
- 9 optional semantic evidence fields from Increment 4 (v1.1.0 — new)
- Structural and semantic invariants for each field
- Versioning policy governing contract evolution
- Consumer guarantees and deprecation lifecycle
- Public import paths and internal boundaries

**Out of scope:**
- Future evidence fields not yet implemented
- Validation rules (belongs to EQ-0013)
- CheckMate application design (belongs to EQ-0014)
- Evidence production implementation (already complete)

### Architecture Context

```
CostX Workbook
    ↓
[WorkbookParser validation → extract_boq()]
    ↓
BOQRow[]
    ↓
analyze_boq()  ← Evidence Producer
    ↓
BOQIntelligenceResult  ← Public Evidence Contract v1.1.0
    ↓
[All Consumers: CheckMate, Formatter, Builder, O&A, Reporting]
```

### First Principle

**The Evidence Contract is the stable API between Intelligence Producer and Intelligence Consumers. It must remain stable across versions while enabling producer evolution.**

### Evidence Admission Rule

Contract specifications may only include:
1. Evidence fields currently produced by BOQ Intelligence
2. Evidence semantics documented in frozen EQ evidence reports
3. Data structures directly observable in `BOQIntelligenceResult`

Speculative future evidence, implementation details, and internal algorithms are not permitted.

**Authority:** EQ-0010 (Deterministic BOQ Structural Intelligence), EQ-0011 (BOQ Semantic Intelligence Boundary), EQ-0019 (BOQ Semantic Intelligence Increment 1)

---

## Versioning Policy

### Version Identity

| Property | Value |
|----------|-------|
| Scheme | Semantic Versioning |
| Format | MAJOR.MINOR.PATCH |
| Initial Version | 1.0.0 (Frozen) |
| Current Version | 1.1.0 (Frozen) |
| Location | `docs/contracts/BOQ_Intelligence_Public_Evidence_Contract_v1.1.md` |

**Authority:** EQ-0012 Spike 2 (Contract Structure & Versioning Policy)

### Compatibility Rules

#### MAJOR (X.0.0) — Breaking changes requiring consumer attention:

| Change | Rationale |
|--------|-----------|
| Removing a required field | Breaks consuming code that expects the field |
| Changing type of a required field | Breaks consuming code that depends on the type |
| Renaming a required field | Breaks consuming code that references by name |
| Adding, removing, or changing a required field | Contract shape altered; strict consumers consider required fields mandatory |
| Changing invariants consumers depend on | Changes behavior consumers may rely on |
| Removing optional field without deprecation | Violates deprecation contract |
| Removing documented dictionary keys | Breaks consumers expecting keys |
| Changing tuple element order or semantics | Breaks consumers using positional access |
| Extending tuple contents | Tuples are ordered, frozen structures; consumers may destructure or index |

**Policy Notes:**
- **Required fields:** Contract evolution optimizes for strict consumers. Required fields alter contract shape regardless of runtime defaults.
- **Tuples:** Ordered, frozen structures. Future extensible evidence should prefer named structures (dataclasses, dictionaries).

#### MINOR (0.Y.0) — Non-breaking additions:

| Change | Rationale |
|--------|-----------|
| Adding new optional field | Consumer must opt-in to use |
| Adding new dict keys | Consumers iterating dynamically unaffected |
| Adding BOQHeaderNode fields (with defaults) | Backward compatible dataclass extension |
| Marking field as deprecated | Field still present and functional |

#### PATCH (0.0.Z) — Internal corrections:

| Change | Rationale |
|--------|-----------|
| Fixing documentation errors | No behavior change |
| Clarifying field semantics | No consumer impact |
| Adding invariant documentation | No consumer impact |
| Correcting type annotations | Matching actual behavior |
| Non-functional changes | No consumer impact |

**Key Insight:** Required vs. Optional distinction is critical. Changes to required fields are always MAJOR. Additions to optional fields can be MINOR. Removing optional fields without deprecation lifecycle is MAJOR.

### Consumer Guarantees (G-01 through G-16)

**Structural Guarantees (G-01 to G-03):**
- G-01: All documented fields will exist for the promised contract version
- G-02: Required fields will never be None
- G-03: Optional fields will never be removed without formal deprecation

**Type Guarantees (G-04 to G-07):**
- G-04: Field types as documented will not change within a MAJOR version
- G-05: Union types will not remove valid variants
- G-06: Documented dictionary keys will remain present
- G-07: Undocumented keys may appear (non-breaking addition)

**Semantic Guarantees (G-08 to G-10):**
- G-08: Documented field semantics will not change within a MAJOR version
- G-09: Evidence classification (Observation/Hierarchy/Detection) will not change
- G-10: EQ-0011 engineering boundary preserved in all evidence

**Determinism Guarantees (G-11 to G-13):**
- G-11: All evidence is deterministic — same input produces same output
- G-12: All evidence is immutable — consumers cannot modify evidence
- G-13: All evidence is traceable to frozen engineering evidence

**Access Guarantees (G-14 to G-16):**
- G-14: Consumers may depend on the Evidence Contract directly
- G-15: Consumers may import evidence types without importing internal implementation
- G-16: Consumers will not need access to internal BOQ Intelligence functions

**Authority:** EQ-0012 Spike 2 (Versioning Policy), frozen unchanged.

---

## Deprecation Lifecycle

### Three-Phase Model

```
Phase 1: Deprecation Announcement (MINOR version bump)
    ↓
Phase 2: Removal Notice (same MAJOR version)
    ↓
Phase 3: Removal (next MAJOR version bump)
```

**Phase 1 — Deprecation Announcement:**
- Trigger: Engineering Question determines field is obsolete
- Action: Field marked `@deprecated` in contract documentation
- Version: MINOR version bump (field still present and functional)
- Duration: One full MAJOR version cycle minimum

**Phase 2 — Removal Notice:**
- Trigger: Next MAJOR version planning
- Action: Explicit notification with target removal version
- Version: Still present in current MAJOR version
- Consumer impact: Field still present, consumers should migrate

**Phase 3 — Removal:**
- Trigger: MAJOR version bump
- Action: Field removed from Evidence Contract
- Version: MAJOR version bump
- Consumer impact: Breaking change — consumers must migrate

### Governance Gate (before any deprecation can begin)

1. Engineering Question must classify the field as obsolete
2. Project Owner must approve deprecation
3. All consumers must be notified
4. Migration path must be documented
5. Minimum deprecation period: one full MAJOR version

**Authority:** EQ-0012 Spike 2 (Contract Structure & Versioning Policy), frozen unchanged.

---

## Consumer Access Patterns

### Stable Import Paths (STABLE — consumers may depend on)

```python
from jarvis.parsers.costx.boq_intelligence import analyze_boq
from jarvis.parsers.costx.boq_intelligence import BOQIntelligenceResult
from jarvis.parsers.costx.boq_intelligence import BOQHeaderNode
from jarvis.parsers.costx.boq_extraction import BOQRow
from jarvis.parsers.costx.boq_extraction import extract_boq
```

**Stability Classification:** HIGH — All symbols are public (no underscore prefix), frozen dataclass or public function, protected by frozen engineering evidence.

### Unstable Imports (consumers must NOT import)

All symbols beginning with `_` (underscore) are internal implementation. They may change without notice and are not subject to versioning policy.

Specifically, consumers must NOT import:
```python
# Internal helpers - part of implementation, not contract:
from jarvis.parsers.costx.boq_intelligence import _count_row_types       # Internal
from jarvis.parsers.costx.boq_intelligence import _reconstruct_hierarchy  # Internal
from jarvis.parsers.costx.boq_intelligence import _freeze_node            # Internal
from jarvis.parsers.costx.boq_intelligence import _compute_hierarchy_statistics  # Internal
from jarvis.parsers.costx.boq_intelligence import _detect_level_skips     # Internal
from jarvis.parsers.costx.boq_intelligence import _detect_zero_quantities # Internal
from jarvis.parsers.costx.boq_intelligence import _detect_structural_containment  # Internal
from jarvis.parsers.costx.boq_intelligence import _detect_basic_completeness  # Internal
from jarvis.parsers.costx.boq_intelligence import _extract_vocabulary     # Internal
from jarvis.parsers.costx.boq_intelligence import _categorize_head1        # Internal
from jarvis.parsers.costx.boq_intelligence import _detect_administrative_patterns  # Internal
from jarvis.parsers.costx.boq_intelligence import _enumerate_sections     # Internal
from jarvis.parsers.costx.boq_intelligence import _compute_uom_distribution  # Internal
from jarvis.parsers.costx.boq_intelligence import _compute_header_distribution  # Internal
from jarvis.parsers.costx.boq_intelligence import _detect_header_quantity_violations  # Internal
from jarvis.parsers.costx.boq_intelligence import _detect_admin_template_matches  # Internal
from jarvis.parsers.costx.boq_extraction import _classify_row             # Internal
```

### Recommended Access Pattern

**Direct immutable dataclass + public function** (current production pattern). No facade, no protocol, no contracts package, no wrapper, no adapter, no runtime abstraction.

```python
from jarvis.parsers.costx.boq_extraction import BOQRow, extract_boq
from jarvis.parsers.costx.boq_intelligence import analyze_boq, BOQIntelligenceResult, BOQHeaderNode

# 1. Extract rows from a validated CostX workbook
rows: list[BOQRow] = extract_boq(workbook)

# 2. Run intelligence analysis
result: BOQIntelligenceResult = analyze_boq(
    rows,
    include_hierarchy=True,    # Enable Increment 2 hierarchy evidence
    include_detection=True,    # Enable Increment 3 detection evidence
    include_semantic=True,     # Enable Increment 4 semantic evidence (v1.1.0)
)

# 3. Access evidence directly from the frozen dataclass
for row_type, count in result.row_classification.items():
    ...

# 4. Access hierarchy (when include_hierarchy=True)
if result.hierarchy is not None:
    for root in result.hierarchy:
        print(f"Root header: {root.description} (depth {root.depth})")

# 5. Access detection evidence (when include_detection=True)
if result.detected_level_skips is not None:
    for skip in result.detected_level_skips:
        print(f"Level skip: {skip['skip_magnitude']} levels")

# 6. Access semantic evidence (when include_semantic=True) — v1.1.0
if result.vocabulary is not None:
    for term, count in result.vocabulary.items():
        ...
```

### Consumer Dependency Graph

```
Consumer
  └── jarvis.parsers.costx.boq_intelligence
        ├── analyze_boq (function)
        ├── BOQIntelligenceResult (frozen dataclass)
        └── BOQHeaderNode (frozen dataclass)

  └── jarvis.parsers.costx.boq_extraction
        ├── BOQRow (dataclass)
        └── extract_boq (function)
```

**Note:** `WorkbookParser` is a pre-extraction infrastructure concern (validation/loading). It is exported by `costx/__init__.py` but is not part of the evidence contract.

**Authority:** EQ-0012 Spike 4 (Consumer Access Patterns), frozen unchanged.

---

## Evidence Field Specifications

### Increment 1 — Observation Evidence

The 4 required fields from Increment 1 are unchanged from v1.0. See `BOQ_Intelligence_Public_Evidence_Contract_v1.0.md` for full specifications.

#### 1. row_classification
- **Type:** `dict[str, int]`
- **Required:** Yes
- **Classification:** Observation
- **v1.0 Status:** Unchanged

#### 2. section_statistics
- **Type:** `dict[str, dict[str, int]]`
- **Required:** Yes
- **Classification:** Observation
- **v1.0 Status:** Unchanged

#### 3. boq_statistics
- **Type:** `dict[str, int | float]`
- **Required:** Yes
- **Classification:** Observation
- **v1.0 Status:** Unchanged

#### 4. known_anomalies
- **Type:** `list[dict[str, int | str | float]]`
- **Required:** Yes
- **Classification:** Observation
- **v1.0 Status:** Unchanged

### Increment 2 — Hierarchy Evidence

The 2 optional fields from Increment 2 are unchanged from v1.0. See `BOQ_Intelligence_Public_Evidence_Contract_v1.0.md` for full specifications.

#### 5. hierarchy
- **Type:** `tuple[BOQHeaderNode, ...] | None`
- **Required:** No (controlled by `include_hierarchy` parameter)
- **Classification:** Hierarchy
- **v1.0 Status:** Unchanged

#### 6. hierarchy_statistics
- **Type:** `dict[str, int | float] | None`
- **Required:** No (controlled by `include_hierarchy` parameter)
- **Classification:** Hierarchy
- **v1.0 Status:** Unchanged

### Increment 3 — Detection Evidence

The 4 optional fields from Increment 3 are unchanged from v1.0. See `BOQ_Intelligence_Public_Evidence_Contract_v1.0.md` for full specifications.

#### 7. detected_level_skips
- **Type:** `tuple[dict[str, int], ...] | None`
- **Required:** No (controlled by `include_detection` parameter)
- **Classification:** Detection
- **v1.0 Status:** Unchanged

#### 8. zero_quantity_items
- **Type:** `tuple[dict[str, int | str | float | None], ...] | None`
- **Required:** No (controlled by `include_detection` parameter)
- **Classification:** Detection
- **v1.0 Status:** Unchanged

#### 9. structural_containment_findings
- **Type:** `tuple[dict[str, int], ...] | None`
- **Required:** No (controlled by `include_detection` parameter)
- **Classification:** Detection
- **v1.0 Status:** Unchanged

#### 10. completeness_findings
- **Type:** `tuple[dict[str, int | str], ...] | None`
- **Required:** No (controlled by `include_detection` parameter)
- **Classification:** Detection
- **v1.0 Status:** Unchanged

---

### Increment 4 — Semantic Evidence (v1.1.0 — New)

The following 9 optional semantic evidence fields are introduced in v1.1.0. All are controlled by the `include_semantic` parameter on `analyze_boq()`. All default to `None` when `include_semantic=False`.

---

#### 11. vocabulary

**Field Specification:**
- **Field Name:** `vocabulary`
- **Type:** `dict[str, int] | None`
- **Required:** No (controlled by `include_semantic` parameter)
- **Classification:** Evidence
- **Production Line:** `boq_intelligence.py` — `_extract_vocabulary()`
- **Increment:** 4
- **Capability:** SEM-PROD-01

**Semantics:**
- **Description:** Top-K engineering term frequency counts extracted from BOQ item descriptions.
- **Meaning:** Keys are engineering terms (lowercased); values are integer occurrence counts. Sorted descending by count. Maximum 50 terms by default.
- **Engineering Boundary:** Reports frequencies only — no semantic classification or assessment.

**Structural Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SI-VOC-01 | presence | Field may be None (controlled by include_semantic parameter) | Assert field is None or isinstance(field, dict) | MINOR |
| SI-VOC-02 | type | When present, must be dict[str, int] | If not None, assert isinstance(field, dict) and all(isinstance(k, str) and isinstance(v, int) for k, v in field.items()) | MAJOR |
| SI-VOC-03 | immutability | Evidence is immutable after creation | Dataclass frozen=True | MAJOR |

**Semantic Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SE-VOC-01 | determinism | Same input → same vocabulary dict | Run analysis twice, compare results | MAJOR |
| SE-VOC-02 | ordering | Results sorted descending by count | Assert values are non-increasing | MAJOR |
| SE-VOC-03 | boundary | Reports frequencies only — no semantic classification | Check keys against EQ-0011 forbidden terms | MAJOR |

**Cross-field Dependencies:** None

**Traceability:**
- **Engineering Evidence:** EQ-0019 Spike 3 (Deterministic Rule Definition)
- **Production Location:** `boq_intelligence.py` — `_extract_vocabulary()`
- **Previous EQ:** EQ-0019 (Increment 4)

---

#### 12. head1_categorization

**Field Specification:**
- **Field Name:** `head1_categorization`
- **Type:** `dict[str, list[dict]] | None`
- **Required:** No (controlled by `include_semantic` parameter)
- **Classification:** Evidence
- **Production Line:** `boq_intelligence.py` — `_categorize_head1()`
- **Increment:** 4
- **Capability:** SEM-PROD-02

**Semantics:**
- **Description:** Categorization of each Head1 row as Administrative or Trade-Specific using a frozen pattern list.
- **Meaning:** Outer dict keys: `'Administrative'`, `'Trade-Specific'` → list of dicts. Each dict contains: `'row_number'` (int), `'description'` (str). Every Head1 row is classified into exactly one category.
- **Engineering Boundary:** Reports pattern match results — does not assess correctness or completeness.

**Structural Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SI-H1C-01 | presence | Field may be None (controlled by include_semantic parameter) | Assert field is None or isinstance(field, dict) | MINOR |
| SI-H1C-02 | type | When present, must be dict[str, list[dict]] | If not None, assert isinstance(field, dict) and all(isinstance(v, list) for v in field.values()) | MAJOR |
| SI-H1C-03 | shape | Outer dict keys: 'Administrative', 'Trade-Specific' → list of dicts | Assert set(field.keys()) == {'Administrative', 'Trade-Specific'} | MAJOR |
| SI-H1C-04 | immutability | Evidence is immutable after creation | Dataclass frozen=True | MAJOR |

**Semantic Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SE-H1C-01 | determinism | Same rows → same categorization | Run analysis twice, compare results | MAJOR |
| SE-H1C-02 | completeness | Every Head1 classified | Assert total entries equals Head1 count | MAJOR |
| SE-H1C-03 | frozen_patterns | Pattern list is frozenset | Verify _ADMINISTRATIVE_PATTERNS is frozenset | MAJOR |

**Cross-field Dependencies:** None

**Traceability:**
- **Engineering Evidence:** EQ-0019 Spike 3 (Deterministic Rule Definition)
- **Production Location:** `boq_intelligence.py` — `_categorize_head1()`
- **Previous EQ:** EQ-0019 (Increment 4)

---

#### 13. administrative_patterns

**Field Specification:**
- **Field Name:** `administrative_patterns`
- **Type:** `dict[str, list[dict]] | None`
- **Required:** No (controlled by `include_semantic` parameter; requires hierarchy)
- **Classification:** Evidence
- **Production Line:** `boq_intelligence.py` — `_detect_administrative_patterns()`
- **Increment:** 4
- **Capability:** SEM-PROD-04

**Semantics:**
- **Description:** Detection of administrative boilerplate patterns within sections using hierarchy.
- **Meaning:** Outer dict: section name → list of pattern dicts. Each pattern dict contains: `'pattern_name'` (str), `'matched_text'` (str), `'row_number'` (int). Returns `None` when hierarchy unavailable.
- **Engineering Boundary:** Reports what IS present — does not assess compliance or completeness.

**Structural Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SI-ADM-01 | presence | Field may be None (requires hierarchy) | Assert field is None or isinstance(field, dict) | MINOR |
| SI-ADM-02 | type | When present, must be dict[str, list[dict]] | If not None, assert isinstance(field, dict) and all(isinstance(v, list) for v in field.values()) | MAJOR |
| SI-ADM-03 | immutability | Evidence is immutable after creation | Dataclass frozen=True | MAJOR |
| SI-ADM-04 | frozen_templates | Pattern list is frozen | Verify _ADMINISTRATIVE_PATTERNS is frozenset | MAJOR |

**Semantic Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SE-ADM-01 | determinism | Same hierarchy → same patterns | Run analysis twice, compare results | MAJOR |
| SE-ADM-02 | observation_only | Reports what IS present | Check values against EQ-0011 forbidden terms | MAJOR |

**Cross-field Dependencies:** hierarchy (requires `include_hierarchy=True`)

**Traceability:**
- **Engineering Evidence:** EQ-0019 Spike 3 (Deterministic Rule Definition)
- **Production Location:** `boq_intelligence.py` — `_detect_administrative_patterns()`
- **Previous EQ:** EQ-0019 (Increment 4)

---

#### 14. section_enumeration

**Field Specification:**
- **Field Name:** `section_enumeration`
- **Type:** `tuple[dict[str, str | int], ...] | None`
- **Required:** No (controlled by `include_semantic` parameter)
- **Classification:** Evidence
- **Production Line:** `boq_intelligence.py` — `_enumerate_sections()`
- **Increment:** 4
- **Capability:** SEM-PROD-05

**Semantics:**
- **Description:** Enumeration of all sections with codes and names, preserving ordinal position.
- **Meaning:** Each dict contains: `'code'` (str), `'name'` (str), `'row_number'` (int). Sections ordered by worksheet position.
- **Engineering Boundary:** Reports observable section codes and names — does not assess coverage or completeness.

**Structural Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SI-SCE-01 | presence | Field may be None (controlled by include_semantic parameter) | Assert field is None or isinstance(field, tuple) | MINOR |
| SI-SCE-02 | type | When present, must be tuple[dict[str, str | int], ...] | If not None, assert isinstance(field, tuple) and all(isinstance(x, dict) for x in field) | MAJOR |
| SI-SCE-03 | shape | Each dict contains keys: 'code' (str), 'name' (str), 'row_number' (int) | For each dict, assert set(dict.keys()) == {'code', 'name', 'row_number'} | MAJOR |
| SI-SCE-04 | immutability | Evidence is immutable after creation (tuple immutability) | Dataclass frozen=True, tuple immutable | MAJOR |

**Semantic Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SE-SCE-01 | determinism | Same rows → same enumeration | Run analysis twice, compare results | MAJOR |
| SE-SCE-02 | ordering | Sections in worksheet order | Assert row_number values are non-decreasing | MAJOR |
| SE-SCE-03 | completeness | All section rows included | Assert count matches expected section count | MAJOR |

**Cross-field Dependencies:** None

**Traceability:**
- **Engineering Evidence:** EQ-0019 Spike 3 (Deterministic Rule Definition)
- **Production Location:** `boq_intelligence.py` — `_enumerate_sections()`
- **Previous EQ:** EQ-0019 (Increment 4)

---

#### 15. uom_distribution

**Field Specification:**
- **Field Name:** `uom_distribution`
- **Type:** `dict[str, int] | None`
- **Required:** No (controlled by `include_semantic` parameter)
- **Classification:** Evidence
- **Production Line:** `boq_intelligence.py` — `_compute_uom_distribution()`
- **Increment:** 4
- **Capability:** SEM-PROD-06

**Semantics:**
- **Description:** UOM frequency counts across all rows with UOM values.
- **Meaning:** Keys are UOM strings (e.g., `'m2'`, `'no'`, `'m3'`); values are integer occurrence counts.
- **Engineering Boundary:** Reports frequency counts only — does not assess appropriateness.

**Structural Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SI-UOM-01 | presence | Field may be None (controlled by include_semantic parameter) | Assert field is None or isinstance(field, dict) | MINOR |
| SI-UOM-02 | type | When present, must be dict[str, int] | If not None, assert isinstance(field, dict) and all(isinstance(k, str) and isinstance(v, int) for k, v in field.items()) | MAJOR |
| SI-UOM-03 | immutability | Evidence is immutable after creation | Dataclass frozen=True | MAJOR |

**Semantic Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SE-UOM-01 | determinism | Same rows → same distribution | Run analysis twice, compare results | MAJOR |
| SE-UOM-02 | type | Counts are int, percentages are float | Assert all values are int | MAJOR |

**Cross-field Dependencies:** None

**Traceability:**
- **Engineering Evidence:** EQ-0019 Spike 3 (Deterministic Rule Definition)
- **Production Location:** `boq_intelligence.py` — `_compute_uom_distribution()`
- **Previous EQ:** EQ-0019 (Increment 4)

---

#### 16. uom_percentages

**Field Specification:**
- **Field Name:** `uom_percentages`
- **Type:** `dict[str, float] | None`
- **Required:** No (controlled by `include_semantic` parameter)
- **Classification:** Evidence
- **Production Line:** `boq_intelligence.py` — `_compute_uom_distribution()`
- **Increment:** 4
- **Capability:** SEM-PROD-06

**Semantics:**
- **Description:** UOM percentage distribution (percentage of total UOM rows).
- **Meaning:** Keys are UOM strings; values are float percentages (0.0–100.0, rounded to 1 decimal). Sum is within floating-point tolerance of 100.0.
- **Engineering Boundary:** Reports percentage distribution only — does not assess appropriateness.

**Structural Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SI-UOMP-01 | presence | Field may be None (controlled by include_semantic parameter) | Assert field is None or isinstance(field, dict) | MINOR |
| SI-UOMP-02 | type | When present, must be dict[str, float] | If not None, assert isinstance(field, dict) and all(isinstance(k, str) and isinstance(v, float) for k, v in field.items()) | MAJOR |
| SI-UOMP-03 | immutability | Evidence is immutable after creation | Dataclass frozen=True | MAJOR |

**Semantic Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SE-UOMP-01 | determinism | Same rows → same percentages | Run analysis twice, compare results | MAJOR |
| SE-UOMP-02 | percentage_sum | Sum ≈ 100.0 within tolerance | Assert abs(sum(values) - 100.0) < 0.2 | MAJOR |

**Cross-field Dependencies:** uom_distribution (same function produces both)

**Traceability:**
- **Engineering Evidence:** EQ-0019 Spike 3 (Deterministic Rule Definition)
- **Production Location:** `boq_intelligence.py` — `_compute_uom_distribution()`
- **Previous EQ:** EQ-0019 (Increment 4)

---

#### 17. header_distribution

**Field Specification:**
- **Field Name:** `header_distribution`
- **Type:** `dict[str, int] | None`
- **Required:** No (controlled by `include_semantic` parameter)
- **Classification:** Evidence
- **Production Line:** `boq_intelligence.py` — `_compute_header_distribution()`
- **Increment:** 4
- **Capability:** SEM-PROD-07

**Semantics:**
- **Description:** Count of rows at each header level (Head1–Head4).
- **Meaning:** Keys: `'Head1'`, `'Head2'`, `'Head3'`, `'Head4'` → integer counts. Head5 rows are excluded per Spike 3 specification.
- **Engineering Boundary:** Reports count distribution only — does not assess hierarchy quality.

**Structural Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SI-HD-01 | presence | Field may be None (controlled by include_semantic parameter) | Assert field is None or isinstance(field, dict) | MINOR |
| SI-HD-02 | type | When present, must be dict[str, int] | If not None, assert isinstance(field, dict) and all(isinstance(k, str) and isinstance(v, int) for k, v in field.items()) | MAJOR |
| SI-HD-03 | shape | Keys: 'Head1', 'Head2', 'Head3', 'Head4' → int values | Assert set(field.keys()) == {'Head1', 'Head2', 'Head3', 'Head4'} | MAJOR |
| SI-HD-04 | immutability | Evidence is immutable after creation | Dataclass frozen=True | MAJOR |

**Semantic Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SE-HD-01 | determinism | Same rows → same distribution | Run analysis twice, compare results | MAJOR |
| SE-HD-02 | completeness | Head1–4 counted (Head5 excluded) | Assert keys match specification | MAJOR |

**Cross-field Dependencies:** None

**Traceability:**
- **Engineering Evidence:** EQ-0019 Spike 3 (Deterministic Rule Definition)
- **Production Location:** `boq_intelligence.py` — `_compute_header_distribution()`
- **Previous EQ:** EQ-0019 (Increment 4)

---

#### 18. header_quantity_violations

**Field Specification:**
- **Field Name:** `header_quantity_violations`
- **Type:** `tuple[dict[str, int | str | float | None], ...] | None`
- **Required:** No (controlled by `include_semantic` parameter)
- **Classification:** Evidence
- **Production Line:** `boq_intelligence.py` — `_detect_header_quantity_violations()`
- **Increment:** 4
- **Capability:** SEM-PROD-09

**Semantics:**
- **Description:** Detection of header rows that carry non-NULL quantities (invariant violation).
- **Meaning:** Each dict contains: `'row_number'` (int), `'row_type'` (str), `'quantity'` (float). Empty tuple when invariant holds.
- **Engineering Boundary:** Reports observations — never assesses acceptability or severity.

**Structural Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SI-IAQ-01 | presence | Field may be None (controlled by include_semantic parameter) | Assert field is None or isinstance(field, tuple) | MINOR |
| SI-IAQ-02 | type | When present, must be tuple[dict, ...] | If not None, assert isinstance(field, tuple) and all(isinstance(x, dict) for x in field) | MAJOR |
| SI-IAQ-03 | shape | Each dict contains keys: 'row_number', 'row_type', 'quantity' | For each dict, assert set(dict.keys()) == {'row_number', 'row_type', 'quantity'} | MAJOR |
| SI-IAQ-04 | immutability | Evidence is immutable after creation (tuple immutability) | Dataclass frozen=True, tuple immutable | MAJOR |

**Semantic Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SE-IAQ-01 | determinism | Same rows → same violations | Run analysis twice, compare results | MAJOR |
| SE-IAQ-02 | boundary | Reports observations — never assesses | Check values against EQ-0011 forbidden terms | MAJOR |

**Cross-field Dependencies:** None

**Traceability:**
- **Engineering Evidence:** EQ-0019 Spike 3 (Deterministic Rule Definition)
- **Production Location:** `boq_intelligence.py` — `_detect_header_quantity_violations()`
- **Previous EQ:** EQ-0019 (Increment 4)

---

#### 19. admin_template_matches

**Field Specification:**
- **Field Name:** `admin_template_matches`
- **Type:** `dict[str, list[dict]] | None`
- **Required:** No (controlled by `include_semantic` parameter)
- **Classification:** Evidence
- **Production Line:** `boq_intelligence.py` — `_detect_admin_template_matches()`
- **Increment:** 4
- **Capability:** SEM-PROD-12

**Semantics:**
- **Description:** Detection of the 5-step administrative sub-template sequence (GENERALLY → REFERENCES → PRICES → GENERAL ITEMS → NOTES AND ASSUMPTIONS).
- **Meaning:** Outer dict: section name → list of match dicts. Each match dict contains: `'pattern_name'` (str), `'matched_text'` (str), `'row_number'` (int). Template sequence is a frozen tuple.
- **Engineering Boundary:** Reports template matches — does not judge completeness or validity.

**Structural Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SI-TMP-01 | presence | Field may be None (controlled by include_semantic parameter) | Assert field is None or isinstance(field, dict) | MINOR |
| SI-TMP-02 | type | When present, must be dict[str, list[dict]] | If not None, assert isinstance(field, dict) and all(isinstance(v, list) for v in field.values()) | MAJOR |
| SI-TMP-03 | immutability | Evidence is immutable after creation | Dataclass frozen=True | MAJOR |
| SI-TMP-04 | frozen_templates | Template sequence is frozen tuple | Verify _ADMIN_TEMPLATE is tuple | MAJOR |

**Semantic Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SE-TMP-01 | determinism | Same rows → same template matches | Run analysis twice, compare results | MAJOR |
| SE-TMP-02 | ordering | Sequence matching preserves worksheet order | Assert row_number values are non-decreasing | MAJOR |

**Cross-field Dependencies:** None

**Traceability:**
- **Engineering Evidence:** EQ-0019 Spike 3 (Deterministic Rule Definition)
- **Production Location:** `boq_intelligence.py` — `_detect_admin_template_matches()`
- **Previous EQ:** EQ-0019 (Increment 4)

---

### BOQHeaderNode Specification

The `BOQHeaderNode` is a frozen dataclass representing a single header (Head1-5) in the reconstructed BOQ hierarchy. Unchanged from v1.0.

**Production Location:** `boq_intelligence.py` — `BOQHeaderNode` class
**Evidence:** EQ-0010 Spike 4 (hierarchy reconstruction algorithm)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| level | int | Yes | Header numeric level. Head1→1, Head2→2, etc. |
| row_number | int | Yes | Original row number from BOQRow. |
| uom | str | Yes | Original UOM string (e.g., "Head1", "Head2"). |
| description | str \| None | Yes | Original description text, None if absent. |
| section | str \| None | Yes | Original section context, None if absent. |
| depth | int | Yes | Computed depth in the reconstructed tree. Root nodes have depth=1. |
| parent_row_number | int \| None | Yes | Row number of the parent header. None for root nodes. |
| children_headers | tuple[BOQHeaderNode, ...] | Yes | Tuple of child header nodes. Empty tuple if no children. |
| children_items | tuple[dict, ...] | Yes | Tuple of child item dicts. Each dict has keys: row_number, code, description, quantity, uom. |

---

## Contract Invariants Summary

### Invariant Counts

| Category | Structural | Semantic | Total |
|----------|-----------|----------|-------|
| Evidence fields (v1.0) | 39 | 31 | 70 |
| Evidence fields (v1.1.0 — new) | 27 | 14 | 41 |
| BOQHeaderNode | 4 | 3 | 7 |
| **Total** | **70** | **48** | **118** |

### Universal Invariants (All Fields)

All 19 evidence fields share these invariants:
1. **Immutability** — Evidence is immutable after creation (frozen dataclass, tuple immutability)
2. **Determinism** — Same input produces same output
3. **Provenance** — All evidence traceable to frozen engineering evidence

### Structural Invariant Categories

| Category | Count | Description |
|----------|-------|-------------|
| Presence | 19 | Field must exist or be None (controlled by parameter) |
| Type | 19 | Field type annotation must match production exactly |
| Shape | 17 | Dictionary keys, tuple structure, list element shape |
| Immutability | 19 | Evidence is immutable after creation |

### Semantic Invariant Categories

| Category | Count | Description |
|----------|-------|-------------|
| Determinism | 19 | Same input always produces same output |
| Provenance | 19 | Traceable to frozen engineering evidence |
| Boundary | 6 | EQ-0011 engineering boundary preserved (v1.0 fields) |
| Meaning | 4 | Evidence meaning is fixed (v1.0 fields) |
| Reproducibility | 1 | Observable from worksheet alone (v1.0 fields) |
| Ordering | 3 | Results sorted in specified order (v1.1.0 fields) |
| Completeness | 3 | All expected entries included (v1.1.0 fields) |
| Frozen Templates | 2 | Pattern/template lists are frozen (v1.1.0 fields) |

### Boundary Preservation

The following 6 fields explicitly preserve the EQ-0011 engineering boundary (Detection vs. Decision):
- `row_classification` (Observation) — v1.0
- `known_anomalies` (Observation) — v1.0
- `detected_level_skips` (Detection) — v1.0
- `zero_quantity_items` (Detection) — v1.0
- `structural_containment_findings` (Detection) — v1.0
- `completeness_findings` (Detection) — v1.0

The 9 v1.1.0 semantic fields also preserve the boundary — all report observable facts only, with no assessment language.

### Violation Handling Policy

**Structural Violations:** Fail fast at analysis time. Raise InvariantViolationError with diagnostic details. No recovery — structural violations are fatal. Consumer impact: analysis fails, no evidence produced.

**Semantic Violations:** Detected at test time via assertions. Raise InvariantViolationError with evidence trace. No recovery — indicates implementation defect. Consumer impact: caught in testing before release.

**Governance:** On violation discovery, create Engineering Question, classify as defect or specification gap, fix implementation or update evidence accordingly.

**Authority:** EQ-0012 Spike 3 (Contract Invariants), frozen unchanged.

---

## Version History

### v1.1.0 — 2026-07-25

**Change Type:** MINOR (non-breaking addition)

**Changes:**
- Added 9 optional semantic evidence fields (SEM-PROD-01 through SEM-PROD-12, excluding deferred)
- Added `include_semantic` parameter to `analyze_boq()`
- All new fields are optional with default `None`
- No existing fields modified, removed, or renamed
- No breaking changes to consumer API

**New Fields:**

| Field | Type | Capability | Controlled By |
|-------|------|-----------|---------------|
| vocabulary | dict[str, int] \| None | SEM-PROD-01 | include_semantic |
| head1_categorization | dict[str, list[dict]] \| None | SEM-PROD-02 | include_semantic |
| administrative_patterns | dict[str, list[dict]] \| None | SEM-PROD-04 | include_semantic + include_hierarchy |
| section_enumeration | tuple[dict, ...] \| None | SEM-PROD-05 | include_semantic |
| uom_distribution | dict[str, int] \| None | SEM-PROD-06 | include_semantic |
| uom_percentages | dict[str, float] \| None | SEM-PROD-06 | include_semantic |
| header_distribution | dict[str, int] \| None | SEM-PROD-07 | include_semantic |
| header_quantity_violations | tuple[dict, ...] \| None | SEM-PROD-09 | include_semantic |
| admin_template_matches | dict[str, list[dict]] \| None | SEM-PROD-12 | include_semantic |

**Invariant Count Change:** 77 → 118 (41 new invariants for 9 new fields)

**Consumer Guarantee Change:** All 16 existing guarantees preserved. No new guarantees added (new fields follow existing guarantee patterns).

---

### v1.0.0 — 2026-07-15

**Change Type:** Initial frozen contract

**Fields:** 10 evidence fields (4 required + 6 optional)
**Invariants:** 77 (43 structural + 34 semantic)
**Consumer Guarantees:** 16
**Verification:** 63/63 MATCH (100%)

---

## Consumer Compatibility

### Backward Compatibility

**All existing consumers are fully backward compatible with v1.1.0.**

| Consumer Action | v1.0 Behavior | v1.1.0 Behavior | Compatible? |
|-----------------|---------------|-----------------|-------------|
| `analyze_boq(rows)` | Returns result with v1.0 fields, new fields = None | Same — new fields default to None | ✓ |
| `analyze_boq(rows, include_hierarchy=True)` | Returns v1.0 + hierarchy fields | Same — new fields still None | ✓ |
| `analyze_boq(rows, include_detection=True)` | Returns v1.0 + detection fields | Same — new fields still None | ✓ |
| Access `result.row_classification` | Works | Works | ✓ |
| Access `result.hierarchy` | Works | Works | ✓ |
| Access `result.detected_level_skips` | Works | Works | ✓ |
| Access `result.vocabulary` | AttributeError (field doesn't exist) | Returns None (field exists, default None) | ✓ (improvement) |

### Consumer Migration Path

**No migration required for existing consumers.**

Consumers that wish to use the new semantic evidence fields should:

1. Call `analyze_boq(rows, include_semantic=True)`
2. Check `result.vocabulary is not None` before accessing (defensive pattern)
3. All new fields follow the same `None`-when-disabled pattern as existing optional fields

### Consumer Impact Assessment

| Consumer | Impact | Action Required |
|----------|--------|-----------------|
| CheckMate (planned) | None — can opt-in to semantic evidence | Call with `include_semantic=True` |
| Formatter | None | No change needed |
| Builder | None | No change needed |
| O&A | None | No change needed |
| Reporting | None | No change needed |

---

## Migration Notes

### For Consumers

**No migration is required.** v1.1.0 is a backward-compatible MINOR version extension.

### For Implementers

When extending BOQ Intelligence in future versions:

1. New evidence fields must be optional with default `None`
2. New fields must be controlled by a parameter (following the `include_*` pattern)
3. New fields must preserve the EQ-0011 evidence/assessment boundary
4. New fields must be deterministic and immutable
5. New fields must be traceable to frozen engineering evidence
6. Adding required fields is a MAJOR version change (requires new EQ disposition)
7. Adding optional fields is a MINOR version change (requires contract update)

### For Contract Maintainers

When updating this contract:

1. Follow the versioning policy (MAJOR/MINOR/PATCH)
2. Update invariant counts in the Contract Invariants Summary
3. Add version history entries
4. Update consumer compatibility assessment
5. Update verification audit
6. All changes must be verified against production implementation

---

## Verification Audit

**Tool:** `tools/eq0012_spike6_contract_verification.py` (v1.0 verification)
**Result:** 100% MATCH — All v1.0 contract elements verified against frozen evidence

| Category | MATCH | Total |
|----------|-------|-------|
| Production Types | 10 | 10 |
| Evidence Fields (v1.0) | 10 | 10 |
| Consumer Guarantees | 16 | 16 |
| Document Sections | 8 | 8 |
| Stable Import Paths | 5 | 5 |
| Versioning Policy | 3 | 3 |
| Deprecation Lifecycle | 6 | 6 |
| Traceability | 3 | 3 |
| No Speculative Content | 0 | 0 |
| **v1.0 Total** | **61** | **61** |

**v1.1.0 Verification (against production implementation):**

| Category | Verified | Total |
|----------|----------|-------|
| New Production Types | 1 | 1 |
| New Evidence Fields | 9 | 9 |
| New Invariants | 41 | 41 |
| Backward Compatibility | 7 | 7 |
| Stable Import Paths (unchanged) | 5 | 5 |
| Consumer Guarantees (preserved) | 16 | 16 |
| **v1.1.0 Total** | **79** | **79** |

**Verification Method:**
- All 9 new fields verified against production fixture (`full_boq.xlsx`)
- All 41 new invariants verified via test suite (53 Increment 4 tests)
- Backward compatibility verified via `TestIncrement4BackwardCompatibility` (2 tests)
- Determinism verified via `TestIncrement4FullPipeline` (3 tests)

**Verification Report:** `data/reports/eq0012_spike6_contract_verification.json` (v1.0)
**IP-0001 Verification:** `docs/implementation/IP_0001/Contract_Verification.md` (v1.1.0)

---

## Document References

| Reference | Description |
|-----------|-------------|
| `src/jarvis/parsers/costx/boq_intelligence.py` | Production implementation (Source of Truth) |
| `src/jarvis/parsers/costx/boq_extraction.py` | BOQ extraction implementation |
| `docs/contracts/BOQ_Intelligence_Public_Evidence_Contract_v1.0.md` | Previous contract version (v1.0) |
| `docs/engineering/questions/EQ_0019_BOQ_Semantic_Intelligence_Increment_1.md` | Engineering Question (EQ-0019) |
| `docs/engineering/evidence/EQ_0019/` | EQ-0019 evidence package |
| `docs/implementation/IP_0001/` | IP-0001 verification package |
| `docs/engineering/Implementation_Governance.md` | Implementation governance v1.0 |
| `docs/engineering/questions/EQ_0012_BOQ_Intelligence_Public_Evidence_Contract.md` | EQ-0012 (contract engineering) |
| `docs/engineering/questions/EQ_0010_Deterministic_BOQ_Structural_Intelligence.md` | EQ-0010 (structural intelligence) |
| `docs/engineering/questions/EQ_0011_BOQ_Semantic_Intelligence_Boundary.md` | EQ-0011 (evidence/assessment boundary) |
| `Engineering_Governance.md v1.0` | Engineering governance |
| `EQ-0007` | Production extraction report |

---

## Document Control

| Property | Value |
|----------|-------|
| **Document ID** | BOQ-INT-EVIDENCE-CONTRACT-v1.1 |
| **Status** | Frozen |
| **Version** | 1.1.0 |
| **Last Updated** | 2026-07-25 |
| **Owner** | Project Owner |
| **Governance** | Engineering_Governance.md v1.0, Implementation_Governance.md v1.0 |
| **Distribution** | Engineering team, all consumers |
| **Previous Version** | v1.0.0 (2026-07-15) |
| **Change Type** | MINOR (9 new optional fields) |

---

**End of Contract Document**
