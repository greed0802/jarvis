# Units of Measurement Standards

**Version:** 1.0  
**Status:** Approved  
**Last Updated:** 2026-07-14  
**Owner:** Project Owner  
**Approvers:** Project Owner

---

## Purpose

This document defines the standard units of measurement used in Bills of Quantities. These standards ensure consistency in quantification, calculation, and pricing across all projects.

This is the **Domain Source of Truth** for measurement units.

## Scope

This document covers:

- Standard measurement units
- Unit abbreviations
- Rounding conventions
- Special unit types
- Decimal place standards

This document applies to all BOQ preparation, measurement, and quantification activities.

---

## Authority

This document records office standard measurement units.

**It does not supersede:**

- Contract-Specified Units
- Client-Preferred Units
- Project-Specific Measurement Requirements
- Australian Standards (AS) measurement codes

**Priority Hierarchy:**

```
Contract-Mandated Units
↓
Client-Specific Units
↓
Office Standard Units (this document)
↓
Default Practice
```

---

## Capability Consumers

**Current Consumers:**
- Parser (validates unit format)
- BOQ Intelligence (recognizes measurement patterns)

**Planned Consumers:**
- CheckMate (will validate unit consistency)
- Formatter (will apply unit formatting)

**Future Consumers:**
- To be determined based on capability development

---

## Definitions

**Unit of Measurement (UOM)**: The standard quantity used to express measurement magnitude.

**Rounding Convention**: The rule for determining decimal places and rounding direction.

**Special Unit**: A non-quantitative unit type used for organizational or calculation purposes.

**Decimal Places**: The number of digits displayed after the decimal point.

---

## Standard Units

### Linear Measurement

**Unit:** m (metre)

**Usage:** Length, width, height, perimeter, linear elements

**Rounding:** Round up to 2 decimal places

**Examples:**
- Wall length: m
- Perimeter: m
- Linear metres of skirting: m
- Height of wall: m

**Provenance:** Australian Standards, office standard practice

---

### Area Measurement

**Unit:** m² (square metre)

**Usage:** Floor area, wall area, ceiling area, surface area

**Rounding:** Round up to 2 decimal places

**Examples:**
- Floor area: m²
- Wall area: m²
- Ceiling area: m²
- Roof area: m²

**Provenance:** Australian Standards, office standard practice

---

### Volume Measurement

**Unit:** m³ (cubic metre)

**Usage:** Concrete volume, excavation, fill, bulk materials

**Rounding:** Round up to 2 decimal places

**Examples:**
- Concrete volume: m³
- Excavation: m³
- Fill: m³
- Bulk earthworks: m³

**Provenance:** Australian Standards, office standard practice

---

### Count Measurement

**Unit:** no (number)

**Usage:** Countable discrete items

**Rounding:** Round up to whole numbers (or 2 decimal places if fractional allowed)

**Examples:**
- Number of doors: no
- Number of windows: no
- Number of fixtures: no
- Number of components: no

**Provenance:** Office standard practice

---

### Weight Measurement

**Unit:** t (tonne)

**Usage:** Weight of materials, typically steel or bulk materials

**Rounding:** Exact (display to actual precision calculated)

**Examples:**
- Steel weight: t
- Material weight: t

**Note:** Display exact weight without rounding for procurement accuracy.

**Provenance:** Australian Standards, office standard practice

---

### Item Unit

**Unit:** Item

**Usage:** Lump sum items, provisional items, single-instance items

**Rounding:** Typically "1" (single item)

**Examples:**
- Lump sum for specific work: Item
- Provisional sum: Item
- Single equipment item: Item

**Provenance:** Standard QS practice

---

## Special Units

### Note Unit

**Unit:** Note

**Usage:** Assumptions, clarifications, preambles without quantities

**Rounding:** N/A (no quantity)

**Examples:**
- Preamble statements
- Assumption notes
- Clarification text

**Purpose:** Provides context without quantification.

**Provenance:** Office standard practice

---

### No IDC Unit

**Unit:** noidc

**Usage:** Non-item, non-dimension, non-calc rows (headers, spacers)

**Rounding:** N/A (no quantity)

**CostX Representation:** Used for OMISSION and ADDITION headers

**Purpose:** Marks organizational rows that are not measured items.

**Provenance:** CostX convention, office standard

---

### End Header 1 Unit

**Unit:** endh1

**Usage:** Spacing after sections, typically after ADDITION sections

**Rounding:** N/A (no quantity)

**CostX Representation:** Provides visual spacing in workbook

**Purpose:** Section formatting and readability.

**Provenance:** CostX convention, office standard

---

## Rounding Conventions

### General Rule

**Standard:** Display all quantities to 2 decimal places.

**Source:** `docs/reference/office_standards/12_Units of Measurements.docx`

**Rationale:** Balances precision with readability.

### Rounding Direction

**Standard:** Round up for m, m², m³, no

**Rationale:** Conservative estimate ensures scope coverage.

**Exception:** Weight (t) displays exact value for procurement accuracy.

### Examples

| Calculated Value | Unit | Displayed Value | Explanation |
|-----------------|------|----------------|-------------|
| 12.3456 | m | 12.35 | Rounded up to 2 decimal places |
| 45.671 | m² | 45.68 | Rounded up to 2 decimal places |
| 8.239 | m³ | 8.24 | Rounded up to 2 decimal places |
| 15.4 | no | 16.00 | Rounded up to whole number |
| 3.14159 | t | 3.14159 | Exact value preserved |

**Provenance:** Office standard practice

---

## Unit Consistency Rules

### UOM-001: Same Item Same Unit

Items with identical descriptions must use identical units.

**Severity:** **Error** if same description has different units

**Example Violation:**
```
Concrete to footings: m³
Concrete to footings: m²  ← Error: inconsistent unit
```

**Provenance:** QS consistency principle

---

### UOM-002: Trade Unit Consistency

Similar items within same trade should use consistent units unless justified.

**Severity:** **Warning** if similar items use different units without justification

**Example:**
```
Excavate trench: m³
Excavate bulk: m³  ← Consistent
Excavate general: m² ← Warning: different unit for similar work
```

**Provenance:** Office quality standard

---

### UOM-003: Appropriate Unit for Work Type

Unit must be appropriate for the type of work measured.

**Severity:** **Error** if unit is inappropriate for work type

**Examples:**
```
Valid:
- Concrete volume: m³
- Wall area: m²
- Skirting length: m

Invalid:
- Concrete volume: m² ← Error: volume requires m³
- Wall area: m ← Error: area requires m²
```

**Provenance:** Fundamental measurement principle

---

## Client-Specific Units

### Standard

**Standard:** Some clients prefer specific units or unit formatting.

**Procedure:**
1. Identify client unit preferences
2. Document in project files
3. Apply consistently across project
4. Do not normalize to office standard if client specifies otherwise

**Examples of Client Variations:**
- "ea" instead of "no"
- "sqm" instead of "m²"
- "cum" instead of "m³"
- "lm" instead of "m"

**Rule:** Client-specified units take precedence over office standard units.

**Provenance:** Client management practice

---

## System Representations

### CostX Representation

| Domain Concept | CostX Representation |
|----------------|---------------------|
| Metre | m |
| Square Metre | m² (or m2) |
| Cubic Metre | m³ (or m3) |
| Number | no |
| Tonne | t |
| Item | Item |
| Note | Note |
| No IDC | noidc |
| End Header 1 | endh1 |

### Future Systems

When supporting additional estimating systems:
- Maintain domain concept (linear, area, volume, count, weight)
- Map to system-specific unit representation
- Preserve rounding conventions
- Validate unit appropriateness

---

## Exceptions

### Imperial Units

**Standard:** Imperial units (feet, inches, yards) not used unless contract-specified.

**Procedure:** If required, convert and document conversion factors used.

### Percentage Units

**Standard:** Percentage adjustments may be used for provisional sums or variations.

**Format:** Display as percentage with "%" symbol.

### Currency Units

**Standard:** Currency is not a measurement unit but a pricing unit.

**Note:** This document covers measurement units only. Pricing is separate.

---

## Rule Provenance

| Rule ID | Rule | Source | Document |
|---------|------|--------|----------|
| UOM-001 | Same Item Same Unit | QS Consistency | Fundamental principle |
| UOM-002 | Trade Unit Consistency | Office Standard | Quality standard |
| UOM-003 | Appropriate Unit for Work Type | Measurement Principle | Fundamental |
| - | 2 Decimal Place Standard | Office Standard | 12_Units of Measurements.docx |
| - | Round Up Convention | Office Standard | Practice convention |
| - | Exact Weight Display | Office Standard | Procurement accuracy |
| - | Standard Unit Abbreviations | Australian Standards | AS measurement codes |

---

## References

### Internal Documents
- `docs/domain/01_QS_Office_Standards.md` - General office standards
- `docs/domain/02_BOQ_Structure.md` - BOQ hierarchy
- `docs/domain/06_Naming_Convention.md` - Description standards

### Office Standards
- `docs/reference/office_standards/12_Units of Measurements.docx` - Unit standards

### External Standards
- Australian Standards (AS) - Measurement codes

---

## Related Documents

- **Upstream:** `docs/domain/01_QS_Office_Standards.md` - Quality requirements
- **Peer:** `docs/domain/06_Naming_Convention.md` - Description construction
- **Downstream:** All BOQ preparation and measurement activities

---

## Document Control

**Change History:**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-01-15 | Project Owner | Initial scaffold |
| 1.0 | 2026-07-14 | Project Owner | Expanded with standard units, rounding conventions, and validation rules |

**Review Schedule:** Annual or upon Australian Standards updates

**Distribution:** All quantity surveying staff, Jarvis Platform

---

## TODO

- [ ] TODO(Project Owner): Define acceptable tolerance for rounding differences in reconciliation
- [ ] TODO(Project Owner): Document conversion factors for imperial to metric (if required)
- [ ] TODO(Project Owner): Establish rules for composite units (e.g., m²/m³ ratios)
- [ ] TODO(Project Owner): Define procedure for client-specific unit approvals
- [ ] TODO(Project Owner): Document special units used by specific clients
- [ ] TODO(Project Owner): Create unit validation test cases for common errors