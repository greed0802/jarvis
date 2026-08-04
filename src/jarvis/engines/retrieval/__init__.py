"""Jarvis retrieval pipeline — Track B1: Canonical Hybrid Retrieval."""

from jarvis.engines.retrieval.contracts import (
    RankedCandidate,
    RetrievalQuery,
    RetrievalTrace,
    SearchFilter,
)
from jarvis.engines.retrieval.protocols import (
    BaseRetriever,
    EmbeddingProvider,
    FusionStrategy,
    VectorIndex,
)
from jarvis.engines.retrieval.coordinator import RetrievalCoordinator
from jarvis.engines.retrieval.fusion import ReciprocalRankFusion, WeightedScoreFusion

__all__ = [
    "RankedCandidate",
    "RetrievalQuery",
    "RetrievalTrace",
    "SearchFilter",
    "BaseRetriever",
    "EmbeddingProvider",
    "FusionStrategy",
    "VectorIndex",
    "RetrievalCoordinator",
    "ReciprocalRankFusion",
    "WeightedScoreFusion",
]