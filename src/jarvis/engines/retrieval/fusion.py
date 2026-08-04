"""Pure-function fusion strategies — RRF and Weighted."""

from __future__ import annotations

from jarvis.engines.retrieval.contracts import RankedCandidate

class ReciprocalRankFusion:
    """RRF fusion: RRF(d) = sum(1 / (k + rank(d)))."""

    def combine(
        self,
        candidate_sets: dict[str, list[RankedCandidate]],
        top_k: int,
        k: int = 60,
    ) -> list[RankedCandidate]:
        return _rrf_fuse(candidate_sets, top_k, k)

class WeightedScoreFusion:
    """Weighted sum of normalized scores."""

    def __init__(self, weights: dict[str, float]) -> None:
        self._weights = weights

    def combine(
        self,
        candidate_sets: dict[str, list[RankedCandidate]],
        top_k: int,
    ) -> list[RankedCandidate]:
        return _weighted_fuse(candidate_sets, top_k, self._weights)

# ---------------------------------------------------------------------------
# Pure helper functions (shared, zero side effects)
# ---------------------------------------------------------------------------

def _rrf_fuse(
    candidate_sets: dict[str, list[RankedCandidate]],
    top_k: int,
    k: int = 60,
) -> list[RankedCandidate]:
    """Pure RRF fusion. Never mutates inputs."""
    doc_scores: dict[str, float] = {}
    doc_contents: dict[str, str] = {}
    doc_origins: dict[str, set[str]] = {}

    for strategy_id, candidates in candidate_sets.items():
        for rank_idx, cand in enumerate(candidates):
            rrf_score = 1.0 / (k + (rank_idx + 1))
            did = cand.document_id
            doc_scores[did] = doc_scores.get(did, 0.0) + rrf_score
            doc_contents.setdefault(did, cand.content)
            doc_origins.setdefault(did, set()).add(strategy_id)

    fused = []
    for doc_id, score in sorted(
        doc_scores.items(),
        key=lambda item: (-item[1], item[0]),
    ):
        fused.append(
            RankedCandidate(
                document_id=doc_id,
                content=doc_contents.get(doc_id, ""),
                score=score,
                strategy_origin=",".join(sorted(doc_origins.get(doc_id, set()))),
            )
        )

    # Assign stable ranks
    for i, c in enumerate(fused):
        c = RankedCandidate(
            document_id=c.document_id,
            content=c.content,
            score=c.score,
            rank=i + 1,
            strategy_origin=c.strategy_origin,
        )
        fused[i] = c

    return fused[:top_k]

def _weighted_fuse(
    candidate_sets: dict[str, list[RankedCandidate]],
    top_k: int,
    weights: dict[str, float],
) -> list[RankedCandidate]:
    """Weighted score fusion. Never mutates inputs."""
    doc_scores: dict[str, float] = {}
    doc_contents: dict[str, str] = {}

    for strategy_id, candidates in candidate_sets.items():
        weight = weights.get(strategy_id, 1.0)
        max_score = max((c.score for c in candidates), default=1.0)
        for cand in candidates:
            normalized = cand.score / max_score if max_score > 0 else 0.0
            weighted = normalized * weight
            doc_scores[cand.document_id] = doc_scores.get(cand.document_id, 0.0) + weighted
            doc_contents.setdefault(cand.document_id, cand.content)

    fused = sorted(
        doc_scores.items(),
        key=lambda x: (-x[1], x[0]),
    )
    results = []
    for i, (doc_id, score) in enumerate(fused[:top_k]):
        results.append(
            RankedCandidate(
                document_id=doc_id,
                content=doc_contents.get(doc_id, ""),
                score=score,
                rank=i + 1,
                strategy_origin=",".join(sorted(weights.keys())),
            )
        )
    return results