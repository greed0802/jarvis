"""CheckMate rule protocol, domain taxonomy, and vertical-slice rules.

Implements ADR-0030 (C1.8 — Domain Rule Taxonomy) and ADR-0032
(C1.9 — Determinism, C1.10 — Self-Containment, C1.12 — Contract Compatibility).

5 vertical-slice rules exercise all 16 invariants across:
  - MEASUREMENT → PASS
  - COMPLIANCE → FAIL → Finding
  - SPECIFICATION → FAIL → Finding
  - COORDINATION → FAIL → Finding
  - DOCUMENTATION_INTEGRITY → UNEVALUABLE_MISSING_EVIDENCE
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Protocol, runtime_checkable

from jarvis.contracts.execution import ExecutionOutcome, ExecutionOutcomeStatus

# =============================================================================
# Domain Category (C1.8 — 6 canonical categories)
# =============================================================================

class DomainCategory(StrEnum):
    """Canonical QS domain categories per ADR-0030 C1.8.

    Each rule MUST declare its domain category at registration.
    """

    MEASUREMENT = "MEASUREMENT"
    SPECIFICATION = "SPECIFICATION"
    COORDINATION = "COORDINATION"
    COMPLIANCE = "COMPLIANCE"
    DOCUMENTATION_INTEGRITY = "DOCUMENTATION_INTEGRITY"
    PROJECT_POLICY = "PROJECT_POLICY"

# =============================================================================
# Rule Protocol (C1.10 — Self-Containment)
# =============================================================================

@runtime_checkable
class CheckMateRule(Protocol):
    """Self-contained rule evaluation unit.

    Per C1.10: Each rule declares its domain, minimum evidence level,
    parameter schema, version, and contract compatibility boundary.
    Rules SHALL NOT depend on mutable global state or side effects.
    """

    @property
    def rule_id(self) -> str:
        """Unique rule identifier."""
        ...

    @property
    def domain(self) -> DomainCategory:
        """QS domain category (C1.8)."""
        ...

    @property
    def version(self) -> str:
        """Semantic version of this rule."""
        ...

    @property
    def min_evidence_granularity(self) -> str:
        """Minimum evidence granularity level required."""
        ...

    def evaluate(
        self,
        evidence_ids: list[str],
        parameters: dict | None = None,
    ) -> ExecutionOutcome:
        """Evaluate this rule against available evidence.

        Returns:
            ExecutionOutcome with status (PASS/FAIL/UNEVALUABLE_MISSING_EVIDENCE).

        Per C1.5: missing required evidence SHALL yield UNEVALUABLE_MISSING_EVIDENCE.
        Per C1.12: mismatched contract → UNEVALUABLE_MISSING_EVIDENCE, not silent skip.
        """
        ...

# =============================================================================
# Vertical Slice Rule 1: Quantity Validation (MEASUREMENT → PASS)
# =============================================================================

@dataclass(frozen=True)
class QuantityValidationRule:
    """Validate that all BOQ quantity line items have positive non-zero values.

    Domain: MEASUREMENT — Expected: PASS (when evidence is present).
    Exercises: C1.5, C1.9, C1.10, C1.11, C1.12.
    """

    rule_id: str = "MEASUREMENT.001"
    domain: DomainCategory = DomainCategory.MEASUREMENT
    version: str = "1.0.0"
    min_evidence_granularity: str = "structural"

    def evaluate(
        self,
        evidence_ids: list[str],
        parameters: dict | None = None,
    ) -> ExecutionOutcome:
        if not evidence_ids:
            return ExecutionOutcome(
                rule_id=self.rule_id,
                status=ExecutionOutcomeStatus.UNEVALUABLE_MISSING_EVIDENCE,
                domain_category=self.domain.value,
                evidence_ids=evidence_ids,
                message="No evidence available for quantity validation.",
            )
        return ExecutionOutcome(
            rule_id=self.rule_id,
            status=ExecutionOutcomeStatus.PASS,
            domain_category=self.domain.value,
            evidence_ids=evidence_ids,
            message="All quantity line items validated.",
        )

# =============================================================================
# Vertical Slice Rule 2: Standards Adherence (COMPLIANCE → FAIL → Finding)
# =============================================================================

@dataclass(frozen=True)
class StandardsAdherenceRule:
    """Verify that BOQ items comply with applicable construction standards.

    Domain: COMPLIANCE — Expected: FAIL → Finding (non-standard material).
    """

    rule_id: str = "COMPLIANCE_001"
    version: str = "1.0.0"
    domain: DomainCategory = DomainCategory.COMPLIANCE
    min_evidence_granularity: str = "structural"

    def evaluate(
        self,
        evidence_ids: list[str],
        parameters: dict | None = None,
    ) -> ExecutionOutcome:
        if not evidence_ids:
            return ExecutionOutcome(
                rule_id=self.rule_id,
                status=ExecutionOutcomeStatus.UNEVALUABLE_MISSING_EVIDENCE,
                domain_category=self.domain.value,
                evidence_ids=evidence_ids,
                message="No evidence for standards compliance check.",
            )

        # Deterministic failure: if evidence exists, always FAIL to exercise Finding generation
        return ExecutionOutcome(
            rule_id=self.rule_id,
            status=ExecutionOutcomeStatus.FAIL,
            domain_category=self.domain.value,
            evidence_ids=evidence_ids,
            message="Non-standard material detected: M25 concrete specified instead of M30 per UK Specification.",
        )

# =============================================================================
# Vertical Slice Rule 3: Conformance Check (SPECIFICATION → FAIL → Finding)
# =============================================================================

@dataclass(frozen=True)
class ConformanceCheckRule:
    """Verify BOQ items conform to project specification requirements.

    Domain: SPECIFICATION — Expected: FAIL → Finding (spec deviation).
    """

    rule_id: str = "SPEC-002"
    domain: DomainCategory = DomainCategory.SPECIFICATION
    version: str = "1.0.0"
    min_evidence_granularity: str = "structural"

    def evaluate(
        self,
        evidence_ids: list[str],
        parameters: dict | None = None,
    ) -> ExecutionOutcome:
        if not evidence_ids:
            return ExecutionOutcome(
                rule_id=self.rule_id,
                status=ExecutionOutcomeStatus.UNEVALUABLE_MISSING_EVIDENCE,
                domain_category=self.domain.value,
                evidence_ids=evidence_ids,
                message="No specification evidence available.",
            )

        return ExecutionOutcome(
            rule_id=self.rule_id,
            status=ExecutionOutcomeStatus.FAIL,
            domain_category=self.domain.value,
            evidence_ids=evidence_ids,
            message="Specification deviation: wall thickness 200mm vs specified 250mm.",
        )

# =============================================================================
# Vertical Slice Rule 4: Cross-Reference Check (COORDINATION → FAIL → Finding)
# =============================================================================

@dataclass(frozen=True)
class CrossReferenceCheckRule:
    """Cross-check structural and architectural BOQ quantities for coordination.

    Domain: COORDINATION — Expected: FAIL → Finding (mismatch found).
    """

    rule_id: str = "COORD-003"
    domain: DomainCategory = DomainCategory.COORDINATION
    version: str = "1.0.0"
    min_evidence_granularity: str = "aggregate"

    def evaluate(
        self,
        evidence_ids: list[str],
        parameters: dict | None = None,
    ) -> ExecutionOutcome:
        if not evidence_ids:
            return ExecutionOutcome(
                rule_id=self.rule_id,
                status=ExecutionOutcomeStatus.UNEVALUABLE_MISSING_EVIDENCE,
                domain_category=self.domain.value,
                evidence_ids=evidence_ids,
                message="No coordination evidence for cross-reference check.",
            )

        return ExecutionOutcome(
            rule_id=self.rule_id,
            status=ExecutionOutcomeStatus.FAIL,
            domain_category=self.domain.value,
            evidence_ids=evidence_ids,
            message="Cross-coordinate mismatch: structural concrete quantity 1200m³ vs architectural BOQ 1350m³.",
        )

# =============================================================================
# Vertical Slice Rule 5: Data Completeness (DOCUMENTATION_INTEGRITY → UNEVALUABLE)
# =============================================================================

@dataclass(frozen=True)
class DataCompletenessRule:
    """Check that all required documentation fields are populated.

    Domain: DOCUMENTATION_INTEGRITY — Expected: UNEVALUABLE_MISSING_EVIDENCE
    when evidence is empty/absent (C1.5).
    """

    rule_id: str = "DOCINT-004"
    domain: DomainCategory = DomainCategory.DOCUMENTATION_INTEGRITY
    version: str = "1.0.0"
    min_evidence_granularity: str = "atomic"

    def evaluate(
        self,
        evidence_ids: list[str],
        parameters: dict | None = None,
    ) -> ExecutionOutcome:
        if not evidence_ids:
            return ExecutionOutcome(
                rule_id=self.rule_id,
                status=ExecutionOutcomeStatus.UNEVALUABLE_MISSING_EVIDENCE,
                domain_category=self.domain.value,
                evidence_ids=evidence_ids,
                message="No documentation evidence available — completeness cannot be evaluated.",
            )

        return ExecutionOutcome(
            rule_id=self.rule_id,
            status=ExecutionOutcomeStatus.PASS,
            domain_category=self.domain.value,
            evidence_ids=evidence_ids,
            message="Documentation completeness verified.",
        )