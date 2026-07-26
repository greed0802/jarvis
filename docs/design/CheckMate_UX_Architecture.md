# CheckMate UX Architecture

## EQ-0021 — CheckMate Application Architecture

### Spike 3 — User Experience Model

**Status:** Complete (Amended — Presentation only renders Model)
**Date:** 2026-07-25
**Amended:** 2026-07-25
**Authority:** EQ-0021 Spike 3

---

## 1. Purpose

Define how findings are presented to the professional estimator. Presentation layer receives only the Presentation Model. No evidence processing, no validation logic, no severity computation in Presentation.

---

## 2. Critical Architecture Rule

**Presentation consumes Presentation Model only.**

Presentation layer MUST:
- Render PresentationFinding[], PresentationSection[], PresentationSummary, PresentationStatistics
- Allow filtering, sorting, navigation on Model data
- Manage review workflow (human decisions)
- Route user actions (accept, reject, flag)

Presentation layer MUST NOT:
- Interpret evidence
- Calculate severity
- Compute recommendations
- Compute statistics
- Validate findings
- Access BOQIntelligenceResult or ValidationFindings

---

## 3. Severity Model (unchanged)

Severity is already computed in Interpretation and stored in PresentationFinding.

| Level | Value | Description |
|-------|-------|-------------|
| HIGH | 3 | Critical — must review |
| MEDIUM | 2 | Important — should review |
| LOW | 1 | Informational |

---

## 4. Finding Grouping (unchanged — from Model)

Presentations already grouped by Interpretation. Presentation only displays groups.

---

## 5. Filtering (from Model)

Filtering operates on PresentationFinding objects:

| Dimension | Values | Default |
|-----------|--------|---------|
| Severity | HIGH, MEDIUM, LOW | All |
| Category | Anomalies, Structural, Completeness, etc. | All |
| Section | Specific sections | All |
| Review status | Unreviewed, Reviewed, Accepted, Rejected, Flagged | Unreviewed |

---

## 6. Navigation (unchanged)

Views render from Presentation Model:

| View | Content from Model | Access |
|------|-------------------|--------|
| Dashboard | PresentationSummary | Default |
| Anomalies | PresentationFinding[] (filtered) | From groups |
| Findings by Category | Grouped PresentationFinding | From groups |
| Evidence Detail | Evidence reference from PresentationFinding | Finding => Evidence |
| Review | Review state overlay on Model | Finding => Review |
| Summary | PresentationSummary + counters | Any => Summary |

---

## 7. Review Workflow (unchanged)

Review operates on findings from Presentation Model. Review state is mutable and separate.

---

## 8. Rendering Principles (Amended)

1. **Only render what is in the Model** — Presentation never recomputes
2. **Severity from Model** — already computed
3. **Statistics from Model** — already assembled
4. **Recommendations from Model** — already generated
5. **Review decisions from user** — mutable overlay

---

## 9. Document Control

| Property | Value |
|----------|-------|
| Document ID | EQ-0021-S3 |
| Engineering Question | EQ-0021 |
| Spike | 3 |
| Status | Complete (Amended) |
| Date | 2026-07-25 |
| Amendments | Presentation consumes only Presentation Model |
| Authority | EQ-0021 |