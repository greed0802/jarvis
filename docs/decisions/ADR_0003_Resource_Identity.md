---
adr: 0003
title: Resource Identity
status: accepted
date: 2026-07-08
author: Dhanrick Eviota
category: Resource
tags:
- Resource
related:
- 03_Core_Ontology_Relationships.md
supersedes: null
superseded_by: null
---

# ADR_0003_Resource_Identity

## Context

Resources may move between storage providers.

## Decision

A Resource keeps the same identity regardless of provider or location.

## Rationale

Identity should not depend on physical storage.

## Alternatives Considered

- Alternative approaches were discussed during architecture design.
- The selected approach best supports Jarvis's long-term modular architecture.

## Consequences

- Stable references
- Easier synchronization.

## Future Considerations

This decision may be revisited if future platform requirements fundamentally change, but it should remain stable unless superseded by a new ADR.

## Related Documents

03_Core_Ontology_Relationships.md
