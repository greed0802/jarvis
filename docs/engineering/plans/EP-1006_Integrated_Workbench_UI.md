# EP-1006: Integrated Workbench Presentation Architecture

**Status:** Active  
**Milestone:** M10.6  
**Owner:** Product Engineering  
**Evidence ID:** EV-1006  
**Date:** 2026-07-30  

---

## Objective

Implement the M10.6 Integrated Workbench Presentation Layer by composing existing M10.2–M10.5
domain capabilities into a toolkit-agnostic presentation architecture. This plan defines the
contracts, state model, view models, navigation routing, pure-function projector, and
orchestrator that form the M10.6 presentation boundary.

---

## Architectural Position

```
M10.1 (Bootstrap)
    ↓
M10.2 (Evidence)          → EvidenceStore / EvidenceRepository
    ↓
M10.3 (Validation)        → CheckMateEngine / FindingReportAssembler
    ↓
M10.4 (Understanding)     → ProjectUnderstandingService
    ↓
M10.5 (Assistant)         → AssistantService
    ↓
M10.6 (Presentation)      ← EP-1006 (this plan)
    ↓
M10.7+ (Concrete UI)
```

EP-1006 sits at M10.6 — it composes domain services but introduces zero domain logic.
All domain contracts (FindingReport, ProjectUnderstanding, AssistantResponse) remain
immutable; the presentation layer only projects them into view models.

---

## Toolkit Agnosticism Invariant

EP-1006 MUST NOT introduce any concrete UI framework dependency.

All UI surfaces are defined as Python `Protocol` interfaces in `interfaces.py`.
Concrete UI implementations (Qt, Textual, React, Tauri, CLI) belong to M10.7+.

---

## Acceptance Criteria

| ID    | Criterion                                                                                        |
|-------|--------------------------------------------------------------------------------------------------|
| AC-1  | Workbench consumes only existing public capability contracts and services; introduces zero domain-level engines. |
| AC-2  | Presentation layer relies strictly on Python Protocol interfaces; zero dependencies on concrete UI frameworks. |
| AC-3  | Selecting an evidence citation generates a NavigationIntent that routes navigation to the target EvidenceReference. |
| AC-4  | Selecting a finding generates a NavigationIntent routing to all associated evidence and chat explanations. |
| AC-5  | WorkbenchOrchestrator successfully executes the complete pipeline: Bind → Validate → Understand → Chat → Inspect. |
| AC-6  | UI interactions (filtering, selecting, expanding) leave underlying domain contracts strictly unmutated. |
| AC-7  | WorkbenchState (domain/workflow state) and WorkbenchViewModel (presentation state) are strictly decoupled. |
| AC-8  | Given identical inputs, WorkbenchProjector produces identical WorkbenchViewModel instances (pure function projection). |

---

## Implementation Steps

### Step 1 — Navigation Contracts & Domain State
- `src/jarvis/presentation/navigation.py`
  - `NavigationAction` (Enum): SELECT_EVIDENCE, SELECT_FINDING, NAVIGATE_CITATION, CLEAR_SELECTION
  - `NavigationOrigin` (Enum): INSPECTOR, EVIDENCE_VIEWER, GROUNDED_CHAT
  - `NavigationIntent` (frozen dataclass)
- `src/jarvis/presentation/state.py`
  - `WorkbenchStage` (Enum)
  - `WorkbenchState` (frozen dataclass)

### Step 2 — View Models & Presentation Interfaces
- `src/jarvis/presentation/viewmodels.py`
  - `FindingInspectorViewModel`, `EvidenceViewerViewModel`, `GroundedChatViewModel`
  - `WorkflowStatusViewModel`, `WorkbenchViewModel`
- `src/jarvis/presentation/interfaces.py`
  - `WorkbenchView` (Protocol)
  - `UserInteractionSink` (Protocol)

### Step 3 — Navigation Router
- `src/jarvis/presentation/router.py`
  - `WorkbenchNavigationRouter`
  - Bidirectional: Evidence ⇄ Finding ⇄ Chat

### Step 4 — Projector & Orchestrator
- `src/jarvis/presentation/projector.py`
  - `WorkbenchProjector` (pure function)
- `src/jarvis/presentation/workbench.py`
  - `WorkbenchOrchestrator`

### Step 5 — Verification Tests
- `tests/applications/test_ep1006_workbench.py`
  - AC-1 through AC-8 coverage

---

## Dependency Map

```
src/jarvis/presentation/ (EP-1006)
    imports from:
        jarvis.contracts.capabilities      (EvidenceReference, Finding, FindingReport)
        jarvis.contracts.understanding     (UnderstandingFinding, ProjectUnderstanding)
        jarvis.contracts.assistant         (AssistantResponse, GroundingStatus)
        jarvis.engines.understanding       (ProjectUnderstandingService)
        jarvis.engines.assistant           (AssistantService)
        jarvis.engines.checkmate           (CheckMateEngine, FindingReportAssembler)
        jarvis.platform.evidence           (EvidenceStore, FileEvidenceRepository)
```

---

## Architecture Invariants

1. **No domain mutation**: The projector reads domain contracts; it NEVER writes to them.
2. **Protocol boundary**: All view surfaces are Protocols; no concrete framework imports.
3. **Pure projection**: WorkbenchProjector is a pure function — same inputs → same outputs.
4. **State decoupling**: WorkbenchState and WorkbenchViewModel are separate types with no shared fields.
5. **Router responsibility**: The router produces NavigationIntent objects; it does NOT update state directly.

---

## Engineering Debt Pre-Assessment

- The `WorkbenchOrchestrator` in AC-5 requires a real or mocked execution pipeline.
  For EP-1006, a mock/stub pipeline is acceptable given M10.7 is not yet complete.
- Bidirectional evidence-finding correlation (AC-3, AC-4) is index-based; full-text search
  is deferred to M10.7+.

---

## Evidence Reference

Upon completion: `docs/engineering/evidence/EV-1006_Integrated_Workbench_UI.md`