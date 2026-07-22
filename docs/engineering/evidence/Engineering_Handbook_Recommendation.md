# Engineering Handbook — Investigation & Recommendation

**Date**: 2026-07-22
**Task**: Task 8 — Engineering Handbook Investigation
**Part of**: Foundation Freeze & Knowledge Consolidation

---

## Question

> Investigate whether the following should remain separate or eventually become one handbook:
> - Engineering Authority
> - Quality Constitution
> - Verification Pipeline
> - Release Process
> - Engineering Debt
> - Repository Workflow

---

## Current State of Engineering Documentation

### What Exists

| Aspect | Current Document | Location |
|---|---|---|
| Engineering Authority | Engineering_Authority.md | docs/engineering/ |
| Quality Constitution | Quality_Assurance_Constitution.md | docs/engineering/ |
| Verification Pipeline | Engineering_Verification_Pipeline.md | docs/engineering/ |
| Engineering Debt | Engineering_Debt_Register.md | docs/engineering/ |
| Governance | Engineering_Governance.md | docs/engineering/ |
| Agent Operating Rules | AI_Agent_Operating_Manual.md | docs/engineering/ |
| **ALL OF THE ABOVE (combined)** | **AGENTS.md** | **Root** |

### Analysis

AGENTS.md (root, 606 lines) already contains ALL of the above as sections:

| Section | AGENTS.md Coverage |
|---|---|
| Project Authority | § Project Authority (lines 40-51) |
| Evidence Hierarchy | § Evidence Hierarchy (lines 104-119) |
| Engineering Philosophy | § Engineering Philosophy (lines 123-143) |
| Architecture Rules | § Architecture Rules (lines 147-202) |
| Engineering Workflow | § Engineering Workflow (lines 205-268) |
| Capability Lifecycle | § Capability Lifecycle (lines 230-268) |
| Implementation Rules | § Implementation Rules (lines 272-290) |
| Multi-Agent Collaboration | § Multi-Agent Collaboration (lines 308-322) |
| Documentation Responsibilities | § Documentation Responsibilities (lines 325-352) |
| Code Review Requirements | § Code Reviews (lines 354-374) |
| Repository Workflow | § Repository Workflow (lines 394-408) |
| Prohibited Actions | § Prohibited Without Approval (lines 412-426) |
| Quality Constitution | § Engineering Quality Assurance Constitution (lines 474-606) |
| Quality Gates 1-3 | § Quality Gates (lines 484-572) |
| Engineering Debt | § Engineering Debt Register pattern (lines 574-592) |
| Communication Guidelines | § Communication Guidelines (lines 430-450) |

### Standalone Documents vs AGENTS.md

| Standalone Files | Duplication with AGENTS.md | Unique Value |
|---|---|---|
| Engineering_Authority.md | § Project Authority is verbatim in AGENTS.md | None beyond what AGENTS.md provides |
| Quality_Assurance_Constitution.md | § QA Constitution is **verbatim copy** of AGENTS.md lines 474-606 | None — exact duplicate |
| Engineering_Verification_Pipeline.md | Tool names and flow described in § Quality gates | Implementation details not in AGENTS.md (tool file paths, register structure) |
| Engineering_Debt_Register.md | Debt pattern defined in AGENTS.md, but not specific debt items | **UNIQUE** — actual debt items with IDs, severity, status |
| Engineering_Governance.md | Entire governance section overlaps | None |
| AI_Agent_Operating_Manual.md | All content expanded from AGENTS.md | Extended explanations of AGENTS.md points |
| Repository_Drift_Report.md | None direct | Unique historical report |

### Overlap Assessment

| Duplicate Content | Count |
|---|---|
| Verbatim copies | 2 (Quality_Assurance_Constitution, Engineering_Authority) |
| Heavily overlapping | 2 (Engineering_Governance, AI_Agent_Operating_Manual) |
| Complementary (no overlap) | 2 (Engineering_Debt_Register, Repository_Drift_Report) |
| Partial overlap | 1 (Engineering_Verification_Pipeline) |

---

## Consolidation Options

### Option A: Single Engineering Handbook (Recommended for future, NOT now)

Merge all standalone documents into one `Engineering_Handbook.md` in docs/engineering/, with:
- AGENTS.md remaining as root authority
- Handbook referencing AGENTS.md for rules
- Debt Register and Drift Report remaining as appendices

**Cons**: Requires restructuring approved engineering documents; risk of AGENTS.md synchronization drift

### Option B: Reference Links (Recommended NOW)

Keep all documents separate but add reference links:
- `Quality_Assurance_Constitution.md` → "See AGENTS.md § Engineering Quality Assurance Constitution"
- `Engineering_Authority.md` → "See AGENTS.md § Project Authority"
- `Engineering_Governance.md` → "See AGENTS.md for authoritative governance rules"

**Pros**: Minimal change, no restructuring, no approval needed
**Cons**: More files to link through

### Option C: Delete Verb-Fixed Duplicates

Remove `Quality_Assurance_Constitution.md` and `Engineering_Authority.md` since they're verbatim extracts of AGENTS.md.

**Pros**: Clean, no duplication
**Cons**: These files may be referenced by external consumers; deleting without auditing references is risky

---

## Recommendation: Option B — Reference Links

**Keep all documents in place. Add reference links to AGENTS.md as the authoritative source.**

Rationale:

1. **AGENTS.md is already the command-and-control document.** All engineering governance, quality rules, and workflow definitions live there. Separate documents amplify duplication.

2. **Some standalone documents have unique value:**
   - Engineering_Debt_Register.md has actual debt items (unique data, not rules)
   - Engineering_Verification_Pipeline.md has tool implementation details (unique data)
   - Repository_Drift_Report.md is a historical report (unique evidence)
   - AI_Agent_Operating_Manual.md expands AGENTS.md with operational technique guidance (supplementary)

3. **Verbatim duplicates (Quality_Assurance_Constitution.md, Engineering_Authority.md) should NOT be deleted** because:
   - They may be referenced by existing consumers
   - The archive policy prohibits deletion
   - Adding a reference link is zero-risk

4. **A single Engineering Handbook would be maintenance-heavy at this stage.** The need will grow as the platform matures, but the Foundation Era should freeze first before restructuring.

### Recommended Actions

1. **Add reference link to `Quality_Assurance_Constitution.md`:**
   > **Authoritative Source**: This document is a verbatim extract of AGENTS.md § Engineering Quality Assurance Constitution. See AGENTS.md in the repository root for the authoritative version.

2. **Add reference link to `Engineering_Authority.md`:**
   > **Authoritative Source**: See AGENTS.md § Project Authority in the repository root for the authoritative engineering authority model.

3. **Add reference link to `Engineering_Governance.md`:**
   > **Authoritative Source**: AGENTS.md in the repository root is the authoritative governance document. This document provides supplemental context.

4. **No restructuring at this time.** The Foundation is frozen. Future handbook consolidation would require an ADR.

5. **For the knowledge base** (docs/knowledge/), 04_Engineering_Governance.md and 09_Methodology.md already cross-reference AGENTS.md as the source. This is sufficient.

---

## Decision

**Action**: Add reference links to standalone engineering documents pointing to AGENTS.md as authoritative.
**Restructuring**: Deferred. No handbook consolidation at this time.
**Reason**: Foundation freeze is the primary goal. Handbook consolidation provides no immediate engineering benefit and risks breaking existing consumer references.

---

**Investigation Date**: 2026-07-22
**Recommendation Status**: Recommending reference links only, no restructuring