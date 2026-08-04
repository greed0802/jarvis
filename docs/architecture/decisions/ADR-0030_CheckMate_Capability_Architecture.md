# ADR-0030: CheckMate Capability Architecture

**Status:** FROZEN
**Date:** 2026-07-29
**Frozen Date:** 2026-07-29
**Authors:** Capability Workstream
**Prerequisites:** ADR-0027, ADR-0028, ADR-0029, EQ-0024 (FROZEN)
**Source Review:** `docs/architecture/reviews/EQ-0024_Project_Owner_Review.md`

---

## Context

EQ-0024 established the CheckMate capability as a deterministic compliance
and validation engine operating as a consumer layer above BOQ Intelligence.
This ADR codifies the capability boundary, domain taxonomy, and vertical
slice specification from the frozen EQ-0024 discovery.

---

## Decision

### Invariant 1 — Evidence Primacy (C1.1)

CheckMate SHALL consume BOQ Intelligence evidence exclusively and SHALL NOT
independently parse, reconstruct, or re-evaluate underlying workbook or
tabular semantics.

**Rationale:** BOQ Intelligence is the sole upstream evidence authority.
CheckMate operates on structured, parsed evidence artifacts. Duplicating
parser logic would violate the consumer boundary and introduce
non-deterministic interpretation paths.

### Invariant 2 — Scope Boundary (C1.3)

CheckMate SHALL NOT generate summaries, construct conversational context,
render reports, or perform any function outside rule evaluation and finding
generation.

**Rationale:** Summarization belongs to Project Understanding, draft
synthesis to AI Assistant, and layout rendering to Formatter. CheckMate's
scope is strictly limited to deterministic rule evaluation against
immutable evidence.

### Invariant 3 — Domain Rule Taxonomy (C1.8)

All CheckMate rules SHALL be classified into one of 6 canonical domain
categories:

| Domain | Category | Min Evidence |
|--------|----------|-------------|
| MEASUREMENT | Quantity Validation | STRUCTURAL |
| SPECIFICATION | Conformance Check | STRUCTURAL |
| COORDINATION | Cross-Reference Check | AGGREGATE |
| COMPLIANCE | Standards Adherence | STRUCTURAL |
| DOCUMENTATION_INTEGRITY | Data Quality | ATOMIC |
| PROJECT_POLICY | Client/Project Policy | DERIVED |

**Rationale:** These categories reflect professional QS review practice
rather than software mechanics. Each rule declares its domain category at
registration, enabling domain-level coverage reporting in the
FindingReport.

### Invariant 4 — Vertical Slice Specification Completeness (C1.16)

The vertical slice SHALL exercise all 16 invariants through at minimum 5
representative rules across at least 4 domain categories, demonstrating
PASS, FAIL, and UNEVALUABLE_MISSING_EVIDENCE outcomes in a single
FindingReport.

**Rationale:** The vertical slice validates capability specification
readiness for Project Owner review before M10 implementation begins. It
proves that the architecture is internally consistent and executable.

---

## Non-Goals (Delegated to M10 Product Workbench)

| Concern | Delegated To |
|---------|-------------|
| UI framework selection (React, Tauri, etc.) | M10 Product Workbench |
| PDF rendering or document display | M10 Product Workbench |
| Prompt engineering for AI Assistant | M10 Product Workbench |
| LLM provider bindings or model selection | M10 Product Workbench |
| Report layout or formatting | Formatter capability |

---

## Consequences

- CheckMate is permanently bounded as a consumer layer above BOQ Intelligence.
- All 6 domain categories are canonical; new categories require ADR amendment.
- The vertical slice specification serves as the M10 readiness gate.
- Downstream capabilities (Project Understanding, AI Assistant, Formatter)
  own their respective concerns with no overlap into CheckMate.

---

## Related Capability ADRs

- **ADR-0031**: Defines the `FindingReport` and public capability contract.
- **ADR-0032**: Defines the `RuleSnapshot`, rule model, and evidence contract.

---

## Freeze Record

| Field | Value |
|-------|-------|
| **Frozen Date** | 2026-07-29 |
| **PO-DEC Reference** | `docs/architecture/reviews/EQ-0024_Project_Owner_Review.md` |
