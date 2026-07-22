# 01 — Project Overview

> **Purpose**: Compressed summary of what Jarvis is, its core values, governing principles, and current state. The entry point for understanding the platform's identity.
> **Part of**: Jarvis Knowledge Consolidation

---

## Responsibilities

This document covers:
- Platform identity (what Jarvis IS and IS NOT)
- Core values (9 permanent values)
- Engineering principles (permanent, technology-independent)
- Current phase and state

It does NOT cover architecture details (see `02_Architecture_Summary.md`), domain knowledge (see `03_Domain_Knowledge.md`), or engineering methodology (see `09_Methodology.md`).

---

## What Jarvis Is

Jarvis is a **modular Professional Intelligence Platform** — not a chatbot, not an AI wrapper, not an experimental playground.

**Identity**:
- Documentation First — architecture documents govern implementation
- Evidence Driven — no production code without verifiable evidence
- ADR Governed — architecture decisions are formal and traceable
- Capability Oriented — platform grows through independently engineered capabilities
- Long-term engineering platform — designed to evolve for many years

**Initial Domain**: Quantity Surveying / Civil Engineering / Cost Estimating

**Current Phase**: Phase 2 — Capability Era (entering Consumer Phase)

---

## Core Values (9 Permanent)

| # | Value | Meaning |
|---|-------|---------|
| 1 | **Human First** | Assists, never autonomously decides. Project Owner is final authority. |
| 2 | **Transparency** | Every decision explainable, every output traceable. |
| 3 | **Accuracy** | Deterministic, verifiable outputs. Evidence over assumptions. |
| 4 | **Trust** | Built through evidence-backed engineering, not marketing. |
| 5 | **Modularity** | Independent capabilities with clear contracts and boundaries. |
| 6 | **Extensibility** | Plugin and skill architecture enables domain expansion. |
| 7 | **Privacy** | Local-first architecture. Data stays under user control. |
| 8 | **Reliability** | Production-grade engineering. Deterministic, repeatable, testable. |
| 9 | **Determinism** | Identical inputs produce identical outputs whenever practical. |

---

## Governing Principles

These are **permanent, technology-independent** principles. Every feature, subsystem, and integration must conform.

### Architecture Principles
- **Architecture First**: Documentation governs implementation. Never code first, document later.
- **ADR Governed**: Architecture decisions are formal, traceable, and frozen upon acceptance.
- **Kernel Separation**: Kernel is control plane only — never creates context, plans, or executes business logic.
- **Ownership Exclusivity**: Each engine owns exactly one concern. Responsibilities never overlap.
- **Consumer Independence**: Capabilities expose public contracts. Consumers never depend on internals.

### Engineering Principles
- **Evidence Hierarchy**: ADRs > Architecture Docs > Production Code > Spike Evidence > Approved Documentation > External References > General AI Knowledge. Higher always overrides lower.
- **Deterministic Engineering**: Production code must be deterministic, repeatable, observable, testable, maintainable.
- **YAGNI**: Implement the smallest production-ready solution. Avoid speculative features.
- **Never Guess**: If evidence is insufficient, propose an Engineering Question or Spike. Production code must never be assumption-driven.
- **Small Iterations**: Prefer incremental improvement over large architectural leaps.

### Governance Principles
- **Human Authority**: Project Owner is final engineering authority. AI agents investigate, recommend, implement, review — never determine architecture independently.
- **Capability Lifecycle**: Discovery → Evaluation → Project Owner Decision → Engineering Question → Spike → Implementation → Validation → Promotion → Release. Never bypass stages without explicit approval.
- **Freeze Process**: EQs, contracts, and domain knowledge are frozen after verification. Frozen artifacts are permanent evidence.

---

## Current State (July 2026)

| Metric | Value |
|--------|-------|
| Phase | Phase 2 — Capability Era |
| Capabilities Implemented | 2 (BOQ Intelligence, Validation Engine) |
| Capabilities Deferred | 5 |
| Engineering Questions Completed | 4 (EQ-0010, EQ-0011, EQ-0012, EQ-0013) — all Frozen, Gate 3 |
| Spike Evidence Reports | 20 (across 4 EQs) |
| Public Contracts Frozen | 2 (BOQ Intelligence Evidence v1.0, Validation Findings v1.0) |
| ADRs Accepted | 26 |
| Production Code | ~1,700 lines Python (Kernel, Application, Validation Engine, domain types) |
| Architecture Implemented | ~20% (most engines are documented but not built) |
| Repository Phase | Entering Consumer Phase — knowledge base becomes primary entry point |

---

## What Jarvis Is NOT

- NOT a chatbot or conversational AI
- NOT an AI wrapper around LLM APIs
- NOT an experimental playground for AI features
- NOT autonomous — always requires human approval for important decisions
- NOT a generic platform — domain-specific (QS/Civil Engineering initially)

---

## Key Decisions

1. **Platform, not product**: Jarvis is engineering infrastructure, not a packaged application
2. **Documentation First**: Architecture documents are the source of truth, not code
3. **Evidence over assumptions**: No production code without verifiable evidence from spikes or prior implementation
4. **Contract-first capabilities**: Every capability exposes a public contract before implementation
5. **Domain grounding**: Initial focus on Quantity Surveying provides concrete domain validation for platform architecture
6. **Consumer Phase entry**: Repository is now mature enough that future work should consume the knowledge base rather than re-scanning all source documents

---

## Dependencies

```
00_Vision.md → 01_Principles.md → ADRs → Architecture Docs → Implementation
```

---

## References

- `docs/00_Vision.md` — Full vision statement (289 lines)
- `docs/01_Principles.md` — Full principles (351 lines)
- `AGENTS.md` — AI agent engineering rules
- `docs/planning/Capability_Register.md` — Current capability states
- `docs/26_Implementation_Status.md` — Implementation status
- `docs/knowledge/02_Architecture_Summary.md` — Architecture details
- `docs/knowledge/09_Methodology.md` — Engineering playbook

---

## Verification Status

| Source | Status |
|--------|--------|
| `docs/00_Vision.md` | **Project Owner Verified** |
| `docs/01_Principles.md` | **Project Owner Verified** |
| `AGENTS.md` | **Project Owner Verified** |
| Capability_Register.md | **Evidence-Backed** |
| 26_Implementation_Status.md | **Evidence-Backed** |

---

**Generated**: 2026-07-15 | **Part of**: Jarvis Knowledge Consolidation