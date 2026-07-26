# CheckMate Application Data Model

## EQ-0021 — CheckMate Application Architecture

### Spike 6 — Application Data Model

**Status:** Complete (Amended — Presentation Model as dedicated state)
**Date:** 2026-07-25
**Amended:** 2026-07-25
**Authority:** EQ-0021 Spike 6

---

## 1. Purpose

Define CheckMate application state. Distinguish between immutable inputs, transient state, review state, and export state. The Presentation Model is introduced as a dedicated immutable projection layer.

---

## 2. State Categories

### 2.1 Immutable Inputs (Read-Only)

| Name | Type | Source |
|------|------|--------|
| evidence | BOQIntelligenceResult | BOQ Intelligence |
| findings | ValidationFindings | Validation Engine |
| workbook_name | str | Platform |
| analysis_date | datetime | Platform |

### 2.2 Interpretation State (Transient, derived ONCE)

| State | Type | Description |
|-------|------|-------------|
| severity_map | mapping[finding_id → Severity] | HIGH/MEDIUM/LOW |
| group_map | mapping[category, list[PresentationFinding]] | Categorized findings |
| recommendation_list | list[Recommendation] | Generated during Interpretation |
| statistics | PresentationStatistics | Computed from evidence |

### 2.3 Presentation Model (Immutable, derived ONCE)

The Presentation Model is THE single deterministic projection consumed by all renderers:

| Type | Description | Consumer |
|------|-------------|----------|
| PresentationFinding | Finding with severity, category, evidence reference, row context | Presentation, Report, Export |
| PresentationSection | Section analysis with statistics | Report |
| PresentationSummary | Workbook-level overview | Dashboard |
| PresentationStatistics | Row/classification/UOM counts | Statistics page |
| PresentationRecommendation | Advisory text with severity | Review, Report |

These are:
- **Immutable** — derived once, never modified
- **Not evidence** — derived from evidence
- **Not findings** — interpreted from findings
- **Deterministic** — same inputs produce identical Model

### 2.4 Review State (Mutable, transient)

| State | Type | Description |
|-------|------|-------------|
| review_status | mapping[finding_id, ReviewStatus] | Map finding to review status |
| accepted_set | set[finding_id] | User accepted |
| rejected_set | set[finding_id] | User rejected |
| flag_set | set[finding_id] | User flagged |
| review_count | int | Count of reviewed items |

Review State is separate from Presentation Model.

### 2.5 Export State

| State | Type | Description |
|-------|------|-------------|
| export_format | str | PDF, CSV, JSON |
| export_path | str | File path |
| export_timestamp | str | ISO 8601 |
| export_ready | bool | True when all HIGH findings reviewed |

---

## 3. Application Lifecycle

```
[Platform initiates]
    ↓
1. CheckMate loads BOQIntelligenceResult + ValidationFindings
    ↓
2. INTERPRETATION layer: severity mapping, grouping, recommendations, statistics
    ↓
3. PRESENTATION MODEL ASSEMBLY: immutable projection assembled
    ↓
4. PRESENTATION layer: renders Presentation Model (CLI in v1, GUI in future)
    ↓
5. REVIEW allows human review of findings
    ↓
6. REVIEW checklist completed → EXPORT enabled
    ↓
7. EXPORT: serializes Presentation Model to PDF, JSON, CSP
    ↓
8. Application complete
```

---

## 4. State Diagram

```
┌────────┐
│  IDLE  │
└───┬────┘
    │ load inputs
┌───▼────────────┐
│ INPUT_LOADED    │ (read-only frozen dataclasses)
└───┬────────────┘
    │ interpret (severity, grouping, recs)
┌───▼────────────┐
│ INTERPRETED     │
└───┬────────────┘
    │ assemble Presentation Model
┌───▼─────────────┐
│ MODEL_ASSEMBLED │ (immutable Presentation Model created)
└───┬─────────────┘
    │ present to user
┌───▼─────────────┐
│ PRESENTING      │
└───┬─────────────┘
    │ review workflow
┌───▼─────────────┐
│ REVIEWING       │ (review state updated)
└───┬─────────────┘
    │ all HIGH reviewed
┌───▼─────────────┐
│ export-enabled  │
└───┬─────────────┘
    │ export
┌───▼─────────────┐
│ COMPLETE        │
└─────────────────┘
```

---

## 5. No Persistence

CheckMate v1 has no persistence layer.
- All state is in-memory
- Export file is the only persistent output
- No database, no file system writes except export

---

## 6. Document Control

| Property | Value |
|----------|-------|
| Document ID | EQ-0021-S6 |
| Engineering Question | EQ-0021 |
| Spike | 6 |
| Status | Complete (Amended) |
| Date | 2026-07-25 |
| Amendments | Presentation Model added as dedicated state |
| Authority | EQ-0021 |