# Object: Task

Category:
Core / Execution

---

# Definition

A Task is the smallest executable unit of work within the Jarvis Platform.

A Task represents a specific unit of work required to execute part of an approved Plan.

Tasks are created and owned by a Workflow.

Tasks reference one or more Capabilities and are fulfilled through Skills.

---

# Purpose

The Task exists to decompose Workflow execution into discrete, executable units of work.

Each Task represents a single operation that can be requested, executed, validated, and completed independently.

Tasks enable the Workflow Engine to coordinate complex execution while maintaining control over execution order, dependencies, progress, retries, and recovery.

A Task should be independently executable.

Given the required Context, Resources, and Capability, a Task should be able to complete without knowledge of the broader Workflow strategy.

---

# Guiding Principle

A Task answers one question:

> **"What specific work must be completed right now?"**

---

# Ownership

Tasks are owned exclusively by the Workflow that created them.

| Owner | Responsibility |
|--------|----------------|
| Workflow Engine | Creates, owns, schedules, and manages the Task lifecycle |
| Skill | Executes the Task |
| Validation Framework | Evaluates Task outputs |

The Planner Engine never owns or directly manages Tasks.

---

# Lifecycle

```text
Created
      │
      ▼
Queued
      │
      ▼
Resolved
      │
      ▼
Executing
      │
      ▼
Completed

or

Failed

or

Cancelled
```

Lifecycle states:

- **Created** — The Workflow creates the Task from an approved Plan.
- **Queued** — Waiting for execution.
- **Resolved** — The required Capability has been resolved to an appropriate Skill implementation.
- **Executing** — The selected Skill is performing the work.
- **Completed** — Execution finished successfully.
- **Failed** — Execution could not be completed successfully.
- **Cancelled** — Execution was intentionally stopped.

---

# Task Composition

A Task may contain:

- Identifier
- Name
- Description
- Capability reference
- Input references
- Parameters
- Dependencies
- Constraints
- Priority
- Execution State
- Execution Metadata
- Timeout
- Retry Policy

Task composition describes execution requirements rather than implementation details.

---

# Execution Modes

A Task may execute:

- Sequentially
- In Parallel
- Conditionally
- After prerequisite Tasks
- With configured Retry Policies

Execution mode is determined exclusively by the Workflow Engine.

---

# Relationships

```text
Plan
      │
      ▼
Workflow
      │
      ▼
Task
      │
      ▼
Capability
      │
      ▼
Capability Registry
      │
      ▼
Capability Resolver
      │
      ▼
Skill
      │
      ▼
Result
```

Relationship summary:

- A Plan contains one or more Tasks.
- A Workflow owns and coordinates its Tasks.
- A Task requests one or more Capabilities.
- The Capability Registry discovers compatible Skill implementations.
- The Capability Resolver selects the appropriate Skill implementation.
- Skills execute the Task.
- Skill execution produces Results.

---

# Task is NOT

A Task is not:

- A Plan
- A Workflow
- A Capability
- A Skill
- A Result

A Task never:

- Creates Plans
- Coordinates other Tasks
- Selects Skill implementations
- Executes Capabilities
- Owns Context
- Owns Knowledge
- Owns Memory
- Produces Results independently

Execution is performed by Skills under Workflow coordination.

---

# Failure Handling

When a Task cannot complete successfully:

1. The Workflow Engine evaluates the failure.
2. Retry policies are applied when appropriate.
3. Alternative Capability resolution may be attempted.
4. The Workflow Engine may request replanning from the Planner Engine.
5. The user may be notified when required.

The Task itself never decides how failures are handled.

Failure management belongs exclusively to the Workflow Engine.

---

# Information Boundaries

## Information entering a Task

- Workflow reference
- Capability reference
- Context reference
- Input references
- Parameters
- Dependencies
- Constraints

## Information produced by a Task

- Execution Status
- Execution Outcome
- Execution Metadata
- Result reference

## Information that never belongs to a Task

- Intent
- Context ownership
- Plans
- Workflows
- Skill implementations
- Knowledge
- Memory
- Platform configuration

---

# Golden Rule

A Task defines one executable unit of work.

It never decides strategy.

It never performs execution.

It never coordinates the broader Workflow.

---

# Guiding Principle

Plans define **what must be accomplished**.

Workflows determine **when Tasks execute**.

Tasks define **one executable unit of work**.

Capabilities define **what operation is required**.

Skills define **how the operation is performed**.

---

# Related Documents

- 05_Data_Flow.md
- 07_Planner_Engine.md
- 08_Workflow_Engine.md
- docs/ontology/core/workflow.md
- docs/ontology/core/capability.md
- docs/ontology/core/result.md

---

# Related ADRs

- ADR_0009 — Skill Architecture
- ADR_0013 — Workflow Ownership
- ADR_0014 — Workflow Determinism
- ADR_0023 — Capability Discovery and Resolution