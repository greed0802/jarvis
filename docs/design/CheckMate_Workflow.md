# CheckMate Workflow Architecture

## EQ-0021 — CheckMate Application Architecture

### Spike 2 — Workflow Architecture

**Status:** Complete (Amended — Presentation Model stage added)
**Date:** 2026-07-25
**Amended:** 2026-07-25
**Authority:** EQ-0021 Spike 2

---

## 1. Purpose

Define the end-to-end CheckMate workflow from workbook input through evidence, validation, findings, presentation model, human review, and export.

---

## 2. Full Workflow Pipeline

```
Stage 1:  Workbook Acquisition
    ↓
Stage 2:  Evidence Generation
    ↓
Stage 3:  Evidence Validation
    ↓
Stage 4:  Evidence Interpretation
    ↓
Stage 5:  Presentation Model Assembly
    ↓
Stage 6:  Presentation
    ↓
Stage 7:  Human Review
    ↓
Stage 8:  Recommendation Formulation (applied from Model)
    ↓
Stage 9:  Report Generation
    ↓
Stage 10: Export
```

---

## 3. Stage Descriptions

### Stage 1-3: Platform-Owned (no CheckMate ownership)

CheckMate does not own Workbook Acquisition, Evidence Generation, or Validation.

### Stage 4: Evidence Interpretation

| Property | Value |
|----------|-------|
| Responsibility | CheckMate |
| Input | BOQIntelligenceResult, ValidationFindings |
| Process | Interpret evidence: severity mapping, grouping, recommendation generation, statistical analysis |
| Output | Interpreted structures (pre-Presentation Model) |
| Ownership | CheckMate OWNS — Interpretation happens ONCE here |

### Stage 5: Presentation Model Assembly

| Property | Value |
|----------|-------|
| Responsibility | CheckMate |
| Input | Output of Interpretation stage |
| Process | Assemble immutable Presentation Model (PresentationFinding[], PresentationSection[], PresentationSummary, PresentationStatistics) |
| Output | Presentation Model (immutable) |
| Ownership | CheckMate OWNS — Single deterministic projection |

### Stage 6: Presentation

| Property | Value |
|----------|-------|
| Responsibility | CheckMate |
| Input | Presentation Model (immutable) |
| Process | Render, filter, sort, navigate, review interface |
| Output | CLI output (v1), future GUI |
| Ownership | CheckMate OWNS — reads only Presentation Model |

### Stage 7: Human Review

| Property | Value |
|----------|-------|
| Responsibility | Professional Estimator + CheckMate |
| Input | Presented findings (from Presentation Model) |
| Process | User reviews, marks reviewed, accepts/rejects |
| Output | Reviewed findings (review state only) |
| Ownership | Review workflow facilitated by CheckMate |

### Stage 8: Recommendation Application

| Property | Value |
|----------|-------|
| Responsibility | CheckMate |
| Input | Reviewed findings + Presentation Model |
| Process | Apply advisory recommendations (already generated in Interpretation) |
| Output | Advisory recommendations displayed |
| Ownership | Recommendations generated during Interpretation, applied here |

### Stage 9: Report Generation

| Property | Value |
|----------|-------|
| Responsibility | CheckMate |
| Input | Presentation Model + review state |
| Process | Assemble structured report from Presentation Model |
| Output | Report document (structured) |
| Ownership | CheckMate OWNS |

### Stage 10: Export

| Property | Value |
|----------|-------|
| Responsibility | CheckMate |
| Input | Report document (from Presentation Model) |
| Process | Convert to PDF, CSV, JSON |
| Output | Export file(s) |
| Ownership | CheckMate OWNS |

---

## 4. Key Architectural Principle

**Interpretation ONCE. Rendering MANY.**

The Presentation Model is assembled exactly once. All downstream stages (Presentation, Review, Report, Export) only read the Presentation Model. No stage after Stage 5 performs evidence interpretation.

---

## 5. Human Review Points (Unchanged)

Same Review Workflow and Finding Grouping Strategy as previously defined.

---

## 6. Document Control

| Property | Value |
|----------|-------|
| Document ID | EQ-0021-S2 |
| Engineering Question | EQ-0021 |
| Spike | 2 |
| Status | Complete (Amended) |
| Date | 2026-07-25 |
| Amendments | Presentation Model Assembly inserted as Stage 5 |
| Authority | EQ-0021 |