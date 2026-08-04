# ES-B101: Hybrid Retrieval Specification

**Status:** Active
**Date:** 2026-07-30
**Paired Plan:** EP-B101
**Evidence:** EV-B101
**Owner:** Product Engineering

---

## 1. RRF Formula

$$RRF(d) = \sum_{m \in M} \frac{1}{k + r_m(d)}$$

Where k=60 (smoothing constant) and r_m(d) is 1-based rank.

---

## 2. RetrievalTrace Schema

```
RetrievalTrace:
  trace_id: str
  query: RetrievalQuery
  strategy_hits: {strategy_id: [RankedCandidate]}
  fused_hits: [RankedCandidate]
  fusion_algorithm: str
  latency_ms: float
  timestamp: str
```

---

## 3. Fusion Determinism

- Stable sort by (score DESC, document_id ASC)
- Zero in-place mutation of input collections