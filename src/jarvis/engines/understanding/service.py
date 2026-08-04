"""ProjectUnderstandingService — read/query interface for understanding data.

Exposes a clean query API that returns only the ProjectUnderstanding
public contract (C1.13). Does NOT expose store internals or raw findings.

Per C1.13: This module SHALL NOT import CheckMateEngine, ExecutionOutcome,
RuleSnapshot, RuleRegistry, or CheckMateRule.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from jarvis.contracts.capabilities import FindingReport
from jarvis.contracts.understanding import ProjectUnderstanding
from jarvis.engines.understanding.importer import ProjectUnderstandingImporter
from jarvis.engines.understanding.store import ProjectUnderstandingStore

@dataclass
class ProjectUnderstandingService:
    """Service facade for the Project Understanding domain.

    Orchestrates the import flow (FindingReport → ProjectUnderstanding)
    and exposes read/query operations over stored understanding records.
    """

    store: ProjectUnderstandingStore = field(default_factory=ProjectUnderstandingStore)
    importer: ProjectUnderstandingImporter = field(
        default_factory=ProjectUnderstandingImporter
    )

    def ingest(self, report: FindingReport) -> ProjectUnderstanding:
        """Ingest a FindingReport and persist its understanding.

        Returns the ProjectUnderstanding record without exposing the
        internal execution model.
        """
        understanding = self.importer.import_report(report)
        self.store.append(understanding)
        return understanding

    def get_understanding(self, report_id: str) -> ProjectUnderstanding | None:
        """Retrieve a specific understanding by report_id.

        Returns:
            The ProjectUnderstanding contract or None if not found.
        """
        return self.store.get(report_id)

    def list_all(self) -> list[ProjectUnderstanding]:
        """List all understanding records.

        Returns:
            All persisted ProjectUnderstanding contracts.
        """
        return self.store.list_all()

    def find_by_category(self, category: str) -> list[ProjectUnderstanding]:
        """Find all understanding records containing findings in a category.

        Args:
            category: The FindingCategory string to search for.

        Returns:
            List of ProjectUnderstanding contracts for reports with findings
            in the specified category.
        """
        return self.store.find_by_category(category)

    def get_summary_statistics(self) -> dict[str, int]:
        """Get aggregate statistics across all understanding records.

        Returns:
            Summary of total reports, rules executed, and findings.
        """
        records = self.store.list_all()
        if not records:
            return {
                "total_reports": 0,
                "total_rules_executed": 0,
                "total_findings": 0,
            }
        total_reports = len(records)
        total_rules = sum(r.total_rules_executed for r in records)
        total_findings = sum(r.total_findings for r in records)
        return {
            "total_reports": total_reports,
            "total_rules_executed": total_rules,
            "total_findings": total_findings,
        }

    @property
    def is_empty(self) -> bool:
        return self.store.record_count == 0