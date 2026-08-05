# Staged Knowledge Candidate: Snapshot-Driven Preview and Export Execution (ID: LK_S0003)

## Metadata
* **ID:** LK_S0003
* **Title:** Snapshot-Driven Preview and Export Execution
* **Knowledge Category:** Architecture
* **Status:** STAGED

## Description
The workspace build run depends on a locked state snapshot ('builder_run_snapshot') compiled from the active plan, active workbook, and active levels. Whenever a preview or run request is made, both the frontend payload and backend validation must prioritize this frozen snapshot over mutable UI workspace parameters or default fallbacks. If dynamic hierarchies exist, the export requests must force a 'rebuild' token initialization to preserve state.

## Rationale
Enforces complete execution determinism. Decoupling the execution backend from live, shifting frontend elements prevents user edits during calculations from introducing race conditions, cache leaks, or configuration drift in output documents.

## Provenance
* **Primary Source:** `knowledge/legacy/intake/workshop/Jarvis Workshop at Home 11052026.zip`
* **Secondary Sources:** `Dhanrick_Jarvis_v4_5_1_24_1_Preview_State_Support_Log_Snapshot_Fix.zip/Dhanrick_AI_Workbench/JARVIS_v4_5_1_24_1_CHANGE_RECORD.md`
* **Archive:** `Dhanrick_Jarvis_v4_5_1_24_1_Preview_State_Support_Log_Snapshot_Fix.zip`
* **Version:** `v4.5.1.24.1`
* **Confidence:** High
* **Extraction Method:** AI Assisted
