# EQ-0010 — Spike 2 — Evidence Report — UOM Pattern Analysis

**Date:** 2026-07-14  
**Status:** Complete — Accepted with Amendments (pending freeze)  
**Investigation:** EQ-0010 Deterministic BOQ Structural Intelligence  
**Governance:** Engineering_Governance.md v1.0

---

## Objective

Investigate whether the observed UOM string patterns (Head1-5) can be deterministically interpreted as structural hierarchy indicators using only production evidence, or whether they remain uninterpretable observational labels.

---

## Outcome: Determinism Verified

**Run 1 == Run 2: True**

All UOM pattern observations are deterministic and reproducible.

---

## BOQRow Schema (Refresher from Spike 1)

The `uom` field is of type `str | None` and is directly Observable on each row.

---

## Observations

### 1. Observed Head UOM Values

| UOM String | Row Count |
|------------|-----------|
| Head1 | 294 |
| Head2 | 394 |
| Head3 | 627 |
| Head4 | 636 |
| Head5 | 60 |

**Finding:** Five distinct UOM strings with the prefix "Head" followed by a digit (1-5) are present in the production data. These strings are directly Observable on each row via the `uom` field. No inference, computation, or domain knowledge is required to access them.

### 2. Observed Head UOM Frequency Distribution

Head rows constitute 2011 of 6349 total rows (31.7%). The distribution across the five UOM strings is:

- Head4 (636) and Head3 (627) are most frequent
- Head1 (294), Head2 (394) less frequent
- Head5 (60) least frequent

No interpretation of what these frequencies mean is made in this spike.

### 3. Observed UOM String Co-occurrence by Section

| Section | Head1 | Head2 | Head3 | Head4 | Head5 |
|---------|-------|-------|-------|-------|-------|
| (none) | 270 | 329 | 551 | 565 | 56 |
| OMISSION | 24 | 64 | 75 | 71 | 4 |
| ADDITION | 0 | 1 | 1 | 0 | 0 |

**Finding:** Head1–Head5 UOM strings were observed in both the default section and the OMISSION section. Head2 and Head3 were also observed in the ADDITION section.

### 4. Item UOM Distribution

| UOM String | Count |
|------------|-------|
| m2 | 1217 |
| no | 908 |
| m | 454 |
| m3 | 461 |
| t | 208 |
| Item | 351 |
| item | 6 |

**Finding:** Item rows carry measurable UOM strings (m2, no, m, m3, t) alongside the string "Item". No head-prefixed strings appear on Item rows.

### 5. UOM Transition Frequencies (Top 10)

The following are observed transitions between consecutive rows, reported by UOM value:

| From UOM | To UOM | Count |
|----------|--------|-------|
| m2 | m2 | 643 |
| no | no | 630 |
| Note | Note | 374 |
| m3 | m3 | 352 |
| Item | Item | 304 |
| Head4 | m2 | 290 |
| Head2 | Head3 | 271 |
| Head3 | Head4 | 257 |
| m2 | Head4 | 181 |
| m | m | 178 |

**Finding:** 107 distinct UOM-to-UOM transition patterns were observed. The top 10 transitions account for the most frequent consecutive UOM value pairs. No interpretation of what these transitions represent structurally is made in this spike. Transition analysis (sequence patterns, parent-child relationships) is assigned to Spike 3.

### 6. Head UOM → Next UOM Frequencies

The following observations list what UOM string appears on the row immediately following each Head UOM string:

| Head UOM | Following UOM | Count |
|----------|---------------|-------|
| Head4 | m2 | 290 |
| Head2 | Head3 | 271 |
| Head3 | Head4 | 257 |
| Head3 | m2 | 169 |
| Head1 | Head2 | 137 |
| Head1 | Note | 101 |
| Head4 | no | 97 |
| Head3 | m | 90 |
| Head4 | m3 | 57 |
| Head4 | m | 57 |
| Head2 | no | 46 |
| Head5 | m3 | 23 |

**Finding:** These are observed adjacency patterns only. No claims about "parent-child", "contains", "deepening", or "backtracking" are made in this spike. Spike 3 will analyze whether these adjacency patterns correspond to structural hierarchy.

---

## Capability State Transitions

| Candidate Engineering Capability | Previous State | New State | Evidence |
|----------------------------------|---------------|-----------|----------|
| Hierarchy indicator (Head1-5 labels) | Unknown | **Observable** | Direct BOQRow.uom field values: Head1, Head2, Head3, Head4, Head5 |

**Note:** "Hierarchy indicator" is the established capability — i.e., the presence and value of Head1-5 UOM strings. Whether these strings constitute a structural hierarchy (depth, parent-child progression) is not determined by this spike. That investigation is assigned to Spike 3 (Row Sequence Analysis).

---

## What This Spike Does NOT Conclude

To preserve evidence-first discipline, this spike explicitly does NOT conclude:

1. **Hierarchy depth is Observable** — The classification "Hierarchy indicator" only establishes that Head1-5 strings exist. Whether Head3 means "level 3" in a hierarchy requires sequence analysis (Spike 3).
2. **Progression patterns** — Head2→Head3 frequency is observed but not interpreted as "deepening" or "parent→child". That requires Spike 3.
3. **Backtracking patterns** — Head4→Head3 is observed but not interpreted. That requires Spike 3.
4. **Domain knowledge requirements** — No external domain document was consulted during this spike. Whether domain knowledge is required overall is investigated in Spike 5.

---

## Production Applicability

Observable UOM strings can be used for:
- **Reporting:** Reading Head1-5 values from the UOM field
- **Display:** Showing UOM values in UI
- **Export:** Including Head1-5 strings in data output

Structural interpretation (hierarchy depth, parent-child relationships, level progression) requires Spike 3 before it can be classified.

---

## Tool

This spike was executed via `tools/eq0010_spike2_uom_pattern_analysis.py`.

---

## Evidence Immutability

This evidence report is frozen. No modifications permitted after publication.