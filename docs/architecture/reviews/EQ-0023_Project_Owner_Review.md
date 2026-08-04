# ====================================================
# PROJECT OWNER REVIEW
# EQ-0023 — EXECUTION RUNTIME ARCHITECTURE
# ====================================================

Date: 2026-07-28
Source: `../engineering/questions/EQ-0023_Execution_Runtime_Architecture.md`
Status: FROZEN
Frozen Date: 2026-07-28

---

## Purpose

This document transforms the EQ-0023 engineering investigation (8 discovery spikes) into a structured Project Owner Review package. It separates architectural commitments from implementation details and engineering debt. ADR authoring is NOT in scope. No runtime changes are proposed here.

---

## 1. Spike 1: Execution Lifecycle

### Evidence Status
[ ] Awaiting Project Owner Decision

### Summary
How should the execution lifecycle be modeled to support deterministic execution, human-in-the-loop approvals, and clear terminal states? The spike compared an in-memory synchronous approach (Alternative A) against a Durable Event-Sourced State Machine via Workflow Engine (Alternative B).

### Key Findings
- A state machine with 6 states (`PENDING`, `RUNNING`, `SUSPENDED`, `COMPLETED`, `FAILED`, `CANCELLED`) is required.
- `SUSPENDED` has sub-states: `WAITING_APPROVAL`, `WAITING_RESOURCES`, `WAITING_DEPENDENCY`.
- In-memory blocking cannot survive platform restarts and consumes compute during human wait periods.
- A durable state machine serializes wait states to an Execution Journal, ensuring restartability.

### Recommendation
Adopt Alternative B. The Workflow Engine must own the Execution State Machine and serialize wait states to an Execution Journal.

### Candidate Architectural Commitments
- Execution state machine ownership lives exclusively in the Workflow Engine.
- All state transitions are journaled to an append-only Execution Journal.
- Human-in-the-loop approval points are modeled as `SUSPENDED` / `WAITING_APPROVAL`.
- Terminal states (`COMPLETED`, `FAILED`, `CANCELLED`) are immutable once reached.

### Candidate Implementation Details
- State machine serialization format.
- Journal entry structure for state transitions.
- Sub-state enumeration for `SUSPENDED`.
- Recovery process to resume from the last committed state.

### Candidate Open Questions / Engineering Debt
- **ED-0023-001:** Journal compaction/archiving strategy for long-running executions.
- What is the maximum `SUSPENDED` idle time before automatic cancellation?

### Proposed Architectural Invariants
1. Execution state is never maintained purely in memory.
2. `SUSPENDED` transitions must always specify a sub-state reason.
3. Terminal states may not transition further.

### Suggested ADR Mapping
- **ADR-0028** (Execution Runtime Lifecycle) — state machine definition.

### Project Owner Disposition
**Status:** ✅ Approved with Refinements (2026-07-28)

**Summary of Refinements & Decisions:**
- Accepted core state machine direction owned exclusively by Workflow Engine.
- **Timeout Policy (PO-DEC-002):** Every execution class MUST define a timeout policy (defaulting to 7 days if unspecified). Expiration transitions the execution to state `CANCELLED` with cancellation reason `EXPIRED` (distinct from `FAILED`).
- **Suspension Mechanics:** Suspension reasons MUST be structured as structured metadata attached to state `SUSPENDED`, rather than separate lifecycle states.

**Approved Architectural Invariants:**
- `Invariant 1.1`: Every execution instance SHALL progress through explicit state transitions owned by the Workflow Engine.
- `Invariant 1.2`: Transitions to state `SUSPENDED` MUST attach structured suspension reason metadata.
- `Invariant 1.3`: Terminal states (`COMPLETED`, `FAILED`, `CANCELLED`) SHALL NOT transition further.
- `Invariant 1.4`: An execution instance SHALL have exactly one active lifecycle state at any point in time.

---

## 2. Spike 2: Capability Planning

### Evidence Status
[ ] Awaiting Project Owner Decision

### Summary
Should the Planner have read-only access to capabilities? How is feasibility represented, and what belongs in a Capability Snapshot? The spike compared live capability discovery against an immutable snapshot approach.

### Key Findings
- Live capability reads during planning may cause race conditions if capabilities upgrade or degrade.
- An immutable `Capability Snapshot` injected into Context at plan creation guarantees determinism.
- Snapshot fields: `timestamp`, `capability_versions`, `feasibility_matrix`.
- Feasibility is a boolean matrix of constraints vs. requirements.
- Planner access must be **strictly read-only**.

### Recommendation
Adopt Alternative B (Immutable Capability Snapshot). Feasibility is a precomputed boolean matrix. Planner has strict read-only access to the snapshot.

### Candidate Architectural Commitments
- Capability Snapshot is immutable and point-in-time.
- Planner Engine receives Capability Snapshot as part of Planning Context.
- Feasibility is a boolean computation, not an AI judgment call.
- Capability registry is the system of record for snapshot generation.

### Candidate Implementation Details
- Snapshot generation trigger (plan request time).
- Schema for `capability_versions` and `feasibility_matrix`.
- Atomicity: snapshot must be complete and consistent at the time of creation.

### Candidate Open Questions / Engineering Debt
- How frequently should the Capability Snapshot be refreshed?
- Is there a stale-snapshot grace period, or is stale information immediately invalid?

### Proposed Architectural Invariants
1. Planner never queries live capability state during plan composition.
2. Capability Snapshot is immutable once injected.
3. Feasibility is strictly boolean — no popularity, preference, or AI judgment embedded.

### Suggested ADR Mapping
- **ADR-0027** — Capability Planning and Feasibility Architecture.

### Project Owner Disposition
**Status:** ✅ Approved with Refinements (2026-07-28)

**Summary of Refinements & Decisions:**
- Accepted read-only Planner model and Capability Registry sovereignty.
- **Versioned Snapshot:** Planning operates exclusively on a versioned, immutable `CapabilitySnapshot` generated by the Capability Registry at plan initiation.
- **Feasibility Boundary:** Feasibility SHALL determine only whether a capability satisfies required binary constraints. Capability selection, ranking, or optimization are separate architectural concerns and SHALL NOT influence feasibility.

**Approved Architectural Invariants:**
- `Invariant 2.1`: The Planner Engine SHALL NOT query the live capability registry during plan composition.
- `Invariant 2.2`: The `CapabilitySnapshot` SHALL be immutable once injected into Context.
- `Invariant 2.3`: Feasibility SHALL determine only whether a capability satisfies required constraints; selection, ranking, or optimization are separate architectural concerns and SHALL NOT influence feasibility.
- `Invariant 2.4`: Every execution plan SHALL reference exactly one `CapabilitySnapshot` throughout its planning lifecycle.

---

## 3. Spike 3: Execution Context

### Evidence Status
[ ] — Awaiting Project Owner Decision

### Summary
Should the Execution Context exist separately from Workspace/Conversation Context? The spike compared Unified Global Context against dedicated, isolated Execution Context.

### Key Findings
- Shared context exposes extreme mutation risk during long-running execution tasks.
- The Execution Context is exclusively owned by the Workflow Engine during execution.
- Minimal fields: `execution_id`, `plan_ref`, `variables`, `secrets_scope_hash`, `virtual_clock_time`.

### Recommendation
Adopt Alternative B — Copy a minimal required subset of Workspace Context into an isolated Execution Context. Ownership is exclusive to the Workflow Engine.

### Candidate Architectural Commitments
- Execution Context is an owned resource of the Workflow Engine during execution.
- Execution Context never shares storage/namespace with Conversation Context.
- Secrets scope is strictly hashed (not stored in plaintext) within Execution Context.
- Variables in Execution Context are typed and versioned.

### Candidate Implementation Details
- Execution Context object schema.
- Copy-from-Workspace logic (which fields to subset).
- Garbage collection after execution ends.
- Secrets storage approach (hash reference only, actual secrets from vault).

### Candidate Open Questions / Edge Questions
- How large can `variables` grow before performance degradation?
- Should Execution Context be transient, ephemeral, or long-lived after execution?

### Proposed Architectural Invariants
- Execution Context Isolation — no shared mutable reference with any other context.
- Secrets must never exist in cleartext within Execution Context.
- Execution Context is created once per execution, never modified structurally.

### Suggested ADR Mapping
- **ADR-0028** (partial) — Execution Runtime Lifecycle covers Execution Context ownership.

### Project Owner Disposition
**Status:** ✅ Approved with Refinements (2026-07-28)

**Summary of Refinements & Decisions:**
- **Exclusive Ownership:** The Workflow Engine exclusively creates, owns, and disposes of the `ExecutionContext`.
- **Retention Policy (PO-DEC-003):** Default retention of 30 days (configurable by execution class and organizational policy). `ExecutionContext` is archived/purged after retention expires. The `ExecutionJournal` remains permanent, immutable, and append-only.
- **Context Hierarchy:** Workspace Context, Conversation Context, and Execution Context remain strictly distinct; data exchange occurs through explicit Workflow Engine interfaces.
- **Secret Security:** `ExecutionContext` stores secret references or cryptographic scope hashes only; cleartext secrets SHALL NEVER be persisted.
- **Typed Variables:** Variables are strongly typed and schema-versioned.

**Approved Architectural Invariants:**
- `Invariant 3.1`: `ExecutionContext` SHALL be completely isolated from conversational or workspace context.
- `Invariant 3.2`: `ExecutionContext` SHALL NEVER contain cleartext secret values.
- `Invariant 3.3`: The structural schema of `ExecutionContext` SHALL remain immutable during execution.
- `Invariant 3.4`: Every execution instance SHALL own exactly one `ExecutionContext` throughout its execution lifecycle.

---

## 4. Spike 4: Plan Validation

### Evidence Status
** — Awaiting Project Owner Decision

### Summary
What constitutes deterministic plan validation and what are the boundaries? The spike compared lazy validation (Alternative A) against strict preflight verification (Alternative B).

### Key Findings
- Validation must be reproducible for deterministic checks.
- Four validation dimensions: Capability Existence, Schema Compatibility, Dependencies Satisfied, Knowledge Availability.
- These are deterministic and belong in PREFLIGHT phase.
- Credentials/Permissions are non-deterministic and belong in RUNTIME phase.
- Lazy validation increases risk of mid-execution crashes.

### Recommendation
Adopt Alternative B — All deterministic checks must pass Preflight Plan Validation before transitioning to `RUNNING`.

### Candidate Architectural Commitments
- Preflight phase is a mandatory gate before `RUNNING`.
- Preflight owns: Capability Existence, Schema Compatibility, Dependencies, Knowledge Availability.
- Runtime owns: Credentials/Permissions.
- All Preflight checks must be deterministic.

### Candidate Implementation Details
- Preflight validation orchestration mechanism.
- Individual validation contracts per check type.
- Error handling on Preflight checks to resolve partial failure path.

### Candidate Open Questions / Edge Questions
- Is there a mechanism for manual override on Preflight validation (e.g., force-execute for recovery)?
- How specific is the failure reason (which capability is missing, not just binary failure)?

### Proposed Architectural Invariants
- PREFLIGHT must run as a separate, idempotent phase before any runtime state is created.
- RUNTIME validation may never block initial execution. It is in-process and can cause suspension.
- Validation failures are always deterministic and reproducible.

### Suggested ADR Mapping
- **ADR-0028** — Execution Runtime Lifecycle (Preflight/Runtime boundary).

### Project Owner Disposition
**Status:** ✅ Approved with Refinements (2026-07-28)

**Summary of Refinements & Decisions:**
- **Validation Boundaries:** Preflight owns deterministic checks (capability existence, schema compatibility, topology, knowledge). Runtime owns dynamic checks (credentials, session tokens, locks).
- **Governed Administrative Override (PO-DEC-004):** Overrides are governance actions (not validation logic branches). Allowed only via explicit `OverrideToken` authorized by Project Owner, justified, and immutably journaled.
- **Audit Identifiability:** Executions started under override remain permanently marked in the `ExecutionJournal`.

**Approved Architectural Invariants:**
- `Invariant 4.1`: An execution plan SHALL NOT transition to `RUNNING` without passing Preflight plan validation, unless a governed administrative override has been authorized and journaled.
- `Invariant 4.2`: Preflight plan validation SHALL be side-effect free and strictly idempotent.
- `Invariant 4.3`: Non-deterministic checks (credentials, live network availability) SHALL NOT be evaluated in Preflight validation.
- `Invariant 4.4`: Every administrative override SHALL be explicitly authorized, justified, and recorded as an immutable event within the `ExecutionJournal`.

---

## 5. Spike 5: Durable Execution

### Evidence Status
** — Awaiting Project Owner Decision

### Summary
When should Context be refreshed before resuming? Should replay always be deterministic? The spike compared live-context resume vs strict checkpointed context.

### Key Findings
- Live context resume could invalidate the prior plan.
- Pinned context may use stale credentials.
- Replay must be strictly deterministic from the journal.
- Context Refresh Triggers are used when credentials change — a new journal entry is required.

### Recommendation
Adopt Alternative B with explicit Context Refresh Triggers. Replay is strictly deterministic. When credentials rotate, the suspension state requests a refresh via a new journal entry.

### Candidate Architectural Commitments
- Replay uses exactly the checkpointed execution journal and Execution Context.
- Context Refresh Trigger is atomic and journaled as a new entry.
- Suspension state must explicitly request a refresh — never implicit updates during resume.
- Checkpoints must include Execution Context, Execution Journal, and State Machine snapshot.

### Candidate Implementation Details
- Journal replay engine structure.
- Checkpoint frequency configuration.
- Context Refresh Trigger events schema.
- Resume validation logic.

### Candidate Open Questions / Edge Questions
- What is checkpoint frequency: per-action or per-execution step?
- Storage bloat from excessively granular journaling — requires compaction strategy (Edge Question, see Spike 1).
- How to detect stale credentials elegantly?

### Proposed Architectural Invariants
- Replay is always strictly deterministic from the journal.
- The execution state must never be created from live system state during resume.
- Context Refresh is always explicit and always journaled.

### Suggested ADR Mapping
- **ADR-0029** — DurableExecutionJournal.

### Project Owner Disposition
**Status:** ✅ Approved with Refinements (2026-07-28)

**Summary of Refinements & Decisions:**
- **Journal Sovereignty:** The `ExecutionJournal` is the sole authoritative source of truth for execution history, replay, and recovery.
- **Replay Boundaries:** Replay reconstructs execution exclusively from immutable journal records and deterministic artifacts (`CapabilitySnapshot`, `ExecutionContext`, `VirtualContextClock`). Replay SHALL NOT consult live external registries or mutable state.
- **Time Virtualization:** `VirtualContextClock` is the exclusive source of execution time; direct host system clock access is strictly prohibited.
- **Governed Context Refresh:** `ContextRefresh` operations are explicit, atomic, journaled, and performed prior to resuming execution.
- **Compaction Strategy (ED-0023-001):** Deferred as engineering debt; governed by the architectural constraint that compaction MUST NEVER compromise replay determinism or auditability.

**Approved Architectural Invariants:**
- `Invariant 5.1`: Replay execution SHALL be driven exclusively by the append-only `ExecutionJournal`.
- `Invariant 5.2`: Execution timestamps SHALL derive exclusively from the `VirtualContextClock`.
- `Invariant 5.3`: Context refresh operations SHALL be explicit, atomic, and journaled prior to resume.
- `Invariant 5.4`: Every replay SHALL produce identical execution decisions when provided with the same immutable journal and deterministic artifacts.
- `Invariant 5.5`: Replay SHALL NOT require live external dependencies to reconstruct historical execution state.

---

## 6. Spike 6: Replanning

### Evidence Status
[ ] — Awaiting Project Owner Decision

### Summary
What are the automatic replanning triggers and human intervention thresholds? The spike compared always-fail-on-error vs hybrid auto-replan limited by retry budget.

### Key Findings
- Capability Unavailability, Configuration Drift, and exhausted timeouts are auto-replanning triggers owned by Planner.
- Semantic changes and Permission Changes require human intervention (SUSPENDED state).
- Hybrid approach prevents infinite retry loops via retry budget.

### Recommendation
Adopt Alternative B (Hybrid Replanning). Workflow Engine delegates recoverable failures to the Planner via `ReplanningContext`.

### Candidate Architectural Commitments
- Planner owns `ReplanningContext` and replanning logic.
- Workflow Engine triggers replanning but does not alter plan design decisions.
- Hard retry budget cap — rebooting never consumed unbounded resources.

### Candidate Implementation Details
- ReplanningContext fields.
- Retry budget counter.
- Suspension policy triggers.

### Candidate Open Questions or Edge Questions
- Retry budget defaults — how should the budget be computed?
- Replan display to human approver UX.

### Proposed Architectural Invariants
- Replanning cannot silently modify the original plan intent.
- Retry budget is enforceable and measured.
- Human review thresholds are explicit and non-bypassable.

### Suggested ADR Mapping
- **ADR-0028** — Execution Lifecycle (covers replanning transition logic and retry budget).

### Project Owner Disposition
**Status:** ✅ Approved with Refinements (2026-07-28)

**Summary of Refinements & Decisions:**
- **Planner Delegation:** Workflow Engine detects failures and delegates replanning to the Planner Engine via an immutable `ReplanningContext`.
- **Intent Preservation:** Replanning SHALL preserve approved execution intent. Any structural or semantic change requires explicit human authorization (`SUSPENDED`).
- **Retry Budget Policy (PO-DEC-001):** Default of 3 automatic retries, configurable per execution class/template, with a platform hard cap of 10. Retry budget applies strictly to autonomous replanning (human approvals, administrative overrides, and manual restarts do NOT consume retry budget).
- **Artifact Preservation:** Autonomous replanning preserves existing deterministic execution artifacts unless a new planning cycle is explicitly authorized.

**Approved Architectural Invariants:**
- `Invariant 6.1`: Replanning SHALL NOT silently modify original plan intent or execution scope.
- `Invariant 6.2`: The retry budget SHALL be explicitly measured and capped; auto-replanning MUST NOT execute indefinitely.
- `Invariant 6.3`: Structural or semantic plan changes SHALL require explicit human authorization prior to resuming execution.
- `Invariant 6.4`: Every automatic replanning attempt SHALL be recorded as an immutable event in the `ExecutionJournal`, including the triggering condition and remaining retry budget.
- `Invariant 6.5`: Automatic replanning SHALL preserve deterministic execution artifacts unless a new planning cycle is explicitly authorized.

---

## 7. Spike 7 — Validation Boundaries

### Evidence Status
**Awaiting Project Owner Decision

### Summary
Distinguish Plan Validation, Preflight, Runtime Validation, and Post Execution Validation.

### Key Findings
- Plan Validation = Planner Engine
- Preflight = Resolver / Workflow
- Runtime Validation = Skill Framework
- Post-Execution = Validation Framework.
- No two phases validate the same property.

### Recommendation
Architecture must reject overlapping validations. Mapping above is binding.

### Candidate Architectural Commitments
- Validation phase ownership matrix as defined.
- No validation may span two phases.
- Each phase has a defined owner.

### Candidate Implementation Details
- Contract per validation phase.
- Error-aggregation format.
- Homogeneous phase hooks.

### Candidate Open Questions / Edge Questions
- Phase transition failure — does failure at one phase void subsequent phases?
- Custom post-execution validation approval process.

### Proposed Architectural Invariants
- Overlap at phase boundaries is prohibited.
- Failures include phase and owner metadata.

### ADR Mapping
- **ADR-0028** — Execution Lifecycle.

### Project Owner Disposition
**Status:** ✅ Approved with Refinements (2026-07-28)

**Summary of Refinements & Decisions:**
- **Strict 1:1 Mapping:** Every validation responsibility has exactly one authoritative owner and one execution phase. Shared or overlapping ownership is prohibited.
- **Zero Overlap & Upstream Trust:** Validation checks shall not be repeated across phases. Downstream phases SHALL trust successful upstream validation unless the underlying property has materially changed.
- **Structured Failure Events:** Validation failures emit structured, phase-attributed failure records (phase, owner, rule ID, execution ID, severity, deterministic reason code) recorded as typed execution events.
- **Validation Boundary Matrix:** Documented phase boundaries across Plan Validation (Planner), Preflight Validation (Resolver/Workflow), Runtime Validation (Skill/Workflow), and Post-Execution Validation (Validation Framework).

**Approved Architectural Invariants:**
- `Invariant 7.1`: Every validation check SHALL belong to exactly one validation phase.
- `Invariant 7.2`: Overlapping or duplicated validation across phase boundaries SHALL be strictly prohibited.
- `Invariant 7.3`: Validation failures SHALL emit structured, phase-attributed failure metadata including phase, owner, and contract identifier.
- `Invariant 7.4`: Downstream phases SHALL trust successful upstream validation unless the validated property has materially changed.
- `Invariant 7.5`: Validation phases SHALL execute in a strict lifecycle order and SHALL NOT execute out of sequence.

---

## 8. Spike 8 — Execution Determinism

### Evidence Status
** — Awaiting Project Owner Decision

### Summary
How is deterministic execution enforced? External dependency behavior pinned.

### Key Findings
- Virtual clock injection. `time.now()` is forbidden in Skills.
- LLM seed stored in journal.
- Dependency versions snapshotted.
- Skills implement idempotent semantics.

### Recommendation
Enforce Virtual Real‑Time Clock injection and Event Sourcing semantics in all Workflow artifacts.

### Candidate Architectural Commitments
- VirtualClock injection for timestamps.
- LLM seed/temperature stored in Execution Journal.
- External dependency versions snapshotted.
- Idempotent Skills enforced via contracts.

### Candidate Open Questions or Edge Debt
- Detection of `time.now()` (or equivalent) inside Skills.
- Non-deterministic third-party library risk.

### Proposed Architectural Invariants
- Time is always injected.
- Actions produce identical output on replay.

### ADR Mapping
- **ADR-0029** — Durable Execution Journal.

### Project Owner Disposition
**Status:** ✅ Approved with Refinements (2026-07-28)

**Summary of Refinements & Decisions:**
- **System Clock Elimination:** Runtime execution components SHALL NOT directly invoke host wall-clock APIs. All execution time is supplied exclusively through the `VirtualContextClock`.
- **Reproducible PRNG Seeding:** Pseudo-random behavior SHALL derive from a deterministic seeding strategy reproducible from immutable execution artifacts.
- **Serialized Async Event Queue:** Asynchronous execution branches MUST serialize state transitions through an ordered event queue before committing to the `ExecutionJournal`.
- **Observable Behavior Determinism:** Supported execution environments SHALL produce identical architecturally observable execution decisions and state transitions for identical deterministic inputs.

**Approved Architectural Invariants:**
- `Invariant 8.1`: Execution components SHALL NOT invoke non-deterministic platform functions directly.
- `Invariant 8.2`: Asynchronous execution SHALL be serialized before journal commits.
- `Invariant 8.3`: Replay SHALL reproduce identical architecturally observable execution decisions and state transitions from identical journal records and deterministic artifacts.
- `Invariant 8.4`: Every deterministic execution input SHALL originate from immutable artifacts or explicitly journaled events.
- `Invariant 8.5`: Runtime scheduling order SHALL NOT influence architecturally observable execution outcomes.

---

# Cross-Cutting Principles

1. **Determinism over Convenience** —
2. **Journal sovereignty** —
3. **Phase boundary integrity** —
4. **Read-only Planner** —

---

# 9. Consolidated ADR Mapping

| ADR | Proposed Title | Spikes Covered |
|------|----------------|----------------|
| ADR-0027 | Capability Planning and Feasibility Architecture | Spike 2, Spike 4 |
| ADR-0028 | Execution Runtime Lifecycle | Spike 1, Spike 3, Spike 6, Spike 7 |
| ADR-0029 | Durable Execution Journal | Spike 5, Spike 8 |

---

## ADR Structuring Recommendation

- **ADR-0027** first (Capability Snapshot + Feasibility).
- **ADR-0028** next (Execution state machine, validation boundaries, replanning triggers).
- **ADR-0029** last (Execution Journal, Virtual Clock, replay, idempotency).

Order is sequential.

---

# 10. Deferred Engineering Debt

| Debt ID | Name | Severity | Blocking? | Resolution Plan | Owning Spike |
|---------|------|----------|-----------|-----------------|--------------|
| ED-0023-001 | Execution Journal Compaction Strategy | Medium | No | Design archiving policy in ADR-0029 | Spike 1 |
| ED-0023-002 | External Dep Non-determinism | Low | No | Capture in dependency version snapshot | Spike 8 |
| ED-0023-003 | `time.now()` detection mechanism | Low | No | Build static analysis rule | Spike 8 |

---

# 11. Questions Requiring Project Owner Decisions

The following require explicit Project Owner decision as part of this review:

### PO-DEC-001: Retry Budget Defaults
**Status:** RESOLVED (2026-07-28)
- **Platform Default:** 3 automatic replanning attempts.
- **Override:** Configurable per execution class or plan template (hard platform cap of 10).
- **Accounting Rule:** Applies strictly to autonomous replanning; human approvals, administrative overrides, and manual restarts do NOT consume retry budget.

### PO-DEC-002: Suspended Max Duration
**Status:** RESOLVED (2026-07-28)
- **Default Timeout:** 7 days.
- **Override:** Configurable per execution class (every execution class MUST define a timeout policy).
- **Expiration Outcome:** Transition to state `CANCELLED` with cancellation reason `EXPIRED`.

### PO-DEC-003: Execution Context Retention Policy
**Status:** RESOLVED (2026-07-28)
- **Default Retention:** 30 days.
- **Override:** Configurable by execution class and organizational policy.
- **Purge Mechanics:** `ExecutionContext` archived/purged per policy; `ExecutionJournal` remains permanent.

### PO-DEC-004: Preflight Validation Override
**Status:** RESOLVED (2026-07-28)
- **Policy:** Governed Administrative Override (Governance Action).
- **Mechanism:** Explicit `OverrideToken` with Project Owner authorization & required justification.
- **Audit Trail:** Immutably recorded in `ExecutionJournal`.

### PO-DEC-005: ADR Authoring Sequence & Review Package Freeze
**Status:** RESOLVED (2026-07-28)
- **Approved ADR Sequence:** ADR-0027 (Capability Planning) → ADR-0028 (Execution Runtime Lifecycle) → ADR-0029 (Durable Execution Journal).
- **Review Package Status:** FROZEN. The EQ-0023 Architecture Review is complete and immutable. Formal ADR authoring is authorized.

---

## 12. Final Recommendation & Next Steps

1. Project Owner to review and decide on PO-DEC-001 through PO-DEC-005.
2. Author and freeze ADR-0027 first — Capability Snapshot + Feasibility Architecture.
3. ADR-0028 (Execution Lifecycle, state machine, replay triggers, validation boundaries) next.
4. ADR-0029 (Execution Journal, Virtual Clock, replay, idempotency) last.
5. After ADR approval: implementation Spike (Execution State Machine serialization) as initial implementation.
6. Update Workflow, Planner, and Validation documentation under approved ADRs.

No code commit until ADR-0027 accepted.

---

## Compliance Review

Architecture Compliance: PASS
Repository Boundary Verification: PASS
Documentation Placement: PASS
Knowledge Boundary: PASS
Repository Drift Detection: PASS
Destructive Operations: NONE

---

END OF EQ-0023 PO REVIEW PACKAGE