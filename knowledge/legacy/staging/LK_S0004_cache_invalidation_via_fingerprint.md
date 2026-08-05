# Staged Knowledge Candidate: Preview Cache Invalidation via Plan Fingerprint (ID: LK_S0004)

## Metadata
* **ID:** LK_S0004
* **Title:** Preview Cache Invalidation via Plan Fingerprint
* **Knowledge Category:** Architecture
* **Status:** STAGED

## Description
To prevent stale preview displays, the client app computes a plan signature (fingerprint) covering the functional inputs: trade, function, custom quantity, unit, zone configurations, level sheets, and active excel workbook. The preview state is cached. Whenever a user types 'Preview', the cached views are opened only if the active plan's fingerprint matches the stored preview configuration, otherwise the cache is invalidated and a fresh compile is triggered.

## Rationale
Avoids rendering and displaying mismatching or out-of-date sheet configurations. For instance, if a user changes the active trade from 'Wall Types' to 'Structural Steel', typing 'Preview' must not display details of the old 'Wall Types' sheet cached in memory.

## Provenance
* **Primary Source:** `knowledge/legacy/intake/workshop/Jarvis Workshop at Home 11052026.zip`
* **Secondary Sources:** `Dhanrick_Jarvis_v4_5_1_24_2B_Preview_Cache_Export_Restore_Level_Reducer_Fix.zip/Dhanrick_AI_Workbench/JARVIS_v4_5_1_24_2B_CHANGE_REPORT.md (Issue 2)`
* **Archive:** `Dhanrick_Jarvis_v4_5_1_24_2B_Preview_Cache_Export_Restore_Level_Reducer_Fix.zip`
* **Version:** `v4.5.1.24.2B`
* **Confidence:** High
* **Extraction Method:** AI Assisted
