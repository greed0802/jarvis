# Staged Knowledge Candidate: Multiline Zone Description Parser Boundaries (ID: LK_S0007)

## Metadata
* **ID:** LK_S0007
* **Title:** Multiline Zone Description Parser Boundaries
* **Knowledge Category:** Behavior
* **Status:** STAGED

## Description
In command texts containing grouped settings (e.g. mapping levels/zones across breaks), description values often extend across multiple lines. The text parser splits inputs cleanly by stopping description field capture for a given zone index instantly when a newline is succeeded by a new zone flag (e.g. 'Zone N:'). This halts parser 'runaway' where subsequent declarations were swallowed as text in the prior zone.

## Rationale
Preserves configuration boundaries. Structured listings of project settings must parse values deterministically rather than appending next-block designations as comments to previous tokens.

## Provenance
* **Primary Source:** `knowledge/legacy/intake/workshop/Jarvis Workshop at Home 11052026.zip`
* **Secondary Sources:** `Dhanrick_Jarvis_v4_5_1_24_2D_Mezz_Alias_Guard_Safe_Export_Zone_Parser_Fix.zip/Dhanrick_AI_Workbench/JARVIS_v4_5_1_24_2D_CHANGE_REPORT.md (Fix 3)`
* **Archive:** `Dhanrick_Jarvis_v4_5_1_24_2D_Mezz_Alias_Guard_Safe_Export_Zone_Parser_Fix.zip`
* **Version:** `v4.5.1.24.2D`
* **Confidence:** High
* **Extraction Method:** AI Assisted
