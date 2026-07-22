# BOQ Intelligence Public Evidence Contract v1.0

## Contract Header

**Version:** 1.0.0
**Status:** Frozen
**Date:** 2026-07-15
**Engineering Question:** EQ-0012
**Governance:** Engineering_Governance.md v1.0
**Principle:** Evidence Before Abstraction
**Source of Truth:** `src/jarvis/parsers/costx/boq_intelligence.py`

---

## Contract Overview

### Purpose

This document defines the Public Evidence Contract between the **BOQ Intelligence** (Evidence Producer) and all **consumers** of deterministic structural evidence extracted from CostX BOQ workbooks. It is the stable, versioned API that decouples evidence production from consumption.

### Scope

**In scope:**
- 10 evidence fields currently produced by BOQ Intelligence (Increments 1-3)
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
BOQIntelligenceResult  ← Public Evidence Contract v1.0
    ↓
[All Consumers: CheckMate, Formatter, Builder, O&A, Reporting]
```

### First Principle

**The Evidence Contract is the stable API between Intelligence Producer and Intelligence Consumers. It must remain stable across versions while enabling producer evolution.**

### Evidence Admission Rule

Contract specifications may only include:
1. Evidence fields currently produced by BOQ Intelligence (Increments 1-3)
2. Evidence semantics documented in frozen EQ-0010/EQ-0011 evidence reports
3. Data structures directly observable in `BOQIntelligenceResult`

Speculative future evidence, implementation details, and internal algorithms are not permitted.

**Authority:** EQ-0010 (Deterministic BOQ Structural Intelligence), EQ-0011 (BOQ Semantic Intelligence Boundary)

---

## Versioning Policy

### Version Identity

| Property | Value |
|----------|-------|
| Scheme | Semantic Versioning |
| Format | MAJOR.MINOR.PATCH |
| Initial Version | Candidate 1.0.0 (final 1.0.0 reserved for Spike 6 completion) |
| Location | `docs/contracts/BOQ_Intelligence_Public_Evidence_Contract_v1.0.md` |

**Authority:** EQ-0012 Spike 2 (Contract Structure & Versioning Policy)

### Compatibility Rules

#### MAJOR (X.0.0) — Breaking changes requiring consumer attention:

| Change | Rationale |
|--------|-----------|
| Removing a required field | Breaks consuming code that expects the field |
| Changing type of a required field | Breaks consuming code that depends on the type |
| Renaming a required field | Breaks consuming code that references by name |
| Adding, removing, or changing a required field | Contract shape altered; strict consumers (generated clients, type systems, validators) consider required fields mandatory regardless of runtime defaults |
| Changing invariants consumers depend on | Changes behavior consumers may rely on |
| Removing optional field without deprecation | Violates deprecation contract |
| Removing documented dictionary keys | Breaks consumers expecting keys |
| Changing tuple element order or semantics | Breaks consumers using positional access |
| Extending tuple contents | Tuples are ordered, frozen structures; consumers often destructure (`a, b, c = result`) or index (`result[2]`); extension breaks these patterns |

**Policy Notes:**
- **Required fields:** Contract evolution optimizes for strict consumers (generated clients, type systems, validators). Required fields alter contract shape regardless of runtime defaults.
- **Tuples:** Ordered, frozen structures. Future extensible evidence should prefer named structures (dataclasses, dictionaries). If a tuple must grow, explicit append-only semantics required in contract.

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

---

#### 1. row_classification

**Field Specification:**
- **Field Name:** `row_classification`
- **Type:** `dict[str, int]`
- **Required:** Yes (always present)
- **Classification:** Observation
- **Production Line:** `boq_intelligence.py:55`
- **Increment:** 1

**Semantics:**
- **Description:** Maps row type strings to their integer counts within the BOQ worksheet. Provides a summary of row type distribution across Head, Note, Section, Item, and Other categories.
- **Meaning:** Keys are row type identifiers (`'Head'`, `'Note'`, `'Section'`, `'Item'`, `'Other'`); values are occurrence counts. The five keys are guaranteed to always exist.
- **Engineering Boundary:** This field represents observation only — no decision language or assessment.

**Structural Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SI-RC-01 | presence | Field must always exist and never be None | Assert field is not None | MAJOR |
| SI-RC-02 | type | Field must be dict[str, int] | Assert isinstance(field, dict) and all(isinstance(k, str) and isinstance(v, int) for k, v in field.items()) | MAJOR |
| SI-RC-03 | immutability | Evidence is immutable after creation | Dataclass frozen=True | MAJOR |
| SI-RC-04 | shape | Keys are row type strings ('Head', 'Note', 'Section', 'Item', 'Other'), values are integer counts | Assert set(field.keys()) == {'Head', 'Note', 'Section', 'Item', 'Other'} | MAJOR |

**Semantic Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SE-RC-01 | determinism | Same worksheet produces same classifications | Run analysis twice, compare results | MAJOR |
| SE-RC-02 | boundary | Classification is observation only — no decision language | Check row type keys against EQ-0011 forbidden terms | MAJOR |
| SE-RC-03 | provenance | Classification traceable to Increment 1 engineering evidence | Assert classification logic matches EQ-0007 specification | MAJOR |
| SE-RC-04 | reproducibility | Classification reproducible from worksheet observation alone | Assert no external state dependencies | MAJOR |

**Cross-field Dependencies:** section_statistics, boq_statistics

**Traceability:**
- **Engineering Evidence:** EQ-0007 (Production Extraction Report), EQ-0010 Spike 1-2
- **Production Location:** `boq_intelligence.py:120-126` (`_count_row_types`)
- **Previous EQ:** EQ-0007 (Increment 1)

---

#### 2. section_statistics

**Field Specification:**
- **Field Name:** `section_statistics`
- **Type:** `dict[str, dict[str, int]]`
- **Required:** Yes (always present)
- **Classification:** Observation
- **Production Line:** `boq_intelligence.py:56`
- **Increment:** 1

**Semantics:**
- **Description:** Maps section names to their quantity statistics. Each section value is a dict with counts of negative and positive quantities observed in that section.
- **Meaning:** Outer dict: section name (e.g., `"ADDITION"`) → section stats dict. Inner dict keys are `'negative_qty'` and `'positive_qty'` → integer counts of rows with those quantity signs.
- **Engineering Boundary:** This field represents structural observation only — no decision language or assessment.

**Structural Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SI-SS-01 | presence | Field must always exist and never be None | Assert field is not None | MAJOR |
| SI-SS-02 | type | Field must be dict[str, dict[str, int]] | Assert isinstance(field, dict) and all(isinstance(v, dict) for v in field.values()) | MAJOR |
| SI-SS-03 | shape | Outer dict: section name → section stats dict. Inner dict keys: 'negative_qty', 'positive_qty' → integer counts | For each section dict, assert set(section.keys()).issubset({'negative_qty', 'positive_qty'}) | MAJOR |
| SI-SS-04 | immutability | Evidence is immutable after creation | Dataclass frozen=True | MAJOR |

**Semantic Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SE-SS-01 | determinism | Same worksheet produces same section statistics | Run analysis twice, compare results | MAJOR |
| SE-SS-02 | meaning | Section statistics represent structural observation only | Verify no decision semantics in keys or values | MAJOR |
| SE-SS-03 | provenance | Statistics traceable to Increment 1 engineering evidence | Assert logic matches EQ-0007 specification | MAJOR |

**Cross-field Dependencies:** row_classification, boq_statistics

**Traceability:**
- **Engineering Evidence:** EQ-0007 Production Extraction Report
- **Production Location:** `boq_intelligence.py:147-161` (`_compute_section_stats`)
- **Previous EQ:** EQ-0007 (Increment 1)

---

#### 3. boq_statistics

**Field Specification:**
- **Field Name:** `boq_statistics`
- **Type:** `dict[str, int | float]`
- **Required:** Yes (always present)
- **Classification:** Observation
- **Production Line:** `boq_intelligence.py:57`
- **Increment:** 1

**Semantics:**
- **Description:** Provides aggregate statistics about the entire BOQ worksheet, including row counts and column completeness indicators.
- **Meaning:** Keys: `'total_rows'` (total row count), `'code_rows'` (rows with code), `'description_rows'` (rows with description), `'quantity_rows'` (rows with quantity), `'uom_rows'` (rows with UOM), `'section_rows'` (rows with section). Values are integer or float counts.
- **Engineering Boundary:** This field represents quantitative observation only — no decision language or assessment.

**Structural Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SI-BS-01 | presence | Field must always exist and never be None | Assert field is not None | MAJOR |
| SI-BS-02 | type | Field must be dict[str, int \| float] | Assert isinstance(field, dict) and all(isinstance(v, (int, float)) for v in field.values()) | MAJOR |
| SI-BS-03 | shape | Required keys: 'total_rows', 'code_rows', 'description_rows', 'quantity_rows', 'uom_rows', 'section_rows' → int or float values | Assert set(field.keys()) == {'total_rows', 'code_rows', 'description_rows', 'quantity_rows', 'uom_rows', 'section_rows'} | MAJOR |
| SI-BS-04 | immutability | Evidence is immutable after creation | Dataclass frozen=True | MAJOR |

**Semantic Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SE-BS-01 | determinism | Same worksheet produces same BOQ statistics | Run analysis twice, compare results | MAJOR |
| SE-BS-02 | meaning | BOQ statistics represent quantitative observation only | Verify no decision semantics in keys or values | MAJOR |
| SE-BS-03 | provenance | Statistics traceable to Increment 1 engineering evidence | Assert logic matches EQ-0007 specification | MAJOR |

**Cross-field Dependencies:** row_classification, section_statistics

**Traceability:**
- **Engineering Evidence:** EQ-0007 Production Extraction Report
- **Production Location:** `boq_intelligence.py:129-144` (`_compute_boq_stats`)
- **Previous EQ:** EQ-0007 (Increment 1)

---

#### 4. known_anomalies

**Field Specification:**
- **Field Name:** `known_anomalies`
- **Type:** `list[dict[str, int | str | float]]`
- **Required:** Yes (always present, may be empty list)
- **Classification:** Observation
- **Production Line:** `boq_intelligence.py:58`
- **Increment:** 1

**Semantics:**
- **Description:** Lists detected omission anomalies — rows in OMISSION sections that have positive quantities. An empty list indicates no anomalies detected.
- **Meaning:** Each anomaly dict contains keys: `'row_number'` (int), `'code'` (str), `'quantity'` (float), `'section'` (str). Anomalies are sorted by row_number.
- **Engineering Boundary:** This field describes observations only — no decision language or assessment. It flags patterns, not problems.

**Structural Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SI-KA-01 | presence | Field must always exist (may be empty list) | Assert field is not None | MAJOR |
| SI-KA-02 | type | Field must be list[dict[str, int \| str \| float]] | Assert isinstance(field, list) and all(isinstance(x, dict) for x in field) | MAJOR |
| SI-KA-03 | shape | Each anomaly dict contains keys: 'row_number' (int), 'code' (str), 'quantity' (float), 'section' (str) | For each anomaly, assert set(anomaly.keys()) == {'row_number', 'code', 'quantity', 'section'} | MAJOR |
| SI-KA-04 | immutability | Evidence is immutable after creation | Dataclass frozen=True | MAJOR |

**Semantic Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SE-KA-01 | determinism | Same worksheet produces same anomaly list | Run analysis twice, compare results | MAJOR |
| SE-KA-02 | boundary | Anomalies describe observations only — no decision language | Check anomaly values against EQ-0011 forbidden terms | MAJOR |
| SE-KA-03 | provenance | Anomalies traceable to Increment 1 engineering evidence | Assert logic matches EQ-0007 specification | MAJOR |

**Cross-field Dependencies:** None

**Traceability:**
- **Engineering Evidence:** EQ-0006 (Omission Anomalies), EQ-0007 Production Extraction Report
- **Production Location:** `boq_intelligence.py:164-178` (`_detect_anomalies`)
- **Previous EQ:** EQ-0007 (Increment 1)

---

### Increment 2 — Hierarchy Evidence

---

#### 5. hierarchy

**Field Specification:**
- **Field Name:** `hierarchy`
- **Type:** `tuple[BOQHeaderNode, ...] | None`
- **Required:** No (controlled by `include_hierarchy` parameter)
- **Classification:** Hierarchy
- **Production Line:** `boq_intelligence.py:59`
- **Increment:** 2

**Semantics:**
- **Description:** Reconstructed BOQ header hierarchy as a tuple of root-level BOQHeaderNode objects. Each node represents a header (Head1-5) in the deterministic tree structure. The hierarchy is built from the linear BOQRow sequence using a stack-based reconstruction algorithm.
- **Meaning:** When `include_hierarchy=True`, this field contains the root header nodes; `None` otherwise. Each BOQHeaderNode has fields: level, row_number, uom, description, section, depth, parent_row_number, children_headers, children_items.
- **Engineering Boundary:** This field represents structural relationships only — no decision language or assessment. The hierarchy is deterministic.

**Structural Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SI-H-01 | presence | Field may be None (controlled by include_hierarchy parameter) | Assert field is None or isinstance(field, tuple) | MINOR |
| SI-H-02 | type | When present, must be tuple[BOQHeaderNode, ...] | If not None, assert isinstance(field, tuple) and all(isinstance(n, BOQHeaderNode) for n in field) | MAJOR |
| SI-H-03 | immutability | Evidence is immutable after creation (tuple + frozen BOQHeaderNode) | Dataclass frozen=True, tuple immutable, BOQHeaderNode frozen | MAJOR |

**Semantic Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SE-H-01 | determinism | Same worksheet produces same hierarchy when include_hierarchy=True | Run analysis twice with same parameters, compare results | MAJOR |
| SE-H-02 | meaning | Hierarchy represents structural relationships only | Verify no decision semantics in node attributes | MAJOR |
| SE-H-03 | provenance | Hierarchy traceable to Increment 2 engineering evidence | Assert logic matches EQ-0010 specification | MAJOR |

**Cross-field Dependencies:** hierarchy_statistics

**Traceability:**
- **Engineering Evidence:** EQ-0010 Spike 4 (hierarchy reconstruction algorithm)
- **Production Location:** `boq_intelligence.py:198-260` (`_reconstruct_hierarchy`)
- **Previous EQ:** EQ-0010 (Increment 2)

---

#### 6. hierarchy_statistics

**Field Specification:**
- **Field Name:** `hierarchy_statistics`
- **Type:** `dict[str, int | float] | None`
- **Required:** No (controlled by `include_hierarchy` parameter)
- **Classification:** Hierarchy
- **Production Line:** `boq_intelligence.py:60`
- **Increment:** 2

**Semantics:**
- **Description:** Provides aggregate statistics about the reconstructed hierarchy, including total header counts, depth distribution, and average items per header by UOM type.
- **Meaning:** Keys: `'total_headers'` (total number of header nodes), `'root_headers'` (number of root-level headers), `'depth_distribution'` (dict mapping depth level to count), `'items_per_header_by_uom'` (dict mapping UOM to average item count). Values are integer or float.
- **Engineering Boundary:** This field represents quantitative hierarchy observation only — no decision language or assessment.

**Structural Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SI-HS-01 | presence | Field may be None (controlled by include_hierarchy parameter) | Assert field is None or isinstance(field, dict) | MINOR |
| SI-HS-02 | type | When present, must be dict[str, int \| float] | If not None, assert isinstance(field, dict) and all(isinstance(v, (int, float)) for v in field.values()) | MAJOR |
| SI-HS-03 | shape | Required keys: 'total_headers', 'root_headers', 'depth_distribution', 'items_per_header_by_uom' → int or float values | If not None, assert set(field.keys()) == {'total_headers', 'root_headers', 'depth_distribution', 'items_per_header_by_uom'} | MAJOR |
| SI-HS-04 | immutability | Evidence is immutable after creation | Dataclass frozen=True | MAJOR |

**Semantic Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SE-HS-01 | determinism | Same worksheet produces same hierarchy statistics when include_hierarchy=True | Run analysis twice with same parameters, compare results | MAJOR |
| SE-HS-02 | meaning | Statistics represent quantitative hierarchy observation only | Verify no decision semantics in keys or values | MAJOR |
| SE-HS-03 | provenance | Statistics traceable to Increment 2 engineering evidence | Assert logic matches EQ-0010 specification | MAJOR |

**Cross-field Dependencies:** hierarchy

**Traceability:**
- **Engineering Evidence:** EQ-0010 Spike 4 (hierarchy statistics)
- **Production Location:** `boq_intelligence.py:279-330` (`_compute_hierarchy_statistics`)
- **Previous EQ:** EQ-0010 (Increment 2)

---

### Increment 3 — Detection Evidence

---

#### 7. detected_level_skips

**Field Specification:**
- **Field Name:** `detected_level_skips`
- **Type:** `tuple[dict[str, int], ...] | None`
- **Required:** No (controlled by `include_detection` parameter)
- **Classification:** Detection
- **Production Line:** `boq_intelligence.py:61`
- **Increment:** 3

**Semantics:**
- **Description:** Records observable facts about level skips in the hierarchy structure. A level skip occurs when a child header's level is more than one greater than its parent's level. Does not assess legitimacy — it is an observation of structure.
- **Meaning:** Each skip dict contains: `'parent_row_number'` (int), `'parent_level'` (int), `'child_row_number'` (int), `'child_level'` (int), `'skip_magnitude'` (int). The magnitude equals `(child_level - parent_level - 1)`.
- **Engineering Boundary:** Detections describe patterns only — no decision language, no assessment of whether the skip is valid.

**Structural Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SI-DLS-01 | presence | Field may be None (controlled by include_detection parameter) | Assert field is None or isinstance(field, tuple) | MINOR |
| SI-DLS-02 | type | When present, must be tuple[dict[str, int], ...] | If not None, assert isinstance(field, tuple) and all(isinstance(x, dict) for x in field) | MAJOR |
| SI-DLS-03 | shape | Each skip dict contains keys: 'parent_row_number', 'parent_level', 'child_row_number', 'child_level', 'skip_magnitude' → int values | For each skip, verify all keys present and all values are int | MAJOR |
| SI-DLS-04 | immutability | Evidence is immutable after creation (tuple immutability) | Dataclass frozen=True, tuple immutable | MAJOR |

**Semantic Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SE-DLS-01 | determinism | Same worksheet produces same level skips when include_detection=True | Run analysis twice with same parameters, compare results | MAJOR |
| SE-DLS-02 | boundary | Detections describe patterns only — no decision language | Check field keys/values against EQ-0011 forbidden terms | MAJOR |
| SE-DLS-03 | provenance | Detections traceable to Increment 3 engineering evidence | Assert logic matches EQ-0011 specification | MAJOR |

**Cross-field Dependencies:** hierarchy

**Traceability:**
- **Engineering Evidence:** EQ-0011 Spike 2, Spike 3
- **Production Location:** `boq_intelligence.py:335-367` (`_detect_level_skips`)
- **Previous EQ:** EQ-0011 (Increment 3)

---

#### 8. zero_quantity_items

**Field Specification:**
- **Field Name:** `zero_quantity_items`
- **Type:** `tuple[dict[str, int | str | float | None], ...] | None`
- **Required:** No (controlled by `include_detection` parameter)
- **Classification:** Detection
- **Production Line:** `boq_intelligence.py:62`
- **Increment:** 3

**Semantics:**
- **Description:** Records observable facts about Item rows with quantity equal to 0.0. Does not assess whether zero quantities are acceptable — it is an observation of quantity values.
- **Meaning:** Each item dict contains: `'row_number'` (int), `'code'` (str), `'description'` (str | None), `'section'` (str | None), `'quantity'` (float), `'uom'` (str | None). Values may be None for optional BOQRow fields.
- **Engineering Boundary:** Detections describe patterns only — no decision language, no assessment of whether zero quantities are errors.

**Structural Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SI-ZQI-01 | presence | Field may be None (controlled by include_detection parameter) | Assert field is None or isinstance(field, tuple) | MINOR |
| SI-ZQI-02 | type | When present, must be tuple[dict[str, int \| str \| float \| None], ...] | If not None, assert isinstance(field, tuple) and all(isinstance(x, dict) for x in field) | MAJOR |
| SI-ZQI-03 | shape | Each item dict contains keys: 'row_number', 'code', 'description', 'section', 'quantity', 'uom' | For each item, verify all keys present | MAJOR |
| SI-ZQI-04 | immutability | Evidence is immutable after creation (tuple immutability) | Dataclass frozen=True, tuple immutable | MAJOR |

**Semantic Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SE-ZQI-01 | determinism | Same worksheet produces same zero quantity items when include_detection=True | Run analysis twice with same parameters, compare results | MAJOR |
| SE-ZQI-02 | boundary | Detections describe patterns only — no decision language | Check field keys/values against EQ-0011 forbidden terms | MAJOR |
| SE-ZQI-03 | provenance | Detections traceable to Increment 3 engineering evidence | Assert logic matches EQ-0011 specification | MAJOR |

**Cross-field Dependencies:** row_classification

**Traceability:**
- **Engineering Evidence:** EQ-0011 Spike 2, Spike 3
- **Production Location:** `boq_intelligence.py:369-396` (`_detect_zero_quantities`)
- **Previous EQ:** EQ-0011 (Increment 3)

---

#### 9. structural_containment_findings

**Field Specification:**
- **Field Name:** `structural_containment_findings`
- **Type:** `tuple[dict[str, int], ...] | None`
- **Required:** No (controlled by `include_detection` parameter)
- **Classification:** Detection
- **Production Line:** `boq_intelligence.py:63`
- **Increment:** 3

**Semantics:**
- **Description:** Records observable facts about structural inversions in the hierarchy. An inversion occurs when a child header's level is greater than its parent's level (child_level > parent_level). This should not occur given the stack-based reconstruction algorithm, but is checked for completeness.
- **Meaning:** Each finding dict contains: `'parent_row_number'` (int), `'parent_level'` (int), `'child_row_number'` (int), `'child_level'` (int).
- **Engineering Boundary:** Findings describe patterns only — no decision language, no semantic scope assessment.

**Structural Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SI-SCF-01 | presence | Field may be None (controlled by include_detection parameter) | Assert field is None or isinstance(field, tuple) | MINOR |
| SI-SCF-02 | type | When present, must be tuple[dict[str, int], ...] | If not None, assert isinstance(field, tuple) and all(isinstance(x, dict) for x in field) | MAJOR |
| SI-SCF-03 | shape | Each finding dict contains keys: 'parent_row_number', 'parent_level', 'child_row_number', 'child_level' → int values | For each finding, verify all keys present and all values are int | MAJOR |
| SI-SCF-04 | immutability | Evidence is immutable after creation (tuple immutability) | Dataclass frozen=True, tuple immutable | MAJOR |

**Semantic Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SE-SCF-01 | determinism | Same worksheet produces same structural findings when include_detection=True | Run analysis twice with same parameters, compare results | MAJOR |
| SE-SCF-02 | boundary | Findings describe patterns only — no decision language | Check field keys/values against EQ-0011 forbidden terms | MAJOR |
| SE-SCF-03 | provenance | Findings traceable to Increment 3 engineering evidence | Assert logic matches EQ-0011 specification | MAJOR |

**Cross-field Dependencies:** hierarchy, row_classification

**Traceability:**
- **Engineering Evidence:** EQ-0011 Spike 3
- **Production Location:** `boq_intelligence.py:398-430` (`_detect_structural_containment`)
- **Previous EQ:** EQ-0011 (Increment 3)

---

#### 10. completeness_findings

**Field Specification:**
- **Field Name:** `completeness_findings`
- **Type:** `tuple[dict[str, int | str], ...] | None`
- **Required:** No (controlled by `include_detection` parameter)
- **Classification:** Detection
- **Production Line:** `boq_intelligence.py:64`
- **Increment:** 3

**Semantics:**
- **Description:** Records observable facts about sections that have zero measurable items within the reconstructed hierarchy. Identifies sections present in the hierarchy structure but lacking any Item rows.
- **Meaning:** Each finding dict contains: `'section'` (str) — section name, `'item_count'` (int) — number of items in that section (always 0 for findings). Findings are ordered by section name.
- **Engineering Boundary:** Findings describe patterns only — no decision language, no assessment of project completeness.

**Structural Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SI-CF-01 | presence | Field may be None (controlled by include_detection parameter) | Assert field is None or isinstance(field, tuple) | MINOR |
| SI-CF-02 | type | When present, must be tuple[dict[str, int \| str], ...] | If not None, assert isinstance(field, tuple) and all(isinstance(x, dict) for x in field) | MAJOR |
| SI-CF-03 | shape | Each finding dict contains keys: 'section' (str), 'item_count' (int) | For each finding, assert set(finding.keys()) == {'section', 'item_count'} | MAJOR |
| SI-CF-04 | immutability | Evidence is immutable after creation (tuple immutability) | Dataclass frozen=True, tuple immutable | MAJOR |

**Semantic Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SE-CF-01 | determinism | Same worksheet produces same completeness findings when include_detection=True | Run analysis twice with same parameters, compare results | MAJOR |
| SE-CF-02 | boundary | Findings describe patterns only — no decision language | Check field keys/values against EQ-0011 forbidden terms | MAJOR |
| SE-CF-03 | provenance | Findings traceable to Increment 3 engineering evidence | Assert logic matches EQ-0011 specification | MAJOR |

**Cross-field Dependencies:** row_classification, section_statistics

**Traceability:**
- **Engineering Evidence:** EQ-0011 Spike 3
- **Production Location:** `boq_intelligence.py:432-476` (`_detect_basic_completeness`)
- **Previous EQ:** EQ-0011 (Increment 3)

---

## BOQHeaderNode Specification

The `BOQHeaderNode` is a frozen dataclass representing a single header (Head1-5) in the reconstructed BOQ hierarchy.

**Production Location:** `boq_intelligence.py:27-45`
**Evidence:** EQ-0010 Spike 4 (hierarchy reconstruction algorithm)

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| level | int | Yes | Header numeric level. Head1→1, Head2→2, etc. |
| row_number | int | Yes | Original row number from BOQRow. |
| uom | str | Yes | Original UOM string (e.g., "Head1", "Head2"). |
| description | str \| None | Yes | Original description text, None if absent. |
| section | str \| None | Yes | Original section context (e.g., "ADDITION", "OMISSION"), None if absent. |
| depth | int | Yes | Computed depth in the reconstructed tree. Root nodes have depth=1. |
| parent_row_number | int \| None | Yes | Row number of the parent header. None for root nodes. |
| children_headers | tuple[BOQHeaderNode, ...] | Yes | Tuple of child header nodes. Empty tuple if no children. |
| children_items | tuple[dict[str, int \| str \| float \| None], ...] | Yes | Tuple of child item dicts. Each dict has keys: row_number, code, description, quantity, uom. |

### Structural Invariants

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SI-HN-01 | presence | All fields are always present (no None for non-optional fields) | Assert all required fields have values | MAJOR |
| SI-HN-02 | type | Types match specifications exactly | Type check each field | MAJOR |
| SI-HN-03 | shape | level=1 for Head1, level=2 for Head2, etc.; depth≥1 for all nodes | Assert level in {1,2,3,4,5} and depth≥1 | MAJOR |
| SI-HN-04 | immutability | BOQHeaderNode is a frozen dataclass | Dataclass frozen=True | MAJOR |

### Semantic Invariants

| ID | Category | Description | Verification |
|----|----------|-------------|--------------|
| SE-HN-01 | determinism | Same input produces same header node structure | Run analysis twice, compare |
| SE-HN-02 | provenance | Tree structure traceable to EQ-0010 Spike 4 | Assert logic matches specification |
| SE-HN-03 | reproducibility | Hierarchy reproducible from worksheet observation alone | Assert no external state dependencies |

---

## Contract Invariants Summary

### Invariant Counts

| Category | Structural | Semantic | Total |
|----------|-----------|----------|-------|
| Evidence fields | 39 | 31 | 70 |
| BOQHeaderNode | 4 | 3 | 7 |
| **Total** | **43** | **34** | **77** |

### Universal Invariants (All Fields)

All 10 evidence fields share these invariants:
1. **Immutability** — Evidence is immutable after creation (frozen dataclass, tuple immutability)
2. **Determinism** — Same input produces same output
3. **Provenance** — All evidence traceable to frozen engineering evidence

### Structural Invariant Categories

| Category | Count | Description |
|----------|-------|-------------|
| Presence | 10 | Field must exist or be None (controlled by parameter) |
| Type | 10 | Field type annotation must match production exactly |
| Shape | 9 | Dictionary keys, tuple structure, list element shape |
| Immutability | 10 | Evidence is immutable after creation |

### Semantic Invariant Categories

| Category | Count | Description |
|----------|-------|-------------|
| Determinism | 10 | Same input always produces same output |
| Provenance | 10 | Traceable to frozen engineering evidence |
| Boundary | 6 | EQ-0011 engineering boundary preserved |
| Meaning | 4 | Evidence meaning is fixed |
| Reproducibility | 1 | Observable from worksheet alone |

### Boundary Preservation

The following 6 fields explicitly preserve the EQ-0011 engineering boundary (Detection vs. Decision):
- `row_classification` (Observation)
- `known_anomalies` (Observation)
- `detected_level_skips` (Detection)
- `zero_quantity_items` (Detection)
- `structural_containment_findings` (Detection)
- `completeness_findings` (Detection)

### Violation Handling Policy

**Structural Violations:** Fail fast at analysis time. Raise InvariantViolationError with diagnostic details. No recovery — structural violations are fatal. Consumer impact: analysis fails, no evidence produced.

**Semantic Violations:** Detected at test time via assertions. Raise InvariantViolationError with evidence trace. No recovery — indicates implementation defect. Consumer impact: caught in testing before release.

**Governance:** On violation discovery, create Engineering Question, classify as defect or specification gap, fix implementation or update evidence accordingly.

**Authority:** EQ-0012 Spike 3 (Contract Invariants), frozen unchanged.

---

## Verification Audit

**Tool:** `tools/eq0012_spike6_contract_verification.py`
**Result:** 100% MATCH — All contract elements verified against frozen evidence

| Category | MATCH | Total |
|----------|-------|-------|
| Production Types | 10 | 10 |
| Evidence Fields | 10 | 10 |
| Consumer Guarantees | 16 | 16 |
| Document Sections | 8 | 8 |
| Stable Import Paths | 5 | 5 |
| Versioning Policy | 3 | 3 |
| Deprecation Lifecycle | 6 | 6 |
| Traceability | 3 | 3 |
| No Speculative Content | 0 | 0 |
| **Total** | **61** | **61** |

**Verification Report:** `data/reports/eq0012_spike6_contract_verification.json`

---

## Document References

| Reference | Description |
|-----------|-------------|
| `src/jarvis/parsers/costx/boq_intelligence.py` | Production implementation (Source of Truth) |
| `src/jarvis/parsers/costx/boq_extraction.py` | BOQ extraction implementation |
| `docs/engineering/evidence/EQ_0012_Spike1_Evidence_Report_Current_Evidence_Inventory.md` | Evidence inventory |
| `docs/engineering/evidence/EQ_0012_Spike2_Evidence_Report_Contract_Versioning_Policy.md` | Versioning policy |
| `docs/engineering/evidence/EQ_0012_Spike3_Evidence_Report_Contract_Invariants.md` | Contract invariants |
| `docs/engineering/evidence/EQ_0012_Spike4_Evidence_Report_Consumer_Access_Patterns.md` | Consumer access patterns |
| `docs/engineering/evidence/EQ_0012_Spike5_Evidence_Report_Contract_Documentation_Standards.md` | Documentation standards |
| `docs/engineering/questions/EQ_0012_BOQ_Intelligence_Public_Evidence_Contract.md` | Engineering Question |
| `Engineering_Governance.md v1.0` | Engineering governance |
| `EQ-0007`, `EQ-0010`, `EQ-0011` | Prior engineering questions |

---

## Document Control

| Property | Value |
|----------|-------|
| **Document ID** | BOQ-INT-EVIDENCE-CONTRACT-v1.0 |
| **Status** | Candidate |
| **Version** | Candidate 1.0.0 |
| **Last Updated** | 2026-07-15 |
| **Owner** | Project Owner |
| **Governance** | Engineering_Governance.md v1.0 |
| **Distribution** | Engineering team, all consumers |

---

**End of Contract Document**