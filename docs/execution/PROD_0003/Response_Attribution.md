# Response Attribution — PROD-0003

Every response from the Knowledge-Driven Assistant declares its origin.

## ResolutionResult

```python
ResolutionResult(
    resolved=True,
    source="Workspace",
    confidence="High",
    payload="Active workspace: Bridge Construction",
    evidence=["Workspace: Bridge Construction", "Created: 2026-07-14"],
    grounded=True,
    execution_time_ms=4.2,
    reason="Active workspace retrieved from WorkspaceRuntime",
    resolution_chain=["WorkspaceResolver"],
)
```

## Source Values

| Source | Description |
|--------|-------------|
| Workspace | Answered by WorkspaceRuntime |
| Artifact | Answered by ArtifactRepository |
| Knowledge | Answered by KnowledgeRegistry |
| Memory | Answered by WorkspaceMemoryService |
| Capability | Capability execution result |
| AI | Unified AI Runtime with grounding |

## Confidence Levels

- **High** — Deterministic platform answer, no AI involved
- **Medium** — AI answer grounded in platform context
- **Low** — Ambiguous or partially resolved

## Developer Mode

When `ShellContext.developer_mode == True`, the resolution chain is displayed:

```
  Source      Workspace
  Confidence  High
  Grounded    Yes
  Chain       WorkspaceResolver
  Time        4.2 ms
```