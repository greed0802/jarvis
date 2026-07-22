# Appendix A: Document Inventory

> **Purpose**: Master inventory of every document in the Jarvis repository. Records path, line count, purpose, verification status, and redundancy flags.
> **Generated**: 2026-07-15
> **Part of**: Jarvis Knowledge Consolidation

---

## Inventory Format

| Field | Description |
|-------|-------------|
| **Path** | Relative path from repository root |
| **Lines** | Approximate line count |
| **Purpose** | Single-sentence summary |
| **Verification** | See classification key below |
| **Redundancy** | Flag if duplicate/obsolete/superseded |

## Verification Classification

| Code | Meaning |
|------|---------|
| `VP` | Verified by Project Owner |
| `EB` | Evidence-backed (production code/tests confirm) |
| `IB` | Implementation-backed (code exists matching doc) |
| `AGV` | AI-generated, Project Owner verified |
| `AGP` | AI-generated, pending Project Owner verification |
| `SP` | Speculative (future architecture, not yet built) |
| `UN` | Unknown authorship |
| `OBS` | Obsolete — superseded by later document |
| `DUP` | Duplicate — same content elsewhere |

---

## Section 1: Root-Level Documents

| Path | Lines | Purpose | Verification | Redundancy |
|------|-------|---------|--------------|------------|
| `AGENTS.md` | ~200 | Mandatory engineering rules for all AI coding agents | `VP` | — |
| `app.py` | 27 | Bootstrap entry point for Jarvis runtime | `IB` | — |
| `ARCHITECTURE_STATUS.md` | ~200 | Current architecture sync status report | `EB` | — |
| `ARCHITECTURE_SYNC_REVIEW.md` | ~300 | Detailed architecture sync findings (6 issues) | `EB` | — |
| `ARCHITECTURE_SYNC_SUMMARY.md` | ~200 | Summary of architecture sync pass 1 | `EB` | — |
| `LICENSE` | — | License file | `VP` | — |
| `pytest.ini` | — | Pytest configuration | `IB` | — |
| `README.md` | ~200 | Project README — overview and quick start | `VP` | — |
| `RELEASE_v0.0.1-alpha.9.md` | ~200 | Release notes for v0.0.1-alpha.9 | `EB` | — |
| `requirements.txt` | ~10 | Python dependencies | `IB` | — |

## Section 2: Architecture Docs (`docs/00-26`)

| Path | Lines | Purpose | Verification | Redundancy |
|------|-------|---------|--------------|------------|
| `docs/00_Vision.md` | 289 | Top-level vision, mission, core values, non-goals | `VP` | — |
| `docs/01_Principles.md` | 351 | Permanent technology-independent design principles | `VP` | — |
| `docs/02_System_Blueprint.md` | ~500 | Complete system architecture blueprint | `AGP` | — |
| `docs/03_Core_Ontology_Relationships.md` | ~400 | Core ontology objects and relationships | `AGP` | — |
| `docs/04_Platform_Kernel.md` | ~300 | Kernel architecture specification | `AGP/IB` | — |
| `docs/05_Data_Flow.md` | 330 | Data flow lifecycle and ownership | `AGP` | — |
| `docs/06_Context_Engine.md` | 282 | Context Engine specification | `AGP/SP` | — |
| `docs/07_Planner_Engine.md` | ~300 | Planner Engine specification | `AGP/SP` | — |
| `docs/08_Workflow_Engine.md` | ~300 | Workflow Engine specification | `AGP/SP` | — |
| `docs/09_AI_Framework.md` | ~200 | AI integration framework | `AGP/SP` | — |
| `docs/10_Memory_Framework.md` | ~200 | Memory framework specification | `AGP/SP` | — |
| `docs/11_Knowledge_Framework.md` | ~200 | Knowledge framework specification | `AGP/SP` | — |
| `docs/12_Resource_Framework.md` | ~200 | Resource framework specification | `AGP/SP` | — |
| `docs/13_Learning_Framework.md` | ~200 | Learning framework specification | `AGP/SP` | — |
| `docs/14_Validation_Framework.md` | ~200 | Validation framework specification | `AGP/IB` | Partially implemented |
| `docs/15_Skill_Framework.md` | ~200 | Skill framework specification | `AGP/SP` | — |
| `docs/16_Plugin_Framework.md` | ~200 | Plugin framework specification | `AGP/SP` | — |
| `docs/17_API_Framework.md` | ~200 | API framework specification | `AGP/SP` | — |
| `docs/18_Storage_Framework.md` | ~200 | Storage framework specification | `AGP/SP` | — |
| `docs/19_Security_Framework.md` | ~200 | Security framework specification | `AGP/SP` | — |
| `docs/20_Event_System.md` | ~200 | Event system specification | `AGP/SP` | — |
| `docs/21_Service_Container.md` | ~200 | Service container specification | `AGP/SP` | — |
| `docs/22_GUI_Framework.md` | ~200 | GUI framework specification | `AGP/SP` | — |
| `docs/23_Deployment_Guide.md` | ~200 | Deployment guide | `AGP/SP` | — |
| `docs/24_Development_Guide.md` | ~200 | Development guide | `AGP/SP` | — |
| `docs/25_Roadmap.md` | ~200 | Development roadmap | `AGP` | — |
| `docs/26_Implementation_Status.md` | ~200 | Current implementation status | `EB` | — |

## Section 3: Domain Documents (`docs/domain/`)

| Path | Lines | Purpose | Verification | Redundancy |
|------|-------|---------|--------------|------------|
| `docs/domain/README.md` | ~50 | Domain layer overview and index | `AGP` | — |
| `docs/domain/glossary.md` | ~100 | Domain terminology glossary | `AGP` | — |
| `docs/domain/01_QS_Office_Standards.md` | ~200 | QS office standards and conventions | `AGP` | — |
| `docs/domain/02_BOQ_Structure.md` | ~300 | BOQ structure: rows, sections, hierarchy | `AGP` | Frozen |
| `docs/domain/03_Trade_Schedule.md` | ~200 | Trade schedule definitions | `AGP` | — |
| `docs/domain/04_Omission_Addition.md` | ~200 | Omission/Addition sign conventions | `AGP` | — |
| `docs/domain/05_UOM_Standards.md` | ~200 | Unit of Measure standards | `AGP` | — |
| `docs/domain/06_Naming_Convention.md` | ~200 | Naming conventions | `AGP` | — |
| `docs/domain/07_Client_Conventions.md` | ~200 | Client-specific conventions | `AGP` | — |
| `docs/domain/08_Checking_Workflow.md` | ~200 | BOQ checking workflow | `AGP` | — |
| `docs/domain/09_Dimension_Group_Guide.md` | ~200 | Dimension group guide | `AGP` | — |
| `docs/domain/10_Drawing_Organization.md` | ~200 | Drawing organization standards | `AGP` | — |
| `docs/domain/DOMAIN_LAYER_V1_1_REVIEW.md` | ~300 | Domain layer v1.1 review findings | `EB` | — |

## Section 4: Engineering Questions (`docs/engineering/questions/`)

| Path | Lines | Purpose | Verification | Redundancy |
|------|-------|---------|--------------|------------|
| `docs/engineering/questions/EQ_0010_Deterministic_BOQ_Structural_Intelligence.md` | 541 | EQ-0010: Deterministic structural intelligence from BOQRow | `EB` | FROZEN, Gate 3 |
| `docs/engineering/questions/EQ_0011_BOQ_Semantic_Intelligence_Boundary.md` | ~400 | EQ-0011: Semantic intelligence boundary | `EB` | FROZEN, Gate 3 |
| `docs/engineering/questions/EQ_0012_BOQ_Intelligence_Public_Evidence_Contract.md` | ~400 | EQ-0012: Public evidence contract for BOQ Intelligence | `EB` | FROZEN, Gate 3 |
| `docs/engineering/questions/EQ_0013_Validation_Engine.md` | 442 | EQ-0013: Validation Engine architecture | `EB` | FROZEN, Gate 3 |

## Section 5: Spike Evidence Reports (`docs/engineering/evidence/`)

### EQ-0010 Spikes (5 reports)
| Path | Lines | Purpose | Verification | Redundancy |
|------|-------|---------|--------------|------------|
| `EQ_0010_Spike1_Evidence_Report_Direct_Field_Observation.md` | ~300 | Direct field observation of BOQRow | `EB` | Complete |
| `EQ_0010_Spike2_Evidence_Report_UOM_Pattern_Analysis.md` | ~300 | UOM pattern analysis | `EB` | Complete |
| `EQ_0010_Spike3_Evidence_Report_Row_Sequence_Analysis.md` | ~300 | Row sequence analysis | `EB` | Complete |
| `EQ_0010_Spike4_Evidence_Report_Hierarchy_Reconstruction.md` | ~300 | Hierarchy reconstruction | `EB` | Complete |
| `EQ_0010_Spike5_Evidence_Report_Domain_Reconciliation.md` | ~300 | Domain knowledge reconciliation | `EB` | Complete |

### EQ-0011 Spikes (5 reports)
| Path | Lines | Purpose | Verification | Redundancy |
|------|-------|---------|--------------|------------|
| `EQ_0011_Spike1_Evidence_Report_Domain_Vocabulary_Discovery.md` | ~300 | Domain vocabulary discovery | `EB` | Complete |
| `EQ_0011_Spike2_Evidence_Report_Evidence_vs_Assessment_Decomposition.md` | ~300 | Evidence vs assessment decomposition | `EB` | Complete |
| `EQ_0011_Spike3_Evidence_Report_Boundary_Validation.md` | ~300 | Boundary validation | `EB` | Complete |
| `EQ_0011_Spike4_Evidence_Report_Engineering_Boundary_Synthesis.md` | ~300 | Engineering boundary synthesis | `EB` | Complete |
| `EQ_0011_Spike5_Evidence_Report_Semantic_Capability_Disposition.md` | ~300 | Semantic capability disposition | `EB` | Complete |

### EQ-0012 Spikes (6 reports)
| Path | Lines | Purpose | Verification | Redundancy |
|------|-------|---------|--------------|------------|
| `EQ_0012_Spike1_Evidence_Report_Current_Evidence_Inventory.md` | 355 | Current evidence inventory | `EB` | Complete |
| `EQ_0012_Spike2_Evidence_Report_Contract_Versioning_Policy.md` | 285 | Contract versioning policy | `EB` | Complete |
| `EQ_0012_Spike3_Evidence_Report_Contract_Invariants.md` | ~300 | Contract invariants | `EB` | Complete |
| `EQ_0012_Spike4_Evidence_Report_Consumer_Access_Patterns.md` | ~300 | Consumer access patterns | `EB` | Complete |
| `EQ_0012_Spike5_Evidence_Report_Contract_Documentation_Standards.md` | ~300 | Contract documentation standards | `EB` | Complete |
| `EQ_0012_Spike6_Verification_Findings.md` | ~400 | Contract verification findings | `EB` | Complete |

### EQ-0013 Spikes (4 reports + freeze)
| Path | Lines | Purpose | Verification | Redundancy |
|------|-------|---------|--------------|------------|
| `EQ_0013_Spike1_Evidence_Report_Validation_Capability_Discovery.md` | ~300 | Validation capability discovery | `EB` | Complete |
| `EQ_0013_Spike2_Evidence_Report_Validation_Rule_Taxonomy.md` | ~300 | Validation rule taxonomy | `EB` | Complete |
| `EQ_0013_Spike3_Evidence_Report_Engine_Scope_and_Responsibilities.md` | ~300 | Engine scope and responsibilities | `EB` | Complete |
| `EQ_0013_Spike4_Evidence_Report_Validation_Engine_Implementation.md` | ~300 | Engine implementation evidence | `EB` | Complete |
| `EQ_0013_Final_Freeze_Report.md` | ~400 | Final freeze report — EQ-0013 closure | `EB` | Complete |

### Capability Matrices
| Path | Lines | Purpose | Verification | Redundancy |
|------|-------|---------|--------------|------------|
| `docs/engineering/capability_matrices/EQ_0010_Structural_Capability_Matrix.md` | 125 | 18 structural capabilities classified | `EB` | Frozen |
| `docs/engineering/capability_matrices/EQ_0011_Semantic_Capability_Matrix.md` | ~150 | 17 semantic capabilities classified | `EB` | Frozen |

## Section 6: ADRs (`docs/decisions/`)

| Path | # | Title | Status | Verification |
|------|---|-------|--------|--------------|
| `ADR_0001_Core_Ontology.md` | 1 | Core Ontology | Accepted | `VP` |
| `ADR_0002_Workspace_vs_Project.md` | 2 | Workspace vs Project | Accepted | `VP` |
| `ADR_0003_Resource_Identity.md` | 3 | Resource Identity | Accepted | `VP` |
| `ADR_0004_Resource_Versioning.md` | 4 | Resource Versioning | Accepted | `VP` |
| `ADR_0005_Deterministic_Planner.md` | 5 | Deterministic Planner | Accepted | `VP` |
| `ADR_0006_Skill_Collaboration.md` | 6 | Skill Collaboration | Accepted | `VP` |
| `ADR_0007_Knowledge_Promotion.md` | 7 | Knowledge Promotion | Accepted | `VP` |
| `ADR_0008_Context.md` | 8 | Context — dynamic, references-not-copies | Accepted | `VP` |
| `ADR_0009_Skill_Architecture.md` | 9 | Skill Architecture — Planner decides WHAT, Skills do work | Accepted | `VP` |
| `ADR_0010_Human_Control.md` | 10 | Human Control — Jarvis assists, never autonomously decides | Accepted | `VP` |
| `ADR_0011_Documentation_Repository.md` | 11 | Documentation Repository | Accepted | `VP` |
| `ADR_0012_Repository_Structure.md` | 12 | Repository Structure | Accepted | `VP` |
| `ADR_0013_Workflow_Ownership.md` | 13 | Workflow Ownership | Accepted | `VP` |
| `ADR_0014_Workflow_Determinism.md` | 14 | Workflow Determinism | Accepted | `VP` |
| `ADR_0015_Result_Persistence.md` | 15 | Result Persistence | Accepted | `VP` |
| `ADR_0016_Result_Traceability.md` | 16 | Result Traceability | Accepted | `VP` |
| `ADR_0017_Platform_Kernel_Philosophy.md` | 17 | Platform Kernel Philosophy | Accepted | `VP` |
| `ADR_0018_Platform_Runtime_Lifecycle.md` | 18 | Platform Runtime Lifecycle | Accepted | `VP` |
| `ADR_0019_Consumer_Independence.md` | 19 | Consumer Independence | Accepted | `VP` |
| `ADR_0020_Engineering_Question_Format.md` | 20 | Engineering Question Format | Accepted | `VP` |
| `ADR_0021_Capability_Engineering_Pattern.md` | 21 | Capability Engineering Pattern | Accepted | `VP` |
| `ADR_0022_Validation_Engine_Architecture.md` | 22 | Validation Engine Architecture | Accepted | `VP` |
| `ADR_0023_Evidence_Contract_Engineering.md` | 23 | Evidence Contract Engineering | Accepted | `VP` |
| `ADR_0024_Workflow_Execution_Model.md` | 24 | Workflow Execution Model | Accepted | `VP` |
| `ADR_0025_Observation_vs_Assessment.md` | 25 | Observation vs Assessment | Accepted | `VP` |
| `ADR_0026_BOQ_Intelligence_Evidence_Contract.md` | 26 | BOQ Intelligence Evidence Contract | Accepted | `VP` |

## Section 7: Contracts (`docs/contracts/`)

| Path | Lines | Purpose | Verification | Redundancy |
|------|-------|---------|--------------|------------|
| `BOQ_Intelligence_Public_Evidence_Contract_v1.0.md` | ~500 | BOQ Intelligence public evidence contract v1.0 | `EB` | Frozen |
| `Validation_Findings_Contract_v1.0.md` | ~400 | Validation Findings contract v1.0 | `EB` | Frozen |

## Section 8: Planning Documents (`docs/planning/`)

| Path | Lines | Purpose | Verification | Redundancy |
|------|-------|---------|--------------|------------|
| `Capability_Register.md` | ~110 | Living capability state register | `EB` | Active |
| `Capability_Roadmap.md` | ~200 | Capability lifecycle governance | `AGP` | — |
| `Capability_Discovery_001.md` | ~200 | First capability discovery (6 candidates) | `EB` | Complete |
| `Capability_Evaluation_001.md` | ~200 | BOQ Intelligence evaluation | `EB` | Complete |
| `M8_Repository_Assessment_and_Consumer_Architecture_Planning.md` | 1618 | M8 repository assessment & consumer planning | `EB` | GO recommendation |

## Section 9: Reference Documents (`docs/reference/`)

| Path | Lines | Purpose | Verification | Redundancy |
|------|-------|---------|--------------|------------|
| `BOQ_Row_Analysis.md` | 128 | Spike #1 BOQ row classification report | `EB` | — |
| `Engineering_Fixtures.md` | 214 | Engineering fixture management policy | `EB` | — |
| `Engineering_Questions.md` | 255 | Master EQ registry (EQ-0001 through EQ-0013) | `EB` | — |
| `Knowledge_Base_Architecture.md` | ~200 | Knowledge base architecture | `AGP` | — |
| `Antora_Playbook_Implementation.md` | ~300 | Antora documentation toolchain | `AGP` | Implemented? |
| `Antora_Content_Structure.md` | ~200 | Antora content organization | `AGP` | — |
| `Antora_Integration_Guide.md` | ~200 | Antora integration instructions | `AGP` | — |
| `Default_Configurations.md` | ~100 | Default configuration reference | `AGP` | — |
| `Type_Safety_Reference.md` | ~100 | Type safety conventions | `AGP` | — |

## Section 10: Other Documentation

| Path | Lines | Purpose | Verification | Redundancy |
|------|-------|---------|--------------|------------|
| `docs/engineering/Engineering_Governance.md` | ~200 | Engineering governance rules | `AGP` | — |
| `docs/engineering/README.md` | ~50 | Engineering docs overview | `AGP` | — |
| `docs/engineering/AI_Agent_Operating_Manual.md` | 406 | AI agent operating procedures | `VP` | — |
| `docs/ontology/README.md` | ~50 | Ontology overview | `AGP` | — |
| `docs/ontology/core/capability.md` | 319 | Capability ontology definition | `AGP` | — |
| `docs/ontology/core/context.md` | ~200 | Context ontology definition | `AGP` | — |
| `docs/ontology/core/intent.md` | ~200 | Intent ontology definition | `AGP` | — |
| `docs/ontology/core/knowledge.md` | ~200 | Knowledge ontology definition | `AGP` | — |
| `docs/ontology/core/memory.md` | ~200 | Memory ontology definition | `AGP` | — |
| `docs/ontology/core/planner.md` | ~200 | Planner ontology definition | `AGP` | — |
| `docs/ontology/core/project.md` | ~200 | Project ontology definition | `AGP` | — |
| `docs/ontology/core/resource.md` | ~200 | Resource ontology definition | `AGP` | — |
| `docs/ontology/core/result.md` | ~200 | Result ontology definition | `AGP` | — |
| `docs/ontology/core/skill.md` | ~200 | Skill ontology definition | `AGP` | — |
| `docs/ontology/core/task.md` | ~200 | Task ontology definition | `AGP` | — |
| `docs/ontology/core/validation.md` | ~200 | Validation ontology definition | `AGP` | — |
| `docs/ontology/core/workflow.md` | ~200 | Workflow ontology definition | `AGP` | — |
| `docs/ontology/core/workspace.md` | ~200 | Workspace ontology definition | `AGP` | — |
| `docs/design/M5_First_CostX_Parser_Specification.md` | ~300 | CostX parser specification | `EB` | Complete |
| `docs/design/M6_Observation_Model.md` | ~300 | Observation model design (REJECTED by ADR-0025) | `EB` | **OBS** — Replaced by ADR-0025 |
| `docs/design/Repository_Knowledge_Preservation_Strategy.md` | ~200 | Knowledge preservation strategy | `AGP` | — |
| `docs/implementation/README.md` | ~50 | Implementation docs overview | `AGP` | — |
| `docs/templates/` | — | Template directory | `AGP` | — |
| `docs/retrospectives/EQ_0012_BOQ_Intelligence_Public_Evidence_Contract.md` | ~300 | EQ-0012 retrospective | `EB` | — |
| `docs/LANGUAGE.md` | ~100 | Language directives for AI agents | `AGP` | **OBS**? — Superseded by AGENTS.md |
| `docs/JARVIS_SPECIFICATION.md` | ~1371 | Comprehensive Jarvis specification | `AGP` | **OBS**? — Superseded by architecture docs |
| `docs/AI_COLLABORATION.md` | ~200 | AI collaboration guidelines | `AGP` | — |
| `docs/CONTRIBUTING.md` | ~200 | Contribution guidelines | `AGP` | — |

## Section 11: Source Code (`src/jarvis/`)

| Path | Lines | Purpose | Verification | Status |
|------|-------|---------|--------------|--------|
| `src/jarvis/__init__.py` | ~5 | Package init | `IB` | Implemented |
| `src/jarvis/version.py` | 2 | Version string | `IB` | Implemented |
| `src/jarvis/application/application.py` | 126 | Composition root — creates Kernel, wires runtime | `IB` | Implemented |
| `src/jarvis/configuration/configuration.py` | 28 | Frozen Configuration dataclass | `IB` | Implemented |
| `src/jarvis/contracts/lifecycle.py` | 48 | LifecycleAware Protocol + LifecycleState enum | `IB` | Implemented |
| `src/jarvis/core/jarvis/kernel.py` | 201 | Kernel — registration, lifecycle orchestration | `IB` | Implemented |
| `src/jarvis/services/logging_service.py` | ~100 | LoggingService implementation | `IB` | Implemented |
| `src/jarvis/domain/boq.py` | ~300 | BOQ domain types (BOQRow, BOQSheet, etc.) | `IB` | Implemented |
| `src/jarvis/domain/capability.py` | ~50 | Capability domain type | `IB` | Implemented |
| `src/jarvis/domain/context.py` | ~50 | Context domain type | `IB` | Implemented |
| `src/jarvis/domain/intent.py` | ~50 | Intent domain type | `IB` | Implemented |
| `src/jarvis/domain/knowledge.py` | ~50 | Knowledge domain type | `IB` | Implemented |
| `src/jarvis/domain/memory.py` | ~50 | Memory domain type | `IB` | Implemented |
| `src/jarvis/domain/planner.py` | ~50 | Planner domain type | `IB` | Implemented |
| `src/jarvis/domain/project.py` | ~50 | Project domain type | `IB` | Implemented |
| `src/jarvis/domain/resource.py` | ~50 | Resource domain type | `IB` | Implemented |
| `src/jarvis/domain/result.py` | ~50 | Result domain type | `IB` | Implemented |
| `src/jarvis/domain/skill.py` | ~50 | Skill domain type | `IB` | Implemented |
| `src/jarvis/domain/workflow.py` | ~50 | Workflow domain type | `IB` | Implemented |
| `src/jarvis/domain/workspace.py` | ~50 | Workspace domain type | `IB` | Implemented |
| `src/jarvis/engines/validation/engine.py` | ~200 | ValidationEngine — finding evaluation | `IB` | Implemented |
| `src/jarvis/engines/validation/__init__.py` | ~5 | Validation engine package | `IB` | Implemented |

### Empty Engine Directories (Documented but NOT Implemented)
| Path | Status |
|------|--------|
| `src/jarvis/engines/builder/` | Empty — not implemented |
| `src/jarvis/engines/costing/` | Empty — not implemented |
| `src/jarvis/engines/descriptions/` | Empty — not implemented |
| `src/jarvis/engines/formatter/` | Empty — not implemented |
| `src/jarvis/engines/formula/` | Empty — not implemented |
| `src/jarvis/engines/qa/` | Empty — not implemented |
| `src/jarvis/core/context/` | Empty — not implemented |
| `src/jarvis/core/learning/` | Empty — not implemented |
| `src/jarvis/core/project/` | Empty — not implemented |
| `src/jarvis/core/session/` | Empty — not implemented |
| `src/jarvis/core/state/` | Empty — not implemented |
| `src/jarvis/core/task/` | Empty — not implemented |

## Section 12: Empty Directories (Structure Only)

| Path | Notes |
|------|-------|
| `scripts/` | Empty — no scripts |
| `workflows/builtin/` | Empty |
| `workflows/organization/` | Empty |
| `workflows/templates/` | Empty |
| `workflows/user/` | Empty |
| `third_party/licenses/` | Empty |
| `third_party/plugins/` | Empty |
| `third_party/skills/` | Empty |
| `third_party/templates/` | Empty |
| `docs/api/` | Empty |
| `docs/architecture/` | Empty |
| `docs/diagrams/` | Empty |
| `data/backups/` | Empty |
| `data/cache/` | Empty |
| `data/embeddings/` | Empty |
| `data/exports/` | Empty |
| `data/knowledge/` | Empty |
| `data/logs/` | Empty |
| `data/projects/` | Empty |
| `data/templates/` | Empty |

---

## Summary Statistics

| Category | Count | Total Lines (est.) |
|----------|-------|---------------------|
| Root docs | 10 | ~1,500 |
| Architecture docs (00-26) | 27 | ~7,000 |
| Domain docs | 13 | ~2,500 |
| Engineering Questions | 4 | ~1,800 |
| Spike evidence reports | 20 | ~6,000 |
| ADRs | 26 | ~5,000 |
| Contracts | 2 | ~900 |
| Planning docs | 5 | ~2,300 |
| Reference docs | 9 | ~1,700 |
| Ontology docs | 14 | ~3,000 |
| Other docs | 10 | ~3,500 |
| **Total docs** | **~140** | **~35,200 lines** |

**Note**: These are approximate counts. Exact verification requires tool-based line counting.