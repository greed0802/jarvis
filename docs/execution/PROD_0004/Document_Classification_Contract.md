# Document Classification Contract

Defines the deterministic precedence for classifying uploaded assets to avoid speculative or AI-first heuristics.

## Precedence Rules
1. **Extension:** Files ending like `.zip`/`.7z` are flagged as `Archive`. `.eml` as `Email`.
2. **Parser Signature / Workbook Structure:** Loaded Excel spreadsheet sheets are scanned using `openpyxl`:
   * If sheets match the Source of Truth schema -> `BOQ` / `Registry`.
   * If sheets have CostX takeoff values or row items -> `BOQ`.
   * If sheets contain checklist names -> `Checklist`.
3. **Metadata Properties:** Checks content descriptors and file size limits.
4. **Filename Keywords:**
   * Starts with `A-`/`AR-`, or keyword matches `architectural`/`arch` -> `Architectural Drawing`.
   * Starts with `S-`/`ST-`, or keyword matches `structural`/`struct` -> `Structural Drawing`.
   * Starts with `C-`/`CI-`, or keyword matches `civil`/`civ` -> `Civil Drawing`.
   * Starts with `M-`/`E-`/`H-`/`F-`/`services` -> `Services Drawing`.
   * Keyword `spec`/`specification` -> `Specification`.
   * Keyword `checklist`/`checks` -> `Checklist`.
   * Keyword `schedule`/`program` -> `Schedule`.
   * Keyword `calc`/`calculation` -> `Calculation`.
   * Keyword `report`/`summary` -> `Report`.
   * Keyword `photo`/`site` -> `Photo`.
   * Keyword `image`/`png`/`jpg` (without site indicator) -> `Image`.
5. **Folder Context:** Mapped parent paths (e.g. `/drawings/` as layout indicators).
6. **Workspace Context:** Checks project specifications templates.
