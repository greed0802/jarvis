# GD-0001: Golden Datasets Governance

**Status:** Active
**Date:** 2026-07-30
**Owner:** Capability Engineering

## 1. Objective
Establish governance and versioning rules for machine-readable ground truth corpora.

## 2. Dataset Schema (v1.0.0)
- `version`: The dataset format version.
- `queries`: Array of test cases.
  - `query_id`: Unique string identifier.
  - `query_text`: The semantic user input.
  - `relevant_evidence`: Strict list of evidence IDs required to answer the query.
  - `query_type`: e.g., "factoid", "reasoning", "aggregation".
  - `difficulty`: e.g., "low", "medium", "hard".
  - `reasoning_depth`: Integer indicating required hops.

## 3. Storage
Machine-readable records MUST live in `docs/evaluation/datasets/` in `.yaml` format, explicitly separated from this markdown.