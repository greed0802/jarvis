# Repository Knowledge Index

**Generated**: 2026-07-22
**Purpose**: Single entry point for all repository knowledge — architecture, engineering, capabilities, contracts, evidence, and governance.
**Part of**: Repository Foundation Freeze

---

## How to Use This Index

This is the master navigation document for the Jarvis repository. Start here for any question about the repository.

**Reading Paths:**

| You want to... | Start with... |
|---|---|
| Understand what Jarvis is | Architecture → Vision & Principles |
| Find the engineering rules AI agents must follow | Governance → AGENTS.md |
| Understand the architecture | Architecture → System Blueprint |
| Check what's implemented | Engineering → Implementation Status |
| Find all ADRs | Architecture → ADRs |
| Find frozen contracts | Contracts |
| Review completed investigations | Evidence → Engineering Questions |
| Check quality pipeline status | Quality → Verification Pipeline |
| Find where code lives | Repository Map → Source |
| Plan a new capability | Capabilities → Capability Roadmap |

---

## 1. Architecture

### Source of Truth Documents

| Document | Location | Purpose |
|---|---|---|
| Vision | docs/00_Vision.md | What Jarvis is and why it exists |
| Principles | docs/01_Principles.md | Engineering principles |
| System Blueprint | docs/02_System_Blueprint.md | Architecture layers |
| Core Ontology | docs/03_Core_Ontology_Relationships.md | Domain concepts and relationships |
| Platform Kernel | docs/04_Platform_Kernel.md | Control plane design |
| Data Flow | docs/05_Data_Flow.md | Information flow through the system |

### Engine & Framework Documentation

| Document | Location | Status |
|---|---|---|
| Context Engine | docs/06_Context_Engine.md | Speculative |
| Planner Engine | docs/07_Planner_Engine.md | Speculative |
| Workflow Engine | docs/08_Workflow_Engine.md | Speculative |
| AI Framework | docs/09_AI_Framework.md | Speculative |
| Memory Framework | docs/10_Memory_Framework.md | Speculative |
| Knowledge Framework | docs/11_Knowledge_Framework.md | Speculative |
| Resource Framework | docs/12_Resource_Framework.md | Speculative |
| Learning Framework | docs/13_Learning_Framework.md | Speculative |
| Validation Framework | docs/14_Validation_Framework.md | Speculative |
| Skill Framework | docs/15_Skill_Framework.md | Speculative |
| Plugin Framework | docs/16_Plugin_Framework.md | Speculative |
| API Framework | docs/17_API_Framework.md | Speculative |
| Storage Framework | docs/18_Storage_Framework.md | Speculative |
| Security Framework | docs/19_Security_Framework.md | Speculative |
| Event System | docs/20_Event_System.md | Speculative |
| Service Container | docs/21_Service_Container.md | Speculative |
| GUI Framework | docs/22_GUI_Framework.md | Speculative |
| Deployment Guide | docs/23_Deployment_Guide.md | Speculative |
| Development Guide | docs/24_Development_Guide.md | Speculative |
| Roadmap | docs/25_Roadmap.md | Speculative |
| Implementation Status | docs/26_Implementation_Status.md | Active |

**Note**: Documents 06-25 are speculative architecture — not implemented. The Implementation Status document (26) is the authoritative source for tracking what exists vs what is planned.

### ADR Registry

All 26 ADRs live in docs/decisions/. Key groupings:

| Category | ADRs | Summary |
|---|---|---|
| Core Ontology | 0001, 0002, 0003, 0004 | Project, Workspace, Resource concepts |
| Planning | 0005 | Deterministic Planner |
| Skills | 0006, 0009 | Skill architecture and collaboration |
| Knowledge | 0007 | Knowledge Promotion |
| Context | 0008, 0022 | Context definition and lifecycle |
| Human Interaction | 0010 | Human control |
| Repository | 0011, 0012 | Documentation and structure |
| Workflow | 0013, 0014, 0024 | Workflow ownership, determinism, execution |
| Results | 0015, 0016 | Result persistence and traceability |
| Platform Kernel | 0017, 0018, 0019 | Kernel philosophy, lifecycle, coordination |
| Runtime Architecture | 0020, 0021, 0023 | Engine vs Framework separation, Control/Data Plane, Capability Discovery |
| Observation | 0025 | Observation Runtime Architecture |

See: docs/decisions/README.md for full index with summaries.

### Architecture Diagrams

| Diagram | Location | Content |
|---|---|---|
| Control Loop | docs/diagrams/control_loop.md | Planner-Workflow-Validation-Skill loop |
| Engineering Review Process | docs/diagrams/engineering_review_process.md | EQ lifecycle |
| Engineering Spikes vs Production | docs/diagrams/engineering_spikes_vs_production_implementation.md | Spike/implementation distinction |

### Domain Knowledge

| Area | Location | Status |
|---|---|---|
| Domain vocabulary | docs/domain/ | 13 files — partial Project Owner verification |
| Ontology definitions | docs/ontology/core/ | 11 concept files |
| Observation model | docs/ontology/observation/ | 9 observation model files |
| Knowledge base summary | docs/knowledge/03_Domain_Knowledge.md | Compressed domain knowledge |

---

## 2. Engineering

### Governance

| Document | Location | Authority |
|---|---|---|
| **AGENTS.md** | Root | **Authoritative** — all governance rules |
| AI Agent Operating Manual | docs/engineering/AI_Agent_Operating_Manual.md | Supplemental — expanded explanation |
| Engineering Governance | docs/engineering/Engineering_Governance.md | Supplemental — overlaps with AGENTS.md |
| Engineering Authority | docs/engineering/Engineering_Authority.md | Supplemental |

### Quality Assurance

| Document | Location | Authority |
|---|---|---|
| Quality Constitution | AGENTS.md § Engineering Quality Assurance Constitution (lines 474-606) && `docs/engineering/Quality_Assurance_Constitution.md` (verbatim extract) | AGENTS.md |
| Verification Pipeline | docs/engineering/Engineering_Verification_Pipeline.md | Reference |
| Tool Registry | tools/quality/Tool_Registry.md | **Authoritative** for tools |

### Quality Tools

| Tool | File | Purpose |
|---|---|---|
| verify_all.py | tools/quality/verify_all.py | Orchestrator — runs all checks |
| verify_versions.py | tools/quality/verify_versions.py | Version consistency |
| verify_registry.py | tools/quality/verify_registry.py | Registry integrity |
| verify_contracts.py | tools/quality/verify_contracts.py | Contract presence/format |
| verify_imports.py | tools/quality/verify_imports.py | Import boundary enforcement |
| verify_tests.py | tools/quality/verify_tests.py | Structural test metrics |
| verify_documentation.py | tools/quality/verify_documentation.py | Documentation structure |

Run: `./.venv/bin/python tools/quality/verify_all.py`

### Engineering Questions

| EQ | Domain | Status | Location |
|---|---|---|---|
| EQ-0010 | BOQ Structural Intelligence | Frozen | docs/engineering/questions/EQ_0010_* |
| EQ-0011 | BOQ Semantic Intelligence | Frozen | docs/engineering/questions/EQ_0011_* |
| EQ-0012 | Evidence Contracts | Frozen | docs/engineering/questions/EQ_0012_* |
| EQ-0013 | Validation Engine | Frozen | docs/engineering/questions/EQ_0013_* |
| EQ-0014 | Parser Regression | Complete | docs/engineering/questions/EQ_0014_* |
| EQ-0015 | Structural Containment | Complete | docs/engineering/questions/EQ_0015_* |

### Spike Evidence (by EQ)

| EQ | Evidence Reports | Location |
|---|---|---|
| EQ-0010 | 5 spikes — structural intelligence | docs/engineering/evidence/EQ_0010_Spike1-5* |
| EQ-0011 | 5 spikes — semantic intelligence | docs/engineering/evidence/EQ_0011_Spike1-5* |
| EQ-0012 | 6 spikes — contracts | docs/engineering/evidence/EQ_0012_* |
| EQ-0013 | 4 spikes — validation | docs/engineering/evidence/EQ_0013_* |
| EQ-0014 | 2 spikes — regression | docs/engineering/evidence/EQ_0014_* |
| EQ-0015 | 4 spikes — containment | docs/engineering/evidence/EQ_0015_* |

### Engineering Debt Register

**Location**: docs/engineering/Engineering_Debt_Register.md

Current engineering debt with IDs, severity, freeze-blocking status, and planned resolution.

### Capability Matrices

| Matrix | Location |
|---|---|
| EQ-0010 Structural Capability | docs/engineering/capability_matrices/EQ_0010_* |
| EQ-0011 Semantic Capability | docs/engineering/capability_matrices/EQ_0011_* |
| EQ-0013 Validation Engine | docs/engineering/capability_matrices/EQ_0013_* |

### Capability Register

**Location**: docs/knowledge/07_Capabilities.md (compressed)

For road map, see: docs/25_Roadmap.md (speculative)

---

## 3. Contracts

### Frozen Public Contracts

| Contract | Version | File | Status |
|---|---|---|---|
| BOQ Intelligence Public Evidence | v1.0 | docs/contracts/BOQ_Intelligence_Public_Evidence_Contract_v1.0.md | Frozen |
| Validation Findings | v1.0 | docs/contracts/Validation_Findings_Contract_v1.0.md | Frozen |

### Contract Development Process

Reference: ADR_0012 Spike evidence (6 spikes documented in docs/engineering/evidence/EQ_0012_*)

---

## 4. Evidence

### Evidence Hierarchy (from AGENTS.md)

1. Accepted ADRs
2. Architecture Documents
3. Production Code
4. Engineering Questions
5. Spike Evidence
6. Approved Documentation
7. External References
8. General AI Knowledge

### Evidence Classification System

| Mark | Meaning |
|---|---|
| EB | Evidence-Backed |
| AGP | AI-Generated, Pending review |
| SP | Speculative (planned, not implemented) |
| OB | Obsolete |
| OV | Project Owner Verified |

### Evidence Repository

Spike tools: `tools/eq*_spike*.py`
Spike data: `data/reports/eq*_spike*_results.json`
Evidence reports: `docs/engineering/evidence/EQ_*_Spike*_Evidence_Report*.md`

---

## 5. Release Process

### Current Version
**0.0.1-alpha** (src/jarvis/version.py — canonical)

### Release Milestones

| Milestone | Date | Notes |
|---|---|---|
| v0.0.1-alpha.9 | Prior release | Release notes in archive/reports/ |
| M9 | Architecture Freeze | Complete |
| M10 | Maintenance Sprint | Complete |
| Foundation Freeze | 2026-07-22 | Current |

### Release Checklist

1. verify_all.py PASS
2. pytest PASS (150 passed, 8 skipped)
3. Documentation sync confirmed
4. Version consistency confirmed
5. Engineering Debt Register reviewed
6. Release notes created
7. Git tag applied
8. RELEASE_*.md committed

---

## 6. Repository Map

See: `docs/engineering/evidence/Repository_Map.md`

---

## 7. Archive

**Location**: archive/
**Archive Policy**: `archive/Archive_Policy.md`
**Inventory**: `archive/Archive_Inventory.md`

Archived items:
- Historical architecture sync reports
- Superseded release notes
- Historical milestone status reports

---

## 8. Knowledge Base (Compressed)

The `docs/knowledge/` directory contains compressed, LLM-friendly summaries:

| File | Content |
|---|---|
| 00_Knowledge_Index | Master reading guide |
| 01_Project_Overview | What Jarvis is |
| 02_Architecture_Summary | Architecture overview |
| 03_Domain_Knowledge | QS/Civil domain |
| 04_Engineering_Governance | Governance summary |
| 05_Engineering_Questions | EQ + spike summaries |
| 06_Contracts | Contract summaries |
| 07_Capabilities | Capability register |
| 08_Consumers | Consumer patterns |
| 09_Methodology | Engineering playbook |
| 10_Implementation_Status | Code vs. docs gap analysis |
| 11_Open_Questions | Deferred EQs and gaps |
| Appendices/ | Detailed registries and inventories |

---

## 8. Planning Documents

| Document | Location |
|---|---|
| Capability Roadmap | docs/planning/ |
| Consumer Specifications | docs/planning/ |
| Deployment Planning | docs/planning/ |
| Design Specifications | docs/design/ |

---

## 9. Historical Archive

| Artifact | Location | Notes |
|---|---|---|
| Architecture sync review | archive/reports/ARCHITECTURE_SYNC_REVIEW.md | 14 issues found |
| Architecture sync summary | archive/reports/ARCHITECTURE_SYNC_SUMMARY.md | Executive summary |
| M7-era status | archive/reports/ARCHITECTURE_STATUS.md | Frozen M7 |
| v0.0.1-alpha.9 release | archive/reports/RELEASE_v0.0.1-alpha.9.md | Superceded |

---

## 10. Quick Reference

The report includes a table of all repository version artifacts and their values for 2026-07-22.

| Item | Value |
|---|---|
| Software Version | 0.0.1-alpha |
| ADR Count | 26 (all Accepted) |
| Frozen EQs | 6 |
| Frozen Contracts | 2 |
| Quality Tools | 7 (6 + 1 orchestrator) |
| Pytest | 150 passed, 8 skipped (all PASS) |
| verify_all.py | PASS |
| Production Lines | ~1,700 |
| Documentation Files | ~140 |
| Evidence Reports | 30+ |
| Spike Tools | 30+ |
| Knowledge Base Docs | 16 |

---

**Generated**: 2026-07-22 | **Part of**: Repository Foundation Freeze