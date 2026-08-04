"""Immutable reasoning contracts and trace artifacts."""

from __future__ import annotations

from dataclasses import dataclass, field

from jarvis.engines.retrieval.contracts import RankedCandidate
from jarvis.contracts.assistant import GroundingContext

@dataclass(frozen=True)
class ReRankedCandidate:
    """A retrieval candidate after reasoning-specific re-ranking."""

    candidate: RankedCandidate
    rerank_score: float
    original_rank: int

@dataclass(frozen=True)
class CompressionSpanMap:
    """Provenance tracking for compressed spans back to source artifacts."""

    original_span: str
    compressed_span: str
    evidence_id: str

@dataclass(frozen=True)
class CompressedContext:
    """Result of context compression retaining full deterministic provenance."""

    target_max_tokens: int
    compressed_text: str
    span_mappings: tuple[CompressionSpanMap, ...]
    preserved_evidence_ids: tuple[str, ...]

@dataclass(frozen=True)
class EvidenceNode:
    """A node inside the synthesized EvidenceGraph."""

    node_id: str
    document_id: str
    revision: str
    evidence_ids: tuple[str, ...]

@dataclass(frozen=True)
class EvidenceEdge:
    """A relationship between nodes inside the synthesized EvidenceGraph."""

    source_node_id: str
    target_node_id: str
    relationship_type: str

@dataclass(frozen=True)
class EvidenceGraph:
    """Immutable multi-document causality and correlation graph."""

    nodes: tuple[EvidenceNode, ...]
    edges: tuple[EvidenceEdge, ...]

@dataclass(frozen=True)
class ReasoningTrace:
    """Complete, immutable per-query reasoning execution record."""

    trace_id: str
    retrieval_trace_id: str
    reranked_candidates: tuple[ReRankedCandidate, ...]
    compressed_context: CompressedContext
    evidence_graph: EvidenceGraph
    grounding_context: GroundingContext
    latency_ms: float
    timestamp: str