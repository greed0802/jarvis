---
adr: 0012
title: Repository Structure
status: accepted
date: 2026-07-08
author: Dhanrick Eviota
category: Architecture
tags:
  - Repository
  - Structure
related:
  - 02_System_Blueprint.md
  - 15_Development_Guide.md
supersedes: null
superseded_by: null
---

# ADR_0012_Repository_Structure

## Context

The Jarvis repository needs a stable, scalable structure that matches the platform architecture.

## Decision

The repository shall adopt a layered structure.

- Source code under `src/jarvis/`
- Documentation under `docs/`
- Architecture decisions under `docs/decisions/`
- Repository automation under `tools/`
- Runtime/user data under `data/`
- Tests under `tests/`
- Third-party components under `third_party/`

The `src/jarvis/` package is organized by responsibility (domain, platform, engines, services, skills, integrations, intelligence, security, resources, workflows, and contracts).

## Rationale

The repository structure should mirror the architecture of Jarvis, making the codebase easier to navigate, extend, and maintain.

## Consequences

### Positive

- Clear separation of responsibilities.
- Better scalability.
- Consistent architecture.
- Easier contributor onboarding.

### Negative

- More initial folders to manage.

## Future Considerations

Future structural changes should be documented through new Architecture Decision Records.

## Related Documents

- 02_System_Blueprint.md
- 24_Development_Guide.md
