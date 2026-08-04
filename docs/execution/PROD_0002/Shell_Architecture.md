# PROD-0002 — Shell Architecture

**Date:** 2026-08-04
**Status:** COMPLETE
**Author:** Product Engineering

---

## 1. Overview

The Interactive Workspace Shell is the first user-facing client of the Jarvis Platform.
It is a **pure presentation layer** that delegates every operation to platform services
through public APIs.

---

## 2. Architecture Principles

1. **Zero Business Logic** — The Shell contains no business logic. Every command delegates
   to WorkspaceAssistant or other platform services.

2. **Command Handler Pattern** — Each command is a handler class implementing `CommandHandler`.
   Desktop/Web/API clients will invoke the same handlers.

3. **Minimal main.py** — `main.py` remains a thin delegator. The Shell is launched via
   `application/bootstrap.py`, allowing future hosts (Desktop, Web, API) to have their
   own bootstrap modules.

4. **Public API Only** — The Shell never accesses internal managers or registries. All
   operations route through `WorkspaceAssistant` public methods.

5. **Async-Aware** — Command handlers detect whether they're in an async context (tests)
   or sync context (interactive shell) and handle both correctly.

---

## 3. Component Structure

```
src/jarvis/
  application/
    bootstrap.py          — Host entry point for interactive shell
  ui/
    shell/
      __init__.py
      shell.py            — WorkspaceShell (REPL loop, banner, prompt)
      commands.py         — Command handler classes + COMMAND_REGISTRY
      formatter.py        — ShellFormatter (clean text rendering)
      history.py          — ShellHistory (persistent via WorkspaceMemoryService)
```

---

## 4. Bootstrap Flow

```
main.py
  → checks args
  → if no args or --developer:
      bootstrap(developer_mode)
        → Application.initialize()
        → Application.start()
        → WorkspaceShell.run()    ← blocks here (interactive loop)
        → Application.shutdown()
```

---

## 5. Command Dispatch Flow

```
User Input
  ↓
Shell._dispatch()
  ↓
CommandHandler.execute()
  ↓
WorkspaceAssistant.<method>()
  ↓
Platform Services (WorkspaceRuntime, KnowledgeEngine, etc.)
```

---

## 6. Command Handler Contract

Every command handler:
- Extends `CommandHandler` (ABC)
- Defines `name`, `description`, `usage`, `developer_only`
- Implements `execute(args: list[str], ctx: ShellContext) -> str`
- Returns displayable text (never modifies UI directly)
- Handles errors gracefully (no stack traces to user)

---

## 7. ShellContext

Immutable context bag passed to every handler:

```python
@dataclass
class ShellContext:
    application: Application
    assistant: WorkspaceAssistant
    session_id: str
    developer_mode: bool
    formatter: ShellFormatter
```

Handlers use `ctx.assistant` for all operations.

---

## 8. Persistent History

Shell history is recorded via `WorkspaceMemoryService`:
- Category: `shell_history`
- Each command invocation stored as a memory entry
- Survives shell restarts
- Queryable via `memory` command

---

## 9. Developer Mode

Launch with `python main.py --developer` to enable:
- `debug runtime` — Kernel state, components, services
- `debug planner` — IntentPlanner configuration
- `debug memory` — Memory graph statistics
- `debug capabilities` — Capability registry contents
- `debug knowledge` — Knowledge engine internals

Developer commands are hidden from normal `help` output.

---

## 10. Error Handling

- All exceptions caught at handler level
- No stack traces shown to users
- Friendly error messages: `[Error] <description>`
- Unknown commands: `Unknown command: <input>. Type "help" for available commands.`

---

## 11. Platform Service Integration

| Shell Command | Delegates To |
|---------------|-------------|
| create-workspace | `WorkspaceAssistant.create_workspace()` |
| open-workspace | `WorkspaceAssistant.open_workspace()` |
| list-workspaces | `WorkspaceAssistant.list_workspaces()` |
| workspace | `WorkspaceAssistant.get_active_workspace()` |
| upload | `WorkspaceAssistant.upload_document()` |
| list-documents | `WorkspaceAssistant.list_documents()` |
| artifacts | `WorkspaceAssistant.get_artifacts_summary()` |
| ask | `WorkspaceAssistant.chat()` (async) |
| summarize | `WorkspaceAssistant.chat()` (async) |
| run | `WorkspaceAssistant.run_capability()` |
| memory | `WorkspaceAssistant.get_memory_summary()` |
| status | `WorkspaceAssistant.get_platform_status()` + Application.state |

---

## 12. Future Extensibility

The same `CommandHandler` classes will be invoked by:
- Desktop UI (Textual, Qt, Electron)
- Web API (FastAPI endpoint → handler)
- Mobile client (REST → handler)
- Test suite (direct handler invocation)

This ensures command logic remains consistent across all clients.

---

## 13. Testing Strategy

**Unit Tests** (`tests/ui/test_shell.py`)
- Formatter rendering
- History persistence
- Command parsing

**Acceptance Tests** (`tests/acceptance/test_product_mvp.py`)
- End-to-end platform boot
- Every command handler exercised
- Real Application + WorkspaceAssistant
- 34 tests covering all phases

---

## 14. Compliance

✅ No internal managers accessed  
✅ All delegation through WorkspaceAssistant  
✅ No business logic in UI layer  
✅ Command handler pattern implemented  
✅ Bootstrap module separates hosting concern  
✅ main.py remains minimal  
✅ Developer mode implemented  
✅ History persisted via WorkspaceMemoryService  
✅ Rich status command  
✅ Async-aware command execution  
✅ Upload performs real artifact registration  
✅ Acceptance tests from entry point  
