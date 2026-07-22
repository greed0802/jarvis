# BOQ Structure

**Version:** 1.0  
**Status:** Approved  
**Last Updated:** 2026-07-14  
**Owner:** Project Owner  
**Approvers:** Project Owner

---

## Purpose

This document defines the hierarchical structure rules for Bills of Quantities. These rules ensure logical organization, maintain relationships between elements, and enable consistent BOQ construction regardless of client formatting preferences or estimating software.

This is the **Domain Source of Truth** for BOQ structural organization.

## Scope

This document covers:

- BOQ hierarchy rules (domain concepts)
- Valid structural patterns
- Structural semantics
- Header relationships
- Item organization
- Structural validation criteria
- System representations

This document applies to all BOQ preparation activities across all project types and estimating systems.

---

## Authority

This document records office understanding of BOQ structural principles.

**It does not supersede:**

- Contract Requirements (specific structure mandates)
- Client Standards (preferred formatting)
- Industry Standards (accepted conventions)

**Priority Hierarchy:**

```
Contract-Mandated Structure
↓
Client Standard Structure
↓
Office Standard Structure (this document)
↓
Default Parsing
```

---

## Capability Consumers

**Current Consumers:**
- Parser (reads and validates structure)
- BOQ Intelligence (validates structural integrity)

**Planned Consumers:**
- CheckMate (will detect structural violations)
- Formatter (will enforce hierarchy rules)

**Future Consumers:**
- To be determined based on capability development

---

## Definitions

### Domain Concepts

**BOQ Hierarchy**: The nested structure of headers and items that organizes quantity information from general to specific.

**Hierarchy Level 1**: Top-level trade or section header (e.g., "SUBSTRUCTURE", "SUPERSTRUCTURE")

**Hierarchy Level 2**: Second-level header subdividing Level 1 (e.g., "Strip Footings", "Ground Floor Slab")

**Hierarchy Level 3**: Third-level header subdividing Level 2 (e.g., "Concrete Work", "Reinforcement")

**Hierarchy Level N**: Additional subdivision levels as required by project complexity

**Measured Item**: A measurable quantity with description, UOM, and quantity (e.g., "Plain concrete 20MPa to footings: m³: 12.50")

**Logical Consistency**: The principle that BOQ structure must remain meaningful and hierarchically sound regardless of absolute positioning.

**Structural Integrity**: The property that parent-child relationships are maintained throughout the BOQ.

### System-Specific Terminology

**CostX Representation:**
- Hierarchy Level 1 → Head1
- Hierarchy Level 2 → Head2
- Hierarchy Level 3 → Head3
- Hierarchy Level 4 → Head4
- Measured Item → Item

**Note:** Other estimating systems may use different terminology for the same hierarchical concepts. The domain concepts remain constant across systems.

---

## Structural Semantics

These are the fundamental semantic rules that define what each structural element means and how it behaves. These semantics are independent of formatting, presentation, or system implementation.

### Section (Hierarchy Level 1-N)

**Purpose:** Groups related work into logical organizational units.

**Semantic Rules:**
- **Never carries quantities** - sections organize but do not measure
- **Provides scope** - defines the boundary for all child elements
- **Establishes context** - all descendant elements inherit this context
- **Must have children** - empty sections indicate incomplete work

**Examples:**
```
SUBSTRUCTURE          ← Section: groups all substructure work
EXTERNAL WALLS        ← Section: groups all external wall work
PRELIMINARIES         ← Section: groups preliminary items
```

**Violations:**
```
INVALID: Section with quantity
SUBSTRUCTURE: 450 m³  ← Error: sections cannot have quantities
```

**Provenance:** Fundamental QS practice

---

### Header (Hierarchy Level 1-N)

**Purpose:** Provides descriptive context for grouped work.

**Semantic Rules:**
- **Never measured** - headers describe but do not quantify
- **Provides classification** - establishes the category of work below
- **Inherits from parent** - meaning is derived from position in hierarchy
- **Must be meaningful** - vague headers indicate poor organization

**Examples:**
```
Strip Footings        ← Header: describes type of foundation work
Concrete Work         ← Header: describes material/trade
Ground Floor Slab     ← Header: describes location and element
```

**Properties:**
- Headers accumulate meaning through hierarchy
- "Concrete Work" under "Strip Footings" under "SUBSTRUCTURE" = substructure strip footing concrete
- Context flows downward through header chain

**Violations:**
```
INVALID: Header carrying measurement
Strip Footings: 12.5 m³  ← Error: headers do not carry quantities
```

**Provenance:** Fundamental QS practice

---

### Measured Item

**Purpose:** Represents measurable work with specific quantities.

**Semantic Rules:**
- **Always owns quantity** - items must have measurable amounts
- **Inherits context** - meaning derived from parent headers
- **Atomic measurement** - single item represents single measurable unit
- **Must be specific** - ambiguous items are invalid

**Examples:**
```
Plain concrete 20MPa to footings: m³: 12.50
Reinforcement fabric F72: m²: 45.00
Excavate trench for footings: m³: 8.75
```

**Properties:**
- Full meaning = header chain + item description
- Item "Plain concrete 20MPa to footings: m³: 12.50" under headers "Concrete Work" → "Strip Footings" → "SUBSTRUCTURE" = complete semantic specification
- Quantity and UOM are mandatory attributes

**Violations:**
```
INVALID: Item without quantity
Plain concrete 20MPa to footings  ← Error: measured items must have quantities

INVALID: Item without UOM
Plain concrete 20MPa to footings: 12.50  ← Error: must specify unit
```

**Provenance:** Fundamental QS practice

---

### Hierarchy

**Purpose:** Provides semantic inheritance and organizational structure.

**Semantic Rules:**
- **Provides inheritance** - child elements inherit meaning from parents
- **Never contributes measurement** - hierarchy organizes, does not quantify
- **Establishes relationships** - defines logical connections between work packages
- **Must be consistent** - hierarchy must follow logical decomposition

**Semantic Inheritance Example:**
```
SUBSTRUCTURE                    ← Context: foundation work
  Strip Footings                ← Inherits: substructure + type: strip footings
    Concrete Work               ← Inherits: substructure strip footing + material: concrete
      Plain concrete 20MPa      ← Inherits: all above + specific: 20MPa concrete to footings
```

**Full Semantic Meaning:**
The measured item inherits:
- Scope: SUBSTRUCTURE
- Element: Strip Footings
- Trade: Concrete Work
- Specification: Plain concrete 20MPa

**Properties:**
- Each level adds semantic specificity
- Parent context is never lost
- Siblings are semantically distinct
- Hierarchy depth indicates complexity

**Violations:**
```
INVALID: Hierarchy carries quantity
SUBSTRUCTURE: 450 m³            ← Error: hierarchy organizes, does not measure
  Strip Footings: 150 m³        ← Error: hierarchy organizes, does not measure
    Item: Plain concrete        ← Only items carry quantities
```

**Provenance:** Fundamental QS practice

---

### Semantic Validation Rules

**SEM-001: Sections Never Measure**
Hierarchy levels 1-N cannot carry quantities.

**Severity:** **Error**

**SEM-002: Headers Provide Context Only**
Headers describe and organize but do not quantify.

**Severity:** **Error**

**SEM-003: Items Always Quantify**
Measured items must have quantity and UOM.

**Severity:** **Error**

**SEM-004: Inheritance Flows Downward**
Child elements inherit semantic meaning from all parents.

**Severity:** N/A (structural property)

**SEM-005: Semantic Completeness**
Full item meaning = inherited context + item specification.

**Severity:** **Warning** (if context unclear or ambiguous)

**Provenance:** Fundamental QS semantic understanding

---

## Fundamental Principle

**Standard:** Hierarchy matters more than absolute ordering.

**Explanation:**

The BOQ structure is fundamentally hierarchical. A valid structure maintains parent-child relationships even if the absolute order of trades or sections varies.

**Rationale:**

- Different clients prefer different trade sequences
- Some clients group by location, others by trade
- The logical relationship is more important than the sequence
- Structure must remain mathematically sound

**Provenance:** Office understanding of BOQ organization principles

**Example Valid Structures:**

```
Structure A (Trade-first):
Level 1: SUBSTRUCTURE
  Level 2: Excavation
    Level 3: Bulk excavation
      Measured Item: Excavate topsoil
      Measured Item: Excavate to formation level
    Level 3: Trench excavation
      Measured Item: Excavate for footings
  Level 2: Concrete
    Level 3: Footings
      Measured Item: Plain concrete 20MPa
      Measured Item: Reinforcement

Structure B (Location-first):
Level 1: GROUND FLOOR
  Level 2: Substructure
    Level 3: Excavation
      Measured Item: Bulk excavation
    Level 3: Concrete
      Measured Item: Footings
Level 1: FIRST FLOOR
  Level 2: Substructure
    Level 3: Concrete
      Measured Item: Suspended slab
```

Both structures are valid because the hierarchy is logically consistent.

---

## Valid Hierarchy Patterns

### Pattern 1: Three-Level Hierarchy
```
Hierarchy Level 1
  Hierarchy Level 2
    Hierarchy Level 3
      Measured Item
      Measured Item
```

**Example:**
```
SUBSTRUCTURE
  Strip Footings
    Concrete Work
      Plain concrete 20MPa to footings: m³: 12.50
      Reinforcement fabric F72: m²: 45.00
```

**CostX Representation:** Head1 → Head2 → Head3 → Item

**Validation:** Pass

---

### Pattern 2: Two-Level Hierarchy
```
Hierarchy Level 1
  Hierarchy Level 2
    Measured Item
    Measured Item
```

**Example:**
```
PRELIMINARIES
  Site Establishment
    Site office accommodation: Item: 1
    Temporary fencing: m: 120.00
```

**CostX Representation:** Head1 → Head2 → Item

**Validation:** Pass

---

### Pattern 3: Single-Level Hierarchy (Rare)
```
Hierarchy Level 1
  Measured Item
  Measured Item
```

**Example:**
```
PROVISIONAL SUMS
  PC Sum for electrical work: Item: 1
  PC Sum for plumbing work: Item: 1
```

**CostX Representation:** Head1 → Item

**Validation:** Pass (acceptable for specific sections like Provisional Sums)

---

### Pattern 4: Extended Hierarchy (Complex Projects)
```
Hierarchy Level 1
  Hierarchy Level 2
    Hierarchy Level 3
      Hierarchy Level 4
        Measured Item
        Measured Item
```

**Example:**
```
SUPERSTRUCTURE
  Floor Structures
    Level 2 Floor
      Slab Construction
        Plain concrete 32MPa to slab: m³: 45.00
        Post-tensioning tendons: m: 350.00
```

**CostX Representation:** Head1 → Head2 → Head3 → Head4 → Item

**Validation:** Pass (requires Project Owner approval and documentation)

---

### Invalid Patterns

```
INVALID: Measured Item at same level as Level 2
Hierarchy Level 1
  Hierarchy Level 2
    Measured Item
  Measured Item  ← Error: breaks hierarchy
```

**Severity:** **Error**

```
INVALID: Skipped level
Hierarchy Level 1
  Hierarchy Level 3  ← Error: missing Level 2
    Measured Item
```

**Severity:** **Error**

```
INVALID: Orphan header
Hierarchy Level 2
  Measured Item  ← Error: no parent Level 1
```

**Severity:** **Error**

---

## Header Relationships

**Standard:** Headers establish scope and context for child elements.

### Relationship Principles

1. **Parent headers define scope**
   - All child elements inherit parent context
   - Child elements must relate to parent scope
   - No child element may exceed parent scope

2. **Sibling headers are mutually exclusive**
   - Level 2 siblings under same Level 1 must not overlap
   - Measured Items under different Level 2s must not duplicate

3. **Headers organize, not measure**
   - Headers group related work
   - Measured Items contain the actual measurements
   - Header text provides context only

**Example:**
```
EXTERNAL WORKS                    ← Level 1: defines scope
  Pavements                       ← Level 2: subset of external works
    Concrete Pavements            ← Level 3: subset of pavements
      Plain concrete 25MPa to paths: m²  ← Measured Item
  Landscaping                     ← Level 2: different subset, non-overlapping
    Topsoil                       ← Level 3: subset of landscaping
      Imported topsoil 150mm deep: m²   ← Measured Item
```

**Provenance:** Office understanding of BOQ organization

---

## Client Formatting Flexibility

**Standard:** Client-specific formatting preferences do not alter the fundamental hierarchy.

**Principle:**

The underlying logical structure remains constant. Presentation may vary.

**Variations Allowed:**
- Different header numbering schemes (1.1.1 vs A.1.1 vs 01.01.01)
- Different indentation or spacing
- Different font or styling
- Different page breaks
- Different header capitalization
- Different system-specific terminology (Head1 vs Section vs Level)

**Variations NOT Allowed:**
- Breaking parent-child relationships
- Measured Items appearing above their parent headers
- Skipping hierarchy levels
- Circular references

**Example:**

```
Office Format (CostX):
1. SUBSTRUCTURE
  1.1 Strip Footings
    1.1.1 Concrete Work
      Plain concrete 20MPa to footings: m³: 12.50

Client Format A:
A SUBSTRUCTURE
  A.1 Strip Footings
    A.1.1 Concrete Work
      Plain concrete 20MPa to footings: m³: 12.50

Client Format B (Different System):
01 SUBSTRUCTURE
  01.01 STRIP FOOTINGS
    01.01.01 CONCRETE WORK
      Plain concrete 20MPa to footings: m³: 12.50
```

All three represent the same valid hierarchy using different presentation conventions.

**Provenance:** Office practice for client management

---

## Structural Validation

**Standard:** BOQ structure must pass the following validation checks.

### Validation Rules

#### V-001: Parent Exists
Every Level 2 must have a Level 1 parent.
Every Level 3 must have a Level 2 parent.
Every Measured Item must have at least a Level 1 parent.

**Severity:** **Error**

#### V-002: No Orphans
No elements float without a parent relationship.

**Severity:** **Error**

#### V-003: Level Progression
Hierarchy levels must increment by 1.
Cannot skip from Level 1 directly to Level 3.

**Severity:** **Error**

#### V-004: Scope Containment
Child elements must fit within parent scope.

**Severity:** **Warning** (requires manual review)

#### V-005: Completeness
Every trade/section must have measured items.
Empty headers indicate incomplete BOQ.

**Severity:** **Warning** (acceptable during drafting, **Error** at submission)

**Provenance:** Office quality standards

**Validation Example:**

```
VALID:
SUBSTRUCTURE                     ← Has children
  Strip Footings                 ← Has parent and children
    Concrete Work                ← Has parent and children
      Measured Item: Plain concrete ← Has all required parents

INVALID:
SUBSTRUCTURE                     ← V-005 violation: No children
  
Strip Footings                   ← V-001 violation: No parent (orphan)
  Concrete Work
    Measured Item: Plain concrete
```

---

## System Representations

Different estimating systems represent the same domain concepts using different terminology. The domain concepts remain constant.

### Current System: CostX

| Domain Concept | CostX Representation |
|----------------|---------------------|
| Hierarchy Level 1 | Head1 |
| Hierarchy Level 2 | Head2 |
| Hierarchy Level 3 | Head3 |
| Hierarchy Level 4 | Head4 |
| Measured Item | Item |

### Future Systems

When supporting additional estimating systems:

1. Map system-specific terminology to domain concepts
2. Maintain validation rules using domain concepts
3. Parser recognizes system-specific representations
4. Validation applies universal domain rules

**Example:**

| Domain Concept | System A | System B |
|----------------|----------|----------|
| Hierarchy Level 1 | Section | Category |
| Hierarchy Level 2 | Subsection | Group |
| Measured Item | Line Item | Entry |

---

## Exceptions

### Simple Projects

**Standard:** Small projects may use simpler hierarchy.

**Acceptable:**
- Level 1 → Measured Item (no Level 2 or Level 3)
- Must still maintain logical grouping
- Typical for small residential or simple fit-outs

### Complex Projects

**Standard:** Very complex projects may require deeper hierarchy.

**Acceptable:**
- Level 1 → Level 2 → Level 3 → Level 4 → Level 5 → Measured Item
- Use sparingly and consistently
- Document rationale
- Requires Project Owner approval

**Note:** CostX currently supports up to Level 4 (Head4). Deeper hierarchies may require alternative representation.

**Severity:** Level 5+ without documentation: **Warning**

### Client-Mandated Structures

**Standard:** Some clients require specific structures.

**Procedure:**
- Follow client requirements exactly
- Document structure in project files
- Validate logical consistency still maintained

---

## Rule Provenance

| Rule ID | Rule | Source | Document |
|---------|------|--------|----------|
| V-001 | Parent Exists | Office Standard | Practice convention |
| V-002 | No Orphans | Office Standard | Practice convention |
| V-003 | Level Progression | Office Standard | Practice convention |
| V-004 | Scope Containment | Office Practice | Quality standards |
| V-005 | Completeness | Office Standard | Quality standards |
| SEM-001 | Sections Never Measure | QS Practice | Fundamental semantics |
| SEM-002 | Headers Provide Context Only | QS Practice | Fundamental semantics |
| SEM-003 | Items Always Quantify | QS Practice | Fundamental semantics |
| SEM-004 | Inheritance Flows Downward | QS Practice | Fundamental semantics |
| SEM-005 | Semantic Completeness | QS Practice | Fundamental semantics |
| - | Hierarchy over Sequence | Office Understanding | BOQ organization |
| - | Client Formatting Flexibility | Office Practice | Client management |
| - | System-Agnostic Concepts | Domain Principle | System independence |

---

## References

### Internal Documents
- `docs/domain/01_QS_Office_Standards.md` - General office standards
- `docs/domain/03_Trade_Schedule.md` - Standard trade sequence (Level 1 organization)
- `docs/domain/06_Naming_Convention.md` - Header and item naming conventions
- `docs/domain/07_Client_Conventions.md` - Client-specific structures

### Office Standards
- `docs/reference/office_standards/09_Format-Template for Workbook.docx`
- `docs/reference/office_standards/standard_trade_schedule.xlsx`

---

## Related Documents

- **Upstream:** `docs/domain/01_QS_Office_Standards.md` - Quality requirements
- **Peer:** `docs/domain/03_Trade_Schedule.md` - Defines Level 1 sequence
- **Downstream:** All BOQ construction and validation activities

---

## Document Control

**Change History:**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-01-15 | Project Owner | Initial scaffold |
| 1.0 | 2026-07-14 | Project Owner | Expanded with system-agnostic concepts, structural semantics, and evidence-based consumer model |

**Review Schedule:** Annual or upon identification of structural edge cases

**Distribution:** All quantity surveying staff, Jarvis Platform

---

## TODO

- [ ] TODO(Project Owner): Define maximum acceptable hierarchy depth beyond Level 4
- [ ] TODO(Project Owner): Add validation rules for circular reference detection
- [ ] TODO(Project Owner): Document procedure for handling non-standard client structures
- [ ] TODO(Project Owner): Create examples library of valid vs invalid structures for common project types
- [ ] TODO(Project Owner): Establish when V-005 (Completeness) transitions from Warning to Error
- [ ] TODO(Project Owner): Document system representations as additional estimating systems are supported