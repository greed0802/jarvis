# 00 — Knowledge Index

> **Purpose**: Master index and reading guide for the Jarvis Engineering Knowledge Base. Entry point for all future AI sessions and Engineering Questions.
> **Generated**: 2026-07-15
> **Part of**: Jarvis Knowledge Consolidation

---

## What This Is

The **Jarvis Engineering Knowledge Base** is the compressed, structured, traceable engineering handbook for the Jarvis platform.

It replaces scanning ~140 scattered Markdown files (~35,000 lines) with a structured hierarchy that fits within modern LLM context windows while preserving provenance and traceability to every source document.

---

## Knowledge Hierarchy

```
00_Knowledge_Index.md          ← YOU ARE HERE

01_Project_Overview.md         ← What Jarvis is, values, principles, current state
02_Architecture_Summary.md     ← Architecture layers, runtime, data flow, implementation status
03_Domain_Knowledge.md         ← Quantity Surveying domain, BOQ structure, evidence/assessment
04_Engineering_Governance.md   ← ADR system, agent rules, governance framework
05_Engineering_Questions.md    ← 4 EQ executive summaries + 20 compressed spike reports
06_Contracts.md                ← 2 frozen public contracts + contract engineering pattern
07_Capabilities.md             ← Capability register, matrices, deferred capabilities
08_Consumers.md                ← Consumer architecture, CheckMate, access patterns
09_Methodology.md              ← Engineering playbook — workflow, gates, lifecycle
10_Implementation_Status.md    ← Code vs docs gap analysis
11_Open_Questions.md           ← Deferred EQs, gaps, verification flags, debt

Appendices/
├── A_Document_Inventory.md    ← Every file in the repository with verification status
├── B_ADR_Registry.md          ← All 26 ADRs summarized
├── C_Domain_Verification_Matrix.md ← Per-document domain verification status
├── D_AI_Authorship_Review.md  ← Repository-wide AI content classification
└── E_Redundancy_Report.md     ← Duplicates, obsolete docs, conflicts, cleanup
```

---

## Reading Paths

### For a New AI Session
```
00_Knowledge_Index → 01_Project_Overview → 02_Architecture_Summary → 09_Methodology
```
Then drill into specific documents based on task.

### For a New Engineering Question
```
00_Knowledge_Index → 01_Project_Overview → 05_Engineering_Questions (check existing EQs)
    → 03_Domain_Knowledge → 06_Contracts → 09_Methodology (follow EQ lifecycle)
```

### For Architecture Review
```
02_Architecture_Summary → Appendix B (ADR Registry) → 04_Engineering_Governance
    → 10_Implementation_Status
```

### For Domain Knowledge Work
```
03_Domain_Knowledge → Appendix C (Domain Verification Matrix)
    → Original docs/domain/ files (for detail)
```

### For Capability Planning
```
07_Capabilities → 05_Engineering_Questions → 06_Contracts → 11_Open_Questions
```

### For Consumer Development
```
08_Consumers → 06_Contracts → 02_Architecture_Summary
```

### For Repository Assessment
```
10_Implementation_Status → Appendix A (Document Inventory)
    → Appendix D (AI Authorship Review) → Appendix E (Redundancy Report)
```

### For Governance Understanding
```
04_Engineering_Governance → 09_Methodology → Appendix B (ADR Registry)
```

---

## Quick Reference: Key Facts

| Question | Answer | See |
|----------|--------|-----|
| What is Jarvis? | Professional Intelligence Platform for QS/Civil Engineering | 01 |
| What phase? | Phase 2 — Capability Era, entering Consumer Phase | 01 |
| What's implemented? | Kernel, Application, Validation Engine (~1,700 lines Python) | 02, 10 |
| What's not implemented? | 82% of documented architecture | 02, 10 |
| How many EQs completed? | 4 (EQ-0010 through EQ-0013), all Frozen Gate 3 | 05 |
| How many contracts? | 2 (BOQ Intelligence Evidence v1.0, Validation Findings v1.0) | 06 |
| How many ADRs? | 26 (all Accepted) | Appendix B |
| How many capabilities? | 2 implemented, 5 deferred | 07 |
| Evidence/Assessment boundary? | Jarvis provides evidence; humans make assessments | 03 |
| Consumer Independence rule? | Consumers depend on contracts, never internals | 06, 08 |
| Engineering workflow? | 10 steps: Review → Evidence → Implement → Test → Verify → Summarize | 09 |
| What needs Project Owner review? | 69% of domain docs, 46% of all docs | 11, Appendix C, D |

---

## Verification Summary (Repository-Wide)

| Classification | % of Documents | Meaning |
|----------------|---------------|---------|
| Project Owner Verified | 3.6% | Authoritative |
| Evidence-Backed | 25.0% | Trustworthy |
| Implementation-Backed | 2.1% | Trustworthy |
| AI-Generated, Pending | 46.4% | Needs review |
| Speculative | 12.9% | Future, not built |
| Obsolete | 2.9% | Do not use |
| Unknown | 7.1% | Needs investigation |

**Bottom line**: ~31% of repository is verified/trustworthy. The engineering evidence system (EQs, spikes, contracts) is the strongest area. Domain knowledge and speculative architecture docs are the weakest.

---

## Source Document Map

This knowledge base compresses content from these primary sources:

| Source Area | Files | Compressed Into |
|-------------|-------|-----------------|
| `docs/00_Vision.md`, `docs/01_Principles.md` | 2 | 01_Project_Overview |
| `docs/02_System_Blueprint.md`, `docs/04_Platform_Kernel.md`, `docs/05_Data_Flow.md` | 3 | 02_Architecture_Summary |
| `docs/domain/` (13 files) | 13 | 03_Domain_Knowledge, Appendix C |
| `AGENTS.md`, `AI_Agent_Operating_Manual.md`, `Engineering_Governance.md` | 3 | 04_Engineering_Governance |
| `docs/engineering/questions/` (4 files) | 4 | 05_Engineering_Questions |
| `docs/engineering/evidence/` (20 files) | 20 | 05_Engineering_Questions (spike summaries) |
| `docs/contracts/` (2 files) | 2 | 06_Contracts |
| `docs/planning/` (5 files) | 5 | 07_Capabilities, 08_Consumers |
| `AGENTS.md`, `AI_Agent_Operating_Manual.md`, `Capability_Roadmap.md` | 3 | 09_Methodology |
| `src/jarvis/` | ~12 files | 10_Implementation_Status |
| `docs/decisions/` (26 files) | 26 | Appendix B |
| All docs | ~140 files | Appendix A |

---

## How to Use This Knowledge Base

1. **Start here** (00_Knowledge_Index) — determine your reading path
2. **Read the relevant core docs** (01-11) for compressed knowledge
3. **Check appendices** for verification status, ADR details, domain matrix
4. **Drill into source documents** only when you need full detail beyond the summary
5. **Trust the verification tags** — do not base engineering decisions on AGP (unverified) or SP (speculative) content

---

## Update Protocol

This knowledge base should be updated when:
- A new Engineering Question is completed and frozen
- A new capability is implemented
- A new contract is frozen
- A new ADR is accepted
- Domain documents are verified by Project Owner
- Implementation status changes significantly
- Open questions are resolved

The `00_Knowledge_Index.md` and `10_Implementation_Status.md` are the most frequently updated documents.

---

## References

- `AGENTS.md` — AI agent engineering rules
- `docs/00_Vision.md` — Vision statement
- `docs/01_Principles.md` — Engineering principles
- All documents referenced in each knowledge document's "References" section

---

**Generated**: 2026-07-15 | **Part of**: Jarvis Knowledge Consolidation