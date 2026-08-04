# Assistant Orchestration — PROD-0003

## Architecture

```
User → Shell → WorkspaceAssistant.resolve()
                     │
              ResolverChain
                     │
    ┌────────────────┼────────────────┬────────────────────┐
    │                │                │                    │
WorkspaceResolver  ArtifactResolver  ...            AIResolver
    │                │                │                    │
WorkspaceRuntime  ArtifactRepo        │              GroundingEngine
                                       │                    │
                                  CapabilityRuntime    AIRuntime
```

## Core Design

**WorkspaceAssistant** is a thin facade that lazily builds a `ResolverChain` and forwards every user request through it.

**IntentPlanner** is a future collaborator that will classify the user's question into `Intent + Target + Action` semantics. Today the resolvers use keyword fallback.

**ExecutionPipeline** owns execution — but for simple queries the pipeline is bypassed in favor of the lightweight `ResolverChain`. When a capability must be executed, the `CapabilityResolver` delegates to the `CapabilityRuntime`.

## Resolver Chain Priority

1. **WorkspaceResolver** — workspace, project, session
2. **ArtifactResolver** — files, drawings, BOQs, specs
3. **KnowledgeResolver** — registered knowledge items
4. **MemoryResolver** — execution traces and graph
5. **CapabilityResolver** — list/execute capabilities
6. **AIResolver** — always resolves (gleser with GroundingEngine)

## Contracts

Every resolver:
- Implements `can_resolve(intent) → bool`
- Implements `resolve(intent, context) → ResolutionResult`
- Is **read-only** unless the intent is explicitly EXECUTE or CREATE
- **Never** calls another resolver

## Response Attribution

Every `ResolutionResult` carries:
- `source` — which resolver answered
- `confidence` — "High", "Medium", or "Low"
- `grounded` — `True` when anchored in platform knowledge
- `evidence` — list of evidentiary strings (capability outputs etc.)
- `resolution_chain` — ordered list of resolvers consulted (developer mode)
- `execution_time_ms` — resolution duration