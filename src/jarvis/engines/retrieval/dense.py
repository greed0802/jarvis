"""DenseVectorRetriever — infrastructure-decoupled dense search."""

from __future__ import annotations

from jarvis.engines.retrieval.contracts import RankedCandidate, RetrievalQuery
from jarvis.engines.retrieval.protocols import EmbeddingProvider, VectorIndex

class DenseVectorRetriever:
    """Delegates storage to VectorIndex and embedding to EmbeddingProvider."""

    retriever_id = "dense_vector"

    def __init__(
        self,
        embedding_provider: EmbeddingProvider,
        vector_index: VectorIndex,
    ) -> None:
        self._embedding = embedding_provider
        self._index = vector_index

    def index_document(self, doc_id: str, text: str) -> None:
        vec = self._embedding.embed_text(text)
        self._index.upsert(doc_id, vec, {"text": text})

    def retrieve(self, query: RetrievalQuery) -> tuple[RankedCandidate, ...]:
        q_vec = self._embedding.embed_text(query.query_text)
        hits = self._index.search(q_vec, query.top_k)

        results = []
        for rank_idx, (doc_id, score) in enumerate(hits, start=1):
            results.append(
                RankedCandidate(
                    document_id=doc_id,
                    content="",
                    score=score,
                    rank=rank_idx,
                    strategy_origin=self.retriever_id,
                )
            )
        return tuple(results)