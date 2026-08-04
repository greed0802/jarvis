# AI Runtime & Provider Orchestration Discovery

## Generation Engine
The repository currently has a Generation Engine at `src/jarvis/engines/generation`. It defines:
- A `GenerationPipeline` (Orchestrates passing logic to providers)
- `BaseProviderClient` and `BaseGenerationProvider` in `protocols.py`
- Clients for OpenAI, Anthropic, Ollama, and a Mock.

## Assistant Engine
Located at `src/jarvis/engines/assistant`. Orchestrates conversation loops and retrieval pipelines.

## Reuse Strategy
We do not need to build a new Runtime Engine from absolute zero; we will **reuse and extend** the `GenerationEngine` and label the overarching umbrella the `AIRuntime`. We need to define standard Request objects independently, implement registries, and wire it correctly behind `AIRuntime`.

The Providers (Google, Groq, Azure, OpenRouter) and strict registry mapping capabilities need to be architected properly via abstract requests (`AIRequest`, `AITool`, `AIResponse`).
