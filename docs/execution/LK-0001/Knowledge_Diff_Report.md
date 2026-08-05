# Knowledge Diff Report

## Mapping Legacy Candidates to Canonical Base
This report matches the staged candidate items against the canonical folder files located in `knowledge/jarvis/`.

### 1. Interactions & Clarification Cards
* **Legacy Staged Candidates:**
  - `LK_S0001` (Clarification Card input retention)
  - `LK_S0010` (Bidirectional Mezzanine aliases)
* **Canonical Base:** `knowledge/jarvis/Interaction_Policy.md` / `knowledge/jarvis/Response_Policy.md`
* **Mismatch/Delta:** Existing policies specify greeting and fallback behavior guidelines, but lack instructions on preserving input states inside builder-specific clarification cycles.

### 2. Workspace Workflow & Mappings
* **Legacy Staged Candidates:**
  - `LK_S0002` (Active plan modification zone preservation)
  - `LK_S0005` (Level parser ranges GF to Level X)
  - `LK_S0007` (Multiline zone splitter boundaries)
  - `LK_S0011` (Task state recovery & rehydration url links)
* **Canonical Base:** `knowledge/jarvis/Engineering_Workflows.md`
* **Mismatch/Delta:** Canonical workflows describe new project setups and BOQ checks abstractly, but omit operational behaviors of level reducers, active workspace state persistence on page reloads, and multi-line text parsing triggers.

### 3. Builder Run Architecture
* **Legacy Staged Candidates:**
  - `LK_S0003` (Snapshot-driven run states)
  - `LK_S0004` (Preview cached inputs fingerprinting signature)
  - `LK_S0006` (Unsafe preview export blocking gates)
* **Canonical Base:** `knowledge/jarvis/Architecture.md`
* **Mismatch/Delta:** Core architecture contains conceptual block diagrams, but does not specify input caching signatures or run snapshots used to guarantee immutability against UI drift.

### 4. Release Registry Verification
* **Legacy Staged Candidates:**
  - `LK_S0008` (Evidence-only negative assertion boundaries)
  - `LK_S0009` (Release metrics: route counts, middleware counts, kill switches)
  - `LK_S0012` (Support Log telemetry suppress logic)
* **Canonical Base:** `knowledge/jarvis/Version.md` / `knowledge/jarvis/Limitations.md`
* **Mismatch/Delta:** Base versions document stability status and constraints but omit release validation gates (monitoring route counts and enforcing Excel kill-switches prior to human acceptance checks).
