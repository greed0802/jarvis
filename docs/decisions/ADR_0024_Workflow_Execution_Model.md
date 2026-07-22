# ADR_0024_Workflow_Execution_Model

# Status

Accepted

---

# Context

The Jarvis Platform separates runtime responsibilities across three Core Runtime Engines:

- Context Engine
- Planner Engine
- Workflow Engine

Previous ADRs established:

- The Context Engine owns Context and Intent (ADR_0022).
- The Planner Engine owns Plans (ADR_0005, ADR_0022).
- The Workflow Engine owns Workflows and Tasks (ADR_0013).

However, the execution behavior of the Workflow Engine—including task scheduling, retries, cancellation, context refresh, and replanning—had not been explicitly ratified.

This ADR establishes the Workflow Execution Model as the authoritative execution architecture.

---

# Decision

The Workflow Engine is the exclusive execution coordinator within the Jarvis Platform.

It transforms an approved Plan into an executable Workflow, creates and manages Tasks, coordinates execution through Skills, monitors progress, and determines whether execution should continue, retry, refresh Context, or request replanning.

Execution authority belongs exclusively to the Workflow Engine.

---

# Execution Responsibilities

The Workflow Engine is responsible for:

- Creating Workflows
- Creating Tasks
- Scheduling execution
- Managing task dependencies
- Coordinating sequential execution
- Coordinating parallel execution
- Coordinating conditional execution
- Tracking execution progress
- Managing retries
- Managing timeouts
- Supporting pause and resume
- Supporting cancellation
- Maintaining execution state
- Requesting Context refresh
- Requesting replanning from the Planner Engine

---

# Task Ownership

Every Task belongs to exactly one Workflow.

Tasks never exist independently.

Tasks never coordinate one another.

Tasks never create additional Tasks.

The Workflow Engine owns the complete Task lifecycle.

---

# Execution Authority

The Workflow Engine determines:

- when a Task begins
- when a Task is retried
- when execution pauses
- when execution resumes
- when execution is cancelled
- when Context should be refreshed
- when replanning should occur

No Skill or Framework may make these decisions independently.

---

# Skill Responsibilities

Skills perform work.

Skills never:

- coordinate execution
- schedule Tasks
- retry Tasks
- refresh Context
- request replanning
- modify Plans
- modify Workflows

Skills report execution results back to the Workflow Engine.

---

# Validation Responsibilities

The Validation Framework evaluates execution outputs.

Validation may provide:

- success
- failure
- warnings
- confidence
- recommendations

The Validation Framework never:

- retries Tasks
- refreshes Context
- requests replanning
- modifies Workflows

Validation communicates only with the Workflow Engine.

---

# Context Refresh

Context refresh is initiated only by the Workflow Engine.

Typical refresh points include:

- Task completion
- Workflow checkpoints
- Explicit user clarification
- Significant execution changes
- Validation feedback requiring additional understanding

Context is never refreshed autonomously during active Task execution.

---

# Replanning

When execution can no longer safely continue, the Workflow Engine requests replanning from the Planner Engine.

Typical reasons include:

- repeated Task failures
- invalid assumptions
- unavailable Resources
- changed user objectives
- execution deadlock
- unrecoverable dependency failures

The Workflow Engine never creates or modifies Plans.

Only the Planner Engine owns Plans.

---

# Execution Lifecycle

```text
Approved Plan
        │
        ▼
Workflow Created
        │
        ▼
Tasks Created
        │
        ▼
Task Execution
        │
        ▼
Validation
        │
        ▼
Workflow Decision
        ├──────── Continue
        ├──────── Retry
        ├──────── Refresh Context
        └──────── Request Replanning
```

---

# Information Ownership

| Information | Owner |
|--------------|----------------|
| Plan | Planner Engine |
| Workflow | Workflow Engine |
| Task | Workflow Engine |
| Execution State | Workflow Engine |
| Progress | Workflow Engine |
| Result References | Workflow Engine |

---

# Rationale

Separating execution coordination from planning preserves deterministic behavior and prevents responsibility overlap.

The Planner Engine determines strategy.

The Workflow Engine executes strategy.

Skills perform work.

Validation evaluates work.

This separation ensures that execution decisions originate from a single authoritative component, improving traceability, explainability, recovery, and maintainability.

---

# Consequences

## Positive

- Single authority for execution decisions.
- Deterministic execution lifecycle.
- Clear separation of planning and execution.
- Simplified retry and recovery behavior.
- Improved observability and auditing.
- Consistent execution across all Skills.

## Negative

- Workflow Engine becomes the central execution coordinator.
- Additional coordination logic is concentrated within a single runtime component.

These trade-offs are accepted in favor of architectural clarity and deterministic execution.

---

# Human Authority

The Workflow Engine coordinates execution on behalf of the user.

User-initiated execution commands always take precedence over autonomous execution decisions.

The Workflow Engine shall immediately honor user requests to:

- Pause execution
- Resume execution
- Cancel execution

The Workflow Engine may autonomously:

- Retry Tasks
- Continue execution
- Refresh Context
- Request replanning

The Workflow Engine may pause execution autonomously only when required to preserve platform safety, data integrity, or architectural policy.

Autonomous cancellation shall occur only when execution cannot safely continue or when explicitly required by platform policy.

Whenever execution is paused or cancelled autonomously, the Workflow Engine shall record the reason and notify the user.

The Workflow Engine shall never override an explicit user decision.

This operationalizes the Human-Always-in-Control principle established by ADR_0010.

---

# Related Documents

- 05_Data_Flow.md
- 08_Workflow_Engine.md
- docs/ontology/core/workflow.md
- docs/ontology/core/task.md

---

# Related ADRs

- ADR_0005_Deterministic_Planner
- ADR_0009_Skill_Architecture
- ADR_0010_Human_Control
- ADR_0013_Workflow_Ownership
- ADR_0014_Workflow_Determinism
- ADR_0020_Runtime_vs_Cross_Cutting_Architecture
- ADR_0021_Control_Plane_and_Data_Plane_Separation
- ADR_0022_Context_Lifecycle_and_Ownership
- ADR_0023_Capability_Discovery_and_Resolution