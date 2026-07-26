# Capability Roadmap v2.0

## Document Control

| Property | Value |
|----------|-------|
| Document ID | ROAD-CAP-002 |
| Status | ACTIVE |
| Version | 2.0 |
| Date | 2026-07-26 |
| Authority | Project Owner |
| Supersedes | All prior development roadmaps |
| Dependencies | Architecture Freeze v1.0 |

---

## 1. Purpose

This roadmap defines future development after the architecture freeze.

All future work is **capability-oriented**. Architecture is complete. No new architectural layers shall be introduced.

Every capability consumes the frozen architecture defined in Architecture Freeze v1.0. No capability modifies the architecture.

---

## 2. Phase Transition

| Property | Before | After |
|----------|--------|-------|
| Development Type | Architecture | Capability |
| Package Prefix | IP (Implementation Package) | CP (Capability Package) |
| Changes | New layers, new contracts | New consumers, new integrations |
| Governance | Architecture authority | Capability authority |
| Primary Document | Architecture Freeze v1.0 | Capability Roadmap v2.0 |

---

## 3. Capability ID Allocation

| Range | Reserved For |
|-------|-------------|
| CP-0001–0099 | CheckMate capabilities |
| CP-0100–0199 | Builder capabilities |
| CP-0200–0299 | Formatter capabilities |
| CP-0300–0399 | Shared infrastructure |
| CP-0400–0499 | Experimental / research |

---

## 4. Capability Categories

### 4.1 User Interfaces

Capabilities that deliver the application to human users.

| ID | Capability | Consumes | Notes |
|----|-----------|----------|-------|
| CP-0001 | CLI Application | PresentationModel, ReviewSession, RenderedDocument, ExportResult | Terminal-based interactive review and export |
| CP-0008 | Desktop GUI | PresentationModel, ReviewSession | Native or Electron desktop application |
| CP-0009 | Web UI | PresentationModel, ReviewSession | Browser-based review interface |

### 4.2 API & Integration

Capabilities that deliver the application to other systems.

| ID | Capability | Consumes | Notes |
|----|-----------|----------|-------|
| CP-0002 | REST API | RenderedDocument, ExportResult | HTTP serving of rendered/exported artifacts |
| CP-0005 | Builder Integration | PresentationModel, ExportResult | Consume CheckMate output in Builder tool |
| CP-0006 | Formatter Integration | PresentationModel | Automated formatting pipeline |
| CP-0011 | Batch Processing | Full pipeline | Scheduled batch processing of multiple BOQ files |

### 4.3 Export Format Expansion

New renderers and exporters for additional formats.

| ID | Capability | Consumes | Notes |
|----|-----------|----------|-------|
| CP-0003 | PDF Export | PresentationModel + ReviewSession → new Renderer + Exporter | Renderer produces text/layout; Exporter outputs PDF bytes |
| CP-0004 | DOCX Export | PresentationModel + ReviewSession → new Renderer + Exporter | Word document output |
| CP-0007 | Excel Export | PresentationModel → new Renderer + Exporter | Requires multi-section workbook logic |

### 4.4 AI & Intelligence

| ID | Capability | Consumes | Notes |
|----|-----------|----------|-------|
| CP-0014 | AI Commentary | RenderedDocument | AI receives exported text, never raw evidence |

### 4.5 Infrastructure

| ID | Capability | Consumes | Notes |
|----|-----------|----------|-------|
| CP-0010 | File System Writer | ExportResult | Write ExportResult bytes to disk |
| CP-0012 | Cloud Storage Delivery | ExportResult | Upload to S3, GCS, Azure Blob |
| CP-0013 | Email Delivery | ExportResult + RenderedDocument | Send rendered reports via email |

---

## 5. Capability Dependency Model

Every capability consumes the frozen architecture. No capability introduces a new architectural layer.

```
                     Frozen Architecture
                     (Interpret Once → Review Once → Render Many → Deliver Anywhere)
                                    │
          ┌─────────────────────────┼─────────────────────────┐
          │                         │                         │
   User Interfaces           Export Formats             API/Integration
   ---------------          ---------------           ----------------
   CP-0001 - CLI             CP-0003 - PDF            CP-0002 - REST API
   CP-0008 - Desktop         CP-0004 - DOCX           CP-0005 - Builder
   CP-0009 - Web             CP-0007 - Excel          CP-0006 - Formatter
                                                      CP-0011 - Batch
          │                         │                         │
          └─────────────────────────┼─────────────────────────┘
                                    │
                            Infrastructure
                            --------------
                            CP-0010 - File Writer
                            CP-0012 - Cloud Storage
                            CP-0013 - Email

   ─────────────────────────────────────────────────────────────────
                                   │
                            AI Capabilities
                            --------------
                            CP-0014 - AI Commentary (consumes exported text)
```

---

## 6. Capability Package Template

Every CP follows this structure:

### 6.1 Package Identity

| Field | Value |
|-------|-------|
| ID | CP-NNNN |
| Name | Short descriptive name |
| Category | User Interface / API / Export / AI / Integration |
| Status | Proposed / In Development / Complete |

### 6.2 Architecture Consumption

| Consumer Entry Point | What CP reads |
|----------------------|---------------|
| PresentationModel | (if applicable) |
| ReviewSession | (if applicable) |
| RenderedDocument | (if applicable) |
| ExportResult | (if applicable) |

### 6.3 What CP MUST NOT Do

1. No new architectural layers
2. No duplicate interpretation
3. No duplicate review
4. No rendering of raw evidence
5. No modification of frozen objects

### 6.4 Deliverables

- Capability implementation
- Tests
- Documentation
- Capability Register entry (if applicable)

---

## 7. Recommended First Capabilities

The following sequence provides the most value for incremental investment:

### Phase 1: Delivery
1. **CP-0001 — CLI Application** — Makes CheckMate usable from the terminal
2. **CP-0003 — PDF Export** — Professional-quality PDF output
3. **CP-0010 — File Writer** — Write exports to disk

### Phase 2: Network
4. **CP-0002 — REST API** — Make the pipeline available over HTTP
5. **CP-0005 — Builder Integration** — Feed output into Builder
6. **CP-0006 — Formatter Integration** — Feed output into Formatter

### Phase 3: Advanced Formats
7. **CP-0004 — DOCX Export** — Word document compatibility
8. **CP-0007 — Excel Export** — Spreadsheet analysis

### Phase 4: User Experience
9. **CP-0008 — Web UI** — Browser-based interface
10. **CP-0009 — Desktop GUI** — Cross-platform application

### Phase 5: Intelligence
11. **CP-0014 — AI Commentary** — AI-assisted report interpretation

### Phase 6: Delivery Expansion
12. **CP-0012 — Cloud Storage** — S3/GCS/Azure delivery
13. **CP-0013 — Email Delivery** — Email-based reporting

---

## 8. Governance

| Property | Value |
|----------|-------|
| Document ID | ROAD-CAP-002 |
| Governing Repository | Jarvis |
| Governing Application | CheckMate |
| Authority | Project Owner |
| Amendment Authority | Project Owner |
| Depends On | Architecture Freeze v1.0 |
| Review Schedule | Quarterly or on significant capability completion |

This roadmap SHALL be updated when capabilities are proposed, started, completed, or rejected. It does not supersede the Architecture Freeze.