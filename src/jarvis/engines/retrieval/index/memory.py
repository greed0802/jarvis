"""InMemoryVectorIndex — mock adapter implementing VectorIndex protocol."""

from __future__ import annotations

from math import sqrt

from jarvis.engines.retrieval.protocols import VectorIndex

class InMemoryVectorIndex(VectorIndex):
    """In-memory vector store for EP-B101 verification.

    Uses cosine similarity for search. No external dependencies.
    """

    def __init__(self) -> None:
        self._store: dict[str, tuple[tuple[float, ...], dict]] = {}

    def upsert(self, id: str, vector: tuple[float, ...], metadata: dict) -> None:
        self._store[id] = (vector, metadata)

    def search(self, vector: tuple[float, ...], top_k: int) -> list[tuple[str, float]]:
        results = []
        for doc_id, (doc_vec, _) in self._store.items():
            sim = self._cosine_similarity(vector, doc_vec)
            results.append((doc_id, sim))
        results.sort(key=lambda x: x[1], reverse=True)
        # deterministic tie-breaking: stable sort, then by id
        return results[:top_k]

    @staticmethod
    def _cosine_similarity(a: tuple[float, ...], b: tuple[float, ...]) -> float:
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = sqrt(sum(x * x for x in a))
        norm_b = sqrt(sum(y * y for y in b))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)