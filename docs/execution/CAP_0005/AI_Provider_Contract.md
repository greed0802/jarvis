# AI Provider Contract

## Core Mandate
Providers simply execute serialized payloads (chat, embeddings, vision, tools). They hold absolutely zero logic pertaining to Workspaces, Sessions, or Application Business Rules.

## Unified AI Schema
To prevent vendor lock-in, the parameters for every model interaction must be funneled through:
- `AIRequest`: The unified request (System Prompts, Messages, Attached Tools, Streaming flags).
- `AIResponse`: Unified yield type.
- `AITool`: JSON Schema definitions of tools independent of OpenAI vs Anthropic formats.
