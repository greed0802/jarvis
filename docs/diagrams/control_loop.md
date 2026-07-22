# Workflow Execution Control Loop

```text
                     Approved Plan
                           │
                           ▼
                    Workflow Engine
                           │
                           ▼
                          Task
                           │
                           ▼
                      Capability
                           │
                           ▼
                 Capability Registry
                           │
                           ▼
                 Capability Resolver
                           │
                           ▼
                         Skill
                           │
                           ▼
                         Result
                           │
                           ▼
                 Validation Framework
                           │
                           ▼
                    Workflow Engine
                           │
      ┌──────────────┬──────────────┬──────────────┬──────────────┐
      │              │              │              │
      ▼              ▼              ▼              ▼
 Continue         Retry      Refresh Context   Request Replanning
      │              │              │              │
      ▼              │              ▼              ▼
 Next Task           │       Context Engine   Planner Engine
      │              │              │              │
      ▼              ▼              ▼              ▼
 Workflow Engine ◄───┴──────────────┴──────────────┘
```

---
## Control Loop Principles

- The Workflow Engine owns execution.
- Skills perform work.
- Validation evaluates execution results.
- Validation never communicates directly with the Planner Engine.
- Continue advances execution.
- Retry repeats the current Task.
- Context refresh updates understanding before continuing.
- Replanning produces a new approved Plan.