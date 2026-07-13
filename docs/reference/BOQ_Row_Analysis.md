# BOQ Row Analysis — Engineering Spike #1 Report

## Engineering Question

Can Jarvis deterministically identify BOQ rows and validate the OMISSION/ADDITION sign convention using the minimum implementation necessary?

## Measurements

| Metric | Value |
|--------|-------|
| Runtime | < 1 second |
| Lines of Code | ~80 lines |
| Correctness | Complete against fixture |

## Row Classification Results

| Type | Count |
|------|-------|
| Head | 2011 |
| Note | 520 |
| Section | 15 |
| Item | 3615 |
| Other | 188 (3.0%) |

**Engineering observation**: The remaining "Other" rows do not currently require classification. The proportion makes future runs against different files easily detectable.

## Section Sign Convention Results

| Section | Negative Qty | Positive Qty |
|---------|-------------|--------------|
| OMISSION | 169 | 7 |
| ADDITION | 0 | 3 |

## Observed Anomalies

7 items within the OMISSION section contain positive quantities (contrary to expected sign convention):

| Row | Code | Qty |
|-----|------|-----|
| 6202 | BE/2 | 21 |
| 6343 | BH/24 | 6 |
| 6344 | BH/25 | 4 |
| 6345 | BH/26 | 1 |
| 6346 | BH/27 | 3 |
| 6347 | BH/28 | 5 |
| 6348 | BH/29 | 5 |

These require architectural or domain review to determine if:
- The quantities represent a convention misunderstanding
- The data contains legitimate exceptions
- The fixture itself has data quality issues

## Engineering Observations

### What stayed coupled

- Column positions are hardcoded (A=Code, B=Desc, C=Qty, D=UOM)
- Row 6 is assumed to be the first data row after headers
- Section boundaries are detected via `UOM='noidc'` + `Desc='OMISSION/ADDITION'`

### What naturally separated

- Row classification logic (marker lookup in Column D)
- Item detection heuristic (slash pattern in Column A)
- Section sign validation (single state variable tracked sections)
- No abstraction threshold was reached; a flat script was sufficient

### Unexpected complexity

- The sign convention requires section-aware validation, not global validation
- Column D contains both semantic markers (Head1-5, Note, noidc) and legitimate UOM values (m2, m3, no)
- The "Other" bucket represents rows not fitting the observed patterns

### Possible future abstractions

None required at this spike scope. Two rules handled classification; one variable tracked section state.

## Explicit Unknowns Carried Forward

1. **Column positions** (A=Code, B=Desc, C=Qty, D=UOM) are only validated against this single file/format. A second real file or format is required before generalizing.

2. **OMISSION/ADDITION marker convention** (UOM='noidc' + Description label) is only validated against this one fixture. Different CostX export types may use different conventions.

3. **The 7 positive-quantity anomalies** in the OMISSION section require domain expertise to determine if:
   - These represent legitimate business exceptions
   - The data entry convention differs from expected sign logic
   - The fixture contains data quality issues that should be corrected

## Answer to Engineering Question

**Question Status**: PARTIALLY ANSWERED

**Confidence**: MEDIUM

**Supporting Evidence**: The spike demonstrates that deterministic identification is possible with the observed rules. However, the presence of 7 positive-quantity items in the OMISSION section, combined with the lack of validation against additional fixtures, prevents a complete answer. The anomalies require domain or architectural review before the sign convention can be confirmed as valid or invalid.

---

## Post-EQ-0007 Reconciliation

This section documents the production implementation reconciliation. The original Spike #1 report above is preserved as historical engineering evidence.

### EQ-0007 Production Extraction Results

| Type | Spike #1 | Production | Difference |
|------|----------|------------|------------|
| Head | 2011 | 2011 | 0 |
| Note | 520 | 520 | 0 |
| Section | 15 | 15 | 0 |
| Item | 3615 | 3605 | -10 |
| Other | 188 | 198 | +10 |
| Total | 6349 | 6349 | 0 |

### Production Implementation Changes

- **Item classification**: Changed from identifier-pattern fallback (`'/' in Column A`) to semantic UOM-based classification. This corrects the misclassification of 10 rows (5 Assumption + 5 endh1) that were incorrectly classified as Item.
- **BOQRow dataclass**: Added to production module (`src/jarvis/parsers/costx/boq_extraction.py`) for structured output.
- **Section context**: Added to BOQRow to preserve deterministic section state.

### Engineering Evidence Reinforced

- **EQ-0001**: Column A is confirmed as an opaque identifier. Identifier-based heuristics must not be used for semantic classification.
- **EQ-0002**: Sign convention mechanism (section-aware validation) remains valid and unchanged.
- **EQ-0006**: QS review confirmed the 7 positive-quantity OMISSION items are data-entry errors. The fixture remains unchanged per Engineering_Fixtures.md.

### Reference

Full evidence: `docs/reference/EQ_0007_Production_Extraction_Report.md`
