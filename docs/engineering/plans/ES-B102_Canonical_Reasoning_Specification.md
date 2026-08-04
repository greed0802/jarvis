# ES-B102: Canonical Reasoning Specification

**Status:** Active
**Date:** 2026-07-30
**Paired Plan:** EP-B102
**Evidence:** EV-B102
**Owner:** Product Engineering

---

## 1. Traceability & Provenance Schema

All text compression operations MUST emit span maps tracking source text back to evidence IDs:

```python
CompressionSpanMap:
  original_span: str
  compressed_span: str
  evidence_id: str
```

## 2. Multi-Document Graph Schema

Evidence synthesized from multiple chunks must be bound into an immutable graph representing cross-document causality or correlation:

```python
EvidenceNode:
  node_id: str
  document_id: str
  revision: str
  evidence_ids: tuple[str, ...]

EvidenceEdge:
  source_node_id: str
  target_node_id: str
  relationship_type: str
```

## 3. Byte-For-Byte Reproducibility

Intermediate models MUST be frozen (`@dataclass(frozen=True)`). Any sort operations MUST be deterministic (e.g. keying by hash/ID ties) to guarantee reproducing identical states.