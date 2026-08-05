# Staged Knowledge Candidate: Project Level Expression Parser and Reducer (ID: LK_S0005)

## Metadata
* **ID:** LK_S0005
* **Title:** Project Level Expression Parser and Reducer
* **Knowledge Category:** Behavior
* **Status:** STAGED

## Description
Level ranges specified in user commands (such as 'GF to Level 11') are expanded sequentially (GF, L1, L2 ... L11). The level parser is equipped with a custom reducer that permits custom abbreviations (such as 'L11 Mezz' or 'Mezzanine') and prevents early return exits on mezzanine descriptors, ensuring they are compiled into the active run matrix correctly.

## Rationale
Prevents structural parsing errors. Level schemas mapped from drawings often rely on non-standard labels (like Mezzanines). Standard range parsers fail on these exceptions unless protected by a sequential range reducer.

## Provenance
* **Primary Source:** `knowledge/legacy/intake/workshop/Jarvis Workshop at Home 11052026.zip`
* **Secondary Sources:** `Dhanrick_Jarvis_v4_5_1_24_2B_Preview_Cache_Export_Restore_Level_Reducer_Fix.zip/Dhanrick_AI_Workbench/JARVIS_v4_5_1_24_2B_CHANGE_REPORT.md (Issue 3)`
* **Archive:** `Dhanrick_Jarvis_v4_5_1_24_2B_Preview_Cache_Export_Restore_Level_Reducer_Fix.zip`
* **Version:** `v4.5.1.24.2B`
* **Confidence:** High
* **Extraction Method:** AI Assisted
