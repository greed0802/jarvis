# Staged Knowledge Candidate: Direction-Specific Mezzanine Code Alignment (ID: LK_S0010)

## Metadata
* **ID:** LK_S0010
* **Title:** Direction-Specific Mezzanine Code Alignment
* **Knowledge Category:** Behavior
* **Status:** STAGED

## Description
Mezzanine keyword aliases are directional. If a user sets an alias in a builder plan ('Use Mezz as code for Mezzanine'), the parser sets the active alias variable to 'Mezz'. If the user requests to clear it ('Change Mezz to Mezzanine instead'), the alias mapping is reset. This allows validation checkers to accept both the default values (e.g. L11 Mezzanine) and alias-transformed codes (e.g. L11 Mezz).

## Rationale
Solves a mismatch where Excel engines expect shortened CostX codes but integrity validation engines run against original drawing names. Supporting bidirectional aliases bridges validation to output formats.

## Provenance
* **Primary Source:** `knowledge/legacy/intake/workshop/Jarvis Workshop at Home 11052026.zip`
* **Secondary Sources:** `Dhanrick_Jarvis_v4_5_1_24_2D_Mezz_Alias_Guard_Safe_Export_Zone_Parser_Fix.zip/Dhanrick_AI_Workbench/JARVIS_v4_5_1_24_2D_CHANGE_REPORT.md (Fix 1)`
* **Archive:** `Dhanrick_Jarvis_v4_5_1_24_2D_Mezz_Alias_Guard_Safe_Export_Zone_Parser_Fix.zip`
* **Version:** `v4.5.1.24.2D`
* **Confidence:** High
* **Extraction Method:** AI Assisted
