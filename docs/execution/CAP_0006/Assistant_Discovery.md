# Assistant Discovery

## Existing Orchestrators
- `src/jarvis/application/conversation.py` (`ConversationService`): Currently directly chains `RetrievalCoordinator` -> `ReasoningPipeline` -> `GenerationPipeline`. Very hardcoded.
- `src/jarvis/engines/assistant/service.py` (`GroundedAssistantService`): Coordinates question interpretation, understanding retrieval, grounding generation, and mock generation.

## Reuse & Redesign
We need a unified orchestration layer named `WorkspaceAssistant` which will act as the singular entry point.
It will replace `ConversationService` by coordinating the `WorkspaceRuntime` (CAP-0003), `KnowledgeAcquisitionEngine` (CAP-0004), and `AIRuntime` (CAP-0005) rather than directly implementing RAG steps.
