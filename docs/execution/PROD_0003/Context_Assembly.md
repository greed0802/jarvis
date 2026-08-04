# Context Assembly — PROD-0003

## GroundingEngine

Formerly known as `ContextAssembler`, the `GroundingEngine` is responsible for assembling comprehensive platform context to ground AI responses.

## Responsibilities

- Collect active workspace, project, and session info
- Collect artifact catalog
- Collect knowledge registry
- Collect memory traces
- Collect user intent

## Design

```python
context = grounding_engine.assemble_context(intent, execution_context)
# Returns a formatted string suitable for AI system prompts
```

## Usage

The `GroundingEngine` is used ONLY by `AIResolver`.
Deterministic resolvers query platform components directly.

## Extensibility

Future context collectors (e.g., ConversationHistory, CapabilityResults)
can be added as additional `_collect_*` methods without changing the AIResolver.