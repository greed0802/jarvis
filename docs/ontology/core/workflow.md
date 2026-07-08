# Workflow

## Definition

A Workflow is the execution strategy of Jarvis. It transforms an approved Intent into one or more executable Tasks and orchestrates their execution to achieve the user's goal.

Unlike the Planner, which decides **what** should be done, the Workflow determines **how** it should be executed. It supervises task execution, evaluates intermediate results, adapts its strategy when necessary, and ensures the execution remains aligned with the user's intent.

A Workflow is deterministic by design but adaptive in execution. Given the same validated context and constraints, it should produce a predictable strategy while remaining capable of responding to new information, clarification, or execution outcomes.

---

## Purpose

The Workflow exists to coordinate execution.

It owns the Tasks required to achieve an Intent, manages their lifecycle, determines execution order, controls branching and parallel execution, monitors progress, and continuously evaluates confidence before producing results.

The Workflow acts as the strategic supervisor between planning and execution.

---

## Ownership

A Workflow can exist at multiple levels.

- **Platform** defines the Workflow architecture and built-in workflows.
- **Workspace** owns active workflow instances during a working session.
- **Project** may store reusable or historical workflows.
- **User** can influence, pause, modify, stop, or save workflows.

---

## Relationship with Planner

Planner decides **what** should be accomplished.

Workflow decides **how** it will be accomplished.

Planner delegates execution.

Workflow manages execution.

---

## Tasks

A Workflow owns its Tasks.

Tasks are execution units delegated to Skills through the Planner and Capability system.

The Workflow monitors task completion, retries, branching, dependencies, and confidence.

---

## Execution

A Workflow supports:

- Sequential execution
- Parallel execution
- Conditional branching
- Retry
- Pause
- Resume
- Rollback (where applicable)
- Progressive execution

Multiple Workflows may exist simultaneously for the same Intent, such as:

- Fastest
- Highest Accuracy
- Lowest Cost
- Offline
- User-defined

The Planner selects the most appropriate Workflow based on Context.

---

## Results

A Workflow may produce:

- Intermediate Results
- Progress Updates
- Draft Results
- Final Results

Intermediate Results may continue to improve in the background until confidence reaches an acceptable threshold or the user approves the current result.

---

## Learning

Workflow execution history should be retained to reduce unnecessary recomputation, improve future execution strategies, and support learning.

Execution history should be reusable where appropriate while respecting permissions and validation.

---

## Failure

A Workflow should avoid failure whenever possible.

If execution confidence becomes insufficient, the Workflow should:

1. Explain what it currently understands.
2. Explain what it intends to do.
3. Identify missing information.
4. Request clarification from the user.

Only unrecoverable platform or system errors should terminate execution.

---

## Guiding Principle

A Workflow answers:

**"How should this Intent be executed?"**