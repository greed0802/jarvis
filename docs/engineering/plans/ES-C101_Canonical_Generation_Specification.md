# ES-C101: Canonical Generation Specification

**Status:** Active
**Date:** 2026-07-30
**Paired Plan:** EP-C101
**Evidence:** EV-C101
**Owner:** Product Engineering

---

## 1. Provider Capabilities Semantics

| Flag | Guarantee |
| :--- | :--- |
| **`supports_streaming`** | Provider can yield incremental chunks asynchronously without buffering. |
| **`supports_tools`** | Provider supports structured function invocations matching JSON schemas. |
| **`supports_images`** | Provider accepts multimodal visual/image inputs in context payloads. |
| **`supports_json`** | Provider supports native structured JSON output constraints. |
| **`supports_system_prompt`** | Provider exposes an independent channel specifically for system instruction tokens. |

## 2. Observer Trace Aggregation (ExecutionTrace)

`ExecutionTrace` sits atop `GenerationTrace`, `ReasoningTrace`, and `RetrievalTrace`.
It is purely an *observer* structure. Under no circumstances may `GenerationPipeline` manually overwrite fields inside inner traces. Traces MUST be `frozen=True`.

## 3. Provider-Neutral Normalization

No object referencing `OpenAI`, `ChatCompletion`, `AnthropicMessage` shall be returned by any class satisfying `BaseGenerationProvider`. The pipeline handles exclusively domain contracts (`AssistantResponse`).