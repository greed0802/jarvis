# EQ-0007 Production Extraction Report

## Engineering Question

EQ-0007 — What is the minimum deterministic production implementation that transforms a validated CostX BOQ workbook into structured BOQ rows while preserving the simplicity demonstrated by Engineering Spike #1?

---

## Implementation

**Module:** `src/jarvis/parsers/costx/boq_extraction.py`

**Lines:** ~90 lines (including BOQRow dataclass)

---

## Scope

- Fixture: `tests/fixtures/costx/full_boq.xlsx` only
- Single supported worksheet (validated by WorkbookParser)
- Deterministic UOM-based classification (EQ-0001)
- Section-aware extraction (EQ-0002)

---

## Classification Results

| Type | Count |
|------|-------|
| Head | 2011 |
| Note | 520 |
| Section | 15 |
| Item | 3605 |
| Other | 198 |
| **Total** | **6349** |

---

## Section Statistics

| Section | Negative Qty | Positive Qty |
|---------|--------------|--------------|
| OMISSION | 169 | 7 |
| ADDITION | 0 | 3 |

---

## Other Bucket Composition

| Category | Count |
|----------|-------|
| Blank UOM rows | 188 |
| Assumption (UOM="Assumption") | 5 |
| endh1 (UOM="endh1") | 5 |
| **Total Other** | **198** |

---

## Reproduced OMISSION Anomalies

Rows with positive quantities in OMISSION section (data-entry errors, EQ-0006):

| Row | Code | Qty |
|-----|------|-----|
| 6202 | BE/2 | 21 |
| 6343 | BH/24 | 6 |
| 6344 | BH/25 | 4 |
| 6345 | BH/26 | 1 |
| 6346 | BH/27 | 3 |
| 6347 | BH/28 | 5 |
| 6348 | BH/29 | 5 |

---

## Tests

Committed tests in `tests/parser/test_boq_extraction.py` (10 tests):

- Total row count verification
- Classification counts verification
- Row structure verification
- Section propagation verification
- OMISSION anomaly reproduction
- Deterministic behavior verification

Full test suite: 48 passed, 8 skipped (38 pre-existing + 10 new BOQ extraction tests).

---

## Runtime

< 1 second for 6,349 rows

---

## Reconciliation with Spike #1

| Metric | Spike #1 | EQ-0007 Production | Difference |
|--------|----------|-------------------|------------|
| Head | 2011 | 2011 | 0 |
| Note | 520 | 520 | 0 |
| Section | 15 | 15 | 0 |
| Item | 3615 | 3605 | -10 |
| Other | 188 | 198 | +10 |
| Total | 6349 | 6349 | 0 |

**Item count difference:** Spike #1 used identifier-pattern fallback (slash heuristic) which misclassified 10 rows (5 Assumption + 5 endh1) as Item. Production uses corrected UOM-based classification per EQ-0001 discovery that Column A is opaque.