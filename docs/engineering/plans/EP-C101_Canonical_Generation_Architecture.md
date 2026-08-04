# EP-C101: Canonical Generation Pipeline (Architecture)

**Status:** Active
**Date:** 2026-07-30
**Milestone:** Track C1
**Paired Spec:** ES-C101
**Paired Evidence:** EV-C101
**Owner:** Product Engineering

---

## 1. Objective

Implement the canonical generation pipeline and provider abstraction. Isolate provider/vendor SDKs from the platform reasoning/orchestration layers, strictly emitting vendor-neutral `AssistantResponse` objects via an `ExecutionTrace` facade.

---

## 2. Architecture

```
GenerationPipeline
  └── BaseGenerationProvider (mock, openai, anthropic) -> Normalizes AssistantResponse
       └── BaseProviderClient (wraps actual API calls)
```
Input: `GroundingContext` (+ observation of `RetrievalTrace`, `ReasoningTrace`)
Output: `ExecutionTrace` -> encompasses all traces and normalized responses.

---

## 3. Acceptance Criteria

| AC | Criterion |
|----|-----------|
| AC-1 | Generation Composition Root: `GenerationPipeline` injects `BaseGenerationProvider`. |
| AC-2 | Adapter & Client Decoupling: `BaseGenerationProvider` separates core logic from `BaseProviderClient` networking. |
| AC-3 | Provider-Neutral Normalization: Only `AssistantResponse` leaks out. |
| AC-4 | Provider Capabilities Metadata: `ProviderMetadata` declares semantics clearly. |
| AC-5 | Strict Citation Preservation: `AssistantResponse.citations` maps 1:1 to constraints limits. |
| AC-6 | Immutable GenerationTrace Emission: Records token usage, timing, finish reason. |
| AC-7 | Observer ExecutionTrace Aggregation: Aggregates traces together without mutating children. |
| AC-8 | Presentation Boundary Independence: Zero imports of `jarvis.presentation` / `ui` / `cli`. |
| AC-9 | Deterministic Mock Provider: `MockGenerationProvider` creates reproducible byte-for-byte responses. |
| AC-10 | Zero Production Regression: Passes all 1198+ existing test suites. |