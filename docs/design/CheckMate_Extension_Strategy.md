# CheckMate Extension Strategy

## EQ-0021 — CheckMate Application Architecture

### Spike 7 — Future Extension Strategy

**Status:** Complete (Amended — Formatter consumes Presentation Model)
**Date:** 2026-07-25
**Amended:** 2026-07-25
**Authority:** EQ-0021 Spike 7

---

## 1. Purpose

Define how future consumers integrate with CheckMate. Formatter now consumes Presentation Model instead of interpreting Evidence Contract directly.

---

## 2. Consumer Dependency Map (Amended)

| Consumer | Status | Consumes | Direct Evidence Access |
|----------|--------|----------|----------------------|
| CheckMate | DESIGNED | Evidence + Findings | Yes (Interpretation only) |
| Formatter | FUTURE | Presentation Model | No |
| Builder | FUTURE | Evidence Contract | Yes (CI integration) |
| O&A | FUTURE | Evidence Contract | Yes (specialized) |
| AI | FUTURE | Exported Presentation Model | No |

---

## 3. Extension Points

### 3.1 Formatter — NOW consumes Presentation Model

```
CheckMate → Presentation Model → Formatter renders for different formats
```

- Formatter receives Presentation Model (not evidence)
- Formatter DOES NOT compute severity, recommendations, or statistics
- Formatter converts Model to target format
- Formatter remains independent — no CheckMate modification

### 3.2 Builder (unchanged)

- Builder consumes Evidence Contract directly for CI integration
- Builder does NOT need CheckMate
- Builder does NOT receive Presentation Model

### 3.3 O&A (unchanged)

- O&A consumes Evidence Contract directly
- O&A does its own interpretation for O&A-specific analysis

### 3.4 AI Extension (unchanged)

- AI reads exported Presentation Model (not raw evidence)
- AI provides advisory commentary
- AI never modifies CheckMate output

---

## 4. Implementation Sequence (Amended)

| Package | Component | Priority | Depends On |
|---------|-----------|----------|-----------|
| IP-0003 | Application Foundation | 1 | Evidence v1.1, Validation v1 |
| IP-0004 | Interpretation Engine | 2 | IP-0003 |
| IP-0005 | Presentation Model | 3 | IP-0004 |
| IP-0006 | Review Workflow | 4 | IP-0005 |
| IP-0007 | Reporting & Export | 4 | IP-0005 |
| IP-0008 | Formatter (future) | 5 | IP-0005 |
| IP-0009 | Builder (future) | 6 | Evidence v1.1 |

---

## 5. Document Control

| Property | Value |
|----------|-------|
| Document ID | EQ-0021-S7 |
| Engineering Question | EQ-0021 |
| Spike | 7 |
| Status | Complete (Amended) |
| Date | 2026-07-25 |
| Amendments | Formatter consumes Presentation Model, IPs reordered |
| Authority | EQ-0021 |