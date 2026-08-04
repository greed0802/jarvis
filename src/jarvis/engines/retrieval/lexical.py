"""BM25LexicalRetriever — simple BM25-inspired keyword retrieval."""

from __future__ import annotations

import re
from math import log

from jarvis.engines.retrieval.contracts import RankedCandidate, RetrievalQuery

class BM25LexicalRetriever:
    """BM25-inspired keyword retriever using token overlap scoring."""

    retriever_id = "bm25_lexical"
    _K1 = 1.5
    _B = 0.75

    def __init__(self, documents: dict[str, str] | None = None) -> None:
        self._docs: dict[str, str] = documents or {}
        self._avgdl: float = 1.0
        self._idf_cache: dict[str, float] = {}
        if self._docs:
            self._compute_idf()

    def add_document(self, doc_id: str, text: str) -> None:
        self._docs[doc_id] = text
        self._compute_idf()

    def retrieve(self, query: RetrievalQuery) -> tuple[RankedCandidate, ...]:
        terms = query.query_text.lower().split()
        N = max(1, len(self._docs))
        avgdl = max(1, sum(len(d.split()) for d in self._docs.values()) / N) if self._docs else 1
        results = []

        for doc_id, text in self._docs.items():
            if query.filter.document_ids and doc_id not in query.filter.document_ids:
                continue
            dl = len(text.split())
            score = 0.0
            for term in terms:
                tf = text.lower().count(term)
                df = sum(1 for d in self._docs.values() if term in d.lower())
                idf = log((N - df + 0.5) / (df + 0.5) + 1)
                numerator = tf * (self._K1 + 1)
                denominator = tf + self._K1 * (1 - self._B + self._B * dl / avgdl)
                score += idf * numerator / denominator
            results.append(RankedCandidate(
                document_id=doc_id,
                content=text[:200],
                score=score,
                strategy_origin=self.retriever_id,
            ))

        results.sort(key=lambda c: c.score, reverse=True)
        for i, c in enumerate(results):
            object.__setattr__(c, "rank", i + 1)
        return tuple(results[:query.top_k])

    def _compute_idf(self) -> None:
        self._idf_cache = {}