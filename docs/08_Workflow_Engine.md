# Workflow Engine

Version: 1.0

---

# Definition

The Workflow Engine is the third Core Runtime Engine of the Jarvis Data Plane.

It transforms approved Plans into executable Workflows and coordinates their execution through Tasks.

The Workflow Engine manages execution.

It never performs the work itself.

---

# Purpose

The Workflow Engine exists to safely coordinate execution while preserving determinism, traceability, and human control.

It bridges planning and execution by managing Workflows, Tasks, execution state, retries, recovery, and progress.

---

# Scope

The Workflow Engine owns execution coordination.

It does not:

- Interpret Intent
- Build Context
- Produce Plans
- Execute Skills
- Validate Results
- Promote Knowledge

---

# Execution Philosophy

The Planner decides strategy.

The Workflow Engine coordinates execution.

Skills perform work.

Validation evaluates outputs.

Learning captures validated experience.

---

# Responsibilities

## Workflow Coordination

- Create Workflows
- Manage Workflow lifecycle
- Track execution progress
- Maintain execution state

## Task Management

- Create Tasks
- Schedule Tasks
- Manage dependencies
- Queue execution
- Monitor completion

## Capability Coordination

- Request Capabilities
- Interact with the Capability Registry
- Invoke the Capability Resolver
- Dispatch Tasks to Skills

## Execution Monitoring

- Monitor execution
- Track retries
- Handle timeouts
- Pause and resume execution
- Support cancellation

## Context Coordination

- Request Context refresh
- Maintain execution consistency

## Replanning

- Detect when execution should stop
- Request replanning from the Planner Engine

---

# Ownership

The Workflow Engine exclusively owns:

- Workflows
- Tasks
- Execution state
- Scheduling
- Progress
- Retry policies

---

# Lifetime

The Workflow Engine exists for the lifetime of an executing Workflow.

It begins after Plan approval.

It completes when the Workflow reaches a terminal state.

---

# Communication

Consumes:

- Approved Plan

Produces:

- Workflow
- Tasks
- Capability requests
- Progress updates
- Result references

Requests:

- Context refresh
- Replanning

---

# Extensibility

New scheduling strategies, execution policies, and recovery mechanisms may be added without changing the Workflow Engine's core responsibilities.

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
Execution
        │
        ▼
Monitoring
        │
        ▼
Completed
```

---

# Execution Control Loop

```text
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
      │
      ▼
Validation Framework
      │
      ▼
Workflow Engine
      ├──────── Continue
      ├──────── Retry
      ├──────── Refresh Context
      └──────── Request Replanning
                     │
                     ▼
               Planner Engine
```

---

# Failure Management

The Workflow Engine manages execution failures.

Possible responses include:

- Retry Task
- Resolve an alternative Skill implementation
- Pause execution
- Cancel execution
- Request Context refresh
- Request replanning

The Workflow Engine never guesses.

---

# Relationships

The Workflow Engine collaborates with:

- Context Engine
- Planner Engine
- Validation Framework
- Capability Registry
- Capability Resolver
- Skill Framework

---

# Information Boundaries

Information entering:

- Approved Plan
- Context references
- Validation feedback

Information produced:

- Workflow
- Tasks
- Progress
- Result references

Information never owned:

- Intent
- Context
- Plans
- Skill implementations
- Knowledge
- Memory

---

# Golden Rule

The Workflow Engine coordinates execution.

It never performs work.

---

# Guiding Principle

> **Execute the approved Plan safely, deterministically, and transparently while preserving user control and execution integrity.**

---

# Related Documents

- 02_System_Blueprint.md
- 04_Platform_Kernel.md
- 05_Data_Flow.md
- 06_Context_Engine.md
- 07_Planner_Engine.md
- 15_Skill_Framework.md

---

# Related ADRs

- ADR_0013 — Workflow Ownership
- ADR_0014 — Workflow Determinism
- ADR_0020 — Runtime vs Cross-Cutting Architecture
- ADR_0021 — Control Plane and Data Plane Separation
- ADR_0022 — Context Lifecycle and Ownership
- ADR_0023 — Capability Discovery and Resolution