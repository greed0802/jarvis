"""Subsystem-specific evaluation helpers (non-retrieval)."""

from __future__ import annotations
import json

def citation_coverage(claim_texts: list[str], cite_ids: list[str]) -> float:
    """Temporary binary placeholder for future claim-level coverage."""
    return 1.0 if cite_ids else 0.0

def unsupported_assertion_rate(claim_texts: list[str], cite_ids: list[str]) -> float:
    """Temporary placeholder for future claim-level ratio checks."""
    return 0.0 if cite_ids else 1.0

def route_correctness(actual_routes: list[str], expected_routes: list[str]) -> float:
    """Explicitly computed using set-overlap semantics for correct route fraction."""
    if not expected_routes:
        return 1.0
    return sum(1 for a in actual_routes if a in expected_routes) / len(expected_routes)

def is_deterministic(output_a: dict, output_b: dict) -> bool:
    """Returning boolean equality over json.dumps(..., sort_keys=True)."""
    return json.dumps(output_a, sort_keys=True) == json.dumps(output_b, sort_keys=True)

# Compatibility alias for existing frameworks testing determinism lists
def projection_determinism_check(runs: list[dict]) -> float:
    if not runs:
        return 1.0
    first = runs[0]
    return 1.0 if all(is_deterministic(r, first) for r in runs) else 0.0