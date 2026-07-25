# Spike 3 — Deterministic Rule Definition

## EQ-0019 BOQ Semantic Intelligence Increment 1

### Purpose
For every Production Ready capability, define deterministic rules, inputs, outputs, invariants, and demonstrate repeatability. No implementation.

---

## Rule Definitions

### SEM-PROD-01: Vocabulary Extraction

**Rule:** Extract top-K engineering terms from BOQ item descriptions by frequency count.

**Inputs:**
- `rows: list[BOQRow]` — extracted BOQ rows
- `max_terms: int = 50` — maximum number of terms to report (optional, default 50)

**Outputs:**
- `vocabulary: dict[str, int]` — mapping of normalized term → occurrence count
- `total_descriptions_analyzed: int` — count of item descriptions scanned

**Algorithm:**
1. Filter rows where `row_type == "Item"` and `description` is not None
2. For each description:
   a. Split by whitespace
   b. Strip punctuation (.,;:()) from each word
   c. Filter words with length > 2 characters
   d. Increment counter for each normalized word (case-preserved)
3. Sort by count descending
4. Return top-K entries

**Invariants:**

| ID | Category | Description | Violation |
|---|---|---|---|
| INV-VOC-01 | determinism | Same input rows always produce same vocabulary dict | MAJOR |
| INV-VOC-02 | ordering | Results sorted descending by count | MINOR |
| INV-VOC-03 | immutability | Output dict is never modified after creation | MAJOR |
| INV-VOC-04 | boundary | Vocabulary reports frequencies only — no semantic meaning | MAJOR |

**Repeatability Demonstration:**
```
Input: BOQRow items with descriptions
Step 1: Count word frequencies across all item descriptions
Step 2: Sort by frequency descending
Step 3: Return {term: count} for top-K

Result: Always identical for same input
```

**Evidence Boundary:** This capability reports term frequencies. It does NOT:
- Classify terms as "engineering" vs "non-engineering"
- Assess importance or relevance
- Infer trade context from vocabulary
- Make any semantic judgment

---

### SEM-PROD-02: Head1 Text Categorization

**Rule:** Categorize each Head1 row as either "Administrative" (boilerplate) or "Trade-Specific" (work breakdown) based on exact text matching against a frozen administrative pattern list.

**Inputs:**
- `rows: list[BOQRow]` — extracted BOQ rows

**Outputs:**
- `head1_categorization: dict[str, list[dict]]` — mapping of category to list of Head1 entries, each with row_number and description
- `administrative_patterns_found: list[str]` — list of matched administrative patterns

**Administrative Category Patterns (frozen):**
```
GENERALLY
REFERENCES
PRICES
GENERAL ITEMS
NOTES AND ASSUMPTIONS
```

**Algorithm:**
1. For each row where `uom == "Head1"`:
   a. Normalize description text (strip whitespace, uppercase for matching)
   b. If text matches any administrative pattern → classify as "Administrative"
   c. Otherwise → classify as "Trade-Specific"
2. Group by classification, preserve row order

**Invariants:**

| ID | Category | Description | Violation |
|---|---|---|---|
| INV-H1C-01 | determinism | Same rows always produce same categorization | MAJOR |
| INV-H1C-02 | completeness | Every Head1 classified as Administrative or Trade-Specific | MAJOR |
| INV-H1C-03 | immutability | Output is never modified after creation | MAJOR |
| INV-H1C-04 | frozen_patterns | Administrative pattern list is frozen — never modified without EQ | MAJOR |

**Repeatability Demonstration:**
```
Input: Head1 rows with descriptions ["GENERALLY", "INSITU CONCRETE", "REFERENCES", "PILING"]
Step 1: Match each against frozen administrative patterns
Step 2: [GENERALLY → Administrative] [INSITU CONCRETE → Trade] [REFERENCES → Administrative] [PILING → Trade]
Output: Administrative: [GENERALLY, REFERENCES], Trade: [INSITU CONCRETE, PILING]

Result: Always identical for same input
```
---

### SEM-PROD-04: Administrative Pattern Detection (Boilerplate)

**Rule:** Detect the presence and sequence of administrative boilerplate patterns (Head1-level and Head2-level) within each trade section.

**Inputs:**
- `hierarchy: tuple[BOQHeaderNode, ...]` — reconstructed hierarchy (from existing Increment 2)

**Outputs:**
- `administrative_sections: dict[str, list[dict]]` — per-section mapping of administrative patterns found
- `missing_patterns: dict[str, list[str]]` — per-section list of expected but missing patterns

**Head1 Boilerplate Patterns (frozen):**
```
GENERALLY, REFERENCES, PRICES, GENERAL ITEMS, NOTES AND ASSUMPTIONS
```

**Head2 Boilerplate Patterns (frozen):**
```
Prices shall include for:
```

**Algorithm:**
1. For each section in the hierarchy:
   a. Collect all Head1 descriptions in order
   b. Match against frozen Head1 boilerplate patterns
   c. Check Head2 children for "Prices shall include for:"
   d. Record found/missing patterns
   e. Report sequence order

**Invariants:**

| ID | Category | Description | Violation |
|---|---|---|---|
| INV-ADM-01 | determinism | Same hierarchy always produces same findings | MAJOR |
| INV-ADM-02 | observation_only | Reports what IS present — not what SHOULD be present | MAJOR |
| INV-ADM-03 | immutability | Output is never modified after creation | MAJOR |
| INV-ADM-04 | frozen_templates | Template patterns are frozen — never modified without EQ | MAJOR |

**Repeatability Demonstration:**
```
Input: Hierarchy where Section F has Head1 entries [GENERALLY, REFERENCES, INSITU CONCRETE, PRICES]
Step 1: Check each Head1 against frozen templates
Step 2: Found: GENERALLY, REFERENCES, PRICES
Step 3: Missing: GENERAL ITEMS, NOTES AND ASSUMPTIONS

Result: Always identical for same input
```
---

### SEM-PROD-05: Section Code Enumeration

**Rule:** Enumerate all sections in the BOQ worksheet with their codes and names, preserving ordinal position.

**Inputs:**
- `rows: list[BOQRow]` — extracted BOQ rows

**Outputs:**
- `sections: tuple[dict[str, str | int], ...]` — ordered tuple of section entries, each with code, name, and row_number

**Algorithm:**
1. For each row where `row_type == "Section"`:
   a. Extract section code from Column A (single or dual-letter, already available via `BOQRow.code`)
   b. Extract section name from Column B (via `BOQRow.description`)
   c. Preserve original row order
2. Return ordered enumeration

**Invariants:**

| ID | Category | Description | Violation |
|---|---|---|---|
| INV-SCE-01 | determinism | Same rows always produce same section enumeration | MAJOR |
| INV-SCE-02 | ordering | Sections preserved in original worksheet order | MAJOR |
| INV-SCE-03 | completeness | All section rows are included | MAJOR |
| INV-SCE-04 | immutability | Output is never modified after creation | MAJOR |

**Repeatability Demonstration:**
```
Input: Rows with section entries [A/GROSS FLOOR AREA, B/DEMOLITION, C/SITE PREPARATION...]
Output: [(code: A, name: GROSS FLOOR AREA), (code: B, name: DEMOLITION), ...]

Result: Always identical for same input
```
---

### SEM-PROD-06: UOM Distribution Reporting

**Rule:** Compute the frequency distribution of Unit of Measure (UOM) values across all measured items in the BOQ.

**Inputs:**
- `rows: list[BOQRow]` — extracted BOQ rows

**Outputs:**
- `uom_distribution: dict[str, int]` — mapping of UOM string → count of items using that UOM
- `uom_percentages: dict[str, float]` — mapping of UOM string → percentage of total items

**Algorithm:**
1. Filter rows where `row_type == "Item"`
2. Count occurrences of each unique `uom` value
3. Compute total item count
4. Calculate percentages
5. Sort by count descending

**Invariants:**

| ID | Category | Description | Violation |
|---|---|---|---|
| INV-UOM-01 | determinism | Same items always produce same distribution | MAJOR |
| INV-UOM-02 | type | Counts are int, percentages are float | MAJOR |
| INV-UOM-03 | percentage_sum | Percentages sum to 100.0 within floating-point tolerance | MAJOR |
| INV-UOM-04 | immutability | Output is never modified after creation | MAJOR |

**Repeatability Demonstration:**
```
Input: 3606 items with UOMs [m2: 1217, no: 908, m3: 461, m: 454, Item: 351, t: 208, item: 6, UOM: 1]
Output: {m2: 1217, no: 908, m3: 461, m: 454, Item: 351, t: 208, item: 6, UOM: 1}
Percentages: {m2: 33.7%, no: 25.2%, m3: 12.8%, m: 12.6%, Item: 9.7%, t: 5.8%, item: 0.2%, UOM: 0.03%}

Result: Always identical for same input
```
---

### SEM-PROD-07: Header Level Count Distribution

**Rule:** Count rows at each hierarchy level (Head1, Head2, Head3, Head4) across the entire BOQ.

**Inputs:**
- `rows: list[BOQRow]` — extracted BOQ rows

**Outputs:**
- `header_distribution: dict[str, int]` — mapping of header level string to count
- Keys: `'Head1'`, `'Head2'`, `'Head3'`, `'Head4'`

**Algorithm:**
1. Filter rows where `row_type == "Head"` and `uom` starts with "Head" followed by digit 1-4
2. Count by exact uom value
3. Return distribution

**Invariants:**

| ID | Category | Description | Violation |
|---|---|---|---|
| INV-HD-01 | determinism | Same rows always produce same distribution | MAJOR |
| INV-HD-02 | completeness | Only Head1-4 counted (Head5 not observed in production) | MAJOR |
| INV-HD-03 | immutability | Output is never modified after creation | MAJOR |
| INV-HD-04 | consistency | Sum of counts equals total Head rows from row_classification | MAJOR |

**Repeatability Demonstration:**
```
Input: BOQ with Head rows [(Head1 x 294), (Head2 x 394), (Head3 x 627), (Head4 x 636)]
Output: {Head1: 294, Head2: 394, Head3: 627, Head4: 636}

Result: Always identical for same input
```
---

### SEM-PROD-09: "Items Always Quantify" Enforcement

**Rule:** Verify and report any header rows (Head1–Head4) that carry non-NULL quantities, enforcing the invariant that only Item rows carry quantities.

**Inputs:**
- `rows: list[BOQRow]` — extracted BOQ rows

**Outputs:**
- `header_quantity_violations: tuple[dict[str, int | str | float | None], ...]` — tuple of violation entries, each with: row_number, uom, description, quantity
- Empty tuple indicates invariant holds (no violations)

**Algorithm:**
1. Filter rows where `row_type == "Head"` and `uom` in Head1-4
2. For each header row, check if `quantity` is not None and quantity != 0
3. Report any header rows with non-NULL quantity as violations

**Invariants:**

| ID | Category | Description | Violation |
|---|---|---|---|
| INV-IAQ-01 | determinism | Same rows always produce same violations | MAJOR |
| INV-IAQ-02 | empty_default | Empty tuple when invariant holds | MAJOR |
| INV-IAQ-03 | immutability | Output is never modified after creation | MAJOR |
| INV-IAQ-04 | boundary | Reports observations — never assesses legitimacy | MAJOR |

**Repeatability Demonstration:**
```
Given: 3606 items all have quantities, 2037 headers all have NULL quantities
Input: All BOQRow entries
Check: For each Head row, is quantity non-NULL?
Result: Empty tuple (no violations)

Given: A header row with quantity = 5.0
Result: [(row_number: X, uom: Head1, description: ..., quantity: 5.0)]

Result: Always identical for same input
```
---

### SEM-PROD-12: Head1 Administrative Sub-Template Recognition

**Rule:** Detect the standard administrative sub-template sequence (GENERALLY → REFERENCES → PRICES → GENERAL ITEMS → NOTES AND ASSUMPTIONS) as a pattern within each section's Head1/Head2 entries.

**Inputs:**
- `rows: list[BOQRow]` — extracted BOQ rows

**Outputs:**
- `template_matches: dict[str, list[dict]]` — per-section mapping of template pattern occurrences
- Each match entry: pattern_name, matched_text, row_number, position_in_sequence

**Algorithm:**
1. For each section:
   a. Scan Head1 entries in order
   b. Match against template sequence: GENERALLY(optional) → REFERENCES(optional) → PRICES(optional) → GENERAL ITEMS(optional) → NOTES AND ASSUMPTIONS(optional)
   c. Record contiguous matches
   d. Report sequence completeness

**Invariants:**

| ID | Category | Description | Violation |
|---|---|---|---|
| INV-TMP-01 | determinism | Same rows always produce same template matches | MAJOR |
| INV-TMP-02 | ordering | Sequence matching respects worksheet order | MAJOR |
| INV-TMP-03 | immutability | Output is never modified after creation | MAJOR |
| INV-TMP-04 | frozen_templates | Template sequence is frozen — never modified without EQ | MAJOR |

**Repeatability Demonstration:**
```
Input: Section F Head1 entries [GENERALLY, REFERENCES, PRICES, INSITU CONCRETE, GENERAL ITEMS]
Check: Match sequential entries against template [GENERALLY, REFERENCES, PRICES, GENERAL ITEMS, NOTES]
Match: GENERALLY(position 1), REFERENCES(position 2), PRICES(position 3)
Partial: GENERAL ITEMS found at position 5 (non-contiguous — INSITU CONCRETE at position 4)
Missing: NOTES AND ASSUMPTIONS

Result: Always identical for same input
```
---

## Summary of Production Ready Capabilities

| ID | Capability | Rule Type | Input Source | Output Format |
|---|---|---|---|---|
| SEM-PROD-01 | Vocabulary extraction | Frequency counting | BOQRow descriptions | dict[str, int] |
| SEM-PROD-02 | Head1 text categorization | Pattern matching | BOQRow Head1 rows | dict[str, list] |
| SEM-PROD-04 | Admin pattern detection | Pattern matching | BOQHeaderNode hierarchy | dict[str, list] |
| SEM-PROD-05 | Section code enumeration | Direct extraction | BOQRow Section rows | tuple[dict] |
| SEM-PROD-06 | UOM distribution reporting | Frequency counting | BOQRow Item rows | dict[str, int] + percentages |
| SEM-PROD-07 | Header level count distribution | Frequency counting | BOQRow Head rows | dict[str, int] |
| SEM-PROD-09 | "Items Always Quantify" enforcement | Invariant checking | BOQRow rows | tuple[dict] |
| SEM-PROD-12 | Admin sub-template recognition | Sequence matching | BOQRow Head1/Head2 | dict[str, list] |

## Repeatability Confirmation

All 8 Production Ready capabilities share these properties:
- **Pure function** — no side effects, no external state
- **Deterministic** — identical inputs produce identical outputs
- **Observation only** — reports what IS present, not what SHOULD be present
- **No AI/heuristics** — exact matching, counting, or direct extraction
- **No domain knowledge** — operates entirely over explicit BOQRow fields
- **Boundary preserved** — never crosses into assessment territory

---

## Document Control

**Version:** 1.0
**Spike:** 3 of 7
**EQ:** EQ-0019
**Status:** Complete
**Last Updated:** 2026-07-25
**Owner:** Project Owner