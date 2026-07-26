"""Presentation Model — Immutable presentation state (IP-0005).

All view models are immutable, deterministic, self-contained,
serializable, and renderer-independent. No interpretation. No
business logic. No rendering.

The PresentationModel is the ONLY object that future renderers consume.

Authority:
  - EQ-0021 (Permanently Frozen)
  - Application Architecture Principles v1.0 (Principle 2 — Rendering Many)
  - IP-0005 — CheckMate Presentation Model Assembly
"""

from __future__ import annotations

from dataclasses import dataclass, field


# ============================================================================
# Leaf View Models
# ============================================================================


@dataclass(frozen=True)
class FindingDisplay:
    """A single finding ready for presentation.

    Contains precomputed display labels, sorting key, and group
    identifier. No renderer computes labels or grouping.

    Attributes:
        finding_id: Rule ID from validation (e.g., 'V-001').
        category: Display category name.
        finding_type: Type label (Error, Warning, Information, etc.).
        severity_label: Presentation-ready severity string (HIGH, MEDIUM, LOW).
        display_title: Human-readable title.
        display_description: Human-readable description.
        sort_key: Deterministic sort key for stable ordering.
        group_identifier: Precomputed group for navigation.
    """

    finding_id: str
    category: str
    finding_type: str
    severity_label: str
    display_title: str
    display_description: str
    sort_key: str
    group_identifier: str


@dataclass(frozen=True)
class RecommendationDisplay:
    """A single recommendation ready for presentation.

    Contains display title, advisory text, severity, category,
    and display ordering. Future renderers simply iterate.

    Attributes:
        recommendation_id: Stable recommendation identifier.
        display_title: Human-readable title.
        advisory_text: Advisory description text.
        severity_label: Presentation severity string.
        category: Display category.
        display_order: Ordering for display list rendering.
    """

    recommendation_id: str
    display_title: str
    advisory_text: str
    severity_label: str
    category: str
    display_order: int


@dataclass(frozen=True)
class SectionDisplay:
    """One BOQ section ready for presentation.

    Externalized by section name. Contains:
    - Finding references
    - Recommendation references
    - Statistics (from evidence)

    Attributes:
        section_name: BOQ section name (e.g., 'Section A').
        display_title: Human-readable title.
        finding_id_count: Number of findings in this section.
        recommending_count: Number of recommendations for this section.
        item_count: Number of items in the section.
    """

    section_name: str
    display_title: str
    finding_id_count: int
    recommendation_count: int
    item_count: int


@dataclass(frozen=True)
class NavigationEntry:
    """A single navigation reference entry.

    Contains a label, target key, and display order. No business meaning.

    Attributes:
        label: Navigation label.
        target_key: Internal target key for navigation.
        href: Link target for navigation.
    """

    label: str
    target_key: str
    href: str


# ============================================================================
# View Models
# ============================================================================


@dataclass(frozen=True)
class DashboardView:
    """Dashboard-level statistics and summary.

    Headline statistics for overview — no computation, just presentation.

    Attributes:
        total_findings: Total number of findings displayed.
        total_recommendations: Total number of recommendations displayed.
        high_severity_count: Count of HIGH severity items.
        medium_severity_count: Count of MEDIUM severity items.
        low_severity_count: Count of LOW severity items.
        total_sections: Total number of sections displayed.
    """

    total_findings: int
    total_recommendations: int
    high_severity_count: int
    medium_severity_count: int
    low_severity_count: int
    total_sections: int


@dataclass(frozen=True)
class SummaryView:
    """Application-level summary view.

    Contains application metadata, interpretation summary, review placeholders,
    and overall status. No formatting.

    Attributes:
        application_title: Application title.
        application_version: Version string.
        execution_timestamp: ISO timestamp.
        finding_summary: One-line summary of findings.
        recommendation_summary: One-line summary of recommendations.
        overall_severity: Highest severity across all findings.
    """

    application_title: str
    application_version: str
    execution_timestamp: str
    finding_summary: str
    recommendation_summary: str
    overall_severity: str


@dataclass(frozen=True)
class FindingView:
    """Presentation-ready findings list.

    Each Entry contains precomputed display labels and sort keys.

    Attributes:
        items: Tuple of FindingDisplay in presentation order.
    """

    items: tuple[FindingDisplay, ...]

    def __len__(self) -> int:
        return len(self.items)


@dataclass(frozen=True)
class RecommendationView:
    """Presentation-ready recommendations list.

    Attributes:
        items: Tuple of RecommendationDisplay in presentation order.
    """

    items: tuple[RecommendationDisplay, ...]

    def __len__(self) -> int:
        return len(self.items)


@dataclass(frozen=True)
class SectionView:
    """Presentation by BOQ section.

    Each section is self-contained with finding/recommendation references
    and statistics. No renderer performs grouping.

    Attributes:
        items: Tuple of SectionDisplay ordered by section.
    """

    items: tuple[SectionDisplay, ...]

    def __len__(self) -> int:
        return len(self.items)


@dataclass(frozen=True)
class NavigationIndex:
    """Precomputed navigation index for one dimension.

    Future UI never searches — navigation already exists.

    Attributes:
        title: Display title for this index.
        items: Tuple of NavigationEntry in display order.
    """

    title: str
    items: tuple[NavigationEntry, ...]

    def __len__(self) -> int:
        return len(self.items)


@dataclass(frozen=True)
class NavigationView:
    """Precomputed navigation indexes for all dimensions.

    Groups find and recommendation-based navigation into named indexes.

    Attributes:
        indexes: Ordered tuple of NavigationIndex entries.
    """

    indexes: tuple[NavigationIndex, ...]

    def __len__(self) -> int:
        return len(self.indexes)


@dataclass(frozen=True)
class MetadataView:
    """Presentation metadata.

    Runtime identity, version, contract, and more. Immutable.

    Attributes:
        runtime_id: Unique execution run ID.
        application_name: Application name.
        application_version: Application version.
        contract_version: Contract version.
        engine_version: Engine version.
        execution_timestamp: ISO timestamp when the presentation was assembled.
        diagnostic_flags: Any diagnostic opt-in flags.
    """

    runtime_id: str
    application_name: str
    application_version: str
    contract_version: str
    engine_version: str
    execution_timestamp: str
    diagnostic_flags: tuple[str, ...]


# ============================================================================
# Root Model
# ============================================================================


@dataclass(frozen=True)
class PresentationModel:
    """Immutable root Presentation Model.

    Every child model is immutable. Contains no business logic, no
    computation, and no rendering.

    This is the ONLY object future renderers, exporters, and GUIs
    consume. It is the permanent architectural boundary established
    by the Application Constitution v1.0.

    Attributes:
        dashboard: Dashboard-level overview.
        summary: Application-level summary.
        findings: Presentation-ready findings.
        recommendations: Presentation-ready recommendations.
        sections: Presentation by BOQ section.
        navigation: Precomputed navigation indexes.
        metadata: Stable runtime identity.
    """

    dashboard: DashboardView
    summary: SummaryView
    findings: FindingView
    recommendations: RecommendationView
    sections: SectionView
    navigation: NavigationView
    metadata: MetadataView