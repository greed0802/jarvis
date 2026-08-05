# -*- coding: utf-8 -*-
import os

def main():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    out_dir = os.path.join(root, "docs", "execution", "PROD_0004")
    os.makedirs(out_dir, exist_ok=True)
    print(f"Generating PROD_0004 docs under: {out_dir}")
    
    write_docs(out_dir)
    print("PROD_0004 docs generation complete.")

def write_docs(out_dir):
    # 1. Document_Discovery.md
    with open(os.path.join(out_dir, "Document_Discovery.md"), "w", encoding="utf-8") as f:
        f.write("""# Document Discovery Report (PROD-0004)

## Discovery of Existing Infrastructure
This discovery report identifies existing endpoints and classes related to file ingestion and indexing in the Jarvis repository.

### 1. Ingestion & Uploads
* **Upload Endpoint:** `WorkspaceAssistant.upload_document(file_path)` inside `src/jarvis/engines/assistant/orchestrator.py`.
* **State Management:** Receives the local path, computes size and SHA-256 hash.

### 2. Artifact Repository
* **Class name:** `ArtifactRepository` inside `src/jarvis/core/artifact/repository.py`.
* **Functions:** `register_artifact(...)` maps virtual file identifiers and creates versions.

### 3. File Parsers
* **CostX BOQ Parser:** `WorkbookParser` inside `src/jarvis/parsers/costx/workbook_parser.py` loads BOQ Excel spreadsheets.
* **BOQ Row Extraction:** `extract_boq(workbook)` inside `src/jarvis/parsers/costx/boq_extraction.py` filters quantities, UOMs, and structures.

### 4. Search & Grounding
* **Orchestrator Loader:** `KnowledgeLoader` inside `src/jarvis/engines/assistant/grounding.py` loads documents into the registry.
* **Attribution:** `ArtifactResolver` inside `src/jarvis/engines/assistant/resolvers/artifact.py` resolves list-artifacts questions.
""")

    # 2. Document_Domain_Contract.md
    with open(os.path.join(out_dir, "Document_Domain_Contract.md"), "w", encoding="utf-8") as f:
        f.write("""# Document Domain Contract

Defines the core logical properties and types constituting the canonical Document Intelligence Layer.

## Domain Schemas

### 1. Document
* `document_id`: Unique identifier (e.g. `doc-art123`).
* `workspace_id`: Active workspace key.
* `name`: Display path filename.
* `classification`: `DocumentClassification` type.
* `lifecycle`: `DocumentLifecycle` status.
* `metadata`: Nested `DocumentMetadata` properties.
* `relationships`: List of connections.
* `recommendations`: Action items.

### 2. DocumentClassification (Enum)
Target classifications: Architectural Drawing, Structural Drawing, Civil Drawing, Services Drawing, Specification, BOQ, Checklist, Schedule, Image, Photo, Spreadsheet, Calculation, Report, Email, Archive, Unknown.

### 3. DocumentLifecycle (Enum)
Transition lifecycle stages: Uploaded -> Registered -> Classified -> Parsed -> Indexed -> Linked -> Validated -> Ready -> Archived.
""")

    # 3. Document_Classification_Contract.md
    with open(os.path.join(out_dir, "Document_Classification_Contract.md"), "w", encoding="utf-8") as f:
        f.write("""# Document Classification Contract

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
""")
    # 4. Document_Relationship_Model.md
    with open(os.path.join(out_dir, "Document_Relationship_Model.md"), "w", encoding="utf-8") as f:
        f.write("""# Document Relationship Model

Defines the structure of the document tracing relationships representation.

## Directional Mappings
* **`supersedes`:** Links document revisions (e.g. `doc-art2` supersedes `doc-art1`). Triggers recommendations for outdated files.
* **`governs`:** A `Specification` governs matching files in the active workspace.
* **`supports`:** A `Drawing` (Architectural/Structural/Civil/Services Layouts) supports a `BOQ` to establish quantity takeoff backing.
* **`validates`:** A QA `Checklist` validates a `BOQ` to verify items calculations.
""")

    # 5. Document_Completeness_Model.md
    with open(os.path.join(out_dir, "Document_Completeness_Model.md"), "w", encoding="utf-8") as f:
        f.write("""# Document Completeness Model

Defines expected document checklists to score readiness.

## Completeness Scores
For a standard takeoff scope, the target checklist expected categories are:
1. **Architectural Drawing**
2. **Structural Drawing**
3. **Specification**
4. **BOQ**
5. **Checklist**

* **Score Calculation:** `Actual Present CategoriesCount / Total Expected CategoriesCount`.
* **Zero Items Warning:** Creates missing recommendations if count of items in any category is 0.
""")

    # 6. Capability_Mapping.md
    with open(os.path.join(out_dir, "Capability_Mapping.md"), "w", encoding="utf-8") as f:
        f.write("""# Capability Mapping

Maps canonical document types to executable system capabilities.

## Execution Requirements Matrix
* **BOQIntelligence:**
  - *Required:* `BOQ` document type.
  - *Optional:* `Checklist`, `Specification`.
* **PDFTakeoff:**
  - *Required:* `Architectural Drawing`.
  - *Optional:* `Specification`.
* **RevisionTracking:**
  - *Required:* `Structural Drawing` and `Architectural Drawing`.
""")

    # 7. Recommendation_Engine.md
    with open(os.path.join(out_dir, "Recommendation_Engine.md"), "w", encoding="utf-8") as f:
        f.write("""# Recommendation Engine Rules

Deterministic registry verification rules mapping gaps to recommendations.

## Active Rules
1. **Gap Rule:** If a classification key is missing from expected, suggest uploading a specific layout (e.g. structural drawing details or spec sheets).
2. **Verification Rule:** If a BOQ exists, recommend running BOQ Intelligence or listing files, and checklist running check validation.
3. **Revision Mismatch Rule:** If a document is superseding another document, display outdated warnings with recommendation to swap them.
""")
    # 8. Workspace_Document_Awareness.md
    with open(os.path.join(out_dir, "Workspace_Document_Awareness.md"), "w", encoding="utf-8") as f:
        f.write("""# Workspace Document Awareness

Mapping assistant queries to deterministic registry facts.

## Assistant Response Patterns
1. **"What documents exist?"** -> Lists registered documents, classifications, and lifecycle states.
2. **"What should I upload next?"** -> Returns missing checklist suggestion cards.
3. **"What can I do with this drawing?"** -> Interrogates capability statuses matching drawings.
4. **"What capabilities are available?"** -> Summarizes executable items and their requirements.
""")

    # 9. Document_Intelligence_Architecture.md
    with open(os.path.join(out_dir, "Document_Intelligence_Architecture.md"), "w", encoding="utf-8") as f:
        f.write("""# Document Intelligence Architecture

High-level architecture showing components organization:

```
                  +--------------------------------+
                  |       WorkspaceAssistant       |
                  +--------------------------------+
                                  │
                                  ▼
                  +--------------------------------+
                  |        DocumentResolver        |
                  +--------------------------------+
                                  │
                                  ▼
             +──────────────────────────────────────────+
             |        DocumentIntelligenceEngine        |
             +──────────────────────────────────────────+
               │        │           │          │       │
               ▼        ▼           ▼          ▼       ▼
           Registry  Classifier  RelEngine  CompEng  RecEngine
```
""")

    # 10. Document_Intelligence_Roadmap.md (Additional Report)
    with open(os.path.join(out_dir, "Document_Intelligence_Roadmap.md"), "w", encoding="utf-8") as f:
        f.write("""# Document Intelligence Roadmap

Core roadmap guiding future document processing evolution.

* **Phase 1: Metadata Awareness (Completed - PROD-0004):** Deterministic classification, relationships structures, and rules suggestions foundation.
* **Phase 2: Parser Intelligence (Future):** Extraction of drawing layers and specification sections from PDF/DWG.
* **Phase 3: Cross-Document Reasoning (Future):** Logical cross-checking of BOQ lines to drawing schedules.
* **Phase 4: Engineering Takeoff Curation (Future):** Deterministic takeoffs calculation.
* **Phase 5: Grounded AI Reasoning (Future):** Final conversational analysis validation.
""")

    # 11. PROD_0004_Final_Report.md
    with open(os.path.join(out_dir, "PROD_0004_Final_Report.md"), "w", encoding="utf-8") as f:
        f.write("""# PROD_0004 Milestone Final Report

Milestone Phase 1 Document Discovery & Intelligence Foundation successfully verified.

## Accomplishments
* Canonical Document Domain entity mapping (`models.py`) built under `domain`.
* Reusable runtime engines checking classifications, links, completeness, and recommendations built under `core`.
* Grounding and assistant queries intercept resolution completed via `DocumentResolver`.
* Zero regressions on MVP commands and self-knowledge suites.
""")


if __name__ == "__main__":
    main()
