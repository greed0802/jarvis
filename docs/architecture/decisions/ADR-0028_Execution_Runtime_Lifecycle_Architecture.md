# ADR-0028: Execution Runtime Lifecycle Architecture

**Status:** FROZEN
**Frozen Date:** 2026-07-28
**Date:** 2026-07-28
**Authors:** Architecture Workstream
**Related Reviews:** EQ-0023 (Spikes 1, 3, 4, 6, 7)
**Prerequisites:** ADR-0027

---

## Context & Problem Statement

The Jarvis Execution Runtime must guarantee deterministic, durable, and restartable execution across long-running workflows with human-in-the-loop approval gates. Without explicit architectural governance, execution state, validation gates, and recovery policies risk becoming entangled across engine boundaries, compromising determinism and auditability.

This ADR codifies the governed execution runtime lifecycle, state machine transitions, runtime variable isolation, preflight validation gates, recovery/replanning policies, and non-overlapping validation boundaries as approved by the Project Owner in the frozen EQ-0023 Architecture Review.

---

## Decision Drivers

- Execution state must survive platform restarts and support deterministic replay.
- Planners and runtime components must operate on deterministically bound context boundaries.
- Validation must occur in distinct, non-overlapping phases with clear ownership.
- Replanning must be bounded and auditable, with explicit human intervention thresholds.
- Every architectural commitment must flow from a frozen Project Owner disposition.

---

## Architectural Commitments & Decisions

### 1. Lifecycle & Timeout Mechanics (Spike 1 · PO-DEC-002)

The Workflow Engine is the exclusive owner of the execution state machine.

| State | Type | Transitions To |
|-------|------|---------------|
| `PENDING` | Initial | `RUNNING`, `CANCELLED` |
| `RUNNING` | Active | `SUSPENDED`, `COMPLETED`, `FAILED`, `CANCELLED` |
| `SUSPENDED` | Active | `RUNNING`, `FAILED`, `CANCELLED` |
| `COMPLETED` | Terminal | None |
| `FAILED` | Terminal | None |
| `CANCELLED` | Terminal | None |

Suspension reasons are modeled as **structured metadata** attached to state `SUSPENDED` rather than as separate lifecycle states.

**Timeout Policy:**
- Every execution class MUST define a timeout policy.
- Default timeout: **7 days** (configurable per execution class).
- Expiration transitions the execution to state `CANCELLED` with cancellation reason `EXPIRED`.
- `EXPIRED` is distinct from `FAILED` - it represents a governance timeout, not an execution fault.

### 2. Execution Context Isolation & Retention (Spike 3 · PO-DEC-003)

The Workflow Engine exclusively creates, owns, and disposes of the `ExecutionContext`.

**Context Hierarchy:**
Workspace Context → Conversation Context → Execution Context
(Strict separation; data exchange only through explicit Workflow Engine interfaces.)

- `ExecutionContext` SHALL be completely isolated from conversational or workspace context.
- Secret values are NEVER stored in cleartext within `ExecutionContext` - only secret references or cryptographic scope hashes.
- Variables are strongly typed and schema-versioned; the structural schema SHALL remain immutable during execution.
- Every execution instance SHALL own exactly one `ExecutionContext` throughout its lifecycle.

**Retention Policy:**
- Default retention: **30 days** (configurable per execution class and organizational policy).
- After retention expires, `ExecutionContext` is archived or purged per policy.
- The `ExecutionJournal` remains **permanent, immutable, and append-only** - unaffected by context purging.

### 3. Plan Validation & Governed Overrides (Spike 4 · PO-DEC-004)

**Preflight Validation Gate:**

| Check | Phase | Deterministic? |
|-------|-------|----------------|
| Capability Existence | Preflight | Yes |
| Schema Compatibility | Preflight | Yes |
| Topology Validity | Preflight | Yes |
| Knowledge Availability | Preflight | Yes |
| Credentials / Permissions | Runtime | No |
| Network / Locks | Runtime | No |

An execution plan SHALL NOT transition to `RUNNING` without passing Preflight validation — unless a governed administrative override has been authorized and journaled.

**Governed Override:**
- Overrides are **governance actions**, not validation logic branches.
- Requires an explicit `OverrideToken` with:
  - Project Owner authorization
  - Required justification
  - Immutable journal entry
- Executions started under override remain **permanently marked** in the `ExecutionJournal`.
- Overrides are required for audits; no silent bypass permitted.

**Preflight idempotency:**
- Preflight plan validation SHALL be side-effect free and strictly idempotent.
- Non-deterministic checks (credentials, live network availability) SHALL NOT be evaluated in Preflight validation.

### 4. Replanning & Retry Budget (Spike 6 · PO-DEC-001)

| Trigger Event | Action | Ownership |
|---------------|--------|-----------|
| Capability Unavailable | Auto-Replan (within budget) | Planner |
| Configuration Drift | Auto-Replan (within budget) | Planner |
| Timeouts (retry exhausted) | Auto-Replan (within budget) | Planner |
| Dependency Semantic Change | → `SUSPENDED`, Human Required | Platform Kernel |
| Permission Changes | → `SUSPENDED`, Human Required | Platform Kernel |

**Replanning Mechanics:**
- Workflow Engine detects failure events and delegates replanning to the Planner Engine via an immutable `ReplanningContext`.
- Replanning SHALL preserve approved execution intent.
- Structural or semantic plan changes require explicit human authorization (`SUSPENDED`).

**Retry Budget Policy:**
- Platform default: **3 automatic replanning attempts**.
- Configurable per execution class or plan template.
- Platform hard cap: **10**.
- **Accounting Rule:** Only autonomous replanning consumes retry budget. Human approvals, administrative overrides, and manual restarts do NOT count against the budget.
- Every automatic replanning attempt SHALL be recorded as an immutable event in the `ExecutionJournal`, including the triggering condition and remaining retry budget.

**Artifact Preservation:**
Autonomous replanning SHALL preserve deterministic execution artifacts unless a new planning cycle is explicitly authorized.

### 5. Validation Boundaries (Spike 7)

| Phase | Owner | Responsible for |
|-------|-------|-----------------|
| Plan Validation | Planner Engine | Plan grammar, execution strategy, risk thresholds, feasibility matrix compliance |
| Preflight Validation | Resolver / Workflow Engine | Capability existence, schema compatibility, node topology, knowledge availability |
| Runtime Validation | Skill Framework / Workflow Engine | Skill payload correctness, intermediate step outputs, runtime execution constraints |
| Post-Execution Validation | Validation Framework | Output contracts, architectural invariants, result integrity |

**Boundary Rules:**
- Strict 1:1 mapping between validation responsibility, phase, and owning framework subsystem.
- Zero boundary overlap - no single property SHALL be validated in multiple phases.
- Downstream phases SHALL trust successful upstream validation unless the validated property has materially changed.
- Validation failure reports SHALL emit structured, phase-attributed failure metadata including phase, owner, and contract identifier.
- Validation phases SHALL execute in strict lifecycle order and SHALL NOT execute out of sequence.

---

## Architectural Invariants

### Lifecycle Invariants (from Spike 1)
- **Invariant 1.1:** Every execution instance SHALL progress through explicit state transitions owned by the Workflow Engine.
- **Invariant 1.2:** Transitions to state `SUSPENDED` MUST attach structured suspension reason metadata.
- **Invariant 1.3:** Terminal states (`COMPLETED`, `FAILED`, `CANCELLED`) SHALL NOT transition further.
- **Invariant 1.4:** An execution instance SHALL have exactly one active lifecycle state at any point in time.

### Execution Context Invariants (from Spike 3)
- **Invariant 3.1:** `ExecutionContext` SHALL be completely isolated from conversational or workspace context.
- **Invariant 3.2:** `ExecutionContext` SHALL NEVER contain cleartext secret values.
- **Invariant 3.3:** The structural schema of `ExecutionContext` SHALL remain immutable during execution.
- **Invariant 3.4:** Every execution instance SHALL own exactly one `ExecutionContext` throughout its execution lifecycle.

### Preflight Validation Invariants (from Spike 4)
- **Invariant 4.1:** An execution plan SHALL NOT transition to `RUNNING` without passing Preflight plan validation, unless a governed administrative override has been authorized and journaled.
- **Invariant 4.2:** Preflight plan validation SHALL be side-effect free and strictly idempotent.
- **Invariant 4.3:** Non-deterministic checks (credentials, live network availability) SHALL NOT be evaluated in Preflight validation.
- **Invariant 4.4:** Every administrative override SHALL be explicitly authorized, justified, and recorded as an immutable event within the `ExecutionJournal`.

### Replanning Invariants (from Spike 6)
- **Invariant 6.1:** Replanning SHALL NOT silently modify original plan intent or execution scope.
- **Invariant 6.2:** The retry budget SHALL be explicitly measured and capped; auto-replanning MUST NOT execute indefinitely.
- **Invariant 6.3:** Structural or semantic plan changes SHALL require explicit human authorization prior to resuming execution.
- **Invariant 6.4:** Every automatic replanning attempt SHALL be recorded as an immutable event in the `ExecutionJournal`, including the triggering condition and remaining retry budget.
- **Invariant 6.5:** Automatic replanning SHALL preserve deterministic execution artifacts unless a new planning cycle is explicitly authorized.

### Validation Boundary Invariants (from Spike 7)
- **Invariant 7.1:** Every validation check SHALL belong to exactly one validation phase.
- **Invariant 7.2:** Overlapping or duplicated validation across phase boundaries SHALL be strictly prohibited.
- **Invariant 7.3:** Validation failures SHALL emit structured, phase-attributed failure metadata including phase, owner, and contract identifier.
- **Invariant 7.4:** Downstream phases SHALL trust successful upstream validation unless the validated property has materially changed.
- **Invariant 7.5:** Validation phases SHALL execute in a strict lifecycle order and SHALL NOT execute out of sequence.

**Total Invariants:** 22

---

## Resolved PO Decisions

| PO-DEC | Topic | Resolution |
|--------|-------|------------|
| PO-DEC-001 | Retry Budget Defaults | 3 default retries, configurable, hard cap 10, autonomous-only accounting |
| PO-DEC-002 | Suspended Max Duration | 7 days default, configurable per execution class, expiry → CANCELLED/EXPIRED |
| PO-DEC-003 | Execution Context Retention | 30 days default, configurable, ExecutionJournal permanent |
| PO-DEC-004 | Preflight Validation Override | Governed OverrideToken with PO authorization, justification, journaled |
| PO-DEC-005 | ADR Sequence & Freeze | ADR-0027 → ADR-0028 → ADR-0029, EQ-0023 frozen |

---

## Consequences

### Positive
- **Deterministic execution**: Allowed states, validation gates, and replay semantics are fully specified.
- **Auditability**: Every transition, override, and replanning event is journaled immutably.
- **Clear component boundaries**: Each engine knows exactly what it owns and what it trusts upstream.
- **Bounded recovery**: Retry budgets and timeouts limit autonomous resource consumption.

### Negative
- **Increased state overhead**: Granular journal and structured metadata increase storage requirements.
- **Engineering debt carry-over**: `ED-0023-001` (Journal Compaction Strategy) remains unresolved and deferred to ADR-0029.
- **Preflight adds latency to startup**: Deterministic preflight checks add absolute processing time before any work begins.

---

## Deferred Engineering Debt

| Debt ID | Description | Target Resolution |
|---------|-------------|-------------------|
| ED-0023-001 | Execution Journal compaction/archiving strategy | ADR-0029 (Durable Execution Journal) |
| ED-0023-002 | External dependency non-determinism (from Spike 8) | ADR-0029 |
| ED-0023-003 | `time.now()` detection in Skills | ADR-0029 |

---

## References

- EQ-0023: Execution Runtime Architecture (`docs/engineering/questions/EQ-0023_Execution_Runtime_Architecture.md`)
- EQ-0023 Project Owner Review (`docs/architecture/reviews/EQ-0023_Project_Owner_Review.md`)
- ADR-0027: Capability Planning and Feasibility Architecture

---

## Decision

APPROVE and ADOPT the Execution Runtime Lifecycle Architecture as specified, with all 22 invariants and 5 resolved PO-*DEC items.

---

## Compliance

Architecture Compliance: PASS
Repository Boundary: PASS
EQ-0023 Traceability: PASS