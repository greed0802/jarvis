# CheckMate Application Architecture

## EQ-0021 — CheckMate Application Architecture

### Spike 1 — Application Boundary

**Status:** Complete (Amended — Presentation Model introduced)
**Date:** 2026-07-25
**Amended:** 2026-07-25
**Authority:** EQ-0021 Spike 1

---

## 1. Purpose

Define CheckMate as the first production application consuming BOQ Intelligence evidence and Validation Findings. Determine CheckMate application boundary, ownership, and relationships with existing platform components.

---

## 2. Application Identity

### 2.1 What CheckMate Is

CheckMate is the **professional quantity surveying guidance application**. It:

1. Consumes BOQ Intelligence evidence (BOQIntelligenceResult)
2. Consumes Validation findings (ValidationFindings)
3. Produces a Presentation Model (single deterministic projection of evidence)
4. Presents evidence and findings to the professional estimator
5. Provides advisory recommendations based on evidence
6. Generates structured reports from the Presentation Model
7. Supports human review workflow
8. Enables export of reports from the Presentation Model

CheckMate is an **Evidence Interpreter** (Tier 3 in Consumer Architecture).

### 2.2 What CheckMate Is NOT

CheckMate SHALL NOT:

1. Produce evidence (owned by BOQ Intelligence)
2. Perform parsing (owned by WorkbookParser)
3. Perform extraction (owned by boq_extraction)
4. Perform validation (owned by Validation Engine)
5. Modify BOQ Intelligence behavior
6. Replace professional estimator judgement
7. Make autonomous decisions
8. Perform automated corrections
9. Modify workbook files
10. Introduce AI or ML processing
11. Allow multiple presentation layers to interpret evidence independently

---

## 3. Application Topology

### 3.1 Layered Architecture

CheckMate follows a **five-layer architecture** with a critical separation at the Presentation Model:

```
┌─────────────────────────────────────────────────────────┐
│                    CheckMate Application                │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │          Evidence Layer (input)                  │   │
│  │  BOQIntelligenceResult | ValidationFindings      │   │
│  │  Read-only. CheckMate does not modify.          │   │
│  └──────────────┬──────────────────────────────────┘   │
│                 │                                       │
│                 ▼                                       │
│  ┌─────────────────────────────────────────────────┐   │
│  │        Interpretation Layer                   │   │
│  │  Severity mapping | Grouping logic             │   │
│  │  Recommendation generation | Statistics       │   │
│  │  Interpretation happens EXACTLY ONCE here.    │   │
│  └──────────────┬──────────────────────────────────┘   │
│                 │                                       │
│                 ▼                                       │
│  ╔═════════════════════════════════════════════════╗   │
│  ║       Presentation Model (immutable)            ║   │
│  ║  PresentationFinding[] | PresentationSection[]   ║   │
│  ║  PresentationSummary | PresentationStatistics   ║   │
│  ║  Derived deterministically from interpretation  ║   │
│  ╚═════════════════════════════════════════════════╝   │
│                 │                                       │
│                 ▼                                       │
│  ┌─────────────────────────────────────────────────┐   │
│  │          Presentation Layer                     │   │
│  │  CLI rendering | Navigation | Filtering        │   │
│  │  Review workflow | User interaction             │   │
│  │  Renders Presentation Model — no analysis       │   │
│  └──────────────┬──────────────────────────────────┘   │
│                 │                                       │
│                 ▼                                       │
│  ┌─────────────────────────────────────────────────┐   │
│  │          Export Layer                           │   │
│  │  Report generation | PDF | JSON | CSV          │   │
│  │  Consumes Presentation Model only              │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### 3.2 Presentation Model — Critical Separation

The **Presentation Model** is the single deterministic projection of evidence produced by Interpretation. It is:

| Property | Description |
|----------|-------------|
| Immutable | Derived once, never modified |
| Deterministic | Same evidence produces identical Model |
| Consumed by renderers | Presentation, Report, Export, Formatter all read from Model |
| Not evidence | Derived from evidence; it is a projection |
| Not findings | Derived from findings; it is interpretation |

All downstream consumers only read the Presentation Model. No renderer performs interpretation.

---

## 4. Ownership Model

### 4.1 CheckMate Ownership

| Responsibility | Owner | Notes |
|----------------|-------|-------|
| Evidence interpretation | CheckMate | Performed ONCE in Interpretation layer |
| Presentation Model production | CheckMate | Single deterministic projection |
| Presentation Model consumption | CheckMate + Future | Formatter consumes too |
| Recommendation formulation | CheckMate | Generated during Interpretation only |
| Evidence presentation | CheckMate | UI/CLI report renders the Model |
| Finding presentation | CheckMate | Renders from Model — severity already computed |
| Report generation | CheckMate | From Presentation Model |
| Human review workflow | CheckMate | Review points, sign-off, tracking |
| Export generation | CheckMate | From Presentation Model |

### 4.2 Non-Ownership

| Responsibility | Owner | CheckMate Relationship |
|----------------|-------|------------------------|
| Evidence production | BOQ Intelligence | Consumer — read-only |
| Finding production | Validation Engine | Consumer — read-only |
| Parsing | WorkbookParser | No dependency |
| Extraction | boq_extraction | No direct dependency |
| Data persistence | Future | Out of scope for v1 |
| User authentication | Future | Out of scope for v1 |
| Multi-user workloads | Future | Out of scope for v1 |
| Professional Judgement | Human estimator | Advisory maintains |

---

## 5. Component Relationships

### 5.1 Dependency Direction

```
BOQ Intelligence → Evidence Contract v1.1.0
                     ↓
CheckMate (read-only)
                     ↓
              Evidence Interpretation (ONCE)
                     ↓
              Presentation Model (immutable)
           ┌─────────┼─────────┐
           │         │         │
    Presentation   Report    Export
      (CLI/GUI)  (structured) (PDF/JSON/CSV)
```

CheckMate depends on two contracts:
1. **BOQ Intelligence Public Evidence Contract v1.1.0** — for evidence
2. **Validation Findings Contract v1.0** — for findings

### 5.2 Future Dependencies

- **Formatter** consumes Presentation Model (not raw evidence)
- **Builder** consumes Evidence Contract directly (no Presentation Model needed)
- **O&A** consumes Evidence Contract directly (separate interpretation)
- **AI** receives exported Presentation Model (never raw evidence)

---

## 6. Input Contracts

### 6.1 Primary Input — BOQIntelligenceResult

Source: analyze_boq()
Contract: BOQ Intelligence Public Evidence Contract v1.1.0
Access: Direct frozen dataclass (read-only)
Import: from jarvis.parsers.costx.boq_intelligence import BOQIntelligenceResult

### 6.2 Secondary Input — ValidationFindings

Source: Validation Engine
Contract: Validation Findings Contract v1.0
Access: Direct frozen dataclass (read-only)

---

## 7. Output Contracts

### Output — Presentation Model

| Output | Format | Consumer |
|--------|--------|----------|
| Presentation Model | Immutable structured | Presentation, Report, Export, Formatter |
| Report | Structured document | Professional estimator, client |
| Export | PDF, CSV, JSON | External systems |

---

## 8. Boundary Enforcement

### 8.1 Must Not Cross

1. CheckMate must not modify evidence — BOQIntelligenceResult is frozen
2. CheckMate must not modify findings — ValidationFindings is frozen
3. CheckMate must not perform validation — belongs to Validation Engine
4. Presentation layer must not interpret evidence — only render Presentation Model
5. Reports must not interpret evidence — consume Presentation Model
6. Export must not reinterpret — serializes Presentation Model

### 8.2 Must Maintain

1. Interpretation performed ONCE and ONLY once
2. Presentation Model is deterministic for same inputs
3. All presentation layers share ONE Model
4. Huma review points for required findings
5. Recommendation flag mandatory advisory

---

## 9. Document Control

| Property | Value |
|----------|-------|
| Document ID | EQ-0021-S1 |
| Engineering Question | EQ-0021 |
| Spike | 1 |
| Status | Complete (Amended) |
| Date | 2026-07-25 |
| Amendments | Presentation Model inserted as separate layer |
| Authority | EQ-0021 |