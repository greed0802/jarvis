# Canonical Knowledge Migration Plan

## Scope
The migration plan defines the sequence of operations to promote staged candidates under `knowledge/legacy/staging/` to the canonical records in `knowledge/jarvis/` once approved.

## Phase 1: Interaction & Response Refinement
* **Target Files:**
  - `knowledge/jarvis/Interaction_Policy.md`
  - `knowledge/jarvis/Response_Policy.md`
* **Staged Content:**
  - Integrate `LK_S0001` (retention of clarification card logic when user inputs non-keyword description strings).
  - Integrate `LK_S0010` (handling bidirectional aliases inside prompts).
  - Integrate `LK_S0012` (telemetry disclosure gate blocking support logs during transaction calls).

## Phase 2: Workflow Expansion
* **Target Files:**
  - `knowledge/jarvis/Engineering_Workflows.md`
* **Staged Content:**
  - Add subsection for **Plan amendments continuity** (`LK_S0002`) protecting level/zone selections when trades shift.
  - Detail sequential range parser capabilities (`LK_S0005`), multiline text splitter rules (`LK_S0007`), and restore state rehydration link parameters (`LK_S0011`).

## Phase 3: Architectural State Standards
* **Target Files:**
  - `knowledge/jarvis/Architecture.md`
* **Staged Content:**
  - Document the **Snapshot Pattern** (`LK_S0003`) locking runtime operations away from UI variables.
  - Document signature calculation algorithm for cache invalidation (`LK_S0004`).
  - Document the roles of evidence-only check engines (`LK_S0008`) for boundary testing.

## Phase 4: Product Version Policy
* **Target Files:**
  - `knowledge/jarvis/Version.md`
  - `knowledge/jarvis/Limitations.md`
* **Staged Content:**
  - Implement release validation requirements (`LK_S0009`), verifying route/middleware counts, and closed workbook switches.
  - Document integrity check gates (`LK_S0006`) blocking downstream excel compile workflows.
