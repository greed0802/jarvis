# Client Conventions

**Version:** 1.0  
**Status:** Approved  
**Last Updated:** 2026-07-14  
**Owner:** Project Owner  
**Approvers:** Project Owner

---

## Purpose

This document defines how client-specific conventions are handled when they differ from office standards. It establishes the precedence hierarchy and documentation requirements for client-specific practices.

This is the **Domain Source of Truth** for client convention management.

## Scope

This document covers:

- Client precedence rules
- Convention precedence hierarchy
- Documentation requirements for client-specific practices
- Application procedures
- Extensibility for new clients

---

## Authority

This document records the principle that client requirements take precedence over office standards.

**Fundamental Principle:**

```
Contract Requirements
↓
Client-Specific Standards
↓
Office Standards
↓
Default Practices
```

This hierarchy applies across all domain areas.

---

## Capability Consumers

**Current Consumers:**
- Parser (reads any client format)
- BOQ Intelligence (recognizes client-specific patterns)

**Planned Consumers:**
- Formatter (will apply client-specific formatting)
- CheckMate (will validate against client-specific rules)

**Future Consumers:**
- To be determined based on capability development

---

## Definitions

**Client Convention**: A standard, practice, or requirement specified by a client that differs from office default standards.

**Contract Requirement**: A mandatory requirement specified in the contract documents.

**Client Preference**: A non-mandatory preference expressed by the client.

**Office Standard**: The default practice when no client-specific requirement exists.

**Client Documentation**: Records of client-specific conventions maintained for consistency across projects.

---

## Precedence Hierarchy

### Level 1: Contract Requirements

**Definition:** Mandatory requirements explicitly stated in contract documents.

**Precedence:** Highest - must be followed exactly

**Examples:**
- Specified BOQ format
- Required trade schedule
- Mandatory measurement standards
- Required submission format

**Action:** Follow exactly as specified in contract.

**Provenance:** Contract documents

---

### Level 2: Client-Specific Standards

**Definition:** Established practices and preferences for a specific client, documented from previous projects.

**Precedence:** High - follow unless contract specifies otherwise

**Examples:**
- Client's standard trade schedule
- Client's preferred terminology
- Client's standard BOQ formatting
- Client's measurement preferences

**Action:** Apply consistently across all projects for that client.

**Provenance:** Client documentation, previous project requirements

---

### Level 3: Office Standards

**Definition:** Default practices established by the office.

**Precedence:** Medium - apply when no client-specific requirement exists

**Examples:**
- Office standard trade schedule
- Office naming conventions
- Office quality standards
- Office formatting standards

**Action:** Apply to all projects unless overridden.

**Provenance:** Domain documents 01-10

---

### Level 4: Default Practices

**Definition:** General industry practices when no specific standard exists.

**Precedence:** Lowest - fallback only

**Examples:**
- General measurement principles
- Common industry terminology
- Standard professional practice

**Action:** Use only when higher precedence standards don't address the situation.

**Provenance:** Industry practice, Australian Standards

---

## Convention Categories

### Formatting Conventions

**Client variations may include:**
- BOQ structure and numbering
- Typography and styling
- Section organization
- Header formatting
- Spacing and layout

**Procedure:**
1. Identify client formatting requirements
2. Document in project files
3. Apply consistently throughout project
4. Do not attempt to "improve" client format

**Rule:** Client formatting takes precedence over office formatting.

---

### Trade Schedule Conventions

**Client variations may include:**
- Different trade sequence
- Trade grouping preferences
- Trade naming/terminology
- Trade subdivisions
- Elemental vs trade organization

**Procedure:**
1. Check if client has standard trade schedule
2. If yes, use client schedule exactly
3. If no, use office standard
4. Document which schedule is being used

**Rule:** Client trade schedule takes precedence.

**Reference:** `docs/domain/03_Trade_Schedule.md`

---

### Measurement Conventions

**Client variations may include:**
- Specific measurement methods
- Measurement standards (e.g., NRM, SMM)
- Tolerance requirements
- Rounding conventions
- Area/volume calculation methods

**Procedure:**
1. Identify client measurement requirements
2. Document methodology in preambles
3. Apply consistently throughout project
4. Validate against client standards

**Rule:** Client measurement standards take precedence.

---

### Naming Conventions

**Client variations may include:**
- Item tag formats
- Description patterns
- Terminology preferences
- Abbreviation standards
- Specification referencing

**Procedure:**
1. Identify client naming requirements
2. Apply consistently across project
3. Do not normalize to office standard
4. Document client-specific terms

**Rule:** Client naming conventions take precedence.

**Reference:** `docs/domain/06_Naming_Convention.md`

---

### Unit Conventions

**Client variations may include:**
- Unit abbreviations (e.g., "ea" vs "no")
- Unit display format (e.g., "m²" vs "sqm")
- Decimal place preferences
- Rounding direction

**Procedure:**
1. Identify client unit preferences
2. Apply consistently throughout project
3. Do not convert to office standard
4. Document in project files

**Rule:** Client unit preferences take precedence.

**Reference:** `docs/domain/05_UOM_Standards.md`

---

## Documentation Requirements

### When Client Convention Differs from Office Standard

**Required Documentation:**

1. **Project Files**
   - Document the deviation
   - Note the source (contract, client standard, client preference)
   - Reference relevant contract clause or client document

2. **Workbook Preambles**
   - Note significant deviations that affect measurement
   - Reference client standards used
   - Clarify any non-standard interpretations

3. **Internal Records**
   - Update client-specific documentation if applicable
   - Note for future projects with same client

**Purpose:** Ensures consistency and traceability.

---

### When Establishing New Client Pattern

**Procedure:**

1. **First Project with New Client**
   - Document all client-specific requirements
   - Note deviations from office standards
   - Create initial client profile if recurring client

2. **Subsequent Projects**
   - Reference established client patterns
   - Note any changes from previous projects
   - Update client documentation if requirements change

3. **Client Documentation Location**
   - Store in project files
   - Reference in project-specific documentation
   - No system modifications required

**Provenance:** Office practice for client management

---

## Application Rules

### CONV-001: Client Precedence

When client convention differs from office standard, client convention takes precedence.

**Severity:** **Error** if office standard applied when client specifies otherwise

**Example:**
```
Client requires "ea" for count unit
Office standard: "no"
Correct: Use "ea"
Error: Use "no" ← Violates client requirement
```

**Provenance:** Fundamental client management principle

---

### CONV-002: Consistency Within Project

Client conventions must be applied consistently throughout single project.

**Severity:** **Error** if client convention applied inconsistently

**Example:**
```
Project using client trade schedule
Correct: All sections follow client sequence
Error: Mix of client and office sequences
```

**Provenance:** Quality standard

---

### CONV-003: Documentation Required

Significant deviations from office standard must be documented.

**Severity:** **Warning** if deviation not documented

**Rationale:** Ensures knowledge transfer and future consistency.

**Provenance:** Office quality standard

---

### CONV-004: No Unsolicited "Improvement"

Do not modify client-specified conventions without client approval.

**Severity:** **Error** if client convention modified without approval

**Rationale:** Client has specified requirements for a reason.

**Provenance:** Professional practice

---

## Exceptions

### When Client Convention Is Unclear

**Procedure:**
1. Seek clarification from client
2. Reference previous projects with same client
3. If unavailable, document assumption and seek approval
4. Do not assume office standard applies

### When Client Convention Conflicts with Contract

**Procedure:**
1. Contract requirements take precedence
2. Seek clarification if conflict appears
3. Document resolution
4. Obtain client approval if interpretation required

### When Client Convention Conflicts with Australian Standards

**Procedure:**
1. Contract/client requirements still take precedence for BOQ format
2. Measurement principles must comply with professional standards
3. Seek clarification if apparent conflict
4. Document approach and obtain approval

---

## Client-Specific Documentation Pattern

### Recommended Structure

For recurring clients, maintain documentation of:

1. **Formatting Standards**
   - BOQ structure
   - Typography
   - Numbering schemes

2. **Trade Schedule**
   - Standard sequence
   - Trade grouping
   - Terminology

3. **Measurement Standards**
   - Specific methods
   - Tolerance requirements
   - Rounding conventions

4. **Naming Conventions**
   - Tag formats
   - Description patterns
   - Abbreviations

5. **Unit Preferences**
   - Unit abbreviations
   - Display formats
   - Decimal places

6. **Submission Requirements**
   - File formats
   - Naming conventions
   - Required documentation

**Storage:** Project files, client-specific documentation

**Purpose:** Consistency across multiple projects for same client

---

## Rule Provenance

| Rule ID | Rule | Source | Document |
|---------|------|--------|----------|
| CONV-001 | Client Precedence | Professional Practice | Client management |
| CONV-002 | Consistency Within Project | Office Standard | Quality standard |
| CONV-003 | Documentation Required | Office Standard | Quality standard |
| CONV-004 | No Unsolicited "Improvement" | Professional Practice | Client management |
| - | Precedence Hierarchy | Professional Practice | Industry standard |
| - | Documentation Requirements | Office Standard | Quality management |

---

## References

### Internal Documents
- `docs/domain/01_QS_Office_Standards.md` - Office standards (Level 3)
- `docs/domain/02_BOQ_Structure.md` - Structure standards
- `docs/domain/03_Trade_Schedule.md` - Trade schedule precedence
- `docs/domain/04_Omission_Addition.md` - Revision methodology
- `docs/domain/05_UOM_Standards.md` - Unit standards
- `docs/domain/06_Naming_Convention.md` - Naming standards

All domain documents reference this precedence hierarchy.

---

## Related Documents

- **Upstream:** Contract documents, Client standards
- **Peer:** All domain documents (01-06, 08-10)
- **Downstream:** All project-specific implementations

---

## Document Control

**Change History:**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-01-15 | Project Owner | Initial scaffold |
| 1.0 | 2026-07-14 | Project Owner | Expanded with precedence hierarchy and application rules |

**Review Schedule:** Annual or upon significant client requirement changes

**Distribution:** All quantity surveying staff, Jarvis Platform

---

## TODO

- [ ] TODO(Project Owner): Create template for client-specific documentation
- [ ] TODO(Project Owner): Document conventions for top 3 recurring clients
- [ ] TODO(Project Owner): Establish procedure for client convention change requests
- [ ] TODO(Project Owner): Define escalation path when client requirement seems unreasonable
- [ ] TODO(Project Owner): Create checklist for identifying client-specific requirements at project start
- [ ] TODO(Project Owner): Document procedure for handling conflicts between client conventions and Australian Standards