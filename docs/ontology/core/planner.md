# Object: Planner

Category:
Core / Decision

---

## Purpose

The Planner transforms a validated Intent and Context into an executable Plan.

It determines the most appropriate strategy for achieving the user's objective by selecting Capabilities, ordering work, estimating confidence, identifying risks, and requesting clarification when required.

The Planner never performs work itself.

---

## Guiding Principle

Planner answers the question:

> **"Given everything I know, what is the best strategy to achieve the user's objective?"**

---

## Guiding Philosophy

The Planner is Jarvis's manager.

It understands the platform's abilities, evaluates the current Context, and designs the most appropriate strategy before any work begins.

The Planner manages the plan.

The Workflow manages the execution.

Skills perform the work.

This separation ensures that planning remains deterministic while execution remains flexible.

---

## Definition

The Planner is a deterministic Platform Engine responsible for transforming user Intent and Context into one or more executable Plans.

It evaluates available Capabilities, Resources, Permissions, Constraints, and Confidence before approving a Plan for execution.

The Planner never executes Skills directly.

---

## Responsibilities

The Planner is responsible for:

- Interpreting Intent
- Understanding Context
- Decomposing goals into tasks
- Selecting Capabilities
- Delegating work
- Ordering execution
- Creating alternative plans
- Estimating confidence
- Assessing risks
- Requesting clarification
- Submitting approved Plans to the Workflow

---

## Artificial Intelligence

The Planner remains deterministic.

AI may assist only when deterministic planning cannot produce sufficient confidence.

AI provides suggestions.

The Planner validates those suggestions before incorporating them into a Plan.

AI never replaces the Planner.

---

## Planning Modes

The Planner may generate:

- Initial Plan
- Alternative Plan
- High Confidence Plan
- Fastest Plan
- Lowest Cost Plan
- User Preferred Plan

---

## Clarification

If confidence is below the required threshold, the Planner must not proceed.

Instead it should:

1. Review Context.
2. Search Memory and Knowledge.
3. Request AI assistance if appropriate.
4. Ask the user for clarification.

Execution should never continue with unresolved ambiguity.

---

## Relationships

Consumes:

- Intent
- Context

Produces:

- Plan

Uses:

- Capability Registry
- Capability Resolver

Submits Plans to:

- Workflow

---

## Planner is NOT

The Planner is not a Workflow.

The Planner is not a Skill.

The Planner is not an AI.

The Planner does not execute work.

The Planner designs the strategy for execution.