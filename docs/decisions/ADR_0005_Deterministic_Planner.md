---
adr: 0005
title: Deterministic Planner
status: accepted
date: 2026-07-08
author: Dhanrick Eviota
category: Platform
tags:
- Planner
- AI
related:
- 04_Platform_Kernel.md
supersedes: null
superseded_by: null
---

# ADR_0005_Deterministic_Planner

## Context

Define AI's role in planning.

## Decision

The Planner is deterministic by default. AI only assists when confidence is insufficient.

## Rationale

Planning should remain predictable and auditable.

## Alternatives Considered

- Alternative approaches were discussed during architecture design.
- The selected approach best supports Jarvis's long-term modular architecture.

## Consequences

- Reliable planning
- AI remains advisory.

## Future Considerations

This decision may be revisited if future platform requirements fundamentally change, but it should remain stable unless superseded by a new ADR.

## Related Documents

04_Platform_Kernel.md
