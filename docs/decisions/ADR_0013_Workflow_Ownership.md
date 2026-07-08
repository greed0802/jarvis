---
adr: 0013
title: Workflow Ownership
status: accepted
date: 2026-07-08
author: Dhanrick Eviota
category: Workflow
---

# ADR_0013_Workflow_Ownership

## Decision

A Workflow owns the Tasks required to execute an Intent.

The Planner decides **what** should be accomplished.

The Workflow decides **how** it will be executed and manages task lifecycle, ordering, branching, retries, progress, and completion.

## Rationale

Separating planning from execution keeps the architecture modular and maintainable.
