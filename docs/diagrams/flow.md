# Jarvis Execution Flow

```text
User Request
      │
      ▼
Intent
      │
      ▼
Context
      │
      ▼
Planner Engine
      │
      ▼
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
Memory
      │
      ▼
Learning Framework
      │
      │
      ├──────── Not Approved ─────────► Memory Retained
      │
      └──────── Approved ─────────────► Knowledge
```

---

## Flow Summary

The Jarvis Platform progresses through four architectural phases:

1. **Understanding**
   - Intent
   - Context

2. **Planning**
   - Planner Engine
   - Approved Plan

3. **Execution**
   - Workflow Engine
   - Task
   - Capability
   - Capability Registry
   - Capability Resolver
   - Skill

4. **Learning**
   - Validation Framework
   - Memory
   - Learning Framework
   - Knowledge (when promoted)

Not every validated Result becomes Knowledge.

Knowledge promotion follows the governance defined by ADR_0007 and requires validation and, where appropriate, explicit human approval.