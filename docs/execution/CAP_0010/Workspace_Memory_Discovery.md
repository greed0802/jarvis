# Workspace Memory Discovery

## Memory Architecture
- **State models:** `jarvis.domain.memory` holds simple stubs.
- **Persistence:** Local journals (ADR-0029 stubs) in `Workspace` directory but no programmatic memory engine linking execution outcomes dynamically back to context.

## Action Plan
1. Detail `WorkspaceMemory` and `KnowledgeGraph` models.
2. Implement `WorkspaceMemoryService` to index execution artifacts.
3. Automatically trigger storage during `ExecutionPipeline.execute_plan()`.
