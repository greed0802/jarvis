"""Pure mathematical metric evaluators. ZERO I/O, Logging, or Framework dependencies."""

from __future__ import annotations
import math

from jarvis.evaluation.subsystem_metrics import (
    citation_coverage,
    unsupported_assertion_rate,
    route_correctness,
    projection_determinism_check,
)

def calculate_recall_at_k(retrieved_ids: list[str], ground_truth_ids: list[str], k: int) -> float:
    """Fraction of relevant evidence retrieved in top K."""
    if not ground_truth_ids:
        return 0.0
    top_k = set(retrieved_ids[:k])
    truth_set = set(ground_truth_ids)
    hits = len(top_k & truth_set)
    return hits / len(truth_set)

def calculate_precision_at_k(retrieved_ids: list[str], ground_truth_ids: list[str], k: int) -> float:
    """Fraction of top K retrieved that are relevant."""
    if not retrieved_ids or k <= 0:
        return 0.0
    top_k = set(retrieved_ids[:k])
    truth_set = set(ground_truth_ids)
    hits = len(top_k & truth_set)
    return hits / min(k, len(retrieved_ids))

def calculate_ndcg_at_k(retrieved_ids: list[str], ground_truth_ids: list[str], k: int) -> float:
    """Normalized Discounted Cumulative Gain at top K.
    Binary relevance: 1 if hit, 0 if miss.
    """
    if not ground_truth_ids:
        return 0.0

    dcg = 0.0
    for i, rid in enumerate(retrieved_ids[:k]):
        if rid in ground_truth_ids:
            # Relevance = 1
            dcg += 1.0 / math.log2(i + 2) # i=0 -> log2(2) = 1

    idcg = 0.0
    # Ideal ranking would have all hits at the beginning
    ideal_hits = min(len(ground_truth_ids), k)
    for i in range(ideal_hits):
        idcg += 1.0 / math.log2(i + 2)

    return dcg / idcg if idcg > 0.0 else 0.0

def calculate_mrr(retrieved_ids: list[str], ground_truth_ids: list[str]) -> float:
    """Multiplicative inverse of the rank of the first relevant evidence ID."""
    if not ground_truth_ids:
        return 0.0
    truth_set = set(ground_truth_ids)
    for i, rid in enumerate(retrieved_ids):
        if rid in truth_set:
            return 1.0 / (i + 1)
    return 0.0

# Legacy compatibility aliases (to prevent evaluation failures)
def precision_at_k(retrieved_ids: list[str], expected_ids: list[str], k: int) -> float:
    return calculate_precision_at_k(retrieved_ids, expected_ids, k)

def recall_at_k(retrieved_ids: list[str], expected_ids: list[str], k: int) -> float:
    return calculate_recall_at_k(retrieved_ids, expected_ids, k)