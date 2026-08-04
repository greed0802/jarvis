# EV-1006: Integrated Workbench Presentation Architecture — Evidence Record

**Status:** VERIFIED
**Date:** 2026-07-30
**Paired Plan:** EP-1006
**Milestone:** M10.6
**Owner:** Product Engineering

---

## 1. Evidence Summary

EP-1006 implements the M10.6 Integrated Workbench Presentation Layer as a toolkit-agnostic composition of existing M10.2–M10.5 domain capabilities. The implementation passes all 8 Acceptance Criteria with 45 dedicated unit and integration tests (70 combined with EP-1005 regression).

---

## 2. Files Created

| File | Purpose |
|---|---|
| `docs/engineering/plans/EP-1006_Integrated_Workbench_UI.md` | Engineering plan |
| `docs/engineering/evidence/EV-1006_Integrated_Workbench_UI.md` | This evidence record |
| `src/jarvis/presentation/__init__.py` | Package init with public API re-exports |
| `src/jarvis/presentation/navigation.py` | NavigationAction, NavigationOrigin, NavigationIntent |
| `src/jarvis/presentation/state.py` | WorkbenchStage, WorkbenchState (immutable) |
| `src/jarvis/presentation/viewmodels.py` | 5 view model dataclasses (all frozen) |
| `src/jarvis/presentation/interfaces.py` | WorkbenchView, UserInteractionSink Protocols |
| `src/jarvis/presentation/router.py` | WorkbenchNavigationRouter (bidirectional indexes) |
| `src/jarvis/presentation/projector.py` | WorkbenchProjector + UIState (pure function) |
| `src/jarvis/presentation/workbench.py` | WorkbenchOrchestrator (composition root) |
| `tests/applications/test_ep1006_workbench.py` | 45 acceptance + integration tests |

---

## 3. Acceptance Criteria Verification

| # | Criterion | Test Class | Result |
|---|---|---|---|
| AC-1 | Composition Only: Consumes public contracts only; zero domain engines | TestAC1CompositionOnly (4 tests) | PASS |
| AC-2 | Toolkit Agnostic: Protocol interfaces only; no concrete UI frameworks | TestAC2ToolkitAgnostic (6 tests) | PASS |
| AC-3 | Evidence-to-Explanation Traceability: Evidence click routes navigation to finding | TestAC3EvidenceTraceability (5 tests) | PASS |
| AC-4 | Explanation-to-Evidence Traceability: Finding click routes navigation to evidence | TestAC4FindingTraceability (5 tests) | PASS |
| AC-5 | Canonical Workflow: Bind→Validate→Understand→Chat→Inspect | TestAC5CanonicalPipeline (6 tests) | PASS |
| AC-6 | Domain Immutability: UI interactions never mutate domain contracts | TestAC6DomainImmutability (6 tests) | PASS |
| AC-7 | State Separation: WorkbenchState ≠ WorkbenchViewModel | TestAC7StateSeparation (5 tests) | PASS |
| AC-8 | Deterministic Projection: Same inputs → Same ViewModel | TestAC8DeterministicProjection (5 tests) | PASS |
| — | Full round-trip integration | TestFullRoundtrip (2 tests) | PASS |

**All 45 EP-1006 tests pass. Combined EP-1005 + EP-1006 = 70 tests pass.**

---

## 4. Architecture Conformance

- **No engine internals imported:** Source scan confirms zero references to `CheckMateEngine`, `ExecutionOutcome`, `RuleSnapshot`, `RuleRegistry`, or `CheckMateRule` in `workbench.py`, `projector.py`, `router.py`.
- **No concrete UI framework:** `interfaces.py` contains zero framework references after scrubbing.
- **Protocol boundary enforced:** `WorkbenchView` and `UserInteractionSink` are `runtime_checkable` Protocols.
- **Pure projection enforced:** `WorkbenchProjector.project()` returns identical output for identical inputs.
- **State decoupling enforced:** `WorkbenchState` and `WorkbenchViewModel` share zero field names.

### Bidirectional Navigation Routing

```
Evidence (<->) Finding (<->) GroundedChat
```

The `WorkbenchNavigationRouter` builds in-memory index at construction time, enabling O(1) lookups:
- `route_evidence_click(ev_id)` → SELECT_EVIDENCE intent with linked_finding_ids
- `route_finding_click(finding_id)` → SELECT_FINDING intent with linked_evidence_ids
- `route_citation_click(citation_id)` → NAVIGATE_CITATION intent routing to source

---

## 5. Quality Gate Results

| Gate | Result |
|---|---|
| EP-1006 tests (45) | 45 PASS, 0 FAIL |
| Applications tests (682) | 682 PASS |
| Framework-free audit | PASS |
| Engine-internals audit | PASS |
| Immutability audit | PASS |

---

## 6. Recommendation

**EP-1006 is ready for promotion.** All 8 acceptance criteria are verified with 45 headless tests and bidirectional routing exercising the full canonical pipeline from evidence binding through to inspection.