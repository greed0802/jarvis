"""CheckMate Interpretation Engine.

Converts platform evidence and findings into interpreted application
state. Interpretation occurs exactly once.

Responsibilities:
- Severity classification (deterministic mapping)
- Finding categorization and grouping
- Recommendation generation (advisory only)
- Statistical aggregation

No Presentation Model. No rendering. No reports. No exports.

Authority:
  - EQ-0021 (Permanently Frozen)
  - Application Architecture Principles v1.0
  - CheckMate Recommendation Policy (EQ-0021-S4)
  - IP-0004 — CheckMate Interpretation Engine
"""

from __future__ import annotations

import enum
from typing import Any

from jarvis.applications.checkmate.context import ApplicationContext
from jarvis.parsers.costx.boq_intelligence import BOQIntelligenceResult
from jarvis.engines.validation.engine import ValidationFindings, ValidationFinding
from jarvis.applications.checkmate.interpretation.models import (
    Severity,
    SeverityInfo,
    SeverityMap,
    FindingGroup,
    FindingGroups,
    Recommendation,
    RecommendationSet,
    InterpretationStatistics,
    InterpretationSummary,
)

# ============================================================================
# Severity Classification Rules
# ============================================================================
# Classification is deterministic: finding_type → Severity
# Contract: Validation Findings Contract v1.0.0 finding_type values
_SEVERITY_RULES: dict[str, Severity] = {
    "Error": Severity.HIGH,
    "Warning": Severity.MEDIUM,
    "Information": Severity.LOW,
    "Critical": Severity.HIGH,
    "Hint": Severity.LOW,
}


def _classify_severity(finding: ValidationFinding) -> SeverityInfo:
    """Classify a single finding's severity deterministically from its finding_type.

    This ensures identical findings always get identical severity.

    Args:
        finding: The validation finding.

    Returns:
        SeverityInfo with classification and reasoning.
    """
    severity: Severity = _SEVERITY_RULES.get(
        finding.finding_type, Severity.LOW
    )
    return SeverityInfo(
        finding_id=finding.rule_id,
        severity=severity,
        reason=f"finding_type='{finding.finding_type}' => {severity.value}",
    )


# ============================================================================
# Finding Grouping
# ============================================================================

def _group_by_category(
    findings: tuple[ValidationFinding, ...],
) -> dict[str, FindingGroup]:
    """Group findings by category.

    Args:
        findings: Tuple of ValidationFindings to group.

    Returns:
        Mapping from category key to FindingGroup.
    """
    groups: dict[str, list[str]] = {}
    for f in findings:
        groups.setdefault(f.category, []).append(f.rule_id)
    return {
        k: FindingGroup(key=k, finding_ids=tuple(v))
        for k, v in groups.items()
    }


def _group_by_severity(
    findings: tuple[ValidationFinding, ...],
    severity_map: SeverityMap,
) -> dict[str, FindingGroup]:
    """Group findings by interpreted severity.

    Args:
        findings: Tuple of ValidationFindings to group.
        severity_map: SeverityMap produced during interpretation.

    Returns:
        Mapping from severity value to FindingGroup.
    """
    severity_dict: dict[str, list[str]] = {}
    for f in findings:
        # Find the severity for this finding
        severity = Severity.LOW  # default
        for entry in severity_map.entries:
            if entry.finding_id == f.rule_id:
                severity = entry.severity
                break
        severity_dict.setdefault(severity.value, []).append(f.rule_id)
    return {
        k: FindingGroup(key=k, finding_ids=tuple(v))
        for k, v in severity_dict.items()
    }


def _group_by_rule(
    findings: tuple[ValidationFinding, ...],
) -> dict[str, FindingGroup]:
    """Group findings by rule_id.

    Args:
        findings: Tuple of ValidationFindings to group.

    Returns:
        Mapping from rule_id to FindingGroup.
    """
    groups: dict[str, list[str]] = {}
    for f in findings:
        groups.setdefault(f.rule_id, []).append("N/A")
    return {
        k: FindingGroup(key=k, finding_ids=tuple(v))
        for k, v in groups.items()
    }


def _group_by_section(
    section_statistics: dict,
) -> dict[str, FindingGroup]:
    """Create section groups from evidence section statistics.

    Args:
        section_statistics: From BOQIntelligenceResult.

    Returns:
        Mapping from section name to FindingGroup (empty).
    """
    groups: dict[str, FindingGroup] = {}
    for section_name in sorted(section_statistics.keys()):
        groups[section_name] = FindingGroup(
            key=section_name,
            finding_ids=(),
        )
    return groups


def _group_findings(
    findings: tuple[ValidationFinding, ...],
    severity_map: SeverityMap,
    evidence: BOQIntelligenceResult,
) -> FindingGroups:
    """Create all finding groups.

    Groups by category, severity, section, and rule.

    Args:
        findings: All validation findings.
        severity_map: Produced severity map.
        evidence: Evidence for section statistics.

    Returns:
        FindingGroups with all four dimensions.
    """
    return FindingGroups(
        groups={
            "category": _group_by_category(findings),
            "severity": _group_by_severity(findings, severity_map),
            "section": _group_by_section(evidence.section_statistics),
            "rule": _group_by_rule(findings),
        }
    )


# ============================================================================
# Recommendation Generation
# ============================================================================
# Recommendations are generated ONLY during Interpretation.
# Source: CheckMate Recommendation Policy (EQ-0021-S4)

def _generate_recommendations(
    evidence: BOQIntelligenceResult,
    findings: tuple[ValidationFinding, ...],
) -> tuple[Recommendation, ...]:
    """Generate advisory recommendations from evidence patterns.

    Based on the Recommendation Policy (EQ-0021-S4), this generates
    recommendations for:
    - Zero quantity items with UOM
    - Level skips > 1
    - Headers with quantities
    - Missing descriptions
    - Missing UOMs

    Args:
        evidence: BOQIntelligenceResult.
        findings: All validation findings.

    Returns:
        Tuple of advisory Recommendations.
    """
    recs: list[Recommendation] = []
    rec_counter: dict[str, int] = {"ZERO": 0, "SKIP": 0, "HEADER_QTY": 0, "MISSING_DESC": 0, "MISSING_UOM": 0}

    # --- Zero-quantity items ---
    zero_items = evidence.zero_quantity_items
    if zero_items and len(zero_items) > 0:
        recs.append(Recommendation(
            id="REC-ZERO-001",
            text=f"Review {len(zero_items)} items with zero quantity — may affect cost plan completeness.",
            severity=Severity.MEDIUM,
            category="Data Quality",
            source_evidence=("zero_quantity_items",),
        ))

    # --- Level skip detection ---
    skips = evidence.detected_level_skips
    if skips and len(skips) > 0:
        recs.append(Recommendation(
            id="REC-LEVEL-001",
            text=f"Verify {len(skips)} level skips in hierarchy — may indicate missing WBS levels.",
            severity=Severity.HIGH,
            category="Structural",
            source_evidence=("detected_level_skips",),
        ))

    # --- Header rows with quantities ---
    header_violations = evidence.header_quantity_violations
    if header_violations and len(header_violations) > 0:
        recs.append(Recommendation(
            id="REC-HEADER-001",
            text=f"Verify {len(header_violations)} headers reporting quantities.",
            severity=Severity.MEDIUM,
            category="Structural",
            source_evidence=("header_quantity_violations",),
        ))

    # --- Missing descriptions ---
    completeness = evidence.completeness_findings
    if completeness and len(completeness) > 0:
        recs.append(Recommendation(
            id="REC-DESC-001",
            text=f"Review {len(completeness)} items missing descriptions — plan accuracy may be affected.",
            severity=Severity.HIGH,
            category="Data Quality",
            source_evidence=("completeness_findings",),
        ))

    # --- Missing UOM ---
    # (from validation findings rather than evidence)
    missing_uom_count: int = 0
    for f in findings:
        if "UOM" in (f.rule_id or "") and f.finding_value:
            try:
                value = f.finding_value
                if isinstance(value, (int, float)):
                    missing_uom_count += int(value)
                elif isinstance(value, str) and value.isdigit():
                    missing_uom_count += int(value)
                else:
                    missing_uom_count += 1
            except (ValueError, TypeError):
                missing_uom_count += 1
    if missing_uom_count > 0:
        recs.append(Recommendation(
            id="REC-UOM-001",
            text=f"Review {missing_uom_count} items missing UOM — unit rates cannot be verified.",
            severity=Severity.HIGH,
            category="Data Quality",
            source_evidence=("findings",),
        ))

    return tuple(recs)


# ============================================================================
# Interpretation Execution
# ============================================================================

def interpret(context: ApplicationContext) -> InterpretationSummary:
    """Execute deterministic interpretation.

    Interpretation occurs exactly once. All renderers consume the resulting
    InterpretationSummary (later transformed into Presentation Model by IP-0005).

    Processing order:
        1. Severity mapping (finding_type → Severity)
        2. Finding grouping (category, severity, section, rule)
        3. Recommendation generation (evidence-driven)
        4. Statistical aggregation

    Args:
        context: Immutable ApplicationContext containing evidence and findings.

    Returns:
        InterpretationSummary with all interpreted state.

    Raises:
        ValueError: If context is None or invalid.
    """
    evidence: BOQIntelligenceResult = context.evidence
    findings: tuple[ValidationFinding, ...] = context.findings.findings

    # Step 1: Severity classification
    severity_entries: tuple[SeverityInfo, ...] = tuple(
        _classify_severity(f) for f in findings
    )
    severity_map: SeverityMap = SeverityMap(entries=severity_entries)

    # Step 2: Finding grouping
    finding_groups: FindingGroups = _group_findings(findings, severity_map, evidence)

    # Step 3: Recommendation generation
    recs: tuple[Recommendation, ...] = _generate_recommendations(evidence, findings)
    recommendation_set: RecommendationSet = RecommendationSet(recommendations=recs)

    # Step 4: Statistics
    high_sev: int = len([e for e in severity_entries if e.severity == Severity.HIGH])
    medium_sev: int = len([e for e in severity_entries if e.severity == Severity.MEDIUM])
    low_sev: int = len([e for e in severity_entries if e.severity == Severity.LOW])
    stats: InterpretationStatistics = InterpretationStatistics(
        total_findings=len(findings),
        high_count=high_sev,
        medium_count=medium_sev,
        low_count=low_sev,
        categories=_count_finding_categories(finding_groups),
        total_sections=_count_sections(evidence),
        total_recommendations=len(recs),
    )

    # Assemble summary
    return InterpretationSummary(
        severity_map=severity_map,
        finding_groups=finding_groups,
        recommendations=recommendation_set,
        statistics=stats,
        is_interpreted=True,
    )


def _count_finding_categories(finding_groups: FindingGroups) -> int:
    """Count distinct finding categories from the 'category' group dimension."""
    return len(list(finding_groups.groups.get("category", {}).keys()))


def _count_sections(evidence: BOQIntelligenceResult) -> int:
    """Count distinct sections from evidence section statistics."""
    return len(list(evidence.section_statistics.keys()))