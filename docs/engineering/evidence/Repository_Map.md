# Repository Map

**Generated**: 2026-07-22
**Purpose**: Visual hierarchy of the Jarvis repository — source, tests, contracts, evidence, quality, knowledge, engineering, planning, and archive.
**Part of**: Repository Foundation Freeze

---

## Repository Structure

```
Jarvis/
│
├── src/jarvis/                          ← Production Code
│   ├── __init__.py
│   ├── version.py                       ← Canonical version (0.0.1-alpha)
│   ├── application/                     ← Composition Root
│   │   ├── application.py
│   ├── configuration/                   ← Configuration subsystem
│   │   ├── configuration.py
│   ├── contracts/                       ← Contract definitions
│   │   ├── lifecycle.py
│   ├── core/
│   │   ├── context/                     [empty — planned]
│   │   ├── jarvis/                      ← Kernel
│   │   │   ├── kernel.py
│   │   ├── learning/                    [empty — planned]
│   │   ├── project/                     [empty — planned]
│   │   ├── session/                     [empty — planned]
│   │   ├── state/                       [empty — planned]
│   │   ├── task/                        [empty — planned]
│   ├── domain/                          # Domain models
│   │   ├── capability.py
│   │   ├── context.py
│   │   ├── intent.py
│   │   ├── knowledge.py
│   │   ├── memory.py
│   │   ├── planner.py
│   │   ├── project.py
│   │   ├── resource.py
│   │   ├── result.py
│   │   ├── skill.py
│   │   ├── workflow.py
│   │   ├── workspace.py
│   ├── engines/
│   │   ├── builder/                     [empty — planned]
│   │   ├── costing/                     [empty — planned]
│   │   ├── descriptions/                [empty — planned]
│   │   ├── formatter/                   [empty — planned]
│   │   ├── formula/                     [empty — planned]
│   │   ├── qa/                          [empty — planned]
│   │   ├── validation/                  ← Validation Engine (implemented)
│   │       ├── engine.py
│   │       ├── data/rule_registry.json
│   ├── integrations/                    [empty — planned]
│   ├── intelligence/
│   │   ├── ai/                          [empty — planned]
│   │   ├── context/                     [empty — planned]
│   │   ├── memory/                      [empty — planned]
│   │   ├── parser/                      ← BOQ Parser (implemented)
│   │   ├── planner/                     [empty — planned]
│   │   ├── router/                      [empty — planned]
│   ├── interface/
│   │   ├── api/                         [empty — planned]
│   │   ├── cli/                         [empty — planned]
│   │   ├── gui/                         [empty — planned]
│   ├── knowledge/                       [empty — planned]
│   ├── parsers/
│   │   ├── __init__.py
│   │   ├── observation.py
│   │   ├── costx/
│   │   │   ├── boq_extraction.py
│   │   │   ├── boq_intelligence.py
│   │   │   ├── loader.py
│   │   │   ├── workbook_parser.py
│   ├── platform/                        [empty — planned]
│   ├── plugins/                         [empty — planned]
│   ├── resources/                       [empty — planned]
│   ├── security/                        [empty — planned]
│   ├── services/
│   │   ├── logging_service.py
│   ├── skills/                          [empty — planned]
│   ├── workflows/                       [empty — planned]
│
├── tests/                              # Test Suite
│   ├── __init__.py
│   ├── test_lifecycle.py
│   ├── fixtures/
│   │   ├── costx/                       ← BOQ test fixtures (.xlsx files)
│   ├── parser/
│   │   ├── test_boq_extraction.py
│   │   ├── test_boq_intelligence.py
│   │   ├── test_observation_models.py
│   │   ├── test_workbook_observe_historical.py
│   │   ├── test_workbook_parser.py
│   │   ├── test_workbook_validation.py
│   ├── reference/
│   │   ├── eq0007_evidence.py
│   ├── validation/
│   │   ├── test_engine.py
│
├── tools/                              # Engineering Tools
│   ├── quality/                         ← Quality Verification Pipeline
│   │   ├── verify_all.py                # Orchestrator
│   │   ├── verify_versions.py           # Version consistency
│   │   ├── verify_registry.py            # Registry integrity
│   │   ├── verify_contracts.py           # Contract checks
│   │   ├── verify_imports.py             # Import boundary
│   │   ├── verify_tests.py               # Test metrics
│   │   ├── verify_documentation.py       # Doc structure
│   │   ├── Tool_Registry.md              # Tool register
│   ├── manifest.json                     # Verifiable tool manifest
│   ├── eq*_spike*.py                     # Spike investigation tools
│   ├── generate_adr_index.py             # ADR index generator
│   ├── generate_docs.py                  # Doc generator
│   ├── register_fixture.py               # Fixture registration
│   ├── build_docs.py                     # Doc builder
│   ├── boq_row_analysis.py              # BOQ analysis utility
│   ├── workbook_inspector.py            # Workbook inspector
│   ├── context_discovery_spike.py       # Context discovery
│   ├── registry_validator.py            # Registry validator
│
├── data/                               # Runtime Data
│   ├── backups/                        [empty]
│   ├── cache/                          [empty]
│   ├── embeddings/                     [empty]
│   ├── exports/                        [empty]
│   ├── knowledge/                      [empty]
│   ├── logs/                           [empty]
│   ├── projects/                       [empty]
│   ├── reports/                        ← Spike evidence data
│   │   ├── eq*_spike*_results.json
│   ├── templates/                      [empty]
│
├── configs/                            [empty — planned configuration]
├── workflows/                          [empty — planned workflows]
├── third_party/                        [empty — planned third-party]
├── scripts/                            [empty — planned scripts]
│
├── archive/                            ← Historical Archive
│   ├── reports/                        ← Historical reports
│   │   ├── ARCHITECTURE_STATUS.md
│   │   ├── ARCHITECTURE_SYNC_REVIEW.md
│   │   ├── ARCHITECTURE_SYNC_SUMMARY.md
│   │   ├── RELEASE_v0.0.1-alpha.9.md
│   ├── Archive_Policy.md
│   ├── Archive_Inventory.md
│   ├── docs/                           [reserved for future doc archives]
│   ├── planning/                       [reserved for future planning archives]
│   ├── prompts/                        [reserved for future prompt archives]
│   ├── temporary/                      [reserved for future temporary items]
│
├── docs/                               # Documentation
│   ├── 00_Vision.md                    # Source of truth
│   ├── 01_Principles.md                # Source of truth
│   ├── 02_System_Blueprint.md          # Source of truth
│   ├── 03_Core_Ontology_Relationships.md  # Source of truth
│   ├── 04_Platform_Kernel.md           # Source of truth
│   ├── 05_Data_Flow.md                 # Source of truth
│   ├── 06-25_*.md                      # Speculative engine/framework docs
│   ├── 26_Implementation_Status.md     # Active status tracker
│   │
│   ├── decisions/                      ← 26 ADRs (all Accepted)
│   │   ├── ADR_0001 through ADR_0025
│   │   ├── README.md (ADR index)
│   │   ├── TEMPLATE.md
│   │
│   ├── contracts/                      ← Frozen public contracts
│   │   ├── BOQ_Intelligence_Public_Evidence_Contract_v1.0.md
│   │   ├── Validation_Findings_Contract_v1.0.md
│   │
│   ├── engineering/                    ← Engineering documentation
│   │   ├── AI_Agent_Operating_Manual.md
│   │   ├── Engineering_Authority.md
│   │   ├── Engineering_Debt_Register.md
│   │   ├── Engineering_Governance.md
│   │   ├── Engineering_Verification_Pipeline.md
│   │   ├── Quality_Assurance_Constitution.md
│   │   ├── Repository_Drift_Report.md
│   │   ├── README.md
│   │   ├── capability_matrices/        # EQ capability matrices (3)
│   │   ├── evidence/                    # EQ evidence reports (30+)
│   │   │   ├── EQ_0010_Spike1-5_*
│   │   │   ├── EQ_0011_Spike1-5_*
│   │   │   ├── EQ_0012_Spike1-6_*
│   │   │   ├── EQ_0013_Spike1-4_*
│   │   │   ├── EQ_0014_Spike1-2_*
│   │   │   ├── EQ_0015_Spike1-4_*
│   │   │   ├── M9_Freeze_Report.md
│   │   │   ├── M10_Maintenance_Report.md
│   │   │   ├── Repository_Foundation_Freeze_Report.md
│   │   │   ├── Repository_Knowledge_Index.md
│   │   │   ├── Repository_Map.md
│   │   ├── questions/                   # EQ definitions (6)
│   │
│   ├── knowledge/                       ← Compressed Knowledge Base
│   │   ├── 00_Knowledge_Index.md
│   │   ├── 01-11_*.md                   # Topic summaries
│   │   ├── Appendices/                  # Detailed registries
│   │
│   ├── ontology/                        ← Ontology definitions
│   │   ├── core/ (11 concept files)
│   │   ├── observation/ (9 files + README)
│   │   ├── supporting/ (1 file)
│   │
│   ├── domain/                          ← Domain knowledge (13 files)
│   ├── planning/                        ← Planning documents (5 files)
│   ├── design/                          ← Design specs (3 files)
│   ├── diagrams/                        ← Architecture diagrams (7 files)
│   ├── reference/                       ← Reference docs (10 files)
│   ├── implementation/                  ← Implementation docs (2 files)
│   ├── api/                             [empty]
│   ├── architecture/                    [empty]
│   ├── workflows/                       [empty]
│   ├── retrospectives/                  ← Retrospectives (4 files)
│
├── AGENTS.md                           # Authoritative engineering rules
├── README.md                           # Project readme
├── LICENSE                             # License
├── requirements.txt                    # Python dependencies
├── app.py                              # Production entry point
├── pytest.ini                          # Test configuration
├── .gitignore                          # Git exclusions
```

---

## Key Navigation Paths

### Where to find code

```
src/jarvis/                    → Production implementation
    ├── application/             → Application entry point
    ├── configuration/           → Configuration
    ├── core/jarvis/             → Kernel (control plane)
    ├── domain/                  → Domain models
    ├── engines/validation/      → Validation Engine
    ├── parsers/costx/           → CostX BOQ parser
    ├── services/                → Logging and services
tests/                        → Test suite
    ├── parser/                    → Parser tests
    ├── validation/                → Validation tests
```

### Where to Find Evidence

```
docs/engineering/evidence/     → Evidence reports (by EQ)
docs/engineering/questions/    → EQ definitions
data/reports/                    → Spike data (JSON)
tools/eq*_spike*.py               → Spike tools
```

### Where to Find Governance

```
AGENTS.md (root)           → Authoritative governance
docs/decisions/               → ADR archive (26 accepted)
docs/engineering/          → Supplemental governance docs
```

### Where to Find Contracts

```
docs/contracts/               → Frozen public contracts
    ├── BOQ_Intelligence_Public_Evidence_Contract_v1.0.md
    ├── Validation_Findings_Contract_v1.0.md
```

### Where to Find Architecture Reference

```
docs/docs/00_Vision.md                → Vision
docs/docs/01_Principles.md            → Principles
docs/docs/02_System_Blueprint.md      → Blueprint
docs/docs/03_Core_Ontology_Relationships.md → Ontology
docs/docs/04_Platform_Kernel.md       → Kernel
docs/docs/05_Data_Flow.md             → Data flow
docs/decisions/                       → ADRs
docs/diagrams/                        → Diagrams
docs/ontology/                        → Ontology definitions
```

### Where to Find History

```
archive/ → Historical artifacts
    ├── reports/     → Old status reports & release notes
    ├── docs/          → Reserved for future archived docs
    ├── planning/      → Reserved for future archived plans
    └── temporary/     → Reserved for future temporary items
```

---

## Implementation Status Summary

**Implemented** (production):
- Application module (app.py, application.py)
- Configuration module (configuration.py)
- Platform Kernel (kernel.py)
- Domain models (12 models)
- Validation Engine (engine.py + rule_registry.json)
- CostX BOQ Parser (4 files)
- Observation models (observation.py)
- Logging Service (logging_service.py)
- Lifecycle contracts (lifecycle.py)

**Not Implemented** (planned infrastructure):
- See empty directories in src/jarvis/ (22 empty subdirs)
- All numbered docs 06-25 are speculative architecture

---

**Generated**: 2026-07-22 | **Part of**: Repository Foundation Freeze