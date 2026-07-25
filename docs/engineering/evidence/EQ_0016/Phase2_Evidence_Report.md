# EQ-0016 — Trade Classification Evidence Report

## Purpose

This report documents the evidence-based patterns discovered from analyzing the CostX fixture data for implementing deterministic trade classification (D-004).

## Fixture Analysis Results

### Trade-to-Prefix Mapping

Based on analysis of `tests/fixtures/costx/full_boq.xlsx`:

| Trade Code | Trade Name | Item Code Prefixes | Item Count |
|------------|------------|-------------------|------------|
| A | GROSS FLOOR AREA (GFA) | A | 24 |
| B | DEMOLITION & SITE CLEARANCE | B | 51 |
| C | SITE PREPARATION | C | 45 |
| D | PILING | D | 155 |
| E | DETAILED EXCAVATION | E | 40 |
| F | IN-SITU CONCRETE | F | 454 |
| G | FORMWORK | G | 370 |
| H | REINFORCEMENT | H | 109 |
| I | POST TENSIONING | I | 31 |
| J | MASONRY - BRICK & BLOCK | J | 55 |
| K | STRUCTURAL STEELWORK | K | 112 |
| L | ROOFING & ROOF PLUMBING | L | 69 |
| M | FAÇADE - MASONRY/BLOCKWORK | M | 66 |
| N | FAÇADE - GLAZING | N | 138 |
| O | FAÇADE - CLADDING | O | 83 |
| P | FAÇADE - LOUVRES & SCREENS | P | 39 |
| Q | INSULATION | Q | 108 |
| R | BUILDING ACCESS SAFETY SYSTEMS | (none) | 0 |
| S | PARTITIONS & LININGS | S | 236 |
| T | SUSPENDED CEILINGS | T | 170 |
| U | RENDERING & PLASTERING | U | 24 |
| V | DOORS, FRAMES & HARDWARE (INCL. INTERNAL GLAZING) | V | 218 |
| W | JOINERY & CARPENTRY | W | 114 |
| X | WINDOW BLINDS | X | 14 |
| Y | METALWORK | Y | 92 |
| Z | SIGNAGE | AA, AB, AC, AD, AE, AF, AG, AH, AI, AJ, AK, AL, AM, AN, AP, AQ, AR, AS, AT, AU, AV, AW, AX, AY, AZ, BA, BB, BC, BD, BE, BF, BG, BH | 1379 |

### Classification Algorithm

The deterministic classification algorithm is based on the following evidence:

1. **Single-letter prefixes (A-Y)**: Items with codes starting with a single letter (A-Y) are classified to the corresponding trade section.

2. **Trade Z (SIGNAGE) exception**: Items with codes starting with AA-AZ or BA-BH are classified as SIGNAGE.

3. **Unknown items**: Items that don't match any known prefix pattern return "UNKNOWN".

### Trade Taxonomy Mapping

The CostX trade sections map to the Jarvis trade taxonomy as follows:

| CostX Trade | Jarvis Trade | Evidence |
|-------------|--------------|----------|
| A (GFA) | ARC | Architectural measurement |
| B (Demolition) | CIV | Civil/site works |
| C (Site Prep) | CIV | Civil/site works |
| D (Piling) | STR | Structural foundations |
| E (Excavation) | CIV | Civil/site works |
| F (Concrete) | STR | Structural concrete |
| G (Formwork) | STR | Structural formwork |
| H (Reinforcement) | STR | Structural steel |
| I (Post-tensioning) | STR | Structural systems |
| J (Masonry) | STR | Structural masonry |
| K (Steelwork) | STR | Structural steel |
| L (Roofing) | ARC | Architectural roofing |
| M (Facade Masonry) | ARC | Architectural facade |
| N (Glazing) | ARC | Architectural glazing |
| O (Cladding) | ARC | Architectural cladding |
| P (Louvres/Screens) | ARC | Architectural elements |
| Q (Insulation) | FIN | Finishes/insulation |
| R (Safety Systems) | (none) | No items |
| S (Partitions) | ARC | Architectural partitions |
| T (Ceilings) | ARC | Architectural ceilings |
| U (Rendering) | FIN | Finishes/rendering |
| V (Doors/Hardware) | ARC | Architectural joinery |
| W (Joinery) | ARC | Architectural joinery |
| X (Blinds) | ARC | Architectural finishes |
| Y (Metalwork) | ARC | Architectural metalwork |
| Z (Signage) | ARC | Architectural signage |

### Implementation Requirements

1. **Deterministic mapping**: Use exact prefix matching, no fuzzy logic
2. **Stable ordering**: Results must be sorted deterministically
3. **Unknown handling**: Return "UNKNOWN" for unmatched items
4. **Pure function**: No side effects, immutable outputs

## Conclusion

The evidence shows clear, deterministic patterns for trade classification based on item code prefixes. The implementation should use exact string matching with the documented prefix-to-trade mappings.