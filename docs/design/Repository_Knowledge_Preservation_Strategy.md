# Repository Knowledge Preservation Strategy

**Version**: 1.0 (RFC)  
**Status**: Draft v1.0 (RFC)  
**Category**: Repository Governance (Candidate)  
**Date**: 2026-07-13  
**Author**: Implementation Engineer

---

# Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| v1.0 | 2026-07-13 | Implementation Engineer | Initial proposal. Observation Runtime case study. Governance Validation Case #1. |

---

# Purpose

This document proposes a candidate strategy for preserving engineering knowledge within the Jarvis repository. It defines a **knowledge lifecycle** governing how artifacts are created, classified, preserved, and potentially reactivated.

This strategy responds to the gap revealed by ADR-0025: while individual ADRs and Engineering Questions articulate how evidence should be treated, no repository-wide policy existed to govern the disposition of artifacts when architectural decisions reject proposals without invalidating the underlying engineering work.

This is a **design document** for repository governance. It is **not** an implementation plan. File moves should only occur after this strategy is accepted and governance procedures are established.

---

# Philosophy

## Existing Principles Preserved

- **Documentation First** — Knowledge artifacts are documented before they are acted upon.
- **Engineering First** — Implementation decisions are grounded in verified evidence.
- **Evidence Before Abstraction** — Architectural decisions follow engineering observation.
- **ADR-Driven Development** — Architecture changes are captured as ADRs.
- **Engineering evidence is immutable** — Evidence reports are never rewritten.
- **Historical engineering reports are never rewritten** — Past investigations remain valid.
- **Fixtures are immutable** — Test data preserves the exact conditions of discovery.

## Knowledge Lifecycle

Repository knowledge moves through a lifecycle, not a static hierarchy. Artifacts transition between states as engineering evidence accumulates and architectural decisions are made.

```
                              ┌─────────────────────┐
                              │  Engineering         │
                              │  Investigation       │
                              │  (Spike / Research)  │
                              └──────────┬──────────┘
                                         │
                                         ▼
                              ┌─────────────────────┐
                              │  Engineering         │
                              │  Evidence            │
                              │  (EQ Report / Data)  │
                              └──────────┬──────────┘
                                         │
                                         ▼
                              ┌─────────────────────┐
                              │  Architecture        │
                              │  Review / ADR        │
                              └──────────┬──────────┘
                                         │
                         ┌───────────────┴───────────────┐
                         ▼                               ▼
              ┌─────────────────────┐         ┌─────────────────────┐
              │  Production          │         │  Historical          │
              │  Knowledge           │         │  Engineering         │
              │  (Active, Supported) │         │  Knowledge           │
              └─────────────────────┘         │  (Preserved,         │
                         │                    │   Immutable)         │
                         │                    └─────────────────────┘
                         ▼                               │
              ┌─────────────────────┐                    │
              │  Deprecated          │                    │
              │  (Superseded but     │                    │
              │   preserved)         │                    │
              └─────────────────────┘                    │
                         │                               │
                         └───────────────┬───────────────┘
                                         ▼
                              ┌─────────────────────┐
                              │  Reference            │
                              │  Knowledge            │
                              │  (Cross-cutting       │
                              │   permanent docs)     │
                              └─────────────────────┘
```

The lifecycle is governed by Engineering Questions (which initiate investigation), Evidence Reports (which capture findings), Project Owner Disposition (which decides outcome), and either Production acceptance or Historical preservation.

## Knowledge States

| State | Meaning | Actionable? | Immutable? |
|-------|---------|-------------|------------|
| Investigation | Active research or spike | Yes | No |
| Evidence | Published engineering findings | No | Yes |
| Production | Active platform code/docs | Yes | No |
| Historical | Preserved rejected/completed work | No | Yes |
| Deprecated | Superseded production artifact | No | Yes |
| Reference | Cross-cutting permanent knowledge | Yes (consultation) | Yes |

## Governance Rule: Historical Knowledge Is Not Production Guidance

Preserved historical knowledge documents what **was attempted** and **why it was not adopted**. It does **not** represent current production architecture.

Future engineers may consult historical knowledge for:

- Understanding prior architectural decisions
- Reproducing engineering evidence
- Evaluating whether new evidence warrants revisiting a decision

Future engineers may **not**:

- Treat historical artifacts as production dependencies
- Cite historical design documents as authoritative architecture
- Use historical implementation as production code without explicit reactivation

A historical artifact becomes reactivated only through a new Engineering Question, new ADR, and Project Owner authorization.

## Reference Knowledge

A fourth category extends the original three-state model: **Reference Knowledge**.

Reference knowledge is cross-cutting documentation that does not belong to any single investigation or production subsystem. It includes:

- Ontology definitions (core concepts, not implementation-specific)
- Engineering practice policies (fixture management, preservation strategy itself)
- Vocabulary and terminology (LANGUAGE.md)
- Professional domain conventions (office standards)

Reference knowledge is **permanent** and **authoritative** within its stated scope. Unlike Historical knowledge, it is actively maintained. Unlike Production knowledge, it does not describe runnable code.

Reference knowledge may itself be historical (a previously accepted ontology now replaced) but remains consultable.

---

# Repository Goals

1. **Reproducibility** — Any engineering investigation must be reproducible from repository artifacts at any point in the future.

2. **Traceability** — Each artifact must be traceable to its originating Engineering Question, ADR, or milestone.

3. **Immutability** — Accepted engineering evidence is never rewritten or deleted.

4. **Clarity** — The repository must clearly distinguish production artifacts from research, historical, and reference artifacts through consistent classification.

5. **Governance** — Preservation decisions require explicit authorization. Implementation engineers propose; the Project Owner disposes.

---

# Preservation Principles

## Principle P1 — Evidence Immutability

Any artifact that has produced accepted engineering evidence becomes immutable. It may not be:

- Deleted without explicit Project Owner authorization.
- Modified in ways that change the evidence it contains.
- Moved to obscure its relationship to accepted evidence.

## Principle P2 — Rejection Does Not Invalidate Evidence

An ADR rejecting an architecture does not invalidate:

- The engineering investigation that produced evidence.
- The implementation artifacts produced during investigation.
- The documents created to explain or record the work.
- The test fixtures used for validation.

These become **Historical Engineering Knowledge**.

## Principle P3 — Classification Before Action

Artifacts must be classified before any movement, deletion, or modification. The classification determines applicable lifecycle rules.

## Principle P4 — Explicit Governance

Preservation decisions follow this chain:

```
Engineering Investigation
    ↓
Engineering Evidence
    ↓
Architecture Review
    ↓
Project Owner Decision
    ↓
Repository Preservation Decision
```

## Principle P5 — Historical Knowledge Is Not Production Guidance

Preserved rejected or superseded artifacts are not authoritative for current development. They are consultable historical records only. Reactivation requires a new Engineering Question, new ADR, and Project Owner authorization.

## Principle P6 — Lifecycle Over Hierarchy

Knowledge transitions between states rather than occupying fixed layers. The diagram in the Philosophy section governs movement.

---

# Repository Knowledge Classification

This strategy defines six proposed knowledge classifications:

## Production

**Purpose**: Actively maintained, tested, and used by the platform.

**Lifecycle**: Continuous evolution through standard development process.

**Ownership**: Implementation Team maintains per milestone plan.

**Examples**: 
- `src/jarvis/parsers/costx/boq_extraction.py` — production parser
- `tests/parser/test_boq_extraction.py` — production tests
- `docs/design/M5_First_CostX_Parser_Specification.md` — accepted design
- `tests/fixtures/costx/full_boq.xlsx` — production fixture

**Movement Rules**: Changes follow standard development workflow (tests, review). May be relocated only for architectural consistency.

## Engineering Research

**Purpose**: Artifacts under active engineering investigation. May become Production or Historical based on ADR outcome.

**Lifecycle**: Active → Production (accepted ADR) OR Active → Historical (rejected ADR)

**Ownership**: Investigation Owner (typically Implementation Engineer) leads; Project Owner disposes.

**Examples**:
- `src/jarvis/parsers/observation.py` (under ADR-0025 review)
- `tests/parser/test_observation_models.py` (evaluated by ADR-0025)
- `docs/ontology/observation/` (8 ontology documents under review)
- Fixtures used in active Engineering Spikes

**Movement Rules**:
- May be modified during active investigation
- Upon ADR decision: accepted → Production, rejected → Historical
- No deletion without Project Owner authorization

## Historical Engineering

**Purpose**: Preserve engineering work whose proposed architecture was rejected or whose investigation is complete. Evidence remains valuable for future re-evaluation.

**Lifecycle**: Permanent. No further evolution anticipated without reactivation.

**Ownership**: Repository Custodian (Project Owner). Implementation Engineers may reference but not modify.

**Examples**:
- `docs/design/M6_Observation_Model.md` — retrospective design record
- `docs/ontology/observation/` (if reclassified after ADR-0025)
- Rejected ADR implementation code and tests
- Engineering Spike reports no longer active

**Why Retained**:
- Evidence may inform future investigations
- Architecture re-evaluation may become necessary
- Engineering process transparency requires audit trail
- Learning value for contributors

**Movement Rules**:
- **No modification** of content
- **May be relocated** only to improve repository clarity
- **Requires explicit Project Owner authorization**
- **Must preserve traceability** to originating evidence

## Experimental

**Purpose**: Exploratory code, prototypes, or spike scripts not yet validated through Engineering Questions. Temporary by nature.

**Lifecycle**: Experimental → Engineering Research (validated) OR Experimental → Deletion (abandoned)

**Ownership**: Creator manages; may request Project Owner disposition.

**Examples**:
- `tools/boq_row_analysis.py` — Spike #1 script (now superseded by production)
- Temporary investigation scripts
- Proof-of-concept branches

**Movement Rules**:
- May be deleted by creator if unused
- May be promoted to Engineering Research with approval
- May be retired to Historical if evidence was produced

## Deprecated

**Purpose**: Production artifacts intentionally retired but preserved for historical continuity.

**Lifecycle**: Production → Deprecated → Historical

**Ownership**: Implementation Team declares; Project Owner may confirm.

**Examples**:
- Legacy parser interfaces
- Obsolete configuration formats
- Retired workflow definitions

**Movement Rules**:
- May be relocated for clarity
- Never deleted
- Reference documentation updated to indicate deprecated status

## Superseded

**Purpose**: Architecture replaced by newer ADR; preserved for audit trail.

**Lifecycle**: Permanent

**Ownership**: Repository Custodian

**Examples**:
- ADRs marked `superseded_by: ADR_NNNN`
- Architecture descriptions replaced by newer decisions

**Movement Rules**:
- No modification
- Relocation only for clarity
- Clearly marked with supersession reference

---

# Governance

## Preservation Decision Process

When artifacts require preservation action (relocation, classification change, or deletion), this process governs:

```
1. Classification Determination
   ↓
2. Evidence Traceability Check
   ↓
3. Engineering Review (if active)
   ↓
4. Project Owner Decision
   ↓
5. Repository Update
   ↓
6. Documentation
```

### Step 1 — Classification Determination

The artifact owner determines the appropriate classification using this document's definitions. If classification is ambiguous, the artifact defaults to **Engineering Research** until resolved.

### Step 2 — Evidence Traceability Check

All related artifacts are identified:
- Associated Engineering Questions
- Related ADRs
- Implementation evidence
- Test fixtures
- Documentation references

### Step 3 — Engineering Review

For rejected architectures, the Engineering Review confirms:
- Rejection status and date
- Evidence preserved by the ADR
- Artifacts requiring preservation
- Classification recommendation

### Step 4 — Project Owner Decision

The Project Owner authorizes:
- Classification assignment
- Any proposed relocations
- Retention or deletion (extremely rare)

### Step 5 — Repository Update

Authorized changes are implemented:
- Files relocated with traceable paths
- README files updated
- Index documents revised
- Classification markers added

### Step 6 — Documentation

All preservation actions are documented through:
- Engineering Questions update (if applicable)
- ADR Reference field (if architecture affected)
- Repository changelog entry

## Implementation Engineer Constraints

Implementation Engineers **must not**:
- Move, archive, or delete rejected architecture artifacts
- Modify historical engineering evidence
- Relocate fixtures without explicit approval
- Assume preservation decisions are their responsibility

Implementation Engineers **should**:
- Identify artifacts requiring preservation decisions
- Document evidence that artifacts represent
- Propose classification for review
- Await Project Owner authorization

## Ownership Summary

| Classification | Owner | Can Propose | Authorizes |
|---------------|-------|-------------|------------|
| Production | Implementation Team | Changes | Milestone Plan |
| Engineering Research | Investigation Owner | Reclassification | Project Owner |
| Historical Engineering | Repository Custodian | — | Project Owner |
| Experimental | Creator | Promotion | Project Owner |
| Deprecated | Implementation Team | Status | Project Owner |
| Superseded | Repository Custodian | — | ADR supersession |

---

# Relationship to ADRs

## ADR Status and Knowledge Classification

| ADR Status | Artifact Classification | Meaning |
|------------|------------------------|---------|
| Proposed | Engineering Research | Under evaluation |
| Accepted | Production Architecture | Active governance |
| Rejected | Historical Engineering | Preserved, not active |
| Superseded | Superseded Architecture | Replaced by newer ADR |

## Rejected ADR Consequences

When an ADR is rejected:
1. The **decision** becomes historical (rejected status preserved).
2. **Evidence** remains valid and transitions to Historical Engineering.
3. **Implementation artifacts** are preserved with clear labeling.
4. **Fixtures** remain immutable in their current locations.
5. **Documents** are annotated with rejection context.

See ADR-0025 as the exemplar: it rejected the Observation Runtime architecture while explicitly preserving all implementation artifacts as historical engineering evidence.

## Reactivation Path

A rejected ADR or its artifacts may be reactivated by:
1. New engineering evidence (with new fixtures where applicable).
2. New Engineering Question demonstrating additional evidence.
3. New ADR proposal addressing the new evidence.
4. Project Owner authorization.
5. Reclassification from Historical Engineering to Engineering Research.

This path prevents architectural stagnation while maintaining governance discipline.

---

# Relationship to Engineering Questions

## Engineering Question Lifecycle

```
Research Backlog
    ↓
Engineering Question Proposed (Engineering Research)
    ↓
Engineering Spike Conducted (Investigation state)
    ↓
Evidence Report Published (Evidence state)
    ↓
ADR Evaluation (if architecture affected)
    ↓
Project Owner Disposition
    ↓
Repository Preservation Decision
    ↓
Artifact Classification Applied
```

## Evidence Report Preservation

Every Engineering Question Evidence Report is **permanent** and becomes **Historical Engineering** upon completion, regardless of whether the investigation leads to production changes. This ensures the repository always retains the reasoning behind every decision.

## Engineering Question as Preservation Anchor

Each Engineering Question that produces evidence anchors its associated artifacts:
- If the EQ leads to production: supporting research becomes Historical (evidence preserved)
- If the EQ is parked: artifacts remain Engineering Research
- If the EQ is superseded by a newer EQ: prior artifacts become Historical

---

# Relationship to Milestones

## Milestone Artifacts

Milestones produce artifacts across classifications:
- **Production**: Implementations delivered and accepted.
- **Historical Engineering**: Design documents for rejected approaches.
- **Engineering Research**: Incomplete investigations parked for future milestones.

## M6 Case Study (Illustrative)

The M6 milestone produced:
- **Production**: None directly (ADR-0025 rejected the architecture).
- **Historical Engineering**: `docs/design/M6_Observation_Model.md`, observation ontology, observation runtime code.
- **Evidence**: EQ-0001 through EQ-0007 reports (permanent).
- **Reference Knowledge**: This preservation strategy itself (cross-cutting).

The milestone name remains a historical marker; individual artifacts follow their classification lifecycle.

---

# Repository Directory Strategy — Future Guidance (Non-Binding)

This section recommends — not prescribes — a consistent directory organization that reflects the knowledge classifications defined above. The goal is repository consistency, not immediate relocation.

**Status**: Non-binding guidance. No engineering evidence currently justifies repository-wide archive or research directory conventions. Observation Runtime demonstrated in-place preservation, not relocation. This section may become actionable after additional governance cases validate relocation requirements.

## Proposed Conventions

| Classification | Recommended Path Convention | Rationale |
|---------------|---------------------------|-----------|
| Production | `docs/`, `src/jarvis/`, `tests/` (standard) | Business as usual |
| Engineering Research | `docs/reference/research/`, `src/jarvis/research/`, `tests/research/` | Separate from production imports |
| Historical Engineering | `docs/design/archive/`, `src/jarvis/archive/`, `tests/archive/` | Preserved but excluded from CI |
| Experimental | `tools/`, `scripts/` (temporary) | Not committed to main without review |
| Deprecated | In-place with `DEPRECATED` marker or moved to archive | Clarity over cleanup |
| Superseded | In-place with supersession ADR reference | Audit trail |

## Recommended Structure (Not Implemented)

```
docs/
├── design/
│   ├── M5_First_CostX_Parser_Specification.md  ← Production
│   └── archive/
│       └── M6_Observation_Model.md              ← Historical Engineering
├── reference/
│   ├── Engineering_Questions.md                  ← Reference Knowledge
│   ├── Engineering_Fixtures.md                   ← Reference Knowledge
│   └── research/                                 ← Engineering Research
├── ontology/
│   ├── observation/                              ← Currently Engineering Research
│   └── core/                                     ← Reference Knowledge
└── decisions/                                    ← Production + Superseded ADRs
```

## Key Recommendations

1. **`docs/design/archive/`** — Rejected design proposals are relocated here only after Project Owner authorization. This keeps active design docs separate from historical ones.

2. **`src/jarvis/research/`** — Experimental code under investigation. Not importable by production code. Production `__init__.py` files must not reference this package.

3. **`tests/research/`** — Tests for research code. Excluded from production CI test runs (but available for manual verification).

4. **`docs/reference/research/`** — Active Engineering Question artifacts. When an EQ closes, its artifacts move to `docs/reference/` (if evidence) or `docs/design/archive/` (if rejected design).

5. **No automated relocation** — All moves require explicit Project Owner authorization per the Governance section.

## What This Strategy Does Not Recommend

- No `archive/` directory at repository root — archive should be scoped per category.
- No deletion of any production or historical evidence artifact.
- No automated cleanup scripts that bypass governance.

---

# Observation Runtime Case Study

## Why Observation Runtime Triggered This Discussion

ADR-0025 rejected the Observation Runtime architecture, stating:

> _"The existing Observation implementation and documentation are retained as historical engineering artifacts until a separate repository cleanup decision is made."_

This statement exposed a governance gap: **no policy existed to determine how "historical engineering artifacts" should be handled** across the repository.

The EQ-0005 report then explicitly listed preservation decisions:

> _"Project Owner to determine archive strategy consistent with ADR-0025 and repository history policy"_

Without a repository-wide preservation policy, every future rejected architecture would face the same ambiguity — individual ad hoc decisions rather than consistent governance.

## What ADR-0025 Actually Rejected

ADR-0025 rejected the **architecture**, not the **engineering work**:

| Rejected | Preserved |
|----------|-----------|
| Observation Runtime as production architecture | Engineering Spike #1 evidence |
| `observe()` as supported production interface | Observation model implementation |
| Runtime abstractions for current scope | Row classification rules discovered |
| Provenance tracking for current format | Sign validation mechanism proven |

This distinction is precisely what the six-class classification system captures: architecture goes to Superseded or Rejected ADR status; engineering evidence transitions to Historical Engineering.

## Why Engineering History Has Value

1. **Audit Trail** — Future contributors understand why decisions were made.
2. **Re-evaluation** — New evidence may justify revisiting rejected architectures.
3. **Learning** — Rejected approaches inform future design decisions.
4. **Transparency** — The engineering process remains visible.
5. **Reproducibility** — Any investigation can be rerun from preserved artifacts.

## Current Status Under This Strategy

All Observation Runtime artifacts remain classified as **Engineering Research** until:

1. This preservation strategy is accepted.
2. Project Owner issues a preservation decision.
3. Authorized classification changes are applied.

No artifacts have been moved, archived, or deleted.

## Observation Runtime Is Not the Problem

Observation Runtime is **merely the first example** revealing the absence of a repository-wide preservation policy. Every future subsystem that undergoes architecture review will face the same question: _What happens to the artifacts when the architecture is rejected?_

This strategy answers that question for **all** subsystems — past, present, and future.

---

# Acceptance Criteria

This strategy addresses all required questions:

## What Kinds of Knowledge Exist in Jarvis?

Six classifications: **Production**, **Engineering Research**, **Historical Engineering**, **Experimental**, **Deprecated**, and **Superseded** — plus a cross-cutting **Reference Knowledge** category.

## How Should Each Kind Be Preserved?

- **Production**: Maintained, tested, evolved
- **Engineering Research**: Preserved per ADR outcome
- **Historical Engineering**: Immutable, traceable, relocated only with approval
- **Experimental**: Managed by creator
- **Deprecated**: Relocated, never deleted
- **Superseded**: Audit trail preserved

## When Should Artifacts Move?

Artifacts move only under governed conditions:

| Transition | Trigger | Authorization |
|-----------|---------|--------------|
| Engineering Research → Production | Accepted ADR | Project Owner |
| Engineering Research → Historical | Rejected ADR | Project Owner |
| Production → Deprecated | Replacement implementation | Implementation Team + PO |
| Deprecated → Historical | Final retirement | Project Owner |
| Any relocation | Clarity improvement | Project Owner |
| Any deletion | Requires explicit Project Owner authorization and permanent repository traceability | Project Owner |

## Who Authorizes Movement?

The **Project Owner** authorizes all classification changes and relocations. Implementation Engineers propose but do not decide.

## Why Preservation Is Different From Production Support

Preservation is **immutable** and **historical**. Production support is **evolvable** and **current**. Preserved artifacts serve future engineers. Production artifacts serve current users.

## How This Aligns With Existing Repository Principles

| Principle | Alignment |
|-----------|-----------|
| Documentation First | Artifacts classified and documented before action |
| Engineering First | Preservation grounded in engineering evidence |
| Evidence Before Abstraction | Classification requires evidence traceability |
| ADR-Driven Development | ADR status determines artifact lifecycle |
| Evidence Immutability | Historical Engineering is never modified |
| Fixture Immutability | Fixtures preserved regardless of ADR outcome |

---

# Governance Validation Cases

## Case #1 — Observation Runtime (Historical Engineering)

**Date**: 2026-07-13  
**Trigger**: ADR-0025 rejected the Observation Runtime as active production architecture.  
**Decision**: Disposition A — Classify as Historical Engineering (In-Place).  
**Authorized by**: Project Owner  

### Validation Scope

Case #1 validated the governance process for an **in-place preservation decision**. It did not validate directory relocation, classification transitions beyond Historical Engineering, or artifact reactivation.

### Artifacts Preserved

| Artifact | Classification | Marker Applied |
|----------|---------------|----------------|
| `src/jarvis/parsers/observation.py` | Historical Engineering | ✅ Header annotation |
| `tests/parser/test_observation_models.py` | Historical Engineering | ✅ Already annotated (ADR-0025 reference) |
| `tests/parser/test_workbook_observe_historical.py` | Historical Engineering | ✅ Already annotated (ADR-0025 reference) |
| `docs/design/M6_Observation_Model.md` | Historical Engineering | ✅ Already annotated (ADR-0025 reference) |
| `docs/ontology/observation/` (8 files) | Historical Engineering | ✅ Referenced by ADR-0025 |
| `docs/decisions/ADR_0025_Observation_Runtime_Architecture.md` | Rejected ADR | ✅ Status preserved as `rejected` |

### Repository State After Classification

- `docs/26_Implementation_Status.md`: M6 heading changed to "Observation Runtime Investigation (Historical)", Status updated to "Architecture Rejected — see ADR-0025", Repository State section added.
- Implementation code: Preserved in-place with Historical Engineering header markers. Not part of the supported production dependency graph.
- No files moved, archived, or deleted.

### Preservation Evidence

All artifacts remain consultable for:
- Understanding why the Observation Runtime was proposed and rejected.
- Reproducing Engineering Spike #1 results (row classification, sign validation).
- Evaluating future multi-format acquisition if evidence warrants revisiting ADR-0025.

### Reactivation Path

Per the Repository Knowledge Preservation Strategy, reactivation requires:
1. New engineering evidence (with new fixtures where applicable).
2. New Engineering Question demonstrating additional evidence.
3. New ADR proposal addressing the new evidence.
4. Project Owner authorization.
5. Reclassification from Historical Engineering to Engineering Research.

---

# Promotion to Accepted Governance

This document is **Draft v1.0 (RFC)** — a candidate governance model. It is not yet Accepted Governance.

Promotion from Draft to Accepted Governance requires successful validation through additional independent governance cases. This aligns with the repository's Evidence Before Promotion philosophy.

Future revisions shall be driven by new governance cases, new engineering evidence, and actual repository usage — not editorial refinement.

---

# Next Steps

Upon acceptance of this strategy:

1. **Acceptance** — Project Owner approves this strategy as repository governance.
2. **Classification Review** — Current Engineering Research artifacts are inventoried.
3. **Preservation Decision** — Project Owner issues preservation decision per the Governance process.
4. **Repository Updates** — Authorized classification changes are applied.
5. **ADR-0025 Update** — ADR-0025 references this strategy for its retention provisions.
6. **Documentation** — This document becomes Reference Knowledge (cross-cutting governance).

---

# Dependencies

This strategy assumes and extends:

- `docs/01_Principles.md` — Foundational principles
- `docs/decisions/ADR_0012_Repository_Structure.md` — Current structure
- `docs/decisions/ADR_0011_Decision_Repository.md` — ADR location
- `docs/reference/Engineering_Fixtures.md` — Fixture immutability
- `docs/decisions/ADR_0025_Observation_Runtime_Architecture.md` — Case foundation
- `docs/reference/Engineering_Questions.md` — Investigation workflow
- `docs/reference/Professional_Research_Backlog.md` — Research pipeline
