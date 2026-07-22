# ADR_0022 — Context Lifecycle and Ownership

Status: Accepted

Date: 2026-07-08

---

# Context

The Jarvis Platform defines the Context Engine as the first Core Runtime Engine of the Data Plane.

The Platform Kernel establishes the runtime environment, while the Context Engine provides the understanding required for planning and execution.

As the architecture evolved through `05_Data_Flow.md`, several cross-cutting questions emerged:

- Who owns Context?
- Who owns Intent?
- When is Context refreshed?
- Who requests a Context refresh?
- How do downstream runtime components consume Context?

Without explicit ownership, multiple runtime components could independently modify or refresh Context, resulting in inconsistent behavior and reduced determinism.

---

# Decision

The Context Engine is the sole owner of Context throughout its lifecycle.

The Context Engine is responsible for:

- Constructing Context
- Maintaining Context
- Refreshing Context when requested
- Interpreting and maintaining Intent
- Providing Context and Intent to downstream runtime components

The Context Engine does not perform planning, workflow orchestration, skill execution, or result generation.

---

# Context Lifecycle

The lifecycle of Context consists of:

1. Context Assembly
2. Context Evaluation
3. Context Availability
4. Context Refresh
5. Context Disposal

Context exists only for the lifetime of the current objective.

It is temporary and should not be treated as persistent storage.

Persistent information belongs to the appropriate Frameworks.

---

# Context Refresh

The Context Engine performs Context refreshes.

The Workflow Engine determines when a refresh should occur.

Typical refresh points include:

- Task completion
- User clarification
- Workflow checkpoints
- Explicit replanning
- Validation feedback

The Context Engine never refreshes Context autonomously during active task execution.

This preserves deterministic workflow execution.

---

# Intent Ownership

Intent is owned by the Context Engine.

The Context Engine interprets raw user requests into a structured Intent.

The Planner Engine consumes Intent but does not own or modify it.

The Workflow Engine executes approved Plans derived from that Intent.

---

# Information Ownership

| Information | Owner |
|------------|-------|
| Context | Context Engine |
| Intent | Context Engine |
| Plan | Planner Engine |
| Workflow | Workflow Engine |
| Task | Workflow Engine |
| Result | Workflow Execution |
| Memory | Memory Framework |
| Knowledge | Knowledge Framework |
| Resources | Resource Framework |

---

# Communication

The Context Engine provides Context and Intent through well-defined runtime interfaces.

Downstream runtime components consume Context but never directly modify it.

Requests to refresh Context are initiated by the Workflow Engine through defined runtime interfaces.

---

# Rationale

Separating ownership from orchestration preserves the single-responsibility principle.

The Context Engine specializes in understanding.

The Planner Engine specializes in decision making.

The Workflow Engine specializes in execution coordination.

This separation prevents hidden state changes during execution and maintains deterministic platform behavior.

---

# Consequences

Benefits:

- Single owner for Context
- Deterministic workflow execution
- Clear engine responsibilities
- Consistent runtime behavior
- Reduced coupling between runtime engines

Trade-offs:

- Workflow execution explicitly manages refresh timing.
- Context refresh requires coordination between runtime engines.
- Additional runtime interfaces are required between the Workflow Engine and Context Engine.

---

# Related Documents

- 03_Core_Ontology_Relationships.md
- 04_Platform_Kernel.md
- 05_Data_Flow.md
- 06_Context_Engine.md
- 07_Planner_Engine.md
- 08_Workflow_Engine.md

---

# Related ADRs

- ADR_0005 — Deterministic Planner
- ADR_0008 — Context
- ADR_0009 — Skill Architecture
- ADR_0013 — Workflow Ownership
- ADR_0014 — Workflow Determinism
- ADR_0020 — Runtime vs Cross-Cutting Architecture
- ADR_0021 — Control Plane and Data Plane Separation