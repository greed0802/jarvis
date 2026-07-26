"""CheckMate Rendering Layer (IP-0007).

Deterministic renderers that convert immutable application state
(PresentationModel + optional ReviewSession) into human-readable
RenderedDocument objects.

Renderers never perform interpretation, validation, review,
persistence, or filesystem operations.

Authority:
  - EQ-0021 (Permanently Frozen)
  - Application Architecture Principles v1.0
  - IP-0007 — CheckMate Rendering Layer
"""