"""Interpreted State Models.

Immutable pre-Presentation Model structures produced by the
Interpretation Engine. These are NOT Presentation Models — they
are internal computational state consumed by the Interpretation layer
and later by IP-0005 (Presentation Model Assembly).

Contains:
- Severity enum
- SeverityMap
- FindingGroup / FindingGroups
- Recommendation / RecommendationSet
- InterpretationStatistics
- InterpretationSummary

No Presentation Model. No rendering. No reports. No exports.

Authority:
  - EQ-0021 (Permanently Frozen)
  - Application Architecture Principles v1.0 (Principle 1 — Interpretation Once)
  - IP-0004 — CheckMate Interpretation Engine
"""

from __future__ import annotations

import enum
from dataclasses import dataclass, field
from typing import Any

class Severity(enum.Enum):
    """Deterministic severity classification for findings and recommendations.

    All severity mapping is performed during Interpretation. Rendering
    never reclassifies.
    """
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

@dataclass(frozen=True)
class SeverityInfo:
    """Immutable record of a single severity classification.

    Provides reasoning for auditability.

    Attributes:
        finding_id: The rule_id of the finding (e.g., "V-001").
        severity: Classified severity.
        reason: Deterministic reason for classification.
    """
    finding_id: str
    severity: Severity
    reason: str


@dataclass(frozen=True)
class SeverityMap:
    """Immutable mapping from finding_id to SeverityInfo.

    Produced once during interpretation. All renderers read from here.
    """
    entries: tuple[SeverityInfo, ...]

    def __len__(self) -> int:
        return len(self.entries)

    def of_severity(self, severity: Severity) -> tuple[SeverityInfo, ...]:
        """Return entries with the given severity."""
        return tuple(e for e in self.entries if e.severity == severity)

    def to_dict(self) -> dict[str, str]:
        """Return a simple {finding_id: severity_value} mapping."""
        return {e.finding_id: e.severity.value for e in self.entries}


@dataclass(frozen=True)
class FindingGroup:
    """Immutable group of findings by category, severity, section, or rule.

    Attributes:
        key: The grouping key (e.g., "Completeness", "HIGH", "Section A").
        finding_ids: Tuple of finding IDs in this group.
        count: Number of findings in the group.
    """
    key: str
    finding_ids: tuple[str, ...]
    count: int = field(init=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "count", len(self.finding_ids))


@dataclass(frozen=True)
class FindingGroups:
    """Immutable container of finding groups organized by category, severity,
    section, and rule.

    Categories supported: category, severity, section, rule.
    The dictionary key is the dimension name (e.g., "category").
    """
    groups: dict[str, dict[str, FindingGroup]]

    @classmethod
    def empty(cls) -> FindingGroups:
        return cls(groups={
            "category": {},
            "severity": {},
            "section": {},
            "rule": {},
        })

    def by_category(self, key: str) -> FindingGroup | None:
        return self.groups.get("category", {}).get(key)

    def by_severity(self, key: str) -> FindingGroup | None:
        return self.groups.get("severity", {}).get(key)

    def by_section(self, key: str) -> FindingGroup | None:
        return self.groups.get("section", {}).get(key)

    def by_rule(self, key: str) -> FindingGroup | None:
        return self.groups.get("rule", {}).get(key)


@dataclass(frozen=True)
class Recommendation:
    """Advisory recommendation generated from evidence patterns.

    Recommendations are advisory, rejectable, deterministic, and
    human-authority preserving. No imperative language.

    Attributes:
        id: Unique recommendation identifier.
        text: Advisory text with counts and context.
        severity: Associated severity level.
        category: Category of evidence/recommendation.
        source_evidence: Evidence fields that supported this recommendation.
    """
    id: str
    text: str
    severity: Severity
    category: str
    source_evidence: tuple[str, ...]


@dataclass(frozen=True)
class RecommendationSet:
    """Immutable collection of all recommendations.

    Produced during Interpretation only. All renderers read from here.
    """
    recommendations: tuple[Recommendation, ...]

    def __len__(self) -> int:
        return len(self.recommendations)

    def by_severity(self, severity: Severity) -> tuple[Recommendation, ...]:
        return tuple(r for r in self.recommendations if r.severity == severity)

    def by_category(self, category: str) -> tuple[Recommendation, ...]:
        return tuple(r for r in self.recommendations if r.category == category)


@dataclass(frozen=True)
class InterpretationStatistics:
    """Immutable statistics computed during interpretation.

    Pure computation — no presentation formatting.

    Attributes:
        total_findings: Total number of findings.
        high_count: Number of HIGH severity findings.
        medium_count: Number of MEDIUM severity findings.
        low_count: Number of LOW severity findings.
        categories: Number of distinct finding categories.
        total_sections: Number of distinct sections referenced.
        total_recommendations: Number of recommendations generated.
    """
    total_findings: int
    high_count: int
    medium_count: int
    low_count: int
    categories: int
    total_sections: int
    total_recommendations: int


@dataclass(frozen=True)
class InterpretationSummary:
    """Immutable summary of the interpretation result.

    Aggregates all interpreted state into a single summary.
    This is NOT a Presentation Model.

    Attributes:
        severity_map: Complete severity mapping.
        finding_groups: Grouped findings.
        recommendations: Generated advisory recommendations.
        statistics: Computed statistics.
        is_interpreted: Flag indicating interpretation was performed.
    """
    severity_map: SeverityMap
    finding_groups: FindingGroups
    recommendations: RecommendationSet
    statistics: InterpretationStatistics
    is_interpreted: bool = True