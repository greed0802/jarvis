# Engineering Questions

## Introduction

Engineering Questions are the primary mechanism by which Jarvis acquires validated engineering knowledge. Architecture should be informed by validated engineering evidence whenever possible, while remaining governed by the Vision, Principles, and accepted ADRs.

This document records engineering knowledge only. It does **not** define architecture, planning, or milestones. Engineering questions arise from implementation spikes, discovery exercises, and codebase observations. Each question captures what was asked, what was found, and what remains unknown. Engineering questions may later produce Architecture Decisions (ADRs), but this document records engineering evidence rather than architectural decisions. Entries are updated only when new engineering evidence becomes available. Architectural discussion alone does not modify this document.

Questions are organized into five categories:

- **Answered** — Sufficient evidence exists to close the question.
- **Evidence Complete — Pending Project Owner Disposition** — Engineering investigation is complete. The evidence report has been published. Formal disposition by the Project Owner is required before the question may transition to Answered or another governance state.
- **Active** — Investigation is underway or pending, with partial evidence.
- **Candidate** — Proposed Engineering Question requiring additional engineering fixtures before investigation may begin.
- **Parked** — No current investigation priority; may be revisited.

---

## Engineering Question Workflow

The following workflow governs how engineering knowledge is acquired and organized:

```
Vision
    │
    ▼
Research Backlog
    │
    ▼
Engineering Question
    │
    ▼
Engineering Spike
    │
    ▼
Engineering Evidence
    │
    ▼
Engineering Disposition
    │
    ▼
Project Owner Decision
    │
    ▼
Repository Acceptance
```

Knowledge organization is earned through repeated engineering evidence. It is never the starting point.

---

## Answered

### EQ-0001: Can Jarvis deterministically identify BOQ row types?

| Field | Value |
|-------|-------|
| **Status** | ANSWERED |
| **Scope** | Engineering Spike #1 — `tools/boq_row_analysis.py` against `full_boq.xlsx` |
| **Evidence** | Spike #1 demonstrated deterministic row classification using observed semantic markers (UOM values and section markers in Column D). A temporary identifier-format fallback was used during the spike but was later determined not to be semantically significant. Runtime < 1 second for 6,354 rows. 3.0% of rows fell into "Other". |
| **Additional Evidence** | Office standard document `docs/reference/office_standards/12_Units of Measurements.docx` independently documents the UOM convention (m, m2, m3, no, t, Item, Note, noidc, endh1). This matches Spike #1's empirically observed UOM values, confirming that UOM-based classification is a documented office convention, not an inference from a single file. |
| **Answer** | Yes. Deterministic row identification is possible using semantic markers. Row classification is determined primarily by UOM values and section markers. Item identifiers are opaque identifiers and should not be used as semantic classifiers. The key engineering discovery — that Column A is an identifier, not a classifier — prevents future reintroduction of identifier-syntax heuristics. |
| **Remaining Unknowns** | (1) Column positions validated against only one file format. (2) Whether the Head1-5, Note, noidc marker set is complete across CostX exports. (3) Whether the "Other" classification rate changes significantly on a different workbook. |
| **Owner** | — |
| **Engineering Discovery** | Column A is an opaque identifier, not a semantic classifier. The temporary slash heuristic (`'/' in identifier and length > 2`) used during the spike was a disposable investigation aid only. Future production implementations shall classify BOQ rows using semantic information (UOM markers, section markers, etc.), not identifier syntax. The "item" lowercase variant is a documented data-entry inconsistency in the fixture, not a distinct engineering convention. |

### EQ-0002: Can Jarvis deterministically validate the OMISSION/ADDITION sign convention?

| Field | Value |
|-------|-------|
| **Status** | ANSWERED |
| **Scope** | Engineering Spike #1 — `tools/boq_row_analysis.py` against `full_boq.xlsx` |
| **Evidence** | Section boundaries detected via UOM='noidc' + Description='OMISSION/ADDITION'. Section state tracked with a single variable. OMISSION section: 169 negative quantities, 7 positive (anomalies). ADDITION section: 0 negative, 3 positive (correct). |
| **Answer** | Yes. Deterministic sign convention validation is possible using section-aware logic. The mechanism is proven: section boundaries are observable, section state is trackable, and sign validity is deterministically assessable per row given its section context. The remaining uncertainty is not about the mechanism — it is about domain interpretation of the 7 anomalous rows. That question is represented by EQ-0006. |
| **Remaining Unknowns** | (1) Whether the OMISSION/ADDITION marker convention (UOM='noidc' + Description label) is consistent across CostX export types. |
| **Owner** | — |
| **Engineering Discovery** | Sign validation cannot be performed as an isolated row property. It requires contextual section state derived from preceding section markers. Section state is observable. |
| **Related Questions** | EQ-0006 — Domain interpretation of the 7 positive-quantity OMISSION items |

### EQ-0003: What are the structural characteristics and observable patterns across multiple CostX export formats?

| Field | Value |
|-------|-------|
| **Status** | ANSWERED |
| **Scope** | Engineering Discovery — `tools/workbook_inspector.py` against three reference workbooks (`full_boq.xlsx`, `formula_workbook.xlsx`, `dimensions_export.xlsx`) |
| **Evidence** | Documented in `docs/reference/M5_CostX_Export_Analysis.md`. Full structural analysis of 3 workbooks: single-sheet BOQ (6,354 rows), formula workbook (543 rows), and multi-sheet dimensions export (90 sheets, ~3,500–4,200 rows each). Observations include column layouts, formula patterns, calculation modes, named ranges, and data type distributions. |
| **Answer** | The three observed workbook types exhibit distinct structural patterns. The current deterministic parser specification is specific to the `full_boq.xlsx` export. Additional formats will require independent engineering evaluation before determining whether they can share a parser implementation. The `dimensions_export.xlsx` format introduces significant complexity (90 sheets, 40 columns, merged cells, varied data types). |
| **Remaining Unknowns** | (1) Whether additional CostX export formats exist beyond these three. (2) How export configuration affects output structure. (3) Whether column layout varies across CostX versions. |
| **Owner** | — |

### EQ-0004: Should the Observation Runtime be adopted as the active production architecture for CostX acquisition?

| Field | Value |
|-------|-------|
| **Status** | ANSWERED |
| **Scope** | Architecture evaluation — ADR-0025 |
| **Evidence** | Engineering Spike #1 (BOQ Row Analysis) demonstrated that ~80 lines of flat script sufficed for complete BOQ row classification and sign validation. No runtime abstractions were naturally produced by the spike. ADR-0025 formally evaluated and rejected the Observation Runtime as the active production architecture. |
| **Answer** | No. The Observation Runtime is not adopted. The supported production acquisition path remains the minimal deterministic parser established by the accepted architecture. The existing Observation implementation and documentation are retained as historical engineering artifacts. |
| **Remaining Unknowns** | Future multi-format or multi-source validation will require re-evaluation of the runtime architecture. This is explicitly noted in ADR-0025 as a future concern, not a current gap. |
| **Owner** | — |

### EQ-0006: Do the 7 positive-quantity OMISSION items in `full_boq.xlsx` represent data entry errors, convention differences, or legitimate business exceptions?

| Field | Value |
|-------|-------|
| **Status** | ANSWERED |
| **Scope** | Domain-level sign convention investigation — Requires domain expert review of rows 6202, 6343–6348 in `full_boq.xlsx` |
| **Evidence** | Spike analysis (EQ-0002) identified 7 rows in the OMISSION section with positive quantities where negative quantities are expected. The anomaly is reproducible. QS review confirmed that rows 6202 and 6343–6348 are data-entry errors rather than legitimate business exceptions or convention differences. |
| **Answer** | The observed anomalies represent data-entry errors. The deterministic validation mechanism remains unchanged. The historical `full_boq.xlsx` fixture is intentionally preserved unchanged in accordance with `Engineering_Fixtures.md`. |
| **Remaining Unknowns** | — |
| **Owner** | QS (Quantity Surveyor) |
| **Clarification** | This question addresses domain interpretation only. The validation mechanism itself is proven and answered by EQ-0002. The fixture remains unchanged as historical evidence. |

### EQ-0007: What is the minimum deterministic production implementation that transforms a validated CostX BOQ workbook into structured BOQ rows while preserving the simplicity demonstrated by Engineering Spike #1?

| Field | Value |
|-------|-------|
| **Status** | ANSWERED |
| **Scope** | Minimum production BOQ extraction — `full_boq.xlsx` fixture. No generalization. No Cubit. No multiple workbook formats. (EQ-0005 remains responsible for future generalization.) |
| **Evidence** | EQ-0001 (deterministic BOQ row identification), EQ-0002 (deterministic sign convention validation), Engineering Spike #1 (`tools/boq_row_analysis.py`), and ADR-0025 (Observation Runtime rejected — minimal deterministic parser is the supported path). See `docs/reference/EQ_0007_Production_Extraction_Report.md` for full verification details. |
| **Answer** | Implementation verified: `src/jarvis/parsers/costx/boq_extraction.py` produces deterministic `BOQRow` objects using UOM-based classification (EQ-0001) and section-aware extraction (EQ-0002). Verified against `full_boq.xlsx`: 6,349 rows extracted, classification counts Item 3605 / Other 198 / Head 2011 / Note 520 / Section 15, the 7 known OMISSION anomalies reproduced exactly. Reconciliation with Spike #1's original figures (Item 3615 / Other 188) documented — the difference is due to Spike #1's now-retired identifier-syntax fallback (EQ-0001). 10 committed regression tests in `tests/parser/test_boq_extraction.py`, all passing. |
| **Remaining Unknowns** | — |
| **Owner** | Cline |
| **Engineering Constraints** | Reuse the existing workbook loader. Column A is an opaque identifier. Row classification is driven by semantic markers. Section-aware validation remains deterministic. No runtime abstractions unless implementation demonstrates necessity. |

---

## Evidence Complete — Pending Project Owner Disposition

### EQ-0005: Can the observed BOQ semantics be generalized across additional CostX exports?

| Field | Value |
|-------|-------|
| **Status** | EVIDENCE COMPLETE — PENDING PROJECT OWNER DISPOSITION |
| **Scope** | Row classification semantic generalization across CostX BOQ exports |
| **Evidence** | Investigation completed. See `docs/reference/EQ_0005_CostX_Export_Generalization_Report.md` for full report. Two fixtures analyzed: `full_boq.xlsx` and `Structural Reinforcement Only.xlsx`. |
| **Answer** | UOM-based classification semantics are supported across the two observed CostX BOQ exports. Structural assumptions (worksheet name, header position, first data row) are falsified — current fixed-row assumptions are unsupported. The core UOM-based classification logic is semantically sound and can be reused, but header/discovery logic requires independent engineering. No generalization is justified yet — two fixtures provide directional evidence but do not meet the Rule of Three. |
| **Open Evidence** | (Q1) Multi-sheet BOQ exports — do they exist? Requires additional fixture. (Q2) Header layout variants — what header row positions exist beyond Row 3 and Row 4? Requires 2+ additional fixtures. (Q3) UOM vocabulary completeness — are there markers beyond the current set? Requires additional fixture with different trade/discipline. (Q4) Localized CostX exports — do non-Australian CostX exports use different conventions? Requires localized fixtures. (Q5) CostX version impact — do different CostX versions produce different export structures? Requires version-dated fixtures. (Q6) Custom report templates — does CostX template customization affect column layout? Requires template-variant fixtures. (Q7) Deterministic header detection — can header row be found algorithmically without hardcoded position? Requires 3+ structurally different fixtures. |
| **Owner** | — |
| **Recommendation** | Maintain intentionally narrow production parser. Recommend Project Owner consider activating candidate EQ-0008 for deterministic worksheet/header discovery when sufficient additional fixtures become available. |
| **Evidence Report** | `docs/reference/EQ_0005_CostX_Export_Generalization_Report.md` |

---

## Active

*No active Engineering Questions at this time.*

---

## Candidate Engineering Questions

### EQ-0008: Can the worksheet structure (worksheet name, header row, first data row, column assignment) be determined deterministically across CostX BOQ exports?

| Field | Value |
|-------|-------|
| **Status** | CANDIDATE |
| **Scope** | Deterministic worksheet/header discovery across CostX BOQ exports |
| **Purpose** | Investigate whether worksheet structure (worksheet name, header row position, first data row position, column assignment) can be determined algorithmically without hardcoded positions. |
| **Prerequisites** | Requires additional engineering fixtures before investigation may begin. Current evidence (2 fixtures) provides directional evidence but does not meet the **Rule of Three** (need 3+ independent fixtures to justify generalization). |
| **Required Evidence** | (1) At least one additional fixture with structural variation. (2) Engineering investigation of header detection heuristics. (3) Investigation of whether metadata columns can be used for structural detection. |
| **Source** | Recommended by EQ-0005 Engineering Investigation Report (Section 5 — Parser Recommendation, Option A) |
| **Owner** | — |

---

## Summary

| ID | Status | Scope |
|----|--------|-------|
| EQ-0001 | ANSWERED | BOQ row identification |
| EQ-0002 | ANSWERED | OMISSION/ADDITION sign convention (mechanism) |
| EQ-0003 | ANSWERED | CostX export format characteristics |
| EQ-0004 | ANSWERED | Observation Runtime architecture (ADR-0025) |
| EQ-0005 | EVIDENCE COMPLETE — PENDING PROJECT OWNER DISPOSITION | BOQ semantic generalization |
| EQ-0006 | ANSWERED | OMISSION positive-quantity anomalies (domain interpretation) |
| EQ-0007 | ANSWERED | Minimum deterministic production BOQ extraction |
| EQ-0008 | CANDIDATE | Deterministic worksheet/header discovery across CostX BOQ exports |

---

## Engineering Governance Reminder

Carry forward the governance established during M6.

**Do not introduce:**
- ontologies
- taxonomies
- runtime abstractions
- generalized models

until engineering evidence demonstrates they are required.

**Evidence precedes organization.**
**Organization precedes architecture.**
**Architecture precedes implementation.**

---

## Repository Status

Current architectural state:

- ✅ Engineering Spike #1 completed
- ✅ ADR-0025 completed
- ✅ Observation Runtime rejected for current CostX acquisition scope
- ✅ Engineering Questions introduced
- ✅ Professional_Research_Backlog.md established
- ✅ M6 Observation Runtime documentation replaced with an explicitly labeled retrospective summary
- ✅ **EQ-0006 closed — QS-confirmed data-entry errors (rows 6202, 6343–6348), historical `full_boq.xlsx` fixture preserved unchanged per `Engineering_Fixtures.md`**
- ✅ **EQ-0007 closed — production BOQ extraction (`boq_extraction.py`) verified against `full_boq.xlsx`; 10 committed regression tests passing**
- ✅ **EQ-0005 evidence complete — generalization report published, pending Project Owner disposition**
- ✅ **EQ-0008 registered as Candidate — requires additional engineering fixtures before investigation**

---

## Next Phase

The next Engineering Question will be selected deliberately after architectural review. The Research Backlog records candidate domains only; it does not prescribe the next investigation.