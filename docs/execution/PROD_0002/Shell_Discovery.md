# PROD-0002 — Shell Discovery Report

**Date:** 2026-08-04
**Status:** COMPLETE
**Author:** Product Engineering
**Operation:** Read-Only

---

## 1. Objective

Discover all existing platform components, CLI infrastructure, and UI patterns
that the Interactive Workspace Shell must reuse. No new components shall be
created where existing ones serve the same purpose.

---

## 2. Discovered Platform Components

| Component | Location | Status |
|-----------|----------|--------|
| Application | `src/jarvis/application/application.py` | Frozen — Composition Root |
| Kernel | `src/jarvis/core/jarvis/kernel.py` | Frozen — Control Plane |
| WorkspaceRuntime | `src/jarvis/core/workspace/runtime.py` | Frozen — Workspace/Session/Project/Knowledge managers |
| KnowledgeAcquisitionEngine | `src/jarvis/engines/knowledge/engine.py` | Frozen — Source/Parser registries |
| AIRuntime | `src/jarvis/engines/airuntime/engine.py` | Frozen — Provider/Model registries |
| WorkspaceAssistant | `src/jarvis/engines/assistant/orchestrator.py` | Frozen — Unified interface for AI + Knowledge + Workspace |
| CapabilityRuntime | `src/jarvis/core/capability/runtime.py` | Frozen — Registry, execute() |
| IntentPlanner | `src/jarvis/engines/planner/engine.py` | Frozen — generate_plan() |
| ExecutionPipeline | `src/jarvis/core/pipeline/engine.py` | Frozen — execute_plan() |
| WorkspaceMemoryService | `src/jarvis/core/memory/engine.py` | Frozen — store_entry(), query() |
| ArtifactRepository | `src/jarvis/core/artifact/repository.py` | Frozen — register_artifact(), get() |

---

## 3. Discovered CLI Infrastructure

| Component | Location | Notes |
|-----------|----------|-------|
| Headless CLI | `src/jarvis/cli/main.py` | Dispatches eval, workbench, datasets, report, doctor |
| CommandDispatcher | `src/jarvis/cli/dispatcher.py` | Routes headless subcommands |
| InteractiveCLIWorkbench | `src/jarvis/cli/workbench.py` | REPL loop for conversation (uses ConversationService) |
| SlashCommands | `src/jarvis/cli/slash_commands.py` | /help, /status, /trace, /clear, /exit |
| CLIFormatter | `src/jarvis/cli/formatter.py` | Renders AssistantResponse, ExecutionTrace |
| ExitCode | `src/jarvis/cli/exitcodes.py` | Deterministic exit codes |

---

## 4. Discovered UI Infrastructure

| Component | Location | Notes |
|-----------|----------|-------|
| UI package | `src/jarvis/ui/__init__.py` | Package established |
| Textual TUI | `src/jarvis/ui/textual/` | Desktop TUI workbench (separate from Shell) |

---

## 5. Current Bootstrap Flow

```
main.py
  → if args: delegate to headless CLI (jarvis.cli.main)
  → else: asyncio.run(run_server())
      → Application(config)
      → app.run()
        → initialize → start → wait for shutdown signal → shutdown
```

The `run_server()` currently waits for Ctrl+C with no interactive prompt.

---

## 6. Domain Models

| Model | Location | Notes |
|-------|----------|-------|
| Workspace | `src/jarvis/domain/workspace.py` | Frozen dataclass: workspace_id, name, created_at, metadata |
| Session | `src/jarvis/domain/session.py` | Frozen dataclass: session_id, workspace_id, created_at |
| KnowledgeItem | `src/jarvis/domain/knowledge.py` | Frozen dataclass: knowledge_id, project_id, resource_uri, content_hash |
| Artifact | `src/jarvis/core/artifact/models.py` | Frozen dataclass with ArtifactType enum |
| MemoryEntry | `src/jarvis/core/memory/models.py` | Frozen dataclass: entry_id, workspace_id, category, content |

---

## 7. Key Findings

1. **`src/jarvis/ui/shell/`** — Approved location under existing `ui/` package.
2. **WorkspaceAssistant** — The canonical entry point for all user-facing operations.
   The Shell shall delegate through WorkspaceAssistant's public API, never touching
   internal managers directly.
3. **Application properties** — `artifact_repository`, `memory_service` properties exist
   but `_artifact_repository` and `_memory_service` are not constructed in `__init__`.
   These need to be wired up.
4. **Version** — `0.0.1-alpha.17` in `src/jarvis/version.py`.
5. **asyncio.to_thread(input, ...)** — Proven pattern from `workbench.py` for
   non-blocking terminal input.

---

## 8. Reuse Decision

| Need | Reuse |
|------|-------|
| Interactive prompt loop | Pattern from `InteractiveCLIWorkbench` |
| Error handling | Catch-and-display pattern from `workbench.py` |
| Existing UI package | `src/jarvis/ui/` |
| Command delegation | Route through WorkspaceAssistant public API |
| Platform lifecycle | Application.initialize() → start() → shell loop → shutdown() |
| History persistence | WorkspaceMemoryService.store_entry() |
