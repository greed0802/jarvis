"""Protocol interfaces for reasoning pipeline components."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from jarvis.engines.retrieval.contracts import RankedCandidate
from jarvis.engines.reasoning.contracts import (
    ReRankedCandidate,
    CompressedContext,
    EvidenceGraph,
)

@runtime_checkable
class BaseReRanker(Protocol):
    """Re-ranks candidates retrieved across fusion strategies for reasoning relevance."""

    def rerank(self, candidates: tuple[RankedCandidate, ...], query: str) -> tuple[ReRankedCandidate, ...]:
        """Produce a newly ranked collection without making in-place modifications."""
        ...

@runtime_checkable
class ContextCompressor(Protocol):
    """Compresses re-ranked candidates into optimal contexts, retaining provenance."""

    def compress(self, candidates: tuple[ReRankedCandidate, ...], max_tokens: int) -> CompressedContext:
        """Compress text while outputting strict CompressionSpanMaps."""
        ...

@runtime_checkable
class MultiDocumentSynthesizer(Protocol):
    """Graph generator that synthesizes causality across multiple documents."""

    def synthesize(self, context: CompressedContext) -> EvidenceGraph:
        """Create an immutable structured graph of evidence references."""
        ...