# EQ-0021 Architecture Recommendation

## CheckMate Application Architecture — Final

### Spike 8 — Architecture Recommendation

**Status:** Complete (Amended — Presentation Model adopted, IPs reordered)
**Date:** 2026-07-25
**Amended:** 2026-07-25
**Authority:** EQ-0021

---

## 1. Recommendation

It is recommended that the Project Owner:

1. **Approve EQ-0021 as PERMANENTLY FROZEN**
2. **Authorize IP-0003: Application Foundation** — the first implementation package

### Architecture Decision

The **Presentation Model** has been adopted as the definitive architectural pattern for CheckMate. Interpretation happens ONCE in the Interpretation layer. All renderers (CLI, future GUI, Reports, Export, Formatter) consume the deterministic Presentation Model.

No architectural changes shall be made to CheckMate without a future Engineering Question.

---

## 2. Architecture Summary (Updated)

### 2.1 Application Topology

CheckMate follows a **five-layer architecture**:

```
Evidence Layer (input, read-only frozen dataclasses)
    ↓
Interpretation Layer (severity, grouping, recommendations — ONCE)
    ↓
Presentation Model (immutable, deterministic projection)
    ↓
Presentation Layer (CLI, future GUI — render only)
    ↓
Export Layer (PDF, JSON, CSV — serialize from Model)
```

### 2.2 Critical Rules

1. **Interpretation ONCE. Rendering MANY.**
2. Presentation Model is the single source of truth for all renderers
3. Presentation layer never interprets evidence
4. Reports never access raw evidence
5. Recommendations generated only in Interpretation
6. Formatter reads Presentation Model, not raw evidence
7. Builder and O&A consume Evidence Contract directly

---

## 3. Implementation Packages (Final Sequence)

| Package | Name | Purpose | Depends On |
|---------|------|---------|-----------|
| **IP-0003** | **Application Foundation** | Application skeleton: inputs, dependency wiring, lifecycle, container. No reports, no UI, no workflow, no recommendations. | Evidence Contract v1.1, Validation Contract v1 |
| IP-0004 | Interpretation Engine | Evidence consumption, severity mapping, grouping, recommendation generation, statistics. Outputs pre-Presentation Model structures. | IP-0003 |
| IP-0005 | Presentation Model | PresentationFinding, PresentationSection, PresentationSummary, PresentationStatistics. Filterable, sortable. No UI rendering. | IP-0004 |
| IP-0006 | Review Workflow | Review state, acceptance, rejection, flagging, progress tracking, export gating. | IP-0005 |
| IP-0007 | Reporting & Export | Structured report generation, PDF/JSON/CSV/Text export. Consumes Presentation Model only. | IP-0005 |

---

## 4. Future Extension Packages

| Package | Description | Depends On |
|---------|-------------|-----------|
| IP-0008 (Future) | Formatter | IP-0005 (Presentation Model) |
| IP-0009 (Future) | Builder | Evidence Contract v1.1 |
| IP-0010 (Future) | O&A Consumer | Evidence Contract v1.1 |
| IP-0011 (Future) | AI Extension | IP-0007 (export format) |

---

## 5. Implementation Sequence

```
IP-0003: Application Foundation         (shell only)
    ↓
IP-0004: Interpretation Engine          (computation)
    ↓
IP-0005: Presentation Model             (immutable projection)
    ↓
IP-0006: Review Workflow                (human review)
    ↓
IP-0007: Reporting & Export             (PDF, JSON, CSV)
```

---

## 6. Freeze Statement

After Project Owner approval, EQ-0021 becomes **PERMANENTLY FROZEN**. No further architecture changes to CheckMate without a new Engineering Question.

---

## 7. Document Control

| Property | Value |
|----------|-------|
| Document ID | EQ-0021-S8 |
| Engineering Question | EQ-0021 |
| Spike | 8 |
| Status | Complete (Frozen) |
| Date | 2026-07-25 |
| Amendments | Presentation Model adopted; IPs reorganized from 5 to 7-step sequence |
| Authority | EQ-0021 |
| Disposition | AWAITING PROJECT OWNER APPROVAL |