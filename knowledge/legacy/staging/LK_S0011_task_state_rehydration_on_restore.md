# Staged Knowledge Candidate: Active Task State and Download Link Rehydration (ID: LK_S0011)

## Metadata
* **ID:** LK_S0011
* **Title:** Active Task State and Download Link Rehydration
* **Knowledge Category:** Workflow
* **Status:** STAGED

## Description
When reload occurs or recovery UI triggers conversation restore, active task properties must preserve completed statuses such as 'export_ready'. The rehydration logic must query active job databases, restore the download URL ('activeConversationTask.last_export_job.result.download_url'), and display download cards to the user immediately, rather than reverting the task state block to 'Approve & Preview'.

## Rationale
Prevents forcing the user to re-run expensive calculations or export actions when they refresh their browser window. Once an export succeeds, the download link remains stable across page refreshes.

## Provenance
* **Primary Source:** `knowledge/legacy/intake/workshop/Jarvis Workshop at Home 11052026.zip`
* **Secondary Sources:** `Dhanrick_Jarvis_v4_5_1_24_2B_Preview_Cache_Export_Restore_Level_Reducer_Fix.zip/Dhanrick_AI_Workbench/JARVIS_v4_5_1_24_2B_CHANGE_REPORT.md (Issue 1)`
* **Archive:** `Dhanrick_Jarvis_v4_5_1_24_2B_Preview_Cache_Export_Restore_Level_Reducer_Fix.zip`
* **Version:** `v4.5.1.24.2B`
* **Confidence:** High
* **Extraction Method:** AI Assisted
