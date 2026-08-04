"""ProjectUnderstandingStore — persistent state and indexes for understanding data.

Owns the persisted ProjectUnderstanding records. Append-only semantics.

Per C1.13: This module SHALL NOT import CheckMateEngine, ExecutionOutcome,
RuleSnapshot, RuleRegistry, or CheckMateRule.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from jarvis.contracts.understanding import ProjectUnderstanding

@dataclass
class ProjectUnderstandingStore:
    """Append-only store for ProjectUnderstanding records.

    Each ingested FindingReport produces exactly one ProjectUnderstanding record.
    The store maintains query indexes for efficient category-based lookups.
    """

    _records: list[ProjectUnderstanding] = field(default_factory=list)

    def append(self, understanding: ProjectUnderstanding) -> None:
        """Persist a ProjectUnderstanding record.

        Records are appended in order. The store does not support mutation
        or deletion — per immutability guarantees of the public contract.
        """
        self._records.append(understanding)

    def list_all(self) -> list[ProjectUnderstanding]:
        """Return all stored understanding records."""
        return list(self._records)

    def get(self, report_id: str) -> ProjectUnderstanding | None:
        """Retrieve a specific understanding by report_id."""
        for record in self._records:
            if record.report_id == report_id:
                return record
        return None

    def find_by_category(self, category: str) -> list[ProjectUnderstanding]:
        """Find all records that contain findings in the given category."""
        results: list[ProjectUnderstanding] = []
        for record in self._records:
            if category in record.findings_by_category:
                results.append(record)
        return results

    @property
    def record_count(self) -> int:
        return len(self._records)