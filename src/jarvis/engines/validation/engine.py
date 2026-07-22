"""Validation Engine — deterministic rule evaluation.

Pure function: Findings = f(Evidence, Rules)

Consumes:
  - BOQIntelligenceResult (Evidence Contract v1.0.0)
  - Validation Rule Registry (packaged with engine)

Produces:
  - ValidationFindings (frozen, immutable, deterministic)

Implements 18 rules: V-001 through V-018.

Does NOT implement:
  - V-801, V-802 (Insufficient Evidence)
  - V-901, V-902 (Boundary Violation)

Authority:
  EQ-0013 Spike 4 — Engine Implementation
  HD-003 — Filesystem coupling eliminated (registry embedded in package)
  HD-004 — finding_type read from registry (heuristic removed)
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from jarvis.parsers.costx.boq_intelligence import BOQIntelligenceResult

# ============================================================
# Frozen Output Model — Validation Findings Contract v1.0.0
# ============================================================

@dataclass(frozen=True)
class ValidationFinding:
    """A single deterministic finding produced by a validation rule.

    Contract: Validation Findings Contract v1.0.0
    """
    rule_id: str
    rule_version: str
    category: str
    finding_type: str
    finding_value: Any
    evidence_fields: tuple[str, ...]


@dataclass(frozen=True)
class ValidationFindings:
    """Collection of validation findings.

    Contract: Validation Findings Contract v1.0.0
    """
    findings: tuple[ValidationFinding, ...]
    engine_version: str
    contract_version: str
    execution_timestamp: str


ENGINE_VERSION = "1.0.0"
CONTRACT_VERSION = "1.0.0"

# Rule statuses that are NOT executed
_SKIP_STATUSES = frozenset({"Candidate", "Deprecated", "Retired"})

# Evidence Contract v1.0.0 required fields (for V-001)
_REQUIRED_EVIDENCE_FIELDS = frozenset({
    "row_classification",
    "section_statistics",
    "boq_statistics",
    "known_anomalies",
})

# Expected row_classification keys (Contract SI-RC-04)
_EXPECTED_RC_KEYS = frozenset({"Head", "Note", "Section", "Item", "Other"})

# Path to embedded rule registry (relative to this module)
_REGISTRY_PATH = Path(__file__).parent / "data" / "rule_registry.json"


def _load_rule_registry() -> dict[str, dict]:
    """Load the Validation Rule Registry from the embedded package resource.

    Registry is bundled with the engine (HD-003: no filesystem coupling
    to data/reports/). Each rule must include:
      rule_id, category, evidence_fields, status, finding_type.

    Returns a dictionary keyed by rule_id for O(1) lookup.
    """
    with open(_REGISTRY_PATH, encoding="utf-8") as f:
        registry_data = json.load(f)
    rules = registry_data["rules"]
    return {r["rule_id"]: r for r in rules}


# ============================================================
# Rule Implementation Functions (18 rules)
# ============================================================

def _rule_V001_required_fields(evidence: BOQIntelligenceResult) -> Any:
    """Check all required evidence fields are present."""
    missing = []
    for field in _REQUIRED_EVIDENCE_FIELDS:
        value = getattr(evidence, field, None)
        if value is None:
            missing.append(field)
    return missing


def _rule_V002_classification_keys(evidence: BOQIntelligenceResult) -> Any:
    """Verify row_classification contains exactly 5 expected keys."""
    actual_keys = set(evidence.row_classification.keys())
    missing_keys = sorted(_EXPECTED_RC_KEYS - actual_keys)
    unexpected_keys = sorted(actual_keys - _EXPECTED_RC_KEYS)
    return {"missing_keys": missing_keys, "unexpected_keys": unexpected_keys}


def _rule_V003_nonnegative_counts(evidence: BOQIntelligenceResult) -> Any:
    """Verify all row_classification values are >= 0."""
    negatives = {
        key: value
        for key, value in evidence.row_classification.items()
        if value < 0
    }
    return negatives


def _rule_V004_row_sum_consistency(evidence: BOQIntelligenceResult) -> Any:
    """Verify sum of row_classification equals total_rows."""
    actual_sum = sum(evidence.row_classification.values())
    total_rows = evidence.boq_statistics.get("total_rows", 0)
    if actual_sum != total_rows:
        return {"actual_sum": actual_sum, "total_rows": total_rows,
                "difference": actual_sum - total_rows}
    return {"actual_sum": actual_sum, "total_rows": total_rows, "difference": 0}


def _rule_V005_section_quantity_nonnegative(evidence: BOQIntelligenceResult) -> Any:
    """Verify all sections have non-negative quantity counts."""
    problematic = {}
    for section, stats in evidence.section_statistics.items():
        quantity_count = stats.get("quantity_count", 0)
        if quantity_count < 0:
            problematic[section] = quantity_count
    return problematic

def _rule_V006_anomaly_row_range(evidence: BOQIntelligenceResult) -> Any:
    """Verify known_anomalies row_numbers are within [1, total_rows]."""
    total_rows = evidence.boq_statistics.get("total_rows", 0)
    out_of_range = []
    for anomaly in evidence.known_anomalies:
        row_number = anomaly.get("row_number")
        if row_number is not None and (row_number < 1 or row_number > total_rows):
            out_of_range.append(row_number)
    return out_of_range


def _rule_V007_code_completeness(evidence: BOQIntelligenceResult) -> Any:
    """Calculate ratio of code_rows to total_rows."""
    total_rows = evidence.boq_statistics.get("total_rows", 0)
    code_rows = evidence.boq_statistics.get("code_rows", 0)
    if total_rows == 0:
        return 0.0
    return round(code_rows / total_rows, 4)


def _rule_V008_description_completeness(evidence: BOQIntelligenceResult) -> Any:
    """Calculate ratio of description_rows to total_rows."""
    total_rows = evidence.boq_statistics.get("total_rows", 0)
    desc_rows = evidence.boq_statistics.get("description_rows", 0)
    if total_rows == 0:
        return 0.0
    return round(desc_rows / total_rows, 4)


def _rule_V009_quantity_completeness(evidence: BOQIntelligenceResult) -> Any:
    """Calculate ratio of quantity_rows to total_rows."""
    total_rows = evidence.boq_statistics.get("total_rows", 0)
    qty_rows = evidence.boq_statistics.get("quantity_rows", 0)
    if total_rows == 0:
        return 0.0
    return round(qty_rows / total_rows, 4)


def _rule_V010_hierarchy_availability(evidence: BOQIntelligenceResult) -> Any:
    """Check if hierarchy evidence is available (not None)."""
    return evidence.hierarchy is not None


def _rule_V011_root_header_count(evidence: BOQIntelligenceResult) -> Any:
    """Report number of root headers, or None if hierarchy unavailable."""
    stats = evidence.hierarchy_statistics
    if stats is None:
        return None
    return stats.get("root_headers")


def _rule_V012_hierarchy_depth(evidence: BOQIntelligenceResult) -> Any:
    """Report min/max depth, or None if hierarchy unavailable."""
    stats = evidence.hierarchy_statistics
    if stats is None:
        return None
    return {
        "min_depth": stats.get("min_depth"),
        "max_depth": stats.get("max_depth"),
    }


def _rule_V013_level_skip_availability(evidence: BOQIntelligenceResult) -> Any:
    """Check if level skip detection evidence is available."""
    return evidence.detected_level_skips is not None


def _rule_V014_level_skip_count(evidence: BOQIntelligenceResult) -> Any:
    """Count detected level skips, or None if unavailable."""
    skips = evidence.detected_level_skips
    if skips is None:
        return None
    return len(skips)


def _rule_V015_level_skip_magnitude(evidence: BOQIntelligenceResult) -> Any:
    """Report min/max skip magnitude, or None if unavailable."""
    skips = evidence.detected_level_skips
    if skips is None:
        return None
    magnitudes = [s.get("skip_levels", 0) for s in skips if "skip_levels" in s]
    if not magnitudes:
        return {"min_magnitude": None, "max_magnitude": None}
    return {"min_magnitude": min(magnitudes), "max_magnitude": max(magnitudes)}


def _rule_V016_zero_quantity_count(evidence: BOQIntelligenceResult) -> Any:
    """Count zero quantity items, or None if unavailable."""
    items = evidence.zero_quantity_items
    if items is None:
        return None
    return len(items)


def _rule_V017_containment_finding_count(evidence: BOQIntelligenceResult) -> Any:
    """Count structural containment findings, or None if unavailable."""
    findings = evidence.structural_containment_findings
    if findings is None:
        return None
    return len(findings)


def _rule_V018_empty_section_count(evidence: BOQIntelligenceResult) -> Any:
    """Count sections with zero items, or None if unavailable."""
    findings = evidence.completeness_findings
    if findings is None:
        return None
    return len(findings)


# Map rule_id to implementation function
_RULE_EXECUTORS: dict[str, Any] = {
    "V-001": _rule_V001_required_fields,
    "V-002": _rule_V002_classification_keys,
    "V-003": _rule_V003_nonnegative_counts,
    "V-004": _rule_V004_row_sum_consistency,
    "V-005": _rule_V005_section_quantity_nonnegative,
    "V-006": _rule_V006_anomaly_row_range,
    "V-007": _rule_V007_code_completeness,
    "V-008": _rule_V008_description_completeness,
    "V-009": _rule_V009_quantity_completeness,
    "V-010": _rule_V010_hierarchy_availability,
    "V-011": _rule_V011_root_header_count,
    "V-012": _rule_V012_hierarchy_depth,
    "V-013": _rule_V013_level_skip_availability,
    "V-014": _rule_V014_level_skip_count,
    "V-015": _rule_V015_level_skip_magnitude,
    "V-016": _rule_V016_zero_quantity_count,
    "V-017": _rule_V017_containment_finding_count,
    "V-018": _rule_V018_empty_section_count,
}


def validate(
    evidence: BOQIntelligenceResult,
    rules: list[str] | str = "all",
) -> ValidationFindings:
    """Execute validation rules against evidence.

    Pure function. Stateless. Deterministic. Immutable output.

    Args:
        evidence: BOQIntelligenceResult from Evidence Contract v1.0.0.
        rules: List of Rule IDs (e.g., ["V-001", "V-007"]) or "all"
               to execute all approved/verified rules.

    Returns:
        ValidationFindings: Frozen collection of findings, ordered by rule_id.

    Engine guarantees:
        - Same evidence + same rules → same finding fields (deterministic)
        - No filesystem writes, network calls, or database access
        - No mutation of evidence or rules
        - No assessment, recommendation, or judgment
        - Deprecated/Retired/Candidate rules are skipped
        - Consumer-independent (no Application logic)

    Authority: EQ-0013 Spike 4
    Contract: Validation Findings Contract v1.0.0
    """
    _registry = _load_rule_registry()

    # Determine which rules to execute
    if rules == "all":
        # Execute all implementable rules (exclude rejected rules)
        rule_ids = sorted(
            rid for rid in _RULE_EXECUTORS
            if rid in _registry
            and _registry[rid]["status"] not in _SKIP_STATUSES
        )
    else:
        rule_ids = sorted(rules)

    findings_list: list[ValidationFinding] = []

    for rule_id in rule_ids:
        # --- Lifecycle Enforcement ---
        rule = _registry.get(rule_id)
        if rule is None:
            continue  # Unknown rule — skip
        status = rule.get("status", "Candidate")
        if status in _SKIP_STATUSES:
            continue  # Not APPROVED/IMPLEMENTED/VERIFIED — skip

        # --- Classification Gate ---
        classification = rule.get("classification", "")
        if classification in ("Boundary Violation", "Insufficient Evidence"):
            continue  # Rejected rules — never execute

        # --- Execution ---
        executor = _RULE_EXECUTORS.get(rule_id)
        if executor is None:
            continue  # No implementation — skip

        finding_value = executor(evidence)

        # --- Finding Assembly ---
        # finding_type read directly from registry (HD-004: no heuristic)
        finding = ValidationFinding(
            rule_id=rule_id,
            rule_version=rule.get("rule_version", "1.0.0"),
            category=rule.get("category", ""),
            finding_type=rule.get("finding_type", "value"),
            finding_value=finding_value,
            evidence_fields=tuple(rule.get("evidence_fields", [])),
        )
        findings_list.append(finding)

    return ValidationFindings(
        findings=tuple(findings_list),
        engine_version=ENGINE_VERSION,
        contract_version=CONTRACT_VERSION,
        execution_timestamp=datetime.now(timezone.utc).isoformat(),
    )