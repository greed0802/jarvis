# CheckMate Reporting Architecture

## EQ-0021 — CheckMate Application Architecture

### Spike 5 — Reporting Architecture

**Status:** Complete (Amended — reports consume Presentation Model)
**Date:** 2026-07-25
**Amended:** 2026-07-25
**Authority:** EQ-0021 Spike 5

---

## 1. Purpose

Define the structure of CheckMate-generated reports. Reports MUST consume the Presentation Model and MUST NOT interpret evidence directly.

---

## 2. Critical Architecture Rule

**Reports consume Presentation Model. They do NOT interpret evidence.**

- Interpretation happens ONCE in the Interpretation layer
- Presentation Model is the sole data source for reports
- Reports serialize Presentation Model content
- Reports never access BOQIntelligenceResult or ValidationFindings directly
- Reports never compute severity, grouping, or recommendations

---

## 3. Report Structure

Every CheckMate report contains:

| Section | Source from Presentation Model | Content |
|---------|-------------------------------|---------|
| Executive Summary | PresentationSummary | Workbook overview, key stats, critical findings |
| Detailed Findings | PresentationFinding[] | Grouped, sorted, with review status |
| Section Reports | PresentationSection[] | Per-section analysis, statistics |
| Hierarchy | PresentationSection[] | Level distribution, WBS tree |
| Statistics | PresentationStatistics | Row counts, classification, UOM distribution |

---

## 4. Report Content Inventory

Each section rendered from the Presentation Model:

| Report Section | Model Source | Format |
|---------------|-------------|--------|
| Executive Summary → Stats | PresentationStatistics | Counts table |
| Executive Summary → SQL | PresentationSummary | Text |
| Findings → Categories | PresentationFinding.category | Grouped list |
| Findings → Detail | PresentationFinding | Finding detail with evidence ref |
| Section Reports | PresentationSection | Per-section table |
| Hierarchy | PresentationSection.level_info | WBS tree |
| Statistics | PresentationStatistics | Distribution tables |

---

## 5. Export Formats (unchanged)

| Format | Use Case |
|--------|----------|
| PDF | Final report |
| CSV | Integration data |
| JSON | External consumption |
| Text | Plaintext summary |

---

## 6. Export Process (Updated)

```
Presentation Model (immutable)
        ↓
    Structured Report assembles from Model
        ↓
    Format converter renders (PDF / CSP / JSON)
        ↓
    Export gating: all HIGH findings reviewed
        ↓
    File written
```

---

## 7. Reporting Principles

1. Reports are deterministic — reproducible from same Presentation Model
2. Reports use only Presentation Model data
3. Reports never reinterpret evidence
4. Reports include review state annotations
5. Export blocked until HIGH findings reviewed

---

## 8. Document Control

| Property | Value |
|----------|-------|
| Document ID | EQ-0021-S5 |
| Engineering Question | EQ-0021 |
| Spike | 5 |
| Status | Complete (Amended) |
| Date | 2026-07-25 |
| Amendments | Reports consume Presentation Model not raw evidence |
| Authority | EQ-0021 |