# 02 — Architecture Summary

> **Purpose**: Compressed architecture overview — layers, runtime lifecycle, data flow, ownership, and current implementation status.
> **Part of**: Jarvis Knowledge Consolidation

---

## Responsibilities

This document covers:
- Platform architecture layers (Control Plane, Data Plane, Skills, Validation, Learning)
- Runtime lifecycle and ownership rules
- Data flow from user request to knowledge
- What is implemented vs documented-only
- Key architectural decisions from ADRs

It does NOT cover project identity (see `01_Project_Overview.md`), domain knowledge (`03_Domain_Knowledge.md`), or detailed methodology (`09_Methodology.md`).

---

## Architecture Layers

### Layer 1: Platform Kernel (Control Plane)
**Status**: IMPLEMENTED (`src/jarvis/core/jarvis/kernel.py`, 201 lines)

**Responsibilities**:
- Component registration and service management
- Lifecycle orchestration (initialize → start → shutdown)
- Service registry (dict-based, no DI framework)
- Reverse-order shutdown, emergency shutdown on start failure

**Kernel NEVER**:
- Creates Context, Plans, Workflows, or Tasks
- Executes business logic
- Executes Skills
- Performs validation or learning

**Governance**: ADR-0017 (Platform Kernel Philosophy)

---

### Layer 2: Application (Composition Root)
**Status**: IMPLEMENTED (`src/jarvis/application/application.py`, 126 lines)

**Responsibilities**:
- Creates runtime components at startup
- Assembles the runtime (wires dependencies)
- Registers services with Kernel
- Handles SIGINT/SIGTERM signals for graceful shutdown
- Orchestrates full lifecycle via `app.run()`

**Entry point**: `app.py` (27 lines) — creates Configuration, Application, calls `app.run()`

---

### Layer 3: Configuration
**Status**: IMPLEMENTED (`src/jarvis/configuration/configuration.py`, 28 lines)

Frozen dataclass. Currently only `log_level: str = "INFO"`. YAGNI-minimal by design.

---

### Layer 4: Data Plane Engines
**Status**: NOT IMPLEMENTED (all engine directories are empty)

| Engine | Responsibility | Directory | Status |
|--------|---------------|-----------|--------|
| Context Engine | Owns Context and Intent; objective-scoped lifetime | `src/jarvis/core/context/` | Empty |
| Planner Engine | Owns Plans; deterministic plan generation | Not scaffolded | Empty |
| Workflow Engine | Owns Workflows and Tasks; execution orchestration | Not scaffolded | Empty |

These are documented in `docs/06_Context_Engine.md`, `docs/07_Planner_Engine.md`, `docs/08_Workflow_Engine.md` but have **zero implementation**.

---

### Layer 5: Skills
**Status**: NOT IMPLEMENTED

Skills perform the actual work. Planner decides WHAT, Workflow decides WHEN/HOW, Skills execute. No Skill infrastructure exists.

---

### Layer 6: Validation Engine
**Status**: IMPLEMENTED (`src/jarvis/engines/validation/engine.py`)

**Responsibilities**:
- Evaluates outputs against a rule registry
- Produces ValidationFindings (findings with severity, rule reference, context)
- Deterministic, reusable infrastructure
- Never modifies inputs (pure evaluation)

**Governance**: ADR-0022, `Validation_Findings_Contract_v1.0.md` (Frozen)

**Domain types**: 12 modules in `src/jarvis/domain/` define BOQRow, Capability, Context, Intent, Knowledge, Memory, Planner, Project, Resource, Result, Skill, Workflow, Workspace.

---

### Layer 7: Learning Engine
**Status**: NOT IMPLEMENTED

Promotes validated Results to Knowledge. `src/jarvis/core/learning/` is empty.

---

## Runtime Lifecycle

```
LifecycleState Enum:
CREATED → INITIALIZING → INITIALIZED → STARTING → RUNNING → STOPPING → STOPPED
                                                                      ↘ ERROR
```

**Contract**: `LifecycleAware` Protocol (`src/jarvis/contracts/lifecycle.py`):
- `initialize()` → `start()` → `shutdown()`
- All runtime components implement this protocol
- Kernel orchestrates lifecycle for all registered components
- Reverse-order shutdown (last registered = first shutdown)
- Emergency shutdown if any component fails during start

---

## Data Flow (Documented, Not Implemented)

```
User Request → Intent → Context → Planner → Approved Plan
    → Workflow → Task → Capability → Capability Registry
    → Capability Resolver → Skill → Result → Validation
    → Memory → Learning → Knowledge
```

**Critical ownership rule**: Each information type is owned by exactly ONE engine. Responsibilities must never overlap.

| Information Type | Owner |
|-----------------|-------|
| Intent | Context Engine |
| Context | Context Engine |
| Plan | Planner Engine |
| Workflow | Workflow Engine |
| Task | Workflow Engine |
| Result | (Result Framework — unresolved reference, see Appendix E) |
| Finding | Validation Engine |
| Knowledge | Learning Engine |

---

## Current Implementation Status

| Component | Code | Tests | Docs | Status |
|-----------|------|-------|------|--------|
| Kernel | ✅ 201 lines | — | ✅ | Production |
| Application | ✅ 126 lines | — | ✅ | Production |
| Configuration | ✅ 28 lines | — | ✅ | Production |
| LoggingService | ✅ ~100 lines | — | ✅ | Production |
| Lifecycle Contract | ✅ 48 lines | — | ✅ | Production |
| Domain Types (12) | ✅ ~600 lines | — | ✅ | Production |
| Validation Engine | ✅ ~200 lines | — | ✅ | Production |
| Context Engine | ❌ Empty dir | — | ✅ (spec) | Not started |
| Planner Engine | ❌ | — | ✅ (spec) | Not started |
| Workflow Engine | ❌ | — | ✅ (spec) | Not started |
| Learning Engine | ❌ Empty dir | — | ✅ (spec) | Not started |
| Skills | ❌ | — | ✅ (spec) | Not started |
| Plugins | ❌ | — | ✅ (spec) | Not started |
| API | ❌ | — | ✅ (spec) | Not started |
| Storage | ❌ | — | ✅ (spec) | Not started |
| GUI | ❌ | — | ✅ (spec) | Not started |
| Security | ❌ | — | ✅ (spec) | Not started |

**Bottom line**: ~20% of documented architecture is implemented. Kernel + Application + Validation Engine are real. Everything else is documentation-only.

**Engineering debt**: 82% of architecture docs are speculative — describing systems that do not exist in code.

---

## Key Architectural Decisions

| ADR | Decision | Impact |
|-----|----------|--------|
| ADR-0017 | Kernel is control plane only | Kernel code never contains business logic |
| ADR-0018 | Runtime lifecycle via LifecycleAware | All components follow init→start→shutdown |
| ADR-0008 | Context is dynamic, references-not-copies, objective-scoped | Context lives only for current objective duration |
| ADR-0019 | Consumer Independence | Capabilities expose public contracts; consumers never depend on internals |
| ADR-0022 | Validation Engine is reusable deterministic infrastructure | ValidationEngine in code is pure evaluation, no side effects |
| ADR-0025 | Evidence/Assessment decomposition | Replaced M6 Observation Model; EQ-0011 boundary follows this |
| ADR-0021 | Contract-first capability engineering | Both implemented capabilities have contracts before code |

---

## Architecture Debt & Risks

1. **82% of documented architecture is unimplemented** — creates confusion between "designed" and "built"
2. **Empty directories** misleadingly suggest implemented engines (`engines/builder/`, `costing/`, etc.)
3. **Unresolved reference**: "Result Framework" in `docs/05_Data_Flow.md` has no corresponding document or code
4. **No test suite** for production code (Kernel, Application, ValidationEngine)
5. **Speculative engine docs** may drift from eventual implementation — ADRs should govern, not framework docs

---

## Dependencies

```
00_Vision → 01_Principles → 02_Blueprint → 04_Kernel → 05_Data_Flow → ADRs → Implementation
```

---

## References

- `docs/02_System_Blueprint.md` — Full system blueprint
- `docs/04_Platform_Kernel.md` — Kernel specification
- `docs/05_Data_Flow.md` — Data flow lifecycle
- `docs/06_Context_Engine.md` through `docs/22_GUI_Framework.md` — Engine/framework specs (mostly speculative)
- `src/jarvis/core/jarvis/kernel.py` — Kernel implementation
- `src/jarvis/application/application.py` — Application implementation
- `src/jarvis/engines/validation/engine.py` — Validation Engine implementation
- ADRs: 0008, 0017, 0018, 0019, 0021, 0022, 0025
- `docs/knowledge/Appendices/B_ADR_Registry.md` — All 26 ADRs summarized
- `docs/knowledge/10_Implementation_Status.md` — Detailed implementation status

---

## Verification Status

| Source | Status |
|--------|--------|
| Kernel, Application, ValidationEngine | **Implementation-Backed** (code exists) |
| `docs/04_Platform_Kernel.md` | **Implementation-Backed** (matches code) |
| `docs/02_System_Blueprint.md` | AI-Generated, Pending Verification |
| `docs/05_Data_Flow.md` | AI-Generated, Pending Verification |
| Engine framework docs (06-22) | **Speculative** (82% unimplemented) |
| Relevant ADRs | **Project Owner Verified** (Accepted) |

---

**Generated**: 2026-07-15 | **Part of**: Jarvis Knowledge Consolidation