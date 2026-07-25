# EQ-0010 — Spike 1 — Evidence Report — Direct Field Observation

**Date:** 2026-07-14  
**Status:** Complete — Frozen (Accepted with Amendments)  
**Investigation:** EQ-0010 Deterministic BOQ Structural Intelligence  
**Governance:** Engineering_Governance.md v1.0

---

## Objective

Establish what is **Observable** from BOQRow fields alone.

No computation, no derivation, no interpretation beyond direct field presence.

---

## Method

1. Load `full_boq.xlsx` via WorkbookParser
2. Execute `extract_boq()` to produce `list[BOQRow]`
3. Enumerate all 7 BOQRow fields
4. Produce field presence statistics and value distributions
5. Repeat execution to verify determinism
6. Record only directly observable properties — no derived or computed classifications

---

## Outcome: Determinism Verified

**Run 1 == Run 2: True**

All field observations are deterministic and reproducible.

---

## BOQRow Schema Verification

The following field types and nullability are observed from the production data structure:

| Field | Python Type | Nullable | Observed Values |
|-------|-------------|----------|-----------------|
| `row_number` | `int` | No | 6–6354 |
| `code` | `str \| None` | Yes | Various identifiers |
| `description` | `str \| None` | Yes | Various text |
| `quantity` | `float \| None` | Yes | -638.0 to 5084.0 |
| `uom` | `str \| None` | Yes | 16 distinct values |
| `row_type` | `str` | No | Head, Item, Note, Other, Section |
| `section` | `Literal["OMISSION", "ADDITION"] \| None` | Yes | OMISSION, ADDITION, None |

This defines the observation boundary. Only these 7 fields and their direct values are Observable.

---

## Observable Capabilities

The following BOQRow fields are **Observable** (directly available in data structure):

| Field | Present | Absent | Present % |
|-------|---------|--------|-----------|
| `row_number` | 6349 | 0 | 100.00% |
| `row_type` | 6349 | 0 | 100.00% |
| `description` | 6278 | 71 | 98.88% |
| `uom` | 6161 | 188 | 97.04% |
| `code` | 4257 | 2092 | 67.05% |
| `quantity` | 3605 | 2744 | 56.78% |
| `section` | 491 | 5858 | 7.73% |

**Note:** All 7 BOQRow fields are Observable from the data structure. Absent values indicate null in the source data, not unobservability. Null presence is itself an observation.

---

## Row Type Distribution

| Type | Count |
|------|-------|
| Head | 2011 |
| Item | 3605 |
| Note | 520 |
| Other | 198 |
| Section | 15 |
| **Total** | **6349** |

---

## UOM Value Distribution

| UOM | Count |
|-----|-------|
| m2 | 1217 |
| no | 908 |
| Head4 | 636 |
| Head3 | 627 |
| Note | 520 |
| m3 | 461 |
| m | 454 |
| Head2 | 394 |
| Item | 351 |
| Head1 | 294 |
| t | 208 |
| Head5 | 60 |
| noidc | 15 |
| item | 6 |
| Assumption | 5 |
| endh1 | 5 |

**Observation only:** This spike observed 16 distinct UOM values. Head1, Head2, Head3, Head4, Head5 are present as UOM strings. No conclusion regarding hierarchy semantics is made in this spike.

---

## Section Distribution

| Section | Count |
|---------|-------|
| (none) | 5858 |
| OMISSION | 479 |
| ADDITION | 12 |

---

## Row Type by Section

| Section | Head | Item | Note | Other | Section |
|---------|------|------|------|-------|---------|
| (none) | 1771 | 3422 | 520 | 145 | 0 |
| ADDITION | 2 | 3 | 0 | 6 | 1 |
| OMISSION | 238 | 180 | 0 | 47 | 14 |

---

## Data Quality Observations

Observational only. No interpretation or correction.

| Observation | Value |
|-------------|-------|
| Row numbers | 6–6354, contiguous (no gaps) |
| Distinct codes | 4257 |
| Distinct descriptions | 2414 |
| Empty strings (code) | 0 |
| Empty strings (description) | 0 |
| Unique quantity values | 547 |

**Null Field Patterns (top 5):**

| Pattern | Count |
|---------|-------|
| Only section is null | 3422 |
| code + quantity + section are null | 1715 |
| quantity + section are null | 581 |
| code + quantity are null | 250 |
| All fields present | 183 |

**Quantity Observations:**

| Measure | Value |
|---------|-------|
| Min | -638.0 |
| Max | 5084.0 |
| Negative count | 169 |
| Zero count | 5 |
| Positive count | 3431 |

**UOM Observations:**

| Observation | Value |
|-------------|-------|
| Distinct UOM values | 16 |
| Standard item UOMs | m2(1217), no(908), m3(461), m(454), t(208), Item(351), item(6) |
| Head UOM strings | Head1(294), Head2(394), Head3(627), Head4(636), Head5(60) |
| Section markers | noidc(15) |
| Note markers | Note(520) |
| Other UOMs | Assumption(5), endh1(5) |

---

## Additional Observables

| Observation | Value |
|-------------|-------|
| Total rows | 6349 |
| Row number range | 6-6354 |
| Row number continuity | Contiguous |

---

## Capability State Transitions

The following capabilities transition from **Unknown → Observable** based on this spike:

| Candidate Engineering Capability | Previous State | New State | Evidence |
|----------------------------------|---------------|-----------|----------|
| Row type | Unknown | **Observable** | Direct BOQRow.row_type field |
| Row number | Unknown | **Observable** | Direct BOQRow.row_number field |
| Code presence | Unknown | **Observable** | Direct BOQRow.code field |
| Description presence | Unknown | **Observable** | Direct BOQRow.description field |
| Quantity value | Unknown | **Observable** | Direct BOQRow.quantity field |
| UOM value | Unknown | **Observable** | Direct BOQRow.uom field |
| Section context | Unknown | **Observable** | Direct BOQRow.section field |

The following capability remains **Unknown** — determining transitions requires algorithmic derivation (Spike 3):

| Candidate Engineering Capability | State | Evidence |
|----------------------------------|-------|----------|
| Row type transitions | Unknown | Not observable from a single field; requires sequence analysis in Spike 3 |

---

## Production Applicability

Observable capabilities can be used immediately for:
- **Reporting:** Direct field reading, summary statistics
- **Export:** All fields available for CSV/JSON output
- **Display:** Complete field values available for UI display
- **Validation:** Field presence checks (code present=67.05%, etc.)

---

## Tool

This spike was executed via `tools/eq0010_spike1_direct_field_observation.py`.

---

## Evidence Immutability

This evidence report is frozen. No modifications permitted after publication.

---

## Amendments Applied

The following amendments were applied per Project Owner disposition before freezing:

1. **Reverted Row Type Transitions:** Changed from "Derivable" back to "Unknown" as transitions require algorithm computation, not direct observation
2. **Removed hierarchy implication:** Head1-5 UOM values reported as observed strings only — no hierarchy semantics implied
3. **Added BOQRow Schema Verification:** Documents field types, nullability, and observation boundary
4. **Added Data Quality Observations:** Observational summary of nulls, empty strings, duplicates, and UOM patterns
5. **Standardized evidence title:** EQ-0010 — Spike 1 — Evidence Report — Direct Field Observation