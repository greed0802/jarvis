# Spike 1 — Evidence Inventory Review

## EQ-0019 BOQ Semantic Intelligence Increment 1

### Purpose
Review every engineering conclusion from EQ-0018. Catalogue hierarchy roles, vocabulary extraction, section semantics, recurring engineering patterns, and structural observations. Produce a capability inventory.

### Evidence Source
EQ-0018 — BOQ Semantic Intelligence (COMPLETED)

---

## 1. Capability Inventory from EQ-0018

### 1.1 Reclassified Capabilities

EQ-0018 reclassified two capabilities from EQ-0011's original classification:

| ID | Capability | EQ-0011 Classification | EQ-0018 Reclassification | Evidence |
|---|---|---|---|---|
| SEM-003 | "Items Always Quantify" | Domain Dependent | **Structurally Deterministic** | 0 of 2037 header rows (Head1–Head4) carry quantities. 3606 measured items all carry quantities. Observable fact across production fixture. |
| V-003 | Level Progression Validation | Domain Dependent | **Structurally Deterministic** | Hierarchy labels are explicit in Column D. Parent-child relationships validated through stack-based algorithm from EQ-0010. |

### 1.2 Confirmed Design Rules (6 total)

| # | Rule | Determinism | Evidence |
|---|---|---|---|
| 1 | No measured items at Head1–Head4 | Structurally Deterministic | All header rows have NULL quantity. Only leaf items (UOM rows) carry quantities. |
| 2 | Five-level hierarchy maximum | Structurally Deterministic | Section → Head1 → Head2 → Head3 → Head4 is deepest observed nesting. |
| 3 | Section codes are not data types | Structurally Deterministic | Section codes (A–Z, AA–BI) are sequential enumerations, not data fields. |
| 4 | Hierarchy labels are explicit in Column D | Structurally Deterministic | BOQ explicitly declares each row's hierarchy role via Column D labels. |
| 5 | Item codes encode the section | Structurally Deterministic | Item code prefix (e.g., F/ from Section F) links items to parent section. |
| 6 | Descriptions embed tags but not hierarchy | Semantically Deterministic | Item tags (e.g., PF1, CT1) appear in descriptions but hierarchy must be reconstructed from Column D labels. |

### 1.3 Semantic Boundary Classification (12 entries)

| Capability | Classification | Basis |
|---|---|---|
| Hierarchy label detection | **Structurally Deterministic** | Column D explicitly provides Head1–Head4 labels |
| Section code detection | **Structurally Deterministic** | Column A provides single/dual-letter codes |
| Item code parsing | **Structurally Deterministic** | Pattern `[Code]/[Number]` |
| UOM extraction | **Structurally Deterministic** | Explicit in Column D for leaf items |
| Vocabulary extraction | **Semantically Deterministic** | Pure frequency counting over description text |
| Head1 text categorization | **Semantically Deterministic** | Rule-based matching of known administrative patterns |
| Level progression validation | **Structurally Deterministic** | Column D hierarchy labels provide clear parent-child relationships |
| Scope containment (structural) | **Structurally Deterministic** | Section boundaries defined by Column A codes |
| "Items Always Quantify" | **Structurally Deterministic** | Observable: 0 of 2037 header rows have quantities |
| Zero-quantity detection | **Structurally Deterministic** | Fact detection over Column C |
| Scope containment (semantic) | **Professional Judgment** | Requires understanding of trade scope boundaries |
| Completeness (full QS) | **Professional Judgment** | Requires project scope knowledge |

### 1.4 Structural Feature Map

| Feature | Value |
|---|---|
| Workbook structure | Single-worksheet per workbook |
| Column A | Item reference code |
| Column B | Description text |
| Column C | Quantity |
| Column D | UOM OR hierarchy label (Head1–Head5, Note) |
| Section breaks | Single-letter codes (A–Z) and two-letter codes (AA–BI) |
| Total sections (full_boq) | 61 codes from A to BI |
| Repeated sections | AV–BI represent NORTH vs SOUTH building variations |

### 1.5 Hierarchy Depth and Frequencies

| Level | Count (full_boq) | Has Quantity? |
|---|---|---|
| Head1 | 294 | NO |
| Head2 | 394 | NO |
| Head3 | 627 | NO |
| Head4 | 636 | NO |
| Item | 3606 | YES |
| Notes | 520 | NO |

### 1.6 UOM Pattern Distribution

| UOM | Count | Percentage |
|---|---|---|
| m2 | 1217 | 33.7% |
| no | 908 | 25.2% |
| m3 | 461 | 12.8% |
| m | 454 | 12.6% |
| Item | 351 | 9.7% |
| t | 208 | 5.8% |
| item | 6 | 0.2% |
| UOM | 1 | 0.03% |

### 1.7 Recurring Engineering Vocabulary (Top 30)

| Term | Count | Domain Context |
|---|---|---|
| Finish | 446 | Finish specification in item descriptions |
| Concrete | 427 | Concrete grade, slump, aggregate specifications |
| Column | 374 | Element type reference |
| Allow | 368 | "Prices shall include for:" allowance descriptions |
| Formwork | 300 | Formwork class references |
| Aluminium | 258 | Aluminium windows, frames, sections |
| Wall | 167 | Wall references |
| Slab | 148 | Slab references |
| Reinforcement | 140 | Reinforcement specifications |
| Glazing | 111 | Glazing references |
| Bar | 108 | Reinforcement bar references |
| Beam | 104 | Beam references |
| Stair | 98 | Stair references |
| Steel | 83 | Steelwork references |
| Fire | 56 | Fire rating, fire protection |
| Soffit | 27 | Soffit references |
| Pipe | 21 | Pipe references |
| Floor | 20 | Floor references |
| Blockwork | 20 | Blockwork references |
| Excavation | 19 | Excavation references |
| Pile | 18 | Pile references |
| Footing | 17 | Footing references |
| Fabric | 15 | Fabric reinforcement |
| Insulation | 13 | Insulation references |
| Site | 11 | Site references |
| Drainage | 11 | Drainage references |
| Cost | 9 | Prime Cost references |
| Joinery | 6 | Joinery references |
| Mesh | 6 | Mesh reinforcement |
| Electrical | 5 | Electrical references |

### 1.8 Head1 Administrative Pattern Template

```
[TRADE SECTION TITLE]
├── GENERALLY
├── REFERENCES
├── PRICES
├── GENERAL ITEMS
├── NOTES AND ASSUMPTIONS
├── [Location 1] e.g. NORTH BUILDING
│   ├── GENERALLY
│   ├── REFERENCES
│   ├── PRICES
│   ├── GENERAL ITEMS
│   ├── [Trade-specific sub-headers]
│   └── NOTES AND ASSUMPTIONS
└── [Location 2] e.g. SOUTH BUILDING
    └── [same sub-pattern]
```

### 1.9 Hierarchy Semantic Roles

| Level | Role | Example |
|---|---|---|
| Section (A-Z, AA-BI) | Top-level trade breakdown | "IN-SITU CONCRETE" |
| Head1 | Conceptual grouping within trade | "GENERALLY", "CONCRETE SUPPLY SUMMARY" |
| Head2 | Sub-grouping of items | "Gross building areas", "Prices shall include for:" |
| Head3 | Element/assembly type | "Footing", "Lift Pit", "Boring" |
| Head4 | Specific element variant | "Pile Cap Footing (50MPa...)" |
| Item (UOM row) | Measurable work item | "F/1 - 40MPa concrete in columns" |

### 1.10 Cross-Trade Pattern Observations

| Pattern | Scope | Determinism |
|---|---|---|
| Every trade begins with boilerplate Head1 entries | Universal (16/16 fixtures) | Semantically Deterministic |
| Every trade uses "Prices shall include for:" as Head2 | Universal (16/16 fixtures) | Semantically Deterministic |
| Item codes follow pattern [SectionCode]/[Number] | Universal | Structurally Deterministic |
| Description pattern: Tag – Dimensions, Description | Universal | Semantically Deterministic |
| All hierarchy levels use Column D for UOM/label | Universal | Structurally Deterministic |
| Notes interspersed at any level with Note in Column D | Universal | Structurally Deterministic |

---

## 2. Capability Inventory Summary

### 2.1 Structurally Deterministic (9 capabilities)

1. **Hierarchy label detection** — Column D provides Head1–Head4 labels
2. **Section code detection** — Column A provides single/dual-letter codes
3. **Item code parsing** — Pattern `[Code]/[Number]`
4. **UOM extraction** — Explicit in Column D for leaf items
5. **Level progression validation** — Column D labels provide parent-child relationships
6. **Scope containment (structural)** — Section boundaries defined by Column A codes
7. **"Items Always Quantify"** — Observable: 0 of 2037 header rows have quantities
8. **Zero-quantity detection** — Fact detection over Column C
9. **Header count frequencies** — Count by level (Head1–Head4) from EQ-0018 data

### 2.2 Semantically Deterministic (4 capabilities)

1. **Vocabulary extraction** — Pure frequency counting over description text
2. **Head1 text categorization** — Rule-based matching of known administrative patterns
3. **Description tag extraction** — Item tags like PF1, CT1 embedded in descriptions
4. **Administrative pattern detection** — Boilerplate Head1/Head2 identification

### 2.3 Professional Judgment (2 capabilities)

1. **Scope containment (semantic)** — Requires understanding of trade scope boundaries
2. **Completeness (full QS)** — Requires project scope knowledge

### 2.4 Already in Production Contract (existing evidence fields)

The following capabilities are already implemented in `BOQIntelligenceResult` per Evidence Contract v1.0:
- Hierarchy label detection → via `_extract_head_level()` (already implemented)
- Level progression validation → via `_detect_level_skips()` (already implemented)
- Zero-quantity detection → via `_detect_zero_quantities()` (already implemented)
- Scope containment (structural) → via `_detect_structural_containment()` (already implemented)
- "Items Always Quantify" → Observable design rule, implicit in hierarchy reconstruction

### 2.5 New Capabilities Not Yet in Production

The following capabilities from EQ-0018 are NOT yet implemented in production code:
- **Vocabulary extraction** — Frequency counting over description text
- **Head1 text categorization** — Rule-based matching of administrative patterns
- **Description tag extraction** — Tag pattern detection
- **Administrative pattern detection** — Boilerplate identification
- **Section code system enumeration** — Section code → name mapping (A = "GROSS FLOOR AREA")
- **UOM pattern distribution reporting** — UOM frequency distribution
- **Header count reporting** — Count of headers at each level
- **Cross-trade pattern verification** — Universal pattern detection

---

## 3. Capability Inventory (Formal)

| ID | Capability | EQ-0018 Evidence | Current State |
|---|---|---|---|
| SEM-PROD-01 | Vocabulary extraction (term frequency) | EQ-0018 §6 — Top 30 terms with counts | Not in production |
| SEM-PROD-02 | Head1 text categorization (administrative vs trade) | EQ-0018 §7 — Boilerplate template | Not in production |
| SEM-PROD-03 | Description tag extraction | EQ-0018 §9 — Tag patterns in descriptions | Not in production |
| SEM-PROD-04 | Administrative pattern detection (boilerplate) | EQ-0018 §7, §9 — Cross-trade boilerplate | Not in production |
| SEM-PROD-05 | Section code enumeration (code → name mapping) | EQ-0018 §3 — 61 codes A–BI | Not in production |
| SEM-PROD-06 | UOM distribution reporting | EQ-0018 §5 — 8 UOMs with percentages | Not in production |
| SEM-PROD-07 | Header level count distribution | EQ-0018 §4 — Head1–Head4 frequencies | Not in production |
| SEM-PROD-08 | Cross-trade pattern verification | EQ-0018 §9 — Universal patterns | Not in production |
| SEM-PROD-09 | "Items Always Quantify" enforcement | EQ-0018 §4, §10 — Reclassified evidence | Implicit in existing |
| SEM-PROD-10 | Items-per-section distribution | EQ-0018 §3, §4 — Section/item correlation | Not in production |
| SEM-PROD-11 | Note frequency distribution by section | EQ-0018 §4 — 520 notes total | Not in production |
| SEM-PROD-12 | Head1 administrative sub-template recognition | EQ-0018 §7 — GENERALLY/REFERENCES/PRICES/GENERAL ITEMS/NOTES | Not in production |

---

## 4. Evidence Integrity Confirmation

All data in this inventory is directly traceable to:
- `docs/engineering/questions/EQ_0018_BOQ_Semantic_Intelligence.md` — 348 lines of documented evidence
- `tools/semantic_pattern_analysis.py` — Analysis tool (521 lines)
- Primary fixture: `full_boq.xlsx` (3606 items)
- 16 trade-specific fixtures

**Verification:** All counts confirmed by running `semantic_pattern_analysis.py` at the time of this report.

---

## Document Control

**Version:** 1.0
**Spike:** 1 of 7
**EQ:** EQ-0019
**Status:** Complete
**Last Updated:** 2026-07-25
**Owner:** Project Owner