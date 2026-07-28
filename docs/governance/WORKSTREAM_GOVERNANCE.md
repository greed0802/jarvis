# Workstream Governance

This document defines the authoritative workstream model governing all engineering, architectural, knowledge, and capability activities in the Jarvis repository.

Every identifier in the repository belongs to exactly one workstream. Workstreams are governed through canonical registers, not directory listings or file names.

---

## Workstreams

| Workstream | Prefix | Purpose | Ownership | Lifecycle | Approval Authority | Identifier Policy | Evidence Location | Status Vocabulary |
|------------|--------|---------|-----------|-----------|--------------------|--------------------|---------------------|---------------------|
| **EQ** Engineering Questions | EQ- | Formal engineering investigations. Gather evidence, evaluate alternatives, produce recommendations. Do not produce implementations directly. | Engineering | Proposal → Discovery → Engineering Spikes → Evidence → Recommendation → Accepted / Frozen | Project Owner | `docs/engineering/Engineering_Register.md` | `docs/engineering/evidence/EQ_XXXX/` | `Draft`, `Open`, `Active`, `Completed`, `Frozen`, `Rejected`, `Superseded` |
| **ADR** Architecture Decision Records | ADR- | Record architectural decisions. Are immutable once accepted. | Architecture | Propose → Draft → Accepted → Deprecated / Superseded | Project Owner | `docs/decisions/ADR_Index.md` | Reviewed within the ADR document itself | `Draft`, `Accepted`, `Rejected`, `Superseded`, `Deprecated` |
| **KE** Knowledge Engineering | KE- | Independent governance stream for knowledge management investigations. NOT an Engineering Question. | Knowledge | Discovery → Extraction → Evidence → Freeze | Project Owner | `docs/knowledge/Knowledge_Register.md` | `docs/execution/KE-XXXX-R/` | `Draft`, `Active`, `Complete`, `Frozen` |
| **CP** Capability Projects | CP- | Capability milestones from roadmap to implementation packages. | Capability | Planning → Design → Implementation → Verification → Release | Project Owner | `docs/planning/Capability_Register.md` | `docs/implementation/IP_XXXX/` | `Planning`, `Active`, `Complete`, `Frozen`, `Deferred` |
| **CB** Capability Builds | CB- | Discrete build sprints within a Capability Project. | Capability Build | Sprint → Build → Test → Verify → Done | Engineering Lead | `docs/planning/Capability_Roadmap.md` | Varies by implementation package | `Active`, `Complete`, `Deferred` |
| **MS** Milestones | MS- | Release milestones and delivery catalogues. | Release Management | Planned → Active → Complete → Released | Project Owner | Release/roadmap documents | `docs/releases/` | `Planned`, `Active`, `Complete`, `Released` |
| **R** Releases | R- / v | Increment release markers tied to milestones. | Release Management | Frozen → Released → Archived | Project Owner | Version (`__version__`/README), release docs | `docs/releases/` | `Alpha`, `Beta`, `Release Candidate`, `Production`, `Archived` |

---

## Identifier Policy

1. Every identifier is self-allocation from its canonical register only
2. No identifier may be inferred from simple directory observation
3. No identifier may be assigned without registration in the corresponding register
4. Re-allocation of identifiers is prohibited (preservation-only rule)
5. Engineering Questions are sequentially numbered (EQ-XXXX format)
6. Identifiers for Active/Frozen/EQ/ADR/KE/CB are permanent and may not be reassigned

---

## Engineering Question Lifecycle

```
Proposal
    ↓
Discovery
    ↓
Engineering Spikes (1-N)
    ├─ Evidence collected
    └─ Alternatives evaluated
    ↓
Evidence & Recommendation
    ↓
Accepted / Frozen or Rejected
    ├─ Accepted: Investigation complete; ADR candidate produced
    ├─ Frozen: Permanent, immutable (requires Project Owner approval)
    ├─ Rejected: Closed with documented reason
    └─ Deferred: Insufficient evidence; may be reopened
```

**Key**: Engineering Questions produce evidence and recommendations. Capability Projects and Capability Builds perform implementation. EQs are frozen via `Engineering_Question_Freeze_Checklist.md`.

---

## Architecture Decision Records Lifecycle

```
Proposed
    ↓
Draft ADR backlink from engineering evidence
    ↓
Final ADR accepted by Project Owner
    ↓
Frozen (immutable, no further modifications)
```

---

## Knowledge Engineering Lifecycle

```
Discovery
    ↓
Inbox import → Source Registration
    ↓
Knowledge Extraction → Evidence → Freeze
    ↓
Knowledge published to `knowledge/registry`
```

KE documents are stored in `docs/knowledge/questions/` (not in `docs/engineering/questions/`).

---

## Capability Projects Lifecycle

```
Capability Discovery
    ↓
Capability Evaluation → Project Decision
    ↓
Engineering Question → EQ Acceptance
    ↓
Spike
    ↓
Implementation Package (IP)
    ↓
Validation → Release
```

---

## Register Synchronization Rules

1. That Engineering Register is the sole authority for Engineering Question identifiers.
2. The Capability Register assigns CP identifiers.
3. The Capability projects are implemented through Builds with CB identifiers.
4. Knowledge operation-related identifiers are governed by a Knowledge Register within `docs/knowledge/`.
5. The ADR index listing within `docs/decisions/` is the single authority for ADR numbers.

---

## Repository Boundaries

| Category | Permanent Location | Register |
|-----------|-------------------|----------|
| Engineering Questions | `docs/engineering/questions/` | `docs/engineering/Engineering_Register.md` |
| EQ Evidence | `docs/engineering/evidence/EQ_XXXX/` | Engineering Register |
| Architecture Decisions | `docs/decisions/` | `docs/decisions/ADR_Index.md` |
| Knowledge Engineering | `docs/knowledge/questions/` | Knowledge Register |
| Knowledge Evidence | `docs/execution/KE-XXXX-R/` | Knowledge Register |
| Capability Implementation | implementation IPs | Capability Register / Roadmap |

---

## Workstream Collision Prevention

- Identifiers **never** migrate between workstreams
- Example: `EQ-0019` cannot later become `KE-0019`
- If a Knowledge Engineering item was accidentally stored in the Engineering directory, it must be moved to its correct directory when detected; the identifier prefix remains unchanged.

---

**Version:** 1.0
**Date:** 2026-07-28
**Authority:** Repository Governance Harmonization Sprint