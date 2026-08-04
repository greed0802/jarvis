# ES-A102: Interactive Textual Workbench TUI Specification

**Status:** Active
**Date:** 2026-07-30
**Paired Plan:** EP-A102
**Evidence:** EV-A102
**Owner:** Product Engineering

---

## 1. Widget Specification

| Widget | Renders From | Keybindings |
|--------|-------------|-------------|
| WorkflowHeaderWidget | WorkflowStatusViewModel | None (display only) |
| FindingInspectorWidget | FindingInspectorViewModel[] | Enter=select, Esc=clear |
| EvidenceViewerWidget | EvidenceViewerViewModel[] | Enter=select, Esc=clear |
| GroundedChatWidget | GroundedChatViewModel[] | Enter=submit, Ctrl+C=citation |

---

## 2. Screen Layout

```
+--------------------------------------+
|         WorkflowHeaderWidget         |
+------------+------------+------------+
| Finding    | Evidence   | Chat       |
| Inspector  | Viewer     | Widget     |
| Widget     | Widget      |           |
+------------+------------+------------+
```

---

## 3. Interaction Flow

1. User clicks/focuses a finding → FindingInspector emits selection
2. Controller dispatches `on_select_finding` → sinks to orchestrator
3. Orchestrator produces new WorkbenchViewModel with highlighted evidence
4. Widgets re-render from the new ViewModel

---

## 4. Headless Testing Mode

App.set_headless(True) disables rendering. Widgets still emit
Controller dispatches deterministically. Test pilot verifies state.