# Application Architecture Principles

## Application Constitution v1.0

**Version:** 1.0 (Foundation)

**Status:** Active

**Authority:** EQ-0021 (Permanently Frozen)

**Applies To:** All production applications on the Jarvis Platform

---

## Document Control

| Property | Value |
|----------|-------|
| Document ID | APP-CONST-001 |
| Version | 1.0 |
| Status | Active |
| Date | 2026-07-25 |
| Authority | EQ-0021 |

---

## Section 1 — Purpose

### 1.1 Why This Constitution Exists

The Application Constitution establishes immutable architectural principles that govern how production applications are architected on the Jarvis Platform.

This document exists because:

1. The Jarvis Platform requires architectural consistency across all production applications
2. Future applications must not redefine architectural principles independently
3. Architectural decisions must be documented, repeatable, and reviewable
4. The platform grows through applications — consistency ensures maintainability

This constitution is **permanent**. Amendments require a future Engineering Question.

### 1.2 Relationship to Existing Documents

| Document | Relationship |
|----------|--------------|
| **Engineering Principles** (`docs/01_Principles.md`) | Engineering governs **HOW** we build. Application Constitution governs **HOW applications are architected**. |
| **System Blueprint** (`docs/02_System_Blueprint.md`) | Blueprint defines platform subsystems. Constitution defines application architecture within those subsystems. |
| **Implementation Governance** (`docs/engineering/Implementation_Governance.md`) | Governance defines IP lifecycle. Constitution defines what applications must conform to. |
| **Consumer Architecture** (`docs/design/BOQ_Consumer_Architecture.md`) | Consumer Architecture defines consumption patterns. Constitution applies those patterns to applications. |
| **CheckMate Architecture** (`docs/design/CheckMate_Application_Architecture.md`) | CheckMate is the reference implementation of this constitution. All future applications follow the same pattern. |

### 1.3 Clarification

- **Engineering Principles** govern the engineering process — how we decide, implement, and validate.
- **Application Constitution** governs the architectural structure — how applications are composed, what rules they follow, and what patterns they use.

These documents are complementary. Both apply to every production application.

---

## Section 2 — Scope

### 2.1 Applies To

This constitution applies to **every production application** on the Jarvis Platform, including but not limited to:

- CheckMate (Quantity Surveying Guidance)
- Formatter (Presentation Model Consumer)
- Builder (Evidence Consumer)
- O&A (Omissions & Additions Consumer)
- Future Reporting Applications
- Future AI Applications
- Every future application layer

### 2.2 Does NOT Apply To

This constitution does **not** apply to:

- Parser subsystems (WorkbookParser, extraction modules)
- Infrastructure components (storage, logging, backup)
- Runtime engines (Context Engine, Planner Engine, Workflow Engine)
- Testing utilities and frameworks
- Engineering investigations and spike evidence

### 2.3 Application Definition

For the purposes of this constitution, an **Application** is:

A production component that consumes platform evidence or contracts and produces outputs for professional users — including presentation, reporting, export, and guidance.

Applications are **Tier 3 consumers** in the Consumer Architecture: they interpret evidence for professional judgment.

---

## Section 3 — Core Principles

### Principle 1 — Immutable Evidence

Evidence produced by platform components is immutable.

Applications must never modify evidence.

| Rule | Enforcement |
|------|-------------|
| Evidence dataclasses are frozen | Frozen dataclass enforcement |
| Applications consume read-only | BOQIntelligenceResult is frozen |
| No mutation paths exist | Consumer contract tests verify |
| Downstream caches must not alter | Architecture review |

### Principle 2 — Immutable Findings

Validation findings are immutable.

Applications consume findings as read-only inputs.

Applications must never generate, modify, or reinterpret findings.

| Rule | Enforcement |
|------|-------------|
| Findings dataclasses are frozen | Frozen dataclass enforcement |
| Applications consume read-only | ValidationFindings is frozen |
| Finding interpretation belongs to Validation Engine | Responsibility boundary |

### Principle 3 — Interpretation Once

Evidence interpretation occurs exactly once.

No downstream renderer performs business interpretation.

| Rule | Enforcement |
|------|-------------|
| Interpretation is performed in a single layer | Architecture topology |
| All downstream consumers read the result | Presentation Model pattern |
| Duplicate interpretation is a design error | Code review |

### Principle 4 — Presentation Model

Applications produce a deterministic Presentation Model.

Presentation Models are immutable.

The Presentation Model is the single authoritative projection of interpreted evidence.

| Property | Requirement |
|----------|-------------|
| Immutable | Derived once, never modified |
| Deterministic | Same evidence → identical Model |
| Complete | All information needed for rendering |
| Self-contained | No reference to raw evidence |

### Principle 5 — Rendering Many

All renderers consume the Presentation Model.

No renderer performs interpretation.

Consumers include:

- CLI
- GUI
- Reports
- Exports
- Formatter
- Future presentation layers

Every consumer reads from the same immutable Model.

### Principle 6 — Producer/Consumer Separation

Applications consume contracts.

Applications never depend on producer internals.

| Rule | Enforcement |
|------|-------------|
| Import only public contract symbols | Consumer contract tests |
| No import from internal modules | Package boundary enforcement |
| No dependency on producer implementation | Import verification |

### Principle 7 — Deterministic Applications

Identical inputs produce identical outputs.

| Stage | Determinism Requirement |
|-------|------------------------|
| Evidence ingestion | Identical evidence in → identical interpretation |
| Presentation Model | Identical interpretation → identical Model |
| Output generation | Identical Model → identical report/export |
| Full pipeline | Identical inputs → identical application outputs |

### Principle 8 — Human Authority

Applications assist professionals.

Applications never replace professional judgment.

| Rule | Enforcement |
|------|-------------|
| Recommendations are advisory | Language is advisory only |
| Critical findings require human review | Export gating mechanism |
| Applications do not approve work | No autonomous approval path |
| Applications do not execute corrections | No modification capability |

### Principle 9 — Advisory Recommendations

Recommendations remain advisory.

Applications never issue commands.

Applications never approve work.

| Language Rule | Permitted | Prohibited |
|---------------|-----------|------------|
| Recommendation | "Consider reviewing this item" | "Correct this item" |
| Finding severity | "High severity: potential discrepancy" | "This must be fixed" |
| Export gate | "Review required before export" | "Export blocked" |
| Guidance | "Common practice suggests..." | "Do this now" |

### Principle 10 — Contract First

Applications communicate only through approved contracts.

No implementation coupling.

| Communication Channel | Mechanism |
|-----------------------|-----------|
| Application → Consumer | Presentation Model contract |
| Application → Upstream | Evidence contract |
| Application ↔ Application | Prohibited (direct) |
| Application ↔ Application | Permitted (via contracts, exports only) |

### Principle 11 — Application Independence

Applications do not depend on each other internally.

Applications communicate only through:

- Contracts
- Presentation Models
- Exports

No application imports another application's internal modules.

No application reuses another application's interpretation.

### Principle 12 — Architecture Before Implementation

Every new application requires:

1. Engineering Question
2. Architecture Approval
3. Implementation Package

No exceptions.

This principle prevents speculative application development and ensures every application has a documented, approved architecture before any production code is written.

---

## Section 4 — Architectural Rules

### 4.1 Mandatory Rules

All production applications must conform to the following rules:

| Rule | Category | Verification |
|------|----------|-------------|
| No mutable evidence | Data integrity | Frozen dataclass enforcement |
| No mutable findings | Data integrity | Frozen dataclass enforcement |
| No duplicated interpretation | Architecture | Code review |
| No business logic in rendering | Presentation | Architecture review |
| No business logic in reports | Report generation | Architecture review |
| No business logic in exports | Export generation | Architecture review |
| No report-specific computation | Report layer | Code review |
| No export-specific computation | Export layer | Code review |
| Presentation Model is single rendering source | Architecture | Contract enforcement |
| All renderers consume Model only | Presentation | Import verification |

### 4.2 Default Architecture Topology

Every application must follow this canonical topology:

```
Platform Evidence
    ↓
Application Interpretation (ONCE)
    ↓
Presentation Model (immutable, deterministic)
    ↓
Presentation Layer (render only)
    ↓
Export Layer (serialize from Model)
```

Deviations from this topology require:

1. Documentation of the deviation
2. Architecture justification
3. Engineering Question approval

### 4.3 Layer Responsibilities

| Layer | Responsibility | Prohibited Actions |
|-------|---------------|-------------------|
| Interpretation | Consume evidence, compute severity, generate recommendations, build Model | Render, export, modify evidence, persist |
| Presentation Model | Hold deterministic projection | Contain evidence references, contain business logic, be mutable |
| Presentation | Render Model, navigation, filtering, human interaction | Interpret evidence, compute metrics, access evidence |
| Export | Serialize Model to output format | Interpret evidence, compute metrics, apply business rules |

---

## Section 5 — Prohibited Patterns

### 5.1 Absolutely Prohibited

The following patterns are prohibited in all production applications:

| Pattern | Reason | Alternative |
|---------|--------|-------------|
| Business logic inside UI | Violates Interpretation Once | Move logic to Interpretation layer |
| Business logic inside reports | Violates Presentation Model | Consume Model; do not compute |
| Business logic inside exports | Violates Presentation Model | Consume Model; do not compute |
| Application-to-application coupling | Violates Application Independence | Communicate via contracts only |
| Mutating evidence | Violates Immutable Evidence | Read-only access |
| Mutating findings | Violates Immutable Findings | Read-only access |
| Multiple interpretation passes | Violates Interpretation Once | Single pass; render from Model |
| Runtime service locators | Hidden coupling | Explicit dependency wiring |
| Plugin architectures (without EQ) | Uncontrolled extension | Requires Engineering Question |
| Hidden side effects | Non-determinism | Pure functions where possible |

### 5.2 Prohibited Without Engineering Question

The following patterns require explicit Engineering Question approval:

| Pattern | Risk | Approval Required |
|---------|------|-------------------|
| Plugin architecture | Uncontrolled extension surface | Yes |
| Dynamic module loading | Non-deterministic behavior | Yes |
| Reflection-based discovery | Hidden coupling | Yes |
| Dependency injection framework | Framework lock-in | Yes |
| Event bus in application layer | Hidden control flow | Yes |
| Asynchronous interpretation | Non-determinism risk | Yes |
| Caching interpreted results | Stale data risk | Yes |

---

## Section 6 — Extension Principles

### 6.1 How Future Applications Extend the Platform

Future applications must:

1. **Consume contracts** — Always depend on approved contracts, never internal modules
2. **Remain independently deployable** — No internal coupling between applications
3. **Avoid circular dependencies** — Application A must never depend on Application B if B depends on A
4. **Never reinterpret another application's output** — An application must not take another application's Presentation Model and interpret it as evidence
5. **Use Presentation Models when rendering** — Any application that renders interpreted data must use the Presentation Model pattern

### 6.2 Application Communication Model

```
Application A                    Application B
    │                                 │
    │  Produces                        │  Consumes
    ▼                                 ▼
Presentation Model A          Presentation Model A
    │                                 │
    │  (via contract)                  │  (read-only)
    │                                 │
    └─────────────► Application B ─────┘
                              │
                              │  Produces
                              ▼
                    Presentation Model B
```

Applications communicate **only** through:

- Published contracts
- Shared Presentation Models (read-only for consumers)
- Export artifacts

### 6.3 Independence Requirements

| Requirement | Verification |
|-------------|-------------|
| No shared mutable state | Architecture review |
| No inter-application imports | Import verification |
| Independent test suites | Separate test directories |
| Independent versioning | Separate version identifiers |
| Independent lifecycle | Separate IP packages |

---

## Section 7 — Governance

### 7.1 Amendment Process

This constitution is **permanent**.

Amendments occur only through:

1. **Engineering Question** — Proposed change with evidence
2. **Architecture Review** — Review against existing principles
3. **Project Owner Approval** — Final decision
4. **Constitution Update** — Version bump, changelog entry

Amendments must never occur during implementation.

### 7.2 Amendment Types

| Type | Description | Version Impact |
|------|-------------|----------------|
| Clarification | Non-substantive wording improvement | PATCH |
| Extension | New principle that does not conflict with existing | MINOR |
| Revision | Change to an existing principle | MAJOR |

### 7.3 Enforcement

| Mechanism | Responsibility | Frequency |
|-----------|---------------|-----------|
| Architecture review | Project Owner | Every IP freeze |
| Contract enforcement | IP verification | Every IP |
| Code review | Contributor | Every PR |
| Automated verification | CI pipeline | Every commit |

### 7.4 Waivers

Architectural waivers to this constitution require:

1. Documented justification
2. Engineering Question
3. Project Owner approval
4. Expiration date or review trigger

No waiver is permanent.

---

## Section 8 — Relationship Diagram

### 8.1 Canonical Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                        Jarvis Platform                           │
│                                                                   │
│  ┌────────────────────────────────────────────────────────┐      │
│  │                 Platform Components                     │      │
│  │  ┌──────────────┐  ┌────────────────┐                  │      │
│  │  │ BOQ Intelligence │ │ Validation Engine │              │      │
│  │  └──────┬───────┘  └───────┬────────┘                  │      │
│  │         │                  │                            │      │
│  │         ▼                  ▼                            │      │
│  │  ┌────────────────────────────────────────────────┐    │      │
│  │  │              Evidence & Findings               │    │      │
│  │  │         (Immutable, read-only contracts)       │    │      │
│  │  └──────────────────────┬─────────────────────────┘    │      │
│  │                         │                              │      │
│  │                         ▼                              │      │
│  │  ┌────────────────────────────────────────────────┐    │      │
│  │  │              Application Layer                  │    │      │
│  │  │                                                 │    │      │
│  │  │  ┌─────────────────────────────────────────┐    │    │      │
│  │  │  │      Interpretation (EXACTLY ONCE)      │    │    │      │
│  │  │  │   Severity │ Grouping │ Recommendations │    │    │      │
│  │  │  └──────────────────┬──────────────────────┘    │    │      │
│  │  │                     │                            │    │      │
│  │  │  ┌─────────────────────────────────────────┐    │    │      │
│  │  │  │     Presentation Model (Immutable)       │    │    │      │
│  │  │  │  Single deterministic projection          │    │    │      │
│  │  │  └──────────────────┬──────────────────────┘    │    │      │
│  │  │                     │                            │    │      │
│  │  │        ┌────────────┼────────────┐               │    │      │
│  │  │        ▼            ▼            ▼               │    │      │
│  │  │  ┌──────────┐ ┌──────────┐ ┌──────────┐        │    │      │
│  │  │  │Presentation│ │ Reports │ │ Exports  │        │    │      │
│  │  │  │ CLI / GUI │ │ Structured│ │PDF/JSON/CSV│     │    │      │
│  │  │  │ Render only│ │ From Model│ │From Model│       │    │      │
│  │  │  └──────────┘ └──────────┘ └──────────┘        │    │      │
│  │  └────────────────────────────────────────────────┘    │      │
│  │                         │                              │      │
│  │                         ▼                              │      │
│  │  ┌────────────────────────────────────────────────┐    │      │
│  │  │            External Consumers                   │    │      │
│  │  │  Formatter │ Builder │ O&A │ AI │ Future       │    │      │
│  │  │  (consume contracts and Presentation Models)   │    │      │
│  │  └────────────────────────────────────────────────┘    │      │
│  └────────────────────────────────────────────────────────┘      │
└──────────────────────────────────────────────────────────────────┘
```

### 8.2 Data Flow Direction

```
Platform → Evidence → Validation → Application → Presentation Model → Presentation → Export → External Consumers
```

Data flows **downward** only.

No upward data flow.

No lateral data flow between applications (except via contracts).

---

## Section 9 — Constitution Checklist

### 9.1 Mandatory Compliance Checklist

Every future Engineering Question proposing a new application architecture must satisfy every item in this checklist.

| # | Requirement | Status | Evidence |
|---|-------------|--------|----------|
| □ | Immutable evidence — Application consumes evidence as read-only frozen dataclasses | | |
| □ | Immutable findings — Validation findings consumed as read-only frozen dataclasses | | |
| □ | Interpretation once — Evidence interpretation occurs exactly once in a dedicated layer | | |
| □ | Presentation Model — Application produces an immutable, deterministic Presentation Model | | |
| □ | No renderer logic — Presentation, Report, Export layers perform no business interpretation | | |
| □ | Advisory recommendations — All recommendations use advisory language | | |
| □ | Human authority preserved — Critical findings require human review | | |
| □ | Contract-only communication — All inter-component communication through approved contracts | | |
| □ | Application independence — No direct dependency on other applications' internals | | |
| □ | Deterministic outputs — Identical inputs produce identical outputs | | |
| □ | No mutable state — Application must not modify evidence or findings | | |
| □ | No hidden side effects — All application behavior must be observable and testable | | |

### 9.2 Verification Methods

| Requirement | Verification Method |
|-------------|-------------------|
| Immutable evidence | Frozen dataclass enforcement tests |
| Immutable findings | Frozen dataclass enforcement tests |
| Interpretation once | Architecture review, code review |
| Presentation Model | Contract enforcement tests |
| No renderer logic | Import verification, code review |
| Advisory recommendations | Language pattern verification |
| Human authority | Export gating tests |
| Contract-only communication | Consumer contract tests |
| Application independence | Import verification tests |
| Deterministic outputs | Determinism tests |
| No mutable state | Integration tests |
| No hidden side effects | Code review, test coverage |

### 9.3 Non-Compliance

If any checklist item cannot be satisfied:

1. Document the exception
2. Justify why the principle cannot be followed
3. Propose an Engineering Question for constitution amendment
4. Obtain Project Owner approval before proceeding

---

## Section 10 — References

| Document | Location |
|----------|----------|
| Engineering Principles | `docs/01_Principles.md` |
| System Blueprint | `docs/02_System_Blueprint.md` |
| Implementation Governance | `docs/engineering/Implementation_Governance.md` |
| Quality Assurance Constitution | `docs/engineering/Quality_Assurance_Constitution.md` |
| Consumer Architecture | `docs/design/BOQ_Consumer_Architecture.md` |
| Consumer Access Patterns | `docs/design/BOQ_Consumer_Access_Patterns.md` |
| CheckMate Application Architecture | `docs/design/CheckMate_Application_Architecture.md` |
| EQ-0021 Architecture Recommendation | `docs/design/EQ_0021_Architecture_Recommendation.md` |
| BOQ Intelligence Public Evidence Contract v1.1 | `docs/contracts/BOQ_Intelligence_Public_Evidence_Contract_v1.1.md` |
| Validation Findings Contract v1.0 | `docs/contracts/Validation_Findings_Contract_v1.0.md` |
| AGENTS.md | `AGENTS.md` |

---

## Section 11 — Version History

| Version | Date | Changes | Authority |
|---------|------|---------|-----------|
| 1.0 | 2026-07-25 | Initial Application Constitution established | EQ-0021 |

---

## Section 12 — Success Criteria

The Application Constitution is successful when:

✅ Every production application references this document for architectural principles

✅ Future Engineering Questions for new applications use the Section 9 checklist

✅ Application architecture is consistent across CheckMate, Formatter, Builder, O&A, and all future applications

✅ No application needs to redefine these principles independently

✅ The constitution remains stable for years — amendments are rare and justified

✅ Architecture reviews reference this document as the authoritative source

✅ Consumers and contributors can predict application architecture without reading each application's design documents

---

*This document is part of the permanent constitutional documents of the Jarvis Platform.*