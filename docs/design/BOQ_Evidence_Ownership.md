# BOQ Evidence Ownership Matrix

## EQ-0020 — BOQ Intelligence Consumer Architecture

### Spike 2 — Evidence Ownership

**Status:** Complete
**Date:** 2026-07-25
**Authority:** EQ-0020 Spike 2

---

## 1. Purpose

Determine ownership of every evidence field in the BOQ Intelligence Public Evidence Contract v1.1.0. Identify the producer, consumer(s), and shared ownership for each evidence element.

---

## 2. Ownership Model

### 2.1 Ownership Categories

| Category | Definition |
|----------|------------|
| **Producer** | The component that generates the evidence field. Owns the field's production logic, invariants, and evolution. |
| **Consumer** | The component that reads and uses the evidence field. Owns interpretation, presentation, and application logic. |
| **Shared Ownership** | Multiple components have ownership responsibilities for different aspects of the field. |
| **Contract** | The Evidence Contract document defines the field's specification. The contract is the authoritative reference for all ownership. |

### 2.2 Ownership Principles

1. **Producer owns production logic** — The producer defines how evidence is generated, what invariants it maintains, and how it evolves.
2. **Consumers own interpretation** — Consumers define how evidence is interpreted, presented, and acted upon.
3. **Contract owns specification** — The Evidence Contract is the authoritative specification for all evidence fields.
4. **No ownership overlap** — Production and interpretation are strictly separated.
5. **Evidence is immutable** — Once produced, evidence cannot be modified by any consumer.

---

## 3. Evidence Field Ownership Matrix

### 3.1 Increment 1 — Observation Evidence (Required Fields)

| Field | Producer | Primary Consumers | Shared Ownership | Contract Authority |
|-------|----------|-------------------|------------------|-------------------|
| `row_classification` | BOQ Intelligence (`_count_row_types`) | Validation Engine, CheckMate, Formatter, Builder, O&A, Reporting | None | Evidence Contract v1.1.0 §3.1 |
| `section_statistics` | BOQ Intelligence (`_compute_section_stats`) | Validation Engine, CheckMate, Formatter, Builder, O&A, Reporting | None | Evidence Contract v1.1.0 §3.2 |
| `boq_statistics` | BOQ Intelligence (`_compute_boq_stats`) | Validation Engine, CheckMate, Formatter, Builder, O&A, Reporting | None | Evidence Contract v1.1.0 §3.3 |
| `known_anomalies` | BOQ Intelligence (`_detect_anomalies`) | Validation Engine, CheckMate, Formatter, Builder, O&A, Reporting | None | Evidence Contract v1.1.0 §3.4 |

### 3.2 Increment 2 — Hierarchy Evidence (Optional Fields)

| Field | Producer | Primary Consumers | Shared Ownership | Contract Authority |
|-------|----------|-------------------|------------------|-------------------|
| `hierarchy` | BOQ Intelligence (`_reconstruct_hierarchy`) | Validation Engine, CheckMate, Formatter, Builder, O&A, Reporting | None | Evidence Contract v1.1.0 §3.5 |
| `hierarchy_statistics` | BOQ Intelligence (`_compute_hierarchy_statistics`) | Validation Engine, CheckMate, Formatter, Builder, O&A, Reporting | None | Evidence Contract v1.1.0 §3.6 |

### 3.3 Increment 3 — Detection Evidence (Optional Fields)

| Field | Producer | Primary Consumers | Shared Ownership | Contract Authority |
|-------|----------|-------------------|------------------|-------------------|
| `detected_level_skips` | BOQ Intelligence (`_detect_level_skips`) | Validation Engine, CheckMate, Formatter, Builder, O&A, Reporting | None | Evidence Contract v1.1.0 §3.7 |
| `zero_quantity_items` | BOQ Intelligence (`_detect_zero_quantities`) | Validation Engine, CheckMate, Formatter, Builder, O&A, Reporting | None | Evidence Contract v1.1.0 §3.8 |
| `structural_containment_findings` | BOQ Intelligence (`_detect_structural_containment`) | Validation Engine, CheckMate, Formatter, Builder, O&A, Reporting | None | Evidence Contract v1.1.0 §3.9 |
| `completeness_findings` | BOQ Intelligence (`_detect_basic_completeness`) | Validation Engine, CheckMate, Formatter, Builder, O&A, Reporting | None | Evidence Contract v1.1.0 §3.10 |

### 3.4 Increment 4 — Semantic Evidence (Optional Fields, v1.1.0)

| Field | Producer | Primary Consumers | Shared Ownership | Contract Authority |
|-------|----------|-------------------|------------------|-------------------|
| `vocabulary` | BOQ Intelligence (`_extract_vocabulary`) | CheckMate, Formatter, Reporting | None | Evidence Contract v1.1.0 §3.11 |
| `head1_categorization` | BOQ Intelligence (`_categorize_head1`) | CheckMate, Formatter, Reporting | None | Evidence Contract v1.1.0 §3.12 |
| `administrative_patterns` | BOQ Intelligence (`_detect_administrative_patterns`) | CheckMate, Builder | None | Evidence Contract v1.1.0 §3.13 |
| `section_enumeration` | BOQ Intelligence (`_enumerate_sections`) | CheckMate, Formatter, Builder, O&A, Reporting | None | Evidence Contract v1.1.0 §3.14 |
| `uom_distribution` | BOQ Intelligence (`_compute_uom_distribution`) | CheckMate, Builder, Reporting | None | Evidence Contract v1.1.0 §3.15 |
| `uom_percentages` | BOQ Intelligence (`_compute_uom_distribution`) | CheckMate, Builder, Reporting | None | Evidence Contract v1.1.0 §3.16 |
| `header_distribution` | BOQ Intelligence (`_compute_header_distribution`) | CheckMate, Builder | None | Evidence Contract v1.1.0 §3.17 |
| `header_quantity_violations` | BOQ Intelligence (`_detect_header_quantity_violations`) | CheckMate, Builder | None | Evidence Contract v1.1.0 §3.18 |
| `admin_template_matches` | BOQ Intelligence (`_detect_admin_template_matches`) | CheckMate, Builder | None | Evidence Contract v1.1.0 §3.19 |

### 3.5 BOQHeaderNode Fields

| Field | Producer | Primary Consumers | Shared Ownership | Contract Authority |
|-------|----------|-------------------|------------------|-------------------|
| `level` | BOQ Intelligence (`_reconstruct_hierarchy`) | Validation Engine, CheckMate, Formatter, Builder, O&A, Reporting | None | Evidence Contract v1.1.0 §4 |
| `row_number` | BOQ Intelligence (`_reconstruct_hierarchy`) | Validation Engine, CheckMate, Formatter, Builder, O&A, Reporting | None | Evidence Contract v1.1.0 §4 |
| `uom` | BOQ Intelligence (`_reconstruct_hierarchy`) | Validation Engine, CheckMate, Formatter, Builder, O&A, Reporting | None | Evidence Contract v1.1.0 §4 |
| `description` | BOQ Intelligence (`_reconstruct_hierarchy`) | Validation Engine, CheckMate, Formatter, Builder, O&A, Reporting | None | Evidence Contract v1.1.0 §4 |
| `section` | BOQ Intelligence (`_reconstruct_hierarchy`) | Validation Engine, CheckMate, Formatter, Builder, O&A, Reporting | None | Evidence Contract v1.1.0 §4 |
| `depth` | BOQ Intelligence (`_reconstruct_hierarchy`) | Validation Engine, CheckMate, Formatter, Builder, O&A, Reporting | None | Evidence Contract v1.1.0 §4 |
| `parent_row_number` | BOQ Intelligence (`_reconstruct_hierarchy`) | Validation Engine, CheckMate, Formatter, Builder, O&A, Reporting | None | Evidence Contract v1.1.0 §4 |
| `children_headers` | BOQ Intelligence (`_reconstruct_hierarchy`) | Validation Engine, CheckMate, Formatter, Builder, O&A, Reporting | None | Evidence Contract v1.1.0 §4 |
| `children_items` | BOQ Intelligence (`_reconstruct_hierarchy`) | Validation Engine, CheckMate, Formatter, Builder, O&A, Reporting | None | Evidence Contract v1.1.0 §4 |

---

## 4. Ownership by Component

### 4.1 BOQ Intelligence (Producer)

**Owns:** All 19 evidence fields + BOQHeaderNode (9 fields)

**Responsibilities:**
- Production logic for all evidence fields
- Structural and semantic invariants
- Determinism guarantees
- Immutability guarantees
- Field evolution within contract versioning policy
- Internal implementation (functions prefixed with `_`)

**Does NOT own:**
- Evidence interpretation
- Evidence presentation
- Evidence application logic
- Evidence validation rules (belongs to Validation Engine)

### 4.2 Validation Engine (Findings Producer)

**Owns:** `ValidationFindings` output structure

**Responsibilities:**
- Rule evaluation logic
- Finding production
- Rule lifecycle management
- Evidence field consumption (read-only)
- Finding determinism

**Does NOT own:**
- Evidence production
- Evidence field evolution
- Consumer interpretation
- Consumer presentation

### 4.3 CheckMate (Primary Consumer)

**Owns:** Interpretation layer, presentation layer, user workflow

**Responsibilities:**
- Evidence interpretation
- Findings interpretation
- User interface
- Validation workflow
- Threshold configuration
- Decision support (human decision remains external)

**Does NOT own:**
- Evidence production
- Evidence field evolution
- Validation rule logic
- Finding production

### 4.4 Formatter (Output Consumer)

**Owns:** Output format rendering

**Responsibilities:**
- Evidence rendering into output formats
- Findings rendering
- Format-specific presentation logic

**Does NOT own:**
- Evidence production
- Evidence interpretation
- Validation logic

### 4.5 Builder (CI/CD Consumer)

**Owns:** Automated pipeline integration

**Responsibilities:**
- Evidence consumption for automated checks
- Findings consumption for pipeline gates
- Machine-readable output

**Does NOT own:**
- Evidence production
- Evidence interpretation
- Validation logic

### 4.6 O&A (Specialized Consumer)

**Owns:** Omission/addition analysis

**Responsibilities:**
- Evidence consumption for O&A analysis
- Findings consumption for O&A-specific checks

**Does NOT own:**
- Evidence production
- Evidence interpretation (beyond O&A scope)
- Validation logic

### 4.7 Reporting (Summary Consumer)

**Owns:** Summary report generation

**Responsibilities:**
- Evidence aggregation for reports
- Findings aggregation
- Report formatting

**Does NOT own:**
- Evidence production
- Evidence interpretation
- Validation logic

---

## 5. Ownership Boundary Matrix

### 5.1 Responsibility vs. Ownership

| Responsibility | Owner | Evidence Contract Authority |
|----------------|-------|----------------------------|
| Evidence production | BOQ Intelligence | Producer |
| Evidence specification | Evidence Contract | Contract |
| Evidence consumption | Consumers | Contract |
| Evidence interpretation | Consumers | Contract |
| Evidence presentation | Consumers | Contract |
| Validation rule logic | Validation Engine | Validation Rule Registry |
| Finding production | Validation Engine | Validation Findings Contract |
| Finding interpretation | Consumers | Validation Findings Contract |
| Finding presentation | Consumers | Validation Findings Contract |

### 5.2 No Ownership Overlap

| Component | Produces Evidence? | Consumes Evidence? | Produces Findings? | Consumes Findings? |
|-----------|-------------------|-------------------|-------------------|-------------------|
| BOQ Intelligence | ✓ (owns) | ✗ | ✗ | ✗ |
| Validation Engine | ✗ | ✓ (read-only) | ✓ (owns) | ✗ |
| CheckMate | ✗ | ✓ | ✗ | ✓ |
| Formatter | ✗ | ✓ | ✗ | ✓ |
| Builder | ✗ | ✓ | ✗ | ✓ |
| O&A | ✗ | ✓ | ✗ | ✓ |
| Reporting | ✗ | ✓ | ✗ | ✓ |

---

## 6. Deliverable

This document is the **Evidence Ownership Matrix** deliverable for EQ-0020 Spike 2.

---

## 7. Document Control

| Property | Value |
|----------|-------|
| **Document ID** | EQ-0020-S2-EVIDENCE-OWNERSHIP |
| **EQ** | EQ-0020 |
| **Spike** | 2 |
| **Status** | Complete |
| **Date** | 2026-07-25 |
| **Owner** | Project Owner |
| **Authority** | EQ-0020 (BOQ Intelligence Consumer Architecture) |
| **References** | BOQ_Intelligence_Public_Evidence_Contract_v1.1.md, EQ-0013 Spike 3 (Engine Scope), EQ-0019 Spike 5 (Consumer Analysis) |

---

**End of Evidence Ownership Matrix**
