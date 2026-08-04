# EP-A102: Track A2 — Interactive Textual Workbench TUI (Architecture)

**Status:** Active
**Date:** 2026-07-30
**Milestone:** Track A2
**Paired Spec:** ES-A102
**Paired Evidence:** EV-A102
**Owner:** Product Engineering

---

## 1. Objective

Build an interactive multi-panel TUI using the Textual framework implementing
the WorkbenchView protocol with passive widgets and bidirectional traceability.

---

## 2. Interaction Pipeline

```
Textual Widget → InteractionController → TextualInteractionSink
  → WorkbenchOrchestrator → WorkbenchProjector → New WorkbenchViewModel
  → Passive Widget Render
```

---

## 3. Acceptance Criteria

| AC | Criterion |
|----|-----------|
| AC-1 | Protocol Compliance — TextualWorkbenchApp implements WorkbenchView |
| AC-2 | Pure VM Rendering — widgets render from immutable WorkbenchViewModel only |
| AC-3 | Bidirectional Navigation — findings ⇄ evidence ⇄ citations |
| AC-4 | Grounded Chat Interactivity — query submission + citation targets |
| AC-5 | Canonical Pipeline — Bind → Validate → Understand → Chat → Inspect |
| AC-6 | One-Way Dependency — zero production imports from ui/textual |
| AC-7 | Regression Protection — all 98 prior tests pass unmodified |
| AC-8 | Headless Testing — async Textual test pilot coverage |
| AC-9 | Deterministic Rendering — same VM = same widget state |