# Intent Planner Discovery

## Existing Architecture Review
- **Assistant Orchestration:** `WorkspaceAssistant` currently bridges AI logic natively within `chat` methods but has no true logical parsing step defining exactly *how* a request translates to an actionable pipeline via Capabilities.
- **Capability Runtime:** Successfully wrapped components (`BOQIntelligenceCapability`), but no orchestration agent currently acts upon `CapabilityRegistry.list_all()`.
- **Domain State:** Built the `Intent` and `Plan` models via CAP-0002.

## Required Implementation
Build `IntentPlanner` which operates statically. It receives intents and returns `ExecutionPlan` constructs mapped from the generic registry metadata injected during boot.
