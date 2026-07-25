# Capability Template

Use this template for every new capability proposal, evaluation, and documentation.

Copy this template, replace the bracketed placeholders, and remove this instruction block.

---

# [Capability Name]

Version: 0.1

---

## Approval Metadata

| Field | Value |
|-------|-------|
| **Status** | [Proposed / Candidate / Approved / Active / Frozen / Completed] |
| **Owner** | [Name or Role] |
| **Effective** | [YYYY-MM-DD] |
| **Supersedes** | [Reference or None] |
| **Sprint Reference** | [CB-XXXX] |

---

## Purpose

[Brief statement. What is this capability and why does it exist?]

---

## Consumers

Who depends on this capability and why?

| Consumer | Type | Dependencies | Notes |
|----------|------|:------------:|-------|
| [Name or role] | [API client, Skill, Workflow, Human, other capability] | [What this consumer needs] | |

If no consumers exist yet, that is acceptable—record "None identified" and explain why the capability is being built first.

---

## Problem

[What concrete problem does this capability solve? Reference production gaps, user needs, or engineering backlog.]

---

## Goals

[What specific outcomes will this capability produce?]

Use bullet points or individual acceptance criteria.

---

## Out of Scope

[List what this capability explicitly does NOT do.]

---

## Dependencies

| Dependency | Type | Status | Notes |
|------------|------|:------:|-------|
| [Name] | [Prerequisite / Baseline / Foundation / Peer] | [Implemented / Deferred] | |

---

## Risks

| Risk | Severity | Impact | Mitigation |
|------|:--------:|--------|------------|
| [Description] | [Low / Medium / High] | [Design, schedule, evidence gaps, etc.] | [How the risk is handled] |

---

## Engineering Questions

| EQ Reference | Status | Key Finding |
|-------------|:------:|-------------|
| [EQ-XXXX] | [Open / In Progress / Answered / Frozen] | [Summary] |

---

## Evidence

| Evidence Source | Type | Status | Traceability |
|----------------|------|:------:|--------------|
| [EQ-XXXX Spike N] | [Observation / Algorithm / Classification / Audit] | [Frozen] | [Which rules or facts trace here] |
| [Domain standard] | [Office standard / QS convention] | [Documented] | [Which rules trace here] |

Evidence completeness: [None / Partial / Complete — all gaps closed]

---

## Public Contract

| Contract | Version | Status |
|----------|:-------:|:------:|
| [Path to contract .md] | [semver] | [Candidate / Frozen] |

Contract stability expectations:
- Data types changed in a MAJOR version only
- Immutable output guarantees
- Semantic versioning rules

---

## Internal Architecture

[How the capability is structured internally.]

- Production modules involved
- Pure functions, extensions of existing types, or net-new components
- No new engines, frameworks, or runtime layers unless explicitly approved
- Imports: list key files and their responsibilities

---

## Tests

| Test File | # Tests | Status |
|-----------|:-------:|:------:|
| [test_*.py] | [N] | [Passing / Failing] |

Regression test count: [N]

Fixture dependencies: [Fixture files used]

---

## Regression

- [ ] Regression tests committed.
- [ ] Existing tests pass.
- [ ] Fixture metadata updated.
- [ ] Architecture audit confirms no drift.

---

## Freeze Report

To be completed when this capability reaches the **Frozen Sub-capability** state.

| Criterion | Met? |
|-----------|:---:|
| All increments pass acceptance criteria | [ ] |
| Public contract stable and versioned | [ ] |
| Regression tests pass against authoritative fixture(s) | [ ] |
| At least one real consumer exercising the capability | [ ] |
| No open EQs within increment scope | [ ] |
| Architecture audit confirms no drift | [ ] |

Freeze Declaration: [Date, rationale]

---

## Known Limitations

[List limitations that exist in the current deliverable.]

---

## Future Expansion

[What future increments might look like. Approved directions, not promises.]

---

## Document History

| Version | Date | Change |
|---------|------|--------|
| 0.0 | [YYYY-MM-DD] | Initial templating. |