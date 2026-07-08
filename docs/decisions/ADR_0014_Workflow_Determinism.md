---
adr: 0014
title: Workflow Determinism
status: accepted
date: 2026-07-08
author: Dhanrick Eviota
category: Workflow
---

# ADR_0014_Workflow_Determinism

## Decision

Workflows are deterministic by design but adaptive during execution.

They may pause, resume, retry, branch, and request clarification while remaining faithful to the validated Intent.

## Rationale

This provides predictable behavior while allowing intelligent adaptation during execution.
