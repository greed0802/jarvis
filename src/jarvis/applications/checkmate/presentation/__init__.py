"""CheckMate Presentation Model Package (IP-0005).

Transforms InterpretationSummary into an immutable PresentationModel.

Single responsibility: projection, organization, navigation preparation,
and view construction. NO interpretation. NO rendering. NO reports.

The PresentationModel is the ONLY output consumed by all future renderers.

Authority:
  - EQ-0021 (Permanently Frozen)
  - Application Architecture Principles v1.0 (Principle 1 — Interpretation Once, Rendering Many)
  - IP-0005 — CheckMate Presentation Model Assembly
"""