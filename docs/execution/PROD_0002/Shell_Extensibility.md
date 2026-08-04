# PROD-0002 — Shell Extensibility Guide

**Date:** 2026-08-04
**Status:** COMPLETE

See Shell_Architecture.md for detailed extensibility patterns.

## Adding Commands

1. Create CommandHandler subclass in commands.py
2. Add to COMMAND_REGISTRY
3. Add tests
4. Update Command_Reference.md

## Key Principles

- Delegate to WorkspaceAssistant public APIs
- Use ShellFormatter for output
- Handle errors gracefully
- Same handlers work in CLI/Desktop/Web/API

## Example

```python
class MyCommand(CommandHandler):
    name = "mycommand"
    description = "Does something"
    
    def execute(self, args, ctx):
        result = ctx.assistant.my_method(args[0])
        return ctx.formatter.success(f"Done: {result}")
```

See existing commands for more examples.
