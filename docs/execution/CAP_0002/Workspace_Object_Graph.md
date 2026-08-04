# Workspace Object Graph

```mermaid
graph TD
    Workspace --> Project
    Workspace --> Session
    Project --> Knowledge
    Knowledge --> Context
    Context --> Memory
    Context --> Intent
    Intent --> Workflow
    Workflow --> Task
    Task --> Capability
    Planner --> Workflow
```
