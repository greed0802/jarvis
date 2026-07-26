# CheckMate Recommendation Policy

## EQ-0021 — CheckMate Application Architecture

### Spike 4 — Recommendation Philosophy

**Status:** Complete (Amended — recs generated in Interpretation only)
**Date:** 2026-07-25
**Amended:** 2026-07-25
**Authority:** EQ-0021 Spike 4

---

## 1. Purpose

Define the distinction between Finding, Observation, Recommendation, and Professional Judgement. Ensure CheckMate recommendations remain advisory and never replace the professional estimator.

---

## 2. Critical Architecture Rule

**Recommendations are generated ONLY during Interpretation.**

- Interpretation layer generates recommendations from evidence patterns
- Presentation Model stores already-generated recommendations
- Presentation layer never generates recommendations
- Presentation layer only renders recommendations from the Model
- Reports serialize recommendations from the Model
- Recommendations remain advisory and rejectable

---

## 3. Definitions (unchanged)

All definitions remain as previously documented (Finding, Observation, Recommendation, Professional Judgement).

---

## 4. Recommendation Formula (unchanged with one addition)

| Pattern | Evidence Source | Recommendation Template |
|---------|----------------|-----------------------|
| Zero quantity with UOM | zero_quantity_items | "Review {count} items with zero quantity — may affect cost plan completeness" |
| Level skip > 1 | detected_level_skips | "Verify {count} level skips in hierarchy — may indicate missing WBS levels" |
| Header with quantity | header_quantity_violations | "Verify {count} headers reporting quantities" |
| Missing description | completeness_findings | "Review {count} items missing descriptions — plan accuracy may be affected" |
| Missing UOM | completeness_findings | "Review {count} items missing UOM — unit rates cannot be verified" |

**Location:** Generated during Interpretation, stored in Presentation Model.

---

## 5. Generation Responsibility

| Stage | Generates Recs | Uses Recs | Action |
|-------|---------------|-----------|--------|
| Interpretation | YES | — | One-time generation from evidence patterns |
| Presentation Model Assembly | — | Stores | Immutable storage of generated recs |
| Presentation | NO | Renders | Displays from Model |
| Review | NO | Displays | Reviewer sees from Model |
| Report | NO | Serializes | Copies from Model to Export |
| Export | NO | Serializes | Copies from Model |

---

## 6. Document Control

| Property | Value |
|----------|-------|
| Document ID | EQ-0021-S4 |
| Engineering Question | EQ-0021 |
| Spike | 4 |
| Status | Complete (Amended) |
| Date | 2026-07-25 |
| Amendments | Recommendation generation consolidated to Interpretation only |
| Authority | EQ-0021 |