# Archive Inventory — Repository Foundation Freeze

**Generated**: 2026-07-22
**Sprint**: Foundation Freeze & Knowledge Consolidation
**Policy**: Nothing deleted. All items preserved in archive/ with original structure reflected.

---

## Classification Legend

| Classification | Meaning |
|---|---|
| **Active** | Currently used/modified; stays in place |
| **Historical Evidence** | Engineering artifact from completed work; moves to archive/reports/ |
| **Archive** | Superseded, old release, or obsolete; moves to archive/ |
| **Temporary** | Placeholder, empty scaffold, or stub; moves to archive/temporary/ |
| **Deprecated** | Still in place but no longer recommended; stays with deprecation notice |
| **Planned** | Future scaffold directory; stays in place for future use |

---

## Root-Level Files

| File | Classification | Rationale | Action |
|---|---|---|---|
| `AGENTS.md` | Active | Primary AI agent governance; the authoritative engineering rules document | Keep in place |
| `ARCHITECTURE_STATUS.md` | Historical Evidence | M7-era milestone status (dated 2026-07-08); superseded by docs/26_Implementation_Status.md | Move to archive/reports/ |
| `ARCHITECTURE_SYNC_REVIEW.md` | Historical Evidence | Comprehensive architecture sync audit (2026-07-08); findings are captured in knowledge base and engineering evidence | Move to archive/reports/ |
| `ARCHITECTURE_SYNC_SUMMARY.md` | Historical Evidence | Executive summary of ARCHITECTURE_SYNC_REVIEW.md; same findings, compressed format | Move to archive/reports/ |
| `RELEASE_v0.0.1-alpha.9.md` | Archive | Superseded release notes; current release info in README.md and version.py | Move to archive/reports/ |
| `app.py` | Active | Production entry point | Keep in place |
| `.gitignore` | Active | Version control configuration | Keep in place |
| `LICENSE` | Active | Project license | Keep in place |
| `pytest.ini` | Active | Test configuration | Keep in place |
| `README.md` | Active | Primary project readme | Keep in place |
| `requirements.txt` | Active | Python dependencies | Keep in place |

---

## Empty Directories (Preserved for Architecture Blueprint)

These directories exist as architectural scaffolding for future capability development. They contain no files and represent planned but not-yet-implemented areas of the platform architecture.

| Directory | Status | Rationale |
|---|---|---|
| `configs/` | Empty | Planned configuration directory |
| `scripts/` | Empty | Planned scripts directory |
| `workflows/builtin/` | Empty | Planned built-in workflows |
| `workflows/organization/` | Empty | Planned org workflows |
| `workflows/templates/` | Empty | Planned workflow templates |
| `workflows/user/` | Empty | Planned user workflows |
| `docs/api/` | Empty | Planned API documentation |
| `docs/architecture/` | Empty | Planned architecture reference |
| `docs/workflows/` | Empty | Planned workflow documentation |
| `data/backups/` | Empty | Backup storage |
| `data/cache/` | Empty | Cache storage |
| `data/embeddings/` | Empty | Embeddings storage |
| `data/exports/` | Empty | Export storage |
| `data/knowledge/` | Empty | Knowledge storage |
| `data/logs/` | Empty | Log storage |
| `data/projects/` | Empty | Project data storage |
| `data/templates/` | Empty | Template data storage |
| `third_party/licenses/` | Empty | Third-party licenses |
| `third_party/plugins/` | Empty | Third-party plugins |
| `third_party/skills/` | Empty | Third-party skills |
| `third_party/templates/` | Empty | Third-party templates |

### Empty src/jarvis Directories (Planned Architecture)

| Directory | Status |
|---|---|
| `src/jarvis/engines/builder/` | Empty — planned |
| `src/jarvis/engines/costing/` | Empty — planned |
| `src/jarvis/engines/descriptions/` | Empty — planned |
| `src/jarvis/engines/formatter/` | Empty — planned |
| `src/jarvis/engines/formula/` | Empty — planned |
| `src/jarvis/engines/qa/` | Empty — planned |
| `src/jarvis/integrations/` | Empty — planned |
| `src/jarvis/intelligence/ai/` | Empty — planned |
| `src/jarvis/intelligence/context/` | Empty — planned |
| `src/jarvis/intelligence/memory/` | Empty — planned |
| `src/jarvis/intelligence/planner/` | Empty — planned |
| `src/jarvis/intelligence/router/` | Empty — planned |
| `src/jarvis/interface/api/` | Empty — planned |
| `src/jarvis/interface/cli/` | Empty — planned |
| `src/jarvis/interface/gui/` | Empty — planned |
| `src/jarvis/knowledge/` | Empty — planned |
| `src/jarvis/platform/` | Empty — planned |
| `src/jarvis/plugins/` | Empty — planned |
| `src/jarvis/resources/` | Empty — planned |
| `src/jarvis/security/` | Empty — planned |
| `src/jarvis/skills/` | Empty — planned |
| `src/jarvis/workflows/` | Empty — planned |

Note: These empty directories represent the architecture blueprint from ADR_0012 (Repository Structure). They are not moved to archive/ because they represent the planned structure for future capability development. They should remain as scaffolding.

---

## Archived Files (Moved to archive/)

### archive/reports/ — Historical Evidence

1. **ARCHITECTURE_STATUS.md** (from root)
   - Original content: M7-era architecture status (2026-07-08)
   - Superseded by: docs/26_Implementation_Status.md
   - Classification: Historical Evidence

2. **ARCHITECTURE_SYNC_REVIEW.md** (from root)
   - Original content: Comprehensive architecture sync audit (14 issues found)
   - Superseded by: docs/engineering/evidence/ captures findings; knowledge base Appendix E documents redundancy
   - Classification: Historical Evidence

3. **ARCHITECTURE_SYNC_SUMMARY.md** (from root)
   - Original content: Executive summary of ARCHITECTURE_SYNC_REVIEW.md
   - Classification: Historical Evidence (duplicate of ARCHITECTURE_SYNC_REVIEW.md in compressed form)

4. **RELEASE_v0.0.1-alpha.9.md** (from root)
   - Original content: Release notes for v0.0.1-alpha.9
   - Superseded by: repository git tags and RELEASE.md pattern for future releases
   - Classification: Archive (superseded release)

---

## docs/knowledge/ — Knowledge Base Classification

| File | Classification | Notes |
|---|---|---|
| `00_Knowledge_Index.md` | Active | Master index — authoritative entry point for the knowledge base |
| `01_Project_Overview.md` | Active | Compressed overview of Jarvis project |
| `02_Architecture_Summary.md` | Active | Compressed architecture summary |
| `03_Domain_Knowledge.md` | Active | Domain knowledge compilation |
| `04_Engineering_Governance.md` | Active — overlaps with AGENTS.md and docs/engineering/ | Duplicates governance concepts also in AGENTS.md (root) and docs/engineering/Engineering_Governance.md. Authoritative source: AGENTS.md. Knowledge base copy kept as cached reference. |
| `05_Engineering_Questions.md` | Active | EQ and spike summaries — authoritative compressed view |
| `06_Contracts.md` | Active | Contract summaries |
| `07_Capabilities.md` | Active | Capability register |
| `08_Consumers.md` | Active | Consumer architecture |
| `09_Methodology.md` | Active — overlaps with AGENTS.md | Duplicates engineering workflow from AGENTS.md lines 205-268 and Quality gates from AGENTS.md lines 474-606. Authoritative source: AGENTS.md. |
| `10_Implementation_Status.md` | Active | Implementation status — companion to docs/26_Implementation_Status.md |
| `11_Open_Questions.md` | Active | Open questions and gaps |
| `Appendices/A_Document_Inventory.md` | Active | File-by-file inventory |
| `Appendices/B_ADR_Registry.md` | Active | ADR summary registry |
| `Appendices/C_Domain_Verification_Matrix.md` | Active | Domain verification status |
| `Appendices/D_AI_Authorship_Review.md` | Active | AI content classification |
| `Appendices/E_Redundancy_Report.md` | Active — overlaps with ARCHITECTURE_SYNC_SUMMARY.md | Contains overlapping findings with now-archived ARCHITECTURE_SYNC_REVIEW.md |

---

## docs/engineering/ Files — Duplication Analysis

| File | Overlaps With | Authoritative Source |
|---|---|---|
| `AI_Agent_Operating_Manual.md` | AGENTS.md (same content, extended form) | AGENTS.md (lines 1-606 — contains same Quality Constitution embedded) |
| `Engineering_Authority.md` | AGENTS.md § Project Authority (lines 40-51) | AGENTS.md |
| `Engineering_Debt_Register.md` | EQ-0013 Final Freeze Report debt section | Self — authoritative debt register |
| `Engineering_Governance.md` | AGENTS.md (entire governance section), knowledge/04_Engineering_Governance.md | AGENTS.md |
| `Engineering_Verification_Pipeline.md` | AGENTS.md § Quality Assurance (lines 474-604), tools/quality/Tool_Registry.md | AGENTS.md defines policy; Tool Registry defines implementation |
| `Quality_Assurance_Constitution.md` | AGENTS.md § Engineering Quality Assurance Constitution (lines 474-606) — verbatim copy | AGENTS.md (embedded copy matches standalone) |
| `Repository_Drift_Report.md` | ARCHITECTURE_SYNC_REVIEW.md (now archived) | Self-contained historical report |
| `README.md` (engineering/) | None — directory index only | Self-contained |

### Duplication Summary
- **Quality_Assurance_Constitution.md** is a verbatim extract of AGENTS.md lines 474-606 → candidate for replacement with reference link
- **AI_Agent_Operating_Manual.md** is an expanded form of AGENTS.md → keep but add note that AGENTS.md is the authoritative source
- **Engineering_Governance.md** overlaps with AGENTS.md + knowledge base → add reference link to AGENTS.md as authoritative

---

## Archive Summary

| Classification | Count |
|---|---|
| **Active (stay in place)** | 200+ files |
| **Historical Evidence → archive/** | 4 root files |
| **Empty scaffold (stay in place)** | 32+ directories |
| **Deprecated** | 0 |
| **Temporary** | 0 |

Total files archived: 4 (all root-level historical reports)

---

## Verification

- No production files were archived
- All archived files are historical evidence/reports from prior sprints
- Empty directories preserved as architectural blueprints
- No files deleted

---

**Generated**: 2026-07-22 | **Part of**: Repository Foundation Freeze