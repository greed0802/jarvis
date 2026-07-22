# Domain Glossary

**Version:** 1.1  
**Last Updated:** 2026-07-14

---

## Purpose

This glossary defines key terms used across the Domain Knowledge Layer. Terms are organized alphabetically for quick reference.

Each major term includes:

- Definition
- **See also**: Related concepts for deeper understanding
- **Related Rule IDs**: Specific rules governing this concept (where applicable)

---

## A

**Acceptance Criteria**

Thresholds that determine whether a validation check passes or fails. Different from the validation itself.

*See also*: Validation, Error, Warning, Severity

*Related Rule IDs*: QS-007 (Error vs Warning classification)

---

**Addendum**

A formal document containing omissions and additions to the original BOQ.

*See also*: Omission, Addition, Global Revision, Local Revision

*Related Rule IDs*: OA-001 through OA-007

---

**Addition**

Introduction or increase of scope to the original or revised BOQ, represented by positive quantities.

*See also*: Omission, Global Revision, Local Revision

*Related Rule IDs*: OA-005, OA-006

---

**Approval**

Final sign-off before BOQ submission confirming all checks are complete and passed.

*See also*: Checkpoint, QA Review, Validation

---

**Authority Hierarchy**

The precedence order for standards: Contract → Client → Office → Default.

*See also*: Client Convention, Contract Requirement, Office Standard

---

## B

**Bill of Quantities (BOQ)**

A document listing all work items with descriptions, quantities, units, and rates for a construction project.

*See also*: Workbook, Measured Item, Hierarchy Level 1-N

---

**BOQ Hierarchy**

The nested structure of headers and items organizing quantity information from general to specific.

*See also*: Hierarchy Level 1-N, Measured Item, Structural Semantics

*Related Rule IDs*: V-001 through V-005, SEM-001 through SEM-005

---

**Bulk Check**

A validation procedure comparing plan gross areas against calculated areas using the office Bulk Check workbook.

*See also*: Acceptance Criteria, Gross Floor Area (GFA)

*Related Rule IDs*: QS-002, WF-001

---

## C

**Checker**

The person responsible for validating BOQ accuracy and completeness.

*See also*: Checkpoint, QA Review

---

**Checkpoint**

A specific validation step in the checking workflow.

*See also*: Validation, Checker, Workflow

*Related Rule IDs*: WF-003

---

**Client Convention**

A standard, practice, or requirement specified by a client that differs from office default standards.

*See also*: Authority Hierarchy, Client Documentation, Office Standard

*Related Rule IDs*: CONV-001 through CONV-004

---

**Client Documentation**

Records of client-specific conventions maintained for consistency across projects.

*See also*: Client Convention, Project Files

---

**Client Preference**

A non-mandatory preference expressed by the client.

*See also*: Client Convention, Contract Requirement

---

**Client Schedule**

A trade schedule specified or preferred by a particular client.

*See also*: Trade Schedule, Office Standard

*Related Rule IDs*: TS-001, TS-005

---

**Common Description**

The general category or type of work in an item description (e.g., "Pad Footing", "Ceramic tile").

*See also*: Specific Description, Description Pattern, Item Tag

---

**Contract Requirement**

A mandatory requirement explicitly stated in contract documents.

*See also*: Authority Hierarchy, Client Convention

---

## D

**Decimal Places**

The number of digits displayed after the decimal point in quantities.

*See also*: Rounding Convention, Unit of Measurement (UOM)

---

**Description Pattern**

The standard structure for constructing item descriptions.

*See also*: Common Description, Specific Description, Item Tag

*Related Rule IDs*: NC-003

---

**Dimension Group**

A CostX measurement file (.5dx) containing organized dimension sheets for a specific trade or building element.

*See also*: Dimension Sheet, Folder Structure, Reconciliation

*Related Rule IDs*: DG-001 through DG-004

---

**Dimension Sheet**

A worksheet within a Dimension Group file containing measurements for a specific element or location.

*See also*: Dimension Group, Folder Structure

---

**Dimensions**

Size specifications in the format Length × Width × Height/Depth.

*See also*: Description Pattern, Item Tag

*Related Rule IDs*: NC-002

---

**Domain Concept**

System-independent concept (e.g., Hierarchy Level 1-N) that applies regardless of estimating software.

*See also*: System Representation, Structural Semantics

---

**Drawing Folder**

A directory containing project drawings organized by discipline and category.

*See also*: Drawing Register, Drawing Reference

---

**Drawing Reference**

The unique identifier for a drawing (e.g., drawing number).

*See also*: Drawing Register, Revision

*Related Rule IDs*: DO-004

---

**Drawing Register**

A document listing all project drawings with revision status.

*See also*: Drawing Reference, Revision, Drawing Folder

*Related Rule IDs*: DO-002

---

## E

**Elemental Trade Schedule**

An alternative organization grouping by building element rather than construction trade.

*See also*: Trade Schedule

*Related Rule IDs*: TS-004

---

**Error**

A validation failure that must be corrected before submission. Blocks submission.

*See also*: Warning, Severity, Acceptance Criteria

*Related Rule IDs*: QS-007

---

## F

**Folder Structure**

The hierarchical organization of files by discipline, trade, and category.

*See also*: Dimension Group, Drawing Folder

---

## G

**Global Revision**

Complete replacement of an original item with a new specification or quantity through omission and addition.

*See also*: Local Revision, Omission, Addition

*Related Rule IDs*: OA-001, OA-002

---

**Gross Floor Area (GFA)**

Total floor area calculated from plans, used in bulk check validation.

*See also*: Bulk Check

*Related Rule IDs*: QS-002

---

## H

**Header (Hierarchy Level 1-N)**

Provides descriptive context for grouped work. Never carries quantities.

*See also*: Hierarchy Level 1-N, Section, Measured Item

*Related Rule IDs*: SEM-002

---

**Hierarchy Level 1**

Top-level trade or section header (e.g., "SUBSTRUCTURE", "SUPERSTRUCTURE").

*See also*: Hierarchy Level 2-N, BOQ Hierarchy

---

**Hierarchy Level 2**

Second-level header subdividing Level 1 (e.g., "Strip Footings", "Ground Floor Slab").

*See also*: Hierarchy Level 1, Hierarchy Level 3-N

---

**Hierarchy Level N**

Additional subdivision levels as required by project complexity.

*See also*: BOQ Hierarchy, Structural Semantics

---

## I

**Item Tag**

A short alphanumeric identifier prefixing an item description (e.g., PF1, CT1, J01).

*See also*: Description Pattern, Common Description, Specific Description

*Related Rule IDs*: NC-001

---

## L

**Local Revision**

Adjustment of only the changed portion of an original item's quantity through partial omission or addition.

*See also*: Global Revision, Omission, Addition

*Related Rule IDs*: OA-003, OA-004

---

**Logical Consistency**

The principle that BOQ structure must remain meaningful and hierarchically sound regardless of absolute positioning.

*See also*: BOQ Hierarchy, Structural Integrity

---

## M

**Measured Item**

A measurable quantity with description, UOM, and quantity (e.g., "Plain concrete 20MPa to footings: m³: 12.50").

*See also*: BOQ Hierarchy, Hierarchy Level 1-N, Header, Section

*Related Rule IDs*: SEM-003

---

## O

**Office Standard**

The default practice when no client-specific requirement exists.

*See also*: Authority Hierarchy, Client Convention

---

**Omission**

Removal or reduction of scope from the original BOQ, represented by negative quantities.

*See also*: Addition, Global Revision, Local Revision

*Related Rule IDs*: OA-005

---

**Original**

The baseline BOQ item before any revisions are applied.

*See also*: Global Revision, Local Revision, Addendum

*Related Rule IDs*: OA-007

---

## Q

**QA Review**

Quality assurance review of standards compliance.

*See also*: Checkpoint, Validation, Checker

---

## R

**Reconciliation**

The process of verifying Dimension Group totals match Workbook quantities.

*See also*: Dimension Group, Workbook

*Related Rule IDs*: QS-003, DG-004, WF-002

---

**Revision**

A version of a drawing or BOQ reflecting design changes.

*See also*: Drawing Register, Global Revision, Local Revision

---

**Rounding Convention**

The rule for determining decimal places and rounding direction for quantities.

*See also*: Decimal Places, Unit of Measurement (UOM)

---

**Rule Provenance**

Documentation of where each rule originates (contract, client, office, or standard practice).

*See also*: Authority Hierarchy, Rule ID

---

## S

**Section (Hierarchy Level 1-N)**

Groups related work into logical organizational units. Never carries quantities.

*See also*: Header, Hierarchy Level 1-N, BOQ Hierarchy

*Related Rule IDs*: SEM-001

---

**Semantic Inheritance**

Child elements inherit meaning from all parent headers in the hierarchy.

*See also*: Structural Semantics, BOQ Hierarchy

*Related Rule IDs*: SEM-004, SEM-005

---

**Severity**

Classification of validation failures as Error (must fix) or Warning (should fix, document).

*See also*: Error, Warning, Acceptance Criteria

*Related Rule IDs*: QS-007

---

**Special Unit**

A non-quantitative unit type used for organizational or calculation purposes (e.g., noidc, endh1).

*See also*: Unit of Measurement (UOM)

---

**Specific Description**

Detailed specifications unique to an item (e.g., material grade, manufacturer, finish).

*See also*: Common Description, Description Pattern, Item Tag

---

**Structural Integrity**

The property that parent-child relationships are maintained throughout the BOQ.

*See also*: BOQ Hierarchy, Logical Consistency

*Related Rule IDs*: V-001, V-002

---

**Structural Semantics**

Fundamental semantic rules defining what each structural element means and how it behaves, independent of formatting.

*See also*: Section, Header, Measured Item, Hierarchy

*Related Rule IDs*: SEM-001 through SEM-005

---

**System Representation**

How a system-specific tool (e.g., CostX) represents domain concepts using its own terminology.

*See also*: Domain Concept

---

## T

**Trade Schedule**

An ordered list of work sections (trades) defining the standard sequence for organizing BOQ content.

*See also*: Hierarchy Level 1, Client Schedule, Office Standard

*Related Rule IDs*: TS-001 through TS-005

---

## U

**Unit of Measurement (UOM)**

The standard quantity used to express measurement magnitude (e.g., m, m², m³, no, t, Item).

*See also*: Decimal Places, Rounding Convention, Special Unit

*Related Rule IDs*: UOM-001 through UOM-003

---

## V

**Validation**

Technical verification of measurements, calculations, or compliance with rules.

*See also*: Checkpoint, Acceptance Criteria, QA Review

---

**Warning**

A validation issue that should be fixed and documented but doesn't block submission.

*See also*: Error, Severity, Acceptance Criteria

*Related Rule IDs*: QS-007

---

**Workbook**

The Excel-based Bill of Quantities document containing measurements, descriptions, quantities, and rates.

*See also*: Bill of Quantities (BOQ), Dimension Group, Reconciliation

---

## Cross-References

For detailed definitions and usage rules, refer to:

- **01_QS_Office_Standards.md**: Quality standards, Error/Warning, Bulk Check
- **02_BOQ_Structure.md**: Hierarchy levels, Structural Semantics
- **03_Trade_Schedule.md**: Trade organization, scheduling rules
- **04_Omission_Addition.md**: Revision methodology, sign conventions
- **05_UOM_Standards.md**: Units of measurement, rounding
- **06_Naming_Convention.md**: Description patterns, tags, folders
- **07_Client_Conventions.md**: Client precedence, documentation
- **08_Checking_Workflow.md**: Validation checkpoints, workflows
- **09_Dimension_Group_Guide.md**: Dimension files, reconciliation
- **10_Drawing_Organization.md**: Drawing management, versioning

---

## Complete Rule ID Index

| Rule ID | Concept | Document |
|---------|---------|----------|
| QS-001 | UK/Australian English | 01_QS_Office_Standards.md |
| QS-002 | ±5% Bulk Check tolerance | 01_QS_Office_Standards.md |
| QS-003 | Dimension Groups reconcile | 01_QS_Office_Standards.md |
| QS-004 | Workbook template structure | 01_QS_Office_Standards.md |
| QS-005 | Typography standards | 01_QS_Office_Standards.md |
| QS-006 | Client override authority | 01_QS_Office_Standards.md |
| QS-007 | Error vs Warning classification | 01_QS_Office_Standards.md |
| V-001 | Parent Exists | 02_BOQ_Structure.md |
| V-002 | No Orphans | 02_BOQ_Structure.md |
| V-003 | Level Progression | 02_BOQ_Structure.md |
| V-004 | Scope Containment | 02_BOQ_Structure.md |
| V-005 | Completeness | 02_BOQ_Structure.md |
| SEM-001 | Sections Never Measure | 02_BOQ_Structure.md |
| SEM-002 | Headers Provide Context | 02_BOQ_Structure.md |
| SEM-003 | Items Always Quantify | 02_BOQ_Structure.md |
| SEM-004 | Inheritance Flows Downward | 02_BOQ_Structure.md |
| SEM-005 | Semantic Completeness | 02_BOQ_Structure.md |
| TS-001 | Client schedule precedence | 03_Trade_Schedule.md |
| TS-002 | Commercial standard sequence | 03_Trade_Schedule.md |
| TS-003 | Residential standard sequence | 03_Trade_Schedule.md |
| TS-004 | Elemental organization | 03_Trade_Schedule.md |
| TS-005 | Client schedule extensibility | 03_Trade_Schedule.md |
| OA-001 | Global Omission Equals Original | 04_Omission_Addition.md |
| OA-002 | Global Addition Independent | 04_Omission_Addition.md |
| OA-003 | Local Adjustment Magnitude | 04_Omission_Addition.md |
| OA-004 | Local Addition Unbounded | 04_Omission_Addition.md |
| OA-005 | Omission Sign Convention | 04_Omission_Addition.md |
| OA-006 | Addition Sign Convention | 04_Omission_Addition.md |
| OA-007 | Original Sign Convention | 04_Omission_Addition.md |
| UOM-001 | Same Item Same Unit | 05_UOM_Standards.md |
| UOM-002 | Trade Unit Consistency | 05_UOM_Standards.md |
| UOM-003 | Appropriate Unit for Work Type | 05_UOM_Standards.md |
| NC-001 | Tag Uniqueness Within Category | 06_Naming_Convention.md |
| NC-002 | Dimension Order Consistency | 06_Naming_Convention.md |
| NC-003 | Description Completeness | 06_Naming_Convention.md |
| NC-004 | Abbreviation Consistency | 06_Naming_Convention.md |
| CONV-001 | Client Precedence | 07_Client_Conventions.md |
| CONV-002 | Consistency Within Project | 07_Client_Conventions.md |
| CONV-003 | Documentation Required | 07_Client_Conventions.md |
| CONV-004 | No Unsolicited "Improvement" | 07_Client_Conventions.md |
| WF-001 | Bulk Check Within ±5% | 08_Checking_Workflow.md |
| WF-002 | Dimension Group Reconciliation | 08_Checking_Workflow.md |
| WF-003 | All Checkpoints Required | 08_Checking_Workflow.md |
| WF-004 | Errors Must Be Resolved | 08_Checking_Workflow.md |
| WF-005 | Warnings Must Be Documented | 08_Checking_Workflow.md |
| DG-001 | Dimension Groups Required | 09_Dimension_Group_Guide.md |
| DG-002 | Standard Folder Structure | 09_Dimension_Group_Guide.md |
| DG-003 | Descriptive File Naming | 09_Dimension_Group_Guide.md |
| DG-004 | Quantities Must Reconcile | 09_Dimension_Group_Guide.md |
| DO-001 | Drawings Must Be Organized | 10_Drawing_Organization.md |
| DO-002 | Drawing Register Required | 10_Drawing_Organization.md |
| DO-003 | Current Revisions Identified | 10_Drawing_Organization.md |
| DO-004 | Drawing References Documented | 10_Drawing_Organization.md |

**Total: 52 Rule IDs**
No duplicates. No skipped sequences. Consistent numbering within each prefix.

---

## Document Control

**Maintenance**: Update when new terms are introduced or existing definitions require clarification.

**Review**: Annual or when domain documents are updated.