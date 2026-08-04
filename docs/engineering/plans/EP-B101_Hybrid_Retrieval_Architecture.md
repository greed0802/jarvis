# EP-B101: Track B1 — Canonical Hybrid Retrieval Pipeline (Architecture)

**Status:** Active
**Date:** 2026-07-30
**Milestone:** Track B1
**Paired Spec:** ES-B101
**Paired Evidence:** EV-B101
**Owner:** Product Engineering

---

## 1. Objective

Build the canonical hybrid retrieval pipeline with composition-root
coordinator, infrastructure-decoupled dense search, pure fusion strategies,
and immutable RetrievalTrace emission.

---

## 2. Architecture

```
RetrievalCoordinator
  ├── BaseRetriever[] (BM25LexicalRetriever, DenseVectorRetriever)
  │     ├── EmbeddingProvider (protocol)
  │     └── VectorIndex (protocol, in-memory adapter)
  └── FusionStrategy (RRF | Weighted)
       └── RetrievalTrace (immutable)
```

---

## 3. Acceptance Criteria

| AC | Criterion |
|----|-----------|
| AC-1 | Composition Root — constructor injection of retrievers + fusion |
| AC-2 | Dense Decoupling — VectorIndex + EmbeddingProvider protocols |
| AC-3 | RetrievalTrace — complete, immutable per-query trace |
| AC-4 | Pure Deterministic Fusion — no in-place mutation, stable sort |
| AC-5 | Public Facade Preservation — backward-compatible API |
| AC-6 | One-Way Dependency — zero presentation/CLI/UI imports |
| AC-7 | Expanded Benchmarking — P@K, R@K, MRR, NDCG, latency |
| AC-8 | Zero Regressions — 108 existing tests pass |