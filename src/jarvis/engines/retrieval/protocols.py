"""Protocol interfaces for retrieval pipeline components."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class BaseRetriever(Protocol):
    """A retrieval strategy that produces ranked candidates for a query."""

    @property
    def retriever_id(self) -> str: ...

    def retrieve(self, query: RetrievalQuery) -> tuple[RankedCandidate, ...]:
        """Return a ranked list of candidates for the query."""
        ...


@runtime_checkable
class EmbeddingProvider(Protocol):
    """Produces dense vector embeddings for text."""

    @property
    def dimension(self) -> int: ...

    def embed_text(self, text: str) -> tuple[float, ...]:
        """Return a fixed-dimension embedding vector for the given text."""
        ...


@runtime_checkable
class VectorIndex(Protocol):
    """Abstract key-vector store with upsert and search operations."""

    def upsert(self, id: str, vector: tuple[float, ...], metadata: dict) -> None:
        ...

    def search(self, vector: tuple[float, ...], top_k: int) -> list[tuple[str, float]]:
        ...


@runtime_checkable
class FusionStrategy(Protocol):
    """Pure function: combines ranked results from multiple strategies."""

    def combine(
        self,
        candidate_sets: dict[str, list[RankedCandidate]],
        top_k: int,
    ) -> list[RankedCandidate]:
        """Produce a fused ranking. MUST NOT mutate inputs."""
        ...