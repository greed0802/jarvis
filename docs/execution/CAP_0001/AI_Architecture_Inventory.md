# AI Architecture Discovery & Inventory (CAP-0001)

## Phase 1 — Inventory

### 1. Existing Classes & Services
- **Generation (`src/jarvis/engines/generation/`)**: 
  - `GenerationPipeline`
  - `BaseProviderClient`, `BaseGenerationProvider`
  - `OpenAIClient`, `AnthropicClient`, `OllamaClient`, `MockClient`
- **Reasoning (`src/jarvis/engines/reasoning/`)**:
  - `TokenWindowCompressor`, `DeduplicatingCompressor`
  - `GraphSynthesizer` (builds `EvidenceGraph`)
- **Retrieval (`src/jarvis/engines/retrieval/`)**:
  - `RetrievalCoordinator` (handles hybrid search)
  - `InMemoryVectorIndex` (CPU-based cosine similarity)
  - `BM25LexicalRetriever`, `DenseVectorRetriever`
- **Understanding (`src/jarvis/engines/understanding/`)**:
  - `ProjectUnderstandingImporter`, `ProjectUnderstandingService`, `ProjectUnderstandingStore` (highly coupled to CheckMate findings)
- **Assistant (`src/jarvis/engines/assistant/`)**: 
  - `AssistantService`
- **Application (`src/jarvis/application/`)**:
  - `ConversationService` (Orchestrates Retrieval → Reasoning → Generation)

### 2. Existing Interfaces & Contracts
- **Contracts (`src/jarvis/contracts/`)**: 
  - `assistant.py`: `AssistantResponse`
  - `capabilities.py`: `FindingReport`
  - `understanding.py`: `ProjectUnderstanding`, `UnderstandingFinding`
  - `GenerationTrace`, `ExecutionTrace`, `ProviderCapabilities`, `ProviderMetadata`, `TokenUsage`
- **Abstractions**:
  - `EmbeddingProvider` (abstract network SDK interface for embeddings)
  - `BaseProviderClient` (low-level LLM API wrapper)

### 3. Existing Runtimes & Registries
- **Runtime**: `src/jarvis/application/runtime.py`, `src/jarvis/core/jarvis/kernel.py`
- **Capability Engine**: `src/jarvis/applications/checkmate/` (CostX rule enforcement)
- **Registries**: `jarvis.engines.checkmate.registry` (only rules, no global AI Tool/Capability register implementation)

### 4. Existing Parsing Engines
- **CostX Boilerplate (`src/jarvis/parsers/costx/`)**:
  - `workbook_parser.py`, `boq_extraction.py`, `loader.py`
  - Specifically designed for deterministic Excel rule-checking. Excludes subjective parsing.
- **Other Parsers**: None present.

### 5. Domains & Models
- `src/jarvis/domain/` contains multiple initialized but empty files (0 bytes): `memory.py`, `context.py`, `workspace.py`, `planner.py`, `project.py`, `knowledge.py`, `intent.py`, `capability.py`, `workflow.py`.

### 6. Workflow Engines
- Directories exist (`workflows/builtin`, `user`, etc.) but contain no runtime logic inside the Python source tree natively executing them.

---

## Phase 2 — Gap Analysis

| Component | Status | Evidence |
| :--- | :--- | :--- |
| **Provider Manager** | PARTIALLY IMPLEMENTED | `engines/generation/clients` has Anthropic, OpenAI, Ollama. Missing: Google, OpenRouter, Groq, Azure. Requires dynamic registry vs hardcoded imports. |
| **Document Engine** | MISSING (Except BOQ) | `parsers/costx/` exists for rigid Excel schemas. No generic PDF, DOCX, CSV parsing. No OCR, semantic chunking pipeline or multi-format ingestion module. |
| **Context Engine** | PARTIALLY IMPLEMENTED | `engines/reasoning/compressor.py` and `GraphSynthesizer` provide context compression and graph tracking. However, `domain/context.py` is 0 bytes. True multi-turn conversation memory mapping is weak. |
| **Memory Engine** | PARTIALLY IMPLEMENTED | `domain/memory.py` is empty. `engines/retrieval/index/memory.py` is just a basic CPU-based vector index. No long-term persistent declarative memory system. |
| **Workspace Engine** | MISSING | `domain/workspace.py` and `project.py` are empty. `core/project/` and `core/session/` lack code. |
| **Planner Engine** | MISSING | `domain/planner.py` is empty. Core lacks planner agents. |
| **Conversation Engine** | PARTIALLY IMPLEMENTED | `application/conversation.py` provides linear orchestration. Lacks router-level dynamic delegation. |
| **Prompt Engine** | MISSING | No dedicated robust template or prompt management engine (folders exist but no programmatic template renderer). |
| **Tool / Capability Integration** | PARTIALLY IMPLEMENTED | Checkmate exists, but `domain/capability.py` is empty. No dynamic function calling (Tool integration) injected into Generation LLM clients. |
| **Workflow Engine** | MISSING | `domain/workflow.py` empty. `workflows/` directories exist but lack python engine (`core/task/` empty). |

---

## Phase 3 — Reuse Plan

### 1. Components to Reuse
- `engines/generation/` concepts: Keep `BaseProviderClient` protocol, but extend it.
- `engines/reasoning/` and `engines/retrieval/`: Retain `RetrievalCoordinator`, compression utilities, and `GraphSynthesizer`.
- `application/conversation.py`: Reuse this as the composition root pattern.

### 2. Components to Extend
- **Provider Framework**: Extend `base.py` to support OpenRouter, Groq, Google, and Azure OpenAI providers. Enable dynamic capability injection (Tools).
- **Retrieval Engine**: Extend abstract `EmbeddingProvider` from in-memory dictionary searches to a rigorous localized vector/DB handler, and add semantic chunker utilities to ingestion.

### 3. Components to Archive
- Pure stub files (0 byte `domain/*.py`) will be reused by giving them actual content rather than archiving.

### 4. Components to Create
- **Document Engine**: Needs PDF/DOCX multi-modal processing and an OCR gateway.
- **Workflow & Planner Engine**: Need concrete domain classes and state execution loops to satisfy multi-agent or agentic tasks.
- **Memory/Workspace Engine**: Implement persistent schema definitions to replace current stubs.