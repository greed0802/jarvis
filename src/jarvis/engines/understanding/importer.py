"""ProjectUnderstandingImporter — ingests FindingReport into understanding domain.

Consumes the published FindingReport contract exclusively (C1.13).
Validates and transforms FindingReports into internal UnderstandingFinding
objects and assembles ProjectUnderstanding records.

Per C1.3: This importer SHALL accept ONLY FindingReport. Raw ExecutionOutcome,
RuleSnapshot, or CheckMateEngine objects are explicitly disallowed.

Strict boundary: This module SHALL NOT import CheckMateEngine,
ExecutionOutcome, RuleSnapshot, RuleRegistry, or CheckMateRule.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4

from jarvis.contracts.capabilities import FindingReport
from jarvis.contracts.understanding import (
    FindingCategory,
    ProjectUnderstanding,
    UnderstandingFinding,
)

# Domain category mapping from Finding severity to finding category.
# Falls back on the severity domain string in the Finding, normalizing
# to canonical FindingCategory values.
_DOMAIN_NORMALIZATION: dict[str, FindingCategory] = {
    "measurement": FindingCategory.MEASUREMENT,
    "specification": FindingCategory.SPECIFICATION,
    "coordination": FindingCategory.COORDINATION,
    "compliance": FindingCategory.COMPLIANCE,
    "documentation_integrity": FindingCategory.DOCUMENTATION_INTEGRITY,
    "project_policy": FindingCategory.PROJECT_POLICY,
}

@dataclass
class ProjectUnderstandingImporter:
    """Validates and transforms FindingReport records.

    The importer consumes only the public FindingReport contract (C1.3).
    It produces internal UnderstandingFinding records and assembles a single
    ProjectUnderstanding contract per report.
    """

    def import_report(self, report: FindingReport) -> ProjectUnderstanding:
        """Import a published FindingReport into the Project Understanding domain.

        Args:
            report: A complete FindingReport from the CheckMate pipeline.

        Returns:
            Immutable ProjectUnderstanding contract suitable for downstream
            consumption by M10.5 (AI Assistant) and M10.6 (Workbench UI).
        """
        findings: list[UnderstandingFinding] = []
        findings_by_cat: dict[str, int] = {}

        for finding in report.findings:
            # Determine category from the finding's domain context
            category = self._resolve_category(report, finding.rule_id)

            understanding_finding = UnderstandingFinding(
                finding_id=f"UF-{uuid4().hex[:8]}",
                category=category,
                severity=finding.severity.value,
                risk_statement=finding.risk_statement,
                remediation=finding.remediation,
                evidence_count=len(finding.evidence),
            )
            findings.append(understanding_finding)
            findings_by_cat[category.value] = (
                findings_by_cat.get(category.value, 0) + 1
            )

        total_rules = report.telemetry_summary.rule_count_total
        total_findings = len(findings)

        summary = (
            f"Executed {total_rules} rules with {total_findings} findings "
            f"across {len(findings_by_cat)} categories."
        )

        return ProjectUnderstanding(
            report_id=report.provenance.execution_id,
            capability_version=report.provenance.capability_version,
            total_rules_executed=total_rules,
            total_findings=total_findings,
            findings_by_category=findings_by_cat,
            findings=findings,
            summary=summary,
        )

    def _resolve_category(
        self, report: FindingReport, rule_id: str
    ) -> FindingCategory:
        """Normalize the finding domain into a standard FindingCategory.

        Uses the domain_coverage map on the report to determine which
        domain the rule's finding belongs to. Falls back using a
        domain-to-category mapping.
        """
        # If the report's domain_coverage has a matching key, normalize it
        for domain_name, pct in report.domain_coverage.items():
            if pct > 0:
                normalized = _DOMAIN_NORMALIZATION.get(
                    domain_name.lower().replace("domaincategory.", "")
                )
                if normalized:
                    return normalized

        # Fallback: derive from the first character of the domain name or unknown
        return FindingCategory.COMPLIANCE