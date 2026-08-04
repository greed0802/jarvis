"""Test suite for Phase 1 - Retrieval Benchmark & Metrics."""

from __future__ import annotations
import inspect

from jarvis.evaluation.metrics import (
    calculate_recall_at_k,
    calculate_precision_at_k,
    calculate_ndcg_at_k,
    calculate_mrr
)

def test_pure_metrics_recall():
    """Verify Recall math."""
    retrieved = ["A", "B", "C", "D"]
    truth = ["B", "E"]
    # Top 3 recall: B is found, E is not. Top 3 are A, B, C.
    assert calculate_recall_at_k(retrieved, truth, k=3) == 0.5
    assert calculate_recall_at_k(retrieved, truth, k=1) == 0.0

def test_pure_metrics_precision():
    """Verify Precision math."""
    retrieved = ["A", "B", "C"]
    truth = ["A", "C"]
    # top 2: A, B. Truth hit is A. 1/2
    assert calculate_precision_at_k(retrieved, truth, k=2) == 0.5
    assert calculate_precision_at_k(retrieved, truth, k=3) == 2/3

def test_pure_metrics_ndcg():
    """Verify NDCG math."""
    # Ideal: A, B. Log2(2)=1, Log2(3)=0.63. IDCG = 1 + 1/log2(3) = 1.6309
    retrieved = ["X", "A", "B"]
    truth = ["A", "B"]
    
    # retrieved relevance: X(0), A(1), B(1)
    # DCG = 0 + 1/log2(3) + 1/log2(4) = 0 + 0.6309 + 0.5 = 1.1309
    score = calculate_ndcg_at_k(retrieved, truth, 3)
    assert 0.69 < score < 0.70 # ~0.693

def test_pure_metrics_mrr():
    """Verify MRR math."""
    retrieved = ["X", "Y", "A", "B"]
    truth = ["A"]
    # A is at rank 3
    assert calculate_mrr(retrieved, truth) == 1.0 / 3

def test_architecture_boundary():
    """Ensure core domain/engines do not import evaluation modules."""
    forbidden = ["evaluation", "jarvis.evaluation"]
    modules = [
        "jarvis.engines.retrieval",
        "jarvis.engines.reasoning",
        "jarvis.engines.generation",
    ]

    import importlib
    for mod_name in modules:
        try:
            mod = importlib.import_module(mod_name)
            src = inspect.getsource(mod)
            for f in forbidden:
                assert f"import {f}" not in src
                assert f"from {f}" not in src
        except ImportError:
            pass

def test_benchmark_runner_deterministic():
    """Ensure runner yields exactly identical outputs over strict inputs."""
    from jarvis.evaluation.retrieval_runner import RetrievalBenchmarkRunner
    import json
    # Running it via the real config guarantees output
    runner1 = RetrievalBenchmarkRunner("docs/evaluation/benchmark_manifest.yaml")
    runner2 = RetrievalBenchmarkRunner("docs/evaluation/benchmark_manifest.yaml")
    
    r1 = runner1.run(iterations=1)
    r2 = runner2.run(iterations=1)
    
    # Should be perfectly identical metrics
    assert r1["metrics"]["NDCG@E_10"] == r2["metrics"]["NDCG@E_10"]
    assert r1["metrics"]["Recall@E_10"] == r2["metrics"]["Recall@E_10"]

import pytest

def test_public_api_backwards_compatibility():
    """Verify that importing non-retrieval helpers from metrics.py still works seamlessly."""
    try:
        from jarvis.evaluation.metrics import (
            citation_coverage,
            unsupported_assertion_rate,
            route_correctness,
            projection_determinism_check,
        )
    except ImportError as e:
        pytest.fail(f"Public API compatibility broken: {e}")

    # Verify they actually function correctly
    assert citation_coverage(["c"], ["a"]) == 1.0
    assert unsupported_assertion_rate(["c"], ["a"]) == 0.0
    assert route_correctness(["a"], ["a"]) == 1.0
    assert projection_determinism_check([{"a": 1}, {"a": 1}]) == 1.0
