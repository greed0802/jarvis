# Domain Knowledge Layer

**Version:** 1.1  
**Last Updated:** 2026-07-14  
**Status:** Complete

---

## Purpose

This directory contains the **Domain Knowledge Layer** for the Jarvis Platform. These documents define quantity surveying domain knowledge in a system-independent, implementation-agnostic manner.

This is **not** system documentation.

This is **not** API documentation.

This is **domain truth**.

---

## What This Layer Contains

The Domain Knowledge Layer captures:

- Quantity surveying practices
- Office standards and conventions
- Validation rules and criteria
- BOQ structure and organization
- Quality assurance workflows
- Measurement principles

These specifications are:

- **Implementation-independent**: Don't describe software
- **System-agnostic**: Apply regardless of estimating tool
- **Evidence-based**: Describe what IS, not what might be
- **Traceable**: Every rule has provenance
- **Governed**: Clear authority hierarchy

---

## Reading Order

New readers should follow this sequence:

1. **README.md** (this document) — Overview and navigation
2. **01_QS_Office_Standards.md** — Core quality framework
3. **02_BOQ_Structure.md** — Fundamental structure concepts
4. **03_Trade_Schedule.md** — Trade organization
5. **04_Omission_Addition.md** — Revision methodology
6. **05_UOM_Standards.md** — Units of measurement
7. **06_Naming_Convention.md** — Description conventions
8. **07_Client_Conventions.md** — Client management
9. **08_Checking_Workflow.md** — Quality workflow
10. **09_Dimension_Group_Guide.md** — Measurement files
11. **10_Drawing_Organization.md** — Drawing management
12. **glossary.md** — Term reference

Documents 01-03 establish the core patterns. Documents 04-10 specialize into specific domains.

---

## Document Dependency Diagram

```
01_QS_Office_Standards.md (Core Quality Framework)
  ├── defines Error/Warning taxonomy used by all
  ├── defines validation rules used by 08
  ├── defines Bulk Check used by 08
  └── references 02, 03, 05, 06, 07, 08, 09

02_BOQ_Structure.md (Core Structure)
  ├── defines Hierarchy Levels used by 03
  ├── defines Structural Semantics
  ├── references 01, 03, 06, 07
  └── referenced by 08 (structure validation)

03_Trade_Schedule.md (Core Trade Organization)
  ├── defines Level 1 trades used by 02
  ├── references 01, 02, 07
  └── referenced by 08 (trade validation)

04_Omission_Addition.md (Revision Methodology)
  ├── defines sign conventions
  ├── references 01, 02
  └── independent specialization

05_UOM_Standards.md (Units)
  ├── defines UOM rules
  ├── references 01, 02, 06
  └── referenced by 08 (unit validation)

06_Naming_Convention.md (Naming)
  ├── defines description patterns
  ├── defines folder structures (used by 09, 10)
  ├── references 01, 02, 05
  └── referenced by 08 (description validation)

07_Client_Conventions.md (Client Management)
  ├── defines precedence hierarchy
  ├── references 01-06 (peers)
  └── referenced by all documents for authority

08_Checking_Workflow.md (Quality Workflow)
  ├── consumes rules from 01-06, 09
  ├── orchestrates validation checkpoints
  └── references all peer documents

09_Dimension_Group_Guide.md (Dimension Files)
  ├── defines measurement file organization
  ├── references 01, 06, 07, 08, 10
  └── references 06 for folder structure

10_Drawing_Organization.md (Drawings)
  ├── defines drawing management
  ├── references 06, 07, 09
  └── references 06 for folder structure

glossary.md (Term Reference)
  └── references all documents
```

---

## Document Classification

### Concept-Defining Documents
Documents that define the core concepts of the domain:

- **02_BOQ_Structure.md**: Hierarchy Level 1-N, Measured Item, Section, Header
- **04_Omission_Addition.md**: Global Revision, Local Revision, Omission, Addition
- **05_UOM_Standards.md**: Standard Units, Special Units

### Rule-Defining Documents
Documents that define the validation rules:

- **01_QS_Office_Standards.md**: QS-001 through QS-007
- **02_BOQ_Structure.md**: V-001 through V-005, SEM-001 through SEM-005
- **03_Trade_Schedule.md**: TS-001 through TS-005
- **04_Omission_Addition.md**: OA-001 through OA-007
- **05_UOM_Standards.md**: UOM-001 through UOM-003
- **06_Naming_Convention.md**: NC-001 through NC-004
- **07_Client_Conventions.md**: CONV-001 through CONV-004
- **08_Checking_Workflow.md**: WF-001 through WF-005
- **09_Dimension_Group_Guide.md**: DG-001 through DG-004
- **10_Drawing_Organization.md**: DO-001 through DO-004

### Workflow-Defining Documents
Documents that describe processes and workflows:

- **08_Checking_Workflow.md**: Nine-checkpoint quality workflow
- **04_Omission_Addition.md**: Revision scenarios

### Reference Documents
Documents that organize and reference knowledge:

- **01_QS_Office_Standards.md**: Quality framework (also rules)
- **07_Client_Conventions.md**: Client precedence (also rules)
- **glossary.md**: Term definitions with cross-references
- **README.md** (this document): Navigation and overview

---

## Authority Hierarchy

All domain documents follow this precedence:

```
Contract Requirements
↓
Client-Specific Standards
↓
Office Standards (these documents)
↓
Default Practices
```

Client requirements always take precedence over office standards.

---

## Document Pattern

Every domain document follows this structure:

### Required Sections

1. **Purpose**: What this document defines
2. **Scope**: What is covered
3. **Authority**: Precedence hierarchy
4. **Capability Consumers**: Who/what uses this knowledge
5. **Definitions**: Key terms
6. **Domain Rules**: The actual standards
7. **Exceptions**: When rules don't apply
8. **Rule Provenance**: Where rules come from
9. **References**: Related documents
10. **Document Control**: Version history

### Optional Sections

- Validation Rules (when applicable)
- Examples (when helpful)
- System Representations (when multiple systems exist)

---

## Key Principles

### 1. Evidence-Based

Documents describe what **IS** true about BOQs and QS practice.

They do **NOT** describe:
- Future capabilities that might use them
- Potential AI reasoning
- Speculative implementations

### 2. System-Agnostic

Domain concepts (e.g., Hierarchy Level 1-N, Measured Item) are independent of any estimating system.

System-specific representations (e.g., CostX Head1-4, Item) are documented separately.

### 3. Capability Consumers

Each document lists:
- **Current Consumers**: Existing capabilities that use this knowledge
- **Planned Consumers**: Capabilities committed to roadmap
- **Future Consumers**: "To be determined" - no speculation

### 4. Rule Provenance

Every rule documents its source:
- Office Standard
- Client Requirement
- Contract Mandate
- Australian Standards
- Professional Practice

### 5. Traceability

Rules have IDs (e.g., QS-001, V-001, UOM-001) for:
- Clear references
- Implementation tracking
- Validation reporting

---

## Using These Documents

### For Quantity Surveyors

These documents formalize office practice. They serve as:
- Training materials
- Quality checklists
- Standards reference
- Client communication

### For Jarvis Platform

These documents provide:
- Validation criteria
- Parsing rules
- Quality standards
- Domain semantics

The platform **reads** these documents.

The platform does **not modify** these documents.

### For Future Capabilities

New capabilities can consume this domain knowledge without requiring:
- Architecture changes
- Domain knowledge rewrites
- System modifications

Domain knowledge is decoupled from implementation.

---

## Domain Layer Metrics

| Metric | Value |
|--------|-------|
| Documents | 12 |
| Rule IDs | 52 |
| Defined Concepts | 50+ (in glossary) |
| Cross-References | 36+ (between documents) |
| TODO Items | ~65 |
| Capability Consumers (Current) | Parser, BOQ Intelligence |
| Capability Consumers (Planned) | CheckMate, Formatter |
| Total Lines | ~5,100 |

---

## Current TODO Classification

### Future Domain Knowledge
- [ ] Define acceptable rounding tolerances for each UOM type (01_QS, 05_UOM)
- [ ] Document multi-stage revisions (04_OA)
- [ ] Create comprehensive abbreviation glossary (06_NC)
- [ ] Document MEP naming standards (06_NC)

### Future Capability
- [ ] Create validation test cases for common errors (05_UOM, 06_NC)
- [ ] Define quality metrics for tracking (08_WF)
- [ ] Create training materials (08_WF, 09_DG)

### Client Knowledge
- [ ] Document trade schedule for top 3 recurring clients (03_TS)
- [ ] Create template for client-specific documentation (07_CC)
- [ ] Document client-specific naming variations (06_NC)
- [ ] Document client-specific organizational patterns (09_DG)

### Evidence Needed
- [ ] Add specific AS code references for structural measurement validation (01_QS)
- [ ] Document conversion factors for imperial to metric (05_UOM)

### Office Decision Required
- [ ] Establish threshold for when Warnings require escalation (01_QS)
- [ ] Define maximum acceptable hierarchy depth (02_BOQ)
- [ ] Establish when V-005 transitions from Warning to Error (02_BOQ)
- [ ] Define procedure for handling hybrid trade schedules (03_TS, 06_NC)

---

## Extensibility

### Adding Client-Specific Knowledge

Client-specific conventions don't require:
- New documents
- System changes
- Architecture modifications

Document client conventions in:
- Project files
- Client-specific documentation
- References in domain documents

### Adding New Rules

When adding rules:
1. Identify which document it belongs to
2. Follow the established pattern
3. Assign rule ID
4. Document provenance
5. Add to Rule Provenance table

### Adding New Concepts

When domain concepts emerge:
1. Determine if it's truly new or fits existing documents
2. If new document needed, follow established pattern
3. Cross-reference from related documents
4. Update glossary
5. Update this README

---

## Document Status

| Document | Status | Lines | Version | Type |
|----------|--------|-------|---------|------|
| 01_QS_Office_Standards.md | ✅ Complete | 468 | 1.0 | Core + Rules |
| 02_BOQ_Structure.md | ✅ Complete | 785 | 1.0 | Core + Concepts + Rules |
| 03_Trade_Schedule.md | ✅ Complete | 329 | 1.0 | Core + Rules |
| 04_Omission_Addition.md | ✅ Complete | 506 | 1.0 | Specialized + Rules |
| 05_UOM_Standards.md | ✅ Complete | 378 | 1.0 | Specialized + Concepts |
| 06_Naming_Convention.md | ✅ Complete | 536 | 1.0 | Specialized + Rules |
| 07_Client_Conventions.md | ✅ Complete | 472 | 1.0 | Reference + Rules |
| 08_Checking_Workflow.md | ✅ Complete | 595 | 1.0 | Workflow + Rules |
| 09_Dimension_Group_Guide.md | ✅ Complete | 453 | 1.0 | Specialized + Rules |
| 10_Drawing_Organization.md | ✅ Complete | 424 | 1.0 | Specialized + Rules |
| glossary.md | ✅ Complete | 176 | 1.1 | Reference |
| README.md | ✅ Complete | - | 1.1 | Reference |

**Total**: 12 documents, ~5,100 lines of domain knowledge, 52 rule IDs

---

## Relationship to Other Documentation

### Platform Architecture

- **docs/00_Vision.md**: Strategic vision
- **docs/01_Principles.md**: Engineering principles
- **docs/02_System_Blueprint.md**: System architecture
- **docs/domain/** (this layer): Domain knowledge

Domain knowledge is consumed by the platform but does not define platform architecture.

### Capability Documentation

- **docs/planning/**: Capability roadmap and evaluation
- **docs/design/**: Implementation specifications
- **docs/domain/** (this layer): Domain specifications

Domain documents are referenced by capability documents but don't specify implementations.

### ADRs

- **docs/decisions/**: Architectural decisions
- **docs/domain/** (this layer): Domain standards

ADRs may reference domain rules but don't override domain authority hierarchy.

---

## Maintenance

### When to Update

Update domain documents when:
- Office practice changes
- Australian Standards update
- New patterns identified
- Client conventions documented
- Errors or ambiguities found

### How to Update

1. Identify affected document(s)
2. Follow established pattern
3. Update version and change history
4. Update cross-references if needed
5. Update glossary if new terms
6. Update this README if structure changes

### Review Schedule

- **Annual**: Full review of all documents
- **Per Project**: Review relevant documents at project start
- **Ad Hoc**: When issues identified

---

## Contact

**Document Owner**: Project Owner

**Questions**: Refer to specific document TODO sections

**Updates**: Follow maintenance procedures above

---

## Summary

The Domain Knowledge Layer provides formal, implementation-independent specifications of quantity surveying knowledge. These documents serve as the source of truth for office practice, validation rules, and quality standards.

This layer enables Jarvis to reason about BOQs without coupling domain knowledge to implementation details.

Welcome to the Domain Knowledge Layer.