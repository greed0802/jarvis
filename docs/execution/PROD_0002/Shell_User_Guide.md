# PROD-0002 — Shell User Guide

**Date:** 2026-08-04
**Status:** COMPLETE

## Quick Start

```bash
python main.py
```

## First Steps

1. `create-workspace MyProject`
2. `upload document.pdf`
3. `list-documents`
4. `ask "question"`
5. `status`
6. `exit`

## Developer Mode

```bash
python main.py --developer
```

Enables debug commands: `debug runtime`, `debug memory`, etc.

## Common Commands

- `help` - Show all commands
- `status` - Platform status
- `workspace` - Show active workspace
- `list-workspaces` - List all workspaces
- `upload <path>` - Upload document
- `artifacts` - List artifacts
- `run <capability>` - Execute capability
- `clear` - Clear screen
- `exit` - Shutdown

See Command_Reference.md for complete documentation.
