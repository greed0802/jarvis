---
adr: 0006
title: Skill Collaboration
status: accepted
date: 2026-07-08
author: Dhanrick Eviota
category: Skills
tags:
- Skill
- Capability
related:
- 15_Skill_Framework.md
supersedes: null
superseded_by: null
---

# ADR_0006_Skill_Collaboration

## Context

Skills often require other abilities.

## Decision

Skills request Capabilities instead of calling other Skills directly.

## Rationale

This avoids circular dependencies and improves modularity.

## Alternatives Considered

- Alternative approaches were discussed during architecture design.
- The selected approach best supports Jarvis's long-term modular architecture.

## Consequences

- Loose coupling
- Better extensibility.

## Future Considerations

This decision may be revisited if future platform requirements fundamentally change, but it should remain stable unless superseded by a new ADR.

## Related Documents

15_Skill_Framework.md
