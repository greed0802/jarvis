"""ProjectUnderstanding public contract for M10.4.

Defines the technology-agnostic immutable contract that downstream consumers
(M10.5 AI Assistant, M10.6 Workbench UI) integrate against.

Per C1.13: This contract is the ONLY public interface exposed by
the Project Understanding domain. Internal models (ExecutionOutcome,
CheckMateEngine, RuleSnapshot) SHALL NOT be imported by this module
or by any Project Understanding component.

Architecture conformance: ADR-0030 (C1.3), ADR-0031 (C1.13, C1.15).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

# =============================================================================
# Domain Classification
# =============================================================================

class FindingCategory(StrEnum):
    """Domain-aligned categories for QS findings per ADR-0030 C1.8."""

    MEASUREMENT = "measurement"
    SPECIFICATION = "specification"
    COORDINATION = "coordination"
    COMPLIANCE = "compliance"
    DOCUMENTATION_INTEGRITY = "documentation_integrity"
    PROJECT_POLICY = "project_policy"


@dataclass(frozen=True)
class UnderstandingFinding:
    """A single quality-related finding as understood by the Project Understanding domain.

    This is the public view of a Finding — technology-agnostic, domain-classified,
    and devoid of engine-specific implementation details.
    """

    finding_id: str
    category: FindingCategory
    severity: str
    risk_statement: str
    remediation: str
    evidence_count: int = 0


# =============================================================================
# ProjectUnderstanding — Public Contract (C1.15)
# =============================================================================

@dataclass(frozen=True)
class ProjectUnderstanding:
    """Immutable public contract for downstream consumers.

    This is the ONLY public output from the Project Understanding domain.
    It contains a digested view of findings without internal engine provenance
    or execution telemetry.

    Per C1.15: Frozen and immutable. No partial or incremental composition.
    """

    report_id: str
    capability_version: str
    total_rules_executed: int = 0
    total_findings: int = 0
    findings_by_category: dict[str, int] = field(default_factory=dict)
    findings: list[UnderstandingFinding] = field(default_factory=list)
    summary: str = ""