# EV-A102: Interactive Textual Workbench TUI — Evidence

**Status:** VERIFIED
**Date:** 2026-07-30
**Paired Plan:** EP-A102
**Paired Spec:** ES-A102
**Milestone:** Track A2
**Owner:** Product Engineering

---

## 1. Implementation Summary

| File | Purpose |
|------|---------|
| `src/jarvis/ui/textual/app.py` | TextualWorkbenchApp (duck-typed WorkbenchView) |
| `src/jarvis/ui/textual/controller.py` | InteractionController |
| `src/jarvis/ui/textual/sink.py` | TextualInteractionSink |
| `src/jarvis/ui/textual/widgets/header.py` | WorkflowHeaderWidget |
| `src/jarvis/ui/textual/widgets/inspector.py` | FindingInspectorWidget |
| `src/jarvis/ui/textual/widgets/viewer.py` | EvidenceViewerWidget |
| `src/jarvis/ui/textual/widgets/chat.py` | GroundedChatWidget |
| `src/jarvis/ui/textual/screens/main_screen.py` | MainWorkbenchScreen |
| `src/jarvis/cli/main.py` | Added --tui flag to workbench |

---

## 2. Test Results

| Suite | Count | Result |
|---|---|---|
| EP-A102 TUI tests | 10 | **PASS** |
| EP-A101 CLI tests | 34 | **PASS** (regression) |
| EP-1100 evaluation | 19 | **PASS** (regression) |
| EP-1006 workbench | 45 | **PASS** (regression) |
| Combined | 108 | **PASS** |

---

## 3. Acceptance Criteria

| AC | Criterion | Status | Evidence |
|----|-----------|--------|----------|
| AC-1 | Protocol Compliance | PASS | Duck-typed WorkbenchView (render + set_headless) |
| AC-2 | Pure VM Rendering | PASS | render() takes immutable WorkbenchViewModel, no mutation |
| AC-3 | Bidirectional Navigation | PASS | InteractionController routes to Sink to Orchestrator |
| AC-4 | Grounded Chat Interactivity | PASS | GroundedChatWidget + Input field via controller |
| AC-5 | Canonical Pipeline | PASS | Orchestrator supports Bind→Validate→Understand→Chat→Inspect |
| AC-6 | One-Way Dependency | PASS | Zero textual imports from capabilities module |
| AC-7 | Regression Protection | PASS | 108 combined tests, zero failures |
| AC-8 | Headless Testing | PASS | 2 async Textual pilot tests pass |
| AC-9 | Deterministic Rendering | PASS | Same VM renders idempotently |

## 4. Architectural Notes

- `TextualWorkbenchApp` cannot subclass both `App` and `WorkbenchView(Protocol)`
  due to metaclass conflict. Duck-typing satisfies the protocol contract instead.
- All widgets accept `update_view_model()` methods receiving immutable ViewModels.
- Headless mode returns immediately for test runners.

## 5. CLI Integration

`jarvis workbench --tui` launches the interactive Textual TUI.

## 6. Recommendation

**EV-A102 may be promoted.** All acceptance criteria pass with headless test
coverage and zero regression impact on existing M10.6/M11.0/Track A1 suites.