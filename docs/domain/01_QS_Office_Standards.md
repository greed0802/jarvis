# QS Office Standards

**Version:** 1.0  
**Status:** Approved  
**Last Updated:** 2026-07-14  
**Owner:** Project Owner  
**Approvers:** Project Owner

---

## Purpose

This document defines the authoritative office standards for quantity surveying work. These standards form the domain knowledge foundation that guides BOQ preparation, validation, and quality assurance.

This is NOT a policy manual.

This is the **Domain Source of Truth** for office practice.

## Scope

This document covers:

- Quality assurance validation rules
- Workbook formatting standards
- Documentation standards
- Language conventions
- Office-wide acceptance criteria

This document applies to all BOQ preparation, checking, and submission activities.

---

## Authority

This document records office practice as domain knowledge.

**It does not supersede:**

- Contract Requirements
- Client Standards
- Australian Standards (AS)
- Project-specific requirements

**Priority Hierarchy:**

```
Contract Requirements
↓
Client Standards
↓
Office Standards (this document)
↓
Default Practices
```

When conflicts arise, higher priority always wins.

---

## Capability Consumers

**Current Consumers:**
- Parser (reads and validates structure)
- BOQ Intelligence (extracts patterns and validates quality)

**Planned Consumers:**
- CheckMate (will automate validation rules)
- Formatter (will apply formatting standards)

**Future Consumers:**
- To be determined based on capability development

---

## Definitions

**Workbook**: The Excel-based Bill of Quantities document containing measurements, descriptions, quantities, and rates.

**Bulk Check**: A validation procedure comparing plan gross areas against calculated areas using the office Bulk Check workbook.

**Dimension Group**: A CostX measurement file containing organized dimension sheets for a specific trade or building element.

**Validation**: The act of checking whether required checks were performed.

**Acceptance Criteria**: The thresholds determining whether a check passes or fails.

**QA**: Quality Assurance - the systematic process of validating work for accuracy, completeness, and conformance to standards.

---

## Language Standard

### Office Standard

**Standard:** UK/Australian English spelling shall be used in all BOQ documentation.

**Examples:**
- "colour" not "color"
- "metre" not "meter"  
- "centre" not "center"
- "labour" not "labor"
- "aluminium" not "aluminum"

**Rationale:** Consistency with Australian construction industry standards and client expectations.

**Provenance:** Office standard practice

**References:**
- Australian Standards (AS) terminology
- Client documentation requirements

---

## Workbook Format Standard

### Office Standard

**Standard:** All workbooks shall follow the office standard template structure.

**Template Structure:**
1. Cover page with project identification
2. Table of contents
3. Preambles and assumptions
4. Trade sections following standard trade schedule
5. Summary pages

**Mandatory Elements:**
- Project name and number
- Revision number and date
- Assumptions clearly documented
- "(NB: ...)" notes for important clarifications
- Consistent UOM throughout
- Page numbering

**Typography Standard:**

| Element | Format |
|---------|--------|
| BUILDING/BLOCK | ALL CAPS, Bold, Calibri 11 |
| HEAD1 | ALL CAPS, Bold, Underline, Calibri 11 |
| Head2 | Bold, Underline, Calibri 11 |
| Head3 | Bold, Calibri 11 |
| Head4 (optional) | Underline, Calibri 11 |
| Items with quantities | Italic, Calibri 11 |
| OMISSION/ADDITION | ALL CAPS, Bold, Calibri 11 |

**Provenance:** `docs/reference/office_standards/09_Format-Template for Workbook.docx`

**References:**
- `docs/domain/02_BOQ_Structure.md` - structural rules
- `docs/domain/03_Trade_Schedule.md` - trade sequencing

---

## Validation Requirements

### 1. Bulk Check Validation

**Validation:** Gross Floor Area (GFA) calculated from plans must be compared against Bulk Check workbook.

**Acceptance Criteria:**
- **Pass:** Discrepancy ≤ ±5%
- **Fail:** Discrepancy > ±5%

**Procedure:**
1. Calculate GFA from architectural plans
2. Enter into Bulk Check workbook
3. Compare against measurement totals
4. If discrepancy > ±5%, investigate and document explanation
5. Document reconciliation in project files

**Severity Classification:**
- Discrepancy > ±5% without investigation: **Error**
- Discrepancy > ±5% with documented explanation: **Warning**
- Bulk Check not performed: **Error**

**Provenance:** Office standard practice documented in `docs/reference/office_standards/bulk_check.xlsx`

**References:**
- `docs/reference/office_standards/bulk_check.xlsx` - calculation workbook
- `docs/domain/08_Checking_Workflow.md` - workflow integration

---

### 2. Dimension Group Reconciliation

**Validation:** Quantities in Dimension Groups must reconcile with Workbook quantities.

**Acceptance Criteria:**
- **Pass:** Exact match (allowing rounding differences < 0.01 for same UOM)
- **Fail:** Any unexplained discrepancy ≥ 0.01

**Validation Points:**
- Total quantities per trade
- Major element quantities
- Area calculations
- Linear measurements

**Severity Classification:**
- Missing Dimension Group: **Error**
- Quantity mismatch > 0.01: **Error**
- Rounding difference < 0.01: **Warning** (document if significant)

**Provenance:** Office standard practice

**References:**
- `docs/domain/09_Dimension_Group_Guide.md` - Dimension Group organization

---

### 3. Description Standards

**Validation:** Item descriptions must meet completeness and clarity requirements.

**Acceptance Criteria:**

**Pass Requirements:**
- Complete and unambiguous description
- Technically accurate
- Consistent with standard terminology
- Includes all relevant specification references
- Uses standard abbreviations
- Proper unit of measurement assigned

**Fail Conditions:**
- Ambiguous or incomplete description: **Error**
- Missing specification references: **Warning**
- Non-standard abbreviations: **Warning**
- Incorrect or missing UOM: **Error**

**Quality Checks:**
- No missing items
- No ambiguous descriptions
- Consistent abbreviation usage
- Required assumptions documented

**Provenance:** Office standard practice

**References:**
- `docs/domain/06_Naming_Convention.md` - description construction
- `docs/domain/05_UOM_Standards.md` - unit standards

---

### 4. Assumptions and Notes

**Standard:** All assumptions affecting measurement or pricing must be documented.

**Format Requirements:**

**Preambles Section:**
- General assumptions applicable to entire BOQ
- Clear, concise language
- Reference to drawings or specifications

**Item-Specific Notes:**
- Format: `(NB: ...)`
- Clarify item-specific assumptions
- Explain non-obvious measurements

**Examples:**

```
PREAMBLES
- All measurements taken from architectural drawings revision A
- Structural elements measured to centre lines
- Excavation measured net with 5% allowance for bulking

ITEM NOTES
- Concrete footings (NB: Includes 10mm starter bars)
- Wall finishes (NB: Measured to internal face of wall)
```

**Acceptance Criteria:**
- **Pass:** All assumptions documented
- **Fail:** Missing assumptions that affect measurement: **Error**
- **Fail:** Missing clarifications for ambiguous items: **Warning**

**Provenance:** Office standard practice

**References:**
- `docs/domain/02_BOQ_Structure.md` - preambles placement
- `docs/domain/06_Naming_Convention.md` - notation format

---

## Error Classification

### Errors (Must Fix Before Submission)

**Missing Items:**
- Trade sections with no items
- Known scope elements not included
- Required preliminary items omitted

**Inconsistencies:**
- UOM varies for similar items within same trade
- Description formats differ inconsistently within same trade
- Numbering sequence breaks
- Cross-reference errors

**Incomplete Information:**
- Missing assumptions affecting measurement
- Undefined abbreviations
- Ambiguous descriptions requiring clarification
- Missing critical specification references

**Calculation Errors:**
- Bulk Check exceeds ±5% without documented explanation
- Dimension Group totals don't match Workbook (≥ 0.01 difference)
- Arithmetic errors in quantities
- Formula errors in calculations

**Severity:** **Error** - submission blocked

---

### Warnings (Should Fix, Submission Allowed With Documentation)

**Minor Inconsistencies:**
- Formatting variations that don't affect clarity
- Minor spelling issues (not technical terms)
- Rounding differences < 0.01

**Documentation Gaps:**
- Missing non-critical assumptions
- Optional clarifications not provided
- Suggested but not required notes

**Best Practice Violations:**
- Non-standard but understandable abbreviations
- Acceptable but non-preferred formatting

**Severity:** **Warning** - document and proceed

---

## Acceptance Workflow

### Standard Validation Sequence

1. **Receipt Review**
   - Verify scope
   - Check drawing revisions
   - Identify client-specific requirements

2. **Technical Validation**
   - Validate Dimension Groups exist
   - Check Workbook structure compliance
   - Verify descriptions and UOM

3. **Bulk Check**
   - Calculate GFA
   - Run reconciliation
   - Document results

4. **QA Validation**
   - Description accuracy
   - Assumption completeness
   - Grammar and spelling
   - Formatting consistency

5. **Submission Preparation**
   - Final review
   - Version control
   - Client-specific formatting
   - Documentation package

**Acceptance Criteria:**
- All **Errors** resolved
- All **Warnings** documented
- All validations performed
- All acceptance criteria met

**References:**
- `docs/domain/08_Checking_Workflow.md` - detailed workflow

---

## Exceptions

### Client-Specific Standards

When client standards conflict with office standards:
1. Client standards take precedence (Authority Hierarchy)
2. Document the deviation in project files
3. Note deviation in workbook preambles if significant
4. Ensure consistency within project

**Reference:**
- `docs/domain/07_Client_Conventions.md`

### Novel Project Types

For project types not covered by standard procedures:
1. Consult with Project Owner
2. Document approach in project files
3. Create project-specific guidelines
4. Update standards if pattern is repeatable

---

## Rule Provenance

| Rule ID | Rule | Source | Document |
|---------|------|--------|----------|
| QS-001 | UK/Australian English | Office Standard | Practice convention |
| QS-002 | ±5% Bulk Check tolerance | Office Standard | bulk_check.xlsx |
| QS-003 | Dimension Groups reconcile | Office Standard | Practice convention |
| QS-004 | Workbook template structure | Office Standard | 09_Format-Template for Workbook.docx |
| QS-005 | Typography standards | Office Standard | 09_Format-Template for Workbook.docx |
| QS-006 | Client override authority | Office Practice | Established precedence |
| QS-007 | Error vs Warning classification | Office Standard | Quality management |

---

## References

### Internal Documents
- `docs/domain/02_BOQ_Structure.md` - BOQ hierarchy rules
- `docs/domain/03_Trade_Schedule.md` - Standard trade organization
- `docs/domain/05_UOM_Standards.md` - Unit of measurement standards
- `docs/domain/06_Naming_Convention.md` - Description construction rules
- `docs/domain/07_Client_Conventions.md` - Client-specific overrides
- `docs/domain/08_Checking_Workflow.md` - Detailed QA procedures
- `docs/domain/09_Dimension_Group_Guide.md` - Measurement file organization

### Office Standards
- `docs/reference/office_standards/09_Format-Template for Workbook.docx`
- `docs/reference/office_standards/bulk_check.xlsx`
- `docs/reference/office_standards/12_Units of Measurements.docx`

### External Standards
- Australian Standards (AS) - relevant construction codes
- Client-specific standards documentation (project-dependent)

---

## Related Documents

- **Upstream:** `docs/01_Principles.md` - Platform principles
- **Peer:** `docs/domain/07_Client_Conventions.md` - Authority precedence
- **Downstream:** All domain documents inherit authority hierarchy

---

## Document Control

**Change History:**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-01-15 | Project Owner | Initial scaffold |
| 1.0 | 2026-07-14 | Project Owner | Expanded with domain modeling approach |

**Review Schedule:** Annual or upon significant practice changes

**Distribution:** All quantity surveying staff, Jarvis Platform

---

## TODO

- [ ] TODO(Project Owner): Add specific AS code references for structural measurement validation
- [ ] TODO(Project Owner): Define acceptable rounding tolerances for each UOM type
- [ ] TODO(Project Owner): Document procedure and template for Bulk Check variance explanations
- [ ] TODO(Project Owner): Create examples library of acceptable vs unacceptable assumption documentation
- [ ] TODO(Project Owner): Establish threshold for when **Warnings** require Project Owner escalation