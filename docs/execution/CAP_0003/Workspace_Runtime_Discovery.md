# Workspace Runtime Discovery

## Executive Analysis
The repository separates the `Application` (Process Orchestrator), the `Kernel` (Runtime Coordinator), and heavily encapsulates `jarvis.platform.workspace` (File-based initialization per ADR-0032). There is NO current runtime memory manager orchestrating the new pure-domain models (Workspace, Project, KnowledgeItem, etc.) implemented in CAP-0002.

## Existing Runtime Reused
- `jarvis.contracts.lifecycle.LifecycleAware`
- `jarvis.core.jarvis.kernel.Kernel`
- `jarvis.application.application.Application`

## Conclusion
We need to create a new module `jarvis.core.workspace.RuntimeManager` that implements `LifecycleAware`, gets bootstrapped by the `Application`, registered in the `Kernel`, and acts as the pure gateway to querying or instantiating the immutable Domain Objects (Workspace, Session, etc.).
