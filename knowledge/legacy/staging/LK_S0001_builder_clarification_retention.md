# Staged Knowledge Candidate: Builder Clarification Card Input Retention (ID: LK_S0001)

## Metadata
* **ID:** LK_S0001
* **Title:** Builder Clarification Card Input Retention
* **Knowledge Category:** Behavior
* **Status:** STAGED

## Description
During interactive chat workflows, if the system is waiting for a clarification response in the builder task, the query router must avoid premature fallback or generalized AI routing. Specifically, if the user replies with a non-keyword string (e.g. details of zones, choices, or custom values for a clarification card), the router is forced to catch the response, re-wrap the pending clarification state, and keep the clarification option drawer/card open rather than reverting to general AI.

## Rationale
Ensures that specialized multi-step form-filling loops (like setting up levels, files, or scopes) are robust and cannot be broken by conversational statements or custom user input that doesn't trigger standard keywords.

## Provenance
* **Primary Source:** `knowledge/legacy/intake/workshop/Jarvis Workshop at Home 11052026.zip`
* **Secondary Sources:** `Dhanrick_Jarvis_v4_5_1_24_2A_Snapshot_Slot_Memory_Export_State_Hotfix.zip/Dhanrick_AI_Workbench/JARVIS_v4_5_1_24_CHANGE_RECORD.md (Bug 1)`
* **Archive:** `Dhanrick_Jarvis_v4_5_1_24_2A_Snapshot_Slot_Memory_Export_State_Hotfix.zip`
* **Version:** `v4.5.1.24`
* **Confidence:** High
* **Extraction Method:** AI Assisted
