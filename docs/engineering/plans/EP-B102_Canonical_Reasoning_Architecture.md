# EP-B102: Canonical Reasoning Architecture

**Status:** Active
**Date:** 2026-07-30
**Milestone:** Track B2
**Paired Spec:** ES-B102
**Paired Evidence:** EV-B102
**Owner:** Product Engineering

---

## 1. Objective

Build the canonical reasoning pipeline that takes immutable `RetrievalTrace` outputs, performs model-neutral Re-Ranking, lossless provenance Context Compression, and Multi-Document Synthesis, culminating in an optimal `GroundingContext` for LLM assimilation.

---

## 2. Architecture

```
ReasoningPipeline
  ├── BaseReRanker (Heuristic / Model) -> ReRankedCandidate
  ├── ContextCompressor (Window / Deduplicating) -> CompressionSpanMap -> CompressedContext
  ├── MultiDocumentSynthesizer (GraphSynthesizer) -> EvidenceGraph
  └── Output: GroundingContext (from jarvis.contracts.assistant)
  └── Observation: ReasoningTrace (immutable)
```

---

## 3. Acceptance Criteria

| AC | Criterion |
|----|-----------|
| AC-1 | Reasoning Composition Root: `ReasoningPipeline` receives dependencies via constructor injection. No LLM calls. |
| AC-2 | Model-Neutral Re-Ranker: Heuristic and Model re-ranking adhere to `BaseReRanker`. |
| AC-3 | Span Provenance Tracking: Compressors emit `CompressionSpanMap` tracking original_span -> tgt -> doc_id. |
| AC-4 | Immutable Graph-Based Synthesis: Synthesizer constructs `frozen=True` `EvidenceGraph` across docs/revisions. |
| AC-5 | Grounding Context Import: `GroundingContext` consumed from `jarvis.contracts.assistant`. |
| AC-6 | Immutable ReasoningTrace Emission: Process emits complete trace artifact. |
| AC-7 | Strict Linear Boundary: Zero imports of presentation, CLI, or UI layers. |
| AC-8 | Expanded EVA-2 Benchmarking: Track Context Reduction, Citation Retention, etc. |
| AC-9 | Intermediate Byte-for-Byte Reproducibility: Identical input -> byte identical output. |
| AC-10 | Zero Production Regression: 124 existing unit/integration tests pass. |