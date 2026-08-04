# EP-1001: M10.1 — Minimum Executable Application Shell & Workspace

**Status:** OPEN
**Date:** 2026-07-29
**Milestone:** M10.1
**Authors:** Product Engineering
**Frozen ADR Baseline:** ADR-0027, ADR-0028, ADR-0029, ADR-0030, ADR-0031, ADR-0032
**Playbook Reference:** `docs/engineering/Engineering_Execution_Playbook.md`

---

## 1. Objective

Establish the minimum executable desktop application shell capable of hosting
future capabilities while proving compliance with frozen architectural
boundaries (ADR-0027 through ADR-0032).

This EP delivers the foundational scaffold that confirms:
- The application can launch, initialize a workspace, and present a
  navigation layout.
- Capability hosting boundaries are enforced from first boot.
- No architectural invariants from ADR-0027 through ADR-0032 are violated
  in the application shell layer.

---

## 2. Scope & Deliverables

| # | Deliverable | Description |
|---|-------------|-------------|
| 1 | Application shell window | Launchable desktop window with capability host layout |
| 2 | Local workspace initialization | On first launch, initialize a local workspace directory structure |
| 3 | Navigation layout | Sidebar or toolbar navigation shell capable of hosting capability views |
| 4 | Capability host interface | A technology-agnostic interface definition for mounting capability panels |
| 5 | Workspace evidence binding stub | A workspace binding mechanism that establishes a local evidence context (stub only) |
| 6 | FindingReport interface stub | A typed interface stub conforming to the ADR-0031 public contract schema |

---

## 3. Architecture Traceability Matrix

| ADR Reference | Decision / Invariant | Planned Implementation | Verification |
|---------------|---------------------|----------------------|-------------|
| ADR-0027 | Capability Planning Boundary | Application shell hosts capability panels via declared interface; no cross-capability coupling | Boundary conformance test: capability panels cannot call each other directly |
| ADR-0028 | Execution Runtime Lifecycle | Application shell initializes runtime context on launch and disposes on close; no persistent background workers in M10.1 | Startup/shutdown lifecycle test |
| ADR-0029 | Durable Execution Journal | Workspace directory structure includes journal storage location; journal is not populated in M10.1 (stub) | Directory structure verification |
| ADR-0030 | Capability Boundary & Non-Goals | Application shell enforces CheckMate as a consumer of workspace evidence; no parser or summarization logic in shell layer | Boundary conformance test: no BOQ parser import in shell layer |
| ADR-0031 | Public Contract Decoupling — FindingReport | FindingReport interface stub typed per ADR-0031 4-tier schema; no internal telemetry exposed | Type conformance test against ADR-0031 schema |
| ADR-0032 | RuleSnapshot Sovereignty — Evidence Binding | Workspace evidence binding initializes an immutable evidence context at workspace open; evidence cannot be modified after binding | Immutability test: post-binding evidence write returns error |

---

## 4. Out of Scope

The following are explicitly excluded from EP-1001:

| Excluded Concern | Reason |
|-----------------|--------|
| Modifying or amending ADR-0027 through ADR-0032 | EPs have zero architectural authority |
| Full rule evaluation engine implementation | Deferred to subsequent EPs per rule taxonomy (ADR-0030, ADR-0032) |
| FindingReport population or CheckMate evaluation logic | Capability implementation deferred to M10.2+ |
| Direct LLM prompt integrations or AI Assistant wiring | M10 Product Workbench concern; not a shell concern |
| PDF rendering or display components | Delegated to M10 Product Workbench (ADR-0030 Out of Scope) |
| Specific UI framework selection as an architectural contract | UI framework selection is an implementation detail, not an architectural boundary |
| Live BOQ Intelligence parser execution | CheckMate is a consumer layer; parsing is upstream of M10.1 scope |
| Hardcoding third-party rendering engines into the public contract | ADR-0031 mandates technology-agnostic public contract |

---

## 5. Acceptance Criteria

| # | Criterion | Pass Condition |
|---|-----------|---------------|
| AC-1 | Application launches cleanly | App starts without exceptions, workspace directory is created |
| AC-2 | Workspace initialization | On first run, workspace directory structure including journal stub location is created |
| AC-3 | Navigation layout renders | Capability host layout renders with placeholder navigation |
| AC-4 | Capability host interface is defined | A typed interface definition for capability panels exists and is import-safe |
| AC-5 | FindingReport interface stub conforms | FindingReport stub matches ADR-0031 4-tier schema (Provenance, Telemetry Summary, Actionable Findings, Domain Coverage) |
| AC-6 | Evidence binding immutability | Post-binding evidence write returns an explicit error or is prohibited by type |
| AC-7 | No cross-capability coupling | Capability panels in the shell cannot directly import or invoke each other |
| AC-8 | Documentation verifier passes | `tools/quality/verify_documentation.py` exits with code 0 |

---

## 6. Quality Gates

The following gates MUST pass before code review:

| Gate | Tool / Command | Required Result |
|------|---------------|----------------|
| Documentation verifier | `python tools/quality/verify_documentation.py` | Exit code 0 |
| Unit tests | Project test runner | All pass |
| Type conformance | Static type checker (project-configured) | Zero type errors |
| Import boundary check | Automated import analysis | No cross-capability direct imports |

---

## 7. Engineering Debt

| ID | Description | Resolution Path |
|----|-------------|----------------|
| ED-001 | FindingReport interface is a stub only; no runtime population | Future EP when CheckMate evaluation engine is implemented |
| ED-002 | Evidence binding produces immutable context but is unpopulated | Future EP when BOQ Intelligence evidence integration is implemented |
| ED-003 | Journal storage location established but journal not activated | Future EP implementing ADR-0029 durable execution journal |

---

## 8. Completion Record

| Field | Value |
|-------|-------|
| **Completed Date** | |
| **ADR Baseline Verified** | ADR-0027 through ADR-0032 |
| **Quality Gate Result** | |