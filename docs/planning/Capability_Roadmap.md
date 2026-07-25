# Capability Era Roadmap

Version: 1.0

---

## Approval Metadata

| Field | Value |
|-------|-------|
| **Status** | Accepted |
| **Owner** | Project Owner |
| **Effective** | 2026-07-13 |
| **Supersedes** | None |

---

## Purpose

This document governs capability planning for the Jarvis Platform.

It defines how new capabilities are discovered, evaluated, selected, and implemented.

It is the single source of truth for the Capability Era roadmap and governance process.

---

## Document Scope

This document does not:

- Define architecture. Architecture remains governed by the Vision, Principles, Blueprint, Platform Kernel, and accepted ADRs.
- Replace Engineering Questions. Engineering Questions remain the mechanism for acquiring validated engineering knowledge.
- Record implementation status. Implementation status is recorded in `docs/26_Implementation_Status.md`.
- Authorize implementation. Implementation is authorized only through the established governance workflow (Project Owner decision after Capability Evaluation).
- Modify accepted ADRs. ADRs are changed only through the ADR process.

Its sole purpose is to govern capability planning.

---

## Governance Objects and Their Relationships

The repository maintains three formal governance objects. This section documents their relationships.

```
Capability
        │
        ├── may require ──▶
        ▼
Engineering Question
        │
        ├── produces ──▶
        ▼
Evidence
        │
        ├── may justify ──▶
        ▼
ADR
```

### How They Interact

| Relationship | Meaning |
|--------------|---------|
| **Capability → Engineering Question** | A capability may have evidence gaps that require investigation before implementation. When gaps exist, an Engineering Question is registered. |
| **Engineering Question → Evidence** | An Engineering Question produces an evidence report through a spike or investigation. The report records what was found. |
| **Evidence → ADR** | Evidence may reveal that an architectural decision is needed. When evidence justifies an architectural commitment, an ADR is proposed. |
| **Capability → Production Milestone** | Once a capability has sufficient evidence (either pre-existing or from an Engineering Question), it becomes a Production Milestone. |

### Why This Matters

These relationships prevent common failure modes:

- **Implementing without evidence** — A capability with evidence gaps must go through an Engineering Question first.
- **Architecture without justification** — An ADR is only proposed when evidence justifies it, not when speculation suggests it.
- **Milestones without governance** — A Production Milestone is only created after Project Owner Decision on a Capability Candidate.

Each governance object has its own lifecycle, its own output, and its own authority. They cooperate but do not substitute for each other.

---

## Capability Lifecycle

Every capability progresses through a defined lifecycle. A capability must not remain permanently in the candidate list — it must reach a terminal state.

```
Proposed
    ↓
Candidate
    ↓
Active Investigation (if required)
    ↓
Approved for Production
    ↓
Implemented
    ↓
Completed
```

Or, at any stage:

```
Rejected
Deferred
Superseded
```

### Lifecycle States

| State | Meaning |
|-------|---------|
| **Proposed** | Identified during Capability Discovery. Not yet evaluated. |
| **Candidate** | Evaluated and recorded in the Current Capability Candidates table. Awaiting Project Owner Decision. |
| **Active Investigation** | An Engineering Question or spike is underway to resolve evidence gaps. |
| **Approved for Implementation** | Project Owner has selected the capability. Scope is defined. Ready for implementation. |
| **Implemented** | Production code, tests, and documentation are complete. |
| **Completed** | Milestone is tagged and closed. The capability is part of the production platform. |
| **Rejected** | Project Owner has decided not to pursue this capability. Reason is recorded. |
| **Deferred** | Capability is valid but not currently prioritized. May be revisited. |
| **Superseded** | Another capability or approach has replaced this one. Reference to the successor is recorded. |

### Terminal States

Every capability must eventually reach one of:

- **Completed** — successfully implemented
- **Rejected** — deliberately not pursued
- **Deferred** — intentionally postponed (with reason)
- **Superseded** — replaced by another approach

A capability that remains in Proposed, Candidate, or Active Investigation indefinitely indicates a governance gap.

---

## Readiness Checkpoints

A capability passes through two distinct readiness checkpoints. These are not the same.

| Checkpoint | Meaning |
|------------|---------|
| **Evidence Ready** | Sufficient evidence exists to implement safely. Engineering Questions are answered. Domain rules are documented. No evidence gaps remain. |
| **Implementation Ready** | Project Owner has selected the capability, scope is defined, and resources are allocated for implementation. |

### Why the Distinction Matters

A capability can be Evidence Ready without being Implementation Ready.

For example: engineering evidence exists, domain rules are documented, but another capability is a higher priority. The capability is Evidence Ready but not Implementation Ready.

This distinction prevents interpreting "High Evidence Readiness" as an instruction to begin coding. Evidence readiness is a precondition for implementation. It is not authorization to implement.

### Readiness Progression

```
No Evidence
    ↓
Partial Evidence
    ↓
Evidence Ready  ← evidence gaps are closed
    ↓
Implementation Ready  ← Project Owner authorizes implementation
    ↓
Implementation begins
```

---

## Capability Era Workflow

Every capability follows this governance flow:

```
Capability Discovery
        ↓
Capability Evaluation
        ↓
Project Owner Decision
        ↓
Capability Candidate
        ↓
Engineering Question (if needed)
        ↓
Spike / Evidence
        ↓
Production Milestone
```

### Stage Definitions

| Stage | Purpose | Output |
|-------|---------|--------|
| **Capability Discovery** | Identify candidate capabilities from production evidence, engineering backlog, and user needs | List of candidates |
| **Capability Evaluation** | Compare candidates by user value, engineering effort, evidence readiness, architectural impact | Ranked recommendation |
| **Project Owner Decision** | Select one capability to pursue | Approved Capability Candidate |
| **Capability Candidate** | Formal scope definition with evidence sources, rule provenance, constraints | Capability specification |
| **Engineering Question** | If evidence gaps exist, define the investigation | EQ registration |
| **Spike / Evidence** | Investigate and produce evidence | Evidence report |
| **Production Milestone** | Implement the capability | Production code, tests, documentation |

### Stage Rules

1. No capability may skip Capability Discovery.
2. No capability may proceed to implementation without Project Owner Decision.
3. No milestone number is assigned until a capability is approved for implementation.
4. Engineering Questions are only registered when evidence gaps exist — not all capabilities require a spike.
5. Each stage produces a defined output. No stage may begin without the previous stage's output.

---

## Capability Discovery Stage

Capability Discovery identifies candidate capabilities from three sources:

### 1. Production Evidence

What does the current production pipeline produce? What is missing?

- Current production: `WorkbookParser`, `extract_boq()`, `BOQRow`
- Known gaps: no validation, no summaries, no exports, no anomaly reporting
- Evidence sources: answered Engineering Questions, spike reports

### 2. Engineering Backlog

What investigations have been completed or are pending?

- EQ-0005 (generalization) — evidence complete, Rule of Three not met
- EQ-0008 (header discovery) — candidate, pending additional fixtures
- EQ-0009 (Context discovery) — evidence complete, extraction is not understanding

### 3. User Needs

What do professional users need that the platform cannot currently provide?

- BOQ validation and quality checking
- Structured summaries and statistics
- Data export in usable formats
- Anomaly detection and reporting

### Discovery Output

The output of Capability Discovery is a list of candidate capabilities, each with:

- Capability name
- Brief description
- Source (production evidence, engineering backlog, or user need)
- Preliminary assessment (high/medium/low for each evaluation criterion)

---

## Capability Evaluation Criteria

Each candidate capability is evaluated against four criteria:

| Criterion | Question |
|-----------|----------|
| **User Value** | Does this capability provide direct, tangible value to professional users? |
| **Engineering Effort** | Can this capability be implemented with minimal code and no speculative features? |
| **Evidence Readiness** | Do answered Engineering Questions or documented standards provide sufficient evidence to implement without a spike? |
| **Architectural Impact** | Can this capability be implemented without introducing new engines, frameworks, runtime components, or ADRs? |

### Evaluation Principles

- Prefer capabilities that require zero architectural expansion.
- Prefer capabilities built entirely from existing evidence.
- Prefer capabilities that compose with existing production types.
- A capability that requires architectural expansion is not disqualified — it simply requires stronger justification.

---

## Rule Provenance

Capabilities may introduce rules (validation, classification, detection). Rules are classified by origin:

### Engineering-Derived Rules

Rules traced to answered Engineering Questions or spike evidence.

Examples:
- Section sign conventions (EQ-0002)
- Row classification consistency (EQ-0001)
- Known anomaly reproduction (EQ-0006)

Governance: Stable until new evidence contradicts them. Changed through the Engineering Question process.

### Domain Rules

Rules sourced from office standards, professional conventions, or QS authority.

Examples:
- Duplicate item codes
- Missing descriptions
- Required UOMs
- Office QA standards

Governance: May evolve independently of parser engineering. Require Project Owner or QS authority to change. Changed when the office standard changes.

### Why the Distinction Matters

Domain rules and engineering rules have different authorities, different lifecycles, and different change triggers. Conflating them leads to incorrect governance — an engineering rule should not be changed because an office standard changed, and a domain rule should not be changed because new fixture evidence emerged.

---

## Current Capability States

The current state of all capabilities is maintained in `docs/planning/Capability_Register.md`.

The Capability Register is the single source of truth for lifecycle states. This section provides a summary for reference.

| Capability | Lifecycle State | Classification | Evidence Ready | Implementation Ready | Dependency |
|------------|:---------------:|:-------------:|:--------------:|:--------------------:|------------|
| **BOQ Intelligence** | Active | Strategic | Yes | Yes (next increments pending) | None |
| **Validation Engine** | Frozen Sub-capability | Supporting | Yes | Yes (Consumer Ready) | BOQ Intelligence (evidence) |
| **Formatter** | Deferred | Deferred | Partial | No | BOQ Intelligence (prerequisite) |
| **CheckMate** | Deferred | Deferred | Partial | No | BOQ Intelligence (baseline), domain rule catalog |
| **Cubit Parser** | Deferred | Deferred | No | No | Fixtures + Engineering Question |
| **PDF Parser** | Deferred | Deferred | No | No | None |
| **AI-Assisted Estimation** | Deferred | Deferred | No | No | BOQ Intelligence + Context Engine + training data |
| **Observation Runtime (M6)** | Historical | Historical | N/A | N/A | None |

### Capability Sequencing Priority

The current prioritization, approved by Project Owner in Capability Evaluation 001:

1. **BOQ Intelligence** — continue active development. Evidence Contract v1.0 is frozen. Next increments pending scoping.
2. **CheckMate** — activate once BOQ Intelligence has matured sufficiently and a domain rule catalog exists.
3. **Formatter** — activate once BOQ Intelligence validation baseline is trusted.

Deferred:
- **Cubit Parser** — requires fixtures from Project Owner
- **PDF Parser** — insufficient evidence; fundamentally different extraction problem
- **AI-Assisted Estimation** — long-term strategic; multiple prerequisite foundations needed

### Completion Criteria Per Priority

#### BOQ Intelligence (Current Active Capability)

| Criterion | Status |
|-----------|:------:|
| Increments 1-3 delivered | Complete |
| Evidence Contract v1.0 Frozen | Complete |
| Regression tests pass (73 tests) | Complete |
| At least one consumer (Validation Engine) | Complete |
| Further increments scoped and approved | Pending |
| All feature items from Discovery 001 delivered | In progress |
| Capability marked Completed | Pending |

#### CheckMate

| Criterion | Status |
|-----------|:------:|
| BOQ Intelligence sufficiently mature | In progress |
| Domain rule catalog formally documented | Not started |
| Capability Evaluation (Eval 002) | Not started |
| Project Owner approval to activate | Pending |

#### Formatter

| Criterion | Status |
|-----------|:------:|
| BOQ Intelligence validation output trusted | In progress |
| Capability Evaluation (Eval 002) | Not started |
| Project Owner approval to activate | Pending |

---

## Illustrative Capability Progression

The following progression reflects the current understanding of capability ordering. It is not normative. Ordering may change as evidence emerges, fixtures become available, or user needs evolve.

### Illustration 1 — BOQ Intelligence

**Classification:** Production work (leading candidate, not yet selected)

**Goal:** Transform raw BOQ extraction into validated, analyzed, summarized, and exportable BOQ intelligence.

**Constraint:** No architectural expansion. Pure functions over existing production types.

**Features (incremental):**
- Section sign validation (engineering-derived)
- Row classification consistency (engineering-derived)
- Anomaly detection (engineering-derived)
- Deterministic summaries and statistics (engineering-derived)
- Section analysis (engineering-derived)
- Trade breakdown (domain rule)
- Duplicate code detection (domain rule)
- Missing description / UOM checks (domain rule)
- CSV / JSON export (engineering)
- Human-readable summary report (engineering)

**Evidence Gate:**
- All engineering-derived rules trace to answered EQs
- All domain rules trace to documented office standards or QS authority
- Regression tests against `full_boq.xlsx`
- The 7 known OMISSION anomalies are detected
- Summary output is factually accurate

**What this does NOT do:**
- Register anything with the Kernel
- Create an engine, framework, or runtime component
- Introduce interfaces or protocols
- Modify the parser

---

### Illustration 2 — Parser Generalization

**Classification:** Engineering investigation

**Trigger:** Project Owner provides 1+ additional CostX export fixtures (different trade, template, or CostX version). Rule of Three must be satisfied (3+ structurally different fixtures).

**Capability:** Deterministic header/worksheet discovery (EQ-0008)

**Evidence Gate:** Header detection algorithm works across all available fixtures without hardcoded positions.

**Outcome:** Either generalization is justified (parser update) or it is not (parser remains narrow). Both outcomes are valid.

---

### Illustration 3 — Runtime Integration

**Classification:** Production work (future, not yet justified)

**Trigger:** A concrete consumer exists that requires runtime access to BOQ data — a Skill, a Workflow, or a user request pipeline.

**Capability:** Connect BOQ extraction and intelligence to the platform runtime.

**Evidence Gate:** A working vertical slice demonstrating runtime access to BOQ data through the Kernel/Application pattern.

**Does not begin until:** A concrete consumer justifies it.

---

### Illustration 4 — Cross-Source Intelligence

**Classification:** Draft governance (not planned)

**Trigger:** Multiple parsers exist in production (CostX + Cubit + Excel + user project data).

**Capability:** Cross-source analysis, comparison, and eventually Context assembly.

**Evidence Gate:** At least two independent parsers producing structured output. A concrete need for cross-source reasoning.

**Only then** revisit Context Engine, Knowledge Framework, and related architecture.

---

## Governance Classification

| Item | Classification |
|------|----------------|
| BOQ Intelligence | **Approved for Implementation** — selected via Capability Evaluation 001 |
| Engineering-derived rules | **Production work** — traced to answered EQs |
| Domain rules | **Domain governance** — require QS/office standard authority |
| EQ-0008 — Header discovery | **Engineering investigation** — pending fixtures |
| Observation Runtime | **Historical engineering** — ADR-0025 |
| Runtime integration | **Production work** — future, not yet justified |
| Context Engine / Knowledge | **Draft governance** — no production evidence yet |

---

## Document Classification

| Document Type | Examples | Mutable? |
|---------------|----------|:--------:|
| **Historical artifacts** | Capability Discovery 001, Capability Evaluation 001, ADRs, Engineering Questions | No |
| **Operational artifacts** | Capability Register, Capability Roadmap, Implementation Status | Yes |

Historical artifacts preserve what was known or decided at a point in time. They are immutable snapshots. Operational artifacts reflect the current state and are updated as governance decisions are made.

---

## Related Documents

| Document | Purpose | Mutable? |
|----------|---------|:--------:|
| `docs/planning/Capability_Register.md` | Current capability states (single source of truth) | Yes |
| `docs/planning/Capability_Discovery_001.md` | Immutable snapshot of Discovery 001 | No |
| `docs/planning/Capability_Evaluation_001.md` | Immutable record of Evaluation 001 and Project Owner decision | No |
| `docs/00_Vision.md` | Where Jarvis is going | No |
| `docs/01_Principles.md` | Governing principles | No |
| `docs/02_System_Blueprint.md` | High-level architecture | No |
| `docs/26_Implementation_Status.md` | What has been built | Yes |
| `docs/reference/Engineering_Questions.md` | Engineering knowledge state | Yes |
| `docs/decisions/` | Accepted ADRs | No |
| `docs/reference/Professional_Research_Backlog.md` | Research backlog | Yes |

---

## Document History

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-07-13 | Initial creation. Establishes Capability Era governance and roadmap. |
| 1.1 | 2026-07-13 | Lifecycle state corrected: "Approved for Production" → "Approved for Implementation". Current Capability Candidates replaced with reference to Capability Register. Document classification (immutable system vs operational) added. Related Documents updated with mutability column. |
| 1.2 | 2026-07-22 | CB-0001 baseline alignment. Updated Current Capability States to match Register classification. Added completion criteria per priority. Added Historical classification. |
