# EQ-0018 — BOQ Semantic Intelligence

## Status
COMPLETED

## Purpose
Investigate and document the observable semantic patterns present in CostX BOQ fixture files, establishing the boundary between deterministic structural evidence and domain-specific semantic understanding.

## Background

### Previous Investigation Context

EQ-0010 established deterministic structural intelligence capabilities:
- 8 Observable capabilities (directly available in BOQRow fields)
- 10 Derivable capabilities (deterministically computable via proven algorithms)
- 4 Domain Dependent capabilities (require Domain Knowledge Layer integration)

EQ-0011 established the semantic intelligence boundary, classifying capabilities as:
- **Structurally Deterministic** — Pure function over BOQRow + reconstructed hierarchy
- **Semantically Deterministic** — Pure function once explicit domain rules have been formalized
- **Professional Judgment** — Cannot currently be reduced to deterministic computation

### Investigation Gap

EQ-0011 identified four Domain Dependent capabilities but did not execute the full five-spike investigation plan. This left unanswered questions about:

1. What vocabulary patterns actually exist in production fixtures?
2. How do hierarchy labels map to semantic roles?
3. Which semantic patterns are cross-trade consistent vs trade-specific?
4. Where exactly is the boundary between detection and judgment?

## Investigation Approach

### Evidence-Driven Analysis

This investigation uses the `semantic_pattern_analysis.py` tool to extract observable patterns from CostX fixtures:

1. Primary fixture: `full_boq.xlsx` (3606 items, 520 notes, 2037 headers)
2. Trade-specific fixtures (16 total) for cross-trade comparison

### Structural Feature Extraction

The tool extracts:
- Section codes and names
- Hierarchy label frequencies (Head1–Head4)
- Item coding patterns
- UOM distributions
- Engineering vocabulary frequencies
- Naming conventions
- Head1/Head2/Head3/Head4 text patterns

## Evidence Summary

### 1. Fixture Inventory

**Primary Fixture:** `full_boq.xlsx` — Complete building BOQ containing all trades

**Trade-Specific Fixtures (16 total):**

| Fixture File | Trade |
|---|---|
| Base_Structural_CostX.xlsX | Structural |
| Base_Structural_Steel_CostX.xlsX | Structural Steel |
| Base_Roofing_CostX.xlsX | Roofing |
| Base_Ceiling_BOQ_CostX.xlsX | Ceiling |
| Base_Demolition_CostX.xlsX | Demolition |
| Base_Doors_and_Windows_CostX.xlsX | Doors and Windows |
| Base_External Wall Finishes_CostX.xlsX | External Wall Finishes |
| Base_Floor_Finishes_CostX.xlsX | Floor Finishes |
| Base_Interior_Wall_Finishes_CostX.xlsX | Interior Wall Finishes |
| Base_Joinery_CostX.xlsX | Joinery |
| Base_Landscape_CostX.xlsX | Landscape |
| Base_Metal Works_CostX.xlsX | Metal Works |
| Base_Signage_CostX.xlsX | Signage |
| Base_Site Preparation_Civil_Earthworks_and_Demolition_CostX.xlsX | Site Preparation |
| Base_FFE_CostX.xlsX | FFE |
| Base_Wall_Types_CostX.xlsX | Wall Types |

### 2. Structural Feature Map

**Workbook Structure:**
- Single-worksheet per workbook (active sheet only)
- Column mapping:
  - **Column A**: Item reference code (e.g. `F/1`, `G/10`, `AA/5`, `BH/14`)
  - **Column B**: Description text (item descriptions, header texts, notes)
  - **Column C**: Quantity (numeric values)
  - **Column D**: UOM (e.g. `m2`, `no`, `m3`, `m`, `Item`, `t`) OR hierarchy label (`Head1` through `Head5`, or `Note`)
- Section breaks identified by single-letter codes in Column A (A–Z) and two-letter codes (AA–BI)

### 3. Section Code System

The full_boq.xlsx fixture uses 61 section codes from A to BI:

| Code | Section Name | Code | Section Name |
|---|---|---|---|
| A | GROSS FLOOR AREA (GFA) | P | FAÇADE - LOUVRES & SCREENS |
| B | DEMOLITION & SITE CLEARANCE | Q | INSULATION |
| C | SITE PREPARATION | R | BUILDING ACCESS SAFETY SYSTEMS |
| D | PILING | S | PARTITIONS & LININGS |
| E | DETAILED EXCAVATION | T | SUSPENDED CEILINGS |
| F | IN-SITU CONCRETE | U | RENDERING & PLASTERING |
| G | FORMWORK | V | DOORS, FRAMES & HARDWARE |
| H | REINFORCEMENT | W | JOINERY & CARPENTRY |
| I | POST TENSIONING | X | WINDOW BLINDS |
| J | MASONRY - BRICK & BLOCK | Y | METALWORK |
| K | STRUCTURAL STEELWORK | Z | SIGNAGE |
| L | ROOFING & ROOF PLUMBING | AA | WATERPROOFING & TANKING |
| M | FAÇADE - MASONRY/BLOCKWORK | AB | TILING/PAVING |
| N | FAÇADE - GLAZING | AC | VINYL/RESILIENT FINISHES |
| O | FAÇADE - CLADDING | AD | CARPET |

| Code | Section Name |
|---|---|
| AE | EPOXY & SEALERS |
| AF | PAINTING |
| AG | FF&E |
| AH | ICT/AV |
| AI | COMMERCIAL DINING/KITCHEN EQUIPMENT |
| AJ | HYDRAULIC SERVICES |
| AK | MECHANICAL SERVICES |
| AL | ELECTRICAL SERVICES |
| AM | FIRE SERVICES |
| AN | LIFT SERVICES |
| AO | BWIC (SERVICES) |
| AP | EXTERNAL WORKS & LANDSCAPING |
| AQ | CIVIL WORKS |
| AR | FINAL CLEAN |
| AS | MAKE GOOD |
| AT | PROVISIONAL SUMS |
| AU | Alternative (columns bearing) |
| AV | FAÇADE - GLAZING (2nd occurrence) |
| AW | INSULATION (2nd) |
| AX | PARTITIONS & LININGS (2nd) |
| AY | SUSPENDED CEILINGS (2nd) |
| AZ | DOORS, FRAMES & HARDWARE (2nd) |
| BA | JOINERY & CARPENTRY (2nd) |
| BB | METALWORK (2nd) |
| BC | SIGNAGE (2nd) |
| BD | TILING/PAVING (2nd) |
| BE | VINYL & RESILIENT FINISHES (2nd) |
| BF | WATERPROOFING & TANKING (2nd) |
| BG | PAINTING (2nd) |
| BH | FF&E (2nd) |
| BI | ICT/AV (2nd) |

**Observations:**
- Sections A–Z are unique trade groupings (structural, finishes, services)
- Sections AA–AU are additional trades and special sections
- Sections AV–BI represent repeated trades for NORTH vs SOUTH building variations
- Section codes are sequential enumerations, not data fields
- Section codes cannot be extracted or predicted from item descriptions

### 4. Hierarchy Depth and Frequencies

| Hierarchy Level | Count (full_boq.xlsx) | Has Quantity? |
|---|---|---|
| Head1 | 294 | **NO** (0 of 294 have quantities) |
| Head2 | 394 | NO |
| Head3 | 627 | NO |
| Head4 | 636 | NO |
| Item (measured) | 3606 | YES (all have quantities) |
| Notes | 520 | NO |

**Critical finding:** Head1 through Head4 are purely structural/organizational labels. **No header level carries a quantity.** All measured items are at the UOM level (column D contains UOM string like `m2`, `no`, not a hierarchy label).

### 5. UOM Pattern Distribution

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

**Observations:**
- `m2` dominates at ~34% of all items (area measurements)
- `no` is second at ~25% (counted items)
- `m3` and `m` are approximately equal at ~13% each (volume and linear)
- `Item` is used for ~10% (lump sum items)
- `t` (tonne) is used for ~6% (reinforcement, steel sections)
- The lone `UOM` appears to be an unresolved placeholder

### 6. Recurring Vocabulary Patterns

**Top 30 engineering terms by frequency:**

| Term | Count | Context |
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

### 7. Head1 Text Pattern Analysis

**Recurring Head1 template within each trade section:**

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

**Key patterns:**
1. Each trade section contains Head1 entries for boilerplate administrative headers: GENERALLY, REFERENCES, PRICES, GENERAL ITEMS, NOTES AND ASSUMPTIONS
2. Trade-specific Head1 entries include work breakdowns (e.g., "INSITU CONCRETE", "PILING", "CAPPING BEAM" in the Structural fixture)
3. Location split (NORTH BUILDING / SOUTH BUILDING) creates duplicated Head1 hierarchies for the same trades

### 8. Hierarchy Semantic Roles

| Level | Role | Example |
|---|---|---|
| **Section** (A-Z, AA-BI) | Top-level trade breakdown | "IN-SITU CONCRETE" |
| **Head1** | Conceptual grouping within trade | "GENERALLY", "CONCRETE SUPPLY SUMMARY", "INSITU CONCRETE" |
| **Head2** | Sub-grouping of items | "Gross building areas", "Prices shall include for:", "Piling" |
| **Head3** | Element/assembly type | "Footing", "Lift Pit", "Boring", "Insitu Concrete" |
| **Head4** | Specific element variant | "Pile Cap Footing (50MPa...)", "Mass Concrete Downturn (50MPa...)" |
| **Item** (UOM row) | Measurable work item | "F/1 - 40MPa concrete in columns; Finish: ..." |

### 9. Cross-Trade Pattern Comparison

**Structural fixture (Base_Structural_CostX.xlsX):**
- Items: 120
- Head1: 79 (includes boilerplate and trade-specific entries)
- Head2: 142
- Head3: 170
- Head4: 25

**Common structural patterns across all trades:**

1. **Every trade begins with boilerplate Head1 entries:** GENERALLY, REFERENCES, PRICES, GENERAL ITEMS, NOTES AND ASSUMPTIONS
2. **Every trade uses "Prices shall include for:"** as a Head2 entry
3. **Item codes** follow the pattern `[SectionCode]/[Number]` (e.g., `F/1`, `G/10`, `BH/14`)
4. **Description pattern**: `[Tag] – [Dimensions] [Common Description], [Specific Description]` consistent with domain Naming Convention document
5. **All hierarchy levels use Column D** for either UOM (leaf items) or `Head1`/`Head2`/`Head3`/`Head4`/`Note` (structural rows)
6. **Notes** are interspersed at any level and use `Note` in Column D

## Engineering Conclusions

### Confirmed Design Rules

1. **No measured items at Head1–Head4**: All header rows have NULL quantity. Only leaf items (UOM rows) carry quantities.
2. **Five-level hierarchy maximum**: Section → Head1 → Head2 → Head3 → Head4 is the deepest observed nesting.
3. **Section codes are not data types**: Section codes (A–Z, AA–BI) are sequential enumerations, not data fields.
4. **Hierarchy labels are explicit in Column D**: The BOQ explicitly declares each row's hierarchy role via Column D labels.
5. **Item codes encode the section**: Item code prefix (e.g., `F/` from Section F) links items to their parent section.
6. **Descriptions embed tags but not hierarchy**: Item tags (e.g., `PF1`, `CT1`) appear in descriptions but hierarchy must be reconstructed from Column D labels.

### Semantic Boundary Classification

| Capability | Classification | Basis |
|---|---|---|
| Hierarchy label detection | Structurally Deterministic | Column D explicitly provides Head1–Head4 labels |
| Section code detection | Structurally Deterministic | Column A provides single/dual-letter codes |
| Item code parsing | Structurally Deterministic | Pattern `[Code]/[Number]` |
| UOM extraction | Structurally Deterministic | Explicit in Column D for leaf items |
| Vocabulary extraction | Semantically Deterministic | Pure frequency counting over description text |
| Head1 text categorization | Semantically Deterministic | Rule-based matching of known administrative patterns |
| Level progression validation | Structurally Deterministic | Column D hierarchy labels provide clear parent-child relationships |
| Scope containment (structural) | Structurally Deterministic | Section boundaries defined by Column A codes |
| "Items Always Quantify" | Structurally Deterministic | Observable: 0 of 2037 header rows have quantities |
| Zero-quantity detection | Structurally Deterministic | Fact detection over Column C |
| Scope containment (semantic) | Professional Judgment | Requires understanding of trade scope boundaries |
| Completeness (full QS) | Professional Judgment | Requires project scope knowledge |

### Reclassification from EQ-0011

EQ-0011 classified SEM-003 ("Items Always Quantify") as Domain Dependent. The evidence from this investigation demonstrates this is **Structurally Deterministic**:

- **Evidence**: 0 of 2037 header rows (Head1–Head4) carry quantities. 3606 measured items all carry quantities.
- **Rule**: If Column D contains a hierarchy label (Head1–Head4), the row header never has a quantity. Only rows with a UOM string in Column D carry quantities.
- **Determinism**: This is an observable fact across the production fixture. No QS judgment is required to detect it.

Similarly, V-003 (Level Progression Validation) is reclassified as **Structurally Deterministic** because hierarchy labels are explicit in Column D, and parent-child relationships can be validated through the stack-based algorithm validated in EQ-0010.

## Tool Delivered

The `tools/semantic_pattern_analysis.py` tool is now available for reproducible evidence extraction. It supports:

```
--fixture <filename>   Analyze a specific fixture file
--all                  Analyze all trade-specific fixtures
--verbose              Verbose output with structural statistics
--json                 Machine-readable JSON output
```

## Evidence Files

- `tools/semantic_pattern_analysis.py` — Analysis tool
- `tests/fixtures/costx/full_boq.xlsx` — Primary fixture (3606 items)
- `tests/fixtures/costx/Base_*.xlsX` — 16 trade-specific fixtures

## Related Documents

- EQ-0010 — Deterministic BOQ Structural Intelligence
- EQ-0011 — BOQ Semantic Intelligence Boundary
- docs/domain/06_Naming_Convention.md
- docs/domain/02_BOQ_Structure.md
- docs/domain/05_UOM_Standards.md

## Document Control

**Version:** 1.0  
**Status:** COMPLETED  
**Last Updated:** 2026-07-25  
**Owner:** Project Owner