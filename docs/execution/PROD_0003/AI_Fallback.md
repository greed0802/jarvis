# AI Fallback — PROD-0003

## Architecture

AI is the LAST resolver in the chain.

```
ResolverChain
  ↓
WorkspaceResolver  ❌ can't resolve
ArtifactResolver   ❌ can't resolve
KnowledgeResolver  ❌ can't resolve
MemoryResolver     ❌ can't resolve
CapabilityResolver ❌ can't resolve
  ↓
AIResolver ✅ always resolves
```

## When AI is invoked

1. The `GroundingEngine` collects all available platform context
2. A complete `AIRequest` is prepared with the grounded context
3. The `AIRuntime.execute_request()` is called
4. The response is returned with `source: "AI"`, `grounded: True`, `confidence: "Medium"`

## Grounding Context

The `GroundingEngine` assembles:

- **Workspace Context**: Active workspace, project, session
- **Artifact Catalog**: Registered artifacts
- **Knowledge Registry**: Knowledge items
- **Memory Traces**: Recent execution history
- **User Intent**: Original question

## Current Limitation

The `AIRuntime` currently returns mocked responses.
When a real AI provider is integrated (e.g., OpenAI, Anthropic, or local models),
the GroundingEngine context will be sent as system context with the user's question.