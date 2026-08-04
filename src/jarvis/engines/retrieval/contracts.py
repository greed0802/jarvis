"""Immutable retrieval contracts and trace artifacts."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class SearchFilter:
    """Metadata filter bounds for targeted retrieval."""

    document_ids: tuple[str, ...] = ()
    sheet_names: tuple[str, ...] = ()
    categories: tuple[str, ...] = ()


@dataclass(frozen=True)
class RetrievalQuery:
    """A retrieval request to the coordinator."""

    query_text: str
    top_k: int = 10
    filter: SearchFilter = field(default_factory=SearchFilter)
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class RankedCandidate:
    """A single candidate document produced by one or fused-by strategies."""

    document_id: str
    content: str
    score: float
    rank: int = 0
    strategy_origin: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class RetrievalTrace:
    """Complete, immutable per-query retrieval execution record."""

    trace_id: str
    query: RetrievalQuery
    strategy_hits: dict[str, tuple[RankedCandidate, ...]]
    fused_hits: tuple[RankedCandidate, ...]
    fusion_algorithm: str
    latency_ms: float
    timestamp: str