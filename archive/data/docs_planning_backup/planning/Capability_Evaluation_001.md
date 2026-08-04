# Capability Evaluation 001

Date: 2026-07-13
Status: Complete — Project Owner Decision Recorded
Reference: `docs/planning/Capability_Discovery_001.md`

---

## Purpose

This document records the first formal Capability Evaluation under the Capability Era governance process.

Each candidate identified in Capability Discovery 001 is evaluated against the four criteria defined in `docs/planning/Capability_Roadmap.md`:

1. User Value
2. Engineering Effort
3. Evidence Readiness
4. Architectural Impact

---

## Evaluation Criteria (from Capability Roadmap)

| Criterion | Question |
|-----------|----------|
| **User Value** | Does this capability provide direct, tangible value to professional users? |
| **Engineering Effort** | Can this capability be implemented with minimal code and no speculative features? |
| **Evidence Readiness** | Do answered Engineering Questions or documented standards provide sufficient evidence to implement without a spike? |
| **Architectural Impact** | Can this capability be implemented without introducing new engines, frameworks, runtime components, or ADRs? |

### Evaluation Principles

- Prefer capabilities that require zero architectural expansion.
- Prefer capabilities built entirely from existing evidence.
- Prefer capabilities that compose with existing production types.
- A capability that requires architectural expansion is not disqualified — it simply requires stronger justification.

---

## Candidate Evaluations

### 1. BOQ Intelligence

| Criterion | Rating | Justification |
|-----------|:------:|---------------|
| **User Value** | **High** | Directly transforms raw extraction into validated, analyzed, and exportable data. Addresses the gap between "the parser runs" and "the QS can use the output." Every feature maps to a concrete professional workflow need. |
| **Engineering Effort** | **Low** | Pure functions over `list[BOQRow]`. No new types, no runtime components, no parser modifications. Each feature is independently implementable and testable. Estimated scope: ~300-500 lines of production code + regression tests. |
| **Evidence Readiness** | **High** | All engineering-derived rules trace to answered EQs (EQ-0001, EQ-0002, EQ-0006, EQ-0007). Domain rules trace to documented office standards (`12_Units of Measurements.docx`). No spike required. No evidence gaps. |
| **Architectural Impact** | **None** | No new engines, frameworks, runtime components, interfaces, protocols, or ADRs. Composes entirely with existing production types (`BOQRow`, `list[BOQRow]`). |

**Overall Assessment:** The strongest candidate by every criterion. Evidence is complete, effort is minimal, value is direct, and architectural impact is zero.

**Risk:** None identified. The only risk is scope creep — the feature list is large and should be delivered incrementally.

---

### 2. Formatter

| Criterion | Rating | Justification |
|-----------|:------:|---------------|
| **User Value** | **Medium** | Export functionality is useful, but export without validation produces untrusted output. The value is contingent on BOQ Intelligence being complete first. |
| **Engineering Effort** | **Low** | Formatting is a presentation concern. CSV and JSON export over `list[BOQRow]` is straightforward. |
| **Evidence Readiness** | **Medium** | No engineering questions are needed for formatting itself. However, the question of *what* to export (which fields, which validations to include in the output) depends on BOQ Intelligence being defined first. |
| **Architectural Impact** | **None** | Pure formatting functions. No architectural expansion. |

**Overall Assessment:** A distinct product capability. Users experience "formatting my BOQ" as a separate intent from "validating my BOQ" or "analyzing my BOQ." Internally, Formatter may share implementation with BOQ Intelligence, but the capability boundary is defined by user intent, not code organization.

**Dependency:** BOQ Intelligence (validation should precede export to ensure exported data is trusted).

---

### 3. CheckMate

| Criterion | Rating | Justification |
|-----------|:------:|---------------|
| **User Value** | **High** | Professional QA checking is critical for QS work. Detecting data-entry errors, missing data, and duplicates directly supports the professional workflow. |
| **Engineering Effort** | **Medium** | Requires a formal domain rule catalog. Each rule must be defined, documented, and traced to its authority (office standard, QS convention, professional standard). The rules themselves are simple; the governance overhead is the effort. |
| **Evidence Readiness** | **Medium** | Domain rules exist in office standards documents but have not been formally cataloged as a rule set. The rules are known (duplicate codes, missing descriptions, invalid UOMs) but require explicit enumeration and QS authority sign-off. |
| **Architectural Impact** | **None** | Pure functions over `list[BOQRow]`. No architectural expansion. |

**Overall Assessment:** A distinct product capability with significant future scope. Today, CheckMate's initial features overlap with BOQ Intelligence's domain rule features. But CheckMate's trajectory leads to project QA, drawing QA, specification QA, cross-workbook QA, rule packs, and company QA policies — all clearly beyond BOQ Intelligence's scope.

**Dependency:** BOQ Intelligence baseline (the validation rules established by BOQ Intelligence form the foundation for CheckMate's rule catalog).

---

### 4. Cubit Parser

| Criterion | Rating | Justification |
|-----------|:------:|---------------|
| **User Value** | **Medium** | Expands the platform to a second estimating platform. Useful if the user's workflow involves Cubit. However, no Cubit fixtures exist and no investigation has been completed. |
| **Engineering Effort** | **Medium** | Similar in structure to the CostX parser but with a different export format. Requires an Engineering Question to investigate Cubit export structure before implementation can begin. |
| **Evidence Readiness** | **Low** | No Cubit fixtures available. No engineering investigation completed. No evidence about Cubit export structure, column layout, or semantic markers. |
| **Architectural Impact** | **None** | A second parser would be a peer to the CostX parser. No architectural expansion required at the parser level. However, if cross-parser analysis becomes necessary, it may eventually trigger Phase 4 (Cross-Source Intelligence) of the Capability Roadmap. |

**Overall Assessment:** Valid candidate but not ready for implementation. Requires fixtures and an Engineering Question before evidence readiness can improve.

**Dependency:** Cubit export fixtures from Project Owner; Engineering Question to investigate Cubit export structure.

---

### 5. PDF Parser

| Criterion | Rating | Justification |
|-----------|:------:|---------------|
| **User Value** | **Low** | PDF extraction is useful in theory but PDF documents vary enormously in structure. The value is low because the engineering cost is high relative to the reliability of the output. |
| **Engineering Effort** | **High** | PDF parsing requires significant engineering — table extraction, layout analysis, handling of scanned documents, font variations, merged cells. This is fundamentally different from structured workbook extraction. |
| **Evidence Readiness** | **Very Low** | No PDF fixtures available. No engineering investigation completed. No evidence about PDF structure or extraction feasibility. |
| **Architectural Impact** | **None** | A PDF parser would be a peer to the CostX parser. No architectural expansion required at the parser level. |

**Overall Assessment:** The weakest candidate. High effort, very low evidence, low value relative to cost. PDF extraction is a fundamentally different engineering problem from workbook extraction.

---

### 6. AI-Assisted Estimation

| Criterion | Rating | Justification |
|-----------|:------:|---------------|
| **User Value** | **High** | AI-assisted estimation is a strategic capability. If achieved, it differentiates the platform significantly. |
| **Engineering Effort** | **High** | Requires AI integration, training data, validation framework, and potentially new architectural components (Context Engine, Knowledge Framework). |
| **Evidence Readiness** | **Very Low** | No AI integration exists. No training data available. Context Engine architecture exists but has no production evidence (EQ-0009 confirmed extraction is not Context assembly). No foundation for AI-assisted estimation. |
| **Architectural Impact** | **Potentially significant** | May require Context Engine implementation, Knowledge Framework, AI integration layer, and validation mechanisms that go beyond the current architecture. |

**Overall Assessment:** High strategic value but completely unready for implementation. Multiple foundational capabilities must exist first (BOQ Intelligence at minimum, likely Context Engine and Knowledge Framework). This is a long-term capability, not a near-term candidate.

**Dependency:** BOQ Intelligence, Context Engine production evidence, training data, AI integration framework.

---

## Capability Relationships

The evaluation reveals dependency relationships between capabilities. These relationships are product-level, not implementation-level. Capabilities may share implementation code while remaining distinct product capabilities.

```
BOQ Intelligence
        │
        ├── prerequisite for ──▶ Formatter
        │
        ├── baseline for ──▶ CheckMate
        │
        └── foundation for ──▶ AI-Assisted Estimation

Cubit Parser
        │
        └── peer of ──▶ CostX Parser (future cross-source analysis)

PDF Parser
        │
        └── independent (no current dependencies)
```

### Relationship Definitions

| Relationship | Meaning |
|--------------|---------|
| **Prerequisite for** | The upstream capability must be substantially complete before the downstream capability delivers user value. Formatter without validation produces untrusted output. |
| **Baseline for** | The upstream capability establishes rules, patterns, or data structures that the downstream capability extends. CheckMate extends BOQ Intelligence's domain rules into a configurable QA platform. |
| **Foundation for** | The upstream capability is one of several prerequisites for the downstream capability. AI-Assisted Estimation requires BOQ Intelligence plus Context Engine plus training data. |
| **Peer of** | The capabilities are structurally similar and may share patterns but serve different data sources. |

### Implementation Sharing

Capabilities may share implementation code. For example:

- BOQ Intelligence may contain the initial implementation of duplicate detection and CSV export.
- Formatter may later extract and extend the export functionality into a dedicated formatting capability.
- CheckMate may later extract and extend the validation rules into a configurable rule engine.

Implementation sharing is an engineering decision. Capability boundaries are a product decision. They are independent concerns.

---

## Evaluation Summary

| Candidate | User Value | Effort | Evidence Ready | Arch. Impact | Composite |
|-----------|:----------:|:------:|:--------------:|:------------:|:---------:|
| **BOQ Intelligence** | High | Low | High | None | **1st** |
| **CheckMate** | High | Medium | Medium | None | **2nd** |
| **Formatter** | Medium | Low | Medium | None | **3rd** |
| **Cubit parser** | Medium | Medium | Low | None | **4th** |
| **AI-assisted estimation** | High | High | Very Low | Potentially significant | **5th** |
| **PDF parser** | Low | High | Very Low | None | **6th** |

---

## Project Owner Decision

| Candidate | Decision | Lifecycle State | Dependency |
|-----------|----------|:---------------:|------------|
| **BOQ Intelligence** | **Approved for Implementation** | Approved | None |
| **Formatter** | **Deferred** | Deferred | BOQ Intelligence (prerequisite) |
| **CheckMate** | **Deferred** | Deferred | BOQ Intelligence (baseline) |
| **Cubit Parser** | **Deferred** | Deferred | Fixtures + Engineering Question |
| **AI-Assisted Estimation** | **Deferred** | Deferred | BOQ Intelligence + Context Engine + training data |
| **PDF Parser** | **Deferred** | Deferred | None (insufficient evidence) |

### Decision Rationale

**BOQ Intelligence** is selected as the first capability. Evidence is complete, effort is minimal, value is direct, and architectural impact is zero.

**Formatter** and **CheckMate** are retained as distinct product capabilities. They are deferred because they depend on BOQ Intelligence being complete first. They are not subsumed — users experience formatting, QA checking, and intelligence as separate intents. Implementation sharing between these capabilities is permitted and expected, but the capability boundaries remain distinct.

**Cubit Parser**, **AI-Assisted Estimation**, and **PDF Parser** are deferred pending evidence, fixtures, or foundational capabilities.

---

## Next Steps

1. BOQ Intelligence transitions to **Approved for Implementation** lifecycle state.
2. Scope the first increment of BOQ Intelligence features.
3. Begin implementation under the Capability Era governance.
4. Upon BOQ Intelligence completion, revisit Formatter and CheckMate for Capability Evaluation.

---

## Document History

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-07-13 | Initial Capability Evaluation. Six candidates evaluated. BOQ Intelligence recommended. |
| 1.1 | 2026-07-13 | Project Owner amendment: Formatter and CheckMate retained as distinct product capabilities. Dependencies recorded instead of subsumption. BOQ Intelligence approved for implementation. |