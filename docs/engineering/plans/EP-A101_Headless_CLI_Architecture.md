# EP-A101: Track A1 — Headless CLI Platform Operations Adapter (Architecture)

**Status:** Active
**Date:** 2026-07-30
**Milestone:** Track A1
**Paired Spec:** ES-A101
**Paired Evidence:** EV-A101
**Owner:** Product Engineering

---

## 1. Objective

Implement a thin, decoupled CLI adapter layer (`jarvis`) enabling headless
execution of workbench, evaluation, dataset, report, and diagnostic operations.

---

## 2. Layered Adapter Pipeline

```
User -> ArgParser -> CommandDispatcher -> ThinCommand
         -> CliApplicationServices -> Orchestrator/Runner -> Renderer -> stdout
```

- **Commands** contain zero business/orchestration/renderer logic.
- **CliApplicationServices** encapsulate platform interactions.
- **Renderers** format output independently of commands.

---

## 3. Acceptance Criteria

| AC | Criterion |
|----|-----------|
| AC-1 | Service Facade: Commands delegate only to CLI Application Services |
| AC-2 | Orchestrator/Runner Integration: Workbench & Eval run through services |
| AC-3 | Renderer Separation: Console, JSON, Markdown renderers are independent |
| AC-4 | Headless View: HeadlessConsoleView implements WorkbenchView protocol |
| AC-5 | Doctor Diagnostic: Structured report (Platform, Presentation, Eval, Datasets, Python, Config, Status) |
| AC-6 | One-Way Dependency: Production modules have zero imports from cli |
| AC-7 | Regression Protection: M10.6 (45) + M11.0 (19) tests pass unchanged |
| AC-8 | Deterministic Exit Codes: all commands return documented codes 0-5 |