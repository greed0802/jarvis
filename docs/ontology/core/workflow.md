# Object: Workflow

Category:
Core / Execution

---

# Definition

A Workflow is the execution structure that coordinates the implementation of an approved Plan.

A Workflow transforms an approved Plan into one or more executable Tasks and manages their execution from creation through completion.

A Workflow never determines strategy.

It coordinates execution.

---

# Purpose

The Workflow exists to bridge planning and execution.

After the Planner Engine produces an approved Plan, the Workflow Engine instantiates a Workflow that owns, schedules, and coordinates the Tasks required to accomplish that Plan.

The Workflow ensures execution remains deterministic, observable, recoverable, and aligned with the approved strategy.

---

# Workflow Answers

> **"How should the approved Plan be executed?"**

Not

> **"What should be done?"**

---

# Workflow Does

A Workflow:

- Owns Tasks
- Coordinates execution
- Schedules Tasks
- Manages dependencies
- Monitors execution progress
- Applies retry policies
- Supports pause and resume
- Coordinates cancellation
- Requests Context refresh
- Requests replanning when required
- Collects execution Results

---

# Workflow Does NOT

A Workflow never:

- Interpret Intent
- Build Context
- Produce Plans
- Select Skill implementations
- Execute Skills
- Validate Results
- Promote Knowledge

Execution is performed by Skills.

Validation belongs to the Validation Framework.

Planning belongs to the Planner Engine.

---

# Workflow Composition

A Workflow may contain:

- Identifier
- Approved Plan reference
- Task collection
- Execution State
- Scheduling policy
- Dependency graph
- Retry policy
- Progress information
- Execution history
- Result references

---

# Workflow Lifecycle

```text
Created
      │
      ▼
Prepared
      │
      ▼
Executing
      │
      ▼
Paused
      │
      ▼
Resumed
      │
      ▼
Completed

or

Cancelled

or

Failed
```

---

# Task Management

A Workflow owns one or more Tasks.

Tasks may execute:

- Sequentially
- In Parallel
- Conditionally

The Workflow Engine determines execution order.

Tasks never coordinate one another.

---

# Context Refresh

The Workflow determines when Context should be refreshed.

Typical refresh points include:

- Task completion
- Workflow checkpoints
- User clarification
- Explicit replanning
- Validation feedback

Context is never refreshed autonomously during active Task execution.

---

# Replanning

When execution can no longer safely continue, the Workflow may request replanning from the Planner Engine.

Typical reasons include:

- Repeated Task failure
- Invalid assumptions
- Changed requirements
- Missing Resources
- Updated user objectives

The Workflow never creates new Plans.

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

---

# Information Boundaries

Workflow owns:

- Tasks
- Execution state
- Scheduling
- Dependencies
- Progress
- Retry policies
- Result references

Workflow never owns:

- Intent
- Context
- Plans
- Capabilities
- Skills
- Knowledge
- Memory

---

# Golden Rule

The Workflow coordinates execution.

It never decides strategy.

It never performs work.

---

# Guiding Principle

Plans define **what** should be accomplished.

Workflows coordinate **how execution proceeds**.

Tasks define **individual work**.

Skills perform the work.

---

# Related Documents

- 05_Data_Flow.md
- 07_Planner_Engine.md
- 08_Workflow_Engine.md
- docs/ontology/core/task.md
- docs/ontology/core/capability.md

---

# Related ADRs

- ADR_0013 — Workflow Ownership
- ADR_0014 — Workflow Determinism
- ADR_0022 — Context Lifecycle and Ownership
- ADR_0023 — Capability Discovery and Resolution