# ====================================================
# ENGINEERING DISCOVERY SPRINT
# EQ-0023 — EXECUTION RUNTIME ARCHITECTURE
# ====================================================

## Governance Note

This investigation was originally filed as EQ-0019 (Execution Runtime Architecture) during the early governance era. During the Repository Governance Harmonization Sprint (2026-07-28), it was renumbered to EQ-0023 to resolve a collision with the permanently frozen EQ-0019 (BOQ Semantic Intelligence Increment 1). The investigation content and conclusions remain unchanged.

## 1. Executive Summary

This Engineering Question (EQ-0023) investigates the Execution Runtime Architecture for the Jarvis platform for the upcoming Capability Era. The investigation focuses on how Jarvis executes work deterministically via the Workflow Engine while satisfying the architectural mandates for durability, restartability, separate validation and planning boundaries, and clear lifecycle ownership. No production runtime changes were made during this sprint. The findings provide the blueprint and ADR candidates required before implementation begins.

## 2. Spike Results

### Spike 1: Execution Lifecycle

#### Problem
How should the execution lifecycle be modeled to support deterministic execution, human-in-the-loop approvals, and clear terminal states?

#### Evidence
According to `docs/08_Workflow_Engine.md` and standard durable execution patterns, executions often require suspension points for approvals or missing resources. A state machine must safely capture these states without blocking system resources.

#### Execution State Machine
Valid transitions and states:
- `PENDING`: Plan accepted, waiting for resources.
- `RUNNING`: Execution actively progressing.
- `SUSPENDED`: Execution paused. Sub-states include `WAITING_APPROVAL`, `WAITING_RESOURCES`, `WAITING_DEPENDENCY`.
- `COMPLETED` (Terminal): Successful completion.
- `FAILED` (Terminal): Error requiring intervention.
- `CANCELLED` (Terminal): Manually terminated or aborted.

#### Alternatives
- **Alternative A:** In-memory synchronous thread blocking.
- **Alternative B:** Durable Event-Sourced State Machine via Workflow Engine.

#### Trade-offs
In-memory blocking cannot survive platform restarts and consumes active compute while waiting for human input. A durable state machine adds write latency but ensures restartability.

#### Recommendation
Adopt **Alternative B**. The Workflow Engine must own the Execution State Machine and serialize wait states to an Execution Journal.

#### Confidence
High.

---

### Spike 2: Capability Planning

#### Problem
Should the Planner have read-only access to capabilities? How is feasibility represented, and what belongs in a Capability Snapshot?

#### Evidence
`docs/07_Planner_Engine.md` establishes that the Planner decides *what* to do based on Context without executing it.

#### Capability Snapshot Proposal
A point-in-time immutable record of available platforms/tools at the moment of plan creation. Fields: `timestamp`, `capability_versions`, `feasibility_matrix`.

#### Alternatives
- **Alternative A:** Live capabilities discovery during planning.
- **Alternative B:** Immutable Capability Snapshot injected into Context.

#### Trade-offs
Live reads may cause race conditions if capabilities upgrade or degrade during the planning window. Snapshots guarantee plan determinism.

#### Recommendation
Adopt **Alternative B** (Snapshot). Feasibility is a boolean matrix of constraints vs. requirements. Planner has strict read-only access.

#### Confidence
High.

---

### Spike 3: Execution Context

#### Problem
Should the Execution Context exist separately from Workspace/Conversation Context? What are its responsibilities?

#### Evidence
The Context Engine (`docs/06_Context_Engine.md`) separates contexts to avoid state pollution and execution drift.

#### Execution Context Proposal
- **Responsibilities:** Store runtime variables, secrets scope, checkpoint references, and intermediate outputs.
- **Ownership:** Exclusively Workflow Engine during execution.
- **Minimal fields:** `execution_id`, `plan_ref`, `variables`, `secrets_scope_hash`, `virtual_clock_time`.

#### Alternatives
- **Alternative A:** Unified Global Context.
- **Alternative B:** Dedicated, isolated Execution Context.

#### Trade-offs
Shared context allows easy data passing but introduces extreme risks of mutation during long-running tasks.

#### Recommendation
Adopt **Alternative B**. Copy minimal required subset of Workspace Context into an isolated Execution Context.

#### Confidence
High.

---

### Spike 4: Plan Validation

#### Problem
What constitutes deterministic plan validation and what are the boundaries?

#### Evidence
`docs/14_Validation_Framework.md` dictates that validations must be reproducible.

#### Validation Matrix
| Requirement | Boundary Phase | Deterministic? |
|-------------|----------------|----------------|
| Capability Exists | PREFLIGHT | Yes |
| Schema Compatible | PREFLIGHT | Yes |
| Dependencies Satisfied | PREFLIGHT | Yes |
| Knowledge Availability | PREFLIGHT | Yes |
| Credentials/Permissions | RUNTIME | No (Can fail if revoked mid-flight) |

#### Alternatives
- **Alternative A:** Lazy validation (evaluate just-in-time).
- **Alternative B:** Strict Preflight Verification before state `RUNNING`.

#### Trade-offs
Lazy validation reduces startup latency but increases risk of mid-execution crashes. Preflight is safer but adds absolute processing time.

#### Recommendation
Adopt **Alternative B**. All deterministic checks (Capability, Schema, Dependencies) must pass Preflight Plan Validation.

#### Confidence
High.

---

### Spike 5: Durable Execution

#### Problem
When must Context be refreshed before resuming? Should replay always be deterministic?

#### Evidence
Durable executions require checkpointing. Replaying must behave exactly as the first execution.

#### Alternatives
- **Alternative A:** Resume uses live context.
- **Alternative B:** Resume strictly uses checkpointed context.

#### Trade-offs
Live context might invalidate the prior plan. Pinned context might use stale credentials.

#### Recommendation
Adopt **Alternative B** with a mechanism for `Context Refresh Triggers`. Replay is strictly deterministic from the journal. If credentials rotate, the suspension state must explicitly request a refresh which logs as a new journal entry.

#### Confidence
Medium-High.

---

### Spike 6: Replanning

#### Problem
What are the automatic replanning triggers and human intervention thresholds?

#### Evidence
The Planner owns Replanning logic. The Workflow Engine requests it.

#### Replanning Decision Matrix
| Trigger Event | Action | Ownership |
|---------------|--------|-----------|
| Capability Unavailable | Auto-Replan | Planner |
| Configuration Drift | Auto-Replan | Planner |
| Timeouts (Retry maxed) | Auto-Replan | Planner |
| Dependency Semantic Change | Suspend / Human | Platform Kernel |
| Permission Changes | Suspend / Human | Platform Kernel |

#### Alternatives
- **Alternative A:** Always fail on error, wait for human.
- **Alternative B:** Agentic auto-replan limited by a retry budget.

#### Trade-offs
Auto-replanning consumes token budgets/compute but provides autonomy. Always failing is safe but not agentic.

#### Recommendation
Adopt **Alternative B**, hybrid Replanning. The Workflow Engine delegates recoverable failures to the Planner using a `ReplanningContext`.

#### Confidence
High.

---

### Spike 7: Validation Boundaries

#### Problem
Distinguish Plan Validation, Preflight, Runtime Validation, and Post Execution Validation.

#### Validation Boundary Matrix
| Boundary Phase | Owner | Goal |
|----------------|-------|------|
| Plan Validation | Planner Engine | Verify plan grammar, strategy, and risk. |
| Preflight | Resolver / Workflow | Verify structural feasibility (schemas, nodes). |
| Runtime Validation | Skill Framework | Evaluate Skill payloads and intermediate results. |
| Post-Execution | Validation Framework | Verify system invariant compliance and final output contracts. |

#### Recommendation
The architecture must firmly reject overlapping validations. Ownership mapping above is final.

#### Confidence
High.

---

### Spike 8: Execution Determinism

#### Problem
How is deterministic execution enforced and external dependency behavior pinned?

#### Evidence
Platform Principle: Determinism over Convenience. Identical inputs → Identical outputs.

#### Execution Determinism Principles
1. **Time Pinned:** Time must be injected via a `VirtualContextClock`. `time.now()` is forbidden in Skills.
2. **AI Isolation:** LLM seed logic must be written to the Execution Journal for replayability.
3. **External Dependencies:** Versions of external packages/systems are snapshotted in `Execution Context`.
4. **Idempotency:** Skills must implement idempotent semantics; rerunning a skill block via journal must yield the same output.

#### Recommendation
Enforce Virtual Clock injection and Event Sourcing semantics in all Workflow Engine artifacts.

#### Confidence
High.

---

## 3. Architectural Findings
Execution in the Capability Era demands a hard separation between strategy (Planner) and stateful execution (Workflow). Evidence points towards requiring an Event-Sourced / Durable Execution pipeline. We cannot safely suspend and wait for human approval in a simple asynchronous call without violating system stability and recovery architecture.

## 4. Alternative Comparison Matrix

| Approach | Scalability | Determinism | Replayability | Implementation Cost | Alignment to Principles |
|----------|-------------|-------------|---------------|---------------------|-------------------------|
| Synchronous Execution | Low | Low | No | Low | Failing (No Durable State) |
| Basic Async Queues | Med | Low | Partial | Med | Low-Medium |
| **Durable Execution Journal** | **High** | **High** | **Yes** | **High** | **Exact match (Recommended)** |

## 5. Recommended Next Steps
1. Formalize ADR-0027, ADR-0028, and ADR-0029.
2. Conduct an implementation Spike focusing purely on the `Execution State Machine` serialization.
3. Create the `Execution Context` interface contract.
4. Update `08_Workflow_Engine.md` and `07_Planner_Engine.md` with boundary decisions based on ADR approval.

## 6. ADR Candidates
### ADR-0027 Capability Planning and Feasibility Architecture
Defines how Capabilities are snapshotted for the Planner Engine and Feasibility representation in Planning Context.

### ADR-0028 Execution Runtime Lifecycle
Defines the PENDING → RUNNING → SUSPENDED → TERMINAL state machine.

### ADR-0029 Durable Execution Journal
Defines the append-only log architecture required for Virtual Clocks, replayability, and execution persistence.

## 7. Implementation Readiness Assessment
**Verdict: NOT READY FOR CODE IMPLEMENTATION.**
- The conceptual boundaries are proven in this document.
- Formal ADRs must be authored and accepted by the Project Owner.
- Data structures (Schemas) for the Execution Journal remain undefined.

## 8. Confidence Assessment
Overall Architecture Confidence: **High**.
Risk area is primarily around the volume of data stored in `Execution Journal` causing bloat. A compaction or archiving strategy will be needed (Open Question).

---

## REPOSITORY QUALITY GATE

Architecture Compliance: PASS
Repository Boundary Verification: PASS
Documentation Placement Verification: PASS
Knowledge Boundary Verification: PASS
Repository Drift Detection: PASS
Destructive Operations: NONE
Files Created: `docs/engineering/EQ-0023_Execution_Runtime_Architecture.md`
Files Modified: None
Engineering Debt: Low (Wait for Journal Compaction strategy)
Risks Remaining: Data bloat from granular durability.

**Recommendation:**
[x] Continue
[x] ADR Required (Author ADR 27, 28, 29)