# BOQ Checking Workflow

**Version:** 1.0  
**Status:** Approved  
**Last Updated:** 2026-07-14  
**Owner:** Project Owner  
**Approvers:** Project Owner

---

## Purpose

This document defines the standard workflow for checking Bills of Quantities before submission. This workflow ensures quality, completeness, and compliance with standards.

This is the **Domain Source of Truth** for BOQ quality assurance workflow.

## Scope

This document covers:

- Standard checking sequence
- Validation checkpoints
- Quality assurance steps
- Approval workflow
- Documentation requirements

This document applies to all BOQ checking and quality assurance activities.

---

## Authority

This document records office standard checking procedures.

**It does not supersede:**

- Contract-Specified Review Procedures
- Client-Specific QA Requirements
- Project-Specific Validation Steps

**Priority Hierarchy:**

```
Contract-Mandated Review Process
↓
Client-Specific QA Process
↓
Office Standard Workflow (this document)
↓
Default Practice
```

---

## Capability Consumers

**Current Consumers:**
- BOQ Intelligence (performs automated checks)

**Planned Consumers:**
- CheckMate (will automate workflow validation)
- Quality Dashboard (will track checking progress)

**Future Consumers:**
- To be determined based on capability development

---

## Definitions

**Checker**: The person responsible for validating BOQ accuracy and completeness.

**Validation**: Technical verification of measurements and calculations.

**QA Review**: Quality assurance review of standards compliance.

**Approval**: Final sign-off before submission.

**Checkpoint**: A specific validation step in the workflow.

---

## Standard Checking Workflow

### Source

**Source:** `docs/reference/office_standards/02_BOQ Checking Workflow.docx`

### Workflow Sequence

```
1. Receipt & Scope Review
   ↓
2. Dimension Group Validation
   ↓
3. Workbook Structure Validation
   ↓
4. Item Description Review
   ↓
5. Bulk Check Validation
   ↓
6. Dimension Group Reconciliation
   ↓
7. Quality Assurance Review
   ↓
8. Final Review & Approval
   ↓
9. Submission Preparation
```

---

## Checkpoint 1: Receipt & Scope Review

### Purpose

Verify scope, identify requirements, confirm drawings and specifications.

### Activities

1. **Verify Scope**
   - Confirm project scope matches expectation
   - Identify any scope changes from initial brief
   - Note any ambiguities or missing information

2. **Check Drawings**
   - Verify drawing revision numbers
   - Confirm all required drawings received
   - Note any discrepancies between drawings

3. **Review Specifications**
   - Confirm specification documents received
   - Identify any specification references needed
   - Note any ambiguities requiring clarification

4. **Identify Client Requirements**
   - Check for client-specific standards
   - Note any special formatting requirements
   - Identify submission requirements

### Validation

- [ ] All required drawings received
- [ ] Drawing revisions noted
- [ ] Specifications complete
- [ ] Client requirements identified
- [ ] Scope ambiguities noted

### Output

Document of scope, drawing list, specification list, client requirements

**Provenance:** Office standard practice

---

## Checkpoint 2: Dimension Group Validation

### Purpose

Verify Dimension Groups exist, are organized correctly, and contain measurements.

### Activities

1. **Verify Existence**
   - Confirm Dimension Groups exist for all trades
   - Check folder structure matches standards
   - Verify file naming follows conventions

2. **Check Organization**
   - Validate dimension sheets organized logically
   - Confirm grouping by element/location
   - Verify consistent structure across trades

3. **Spot Check Content**
   - Sample dimensions from major elements
   - Verify dimension formulas correct
   - Check calculation methods appropriate

### Validation

- [ ] Dimension Groups exist for all trades
- [ ] Folder structure correct
- [ ] File naming follows conventions
- [ ] Dimensions organized logically
- [ ] Spot check calculations verified

### Severity

- Missing Dimension Group: **Error**
- Incorrect organization: **Warning**
- Calculation errors: **Error**

**Reference:** `docs/domain/09_Dimension_Group_Guide.md`

**Provenance:** Office quality standard

---

## Checkpoint 3: Workbook Structure Validation

### Purpose

Verify BOQ structure complies with hierarchical rules and formatting standards.

### Activities

1. **Validate Hierarchy**
   - Check hierarchy levels progress correctly
   - Verify no orphan elements
   - Confirm parent-child relationships maintained

2. **Check Trade Schedule**
   - Verify trade sequence appropriate (client vs office)
   - Confirm all required trades present
   - Validate trade naming consistent

3. **Verify Formatting**
   - Check typography follows standards
   - Verify header formatting correct
   - Confirm consistent styling throughout

### Validation

- [ ] Hierarchy structure valid
- [ ] No orphan elements
- [ ] Trade schedule correct
- [ ] All trades present
- [ ] Formatting standards met

### Severity

- Invalid hierarchy: **Error**
- Orphan elements: **Error**
- Wrong trade schedule: **Warning** (if client-specified)
- Formatting issues: **Warning**

**Reference:** `docs/domain/02_BOQ_Structure.md`, `docs/domain/03_Trade_Schedule.md`

**Provenance:** Office quality standard

---

## Checkpoint 4: Item Description Review

### Purpose

Verify item descriptions are complete, accurate, and follow naming conventions.

### Activities

1. **Check Completeness**
   - Verify all mandatory components present
   - Confirm specifications sufficient for procurement
   - Check for ambiguous descriptions

2. **Validate Naming**
   - Verify tags unique and consistent
   - Check dimension formatting correct
   - Confirm terminology appropriate

3. **Review UOM**
   - Validate units appropriate for work type
   - Check unit consistency within trades
   - Verify decimal places correct

4. **Spot Check Specifications**
   - Sample key items for specification accuracy
   - Verify manufacturer references correct
   - Check material grades specified

### Validation

- [ ] All descriptions complete
- [ ] Tags unique and consistent
- [ ] Dimensions formatted correctly
- [ ] Units appropriate and consistent
- [ ] Specifications accurate

### Severity

- Incomplete description: **Error**
- Missing specification: **Warning**
- Incorrect UOM: **Error**
- Ambiguous description: **Error**

**Reference:** `docs/domain/05_UOM_Standards.md`, `docs/domain/06_Naming_Convention.md`

**Provenance:** Office quality standard

---

## Checkpoint 5: Bulk Check Validation

### Purpose

Validate gross floor area calculations reconcile with bulk check within tolerance.

### Activities

1. **Calculate GFA**
   - Measure gross floor area from plans
   - Enter into Bulk Check workbook
   - Calculate expected quantities

2. **Compare with BOQ**
   - Compare Bulk Check totals with BOQ totals
   - Calculate discrepancy percentage
   - Identify areas of significant difference

3. **Investigate Variances**
   - If discrepancy > ±5%, investigate cause
   - Document explanation for variances
   - Adjust measurements if calculation error found

### Validation

- [ ] GFA calculated from plans
- [ ] Bulk Check completed
- [ ] Discrepancy within ±5% OR explained
- [ ] Variances investigated
- [ ] Documentation complete

### Severity

- Bulk Check not performed: **Error**
- Discrepancy > ±5% without explanation: **Error**
- Discrepancy > ±5% with explanation: **Warning**

**Reference:** `docs/domain/01_QS_Office_Standards.md` (Bulk Check Validation)

**Provenance:** Office quality standard

---

## Checkpoint 6: Dimension Group Reconciliation

### Purpose

Verify quantities in Dimension Groups match quantities in Workbook.

### Activities

1. **Extract Totals**
   - Extract total quantities from each Dimension Group
   - Extract corresponding totals from Workbook
   - Group by trade and element

2. **Compare Quantities**
   - Compare Dimension Group totals with Workbook totals
   - Identify discrepancies
   - Check for rounding differences

3. **Investigate Discrepancies**
   - If discrepancy ≥ 0.01, investigate cause
   - Verify dimension formulas correct
   - Check for missing or duplicate items

4. **Document Results**
   - Record reconciliation results
   - Note any acceptable rounding differences
   - Document resolution of discrepancies

### Validation

- [ ] Dimension Group totals extracted
- [ ] Workbook totals extracted
- [ ] Comparison performed
- [ ] Discrepancies ≥ 0.01 investigated
- [ ] Results documented

### Severity

- Missing Dimension Group: **Error**
- Discrepancy ≥ 0.01: **Error**
- Rounding difference < 0.01: **Warning** (document if significant)

**Reference:** `docs/domain/01_QS_Office_Standards.md` (Dimension Group Reconciliation)

**Provenance:** Office quality standard

---

## Checkpoint 7: Quality Assurance Review

### Purpose

Comprehensive review of quality, consistency, and standards compliance.

### Activities

1. **Grammar and Spelling**
   - Check item descriptions for errors
   - Verify preambles and notes clear
   - Confirm terminology consistent

2. **Assumption Documentation**
   - Verify all assumptions documented
   - Check preambles complete
   - Confirm item notes present where needed

3. **Consistency Check**
   - Verify similar items described consistently
   - Check abbreviations used consistently
   - Confirm formatting consistent throughout

4. **Standards Compliance**
   - Verify office standards followed
   - Check client-specific requirements met
   - Confirm language standards applied

### Validation

- [ ] Grammar and spelling checked
- [ ] Assumptions documented
- [ ] Preambles complete
- [ ] Consistency verified
- [ ] Standards compliance confirmed

### Severity

- Missing assumptions: **Error**
- Grammar errors in technical terms: **Warning**
- Inconsistent descriptions: **Warning**
- Standards violations: Varies (see specific standard)

**Reference:** `docs/domain/01_QS_Office_Standards.md`

**Provenance:** Office quality standard

---

## Checkpoint 8: Final Review & Approval

### Purpose

Final sign-off before submission confirming all checks complete and passed.

### Activities

1. **Review Checklist**
   - Confirm all checkpoints completed
   - Verify all **Errors** resolved
   - Document all **Warnings** with explanations

2. **Spot Check**
   - Sample random items for final verification
   - Check key quantities one more time
   - Verify critical specifications

3. **Approval**
   - Checker signs off on quality
   - Project Owner approval if required
   - Document approval in project files

### Validation

- [ ] All checkpoints completed
- [ ] All **Errors** resolved
- [ ] All **Warnings** documented
- [ ] Spot check performed
- [ ] Approval obtained

### Output

Approved BOQ ready for submission

**Provenance:** Office quality standard

---

## Checkpoint 9: Submission Preparation

### Purpose

Prepare final deliverables for client submission.

### Activities

1. **Version Control**
   - Confirm revision number correct
   - Update revision history
   - Verify date current

2. **File Preparation**
   - Save final version
   - Create PDF if required
   - Prepare supporting documentation

3. **Client-Specific Formatting**
   - Apply any client-specific final formatting
   - Verify client requirements met
   - Check file naming conventions

4. **Documentation Package**
   - Include all required documents
   - Verify completeness
   - Organize per client requirements

### Validation

- [ ] Version control complete
- [ ] Files prepared
- [ ] Client formatting applied
- [ ] Documentation package complete
- [ ] Ready for submission

### Output

Final submission package

**Provenance:** Office practice

---

## Exception Handling

### When Errors Found

**Procedure:**
1. Document error clearly
2. Return to appropriate checkpoint for correction
3. Re-validate after correction
4. Continue workflow

### When Timeline Critical

**Procedure:**
1. Prioritize **Error** resolution
2. Document **Warnings** for post-submission correction
3. Obtain Project Owner approval for proceeding with documented warnings
4. Submit with clear documentation of outstanding items

### When Client Requirements Unclear

**Procedure:**
1. Seek clarification from client
2. Document assumption if clarification not available
3. Proceed with documented assumption
4. Flag for confirmation upon submission

---

## Rule Provenance

| Rule ID | Rule | Source | Document |
|---------|------|--------|----------|
| WF-001 | Bulk Check Within ±5% | Office Standard | 02_BOQ Checking Workflow.docx |
| WF-002 | Dimension Group Reconciliation | Office Standard | 02_BOQ Checking Workflow.docx |
| WF-003 | All Checkpoints Required | Office Standard | Quality management |
| WF-004 | Errors Must Be Resolved | Office Standard | Quality management |
| WF-005 | Warnings Must Be Documented | Office Standard | Quality management |

---

## References

### Internal Documents
- `docs/domain/01_QS_Office_Standards.md` - Quality standards and validation rules
- `docs/domain/02_BOQ_Structure.md` - Structure validation
- `docs/domain/03_Trade_Schedule.md` - Trade sequence validation
- `docs/domain/05_UOM_Standards.md` - Unit validation
- `docs/domain/06_Naming_Convention.md` - Description validation
- `docs/domain/09_Dimension_Group_Guide.md` - Dimension Group validation

### Office Standards
- `docs/reference/office_standards/02_BOQ Checking Workflow.docx` - Workflow definition

---

## Related Documents

- **Upstream:** `docs/domain/01_QS_Office_Standards.md` - Defines validation rules
- **Peer:** All domain documents (provide validation criteria)
- **Downstream:** All BOQ submission activities

---

## Document Control

**Change History:**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-01-15 | Project Owner | Initial scaffold |
| 1.0 | 2026-07-14 | Project Owner | Expanded with complete workflow and checkpoints |

**Review Schedule:** Annual or upon process improvements

**Distribution:** All quantity surveying staff, Jarvis Platform

---

## TODO

- [ ] TODO(Project Owner): Create detailed checklist template for each checkpoint
- [ ] TODO(Project Owner): Define time estimates for each checkpoint
- [ ] TODO(Project Owner): Establish quality metrics for tracking
- [ ] TODO(Project Owner): Document escalation procedures for blocked workflows
- [ ] TODO(Project Owner): Create training materials for workflow
- [ ] TODO(Project Owner): Define roles and responsibilities at each checkpoint