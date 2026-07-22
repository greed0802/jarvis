# 03 — Domain Knowledge

> **Purpose**: Compressed summary of the Quantity Surveying domain knowledge documented in `docs/domain/`. Captures verified facts, critical boundaries, and flags unverified content.
> **Part of**: Jarvis Knowledge Consolidation

---

## Responsibilities

This document covers:
- Domain overview (Quantity Surveying, BOQ structure)
- Verified BOQ structure and evidence/assessment boundary
- Key domain concepts with verification status
- What is frozen vs pending verification

It does NOT cover platform architecture (see `02_Architecture_Summary.md`) or specific EQ findings (see `05_Engineering_Questions.md`). Per-document verification details are in [Appendix C](Appendices/C_Domain_Verification_Matrix.md).

---

## Domain Overview

**Domain**: Quantity Surveying / Civil Engineering / Cost Estimating
**Primary Artifact**: Bill of Quantities (BOQ)
**Source Format**: CostX Excel workbooks (.xlsx)
**Production Fixture**: `full_boq.xlsx` (single-fixture investigation pattern per EQ-0010)

---

## BOQ Structure (FROZEN — Evidence-Backed)

**Source**: `docs/domain/02_BOQ_Structure.md` — validated by EQ-0010 (structural intelligence) and EQ-0011 (semantic boundary)

### BOQRow Fields

| Field | Type | Description | Source EQ |
|-------|------|-------------|-----------|
| `row_type` | Enum | ITEM, SECTION_HEADER, BLANK, SUBTOTAL, etc. | EQ-0007, EQ-0010 |
| `row_number` | int | Sequential row index within workbook | EQ-0007 |
| `code` | str | Item code (e.g., trade code, reference number) | EQ-0007 |
| `description` | str | Full item description text | EQ-0007 |
| `quantity` | float | Numeric quantity value | EQ-0007 |
| `uom` | str | Unit of Measure (e.g., m, m2, m3, nr, hr) | EQ-0007, EQ-0010 |
| `rate` | float | Unit rate (price per UOM) | EQ-0007 |
| `amount` | float | quantity × rate | EQ-0007 |
| `section_context` | str | Section/subsection label the row belongs to | EQ-0010 |

### Row Types
- **ITEM**: Measureable work item with quantity, UOM, rate, amount
- **SECTION_HEADER**: Grouping label (e.g., "Excavation", "Concrete Works")
- **BLANK**: Empty separator row
- **SUBTOTAL**: Aggregation row within a section
- Additional types classified in EQ-0010 capability matrix

### Hierarchy
```
Workbook → Sections → Sub-sections → ITEM rows
```
Section headers indicate hierarchy boundaries. Parent-child relationships are derivable from row sequence and section context (EQ-0010 Spike 3).

---

## Evidence vs Assessment (CRITICAL BOUNDARY)

**Source**: EQ-0011, ADR-0025. This is the foundational engineering boundary for all BOQ capabilities.

| Category | Definition | Examples | Provider |
|----------|-----------|----------|----------|
| **Evidence** | Objectively observable in data | Row type, quantity value, UOM string, sign (positive/negative), code presence, section context | **Jarvis** (deterministic extraction) |
| **Assessment** | Requires domain judgment | Trade classification, item categorization, measurement compliance, "reasonable rate" evaluation | **Human QS** (domain expertise) |

**Engineering Rule**: Jarvis provides evidence; humans make assessments. Never cross this boundary in platform code.

This boundary is frozen by ADR-0025 and EQ-0011 Gate 3.

---

## Domain Concepts & Verification Status

| Concept | Document | Verification | Key Knowledge |
|---------|----------|--------------|---------------|
| **BOQ Structure** | `02_BOQ_Structure.md` | **Evidence-Backed** (FROZEN) | Row types, fields, hierarchy, section context |
| **Omission/Addition** | `04_Omission_Addition.md` | **Evidence-Backed** (FROZEN) | Sign conventions: positive=addition, negative=omission. Validated by EQ-0002. |
| **UOM Standards** | `05_UOM_Standards.md` | Partially Verified | Common UOMs (m, m2, m3, nr, hr, kg, t, ls) confirmed by EQ-0010 Spike 2. Edge cases and non-standard UOMs need Project Owner review. |
| **Trade Schedule** | `03_Trade_Schedule.md` | **AGP** — Needs Review | Classification system for work types. Partially referenced by EQ-0011. |
| **Naming Conventions** | `06_Naming_Convention.md` | **AGP** — Needs Review | Item description standards. Patterns observed in data but formal conventions not verified. |
| **QS Office Standards** | `01_QS_Office_Standards.md` | **AGP** — Needs Review | Office-specific practices. |
| **Client Conventions** | `07_Client_Conventions.md` | **AGP** — Needs Review | Client-specific requirements. |
| **Checking Workflow** | `08_Checking_Workflow.md` | **AGP** — Needs Review | Human QA process for BOQ review. |
| **Dimension Groups** | `09_Dimension_Group_Guide.md` | **AGP** — Needs Review | Measurement category groupings. |
| **Drawing Organization** | `10_Drawing_Organization.md` | **AGP** — Needs Review | Drawing management conventions. |
| **Glossary** | `glossary.md` | Partially Verified | Domain terminology. Some terms confirmed by EQ-0011 Spike 1. |
| **Domain Layer Review** | `DOMAIN_LAYER_V1_1_REVIEW.md` | **Evidence-Backed** | Reconciliation of AI-generated docs with EQ evidence. |

---

## Frozen Domain Knowledge

Only 2 documents are frozen and safe for engineering use:

1. **`02_BOQ_Structure.md`** — BOQ row structure, types, fields, hierarchy
2. **`04_Omission_Addition.md`** — Sign conventions for additions and omissions

All other domain documents require Project Owner verification before use in engineering decisions.

---

## Verification Summary

| Status | Count | % |
|--------|-------|---|
| Evidence-Backed (Frozen) | 2 | 15% |
| Partially Verified | 2 | 15% |
| Pending Project Owner Verification | 9 | 69% |

**Critical Finding**: 69% of domain knowledge is AI-generated and unverified. Future capabilities requiring domain knowledge (trade classification, measurement validation, naming enforcement) should NOT proceed until relevant domain documents are verified by the Project Owner.

---

## Recommendations

1. **Before implementing trade-aware capabilities**: Verify `03_Trade_Schedule.md`
2. **Before implementing UOM validation**: Complete verification of `05_UOM_Standards.md`
3. **Before implementing description parsing**: Verify `06_Naming_Convention.md`
4. **Before implementing QA capability**: Verify `08_Checking_Workflow.md`
5. **Establish Domain Freeze process**: Domain documents must be verified and frozen before dependent capability implementation begins

---

## Dependencies

```
Domain Docs → EQ Evidence (EQ-0010, EQ-0011) → Frozen Domain Knowledge → Capabilities
```

---

## References

- `docs/domain/` — All 13 domain documents
- `docs/domain/DOMAIN_LAYER_V1_1_REVIEW.md` — Domain reconciliation review
- EQ-0010 evidence reports (Spikes 1-5) — Structural intelligence
- EQ-0011 evidence reports (Spikes 1-5) — Semantic boundary
- ADR-0025 — Observation vs Assessment
- `docs/knowledge/Appendices/C_Domain_Verification_Matrix.md` — Per-document verification matrix

---

## Verification Status

| Source | Status |
|--------|--------|
| `02_BOQ_Structure.md` | **Evidence-Backed** (FROZEN) |
| `04_Omission_Addition.md` | **Evidence-Backed** (FROZEN) |
| EQ-0010, EQ-0011 evidence | **Evidence-Backed** (spike tools + verification audits) |
| Remaining domain docs (9) | **AI-Generated, Pending Project Owner Verification** |

---

**Generated**: 2026-07-15 | **Part of**: Jarvis Knowledge Consolidation