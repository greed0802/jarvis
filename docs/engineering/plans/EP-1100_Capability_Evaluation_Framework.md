# EP-1100: M11.0 — Capability Evaluation Framework (Architecture)

**Status:** Active
**Date:** 2026-07-30
**Milestone:** M11.0
**Paired Spec:** ES-1100
**Paired Evidence:** EV-1100
**Owner:** Product Engineering

---

## 1. Objective

Implement a decoupled Platform Evaluation Framework that measures capability
quality across five domains (EVA-1 through EVA-5) against the frozen M10.6
platform state. The framework acts as an independent observer — production
runtime modules MUST NOT import from `src/jarvis/evaluation/`.

---

## 2. Subsystem Architecture

```
evaluation/
├── datasets/golden/          # Versioned golden datasets
│   └── boq_baseline/         # BOQ baseline dataset
│       ├── case_001/          # Individual evaluation case
│       └── ...
├── src/jarvis/evaluation/    # Framework source (independent observer)
│   ├── __init__.py
│   ├── contracts.py          # Immutable evaluation contracts
│   ├── registry.py           # Evaluator registry & discovery
│   ├── datasets.py           # Dataset loader
│   ├── metrics.py            # Pure math functions
│   ├── evaluators/           # Reference plugin evaluators
│   │   ├── __init__.py
│   │   ├── retrieval.py      # EVA-1
│   │   ├── grounding.py      # EVA-2
│   │   ├── navigation.py     # EVA-3
│   │   ├── projection.py     # EVA-4
│   │   └── workflow.py       # EVA-5
│   ├── runner.py             # Profile-driven runner
│   └── report.py             # Report exporter
└── tests/evaluation/          # Evaluation framework tests
    └── test_ep1100_evaluation_framework.py
```

---

## 3. One-Way Dependency Flow

```
src/jarvis/evaluation/ (observer)
        |  reads/imports
        v
src/jarvis/contracts/  (capabilities)
src/jarvis/presentation/ (viewmodels, projector, router, orchestrator)
src/jarvis/engines/     (assistant, understanding, checkmate)
        |
        | SHALL NOT import above
        X
src/jarvis/evaluation/
```

Production runtime modules (`engines/`, `platform/`, `presentation/`) MUST NOT
import from `src/jarvis/evaluation/`. The evaluation framework reads production
contracts only.

---

## 4. Architecture/Policy Separation

| Artifact | Content |
|----------|---------|
| EP-1100 | Subsystem architecture, component hierarchy, interfaces, plugin discovery, runner execution model |
| ES-1100 | Metrics definitions, mathematical formulas, pass/fail promotion thresholds, quality profiles, golden dataset specs |
| EV-1100 | Empirical baseline benchmark results recorded against frozen M10.6 state |

---

## 5. Acceptance Criteria

| # | Criterion |
|---|---|
| AC-1 | Architecture/Policy Separation: EP-1100 contains architecture; ES-1100 contains specs |
| AC-2 | Registry/Protocol Decoupling: Evaluator protocol + dynamic registry |
| AC-3 | Dataset/Case Hierarchy: Structured, versioned golden cases |
| AC-4 | Complete Provenance: EvaluationProvenance in every EvaluationReport |
| AC-5 | Quality Profiles: Smoke, Regression, Release, Research profiles |
| AC-6 | Promotion Gate Differentiation: Gates vs. informational metrics |
| AC-7 | Reference Evaluators: Plugin evaluators for EVA-1 through EVA-5 |
| AC-8 | Genuine Baseline Evidence: EV-1100 records observed M10.6 outputs |
| AC-9 | Architectural Independence: Zero reverse imports |