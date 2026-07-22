# Naming Convention

**Version:** 1.0  
**Status:** Approved  
**Last Updated:** 2026-07-14  
**Owner:** Project Owner  
**Approvers:** Project Owner

---

## Purpose

This document defines the standard naming conventions for BOQ item descriptions, dimension groups, drawings, and folders. These conventions ensure consistency, clarity, and completeness in all project documentation.

This is the **Domain Source of Truth** for naming standards.

## Scope

This document covers:

- Item description construction
- Tag conventions
- Dimension patterns
- Common abbreviations
- Drawing naming
- Folder naming
- Dimension Group naming

This document applies to all BOQ preparation, measurement, and documentation activities.

---

## Authority

This document records office standard naming conventions.

**It does not supersede:**

- Contract-Specified Naming
- Client-Preferred Terminology
- Project-Specific Naming Requirements

**Priority Hierarchy:**

```
Contract-Mandated Naming
↓
Client-Specific Naming
↓
Office Standard Naming (this document)
↓
Default Practice
```

---

## Capability Consumers

**Current Consumers:**
- Parser (recognizes description patterns)
- BOQ Intelligence (extracts semantic information from descriptions)

**Planned Consumers:**
- CheckMate (will validate description completeness)
- Formatter (will apply naming standards)

**Future Consumers:**
- To be determined based on capability development

---

## Definitions

**Item Tag**: A short alphanumeric identifier prefixing an item description (e.g., PF1, CT1, J01).

**Description Pattern**: The standard structure for constructing item descriptions.

**Common Description**: The general category or type of work (e.g., "Pad Footing", "Ceramic tile").

**Specific Description**: Detailed specifications unique to the item (e.g., material grade, manufacturer, finish).

**Dimensions**: Size specifications in the format Length × Width × Height/Depth.

---

## Item Description Construction

### General Structure

**Standard Pattern:**

```
[Tag] – [Dimensions] [Common Description], [Specific Description]
```

**Components:**

1. **Item TAG** - Alphanumeric identifier
2. **Dimensions** - Length × Width × Height/Depth (where applicable)
3. **Common Description** - General work type
4. **Specific Description** - Detailed specifications

**Source:** `docs/reference/office_standards/03_Naming Convention.docx`

---

## Component Definitions

### 1. Item TAG

**Purpose:** Short unique identifier for item type

**Format:** Alphanumeric (letters + numbers)

**Examples:**
- PF1, PF2, PF3 (Pad Footings)
- CT1, CT2 (Ceramic Tiles)
- J01, J02 (Joinery)
- SC1, SC2 (Steel Columns)

**Rules:**
- Keep concise (typically 2-4 characters)
- Use consistent prefixes for item categories
- Number sequentially within category

---

### 2. Length

**Definition:** Longest dimension except height/depth

**Format:** Number in millimeters (no unit suffix)

**Examples:**
- 2500 (2500mm)
- 1200 (1200mm)

**Rules:**
- Always express in millimeters
- No decimal points for dimensions
- Longest horizontal dimension

---

### 3. Width

**Definition:** Second horizontal dimension

**Format:** Number in millimeters (no unit suffix)

**Examples:**
- 1500 (1500mm)
- 600 (600mm)

**Rules:**
- Perpendicular to length
- Expressed in millimeters
- Second largest dimension

---

### 4. Height/Depth

**Definition:** Vertical dimension or depth measurement

**Format:** Number in millimeters with descriptor (e.g., "high", "depth", "thick")

**Examples:**
- 1000mm depth
- 900mm high
- 150mm thick

**Rules:**
- Include descriptor ("high", "depth", "thick")
- Vertical or into-surface measurement
- Always clarify orientation

---

### 5. Common Description

**Definition:** General category or type of work

**Purpose:** Establishes what the item is

**Examples:**
- Pad Footing
- Ceramic tile
- Steel Column
- Lower kitchen cabinet

**Rules:**
- Use standard industry terminology
- Be concise but clear
- Capitalize appropriately

---

### 6. Specific Description

**Definition:** Detailed specifications unique to item

**Purpose:** Provides complete specification for procurement/construction

**Examples:**
- "National tiles-NT17-4326FL (R10)"
- "with LAM1 laminate carcass, ST1 stone top"
- "31.4kg/m, 1088mm Surface Perimeter"

**Rules:**
- Include manufacturer/brand if specified
- Include grade, finish, rating
- Include associated materials
- Reference other tagged items if needed

---

## Description Patterns by Category

### Structural Elements

**Pattern:** [Tag] – [Length]×[Width]×[Depth] [Element Type]

**Example:**
```
PF1 – 2500×1500×1000mm depth Pad Footing
```

**Components:**
1. Tag: PF1
2. Length: 2500mm
3. Width: 1500mm  
4. Depth: 1000mm depth
5. Common Description: Pad Footing

---

### Finishes

**Pattern:** [Tag] – [Length]×[Width] [Finish Type], [Specification]

**Example:**
```
CT1 – 600×300mm wide Ceramic tile, National tiles-NT17-4326FL (R10)
```

**Components:**
1. Tag: CT1
2. Length: 600mm
3. Width: 300mm wide
4. Common Description: Ceramic tile
5. Specific Description: National tiles-NT17-4326FL (R10)

---

### Joinery

**Pattern:** [Tag] – [Length]×[Width]×[Height] [Joinery Type], [Materials and Features]

**Example:**
```
J01 – 2500×600×900mm high lower kitchen cabinet, with LAM1 laminate carcass, ST1 stone top, with provisions for sink and microwave
```

**Components:**
1. Tag: J01
2. Length: 2500mm
3. Width: 600mm
4. Height: 900mm high
5. Common Description: lower kitchen cabinet
6. Specific Description: with LAM1 laminate carcass, ST1 stone top, with provisions for sink and microwave

---

### Steel Sections

**Pattern:** [Tag] – [Section Size] [Element Type], [Unit Weight], [Surface Perimeter]

**Example:**
```
SC1 – 250UB31 Steel Column, 31.4kg/m, 1088mm Surface Perimeter
```

**Components:**
1. Tag: SC1
2. Steel Section: 250UB31
3. Common Description: Steel Column
4. Unit Weight: 31.4kg/m
5. Surface Perimeter: 1088mm Surface Perimeter

**Note:** Steel sections follow different pattern due to standard section sizing

---

## Common Abbreviations

### Structural

- **m**: metre
- **mm**: millimetre
- **MPa**: Megapascal (concrete strength)
- **F**: Fabric (reinforcement)
- **UB**: Universal Beam
- **UC**: Universal Column
- **RHS**: Rectangular Hollow Section
- **SHS**: Square Hollow Section
- **CHS**: Circular Hollow Section

### Finishes

- **LAM**: Laminate
- **ST**: Stone
- **CT**: Ceramic Tile
- **VCT**: Vinyl Composite Tile

### Locations

- **GF**: Ground Floor
- **L1, L2**: Level 1, Level 2
- **RF**: Roof
- **B1, B2**: Basement 1, Basement 2

### General

- **incl.**: including
- **excl.**: excluding
- **approx.**: approximately
- **dia.**: diameter
- **typ.**: typical

**Source:** Office standard practice

---

## Dimension Group Naming

### Folder Structure

**Source:** `docs/reference/office_standards/03_Naming Convention.docx`

**Architectural Dimension Groups:**

```
Architectural\
  Roofing\
    Roof Sheeting
    Roof Accessories
  Metalworks\
    Handrails, Balustrade and Screens
    Tactile Indicator, Nosing and Bollards
  Floor Finishes\
    Floor finishes
    Floor accessories
  Ceiling Finishes\
    Ceiling Finishes
    Ceiling Accessories
  External Wall Finishes\
    External Wall Finishes
    External Wall Accessories
  Internal Wall Finishes\
    Internal Wall Finishes
    Internal Wall Accessories
  FFE\
    Sanitary Fixtures
    Appliances and Equipment
    Loose Furniture
  Doors\
    External Doors
    Internal Doors
  Windows\
    External Windows
    Internal Windows
    External Glazed Doors
    Internal Glazed Doors
  Partitions\
    External Walls
    Internal Walls
  Joinery\
  Signage\
```

**Structural Dimension Groups:**

```
Structural\
  Structural Concrete\
    Bored Piers
    Pad Footing
    Pile Cap
    Strip Footing
    Ground Beams
    Columns
    Walls
    Upstand & Downstand
    Hobs, Kerbs and Islands
    Slab on Ground
    Suspended Slab
    Suspended Beams
    Drop Panel
    Stairs
    Joints
    Others
  Structural Steel\
    Columns\
      CHS, UB, UC
      EA, UA, RHS, SHS
      PFC
    Framing\
      CHS, UB, UC
      EA, UA, RHS, SHS
      PFC
    Purlins, Girts and Bracings\
  Precast Concrete\
```

**Civil Works Dimension Groups:**

```
Civil Works\
  Sediment Control\
  Storm Water\
    Pipes
    Pits
    OSD
    Others
  Fence & Gates\
  Roadworks, Foot Path and Pavement\
    Pavement
    Kerb, Gutter and Island
    Pavement Accessories
  Retaining Walls\

Earthworks\
  Bulk Earthworks\
  Detailed Excavation\

Landscaping\
  Plants\
  Softscape\
  Hardscape\

Demolition\
```

---

## Drawing Organization

### Drawing Folder Structure

**Source:** `docs/reference/office_standards/03_Naming Convention.docx`

```
Architectural\
  Roofing
  Metalworks
  Floor Finishes
  Ceiling Finishes
  External Wall Finishes
  Internal Wall Finishes
  FFE
  Joinery
  Doors and Windows
  Partitions

Structural\
  Structural Concrete
  Structural Steel

Civil Works\
  Earthworks
  Landscaping
  Demolition
```

**Rules:**
- Match dimension group categories
- Group by discipline first
- Then by element type
- Maintain consistency with dimension groups

---

## Naming Consistency Rules

### NC-001: Tag Uniqueness Within Category

Tags must be unique within their category across the project.

**Severity:** **Error** if duplicate tags in same category

**Example Violation:**
```
PF1 – 2500×1500×1000mm depth Pad Footing (Type A)
PF1 – 3000×2000×1200mm depth Pad Footing (Type B) ← Error: duplicate tag
```

---

### NC-002: Dimension Order Consistency

Dimensions must follow Length × Width × Height/Depth order consistently.

**Severity:** **Warning** if order varies

**Correct:**
```
2500×1500×1000mm depth
```

**Incorrect:**
```
1500×2500×1000mm depth (width×length×depth - wrong order)
```

---

### NC-003: Description Completeness

Descriptions must include all mandatory components for the item type.

**Severity:** **Error** if mandatory components missing

**Mandatory Components:**
- Structural: Dimensions + Element Type
- Finishes: Dimensions + Finish Type + Specification
- Steel: Section + Element Type + Properties
- Joinery: Dimensions + Type + Materials

---

### NC-004: Abbreviation Consistency

Use standard abbreviations consistently throughout project.

**Severity:** **Warning** if non-standard abbreviations used

**Standard:**
```
incl. (including)
mm (millimetre)
```

**Non-Standard:**
```
including (spell out - verbose)
MM (incorrect case)
```

---

## Client-Specific Naming

### Standard

**Standard:** Some clients require specific naming conventions.

**Procedure:**
1. Identify client naming requirements
2. Document in project files
3. Apply consistently across project
4. Do not normalize to office standard if client specifies otherwise

**Examples:**
- Different tag formats (e.g., "PF-01" instead of "PF1")
- Specific terminology (e.g., "Slab" vs "Floor")
- Additional required information

**Rule:** Client-specified naming takes precedence.

---

## Rule Provenance

| Rule ID | Rule | Source | Document |
|---------|------|--------|----------|
| NC-001 | Tag Uniqueness Within Category | Office Standard | Practice convention |
| NC-002 | Dimension Order Consistency | Office Standard | 03_Naming Convention.docx |
| NC-003 | Description Completeness | Office Standard | Practice convention |
| NC-004 | Abbreviation Consistency | Office Standard | Practice convention |
| - | General Description Pattern | Office Standard | 03_Naming Convention.docx |
| - | Dimension Group Structure | Office Standard | 03_Naming Convention.docx |
| - | Drawing Folder Structure | Office Standard | 03_Naming Convention.docx |

---

## References

### Internal Documents
- `docs/domain/01_QS_Office_Standards.md` - General office standards
- `docs/domain/02_BOQ_Structure.md` - BOQ hierarchy
- `docs/domain/05_UOM_Standards.md` - Unit standards
- `docs/domain/09_Dimension_Group_Guide.md` - Dimension Group organization

### Office Standards
- `docs/reference/office_standards/03_Naming Convention.docx` - Naming patterns

---

## Related Documents

- **Upstream:** `docs/domain/01_QS_Office_Standards.md` - Quality requirements
- **Peer:** `docs/domain/05_UOM_Standards.md` - Unit conventions
- **Peer:** `docs/domain/09_Dimension_Group_Guide.md` - File organization
- **Downstream:** All BOQ preparation and documentation activities

---

## Document Control

**Change History:**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-01-15 | Project Owner | Initial scaffold |
| 1.0 | 2026-07-14 | Project Owner | Expanded with description patterns, abbreviations, and folder structures |

**Review Schedule:** Annual or upon identification of new naming patterns

**Distribution:** All quantity surveying staff, Jarvis Platform

---

## TODO

- [ ] TODO(Project Owner): Create comprehensive abbreviation glossary with all standard abbreviations
- [ ] TODO(Project Owner): Document naming conventions for MEP (Mechanical, Electrical, Plumbing) items
- [ ] TODO(Project Owner): Establish rules for compound item descriptions (multiple materials/finishes)
- [ ] TODO(Project Owner): Define procedure for handling non-English manufacturer names
- [ ] TODO(Project Owner): Document client-specific naming variations for top clients
- [ ] TODO(Project Owner): Create validation checklist for description completeness