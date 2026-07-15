# EQ-0012 — Spike 5 — Evidence Report — Contract Documentation Standards

**Date:** 2026-07-15  
**Status:** Complete (Pre-Freeze)  
**Investigation:** EQ-0012 BOQ Intelligence Public Evidence Contract  
**Governance:** Engineering_Governance.md v1.0  
**Principle:** Evidence Before Abstraction  
**Source of Truth:** `docs/engineering/evidence/` (Spikes 1-4 frozen evidence)

---

## Objective

Define documentation requirements and format standards for the BOQ Intelligence Public Evidence Contract v1.0.

This spike establishes the template and quality standards that the final contract document must follow.

---

## Methodology

Systematic analysis of frozen evidence from Spikes 1-4 to derive documentation format requirements. Every standard traces to existing evidence or production implementation.

**Tool:** `tools/eq0012_spike5_contract_documentation_standards.py`

---

## Engineering Questions

### Q1: What documentation is required for each evidence field?

**Finding:** 8 required document sections:

| # | Section | Elements | Evidence Source |
|---|---|---|---|
| 1 | Contract Header | 7 | Requirement: establish identity, version, authority |
| 2 | Contract Overview | 5 | Requirement: scope, architecture context |
| 3 | Versioning Policy | 6 | Spike 2 (frozen) |
| 4 | Deprecation Lifecycle | 3 | Spike 2 (frozen) |
| 5 | Consumer Access Patterns | 4 | Spike 4 (frozen) |
| 6 | Evidence Field Specifications | 10 per field | Spike 1, 3 (frozen) |
| 7 | BOQHeaderNode Specification | 3 | Production `boq_intelligence.py:27-45` |
| 8 | Contract Invariants Summary | 5 | Spike 3 (frozen) |

### Q2: How are field semantics specified?

**Finding:** Template-based per field with 3 required components:

| Component | Format | Example |
|---|---|---|
| Description | Single paragraph (2-3 sentences) | "Maps row type strings to integer counts..." |
| Meaning | Bullet points | "Keys: row type identifiers; Values: occurrence counts" |
| Engineering Boundary | Single sentence | "Observation only — no decision language or assessment" |

### Q3: How are data structure invariants documented?

**Finding:** Table-based per field (from Spike 3 format):

```
| ID | Category | Description | Verification | Violation Impact |
```

Split into structural and semantic sections. 70 invariants total (39 structural, 31 semantic).

### Q4: How are evidence constraints described?

**Finding:** Inline within field specification:

| Constraint | Format | Example |
|---|---|---|
| Optionality | Required or Optional | "Required (always present)" / "Optional (controlled by include_detection)" |
| Field Relationships | List | "Dependencies: hierarchy, row_classification" |
| Version Stability | Reference | "MAJOR version-locked per Spike 2 policy" |

### Q5: How is evidence traceability maintained?

**Finding:** 4 per-field + 3 document-level traceability requirements:

**Per-field:**
1. Engineering Evidence Reference (EQ report)
2. Production Location (file:line)
3. Previous EQ Reference
4. Contract Documentation Reference (Spike #)

**Document-level:**
1. Source of Truth Statement
2. Governance Reference
3. Verification Audit Record

**Traceability chain:**
```
Engineering Question → Spike Reports → Production Implementation → Frozen Evidence → Contract v1.0 → Verification Audit
```

**Principle:** Documentation never defines production. Production defines documentation.

### Q6: What format should the contract document follow?

**Finding:** 8-section Markdown document following the template defined in this report. Section sequence:

```
1. Contract Header
2. Contract Overview
3. Versioning Policy
4. Deprecation Lifecycle
5. Consumer Access Patterns
6. Evidence Field Specifications (10 fields)
7. BOQHeaderNode Specification
8. Contract Invariants Summary
```

---

## Per-Field Documentation Template

Each of the 10 evidence fields must be documented using this template:

### Field Specification Block

```
**Field Name:** [exact production name]
**Type:** [exact production type annotation]
**Required:** [true/false]
**Classification:** [Observation/Hierarchy/Detection]
**Production Line:** [boq_intelligence.py line number]
**Increment:** [1/2/3]
```

### Semantics Block

```
**Description:** [2-3 sentence human-readable description]
**Meaning:** [bullet points explaining each key/value]
**Engineering Boundary:** [single sentence confirming observation/detection only]
```

### Structural Invariants Table

```
| ID | Category | Description | Verification | Violation Impact |
```

### Semantic Invariants Table

```
| ID | Category | Description | Verification | Violation Impact |
```

### Cross-field Dependencies

```
**Dependencies:** [list of field names]
```

### Traceability

```
**Engineering Evidence:** [EQ report reference]
**Production Location:** [file:line]
**Previous EQ:** [EQ identifier]
```

---

## Field Documentation Order

Fields must be documented in Increment order:

**Increment 1 (Observation):**
1. row_classification
2. section_statistics
3. boq_statistics
4. known_anomalies

**Increment 2 (Hierarchy):**
5. hierarchy
6. hierarchy_statistics

**Increment 3 (Detection):**
7. detected_level_skips
8. zero_quantity_items
9. structural_containment_findings
10. completeness_findings

---

## Versioning Policy Section Template

The contract versioning section must include:

1. Version identity (Semantic Versioning MAJOR.MINOR.PATCH)
2. MAJOR breaking changes list
3. MINOR non-breaking additions list
4. PATCH internal corrections list
5. Policy notes on required fields and tuples
6. 16 consumer guarantees (G-01 through G-16)
7. Three-phase deprecation lifecycle
8. Governance gate requirements

---

## Consumer Access Patterns Section Template

The consumer access section must include:

1. 5 stable import paths (from Spike 4)
2. 9 must-not-import symbols (from Spike 4)
3. Recommended access pattern with Python code example
4. Consumer usage flow diagram

---

## BOQHeaderNode Specification

Must document all 9 fields of the `BOQHeaderNode` frozen dataclass:

| Field | Type | Description |
|---|---|---|
| level | int | Head1→1, Head2→2, etc. |
| row_number | int | Original BOQRow.row_number |
| uom | str | Original UOM string |
| description | str \| None | Original description |
| section | str \| None | Original section context |
| depth | int | Computed depth in tree |
| parent_row_number | int \| None | Parent's row_number, None for roots |
| children_headers | tuple[BOQHeaderNode, ...] | Child header nodes |
| children_items | tuple[dict, ...] | Child items |

---

## Contract Invariants Summary Template

Must include:

1. Summary counts (70 total: 39 structural, 31 semantic)
2. Universal invariants (immutability, determinism, provenance)
3. Structural categories (presence: 10, type: 10, shape: 9, immutability: 10)
4. Semantic categories (determinism: 10, provenance: 10, boundary: 6, meaning: 4, reproducibility: 1)
5. Violation handling policy summary

---

## Verification Audit

**Tool:** `tools/eq0012_spike5_verification_audit.py`  
**Result:** **13 MATCH — All standards traceable to frozen evidence**  
**Report:** `data/reports/eq0012_spike5_verification_audit.json`

| Category | Total | MATCH | Drift |
|---|---|---|---|
| Frozen Evidence Files Exist | 4 | 4 | 0 |
| Section Requirements Traceable | 8 | 8 | 0 |
| Field Order Correct | 1 | 1 | 0 |
| **Total** | **13** | **13** | **0** |

---

## Conclusion

**Status:** Complete

**Key Findings:**
- 8 required contract document sections defined
- Per-field template with 5 specification blocks established
- 70 invariants documented in table format
- Traceability chain defined with 4 per-field + 3 document-level requirements
- All 13 verification checks MATCH — all standards traceable to frozen evidence

**Verification Audit:** 13 MATCH — All documentation matches frozen evidence

**Recommendation:** Proceed to Spike 6 (Evidence Contract v1.0 Specification) to author the final contract document using these standards.

---

## Tool

**Analysis Tool:** `tools/eq0012_spike5_contract_documentation_standards.py`  
**Analysis Output:** `data/reports/eq0012_spike5_documentation_standards.json`  
**Verification Tool:** `tools/eq0012_spike5_verification_audit.py`  
**Verification Output:** `data/reports/eq0012_spike5_verification_audit.json`

---

**End of Evidence Report**