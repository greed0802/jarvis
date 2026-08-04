"""Re-ranking algorithms (Heuristic and Model-based)."""

from __future__ import annotations

import re

from jarvis.engines.retrieval.contracts import RankedCandidate
from jarvis.engines.reasoning.contracts import ReRankedCandidate

class HeuristicReRanker:
    """Fast, deterministic re-ranking based on exact term match density."""

    def rerank(self, candidates: tuple[RankedCandidate, ...], query: str) -> tuple[ReRankedCandidate, ...]:
        terms = [t.lower() for t in query.split() if len(t) > 2]
        reranked = []
        for cand in candidates:
            content_lower = cand.content.lower()
            density = sum(content_lower.count(t) for t in terms) / max(1, len(content_lower.split()))
            rerank_score = cand.score + density
            reranked.append(ReRankedCandidate(
                candidate=cand,
                rerank_score=rerank_score,
                original_rank=cand.rank,
            ))

        # Deterministic sort: score desc, document_id asc
        reranked.sort(key=lambda r: (-r.rerank_score, r.candidate.document_id))
        return tuple(reranked)

class ModelReRanker:
    """Mock model-based re-ranker for EP-B102 verification (no external inference)."""

    def rerank(self, candidates: tuple[RankedCandidate, ...], query: str) -> tuple[ReRankedCandidate, ...]:
        # Sort completely deterministically to simulate model deterministic output
        reranked = [
            ReRankedCandidate(candidate=c, rerank_score=c.score * 1.5, original_rank=c.rank)
            for c in candidates
        ]
        reranked.sort(key=lambda r: (-r.rerank_score, r.candidate.document_id))
        return tuple(reranked)