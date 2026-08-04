# RB-0001: Retrieval Benchmark Evaluation Methodology

**Status:** Active
**Date:** 2026-07-30
**Owner:** Capability Engineering

## 1. Objective
Define pure metric formulas, measurement protocols, acceptance gates, and promotion gates without hardcoding baseline target values or expected performance scores.

## 2. Measurement Protocol
- Iterations: 5 distinct execution passes.
- Statistics: Compute median, min, max, and stddev across all 5 iterations.
- Base evidence metrics: Recall@E_K, Precision@E_K, NDCG@E_K, MRR@E.
- Latency metrics: P50_MS and P95_MS.

## 3. Pure Metric Formulas
- **Recall@K (Recall@E_K):** The fraction of total relevant evidence IDs successfully retrieved within the top K candidates.
- **Precision@K (Precision@E_K):** The fraction of candidates in the top K that are relevant evidence IDs.
- **NDCG@K (NDCG@E_K):** Normalized Discounted Cumulative Gain at K, where relevance is binary (1 if in golden set, 0 otherwise).
- **MRR (MRR@E):** Multiplicative inverse of the rank of the first relevant evidence ID.

## 4. Acceptance & Promotion Gates
- **Acceptance Gate:** Execution must complete successfully (0 failures) and emit a valid v1.0.0 schema JSON.
- **Promotion Gate:** The candidate must demonstrate statistically significant improvement in `NDCG@E_10` over the current Active Baseline without increasing P95_MS latency beyond bounds. NOTE: No static numbers are hardcoded here; success is strictly relative to the registered active baseline.

## 5. Implementation Isolation
Metrics MUST be computed against granular evidence IDs derived from `RetrievalTrace`. Pure math definitions only.