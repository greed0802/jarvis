# Dimension Group Guide

**Version:** 1.0  
**Status:** Approved  
**Last Updated:** 2026-07-14  
**Owner:** Project Owner  
**Approvers:** Project Owner

---

## Purpose

This document defines organization and management standards for Dimension Groups (CostX measurement files). Dimension Groups contain the detailed dimensional measurements that feed quantities into the BOQ.

This is the **Domain Source of Truth** for Dimension Group organization.

## Scope

This document covers:

- Dimension Group folder structure
- File naming conventions
- Organization principles
- Sheet organization within files
- Reconciliation requirements

This document applies to all measurement and dimension file management activities.

---

## Authority

This document records office standards for Dimension Group organization.

**It does not supersede:**

- Contract-Specified Organization
- Client-Preferred Organization
- Project-Specific Requirements

**Priority Hierarchy:**

```
Contract-Mandated Organization
↓
Client-Specific Organization
↓
Office Standard Organization (this document)
↓
Default Practice
```

---

## Capability Consumers

**Current Consumers:**
- Parser (reads Dimension Group files)
- BOQ Intelligence (validates organization)

**Planned Consumers:**
- CheckMate (will validate Dimension Group structure)
- Reconciliation Tool (will automate quantity matching)

**Future Consumers:**
- To be determined based on capability development

---

## Definitions

**Dimension Group**: A CostX measurement file (.5dx) containing organized dimension sheets for a specific trade or building element.

**Dimension Sheet**: A worksheet within a Dimension Group file containing measurements for a specific element or location.

**Folder Structure**: The hierarchical organization of Dimension Group files by discipline and trade.

**Reconciliation**: The process of verifying Dimension Group totals match Workbook quantities.

---

## Organization Principles

### Principle 1: Group by Trade/Element

**Standard:** Organize Dimension Groups by trade category and element type.

**Rationale:**
- Matches BOQ trade organization
- Enables efficient measurement workflow
- Facilitates checking and reconciliation
- Maintains logical grouping

### Principle 2: Consistent Structure

**Standard:** Use consistent folder structure across all projects unless client specifies otherwise.

**Rationale:**
- Predictable organization
- Easier file location
- Consistent checking workflow
- Knowledge transfer between projects

### Principle 3: Descriptive Naming

**Standard:** File and folder names must clearly indicate content.

**Rationale:**
- Quick identification of content
- Reduces errors
- Supports audit trail
- Facilitates collaboration

**Reference:** `docs/domain/06_Naming_Convention.md`

**Provenance:** Office standard practice

---

## Folder Structure

### Standard Organization

**Source:** `docs/domain/06_Naming_Convention.md` (Dimension Group Naming section)

### Architectural Dimension Groups

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

### Structural Dimension Groups

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

### Civil Works Dimension Groups

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

**Provenance:** Office standard practice, documented in `docs/domain/06_Naming_Convention.md`

---

## File Naming

### Standard Format

**Pattern:** `[Trade]_[Element]_[Location].5dx`

**Examples:**
- `Concrete_PadFooting_GridA-D.5dx`
- `Finishes_CeramicTile_Bathrooms.5dx`
- `Steel_Columns_Level1.5dx`

### Guidelines

1. **Trade First**
   - Identifies primary discipline
   - Matches folder organization

2. **Element Second**
   - Describes what is measured
   - Specific enough for identification

3. **Location Third (Optional)**
   - Adds location context if needed
   - Useful for large projects

4. **Avoid Generic Names**
   - "Dimensions.5dx" is not acceptable
   - "Measurements.5dx" is not acceptable
   - Be specific and descriptive

**Provenance:** Office standard practice

---

## Sheet Organization Within Files

### Standard Principles

1. **One Element Type Per Sheet**
   - E.g., All PF1 pad footings on one sheet
   - All CT1 tiles on another sheet
   - Maintains clarity and traceability

2. **Logical Grouping**
   - Group by location if multiple locations
   - Group by level for multi-story
   - Group by grid line for large buildings

3. **Descriptive Sheet Names**
   - Sheet name should indicate content
   - E.g., "PF1 - Grid A-D", "CT1 - Bathrooms Level 1"

4. **Consistent Ordering**
   - Order sheets logically within file
   - Follow construction sequence if applicable
   - Alphabetical or numerical as appropriate

**Provenance:** Office standard practice

---

## Dimension Group Rules

### DG-001: Dimension Groups Required for All Trades

Every trade with quantities must have corresponding Dimension Groups.

**Severity:** **Error** if trade quantities exist without Dimension Groups

**Rationale:** Enables verification and audit trail.

**Provenance:** Office quality standard

---

### DG-002: Folder Structure Must Match Standards

Dimension Groups must be organized according to standard folder structure unless client specifies otherwise.

**Severity:** **Warning** if non-standard structure used without documentation

**Rationale:** Consistency and predictability.

**Provenance:** Office standard

---

### DG-003: File Naming Must Be Descriptive

Dimension Group files must have descriptive names indicating content.

**Severity:** **Warning** if generic names used (e.g., "Dimensions.5dx")

**Rationale:** Identification and error prevention.

**Provenance:** Office standard

---

### DG-004: Quantities Must Reconcile

Dimension Group totals must reconcile with Workbook quantities within tolerance (< 0.01 for same UOM).

**Severity:** **Error** if discrepancy ≥ 0.01

**Rationale:** Accuracy and quality assurance.

**Reference:** `docs/domain/01_QS_Office_Standards.md` (Dimension Group Reconciliation)

**Provenance:** Office quality standard

---

## Reconciliation Process

### Standard Procedure

1. **Extract Dimension Group Totals**
   - Sum all quantities by item tag
   - Group by UOM
   - Document extraction date

2. **Extract Workbook Totals**
   - Sum corresponding BOQ quantities
   - Match by description and UOM
   - Document extraction date

3. **Compare**
   - Calculate differences
   - Identify discrepancies ≥ 0.01
   - Document comparison

4. **Investigate Discrepancies**
   - Check for missing items
   - Verify formulas correct
   - Check for duplicates

5. **Document Results**
   - Record reconciliation outcome
   - Note any acceptable differences
   - Document resolution

**Reference:** `docs/domain/08_Checking_Workflow.md` (Checkpoint 6)

**Provenance:** Office quality standard

---

## Client-Specific Organization

### Standard

**Standard:** Some clients require specific Dimension Group organization.

**Procedure:**
1. Identify client requirements
2. Document organization used
3. Apply consistently across project
4. Do not normalize to office standard if client specifies otherwise

**Examples:**
- Different folder hierarchy
- Different naming conventions
- Different file grouping

**Rule:** Client requirements take precedence.

**Reference:** `docs/domain/07_Client_Conventions.md`

---

## Best Practices

### File Management

1. **Regular Backups**
   - Maintain version history
   - Store securely
   - Document file locations

2. **Clear Organization**
   - Don't mix unrelated measurements in one file
   - Keep file sizes manageable
   - Use subfolders for complex projects

3. **Naming Consistency**
   - Use consistent naming patterns within project
   - Avoid special characters in filenames
   - Use underscores, not spaces

### Sheet Management

1. **Clear Sheet Names**
   - Indicate content clearly
   - Reference item tags where applicable
   - Note locations if relevant

2. **Logical Ordering**
   - Arrange sheets in construction sequence
   - Group related measurements
   - Maintain consistency across files

3. **Documentation**
   - Include notes for complex measurements
   - Document assumptions
   - Reference drawing numbers

**Provenance:** Office best practices

---

## Rule Provenance

| Rule ID | Rule | Source | Document |
|---------|------|--------|----------|
| DG-001 | Dimension Groups Required | Office Standard | Quality standard |
| DG-002 | Standard Folder Structure | Office Standard | Practice convention |
| DG-003 | Descriptive File Naming | Office Standard | Practice convention |
| DG-004 | Quantities Must Reconcile | Office Standard | Quality standard |
| - | Organization Principles | Office Standard | Practice convention |
| - | Sheet Organization | Office Standard | Best practices |

---

## References

### Internal Documents
- `docs/domain/01_QS_Office_Standards.md` - Reconciliation requirements
- `docs/domain/06_Naming_Convention.md` - Naming conventions and folder structure
- `docs/domain/07_Client_Conventions.md` - Client precedence
- `docs/domain/08_Checking_Workflow.md` - Checking procedures
- `docs/domain/10_Drawing_Organization.md` - Drawing folder alignment

---

## Related Documents

- **Upstream:** `docs/domain/06_Naming_Convention.md` - Defines folder structure
- **Peer:** `docs/domain/10_Drawing_Organization.md` - Parallel organization
- **Downstream:** Measurement and reconciliation activities

---

## Document Control

**Change History:**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-01-15 | Project Owner | Initial scaffold |
| 1.0 | 2026-07-14 | Project Owner | Expanded with organization principles and reconciliation procedures |

**Review Schedule:** Annual or upon identification of organizational improvements

**Distribution:** All quantity surveying staff, Jarvis Platform

---

## TODO

- [ ] TODO(Project Owner): Create standard templates for common Dimension Group files
- [ ] TODO(Project Owner): Document procedure for handling very large projects with extensive Dimension Groups
- [ ] TODO(Project Owner): Establish guidelines for when to split vs combine Dimension Group files
- [ ] TODO(Project Owner): Define archival procedures for completed projects
- [ ] TODO(Project Owner): Create training materials for Dimension Group organization
- [ ] TODO(Project Owner): Document client-specific organizational patterns for recurring clients