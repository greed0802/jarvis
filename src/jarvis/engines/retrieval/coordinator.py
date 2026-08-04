"""RetrievalCoordinator — composition root for hybrid retrieval."""

from __future__ import annotations

import time
from uuid import uuid4

from jarvis.engines.retrieval.contracts import (
    RankedCandidate,
    RetrievalQuery,
    RetrievalTrace,
)
from jarvis.engines.retrieval.protocols import BaseRetriever, FusionStrategy

class RetrievalCoordinator:
    """Composition root: receives retrievers + fusion via constructor injection.

    Executes all registered retrieval strategies, applies fusion,
    and emits a complete RetrievalTrace.
    """

    def __init__(
        self,
        retrievers: list[BaseRetriever],
        fusion: FusionStrategy,
    ) -> None:
        self._retrievers = retrievers
        self._fusion = fusion

    @property
    def retriever_ids(self) -> list[str]:
        return [r.retriever_id for r in self._retrievers]

    def execute_query(self, query: RetrievalQuery) -> RetrievalTrace:
        """Run all strategies, fuse results, and emit trace."""
        trace_id = uuid4().hex[:12]
        start = time.time()

        strategy_hits: dict[str, tuple[RankedCandidate, ...]] = {}
        hits_mutable: dict[str, list[RankedCandidate]] = {}
        for retriever in self._retrievers:
            candidates = retriever.retrieve(query)
            results_stable = tuple(sorted(candidates, key=lambda c: (-c.score, c.document_id)))
            strategy_hits[retriever.retriever_id] = results_stable
            hits_mutable[retriever.retriever_id] = list(results_stable)

        fused = self._fusion.combine(hits_mutable, query.top_k)
        end = time.time()
        fused_tuple = tuple(fused)

        return RetrievalTrace(
            trace_id=trace_id,
            query=query,
            strategy_hits=strategy_hits,
            fused_hits=fused_tuple,
            fusion_algorithm=type(self._fusion).__name__,
            latency_ms=round((end - start) * 1000, 1),
            timestamp=str(int(start)),
        )