# Document Discovery Report (PROD-0004)

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
