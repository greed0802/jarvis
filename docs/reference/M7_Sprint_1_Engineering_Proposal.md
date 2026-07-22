# M7 Sprint 1 — Engineering Question Discovery

**Date**: 2026-07-13  
**Sprint**: M7 — Context Engine Runtime, Sprint 1  
**Classification**: Engineering Research  
**Author**: Implementation Engineer (Cline)

---

## Existing Engineering Questions Checked

This proposal was written after reviewing the current engineering knowledge state:

- **EQ-0005**: BOQ semantic generalization — evidence complete, pending Project Owner disposition
- **EQ-0007**: Minimum deterministic production BOQ extraction — answered
- **ADR-0025**: Observation Runtime architecture rejected
- **Repository Knowledge Preservation Strategy**: Draft v1.0 (RFC)

No existing Engineering Question addresses what observable information can be assembled from the current production pipeline, or whether that information satisfies the architectural definition of Context.

---

## 1. Repository Architecture Review

### Sources Reviewed

- `00_Vision.md` — Vision statement, guiding philosophy ("Understand before planning")
- `01_Principles.md` — Principle 5 (Evidence Before Assumptions), Principle 6 (Modular Architecture)
- `02_System_Blueprint.md` — High-level architecture: Context Engine is first Core Runtime Engine in Data Plane
- `03_Core_Ontology_Relationships.md` — Context: "What information is relevant right now?"; Context references Resources, Memory, Knowledge, Workspace, Project, User, Organization, Intent
- `04_Platform_Kernel.md` — Control Plane / Data Plane separation; Kernel never creates Context
- `05_Data_Flow.md` — Understanding Flow: User Request → Intent → Context → Planner; Context Engine assembles Context by referencing Resources, Memory, Knowledge, Workspace, Project, User, Runtime metadata
- `06_Context_Engine.md` — Context Engine definition, scope, ownership, composition, lifecycle
- ADR-0008 (Context) — Context is dynamically assembled, stores references instead of copies
- ADR-0022 (Context Lifecycle and Ownership) — Context Engine sole owner of Context; lifecycle: Assembly → Evaluation → Availability → Refresh → Disposal; Workflow Engine triggers refresh

### What Context Is Architecturally Intended to Represent

Context is a **temporary, assembled understanding** of the information relevant to the current objective. It:

- References information rather than duplicating it
- Exists only for the lifetime of the current objective
- Is assembled from Resources, Memory, Knowledge, Workspace, Project, User, Organization, and Runtime metadata
- Is produced by the Context Engine and consumed by the Planner Engine
- Is refreshed only when the Workflow Engine requests it

### What Parts of That Design Are Already Supported

| Architectural Concept | Supported by Production? | Evidence |
|----------------------|--------------------------|----------|
| Data Plane entry point | No | No Context Engine exists; no Data Plane entry path defined |
| Context referencing Resources | No | No Resource Framework exists |
| Context referencing Memory | No | No Memory Framework exists |
| Context referencing Knowledge | No | No Knowledge Framework exists |
| Context referencing Workspace/Project/User | No | No workspace/project/user concepts exist in code |
| Context referencing Runtime metadata | **Partial** | Kernel exists (Control Plane), but exposes no Data Plane metadata |
| Intent interpretation | No | No user request pipeline exists; no Intent type |
| Context lifecycle (Assembly → Availability → Disposal) | No | No lifecycle implemented |

### What Assumptions Remain Unvalidated

1. **Whether parser output alone can contribute to Context** — The architecture assumes Context draws from many sources (Resources, Memory, Knowledge, etc.), none of which exist. Parser output is only one possible Context source. It is unknown whether parser-derived structured data alone constitutes sufficient observable information for any objective.

2. **Context-as-references vs. Context-as-data** — ADR-0008 states Context stores "references instead of copies." But with no Memory or Knowledge frameworks, there is nothing to reference. Any assembled information will necessarily be embedded data, not references.

3. **Intent is meaningful without a Planner** — The architecture states Intent flows to Planner, which then creates a Plan. But at current maturity, no Planner exists. Intent interpretation without a downstream Planner may be architecturally incoherent — it produces an artifact with no consumer.

4. **Context refresh requires a Workflow Engine** — ADR-0022 explicitly ties refresh to the Workflow Engine. Without a Workflow Engine, Context either never refreshes (static) or refreshes without coordination (violating ADR-0022).

5. **"Objective" is undefined** — Context exists for the lifetime of "the current objective." No definition of what constitutes an objective exists in code or documentation.

---

## 2. Production State Review

### Production Artifacts That Could Contribute Observable Information

| Artifact | Purpose | Relevance | Observable Capability |
|----------|---------|-----------|----------------------|
| `WorkbookParser` | Load + validate CostX BOQ workbooks | **High** — validates a source file before extraction | Validates workbook has exactly one "CostX" worksheet, not empty |
| `extract_boq()` | Extract structured BOQ rows from validated workbook | **High** — produces the first structured data available to the Data Plane | Produces `list[BOQRow]` with row_number, code, description, quantity, uom, row_type, section |
| `BOQRow` | Structured BOQ row dataclass | **High** — the primary structured data type | 7 fields: row_number, code, description, quantity, uom, row_type, section |
| `Configuration` | Platform configuration (log_level) | **Low** — Control Plane only, no Data Plane fields | Single field: log_level |
| `Kernel` | Control Plane lifecycle manager | **Indirect** — manages component lifecycle | LifecycleAware contract, service registration |
| `Application` | Composition Root | **Indirect** — constructs and registers components | Creates Kernel, registers LoggingService, runs lifecycle |
| `LoggingService` | Platform logging | **None** — utility service only | Logging |

### Key Observation

The parser produces **deterministic structured data** (`list[BOQRow]`) from a **validated source file** (CostX workbook). This is the only data available at current repository maturity.

The parser is **not registered with the Kernel**. It exists as a standalone library function (`extract_boq`), not as a LifecycleAware component. There is no path from the Application/Kernel to parser output.

### What Does Not Exist

- No Context module, class, or interface
- No Intent module, class, or interface
- No Data Plane entry point (no code calls `extract_boq` during platform runtime)
- No Resource abstraction representing a CostX workbook
- No Memory, Knowledge, Workspace, Project, or User concepts
- No Planner, Workflow, or Skill engines
- No user request pipeline

---

## 3. Proposed M7 Engineering Question

**EQ-0009: What observable information can be deterministically assembled from the current production pipeline, and does that satisfy the architectural definition of Context?**

### Motivation

The architecture defines Context as the first Data Plane engine, consumed by the Planner Engine. No Planner exists. **Context has no consumer at current repository maturity.** This is the fundamental reason M7 exists — to discover what observable information is actually available before any investment in downstream engines.

### Why This Question

Every architectural reference to Context assumes downstream components (Planner, Workflow), cross-cutting frameworks (Memory, Knowledge, Resources), and a user request pipeline — none of which exist.

This question does not assume Context exists or that BOQRow data constitutes Context. It asks: **What information is actually observable, and does it match the architectural definition?**

### Scope Boundaries

- **In scope**: Discovering what structured information can be assembled from the current production pipeline. Evaluating whether that information satisfies the architectural definition of Context. Testing against `full_boq.xlsx`.
- **Out of scope**: Intent interpretation, Planner, Workflow, Skills, Memory, Knowledge, Resources, AI, user requests. Any architecture not justified by current evidence. Defining a production Context type. Creating a Context Engine.

### Why This Is the Smallest Viable Question

1. It uses **existing parser output** — no new parsing required.
2. It uses **real fixtures** — `full_boq.xlsx` is available.
3. It avoids **all future architecture** — no Planner, Workflow, AI, Memory, Knowledge.
4. It is **answerable by evidence** — either the observable information satisfies the architectural definition, or it does not. Both outcomes are valid engineering results.
5. It **does not assume the answer** — the spike discovers what information emerges. The report evaluates.

### What This Question Does NOT Do

- Does NOT implement the Context Engine from `06_Context_Engine.md`
- Does NOT create Intent, Planner, Workflow, or any downstream engine
- Does NOT create Resource, Memory, or Knowledge frameworks
- Does NOT define ontology for Context
- Does NOT create interfaces for future architecture
- Does NOT introduce abstractions without evidence
- Does NOT assume BOQRow data constitutes Context

---

## 4. Engineering Spike Design

### Spike Name

**Context Discovery Spike**

This spike is explicitly investigative and the spike shall not be interpreted as defining production architecture.

### Objective

Discover what structured information can be deterministically assembled from the current production pipeline, without pre-selecting statistics, summaries, or any specific data shape. The spike discovers. The evidence report evaluates.

### Spike Script

A single Python script (`tools/context_discovery_spike.py`) that:

1. **Loads** `full_boq.xlsx` using `WorkbookParser.load()`
2. **Validates** using `WorkbookParser.validate()`
3. **Extracts** BOQ rows using `extract_boq(workbook)`
4. **Discovers** what information naturally emerges from the extraction output — without pre-selecting statistics, summaries, row counts, section counts, or metadata. The spike observes, it does not predict.
5. **Assembles** a candidate structured information model from the discovered observations.
6. The spike script documents what was observable and what was not. **Evaluation** — whether the assembled information satisfies the architectural definition of Context — belongs to the evidence report, not the spike script. The spike discovers. The report evaluates.

### Spike Design Constraints

- Single flat script — no classes, no interfaces, no abstractions
- No registration with Kernel (spike is investigative, not production)
- No new types in `src/jarvis/` (spike stays in `tools/`)
- Uses only existing production imports: `WorkbookParser`, `extract_boq`, `BOQRow`
- No speculative architecture
- No pre-selection of what information "should" emerge

### Why a Spike (Not Implementation)

Per the engineering workflow, spikes answer questions before production implementation. This follows the exact pattern that succeeded for BOQ extraction (Spike #1 → EQ-0001/EQ-0002 → EQ-0007 production).

### What the Spike Produces

The spike produces **evidence**, not Context. The spike discovers; the report evaluates. The evaluation of whether the discovered information satisfies the architectural definition of Context belongs to the evidence report, not the spike script. The spike and the report are distinct engineering steps.

---

## 5. Success Criteria

### Evidence Required

1. **Discovery**: The spike observes what structured information can be assembled from `full_boq.xlsx` extraction output without pre-selection.
2. **Determinism**: Two runs on the same fixture produce identical observations.
3. **Gap Analysis**: Document what the architectural definition of Context requires that cannot be satisfied with current production artifacts.
4. **Fixture Verification**: Observations verified against `full_boq.xlsx` (6,349 extracted rows, known classification counts).

### Completion Criteria

| Criterion | Threshold |
|-----------|-----------|
| Spike script runs to completion | Must succeed |
| Observable information documented | Complete inventory of what emerged |
| Determinism verified | Two identical runs → identical output |
| Architectural gap analysis complete | All assumptions from `06_Context_Engine.md` checked against production reality |
| Evidence report published | Report written and committed |

### Failure Conditions

**Falsification is valid evidence.** If the discovered observable information does not satisfy the architectural definition of Context, that answers the Engineering Question. It is not a failure — it is a successful engineering outcome that informs the next question.

Failure to satisfy the architectural definition of Context is considered a successful engineering outcome because it answers the Engineering Question.

If the spike concludes BOQ extraction is insufficient, it shall identify exactly which additional observable information is missing, without proposing architecture to obtain it.

---

## 6. Risks

### Architectural Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| **Scope creep into Planner/Workflow** — The architecture naturally pulls toward "and then plan, and then execute." | Low | Spike constraints explicitly exclude Planner, Workflow, and all downstream engines. |

### Evidence Gaps

| Gap | Impact |
|-----|--------|
| No "objective" concept exists in code | Context is architecturally scoped to an objective, but objectives are undefined. The spike must document whether this prevents assembly. |
| No Resource abstraction for CostX workbook | The architecture assumes Resources as a framework. The spike must treat the workbook path as a raw source identifier. |
| No user request pipeline | Context assembly in the architecture begins with a user request producing Intent. The spike has no user request. Document whether this matters for assembly. |

### Assumptions Requiring Validation

1. **Whether BOQRow data contains enough information to constitute Context** — The architecture envisions Context drawing from many sources. A single parser output may be too narrow. The spike discovers, it does not assume.
2. **Whether "understanding" is measurable from structured data** — The architecture defines Context as "understanding." Whether structured observations constitute "understanding" must be evaluated from evidence, not assumed.
3. **Whether determinism is achievable without a formal Context Engine** — ADR-0022 defines a lifecycle. A flat script has no lifecycle. Whether deterministic output is sufficient must be tested.

---

## 7. Recommendation

### Primary Recommendation

**Proceed with the Context Discovery Spike.**

Rationale:

- The spike is **small** — a single flat script, following the proven Spike #1 pattern.
- The spike is **safe** — it modifies no production code, creates no abstractions, stays in `tools/`.
- The spike **answers a real question** — the architecture says "Context first," but no evidence exists about what observable information is actually available.
- The spike **either validates or falsifies** — either outcome produces actionable evidence.
- The spike **costs almost nothing** — it uses existing fixtures, existing parser, no new dependencies.

### If Observable Information Satisfies the Architectural Definition

The Engineering Question is answered positively. The Project Owner may authorize the next engineering question. No production Context Engine is authorized by this spike alone — exactly as EQ-0005 required Project Owner disposition before any generalization implementation.

### If Observable Information Does Not Satisfy the Architectural Definition

The evidence report documents exactly what is missing. This becomes the basis for the next Engineering Question, potentially addressing the specific gap identified. The Project Owner determines the next investigation.

### What This Sprint Does NOT Recommend

- Skipping the spike and implementing Context directly — violates Evidence Before Assumptions
- Defining a Context Engine specification — premature without evidence
- Creating ontology for Context — violates Evidence Before Promotion
- Introducing Resource, Memory, or Knowledge frameworks — YAGNI; build only what evidence demonstrates is necessary
- Proposing architecture to fill gaps identified by the spike — the spike identifies gaps; architecture responds to Project Owner disposition