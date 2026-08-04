# ADR-0029: Durable Execution Journal Architecture

**Status:** FROZEN
**Frozen Date:** 2026-07-28
**Date:** 2026-07-28
**Authors:** Architecture Workstream
**Related Reviews:** EQ-0023 (Spikes 5 & 8)
**Prerequisites:** ADR-0027, ADR-0028

---

## Context & Problem Statement

The Jarvis Execution Runtime must survive process crashes, host restarts, and distributed execution nodes while maintaining strict determinism. Without a governing architecture for state persistence, clock virtualization, and concurrency serialization, execution replay can diverge from original runs due to wall-clock calls, unseeded randomness, or race conditions in asynchronous branches.

This ADR codifies the durable execution journal architecture, deterministic replay boundaries, time virtualization, context refresh governance, and non-deterministic input elimination as approved by the Project Owner in the frozen EQ-0023 Architecture Review.

---

## Decision Drivers

- Execution state must survive platform restarts: no in-memory state.
- Replay must produce bit-identical architecturally observable decisions from identical inputs.
- Host wall-clock access must be eliminated from runtime execution components.
- Asynchronous concurrency must not influence replayability.
- Journal compaction must never compromise determinism or auditability.

---

## Architectural Commitments & Decisions

### 1. Journal Sovereignty (Spike 5)

The `ExecutionJournal` is the **sole authoritative source of truth** for execution history, state transitions, replay, and recovery.

- All execution state transitions are append-only to the journal.
- State recovery MUST NEVER reconstruct execution state from mutable runtime objects or live services.
- The journal simultaneously acts as the WAL (write-ahead log), audit trail, and replay source.
- Journal writes are ordered events — commit ordering is execution ordering.

### 2. Deterministic Replay Boundaries (Spike 5)

Replay executes exclusively from four immutable artifacts:

| Artifact | Purpose |
|----------|---------|
| `ExecutionJournal` | Ordered event log; state transitions, triggers, refresh records |
| `CapabilitySnapshot` | Immutable capability state at plan initiation |
| `ExecutionContext` | Checkpointed execution variables, secrets scope hashes |
| `VirtualContextClock` | Deterministic time source |

**Replay SHALL NOT** consult:
- Live capability registries
- Current workspace or conversation context
- Host wall-clock / system time APIs
- External mutable state or services

### 3. Time Virtualization — VirtualContextClock (Spike 5)

All execution timestamps derive exclusively from an injected `VirtualContextClock`.

- Direct host wall-clock/gate clock access (`time.now()`, `System.currentTimeMillis()`, etc.) is **strictly prohibited** within all execution components, Skills, and validation frameworks.
- The `VirtualContextClock` ensures identical timestamps during replay.
- Clock resolution and drift behavior are defined at platform_init-time and held constant per execution.

### 4. Governed Context Refresh (Spike 5)

Environments change (credential rotations, DNS updates, rolling upgrades). Context refresh is explicit, atomic, and part of replay history.

**ContextRefresh Mechanics:**
- A `ContextRefresh` operation is an **atomic journal entry**.
- It is performed **prior** to resuming execution from a `SUSPENDED` state.
- It becomes a permanent event in the replay stream.
- Implicit, non-journaled refreshes are forbidden.

Example lifecycle flow:
```
Suspend → ContextRefresh (journaled) → Resume execution
```

### 5. Execution Determinism & Concurrency (Spike 8)

**Deterministic Randomness:**
All pseudo-random behavior during execution is derived from a **deterministic PRNG** seeded by `execution_id` and step position/branch identity. This ensures random/chance-based decisions are reproducible.

**Serialized Async Event Queue:**
Asynchronous execution branches **MUST** serialize their state transitions through a deterministic, ordered serialized commit queue before entries are written to the `ExecutionJournal`. This removes scheduling jitter and thread interleaving from the replayable history.

**Observable Outcome Determinism:**
Every supported execution environment SHALL produce **identical architecturally observable execution decisions and state transitions** for identical deterministic inputs. Bit-different floating-point or internal representation differences that do not change architectural decisions are outside the scope; architecture decisions must match exactly.

### 6. Compaction Strategy Policy (ED-0023-001 — Deferred)

Append-only journals grow unbounded. Compaction is a known engineering debt item.

Governance rule:
```
Compaction strategies SHALL NOT compromise deterministic-replay capability or audit integrity under any circumstances.
```

Compaction algorithm design (snapshotting, log truncation, archival tiers) is deferred to implementation scope and must pass replay compliance validation before acceptance.

---

## Architectural Invariants

### Durable Execution Invariants (from Spike 5)
- **Invariant 5.1:** Replay execution SHALL be driven exclusively by the append-only `ExecutionJournal`.
- **Invariant 5.2:** Execution timestamps SHALL derive exclusively from the `VirtualContextClock`.
- **Invariant 5.3:** Context refresh operations SHALL be explicit, atomic, and journaled prior to resume.
- **Invariant 5.4:** Every replay SHALL produce identical execution decisions when provided with the same consistent journal and deterministic artifacts.
- **Invariant 5.5:** Replay SHALL NOT require live external dependencies to reconstruct historical execution state.

### Execution Determinism Invariants (from Spike 8)
- **Invariant 8.1:** Execution components SHALL NOT invoke non-deterministic platform functions directly.
- **Invariant 8.2:** Asynchronous execution SHALL be serialized before journal commit.
- **Invariant 8.3:** Replay SHALL reproduce identical architecturally observable execution decisions and state transitions from identical journal records and deterministic artifacts.
- **Invariant 8.4:** Every deterministic execution input SHALL originate from immutable artifacts or explicitly journaled events.
- **Invariant 8.5:** Runtime scheduling order SHALL NOT influence architecturally observable execution outcomes.

**Total Invariants:** 10

---

## Resolved PO Decisions

| PO-DEC | Topic | Resolution |
|--------|-------|------------|
| PO-DEC-005 | ADR Sequence & Freeze | ADR-0027 → ADR-0028 → ADR-0029, EQ-0023 frozen |

---

## Consequences

### Positive
- **Deterministic replay**: Exchange host restarts guarantee identical execution outcomes.
- **Virtualized time**: Elimination of timezone/drift/clock-skew replay bugs.
- **Async determinism**: Concurrency artifacts such as "heisenbugs" are eliminated by serialized event queue ordering.
- **Verifiable context freshness**: Atomic, journaled context refresh operations prevent implicit mutation.

### Negative
- **Storage overhead**: Append-process journal grows linearly with execution step count.
- **Serialization latency**: Async event queue serialization adds overhead to parallel execution.
- **Tight coupling on VirtualClock**: Any corruption of the virtual clock breaks replay for all journaled events.

---

## Deferred Engineering Debt

| Debt ID | Description | Target Resolution |
|--------|-------------|--------------------|
| ED-0023-001 | Execution Journal compaction/archiving strategy | Deferred to future implementation. Any implementation shall preserve replay determinism and auditability. |
| ED-0023-002 | External dependency non-determinism detection — dependency version pinning | External dependency snapshot design | 
| ED-0023-003 | `time.now()` detection mechanism in component gates | Static analysis; runtime checker | 

---

## References

- EQ-0023: Execution Runtime Architecture (`docs/engineering/questions/EQ-0023_Execution_Runtime_Architecture.md`)
- EQ-0023 Project Owner Review (`docs/architecture/reviews/EQ-0023_Project_Owner_Review.md`)
- ADR-0027: Capability Planning and Feasibility Architecture
- ADR-0028: Execution Runtime Lifecycle Architecture

---

## Decision

APPROVE and ADOPT the Durable Execution Journal Architecture as specified, including all 10 execution invariants, governed context refresh policy, and 3 deferred implementation items.

---

## Compliance

Architecture Compliance: PASS
Repository Boundary: PASS
EQ-0023 Traceability: PASS