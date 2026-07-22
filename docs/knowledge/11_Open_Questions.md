# 11 — Open Questions

> **Purpose**: Catalog of deferred Engineering Questions, known gaps, unresolved issues, and verification flags requiring Project Owner attention.
> **Part of**: Jarvis Knowledge Consolidation

---

## Responsibilities

This document covers:
- Deferred EQs from the master registry
- Known architecture/documentation gaps
- Verification flags — documents requiring Project Owner review
- Engineering debt requiring resolution
- Future capability activation prerequisites

This is the **active issues list** for the repository. It should be updated as items are resolved.

---

## Deferred Engineering Questions

From `docs/reference/Engineering_Questions.md`:

| EQ | Title | Status | Blocker |
|----|-------|--------|---------|
| EQ-0001 | BOQ Row Identification | Complete? | Pre-EQ-0010 foundational work |
| EQ-0002 | Sign Convention | Complete? | Pre-EQ-0010 foundational work |
| EQ-0003 through EQ-0006 | Various early EQs | Unknown | Need status review |
| EQ-0007 | Production Extraction | Complete | Foundation for all later EQs |
| EQ-0008 | (Unknown topic) | Deferred | Need to locate EQ document |
| EQ-0009 | (Unknown topic) | Deferred | Need to locate EQ document |

**Action**: Review `docs/reference/Engineering_Questions.md` for complete EQ status list. Several EQs pre-date the current documentation structure and may need archival.

---

## Architecture & Documentation Gaps

| # | Gap | Severity | Source | Resolution |
|---|-----|----------|--------|------------|
| 1 | **"Result Framework" reference unresolved** | MEDIUM | `docs/05_Data_Flow.md` line 208 | Either create Result Framework doc or update reference to `docs/ontology/core/result.md` |
| 2 | **ARCHITECTURE_SYNC_REVIEW issues** | MEDIUM | `ARCHITECTURE_SYNC_REVIEW.md` | 6 issues identified. Need audit of which are resolved. |
| 3 | **No test suite for production code** | HIGH | `src/jarvis/` | Kernel, Application, ValidationEngine have zero unit tests |
| 4 | **Missing M4-M7 blueprint docs** | LOW | M8 document references these | Blueprints may exist under different names or may need creation |
| 5 | **Antora implementation status unclear** | LOW | `docs/reference/Antora_*.md` (3 files) | Documented but no generated site found |
| 6 | **BOQ Intelligence Increment 1 blueprint missing** | LOW | Multiple references | Code exists, no separate blueprint doc found |

---

## Verification Flags — Documents Requiring Project Owner Review

**HIGH PRIORITY** (directly impact current capabilities):

| Document | Reason | Impact if Unverified |
|----------|--------|---------------------|
| `docs/domain/03_Trade_Schedule.md` | Needed for semantic classification | Cannot implement trade-aware features |
| `docs/domain/05_UOM_Standards.md` | Needed for UOM validation rules | Validation rules may be incomplete |
| `docs/domain/06_Naming_Convention.md` | Needed for description parsing | Cannot validate item descriptions |
| `docs/engineering/Engineering_Governance.md` | Governance framework | Governance rules unverified |

**MEDIUM PRIORITY** (impact future capabilities):

| Document | Reason |
|----------|--------|
| `docs/domain/08_Checking_Workflow.md` | Needed for QA capability |
| `docs/domain/09_Dimension_Group_Guide.md` | Needed for measurement intelligence |
| `docs/planning/Capability_Roadmap.md` | Capability lifecycle governance |
| `docs/02_System_Blueprint.md` | Architectural blueprint (mostly speculative) |
| `docs/03_Core_Ontology_Relationships.md` | Ontology relationships |

**LOW PRIORITY** (office/client-specific, future domains):

| Document | Reason |
|----------|--------|
| `docs/domain/01_QS_Office_Standards.md` | Office practices |
| `docs/domain/07_Client_Conventions.md` | Client-specific |
| `docs/domain/10_Drawing_Organization.md` | Drawing management |
| `docs/design/Repository_Knowledge_Preservation_Strategy.md` | Knowledge strategy |
| All 14 ontology docs | Ontology definitions |

---

## Engineering Debt Requiring Resolution

| Debt Category | Specific Item | Recommended Action |
|---------------|---------------|--------------------|
| Test Debt | No unit tests for Kernel, Application, ValidationEngine | Create pytest suite for production code |
| Documentation Debt | 82% of architecture docs are speculative | Tag speculative docs; consolidate into Future Architecture appendix |
| Verification Debt | 69% of domain docs unverified | Project Owner review of priority domain docs |
| Structure Debt | ~30 empty directories | Either implement, add README placeholders, or remove |
| Reference Debt | "Result Framework" reference | Resolve or document as future component |
| Integration Debt | No CI/CD pipeline | Set up GitHub Actions for linting + testing |
| Packaging Debt | No setup.py/pyproject.toml | Package Jarvis as installable Python project |

---

## Future Capability Activation Prerequisites

| Capability | What Must Happen First |
|------------|----------------------|
| BOQ Summaries | 1. Summary aggregation logic designed 2. EQ proposed 3. Contract defined |
| BOQ Export | 1. Export engine designed 2. Format templates 3. EQ proposed |
| Anomaly Detection | 1. Statistical baseline established 2. Anomaly rules defined 3. EQ proposed |
| QA Workflow | 1. `08_Checking_Workflow.md` verified by Project Owner 2. QA engine designed 3. EQ proposed |
| Cost Analysis | 1. Rate database sourced 2. Cost benchmarking domain knowledge verified 3. EQ proposed |
| CheckMate (Consumer) | 1. Requirements defined 2. Implementation authorized by Project Owner |

---

## Obsolete Documents — Pending Archive Action

| Document | Action |
|----------|--------|
| `docs/LANGUAGE.md` | Archive — superseded by AGENTS.md |
| `docs/JARVIS_SPECIFICATION.md` | Archive — superseded by modular docs |
| `docs/design/M6_Observation_Model.md` | Tag as OBSOLETE — rejected by ADR-0025 |
| `docs/planning/Capability_Discovery_001.md` | Archive — completed |
| `docs/planning/Capability_Evaluation_001.md` | Archive — completed |

---

## Repository Cleanup Candidates

| Action | Impact |
|--------|--------|
| Remove empty directories or add README placeholders | Reduces misleading structure |
| Consolidate 21 speculative engine docs | Reduces architecture doc surface by 75% |
| Update `docs/05_Data_Flow.md` Result Framework reference | Fixes broken reference |
| Create test suite for production code | Enables quality verification |
| Set up GitHub Actions CI | Automates quality gates |

---

## References

- `docs/reference/Engineering_Questions.md` — Master EQ registry
- `ARCHITECTURE_SYNC_REVIEW.md` — Architecture sync issues
- `docs/knowledge/Appendices/C_Domain_Verification_Matrix.md` — Domain verification status
- `docs/knowledge/Appendices/D_AI_Authorship_Review.md` — AI authorship classification
- `docs/knowledge/Appendices/E_Redundancy_Report.md` — Redundancy findings
- `docs/knowledge/10_Implementation_Status.md` — Implementation gaps

---

**Generated**: 2026-07-15 | **Part of**: Jarvis Knowledge Consolidation
**Status**: Active — update as items are resolved