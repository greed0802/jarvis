# Drawing Organization

**Version:** 1.0  
**Status:** Approved  
**Last Updated:** 2026-07-14  
**Owner:** Project Owner  
**Approvers:** Project Owner

---

## Purpose

This document defines standards for organizing project drawings. Proper drawing organization supports efficient measurement, reference tracking, and quality assurance.

This is the **Domain Source of Truth** for drawing file organization.

## Scope

This document covers:

- Drawing folder structure
- File naming conventions
- Drawing register maintenance
- Version control principles

This document applies to all project drawing management activities.

---

## Authority

This document records office standards for drawing organization.

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
- (No direct automated consumers currently)

**Planned Consumers:**
- Drawing Register Tool (will track drawing versions)
- Validation Tool (will verify drawing references)

**Future Consumers:**
- To be determined based on capability development

---

## Definitions

**Drawing Folder**: A directory containing project drawings organized by discipline and category.

**Drawing Register**: A document listing all project drawings with revision status.

**Drawing Reference**: The unique identifier for a drawing (e.g., drawing number).

**Revision**: A version of a drawing reflecting design changes.

---

## Folder Structure

### Standard Organization

**Source:** `docs/domain/06_Naming_Convention.md` (Drawing Folders section)

### Architectural Drawings

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
```

### Structural Drawings

```
Structural\
  Structural Concrete
  Structural Steel
```

### Civil Works Drawings

```
Civil Works\
  Earthworks
  Landscaping
  Demolition
```

### General Drawings

```
General\
  Site Plans
  Floor Plans
  Elevations
  Sections
  Details
```

**Provenance:** Office standard practice, documented in `docs/domain/06_Naming_Convention.md`

---

## Organization Principles

### Principle 1: Match Dimension Group Structure

**Standard:** Drawing folders should align with Dimension Group folder structure.

**Rationale:**
- Facilitates measurement workflow
- Easy cross-reference between drawings and measurements
- Consistent mental model
- Reduces errors

**Reference:** `docs/domain/09_Dimension_Group_Guide.md`

### Principle 2: Group by Discipline First

**Standard:** Organize by discipline (Architectural, Structural, Civil) before element type.

**Rationale:**
- Matches typical drawing issue structure
- Aligns with professional disciplines
- Industry standard practice

### Principle 3: Descriptive Folder Names

**Standard:** Folder names must clearly indicate drawing content.

**Rationale:**
- Quick identification
- Reduces navigation time
- Prevents misfiling

**Provenance:** Office standard practice

---

## File Naming

### Standard Format

**Pattern:** Use drawing number as received from design team.

**Guidelines:**

1. **Preserve Original Drawing Numbers**
   - Do not rename drawings
   - Maintain architect/engineer numbering
   - Enables clear reference in BOQ

2. **Include Revision in Filename (Optional)**
   - E.g., `A-101-RevB.pdf`
   - Helps identify current version
   - Prevents using outdated drawings

3. **Consistent File Type**
   - Prefer PDF for distribution
   - Maintain DWG if required for measurement
   - Document which format is authoritative

**Provenance:** Office standard practice

---

## Drawing Register

### Purpose

Track all project drawings and their revision status.

### Standard Information

**Minimum Required:**
- Drawing Number
- Drawing Title
- Discipline
- Revision
- Date Received
- File Location

**Optional:**
- Drawn By
- Checked By
- Notes

### Maintenance

1. **Update on Receipt**
   - Log all new drawings immediately
   - Note revision and date
   - Update file locations

2. **Track Superseded Drawings**
   - Move old revisions to archive folder
   - Maintain register entry with superseded status
   - Document revision history

3. **Regular Review**
   - Verify current revisions used in measurements
   - Check for missing drawings
   - Confirm all drawings catalogued

**Provenance:** Office quality standard

---

## Version Control

### Standard Practices

1. **Current Revision Folder**
   - Keep only current revisions in main folders
   - Clearly labeled as "Current"
   - All measurement work references this folder

2. **Superseded Folder**
   - Archive old revisions
   - Maintain for reference
   - Clearly labeled as "Superseded" or "Archive"

3. **Drawing References**
   - Always reference drawing number AND revision
   - Document which revision used for measurements
   - Note in BOQ preambles if critical

### Revision Tracking

**In BOQ Preambles:**

```
DRAWING REFERENCES
All measurements taken from:
- Architectural Drawings Revision C, dated 2026-01-15
- Structural Drawings Revision B, dated 2026-01-10
- Civil Drawings Revision A, dated 2026-01-05
```

**Provenance:** Office quality standard

---

## Drawing Organization Rules

### DO-001: Drawings Must Be Organized

Project drawings must be organized according to standard folder structure unless client specifies otherwise.

**Severity:** **Warning** if drawings not organized

**Rationale:** Efficient workflow and error prevention.

**Provenance:** Office standard

---

### DO-002: Drawing Register Required

All projects must maintain a drawing register.

**Severity:** **Warning** if drawing register missing or incomplete

**Rationale:** Version control and quality assurance.

**Provenance:** Office quality standard

---

### DO-003: Current Revisions Identified

Current drawing revisions must be clearly identified and separated from superseded drawings.

**Severity:** **Error** if measurements based on superseded drawings

**Rationale:** Accuracy and professional standards.

**Provenance:** Professional practice

---

### DO-004: Drawing References Documented

BOQ must document which drawing revisions were used for measurements.

**Severity:** **Error** if drawing references missing from preambles

**Rationale:** Audit trail and professional standards.

**Provenance:** Professional practice, office quality standard

---

## Client-Specific Organization

### Standard

**Standard:** Some clients provide drawings with specific organization.

**Procedure:**
1. Receive drawings in client format
2. Reorganize into office standard structure if beneficial
3. Maintain register of original vs reorganized structure
4. Document any reorganization

**Alternative:** Maintain client structure if it works effectively.

**Rule:** Adapt to what works best for the project.

**Reference:** `docs/domain/07_Client_Conventions.md`

---

## Best Practices

### File Management

1. **Clear Folder Structure**
   - Don't mix disciplines in folders
   - Keep structure shallow (avoid deep nesting)
   - Use subfolders for large projects

2. **Consistent Naming**
   - Preserve original drawing numbers
   - Don't add prefixes or suffixes unless necessary
   - Maintain consistency across project

3. **Version Management**
   - Keep only current revisions in working folders
   - Archive superseded drawings promptly
   - Document revision changes

### Drawing Register

1. **Keep Updated**
   - Update immediately upon receipt
   - Review weekly during active projects
   - Final check before BOQ submission

2. **Include Context**
   - Note reason for revision if significant
   - Flag critical changes affecting measurements
   - Document any discrepancies between drawing sets

3. **Share with Team**
   - Accessible to all project staff
   - Central location
   - Clear format

**Provenance:** Office best practices

---

## Integration with Measurement Workflow

### Drawing to Dimension Group Link

**Best Practice:** Maintain clear link between drawings and Dimension Groups.

**Method:**
1. Reference drawing numbers in Dimension Group sheets
2. Use same folder organization for both
3. Note drawing revisions in Dimension Group files

**Benefit:**
- Traceability
- Easier verification
- Audit trail

**Reference:** `docs/domain/09_Dimension_Group_Guide.md`

---

## Rule Provenance

| Rule ID | Rule | Source | Document |
|---------|------|--------|----------|
| DO-001 | Drawings Must Be Organized | Office Standard | Practice convention |
| DO-002 | Drawing Register Required | Office Standard | Quality standard |
| DO-003 | Current Revisions Identified | Professional Practice | Industry standard |
| DO-004 | Drawing References Documented | Professional Practice | Industry standard |
| - | Folder Structure | Office Standard | Practice convention |
| - | Version Control | Office Standard | Quality management |

---

## References

### Internal Documents
- `docs/domain/06_Naming_Convention.md` - Drawing folder structure definition
- `docs/domain/07_Client_Conventions.md` - Client precedence
- `docs/domain/09_Dimension_Group_Guide.md` - Parallel organization

---

## Related Documents

- **Upstream:** `docs/domain/06_Naming_Convention.md` - Defines folder structure
- **Peer:** `docs/domain/09_Dimension_Group_Guide.md` - Parallel organization
- **Downstream:** Measurement and verification activities

---

## Document Control

**Change History:**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-01-15 | Project Owner | Initial scaffold |
| 1.0 | 2026-07-14 | Project Owner | Expanded with organization principles and version control |

**Review Schedule:** Annual or upon identification of organizational improvements

**Distribution:** All quantity surveying staff, Jarvis Platform

---

## TODO

- [ ] TODO(Project Owner): Create standard drawing register template
- [ ] TODO(Project Owner): Define procedure for handling drawing discrepancies
- [ ] TODO(Project Owner): Establish guidelines for digital vs paper drawing management
- [ ] TODO(Project Owner): Document integration with document control systems
- [ ] TODO(Project Owner): Create training materials for drawing organization
- [ ] TODO(Project Owner): Define archival procedures for completed projects