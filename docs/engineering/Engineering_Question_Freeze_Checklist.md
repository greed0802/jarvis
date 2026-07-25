# Engineering Question Freeze Checklist

**Authority:** EQ-0017 Repository Governance Migration
**Status:** Active
**Version:** 1.0
**Date:** 2026-07-23

---

## Purpose

This checklist defines the mandatory requirements for freezing any Engineering Question in the Jarvis repository. Freeze represents the formal completion of an Engineering Question and its readiness for Project Owner disposition.

Every Engineering Question MUST pass all checklist items before being marked as "Completed" in the Engineering Register.

---

## Freeze Checklist

### ✅ Authority Document Complete

- [ ] **Problem Statement**: Clearly defined engineering problem
- [ ] **Research Question**: Specific, answerable question formulated
- [ ] **Scope**: Investigation boundaries explicitly defined
- [ ] **Non-Goals**: Out-of-scope items documented
- [ ] **Investigation Plan**: Methodology and approach specified
- [ ] **Success Criteria**: Objective measures of completion
- [ ] **Exit Criteria**: Conditions for concluding investigation
- [ ] **Decision Framework**: How findings will be evaluated
- [ ] **Stakeholders**: All relevant parties identified
- [ ] **Dependencies**: External requirements documented
- [ ] **Risks**: Potential issues and mitigation strategies
- [ ] **Project Owner Approval**: Initial authorization obtained

### ✅ Evidence Package Complete

- [ ] **Dedicated Package**: `docs/engineering/evidence/EQ_XXXX/` created
- [ ] **Package README**: Contains standard metadata sections
- [ ] **Evidence Reports**: All spikes documented with findings
- [ ] **Investigation Tools**: All scripts preserved in package
- [ ] **Data Reports**: All generated artifacts included
- [ ] **Capability Matrix**: Final state documented (if applicable)
- [ ] **Migration Documentation**: Asset relocation records (if applicable)
- [ ] **Compliance Report**: Governance adherence evidence

### ✅ Investigation Reproducible

- [ ] **Spike Scripts**: All investigation tools preserved
- [ ] **Fixture References**: Source data identified and accessible
- [ ] **Methodology Documentation**: Step-by-step process recorded
- [ ] **Environment Specifications**: Execution context documented
- [ ] **Result Verification**: Independent reproduction possible
- [ ] **Deterministic Outcomes**: Identical inputs produce identical outputs

### ✅ Reports Finalized

- [ ] **Findings Documented**: All observations recorded
- [ ] **Traceability Established**: Finding → Evidence → Fixture → Spike chain
- [ ] **Conclusions Evidence-Based**: All conclusions supported by data
- [ ] **Recommendations Justified**: Implementation rationale provided
- [ ] **Alternative Approaches**: Considered options documented
- [ ] **Limitations Acknowledged**: Known gaps and constraints identified
- [ ] **Future Work**: Deferred investigations or enhancements noted

### ✅ Generated Artifacts Classified

- [ ] **Data Reports**: Categorized by spike and purpose
- [ ] **Tools**: Classified as historical vs reusable
- [ ] **Contracts**: Related contracts identified and referenced
- [ ] **ADRs**: Architectural decisions documented
- [ ] **Capability Matrices**: Final state preserved
- [ ] **Verification Artifacts**: Quality gate evidence included

### ✅ Tool Promotion Reviewed

- [ ] **Reusable Tools**: Identified for promotion to `tools/quality/`
- [ ] **Promotion Justification**: Business case documented
- [ ] **Historical Tools**: Preserved in original EQ package
- [ ] **Tool Registry**: Updated with new promotions
- [ ] **Manifest**: `tools/manifest.json` updated
- [ ] **Contract Compliance**: Promoted tools follow quality tool contract

### ✅ Documentation Links Verified

- [ ] **Internal Links**: All markdown links functional
- [ ] **Relative Paths**: Follow `../questions/` pattern for authority docs
- [ ] **Cross-References**: All EQ references accurate
- [ ] **No Broken Links**: Systematic validation performed
- [ ] **Navigation**: Engineering Register links tested
- [ ] **Evidence Package Links**: README references verified

### ✅ Engineering Register Updated

- [ ] **EQ Entry**: Added to Active Engineering Questions table
- [ ] **Authority Document**: Correct path to `questions/EQ_XXXX.md`
- [ ] **Evidence Package**: Correct path to `evidence/EQ_XXXX/`
- [ ] **Status**: Accurate completion status
- [ ] **Outcome**: Disposition recorded
- [ ] **Repository Location**: Standardized format
- [ ] **Metadata**: Owner, dates, related ADRs/contracts (if available)

### ✅ Repository Governance Audit Passed

- [ ] **Structure**: Follows EQ-0016 governance model
- [ ] **Naming Conventions**: Standard patterns applied
- [ ] **No Orphaned Assets**: All artifacts properly classified
- [ ] **No Duplicated Assets**: No redundant evidence
- [ ] **Asset Location**: All files in correct directories
- [ ] **Governance Compliance**: Adheres to Engineering Governance v1.0

### ✅ Project Owner Approval Recorded

- [ ] **Approval Date**: Documented in authority document
- [ ] **Approval Criteria**: All requirements met
- [ ] **Disposition**: Formal decision recorded
- [ ] **Implementation Authorization**: Granted if applicable
- [ ] **Freeze Confirmation**: Explicit approval obtained
- [ ] **Engineering Register**: Status updated to "Completed"

---

## Freeze Process

### Step 1: Pre-Freeze Review
- Engineering team performs self-audit against checklist
- All checklist items marked complete
- Evidence package finalized
- Authority document finalized

### Step 2: Quality Gate Verification
- Run `tools/quality/verify_all.py` for automated checks
- Execute `tools/quality/verify_documentation.py` for link validation
- Run `tools/quality/verify_registry.py` for register integrity
- Address any findings before proceeding

### Step 3: Project Owner Review
- Submit freeze request with checklist evidence
- Project Owner performs independent verification
- Project Owner records approval or requests corrections
- If approved, proceed to freeze

### Step 4: Freeze Execution
- Update Engineering Register status to "Completed"
- Update authority document status to "COMPLETED"
- Record freeze date and Project Owner approval
- Archive any superseded documents
- Announce freeze completion

### Step 5: Post-Freeze Validation
- Verify all links still functional
- Confirm Engineering Register accuracy
- Validate evidence package accessibility
- Document any remaining known issues

---

## Checklist Version History

| Version | Date | Changes | Authority |
|---------|------|---------|-----------|
| 1.0 | 2026-07-23 | Initial checklist established | EQ-0017 |

---

## Relationship to Governance

This checklist implements the freeze requirements defined in:
- `docs/engineering/Engineering_Governance.md` § Investigation Approval Gates
- `AGENTS.md` § Engineering Workflow
- `docs/engineering/Quality_Assurance_Constitution.md` Quality Gate 2

---

## Usage Requirements

**Mandatory**: This checklist is required for ALL Engineering Questions starting with EQ-0018.

**Retrospective Application**: EQ-0010 through EQ-0017 are grandfathered but should be audited against this checklist during governance hardening sprints.

**Tool Integration**: Future versions may integrate with automated verification tools.

**Evolution**: Checklist may be updated through governance evolution process with version tracking.