# ADR-0032: Rule Model, Registry & Evidence Contract

**Status:** FROZEN
**Date:** 2026-07-29
**Frozen Date:** 2026-07-29
**Authors:** Capability Workstream
**Prerequisites:** ADR-0030, ADR-0031, EQ-0024 (FROZEN)
**Source Review:** `docs/architecture/reviews/EQ-0024_Project_Owner_Review.md`

---

## Context

EQ-0024 established the evidence contract, rule model, and registry
architecture that govern how CheckMate rules consume evidence, execute
deterministically, and maintain compatibility with evolving BOQ Intelligence
schemas. This ADR codifies those commitments from the frozen EQ-0024
discovery.

---

## Decision

### Evidence Granularity Hierarchy

CheckMate evidence artifacts are classified into four granularity levels:

| Level | Name | Description | Example |
|-------|------|-------------|---------|
| 1 | ATOMIC | A single typed cell value (numeric, string, unit) | `Sheet1!C42 = 12.5` |
| 2 | STRUCTURAL | A named row, section, or collection of related cells with defined schema | A BOQ item row with quantity, unit, rate |
| 3 | AGGREGATE | Computed summary values across STRUCTURAL records | `Total Concrete = SUM(concrete line items)` |
| 4 | DERIVED | Inferred measurements or computed features produced by BOQ Intelligence | `Steel ratio = steel_area / concrete_area` |

### Invariant 1 — Evidence Immutability (C1.4)

Published BOQ Intelligence evidence artifacts are immutable inputs to
CheckMate. Once evidence for a run is bound, it SHALL NOT be modified,
extended, or reinterpreted during rule evaluation.

**Rationale:** Immutability guarantees that all rules in a run evaluate
against the same evidence state. Any post-binding modification would
violate determinism and make results non-reproducible.

### Invariant 2 — Deterministic Non-Evaluation (C1.5)

When rule-required evidence is missing (absent from the evidence snapshot),
CheckMate SHALL produce an explicit UNEVALUABLE_MISSING_EVIDENCE finding
rather than run ungrounded inference, silently skip the rule, or raise an
exception.

**Rationale:** Silent failures or exceptions hide coverage gaps. Ungrounded
inference produces misleading results. The explicit UNEVALUABLE outcome
clearly communicates that a rule could not be evaluated, enabling QS
professionals to understand evidence coverage limitations.

### Invariant 3 — Rule Determinism (C1.9)

Every CheckMate rule SHALL produce deterministic output given the same BOQ
evidence snapshot and rule version. Rules SHALL NOT depend on external
service calls, random number generators, or mutable global state during
evaluation.

**Rationale:** Determinism is foundational to the CheckMate capability.
Non-deterministic rules would produce non-reproducible FindingReports,
undermining auditability and trust.

### Invariant 4 — Rule Self-Containment (C1.10)

Each rule SHALL be a self-contained evaluation unit with declared domain
category, minimum evidence threshold, parameter schema, version, and
contract compatibility assertions. Rule evaluation SHALL NOT depend on
mutable global state or the side effects of other rules.

**Rationale:** Self-contained rules enable independent execution, parallel
evaluation, and clear dependency boundaries. Side-effect dependencies
between rules would create hidden coupling and non-deterministic ordering
dependencies.

### Invariant 5 — Bound RuleSnapshot Sovereignty (C1.11)

At execution initiation, the rule registry SHALL produce an immutable
RuleSnapshot containing all eligible rules bound to that run. Rules SHALL
NOT be added, removed, or modified after snapshot capture.

**Rationale:** The RuleSnapshot ensures that all rules evaluated in a run
are known and fixed at initiation. Post-initiation rule changes would
violate determinism and make results non-reproducible.

### Invariant 6 — Contract Compatibility Boundary (C1.12)

Each rule SHALL declare its contract compatibility boundary. When BOQ
Intelligence evidence schema changes result in a rule's declared contract
being unsatisfiable, the rule SHALL yield UNEVALUABLE_MISSING_EVIDENCE
rather than silently degrading or producing incorrect results.

**Rationale:** Evidence schema evolution is inevitable. Rules must be
explicit about what evidence they require. A rule that silently operates
on mismatched evidence schemas could produce incorrect results that appear
valid.

### Rule Architecture (4 Core Questions)

**Q1: Self-Containment** — A rule declares its domain category, minimum
evidence level, parameter schema, version, and contract compatibility
assertions. Evaluation operates exclusively on declared inputs.

**Q2: Execution Lifecycle** — Registry resolves eligible rules into an
immutable RuleSnapshot at run initiation. Each rule executes independently.
Rules must not mutate evidence, other rules, or rule results. Only FAIL
outcomes generate Findings.

**Q3: Registry Governance Contract** — The rule registry is the sole source
of truth. It enforces unique identity, semantic versioning, domain
classification, parameter schema validation, and immutable content after
version publication.

**Q4: Version Compatibility** — Rules declare a contract compatibility
boundary. When evidence schema changes unsatisfy a rule's contract, the
rule yields UNEVALUABLE_MISSING_EVIDENCE, not silent failure.

---

## Consequences

- Evidence is permanently immutable once a run is bound.
- Every rule evaluation is deterministic and reproducible.
- Missing evidence is explicitly surfaced, never silently ignored.
- The RuleSnapshot pattern guarantees a fixed rule set per run.
- Evidence schema evolution is handled through explicit contract
  compatibility checks, not silent degradation.
- The rule registry is the sole source of truth for all CheckMate rules.

---

## Related Capability ADRs

- **ADR-0030**: Defines CheckMate capability boundaries and domain taxonomy.
- **ADR-0031**: Defines the `FindingReport` and public capability contract.

---

## Freeze Record

| Field | Value |
|-------|-------|
| **Frozen Date** | 2026-07-29 |
| **PO-DEC Reference** | `docs/architecture/reviews/EQ-0024_Project_Owner_Review.md` |
