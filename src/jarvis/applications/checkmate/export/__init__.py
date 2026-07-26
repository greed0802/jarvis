"""CheckMate Export & Delivery Layer (IP-0008).

Exporters consume only RenderedDocument objects. They never perform
rendering, review, interpretation, or validation. Exporters convert
in-memory RenderedDocument into delivery-ready ExportResult containing
content bytes, checksums, and metadata.

Architecture:
  Interpret Once → Review Once → Render Many → Deliver Anywhere

Authority:
  - EQ-0021 (Permanently Frozen)
  - Application Architecture Principles v1.0
  - IP-0008 — CheckMate Export & Delivery Layer
"""