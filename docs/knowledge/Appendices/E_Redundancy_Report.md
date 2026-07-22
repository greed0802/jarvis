# Appendix E: Redundancy Report

> **Purpose**: Identify duplicate, obsolete, superseded, conflicting, and archive-worthy content across the Jarvis repository.
> **Generated**: 2026-07-15
> **Part of**: Jarvis Knowledge Consolidation

---

## 1. Obsolete Documents — Recommend Archiving

| Document | Reason | Recommendation |
|----------|--------|----------------|
| `docs/LANGUAGE.md` | Language directives for AI agents. Functionally superseded by `AGENTS.md` which is the authoritative source and takes explicit precedence. LANGUAGE.md uses different tone/format and has not been referenced in any EQ or ADR. | **Archive** to `docs/archive/` |
| `docs/JARVIS_SPECIFICATION.md` (1371 lines) | Comprehensive specification written early in development. Content is now distributed across `docs/00-26` architecture documents and `AGENTS.md`. Contains older terminology and references to designs that have since evolved. | **Archive** — superseded by modular architecture docs |
| `docs/design/M6_Observation_Model.md` | Observation model design that was **explicitly REJECTED** by ADR-0025 (Observation vs Assessment). The EQ-0011 investigation replaced the observation model with the Evidence vs Assessment decomposition. | **Tag as OBSOLETE** with link to ADR-0025 |
| Older release notes (if multiple exist) | `RELEASE_v0.0.1-alpha.9.md` exists. If earlier release notes exist, they may be consolidated. | Check for earlier releases; consolidate into single release history |

## 2. Duplicate/Overlapping Content

| Topic | Documents with overlap | Recommendation |
|-------|----------------------|----------------|
| **BOQ Row structure** | `docs/domain/02_BOQ_Structure.md` + `docs/reference/BOQ_Row_Analysis.md` + EQ-0010 Spike1 evidence report | BOQ_Row_Analysis.md is the original spike evidence; 02_BOQ_Structure.md is the frozen domain doc. Both are valid — domain doc is the authoritative reference, spike is historical evidence. Keep both but cross-reference. |
| **Engineering Question registry** | `docs/reference/Engineering_Questions.md` + individual EQ files | Engineering_Questions.md is the master index. Individual EQs are authoritative for details. Keep both — index serves as quick lookup. |
| **Architecture framework docs** (05-26) | Each framework doc + `docs/02_System_Blueprint.md` (which covers the whole system) | The Blueprint is the architectural overview. Individual framework docs provide detail. However, since most engines are not implemented, the framework docs are largely speculative. Consider consolidating all unimplemented engine docs into a single "Future Architecture" appendix. |
| **Ontology docs** (14 files) | `docs/ontology/core/*.md` + `docs/03_Core_Ontology_Relationships.md` | The ontology relationship doc summarizes all core ontology objects. Individual ontology files provide detail. Keep relationships doc as summary; individual ontology docs as reference. |
| **ADR vs architecture docs** | Several ADRs (e.g., ADR-0022 Validation Engine Architecture) overlap with framework docs (e.g., `docs/14_Validation_Framework.md`) | ADRs are the authoritative decisions. Framework docs should reference ADRs. Where conflict exists, ADR wins per Evidence Hierarchy. |

## 3. Conflicts and Version Drift

| Issue | Details | Resolution |
|-------|---------|------------|
| **ARCHITECTURE_SYNC_REVIEW issue #6** | `docs/05_Data_Flow.md` references "Result Framework" as owner of Results, but no Result Framework documentation exists. | Unresolved documentation gap. Flag for Project Owner. |
| **Framework docs vs ADR-0025** | `docs/design/M6_Observation_Model.md` describes an observation model rejected by ADR-0025. Framework docs may still reference the rejected design pattern. | Audit all framework docs for references to observation model; update to reflect Evidence/Assessment decomposition. |
| **Domain docs vs EQ evidence** | Some domain docs (01-10) were AI-generated based on domain knowledge extraction. EQ-0011 Spike 5 reconciled AI-generated domain knowledge with engineering evidence. The `DOMAIN_LAYER_V1_1_REVIEW.md` captures this reconciliation. | Domain docs should carry verification tags noting which content was confirmed by EQ evidence and which remains AI-generated. |
| **ADR numbering** | Task description referenced ADR-0021 (Capability Engineering Pattern), ADR-0022 (Validation Engine Architecture), ADR-0023 (Evidence Contract Engineering). Actual files may use slightly different titles. | Verify ADR file numbers/titles are consistent. |
| **Empty directories vs documented design** | `src/jarvis/engines/builder/`, `costing/`, `descriptions/`, `formatter/`, `formula/`, `qa/` exist as empty directories. These are referenced in planning docs but have no implementation. | Either implement or remove directories to avoid misleading structure. |

## 4. Historical Artifacts — Candidate for Archive

| Document | Reason |
|----------|--------|
| `docs/planning/Capability_Discovery_001.md` | Completed discovery exercise. Results are captured in Capability_Register.md. |
| `docs/planning/Capability_Evaluation_001.md` | Completed evaluation. Decision captured in Capability_Register.md. |
| Early milestone planning docs (if they exist in docs/planning/) | M4, M5, M6, M7 blueprints were not found — may exist under different names. If found, completed milestones can be archived. |
| `ARCHITECTURE_SYNC_REVIEW.md` | Findings document from sync pass 1. If all issues resolved, can be archived. If issues remain open, keep active. |
| `ARCHITECTURE_SYNC_SUMMARY.md` | Summary of sync pass 1. Same disposition as REVIEW. |

## 5. Broken or Suspicious References

| Reference | Found In | Issue |
|-----------|----------|-------|
| "Result Framework" | `docs/05_Data_Flow.md` line 208 | No Result Framework document exists. Possibly refers to `docs/ontology/core/result.md` or an unimplemented engine. |
| M4, M5, M6, M7 planning docs | M8 assessment document references these | These blueprints were expected but not found in `docs/planning/`. May exist elsewhere or may be missing. |
| "BOQ Intelligence Increment 1" | Multiple references | Code exists in `src/jarvis/domain/boq.py`. No separate Increment 1 blueprint found. |
| Antora references | Multiple docs in `docs/reference/` | Antora toolchain is documented but no generated Antora site was found. Check implementation status. |

## 6. Consolidation Recommendations

| Current State | Recommendation |
|---------------|----------------|
| 27 architecture framework docs (00-26) | Keep 00_Vision, 01_Principles, 02_Blueprint, 04_Kernel, 05_Data_Flow, 14_Validation_Framework as active. Consolidate remaining 21 speculative engine/framework docs into a single `Future_Architecture_Reference.md` appendix until engines are implemented. |
| 14 ontology docs | Keep `03_Core_Ontology_Relationships.md` as the master summary. Keep `ontology/core/capability.md` and `ontology/core/validation.md` as implemented. Consolidate remaining 12 into a reference appendix. |
| ~20 spike evidence reports | Compress into EQ executive summaries in the knowledge base. Keep originals as traceable evidence. Do NOT remove. |
| 3+ Antora docs | Consolidate into single Antora guide or archive if Antora is not actively used. |
| `docs/reference/` (9 files) | BOQ_Row_Analysis, Engineering_Fixtures, Engineering_Questions are active. Remaining 6 can be consolidated. |

## 7. Repository Cleanup Candidates

| Path | Issue | Recommendation |
|------|-------|----------------|
| `scripts/` | Empty directory | Remove or populate |
| `workflows/` (all 4 subdirs) | Empty directories | Remove or populate |
| `third_party/` (all 4 subdirs) | Empty directories | Remove or populate |
| `docs/api/` | Empty directory | Remove or populate |
| `docs/architecture/` | Empty directory | Remove or populate |
| `docs/diagrams/` | Empty directory | Remove or populate |
| `src/jarvis/engines/builder/` etc. (6 dirs) | Empty engine directories | Documented engines with no code. Either implement or remove dirs. |
| `src/jarvis/core/context/` etc. (6 dirs) | Empty core directories | Same — implement or remove. |
| `data/backups/` etc. (8 dirs) | Empty data directories | Scaffolding for future use. Keep if planned for near-term implementation. |

---

## Priority Actions

1. **HIGH**: Tag `docs/LANGUAGE.md` and `docs/JARVIS_SPECIFICATION.md` as obsolete; move to archive
2. **HIGH**: Tag `docs/design/M6_Observation_Model.md` as superseded by ADR-0025
3. **MEDIUM**: Resolve ARCHITECTURE_SYNC_REVIEW issue #6 (missing Result Framework)
4. **MEDIUM**: Audit framework docs for ADR-0025 compliance (observation vs evidence/assessment)
5. **LOW**: Clean up empty directories or create placeholder READMEs explaining their intended purpose
6. **LOW**: Consolidate speculative engine docs into single reference appendix
7. **LOW**: Archive completed planning docs (Capability_Discovery_001, Capability_Evaluation_001)