---
adr: 0009
title: Skill Architecture
status: accepted
date: 2026-07-08
author: Dhanrick Eviota
category: Skills
tags:
- Skill
- Architecture
related:
- 15_Skill_Framework.md
supersedes: null
superseded_by: null
---

# ADR_0009_Skill_Architecture

## Context

Separate planning from execution.

## Decision

Planner decides WHAT. Workflow decides WHEN/HOW. Skills perform the work.

## Rationale

Clear responsibilities reduce coupling.

## Alternatives Considered

- Alternative approaches were discussed during architecture design.
- The selected approach best supports Jarvis's long-term modular architecture.

## Consequences

- Modular execution pipeline.

## Future Considerations

This decision may be revisited if future platform requirements fundamentally change, but it should remain stable unless superseded by a new ADR.

## Related Documents

15_Skill_Framework.md

