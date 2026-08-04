# Intent Planner Contract

## Constraints
- Evaluates Intents purely heuristically, returning an `ExecutionPlan`.
- Must explicitly rely entirely off `CapabilityRegistry` metadata schemas (`supported_intents`).
- NEVER executes tool logic themselves.

## Contracts
- `IntentMatch`: Weighted score aligning an Intent with a registered specific Capability.
- `ExecutionPlan`: Deterministic chain of execution targets based purely off match resolution.
