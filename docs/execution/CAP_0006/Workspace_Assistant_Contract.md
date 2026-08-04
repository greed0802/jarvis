# Workspace Assistant Contract

## Responsibilities
- Coordinates the flow of user intents through the appropriate platform runtimes.
- Orchestrates context assembly from Workspace Domain objects.
- Does NOT execute business logic, retrieval, or reasoning directly.

## Public API
- `invoke(intent: str, workspace_id: str, session_id: str)`
- `upload(file_path: str, workspace_id: str, project_id: str)`

## Tool Invocation
- Maintains knowledge of deterministic tools. Emits structural commands to AIRuntime for LLM usage, and vectors outputs back to user.
