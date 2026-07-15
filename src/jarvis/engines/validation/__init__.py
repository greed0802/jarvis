"""Validation Engine — deterministic validation rule evaluation.

Consumes BOQIntelligenceResult (Evidence Contract v1.0.0) and the
Validation Rule Registry to produce ValidationFindings.

Authority:
- EQ-0013 Spike 1 (Validation Capability Discovery)
- EQ-0013 Spike 2 (Validation Rule Taxonomy)
- EQ-0013 Spike 3 (Engine Scope & Responsibilities)
- EQ-0013 Spike 4 (Engine Implementation)

The Validation Engine is a pure function:
  Findings = f(Evidence, Rules)

It is:
  - Stateless
  - Deterministic
  - Immutable (produces frozen output)
  - Side-effect free (no filesystem, network, database)
  - Consumer-independent (no CheckMate/Formatter/Builder logic)
"""