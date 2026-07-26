"""Presentation Assembler — Immutable presentation state construction (IP-0005).

Converts computational state (InterpretationSummary) into immutable
presentation state (PresentationModel). Single responsibility: projection,
organization, navigation preparation, and view construction.

Assembler performs NO interpretation. It only:
- Copies values
- Projects fields
- Renames for presentation
- Organizes into views
- Builds navigation indexes

NO business logic. NO mutation. NO rendering.

Authority:
  - EQ-0021 (Permanently Frozen)
  - Application Architecture Principles v1.0 (Principle 2 — Rendering Many)
  - IP-0005 — CheckMate Presentation Model Assembly
"""

from __future__ import annotations

from datetime import datetime, timezone

from jarvis.applications.checkmate.context import ApplicationContext
from jarvis.applications.checkmate.interpretation.models import (
    Severity,
    InterpretationStatistics,
    InterpretationSummary,
)
from jarvis.engines.validation.engine import ValidationFinding
from jarvis.applications.checkmate.presentation.models import (
    DashboardView,
    FindingDisplay,
    FindingView,
    MetadataView,
    NavigationEntry,
    NavigationIndex,
    NavigationView,
    PresentationModel,
    RecommendationDisplay,
    RecommendationView,
    SectionDisplay,
    SectionView,
    SummaryView,
)

# ============================================================================
# Severity → severity_label mapping (no classification — already done)
# ============================================================================
_SEVERITY_TO_LABEL: dict[Severity, str] = {
    Severity.HIGH: "HIGH",
    Severity.MEDIUM: "MEDIUM",
    Severity.LOW: "LOW",
}

# ============================================================================
# Presentation Assembler — Public API
# ============================================================================

def assemble(context: ApplicationContext, interpretation: InterpretationSummary) -> PresentationModel:
    """Assemble an immutable PresentationModel from interpreted state.

    This is a pure projection — NO interpretation or computation.
    All values come directly from the interpreted summary.

    Args:
        context: Immutable ApplicationContext (for metadata, evidence, findings).
        interpretation: Immutable InterpretationSummary.

    Returns:
        Immutable PresentationModel consumed by all future renderers.
    """
    evidence = context.evidence
    findings_tuple = context.findings.findings
    severity_map = interpretation.severity_map
    stats = interpretation.statistics
    recs = interpretation.recommendations

    # ---- Dashboard ----
    dashboard = DashboardView(
        total_findings=stats.total_findings,
        total_recommendations=stats.total_recommendations,
        high_severity_count=stats.high_count,
        medium_severity_count=stats.medium_count,
        low_severity_count=stats.low_count,
        total_sections=stats.total_sections,
    )

    # ---- Summary ----
    overall_severity = _compute_overall_severity(stats)
    summary = SummaryView(
        application_title="CheckMate — BOQ Validation",
        application_version=context.application_version,
        execution_timestamp=context.execution_timestamp,
        finding_summary=f"{stats.total_findings} finding(s) detected across {stats.categories} categor{_y_plural(stats.categories)}.",
        recommendation_summary=f"{stats.total_recommendations} advisory recommendation(s) generated.",
        overall_severity=overall_severity,
    )

    # ---- Finding View ----
    findings_displays: list[FindingDisplay] = []
    for i, finding in enumerate(findings_tuple):
        # Find severity from the map
        severity_label = severity_map.to_dict().get(finding.rule_id, "LOW")
        group_key = f"{severity_label}_{finding.category}"
        display = FindingDisplay(
            finding_id=finding.rule_id,
            category=finding.category,
            finding_type=finding.finding_type,
            severity_label=severity_label,
            display_title=_finding_title(finding),
            display_description=_finding_description(finding, severity_label),
            sort_key=_finding_sort_key(severity_label, finding.category, i),
            group_identifier=group_key,
        )
        findings_displays.append(display)

    findings_view = FindingView(items=tuple(findings_displays))

    # ---- Recommendation View ----
    rec_displays: list[RecommendationDisplay] = []
    for i, rec in enumerate(recs.recommendations):
        rec_displays.append(RecommendationDisplay(
            recommendation_id=rec.id,
            display_title=_recommendation_title(rec),
            advisory_text=rec.text,
            severity_label=_SEVERITY_TO_LABEL.get(rec.severity, "LOW"),
            category=rec.category,
            display_order=i,
        ))
    rec_view = RecommendationView(items=tuple(rec_displays))

    # ---- Section View ----
    section_displays: list[SectionDisplay] = []
    for section_name in sorted(evidence.section_statistics.keys()):
        section_data = evidence.section_statistics.get(section_name, {})
        display = SectionDisplay(
            section_name=section_name,
            display_title=f"Section — {section_name}",
            finding_id_count=0,  # Sections don't yet have per-section finding counts from the evidence
            recommendation_count=0,
            item_count=section_data.get("items", 0),
        )
        section_displays.append(display)
    sections_view = SectionView(items=tuple(section_displays))

    # ---- Navigation View ----
    navigation = _build_navigation(findings_displays, rec_displays, section_displays)

    # ---- Metadata ----
    metadata = MetadataView(
        runtime_id=context.runtime_id,
        application_name="CheckMate",
        application_version=context.application_version,
        contract_version=context.findings.contract_version,
        engine_version=context.findings.engine_version,
        execution_timestamp=context.execution_timestamp,
        diagnostic_flags=(),
    )

    return PresentationModel(
        dashboard=dashboard,
        summary=summary,
        findings=findings_view,
        recommendations=rec_view,
        sections=sections_view,
        navigation=navigation,
        metadata=metadata,
    )

# ============================================================================
# Private Helpers — pure projection only
# ============================================================================

def _y_plural(n: int) -> str:
    return "ies" if n != 1 else "y"

def _compute_overall_severity(stats: InterpretationStatistics) -> str:
    """Return the highest severity label based on counts."""
    if stats.high_count > 0:
        return "HIGH"
    if stats.medium_count > 0:
        return "MEDIUM"
    if stats.low_count > 0:
        return "LOW"
    return "NONE"

_SEV_ORDER: dict[str, int] = {"HIGH": 0, "MEDIUM": 10, "LOW": 20}

def _finding_sort_key(severity_label: str, category: str, index: int) -> str:
    """Deterministic sort key — HIGH first, then category alphabetically, then index."""
    order = _SEV_ORDER.get(severity_label, 30)
    return f"{order:02d}_{category}_{index:04d}"

def _finding_title(finding: ValidationFinding) -> str:
    """Create display title from finding fields."""
    cat = finding.category or "Unknown"
    ftype = finding.finding_type or "Issue"
    return f"{ftype} — {cat} — {finding.rule_id}"

def _finding_description(finding: ValidationFinding, severity_label: str) -> str:
    """Create human-readable description for a finding."""
    cat = finding.category or "unknown"
    ftype = finding.finding_type or "issue"
    return f"{ftype} severity {severity_label} in category '{cat}' (rule {finding.rule_id})."

def _recommendation_title(rec) -> str:
    """Create display title from recommendation."""
    return f"{rec.id} — {rec.category} ({_SEVERITY_TO_LABEL.get(rec.severity, 'LOW')})"

def _build_navigation(
    findings: list[FindingDisplay],
    recommendations: list[RecommendationDisplay],
    sections: list[SectionDisplay],
) -> NavigationView:
    """Build precomputed navigation indexes.

    No computation of groupings — the groups are already organized.
    """
    indexes: list[NavigationIndex] = []

    # By Severity
    sev_entries: dict[str, list[NavigationEntry]] = {}
    for fd in findings:
        sev_entries.setdefault(fd.severity_label, []).append(NavigationEntry(
            label=fd.finding_id,
            target_key=fd.finding_id,
            href=f"#finding-{fd.finding_id}",
        ))
    for sev_label in ("HIGH", "MEDIUM", "LOW"):
        if sev_label in sev_entries:
            indexes.append(NavigationIndex(
                title=f"Findings — {sev_label} Severity",
                items=tuple(sev_entries[sev_label]),
            ))

    # By Category
    cat_entries: dict[str, list[NavigationEntry]] = {}
    for fd in findings:
        cat_entries.setdefault(fd.category, []).append(NavigationEntry(
            label=fd.finding_id,
            target_key=fd.finding_id,
            href=f"#finding-{fd.finding_id}",
        ))
    for cat in sorted(cat_entries.keys()):
        indexes.append(NavigationIndex(
            title=f"Findings — {cat}",
            items=tuple(cat_entries[cat]),
        ))

    # By Section
    sec_entries: list[NavigationEntry] = []
    for section in sections:
        sec_entries.append(NavigationEntry(
            label=section.display_title,
            target_key=section.section_name,
            href=f"#section-{section.section_name}",
        ))
    if sec_entries:
        indexes.append(NavigationIndex(
            title="By Section",
            items=tuple(sec_entries),
        ))

    # Recommendations by Severity
    rec_sev_entries: dict[str, list[NavigationEntry]] = {}
    for rd in recommendations:
        rec_sev_entries.setdefault(rd.severity_label, []).append(NavigationEntry(
            label=rd.recommendation_id,
            target_key=rd.recommendation_id,
            href=f"#rec-{rd.recommendation_id}",
        ))
    for sev_label in ("HIGH", "MEDIUM", "LOW"):
        if sev_label in rec_sev_entries:
            indexes.append(NavigationIndex(
                title=f"Recommendations — {sev_label} Severity",
                items=tuple(rec_sev_entries[sev_label]),
            ))

    # Recommendations by Category
    rec_cat_entries: dict[str, list[NavigationEntry]] = {}
    for rd in recommendations:
        rec_cat_entries.setdefault(rd.category, []).append(NavigationEntry(
            label=rd.recommendation_id,
            target_key=rd.recommendation_id,
            href=f"#rec-{rd.recommendation_id}",
        ))
    for cat in sorted(rec_cat_entries.keys()):
        indexes.append(NavigationIndex(
            title=f"Recommendations — {cat}",
            items=tuple(rec_cat_entries[cat]),
        ))

    return NavigationView(indexes=tuple(indexes))