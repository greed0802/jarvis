---
adr: 0020
title: Runtime vs Cross-Cutting Architecture
status: accepted
date: 2026-07-08
author: Dhanrick Eviota
category: Architecture
---

# ADR_0020_Runtime_vs_Cross_Cutting_Architecture

## Context

The original architecture classified Context, Planner, Workflow, Learning, and Validation as Core Engines.

Further architectural refinement determined that Learning and Validation support multiple platform components rather than participating directly in the execution pipeline.

## Decision

The Jarvis Platform separates runtime execution from cross-cutting capabilities.

### Core Runtime Engines

- Context Engine
- Planner Engine
- Workflow Engine

### Cross-Cutting Frameworks

- Learning Framework
- Validation Framework
- Memory Framework
- Knowledge Framework
- Resource Framework

## Rationale

Execution engines transform user intent into execution. Cross-cutting frameworks provide reusable capabilities that support multiple subsystems without becoming part of the execution pipeline.

## Consequences

- Clear separation of responsibilities.
- Reduced coupling.
- Easier extensibility.
- Consistent with the Platform Kernel philosophy.

## Related Documents

- 02_System_Blueprint.md
- 04_Platform_Kernel.md
