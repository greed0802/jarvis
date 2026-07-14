# Omission and Addition

**Version:** 1.0  
**Status:** Approved  
**Last Updated:** 2026-07-14  
**Owner:** Project Owner  
**Approvers:** Project Owner

---

## Purpose

This document defines the omission and addition methodology used for BOQ revisions in Australian quantity surveying practice. This methodology allows transparent tracking of scope changes, variations, and design modifications throughout a project's lifecycle.

This is the **Domain Source of Truth** for BOQ revision methodology.

## Scope

This document covers:

- Global revision methodology
- Local revision methodology
- Omission and addition formatting
- Quantity sign conventions
- Revision validation rules

This document applies to all BOQ revisions, addendums, and variations.

---

## Authority

This document records Australian quantity surveying standard practice for scope revisions.

**It does not supersede:**

- Contract-Specified Revision Formats
- Client-Preferred Revision Methods
- Project-Specific Variation Procedures

**Priority Hierarchy:**

```
Contract-Mandated Revision Format
↓
Client-Specific Revision Format
↓
Office Standard (this document)
↓
Default Practice
```

---

## Capability Consumers

**Current Consumers:**
- Parser (reads omission/addition structures)
- BOQ Intelligence (recognizes revision patterns)

**Planned Consumers:**
- CheckMate (will validate revision mathematics)
- Formatter (will apply revision formatting)

**Future Consumers:**
- To be determined based on capability development

---

## Definitions

**Omission**: Removal or reduction of scope from the original BOQ. Represented by negative quantities.

**Addition**: Introduction or increase of scope to the original or revised BOQ. Represented by positive quantities.

**Global Revision**: Complete replacement of an original item with a new specification or quantity.

**Local Revision**: Adjustment of only the changed portion of an original item's quantity.

**Original**: The baseline BOQ item before any revisions are applied.

**Addendum**: A formal document containing omissions and additions to the original BOQ.

---

## Global Revision

### Definition

**Standard:** Global revision completely removes the original item and introduces a new item.

### Structure

```
Original Item
Quantity: 100

OMISSION
Quantity: -100 (complete removal)

ADDITION
Quantity: 82 (new item)
```

### Business Meaning

Global revision indicates:
- Complete replacement of original scope
- Different specification, material, or method
- Original work no longer required
- New work introduced with different specification

### Example

```
Original:
Plain concrete 20MPa to footings: m³: 100.00

OMISSION:
Plain concrete 20MPa to footings: m³: -100.00

ADDITION:
Plain concrete 32MPa to footings: m³: 82.00
```

**Business Interpretation:** The 20MPa concrete specification is completely replaced with 32MPa concrete. The quantity also changed from 100 m³ to 82 m³.

### Validation Rules

**OA-001: Global Omission Must Equal Original**
When performing global revision, omission quantity must equal negative of original quantity.

**Severity:** **Error** if omission ≠ -(original)

**OA-002: Global Addition Is Independent**
Global addition quantity is independent of original quantity (may be larger, smaller, or same).

**Severity:** N/A (not a constraint)

**Provenance:** Australian QS standard practice

---

## Local Revision

### Definition

**Standard:** Local revision adjusts only the changed portion of the original item.

### Structure - Reduction

```
Original Item
Quantity: 100

OMISSION
Quantity: -12 (reduction only)

Net Result: 88
```

### Structure - Increase

```
Original Item
Quantity: 100

ADDITION
Quantity: 12 (increase only)

Net Result: 112
```

### Business Meaning

Local revision indicates:
- Same specification maintained
- Quantity adjustment only
- Original work partially remains (if omission)
- Original work supplemented (if addition)

### Example - Reduction

```
Original:
Excavate trench for footings: m³: 100.00

OMISSION:
Excavate trench for footings: m³: -12.00

Net: 88.00 m³
```

**Business Interpretation:** Same excavation work, reduced by 12 m³. 88 m³ remains in scope.

### Example - Increase

```
Original:
Excavate trench for footings: m³: 100.00

ADDITION:
Excavate trench for footings: m³: 12.00

Net: 112.00 m³
```

**Business Interpretation:** Same excavation work, increased by 12 m³. Total scope now 112 m³.

### Validation Rules

**OA-003: Local Adjustment Magnitude**
Local omission must be less than original quantity in absolute terms.

**Severity:** **Warning** if |omission| ≥ original (consider global revision instead)

**OA-004: Local Addition Has No Upper Bound**
Local addition may be any positive quantity.

**Severity:** N/A (not a constraint)

**Provenance:** Australian QS standard practice

---

## Omission and Addition Formatting

### Standard Format

**Source:** `docs/reference/office_standards/05_Addendum Format.docx`

**Formatting Rules:**

1. **OMISSION Header**
   - ALL CAPITAL LETTERS
   - Bold
   - Calibri 11
   - Unit column: "noidc"

2. **ADDITION Header**
   - ALL CAPITAL LETTERS
   - Bold
   - Calibri 11
   - Unit column: "noidc"

3. **Spacing**
   - "endh1" unit after ADDITION section for spacing

4. **Item Listing**
   - List all items with addendum under OMISSION (make negative)
   - Incorporate necessary adjustments/additions under ADDITION

**CostX Representation:**
- OMISSION and ADDITION are represented as special row types
- "noidc" in unit column indicates non-item, non-dimension, non-calc row
- "endh1" provides section spacing

**Provenance:** `docs/reference/office_standards/05_Addendum Format.docx`

---

## Quantity Sign Conventions

### Standard Signs

**Original Items:** Always positive quantities

**Omissions:** Always negative quantities

**Additions:** Always positive quantities

### Sign Validation Rules

**OA-005: Omission Sign Convention**
Omission quantities must be negative.

**Severity:** **Error** if omission quantity is positive

**Rationale:** Positive omission indicates data entry error or misunderstanding of methodology.

**OA-006: Addition Sign Convention**
Addition quantities must be positive.

**Severity:** **Error** if addition quantity is negative

**Rationale:** Negative addition indicates data entry error or misunderstanding of methodology.

**OA-007: Original Sign Convention**
Original item quantities must be positive (or zero for provisional items).

**Severity:** **Error** if original quantity is negative

**Provenance:** Fundamental QS arithmetic convention

---

## Revision Scenarios

### Scenario 1: Complete Replacement (Global)

**Use When:**
- Specification changes
- Material changes
- Method changes
- Complete design change

**Pattern:** Original → Omit all → Add new

### Scenario 2: Quantity Reduction (Local)

**Use When:**
- Same specification
- Reduced scope
- Partial deletion

**Pattern:** Original → Omit partial → Net reduces

### Scenario 3: Quantity Increase (Local)

**Use When:**
- Same specification
- Increased scope
- Additional work

**Pattern:** Original → Add partial → Net increases

### Scenario 4: Deletion Only (Global)

**Use When:**
- Work completely removed
- No replacement

**Pattern:** Original → Omit all → (No addition)

### Scenario 5: New Work (Addition Only)

**Use When:**
- Work not in original
- Pure addition to scope

**Pattern:** (No original) → Add new

---

## System Representations

### CostX Representation

| Domain Concept | CostX Representation |
|----------------|---------------------|
| OMISSION Header | Special row type with "noidc" unit |
| ADDITION Header | Special row type with "noidc" unit |
| Section Spacing | "endh1" unit marker |
| Omission Item | Item with negative quantity |
| Addition Item | Item with positive quantity |

### Future Systems

When supporting additional estimating systems, maintain domain concepts:
- Omission = negative quantity adjustment
- Addition = positive quantity adjustment
- Headers indicate section boundaries

---

## Exceptions

### Client-Specific Formats

**Standard:** Some clients require specific omission/addition formats.

**Procedure:**
- Follow client format exactly
- Maintain mathematical consistency
- Validate sign conventions still apply
- Document client-specific requirements

### Combined Revisions

**Standard:** Some clients combine multiple revisions in single addendum.

**Procedure:**
- Maintain clear revision sequence
- Document cumulative effect
- Validate net quantities
- Ensure traceability

---

## Rule Provenance

| Rule ID | Rule | Source | Document |
|---------|------|--------|----------|
| OA-001 | Global Omission Equals Original | Australian QS Practice | Standard methodology |
| OA-002 | Global Addition Independent | Australian QS Practice | Standard methodology |
| OA-003 | Local Adjustment Magnitude | Australian QS Practice | Standard methodology |
| OA-004 | Local Addition Unbounded | Australian QS Practice | Standard methodology |
| OA-005 | Omission Sign Convention | QS Arithmetic | Fundamental convention |
| OA-006 | Addition Sign Convention | QS Arithmetic | Fundamental convention |
| OA-007 | Original Sign Convention | QS Arithmetic | Fundamental convention |
| - | Formatting Standards | Office Standard | 05_Addendum Format.docx |

---

## References

### Internal Documents
- `docs/domain/01_QS_Office_Standards.md` - General office standards
- `docs/domain/02_BOQ_Structure.md` - BOQ hierarchy and structure

### Office Standards
- `docs/reference/office_standards/05_Addendum Format.docx` - Formatting rules
- `docs/reference/office_standards/09_Format-Template for Workbook.docx` - Typography

---

## Related Documents

- **Upstream:** `docs/domain/01_QS_Office_Standards.md` - Quality requirements
- **Peer:** `docs/domain/02_BOQ_Structure.md` - Structural organization
- **Downstream:** All BOQ revision and variation activities

---

## Document Control

**Change History:**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-01-15 | Project Owner | Initial scaffold |
| 1.0 | 2026-07-14 | Project Owner | Expanded with global/local revision rules, validation, and business meaning |

**Review Schedule:** Annual or upon identification of new revision patterns

**Distribution:** All quantity surveying staff, Jarvis Platform

---

## TODO

- [ ] TODO(Project Owner): Document procedure for multi-stage revisions (original → rev1 → rev2 → rev3)
- [ ] TODO(Project Owner): Define rules for provisional sum omissions/additions
- [ ] TODO(Project Owner): Document handling of percentage-based variations
- [ ] TODO(Project Owner): Create examples of complex revision scenarios (combined global/local)
- [ ] TODO(Project Owner): Establish rules for when local vs global revision should be used
- [ ] TODO(Project Owner): Document impact of omission/addition on rates (if rate changes)