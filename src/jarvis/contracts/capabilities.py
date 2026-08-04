"""Capability hosting contracts for the CheckMate capability layer.

Defines the technology-agnostic interface contracts per frozen ADR-0030 and
ADR-0031. These contracts govern how capabilities are hosted, how the public
FindingReport is structured, and how workspace evidence is bound.

No implementation logic lives here — only type definitions and invariants.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Protocol, runtime_checkable

# =============================================================================
# ADR-0031: FindingReport & Public Contract
# =============================================================================


class Severity(StrEnum):
    """Finding severity taxonomy per C1.6 invariant.

    Only these four levels are valid.CRITICAL/MAJOR findings indicate
    violations that require corrective action.
    """

    CRITICAL = "CRITICAL"
    MAJOR = "MAJOR"
    MINOR = "MINOR"
    INFORMATIONAL = "INFORMATIONAL"


class EvidenceSourceType(StrEnum):
    """Evidence source types per C1.2 Evidence Grounding invariant."""

    CELL = "cell"
    ROW = "row"
    SECTION = "section"
    RANGE = "range"
    COMPUTED = "computed"


@dataclass(frozen=True)
class EvidenceReference:
    """Immutable reference to source evidence (C1.2 invariant).

    Every Finding SHALL reference at least one EvidenceReference.
    """

    document_id: str
    sheet: str
    evidence_id: str
    source_type: EvidenceSourceType
    page: int | None = None
    bbox: dict | None = None
    text_span: dict | None = None


@dataclass(frozen=True)
class Finding:
    """An actionable QS finding (C1.6 invariant).

    A Finding is NOT the same as a rule execution outcome. Only FAIL
    outcomes MAY generate Findings per C1.7.
    """

    rule_id: str
    severity: Severity
    evidence: list[EvidenceReference] = field(default_factory=list)
    risk_statement: str = ""
    remediation: str = ""

    def __post_init__(self) -> None:
        if not self.evidence:
            raise ValueError("A Finding must reference at least one EvidenceReference.")
        if not self.risk_statement:
            raise ValueError("A Finding must include a risk statement.")
        if not self.remediation:
            raise ValueError("A Finding must include actionable remediation.")


# =============================================================================
# ADR-0031 — FindingReport Public Contract
# =============================================================================

@dataclass(frozen=True)
class ReportProvenance:
    """Provenance block embedded in every FindingReport (C1.14).

    Links the report to its exact execution context for full reproducibility.
    """

    execution_id: str
    evidence_fingerprint: str
    rule_snapshot_hash: str
    capability_version: str


@dataclass(frozen=True)
class TelemetrySummary:
    """Operational telemetry (C1.13 — internal, not public)."""

    rule_count_total: int = 0
    rule_count_executed: int = 0
    rule_count_unevaluable: int = 0
    execution_duration_ms: float = 0.0
    coverage_pct: float = 0.0


@dataclass(frozen=True)
class FindingReport:
    """Public capability output contract (C1.13, C1.15).

    A FindingReport is the complete, deterministic result of a single
    execution run. It is technology-agnostic and contains no internal
    execution telemetry beyond the provenance block.

    Reports SHALL NOT be incrementally composed or retroactively modified.
    """

    provenance: ReportProvenance
    telemetry_summary: TelemetrySummary
    findings: list[Finding] = field(default_factory=list)
    domain_coverage: dict[str, float] = field(default_factory=dict)


# =============================================================================
# ADR-0030 — Capability Host Interface
# =============================================================================

@runtime_checkable
class CapabilityHost(Protocol):
    """Interface contract for any capability panel hosted in the shell.

    Per ADR-0030, capabilities are mounted through this interface and SHALL
    NOT directly import or invoke other capabilities. The shell enforces
    this boundary.
    """

    @property
    def capability_id(self) -> str:
        """Unique identifier for this capability."""
        ...

    async def initialize(self) -> None:
        """Initialize the capability within its host context."""
        ...

    async def dispose(self) -> None:
        """Dispose of capability resources when unmounted."""
        ...


# =============================================================================
# ADR-0032 — Workspace Evidence Binding
# =============================================================================

class EvidenceGranularity(StrEnum):
    """Evidence granularity levels per ADR-0032 C1.4 hierarchy."""

    ATOMIC = "atomic"
    STRUCTURAL = "structural"
    AGGREGATE = "aggregate"
    DERIVED = "derived"

class EvidenceBindingFrozenError(Exception):
    """Raised when attempting to modify evidence after binding is frozen."""


@runtime_checkable
class EvidenceContext(Protocol):
    """Protocol-level evidence context per ADR-0032.

    Per C1.4/C1.12, evidence is frozen at binding and cannot be rewritten.
    """

    @property
    def is_bound(self) -> bool:
        """Whether the evidence context has been sealed (immutable)."""
        ...

    def bind(self, evidence_path: str) -> list[str]:
        """Bind evidence and freeze for the life of this context.

        Returns:
            List of evidence artifacts bound into the context.

        Raises:
            EvidenceBindingFrozenError: if evidence is already bound.
        """
        ...

@runtime_checkable
class EvidenceRepository(Protocol):
    """Capability-neutral query interface for evidence retrieval.

    Provides read-only access to persisted evidence records.
    Used by downstream CheckMate rules to resolve evidence dependencies.
    """

    def get(self, evidence_id: str) -> EvidenceReference | None:
        """Retrieve an evidence record by its unique identifier."""
        ...

    def list(self) -> list[EvidenceReference]:
        """List all evidence records currently stored."""
        ...

    def find_by_document(self, document_id: str) -> list[EvidenceReference]:
        """Find all evidence records belonging to a specific document."""
        ...

    def find_by_sheet(self, document_id: str, sheet: str) -> list[EvidenceReference]:
        """Find all evidence records for a specific sheet in a document."""
        ...

    def find_by_source_type(self, source_type: EvidenceSourceType) -> list[EvidenceReference]:
        """Find all evidence records of a specific source type."""
        ...

    def find_by_granularity(self, granularity: EvidenceGranularity) -> list[EvidenceReference]:
        """Find all evidence records at a specific granularity level."""
        ...
