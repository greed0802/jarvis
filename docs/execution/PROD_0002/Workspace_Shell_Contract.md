# PROD-0002 — Workspace Shell Contract

**Date:** 2026-08-04
**Status:** ACCEPTED
**Author:** Product Engineering

---

## 1. Responsibilities

The Workspace Shell is a **pure presentation layer**. It SHALL:

- Accept user input from the terminal
- Parse input into commands and arguments
- Delegate every command to a platform service (primarily WorkspaceAssistant)
- Format and display responses as clean readable text
- Handle errors gracefully with user-friendly messages
- Persist command history via WorkspaceMemoryService

The Workspace Shell SHALL NOT:

- Contain business logic
- Communicate directly with AI providers
- Access internal managers or registries
- Create runtime components
- Modify platform state without going through public service APIs

---

## 2. Lifecycle

```
Application.initialize()
    ↓
Application.start()
    ↓
WorkspaceShell.run()     ← Blocks here (interactive loop)
    ↓
Application.shutdown()   ← Triggered by exit command or signal
```

The Shell is created AFTER the platform reaches RUNNING state.
The Shell's `run()` method is the blocking interactive loop.
When `run()` returns (via `exit` command or signal), the platform shuts down.

---

## 3. Public Commands

### Phase 1 — Core

| Command | Description | Delegates To |
|---------|-------------|-------------|
| `help` | Display available commands | Shell internal |
| `status` | Platform status summary | Application + WorkspaceAssistant |
| `version` | Platform version manifest | Shell internal (reads version) |
| `clear` | Clear terminal screen | Shell internal |
| `exit` | Graceful platform shutdown | Shell → Application.shutdown() |

### Phase 2 — Workspace

| Command | Description | Delegates To |
|---------|-------------|-------------|
| `create-workspace <name>` | Create new workspace | WorkspaceAssistant |
| `open-workspace <name>` | Set active workspace | WorkspaceAssistant |
| `list-workspaces` | List all workspaces | WorkspaceAssistant |
| `workspace` | Show active workspace | WorkspaceAssistant |

### Phase 3 — Knowledge & Artifacts

| Command | Description | Delegates To |
|---------|-------------|-------------|
| `upload <path>` | Validate, detect type, register artifact | WorkspaceAssistant |
| `list-documents` | List knowledge items | WorkspaceAssistant |
| `artifacts` | List registered artifacts | WorkspaceAssistant |

### Phase 4 — Conversation & Execution

| Command | Description | Delegates To |
|---------|-------------|-------------|
| `ask "<question>"` | Ask workspace assistant | WorkspaceAssistant |
| `summarize` | Summarize workspace context | WorkspaceAssistant |
| `run <capability>` | Execute registered capability | WorkspaceAssistant |
| `memory` | Show workspace memory entries | WorkspaceAssistant |

### Phase 5 — Developer Mode (--developer)

| Command | Description |
|---------|-------------|
| `debug runtime` | Show runtime internal state |
| `debug planner` | Show planner configuration |
| `debug memory` | Show memory graph details |
| `debug capabilities` | Show capability registry |
| `debug knowledge` | Show knowledge engine state |

---

## 4. Error Handling

- All exceptions caught at the Shell level
- No stack traces shown to users
- Friendly deterministic error messages
- Pattern: `"Error: <description>"`
- Unknown commands: `"Unknown command: <input>. Type 'help' for available commands."`

---

## 5. Prompt Behavior

```
Jarvis>
```

When a workspace is active:

```
Jarvis [workspace-name]>
```

---

## 6. Exit Behavior

The `exit` command:

1. Displays "Shutting down Jarvis Platform..."
2. Sets the shell running flag to False
3. Returns control to bootstrap, which calls Application.shutdown()
4. Platform performs graceful shutdown of all components in reverse order

Ctrl+C also triggers graceful exit.

---

## 7. Session Behavior

- One session per shell invocation
- Session created on shell startup
- Session ID tracked for all command execution context
- Command history persisted via WorkspaceMemoryService

---

## 8. Workspace Awareness

- Shell displays active workspace in prompt
- Workspace-scoped commands require an active workspace
- If no workspace is active, those commands return:
  `"No active workspace. Use 'create-workspace <name>' or 'open-workspace <name>' first."`

---

## 9. Startup Screen

```
==================================================
Jarvis Platform v{version}
Workspace: (none)
Platform Status: RUNNING
Type "help" for available commands.
==================================================
```

---

## 10. Command Handler Pattern

Every command is implemented as a handler class:

```
CommandHandler
    ↓
    execute(args, context) → str
```

This ensures:
- Desktop UI can invoke the same handlers
- Web API can invoke the same handlers
- Tests can invoke handlers directly
- No coupling to terminal I/O in command logic
