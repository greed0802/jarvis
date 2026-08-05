# Jarvis Platform Architecture

## Core Components

The platform architecture is divided into the **Control Plane (Kernel)** and **Composition Root (Application)**.

```
                    +------------------------------------+
                    |        Workspace Shell             |
                    +------------------------------------+
                                      |
                                      v
                    +------------------------------------+
                    |        Workspace Assistant         |
                    +------------------------------------+
                                      |
                                      v
                    +------------------------------------+
                    |           IntentPlanner            |
                    +------------------------------------+
                                      |
                                      v
                    +------------------------------------+
                    |         ExecutionPipeline          |
                    +------------------------------------+
                                      |
                                      v
                    +------------------------------------+
                    |           ResolverChain            |
                    +------------------------------------+
  +-------------------+-------------------+-------------------+--------------------+
  |                   |                   |                   |                    |
  v                   v                   v                   v                    v
WorkspaceResolver  ArtifactResolver  KnowledgeResolver  MemoryResolver  CapabilityResolver
  |                   |                   |                   |                    |
  v                   v                   v                   v                    v
WorkspaceRuntime   ArtifactRepository  KnowledgeRegistry WorkspaceMemory   CapabilityRuntime
                                                                                   |
                                                                                   v
                                                                            AIResolver (grounded)
```

## Boundary Rules

- **Platform Kernel**: Control Plane owning configuration, registration, lifecycle, and service management. Does not contain workflows, plans, or business logic.
- **Application**: The Composition Root which instantiates and wires all platform services together.
- **Runtime Ownership**: Context Engine owns Context, Planner Engine owns Plans, Workflow Engine owns Workflows and Tasks.
- **Resolvers**: Independent platform connectors. Resolvers SHALL be read-only unless the intent specifically requests mutation (CREATE, UPDATE, DELETE). Resolvers SHALL never call each other directly.
- **Snapshot-Driven calculation**: Execution tasks (preview, run, export, and jobs) run against a locked `builder_run_snapshot` representing the active plan details at initialization, shielding computations from live workspace state drift. Dynamic hierarchies force a `rebuild` mode to retain integrity. *Source Code Alignment: LK_S0003*
- **Cached Preview Invalidation**: Client-side preview data is tagged with a plan fingerprint signature of active options (workbook, trade, custom unit, levels, and zones). If active values deviate from this fingerprint, the cache is invalidated, blocking out-of-date presentations. *Source Code Alignment: LK_S0004*
- **Evidence static evaluation boundaries**: Router rules and policy boundaries can be verified statically with mock evaluator loops (evaluator_executable=false). This generates verifiable policy validation evidence without invoking active code modification or attach gates. *Source Code Alignment: LK_S0008*

*Lightweight Source References: LK_S0003, LK_S0004, LK_S0008*
