# Spike 2 — Capability Classification

## EQ-0019 BOQ Semantic Intelligence Increment 1

### Purpose
Classify every discovered capability from EQ-0018 into: Production Ready, Needs Additional Evidence, Consumer Feature, Future Research, or Rejected. Every classification requires evidence.

### Classification Categories

| Category | Definition |
|---|---|
| **Production Ready** | Sufficient evidence exists, deterministic rules can be defined, no domain knowledge required, architecture compatible |
| **Needs Additional Evidence** | Promising capability but insufficient evidence for production (needs more fixtures, domain verification, or cross-trade analysis) |
| **Consumer Feature** | Valuable to consumers but requires consumer-specific design decisions first |
| **Future Research** | Requires new Engineering Question or spike investigation |
| **Rejected** | Evidence demonstrates this capability cannot be deterministic, violates architecture, or duplicates existing functionality |

---

## 1. Capability Classifications

### SEM-PROD-01: Vocabulary Extraction (term frequency)

**Classification: Production Ready**

**Evidence:**
- EQ-0018 §6 documents 30 recurring engineering terms with exact frequencies
- `semantic_pattern_analysis.py` implements deterministic vocabulary extraction via `extract_vocabulary()` (lines 233-267)
- Pure frequency counting — no AI, no heuristics, no domain judgment
- Input: `list[BOQRow]` description fields
- Output: `dict[str, int]` mapping terms to occurrence counts
- Cross-trade verification confirms vocabulary terms appear consistently

**Determinism:** Pure function — same descriptions produce same frequency counts
**Architecture:** Fits within existing `analyze_boq()` pure function pattern
**Contract Impact:** New optional field in BOQIntelligenceResult (MINOR addition)

---

### SEM-PROD-02: Head1 Text Categorization (administrative vs trade)

**Classification: Production Ready**

**Evidence:**
- EQ-0018 §7 documents the Head1 administrative template pattern
- EQ-0018 §9 confirms pattern across all 16 trade-specific fixtures
- 5 administrative categories identified: GENERALLY, REFERENCES, PRICES, GENERAL ITEMS, NOTES AND ASSUMPTIONS
- `semantic_pattern_analysis.py` implements categorization in `extract_hierarchy_patterns()` (lines 287-323) with deterministic category mapping
- Rule-based pattern matching — no AI, no probabilistic reasoning

**Determinism:** Pure function — matches Head1 text against known patterns
**Architecture:** Fits within existing `analyze_boq()` — produces observation-only categorization
**Contract Impact:** New optional field in BOQIntelligenceResult (MINOR addition)

---

### SEM-PROD-03: Description Tag Extraction

**Classification: Needs Additional Evidence**

**Evidence:**
- EQ-0018 §9 notes: "Item tags (e.g., PF1, CT1) appear in descriptions"
- EQ-0018 Design Rule #6: "Descriptions embed tags but not hierarchy"
- However, no systematic tag pattern analysis was performed across all 3606 items
- Tag format, position, and semantics are not fully documented
- Cross-trade tag consistency is NOT confirmed

**Rationale for Deferral:**
- Insufficient evidence about tag format conventions
- No documented tag taxonomy or glossary
- Risk of over-generalizing from observed examples
- Requires dedicated spike on tag pattern analysis

---

### SEM-PROD-04: Administrative Pattern Detection (boilerplate)

**Classification: Production Ready**

**Evidence:**
- EQ-0018 §7 documents complete boilerplate template
- EQ-0018 §9 confirms: "Every trade begins with boilerplate Head1 entries" and "Every trade uses 'Prices shall include for:' as Head2"
- Confirmed across all 16 trade-specific fixtures (universal pattern)
- Deterministic: explicitly check Head1 text against known boilerplate texts
- Pattern: [REFERENCES, GENERALLY, PRICES, GENERAL ITEMS, NOTES AND ASSUMPTIONS]

**Determinism:** Pure function — exact string matching against frozen boilerplate list
**Architecture:** Fits within `analyze_boq()` as additional observation evidence
**Contract Impact:** New optional field in BOQIntelligenceResult (MINOR addition)

---

### SEM-PROD-05: Section Code Enumeration (code → name mapping)

**Classification: Production Ready**

**Evidence:**
- EQ-0018 §3 documents 61 section codes from A to BI with names
- Section codes are explicitly provided in Column A of the worksheet
- Deterministic: extract section code + section name from section rows
- No inference, no mapping table, no domain knowledge required
- Direct structural observation

**Determinism:** Pure function — same worksheet produces same section list
**Architecture:** Fits within existing `_compute_section_stats()` pattern
**Contract Impact:** Existing `section_statistics` field can be extended (MINOR addition)

---

### SEM-PROD-06: UOM Distribution Reporting

**Classification: Production Ready**

**Evidence:**
- EQ-0018 §5 documents 8 unique UOMs with exact counts and percentages
- UOM is explicitly provided in Column D for leaf items
- `semantic_pattern_analysis.py` extracts UOM patterns in `extract_uom_patterns()` (lines 220-230)
- Pure counting — no AI, no domain judgment
- Deterministic: same items produce same distribution

**Determinism:** Pure function — frequency counting over UOM field
**Architecture:** Fits within `analyze_boq()` as additional observation evidence
**Contract Impact:** New optional field in BOQIntelligenceResult (MINOR addition)

---

### SEM-PROD-07: Header Level Count Distribution

**Classification: Production Ready**

**Evidence:**
- EQ-0018 §4 documents Head1 (294), Head2 (394), Head3 (627), Head4 (636) counts
- Hierarchy levels are explicitly declared in Column D
- Deterministic: count rows by Head1–Head4 label
- Already partially implemented in `row_classification` (counts Head as aggregate)
- This capability adds per-level breakdown

**Determinism:** Pure function — counts rows by explicit Column D labels
**Architecture:** Fits within existing `_count_row_types()` — extend with per-level breakdown
**Contract Impact:** Existing `row_classification` field extension (MINOR addition — adding new key)

---

### SEM-PROD-08: Cross-Trade Pattern Verification

**Classification: Needs Additional Evidence**

**Evidence:**
- EQ-0018 §9 identifies 6 universal patterns across 16 fixtures
- However, only 16 of 61 possible trade sections were verified
- Main fixture (full_boq.xlsx) contains 61 sections not all independently verified for pattern consistency
- Some patterns (e.g., description tag format) need more systematic analysis
- Cross-trade pattern verification is valuable but requires fixture expansion

**Rationale for Deferral:**
- Only 16 of 61 sections verified as trade-specific fixtures
- Pattern universality claim needs broader evidence base
- Risk: patterns observed in 16 fixtures may not generalize to all 61

---

### SEM-PROD-09: "Items Always Quantify" Enforcement

**Classification: Production Ready**

**Evidence:**
- EQ-0018 §10 reclassifies SEM-003 from Domain Dependent → Structurally Deterministic
- Evidence: 0 of 2037 header rows carry quantities; 3606 items all carry quantities
- Deterministic: verify that every row with Head1–Head4 in Column D has NULL quantity
- Already implicit in existing hierarchy reconstruction (no header row carries items)
- Can be formalized as an invariant check

**Determinism:** Pure function — check invariant over BOQRow list
**Architecture:** Fits within existing detection evidence pattern (like `_detect_zero_quantities`)
**Contract Impact:** New optional detection field in BOQIntelligenceResult (MINOR addition)

---

### SEM-PROD-10: Items-Per-Section Distribution

**Classification: Needs Additional Evidence**

**Evidence:**
- EQ-0018 §3 and §4 provide section counts and item counts
- Items-per-section is derivable from existing BOQRow data
- However, no systematic items-per-section analysis was performed in EQ-0018
- Consumer value is unclear — not yet requested by any consumer

**Rationale for Deferral:**
- Not requested by any consumer (CheckMate, Formatter, Builder, Reporting)
- Derivable from existing evidence (section_statistics + row_classification)
- YAGNI — implement when consumer needs it

---

### SEM-PROD-11: Note Frequency Distribution by Section

**Classification: Consumer Feature**

**Evidence:**
- EQ-0018 §4 documents 520 notes total
- Notes are assigned to sections via parent section context
- Derivable from BOQRow data (filter note rows + group by section)
- Consumer value depends on CheckMate requirements

**Rationale for Consumer Feature Classification:**
- Valuable for CheckMate's note review feature (planned)
- Not valuable as standalone BOQ Intelligence capability
- Should be implemented as part of CheckMate consumer design
- Current note detection already exists in `row_classification`

---

### SEM-PROD-12: Head1 Administrative Sub-Template Recognition

**Classification: Production Ready**

**Evidence:**
- EQ-0018 §7 documents the full sub-template: GENERALLY → REFERENCES → PRICES → GENERAL ITEMS → NOTES AND ASSUMPTIONS
- This pattern repeats for each location (NORTH BUILDING, SOUTH BUILDING)
- Deterministic: check Head1 and Head2 text sequence against frozen template
- Confirmed across 16 trade fixtures
- Pure rule-based matching

**Determinism:** Pure function — sequence matching of Header texts against template
**Architecture:** Fits within `analyze_boq()` as additional observation
**Contract Impact:** New optional field in BOQIntelligenceResult (MINOR addition)

---

## 2. Classification Summary

### 2.1 Production Ready (8 capabilities)

| ID | Capability |
|---|---|
| SEM-PROD-01 | Vocabulary extraction (term frequency) |
| SEM-PROD-02 | Head1 text categorization (administrative vs trade) |
| SEM-PROD-04 | Administrative pattern detection (boilerplate) |
| SEM-PROD-05 | Section code enumeration (code → name mapping) |
| SEM-PROD-06 | UOM distribution reporting |
| SEM-PROD-07 | Header level count distribution |
| SEM-PROD-09 | "Items Always Quantify" enforcement |
| SEM-PROD-12 | Head1 administrative sub-template recognition |

### 2.2 Needs Additional Evidence (3 capabilities)

| ID | Capability | Blockers |
|---|---|---|
| SEM-PROD-03 | Description tag extraction | Insufficient tag pattern analysis, no tag taxonomy |
| SEM-PROD-08 | Cross-trade pattern verification | Only 16/61 sections verified, needs fixture expansion |
| SEM-PROD-10 | Items-per-section distribution | No consumer request, YAGNI applies |

### 2.3 Consumer Feature (1 capability)

| ID | Capability | Rationale |
|---|---|---|
| SEM-PROD-11 | Note frequency distribution by section | Valuable for CheckMate note review, not as standalone intelligence |

### 2.4 Future Research (0 capabilities)

No capabilities classified as Future Research.

### 2.5 Rejected (0 capabilities)

No capabilities classified as Rejected.

---

## 3. Classification Summary Table

| ID | Capability | Classification | Primary Evidence |
|---|---|---|---|
| SEM-PROD-01 | Vocabulary extraction | **Production Ready** | EQ-0018 §6 |
| SEM-PROD-02 | Head1 text categorization | **Production Ready** | EQ-0018 §7, §9 |
| SEM-PROD-03 | Description tag extraction | Needs Additional Evidence | EQ-0018 §9 |
| SEM-PROD-04 | Admin pattern detection | **Production Ready** | EQ-0018 §7, §9 |
| SEM-PROD-05 | Section code enumeration | **Production Ready** | EQ-0018 §3 |
| SEM-PROD-06 | UOM distribution reporting | **Production Ready** | EQ-0018 §5 |
| SEM-PROD-07 | Header level count distribution | **Production Ready** | EQ-0018 §4 |
| SEM-PROD-08 | Cross-trade pattern verification | Needs Additional Evidence | EQ-0018 §9 |
| SEM-PROD-09 | "Items Always Quantify" | **Production Ready** | EQ-0018 §4, §10 |
| SEM-PROD-10 | Items-per-section distribution | Needs Additional Evidence | EQ-0018 §3, §4 |
| SEM-PROD-11 | Note frequency by section | Consumer Feature | EQ-0018 §4 |
| SEM-PROD-12 | Admin sub-template recognition | **Production Ready** | EQ-0018 §7 |

---

## Document Control

**Version:** 1.0
**Spike:** 2 of 7
**EQ:** EQ-0019
**Status:** Complete
**Last Updated:** 2026-07-25
**Owner:** Project Owner