# Execution Pipeline Contract

## Core Invariants
- Sequentially executes list of capability targets mapped inside incoming planner scopes.
- Propagates Stage output forward inside `PipelineContext`.
- Does NOT parse user intents.
- Terminates execution runs cleanly on any critical stage failure.
