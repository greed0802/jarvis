# Recommendation Engine Rules

Deterministic registry verification rules mapping gaps to recommendations.

## Active Rules
1. **Gap Rule:** If a classification key is missing from expected, suggest uploading a specific layout (e.g. structural drawing details or spec sheets).
2. **Verification Rule:** If a BOQ exists, recommend running BOQ Intelligence or listing files, and checklist running check validation.
3. **Revision Mismatch Rule:** If a document is superseding another document, display outdated warnings with recommendation to swap them.
