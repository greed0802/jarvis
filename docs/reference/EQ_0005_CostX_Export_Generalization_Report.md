# EQ-0005: CostX Export Generalization Investigation

**Status**: Evidence Complete — Pending Project Owner Disposition
**Scope**: Row classification semantic generalization across CostX BOQ exports
**Fixtures Analyzed**: `full_boq.xlsx`, `Structural Reinforcement Only.xlsx`
**Date**: 2026-07-13
**Author**: Implementation Engineer (Engineering Investigation)

---

The engineering investigation demonstrates that UOM-based BOQ semantics are supported across the observed CostX export families, while workbook structure (worksheet name, header position, first data row, and metadata layout) varies between exports.

The current production parser remains intentionally narrow and continues to define the supported production scope.

No production parser changes are authorized as a result of EQ-0005.

A future Engineering Question (candidate: EQ-0008) may investigate deterministic structural discovery after sufficient additional engineering evidence becomes available.

Proceed with repository stabilization before commencing M7.

## 1. Observations

### 1.1 Workbook-Level Observations

| Property | `full_boq.xlsx` | `Structural Reinforcement Only.xlsx` | Match? |
|---|---|---|---|
| File size | 241,295 bytes | 91,522 bytes | Different |
| Sheet count | 1 | 1 | **Same** |
| Sheet name | `CostX` | `Structural Reinforcement` | **Different** |
| Header row | Row 4 | Row 3 | **Different** |
| First data row | Row 6 | Row 5 | **Different** |
| Total rows | 6,354 | 1,055 | Different |
| Total columns | 9 (A-I) | 26 (A-Z) | **Different** |
| Core BOQ columns | A-D (Code, Desc, Qty, UOM) | A-D (Code, Desc, Qty, UOM) | **Same** |
| Metadata columns | E-I (Rate, SubTotal, Factor, Total, Total) | E-R (Rate, SubTotal, Factor, Total, Total + Level, Zone, Pour, Element, ...) | Different |
| Auto-filter | None | `$A$1:$R$1055` | **Different** |
| Creator | `openpyxl` | `Pia A. Nailes` | Different |
| Calculation mode | `fullCalcOnLoad=True` | `fullCalcOnLoad=True` | **Same** |
| Excel base date | 1900 date system | 1900 date system | **Same** |
| Formulas | Yes (columns F, I) | Yes (columns F, H, I) | **Same** |

### 1.2 Header Row Comparison

| Column | `full_boq.xlsx` (Row 4) | `Structural Reinforcement Only.xlsx` (Row 3) | Match? |
|---|---|---|---|
| A | Code | Code | **Same** |
| B | Description | Description | **Same** |
| C | Quantity | Quantity | **Same** |
| D | UOM | UOM | **Same** |
| E | Rate | Rate | **Same** |
| F | SubTotal | SubTotal | **Same** |
| G | Factor | Factor | **Same** |
| H | Total | Total | **Same** |
| I | Total | Total | **Same** |
| J | (empty) | Level | New |
| K | (empty) | Zone | New |
| L | (empty) | Pour | New |
| M | (empty) | Element | New |
| N | (empty) | Element No. | New |
| O | (empty) | Product Category | New |
| P | (empty) | Product Code | New |
| Q | (empty) | Product Description | New |
| R | (empty) | Bar Shape | New |

### 1.3 Column Taxonomy Comparison

#### Column A (Code / Identifier)

| Property | `full_boq.xlsx` | `Structural Reinforcement Only.xlsx` |
|---|---|---|
| Non-empty cells | 4,260 | 235 |
| Unique values | Hundreds (hierarchical: A, A/1, B/2, etc.) | **3 total** (`Code`, `**`, blank) |
| Content pattern | Hierarchical identifiers (letter/number combos) | **Essentially empty** — only `**` marker on total rows |
| Classification use | Opaque identifier per EQ-0001 | Confirmed as **not a semantic classifier** |

**Observation**: Column A in `Structural Reinforcement Only.xlsx` is effectively empty for data rows. The only non-empty values are:
- Row 3: `Code` (header)
- Row 1055: `**` (total row marker)

This confirms EQ-0001's finding: Column A is an opaque identifier. In this workbook, it contains no data, reinforcing that identifier-based heuristics would entirely fail.

#### Column B (Description)

Both workbooks contain text descriptions, wrapped text, and hierarchical content descriptions. Consistent.

#### Column C (Quantity)

| Property | `full_boq.xlsx` | `Structural Reinforcement Only.xlsx` |
|---|---|---|
| Non-empty cells | 3,606 | 622 |
| Data type | Predominantly numeric | **621 numeric, 1 text** |
| Number format | Various | `#,##0.00` |

Consistent: quantity column is numeric across both fixtures.

#### Column D (UOM / Semantic Marker)

| UOM Value | `full_boq.xlsx` | `Structural Reinforcement Only.xlsx` | Classification |
|---|---|---|---|
| Head1 | 294 | 16 | Section header |
| Head2 | 394 | 22 | Section header |
| Head3 | 627 | 57 | Section header |
| Head4 | 636 | 105 | Section header |
| Head5 | 60 | 212 | Section header |
| Note | 520 | 13 | Note row |
| Item | 351 | 6 | Item row |
| item | 6 | 0 | Item row (lowercase variant) |
| m | 454 | 40 | UOM — Item |
| m2 | 1,217 | 35 | UOM — Item |
| m3 | 461 | 0 | UOM — Item |
| no | 908 | 3 | UOM — Item |
| t | 208 | 537 | UOM — Item |
| noidc | 15 | **0** | Section boundary |
| endh1 | 5 | **0** | Assumption end marker |
| Assumption | 5 | **0** | Assumption marker |
| UOM | 1 | 1 | Header row marker |

**Key Findings**:
1. Head1-5, Note, Item, m, m2, no, t are **present across both fixtures**.
2. `noidc` marker is **absent** from Structural Reinforcement Only.xlsx — no OMISSION/ADDITION sections exist.
3. `endh1` and `Assumption` are **absent** from Structural Reinforcement Only.xlsx.
4. `m3` is **absent** from Structural Reinforcement Only.xlsx (not needed for structural reinforcement work).
5. `t` (tonnes) is the **dominant UOM** in Structural Reinforcement (537 occurrences) — consistent with structural steel measurement.
6. `Item` and `item` lowercase variant: Structural Reinforcement uses only uppercase `Item` (6 occurrences).

### 1.4 Expanded Metadata Columns (J-R)

The Structural Reinforcement workbook contains **9 additional metadata columns** not present in full_boq:

| Column | Header | Description | Unique Values | Purpose |
|---|---|---|---|---|
| J | Level | Level/Location | 27 | Location tracking |
| K | Zone | Zone | 4 | Zoning |
| L | Pour | Pour number | 17 | Pour sequencing |
| M | Element | Element type | 12 | Structural element |
| N | Element No. | Element number | 50 | Element identification |
| O | Product Category | Material category | 7 | Material type |
| P | Product Code | Material code | 23 | Material specification |
| Q | Product Description | Material description | 28 | Material details |
| R | Bar Shape | Shape classification | 13 | Bar bending shape |

These columns represent **CostX structural reinforcement export metadata**. They are not BOQ classification columns — they are supplementary structural engineering data.

### 1.5 Section Boundaries

| Property | `full_boq.xlsx` | `Structural Reinforcement Only.xlsx` |
|---|---|---|
| OMISSION section | Present (noidc marker) | **Absent** |
| ADDITION section | Present (noidc marker) | **Absent** |
| Section propagation needed | Yes | **No** — no sections |

**Observation**: The Structural Reinforcement BOQ is a single-section (non-OMISSION/ADDITION) export. Section propagation logic would identify no sections, and all rows would have `section=None`.

---

## 2. Semantic Findings

### Finding S1: UOM-Based Classification Survives Across Exports

The core semantic discovery from EQ-0001 — that UOM values in Column D deterministically determine row classification — is **supported** by the second fixture.

**Evidence**: Full UOM marker set comparison (Section 1.3):
- Head1-5: Present in both fixtures
- Note: Present in both fixtures
- Item: Present in both fixtures
- m, m2, no, t: Present in both fixtures
- item (lowercase): Present in full_boq, absent in Structural Reinforcement (no impact — uppercase `Item` handles both)

**Fixture**: `full_boq.xlsx` and `Structural Reinforcement Only.xlsx`, Column D
**Classification**: **SUPPORTED**

### Finding S2: UOM Vocabulary Is Subset, Not Superset

The second fixture uses a **subset** of the full_boq UOM vocabulary. No new UOM markers were discovered.

**Evidence**: All UOM values in Structural Reinforcement are a subset of those in full_boq:
- `m3` absent (not needed for structural reinforcement)
- `noidc` absent (no OMISSION/ADDITION sections)
- `endh1` absent (no assumption markers)
- `Assumption` absent (no assumption markers)

**Fixture**: `Structural Reinforcement Only.xlsx`, Column D
**Classification**: **SUPPORTED** — Vocabulary subset is valid. No new markers found.

### Finding S3: Item Classification Without Identifier Fallback Produces Correct Results

The EQ-0007 production implementation (UOM-only classification, no identifier heuristic) would classify Structural Reinforcement correctly.

**Evidence**: The 6 `Item` rows in Structural Reinforcement are identified by the `Item` UOM value. No identifier-based fallback is needed. The "Other" bucket would contain rows with UOM values not in the current set (if any new ones were found — none were).

**Fixture**: `Structural Reinforcement Only.xlsx`, Column D
**Classification**: **SUPPORTED**

### Finding S4: Section Propagation Is Context-Dependent

OMISSION/ADDITION section markers are **workbook-specific**. The current logic correctly handles their absence.

**Evidence**: `noidc` markers are entirely absent from Structural Reinforcement. The `extract_boq()` function would return `section=None` for all rows — no error, no incorrect behavior.

**Fixture**: `Structural Reinforcement Only.xlsx`
**Classification**: **SUPPORTED** — Current behavior is correct for both workbooks.

---

## 3. Structural Findings

### Finding F1: Worksheet Name Is Export-Specific

The assumption "worksheet is named `CostX`" is **unsupported**.

**Evidence**: `Structural Reinforcement Only.xlsx` uses worksheet name `Structural Reinforcement`.

**Fixture**: `Structural Reinforcement Only.xlsx`, sheet metadata
**Classification**: **FALSIFIED** — The current `WorkbookParser.validate()` check for `"CostX"` worksheet name would reject this workbook.

### Finding F2: Header Row Position Is Export-Specific

The assumption "header row is Row 4" is **unsupported**.

**Evidence**: `Structural Reinforcement Only.xlsx` has headers at Row 3.

**Fixture**: `Structural Reinforcement Only.xlsx`, Row 3
**Classification**: **FALSIFIED** — Current fixed-row assumption (Row 4) is unsupported.

### Finding F3: First Data Row Position Is Export-Specific

The assumption "first data row is Row 6" is **unsupported**.

**Evidence**: `Structural Reinforcement Only.xlsx` report content begins at Row 5. The first BOQ data row begins at Row 6 (header at Row 3, blank Row 4, title at Row 5, BOQ data from Row 6).

**Fixture**: `Structural Reinforcement Only.xlsx`, Row 5-6
**Classification**: **FALSIFIED** — Current fixed-row assumption (`_FIRST_DATA_ROW = 6`) is unsupported.

### Finding F4: Code Column Content Is Export-Specific

The assumption "Column A contains hierarchical codes" is **unsupported** as a structural requirement.

**Evidence**: `Structural Reinforcement Only.xlsx` Column A is essentially empty for data rows (only `**` on total rows). This does not affect classification — code extraction returns `None` gracefully.

**Fixture**: `Structural Reinforcement Only.xlsx`, Column A
**Classification**: **FALSIFIED** — Column A content varies by export type. Current code handles this correctly (returns `None` for empty codes).

### Finding F5: Metadata Columns Are Export-Configurable

The assumption "columns E-I are the full extent of metadata" is **unsupported**.

**Evidence**: `Structural Reinforcement Only.xlsx` adds 9 additional columns (J-R) with structural engineering metadata.

**Fixture**: `Structural Reinforcement Only.xlsx`, Columns J-R
**Classification**: **FALSIFIED** — Metadata columns vary by CostX export configuration. Current parser ignores columns beyond D, which is correct behavior for the current scope.

### Finding F6: Single-Sheet Structure Is Supported

The assumption "exactly 1 worksheet" is **supported**.

**Evidence**: Both fixtures have exactly one worksheet.

**Fixture**: Both workbooks
**Classification**: **SUPPORTED** — Both observed exports are single-sheet.

---

## 4. Production Assumption Matrix

| # | Production Assumption | Current Code Location | Classification | Evidence |
|---|---|---|---|---|
| A1 | Worksheet is named "CostX" | `workbook_parser.py:110` | **FALSIFIED** | F1 — Structural Reinforcement uses different name |
| A2 | Exactly 1 worksheet | `workbook_parser.py:104` | **SUPPORTED** | F6 — Both fixtures have 1 sheet |
| A3 | Header row is Row 4 | `workbook_parser.py` (implicit) | **FALSIFIED** | F2 — Header at Row 3 in Structural Reinforcement |
| A4 | First data row is Row 6 | `boq_extraction.py:31` | **FALSIFIED** | F3 — First data row at Row 5 in Structural Reinforcement |
| A5 | Column A = Code | `boq_extraction.py:25` | **SUPPORTED** | E1 — Header confirms |
| A6 | Column B = Description | `boq_extraction.py:26` | **SUPPORTED** | E1 — Header confirms |
| A7 | Column C = Quantity | `boq_extraction.py:27` | **SUPPORTED** | E1 — Header confirms |
| A8 | Column D = UOM | `boq_extraction.py:28` | **SUPPORTED** | E1 — Header confirms |
| A9 | UOM-based classification via Head1-5, Note, Item, m, m2, m3, no, t | `boq_extraction.py:36` | **SUPPORTED** | S1, S2, S3 — All markers work across both fixtures |
| A10 | Section propagation via noidc markers | `boq_extraction.py:90-91` | **WORKBOOK-SPECIFIC** | S4 — Only full_boq has sections |
| A11 | Column A contains hierarchical codes | `boq_extraction.py` (extracted but not classified) | **FALSIFIED** | F4 — Empty in Structural Reinforcement |
| A12 | Row count > 1,000 | `boq_extraction.py` (implicit) | **SUPPORTED** | Both fixtures have > 1,000 rows |

### Assumption Classification Summary

| Classification | Count | Assumptions |
|---|---|---|
| **SUPPORTED** | 7 | A2, A5, A6, A7, A8, A9, A12 |
| **FALSIFIED** | 4 | A1, A3, A4, A11 |
| **WORKBOOK-SPECIFIC** | 1 | A10 |
| **EXPORT-SPECIFIC** | 0 | — |
| **UNKNOWN** | 0 | — |

---

## 5. Parser Recommendation

### Option A (Recommended): Maintain intentionally narrow production. Open a new Engineering Question.

**Rationale**: The existing production parser (`WorkbookParser` + `extract_boq`) is designed for the full_boq.xlsx format. The Structural Reinforcement workbook demonstrates that:

1. **Semantic findings**: UOM-based classification rules survive across exports. No semantic changes required.
2. **Structural findings**: Worksheet name, header row position, first data row position are export-specific. Current fixed-row assumptions are unsupported.
3. **Section propagation is workbook-specific**: Current logic correctly handles absence of sections.

### Recommendation: Option A

1. **Do not modify the current production parser** — it correctly handles the full_boq.xlsx format.
2. **Recommend the Project Owner consider opening** Engineering Question EQ-0008 after sufficient additional fixtures become available.
3. The UOM-based classification logic is semantically sound and can be reused, but header/discovery logic requires independent engineering.

### Rejected: Option B

**Do not generalize the parser now.** The evidence is insufficient to justify:
- A multi-format parser
- Automatic worksheet discovery
- Header row auto-detection

Two fixtures provide directional evidence but do not meet the **Rule of Three** (need 3+ independent fixtures to justify generalization).

### Recommended New Engineering Question

**EQ-0008 (Proposed)**: Can the worksheet structure (worksheet name, header row, first data row, column assignment) be determined deterministically across CostX BOQ exports?

This question requires:
1. At least one additional fixture with structural variation.
2. Engineering investigation of header detection heuristics.
3. Investigation of whether metadata columns can be used for structural detection.

---

## 6. Parser Cleanup Checklist

The following items are recommended for cleanup. This is a documentation-only checklist — do not perform cleanup.

| Item | File | Description | Priority |
|---|---|---|---|
| C1 | `src/jarvis/parsers/observation.py` | Observation runtime (rejected by ADR-0025) | HIGH — Project Owner to determine archive strategy consistent with ADR-0025 and repository history policy |
| C2 | `tests/parser/test_observation_models.py` | Observation model tests (rejected by ADR-0025) | HIGH — Project Owner to determine archive strategy consistent with ADR-0025 and repository history policy |
| C3 | `tests/parser/test_workbook_observe_historical.py` | Historical observe() tests (8 skipped) | HIGH — Project Owner to determine archive strategy consistent with ADR-0025 and repository history policy |
| C4 | `docs/ontology/observation/` | 8 observation ontology documents (rejected by ADR-0025) | HIGH — Project Owner to determine archive strategy consistent with ADR-0025 and repository history policy |
| C5 | `temp_uom_check.py` | Temporary investigation script | LOW — Remove after review |
| C6 | `temp_verify_extraction.py` | Temporary verification script | LOW — Remove after review |
| C7 | `requirements.txt` | Empty file (0 bytes) — needs dependencies | MEDIUM — Populate with project dependencies |
| C8 | `docs/design/M6_Observation_Model.md` | Design document for rejected architecture | MEDIUM — Project Owner to determine archive strategy |

---

## 7. Evidence Traceability Matrix

| ID | Observation | Fixture | Evidence | Production Impact | Recommendation |
|---|---|---|---|---|---|
| T1 | Column positions A-D are identical | Both workbooks, Row 3/4 headers | E1 | None — supported | Maintain current column mapping |
| T2 | UOM markers Head1-5, Note, m, m2, no, t present in both | Both workbooks, Column D | E2 | None — supported | Maintain UOM-based classification |
| T3 | Worksheet name differs | `Structural Reinforcement Only.xlsx` | E3 | Fails validation — `WorkbookParser.validate()` rejects non-"CostX" names | Open EQ-0008 for investigation |
| T4 | Header row differs (Row 3 vs Row 4) | Both workbooks | E4 | Fails extraction — `extract_boq()` starts at wrong row | Open EQ-0008 for investigation |
| T5 | First data row differs (Row 5 vs Row 6) | Both workbooks | E5 | Fails extraction — hardcoded `_FIRST_DATA_ROW = 6` is wrong | Open EQ-0008 for investigation |
| T6 | No section markers in Structural Reinforcement | `Structural Reinforcement Only.xlsx` | E6 | Section propagation returns `None` for all rows — no error | No action needed — correct behavior |
| T7 | Column A essentially empty in Structural Reinforcement | `Structural Reinforcement Only.xlsx` | E7 | No impact — `extract_boq()` handles `None` code values | No action needed |
| T8 | Expanded metadata columns in Structural Reinforcement | `Structural Reinforcement Only.xlsx` | E8 | No impact — current parser ignores columns beyond D | No action needed |

---

## 8. Open Evidence

The following questions cannot currently be answered. Each requires additional engineering fixtures.

| Question | Category | Required Evidence |
|---|---|---|
| Q1 | **Multi-sheet BOQ exports** — Do multi-sheet BOQ exports exist? | Additional fixture |
| Q2 | **Header layout variants** — What header row positions exist beyond Row 3 and Row 4? | 2+ additional fixtures |
| Q3 | **UOM vocabulary completeness** — Are there UOM markers beyond the current set? | Additional fixture with different trade/discipline |
| Q4 | **Localized CostX exports** — Do non-Australian CostX exports use different conventions? | Localized fixtures |
| Q5 | **CostX version impact** — Do different CostX versions produce different export structures? | Version-dated fixtures |
| Q6 | **Custom report templates** — Does CostX template customization affect column layout? | Template-variant fixtures |
| Q7 | **Deterministic header detection** — Can header row be found algorithmically without hardcoded position? | 3+ structurally different fixtures |

**Status**: Insufficient evidence — additional engineering fixtures required for each open question.

---

## 9. Engineering Conclusions

### Conclusion 1: Semantics Survive, Structure Fails
The core semantic discovery from EQ-0001 — UOM-based row classification — is **supported** by the second fixture. The structural assumptions (worksheet name, header row position, first data row) are **falsified**. This is the primary engineering outcome of EQ-0005.

### Conclusion 2: UOM Vocabulary Is a Subset
No new UOM markers were discovered. The second fixture uses a subset of the known vocabulary. This supports the current classification set as sufficient for the observed export types.

### Conclusion 3: No Generalization Justified Yet
Two fixtures provide directional evidence but do not meet the **Rule of Three**. At least one more structurally variant fixture is needed before generalizing the parser.

### Conclusion 4: Section Propagation Is Context-Dependent
OMISSION/ADDITION section markers are **workbook-specific**. The current logic correctly handles their absence (returning `section=None`).

### Conclusion 5: New Engineering Question Is Justified
The evidence supports proposing **EQ-0008** to investigate deterministic worksheet/header discovery. However, this should not proceed until additional fixtures are available.

---

## 10. Architectural Observation (Non-Normative)

Across the observed fixtures, workbook structure and BOQ semantics vary independently. The current evidence suggests these should continue to be treated as separate engineering concerns until additional evidence justifies further architectural evolution.

Specifically:
- **Workbook Structure** (worksheet name, header row, first data row, metadata columns, auto-filter) is export-configurable and varies between exports without affecting semantics.
- **BOQ Semantics** (UOM-based classification, quantity extraction, description extraction, section propagation) is stable across both observed exports.

This separation of concerns is an engineering observation, not an architectural decision. It records the insight that structural discovery logic and semantic extraction logic can be independently engineered and validated.

---

## 11. Update to Engineering Questions Registry

The following section should update `docs/reference/Engineering_Questions.md` for EQ-0005:

**EQ-0005 Status**: Evidence Complete — Pending Project Owner Disposition

**Evidence Summary**: UOM-based classification semantics are supported across the two observed CostX BOQ exports. Structural assumptions (worksheet name, header position, first data row) are falsified — current fixed-row assumptions are unsupported.

**Recommendation**: Option A — Maintain intentionally narrow production parser. Propose EQ-0008 for deterministic worksheet/header discovery when additional fixtures become available.

**Remaining Unknowns**: See Section 8 — Open Evidence (7 open questions).