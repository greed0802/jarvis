# Execution Pipeline Discovery

## Existing Flow
- `IntentPlanner` generates a single-step mock `Plan` strategies (e.g. `EXECUTE BOQIntelligence`).
- `WorkspaceAssistant` intercepts this strategy and calls `CapabilityRuntime` directly.
- There is no pipeline abstraction matching consecutive execution stages.

## Execution Design
We will introduce `ExecutionPipeline` in its own module `src/jarvis/core/pipeline`. It will receive `Plan` parameters and dynamically resolve them sequentially under structured execution hooks, pushing outputs along stage boundaries.
