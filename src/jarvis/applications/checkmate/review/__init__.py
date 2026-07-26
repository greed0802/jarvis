"""CheckMate Review Session Package (IP-0006).

Provides the human interaction layer of CheckMate. Review consumes ONLY
the immutable PresentationModel. It records human decisions without
performing any interpretation, rendering, or export.

Review Session components:
- PresentationId — stable, renderer-independent identity
- ReviewDecisions — immutable decision state
- ReviewNotes — reviewer-authored annotations
- Bookmarks — return-later references
- ReviewProgress — deterministic completion tracking
- ReviewSession — composition root

No rendering. No interpretation. No reports.

Authority:
  - EQ-0021 (Permanently Frozen)
  - Application Architecture Principles v1.0
  - IP-0006 — CheckMate Review Session & Human Workflow
"""