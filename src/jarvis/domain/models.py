"""Domain Rule data models.

Defines the deterministic production dataclasses for representing
all BOQ domain rules — both Engineering-derived and Domain-derived.

No inheritance hierarchy.
No runtime registration framework.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any


class RuleAuthority(Enum):
    """Source of authority for a rule.

    Engineering-Derived rules are traced to answered Engineering Questions
    or spike evidence. They are stable until new evidence contradicts them.

    Domain-Derived rules are sourced from office standards, professional
    conventions, or QS authority. They evolve when the office standard changes.
    """

    ENGINEERING = auto()
    """Rule derived from reverse-engineering CostX exports, fixture analysis,
    or structural properties of the data. Traced to an answered EQ."""

    DOMAIN = auto()
    """Rule derived from office standards, QS conventions, or other
    professional domain knowledge. Requires Project Owner or QS authority."""


class RuleCategory(Enum):
    """Functional category of a rule."""

    # Evidence Integrity — rules verifying evidence structure and availability
    EVIDENCE_INTEGRITY = auto()
    # Classification — rules verifying row/section classification
    CLASSIFICATION = auto()
    # Sign Convention — rules verifying quantity sign conventions
    SIGN_CONVENTION = auto()
    # Structural — rules verifying hierarchy and structural relationships
    STRUCTURAL = auto()
    # Completeness — rules verifying data completeness
    COMPLETENESS = auto()
    # Anomaly Detection — rules detecting known anomalous patterns
    ANOMALY_DETECTION = auto()
    # Domain Quality — rules from office standards (duplicates, missing data, etc.)
    DOMAIN_QUALITY = auto()
    # Trade Classification — rules classifying items by trade
    TRADE = auto()
    # Consumption — rules for downstream formatting/export
    CONSUMPTION = auto()


class RuleSeverity(Enum):
    """Severity of rule violation or observation."""

    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()


class RuleStatus(Enum):
    """Implementation status of a rule.

    Mirrors the Validation Engine lifecycle (EQ-0013 Spike 2).
    """

    CANDIDATE = auto()
    """Rule identified but not yet implemented."""
    APPROVED = auto()
    """Rule approved for implementation."""
    IMPLEMENTED = auto()
    """Rule is implemented in production code."""
    VERIFIED = auto()
    """Rule has been verified against production evidence."""
    FROZEN = auto()
    """Rule is frozen — stable and immutable for consumers."""
    DEPRECATED = auto()
    """Rule is deprecated — still functional but should not be relied upon."""
    RETIRED = auto()
    """Rule is removed from active use."""
    INSUFFICIENT_EVIDENCE = auto()
    """Rule cannot be implemented due to insufficient evidence."""
    BOUNDARY_VIOLATION = auto()
    """Rule violates the EQ-0011 Observe/Detect/Assess/Recommend boundary."""


@dataclass(frozen=True)
class DomainRule:
    """A single deterministic domain rule.

    Represents exactly one rule, classified by authority and category,
    with traceability to engineering evidence or domain standards.

    No inheritance. No runtime registration framework.
    Immutable dataclass with explicit fields.
    """

    # === Identity ===
    rule_id: str
    """Unique stable identifier for this rule (e.g. 'D-001', 'E-001')."""

    name: str
    """Human-readable rule name."""

    description: str
    """What this rule detects, validates, or observes."""

    # === Classification ===
    authority: RuleAuthority
    """Source of authority: ENGINEERING or DOMAIN."""

    category: RuleCategory
    """Functional category of the rule."""

    severity: RuleSeverity
    """Severity of a violation or observation."""

    status: RuleStatus
    """Implementation lifecycle status."""

    # === Traceability ===
    eq_reference: str | None
    """Engineering Question reference (e.g. 'EQ-0010', 'EQ-0011').
    None for domain rules not traced to an EQ."""

    evidence_reference: str | None
    """Specific evidence report or spike reference.
    None if the rule is domain-derived without a spike."""

    authority_reference: str | None
    """Document reference for the authority (office standard, contract, etc.).
    Examples: 'docs/domain/02_BOQ_Structure.md', 'docs/reference/office_standards/12_Units of Measurements.docx'."""

    # === Dependencies ===
    inputs: tuple[str, ...] = field(default_factory=tuple)
    """Evidence fields from BOQIntelligenceResult that this rule consumes.
    References fields from the Public Evidence Contract v1.0.0."""

    # === Consumer ===
    consumers: tuple[str, ...] = field(default_factory=tuple)
    """Downstream consumers that depend on this rule's output.
    Examples: 'Validation Engine', 'CheckMate', 'Formatter'."""

    # === Regression ===
    regression_test: str | None = None
    """Path to the regression test that exercises this rule.
    Example: 'tests/domain/test_registry.py'."""

    # === Documentation ===
    notes: str | None = None
    """Additional notes about the rule's behavior, limitations, or future work."""

    # === Version ===
    rule_version: str = "1.0.0"
    """Semver version for this rule. Independent of the evidence contract.
    Incremented when the rule's logic or behavior changes."""

    def __post_init__(self) -> None:
        """Validate rule invariants after construction."""
        if not self.rule_id:
            raise ValueError("rule_id must not be empty")
        if not self.name:
            raise ValueError("name must not be empty")
        if not self.description:
            raise ValueError("description must not be empty")

        # Validate rule_id format
        if not self.rule_id.startswith(("D-", "E-")):
            raise ValueError(
                f"rule_id must start with 'D-' (domain) or 'E-' (engineering): "
                f"got {self.rule_id!r}"
            )


@dataclass(frozen=True)
class RuleRegistry:
    """Immutable collection of DomainRules.

    Provides deterministic ordering and stable identifiers.
    No reflection. No plugins. No dynamic imports.
    """

    rules: tuple[DomainRule, ...]
    """All registered rules, sorted by rule_id for determinism."""

    def __post_init__(self) -> None:
        """Validate registry invariants."""
        if not self.rules:
            raise ValueError("Registry must contain at least one rule")

        # Verify deterministic ordering
        rule_ids = [r.rule_id for r in self.rules]
        if rule_ids != sorted(rule_ids):
            raise ValueError("Rules must be sorted by rule_id")

        # Verify unique IDs
        if len(rule_ids) != len(set(rule_ids)):
            raise ValueError("Duplicate rule_id detected in registry")

        # Verify no empty rule strings
        for rule in self.rules:
            if not rule.rule_id:
                raise ValueError(f"Rule with empty rule_id in registry")

    def get(self, rule_id: str) -> DomainRule | None:
        """Look up a rule by ID. O(n) — acceptable for small registries."""
        for rule in self.rules:
            if rule.rule_id == rule_id:
                return rule
        return None

    def by_category(self, category: RuleCategory) -> tuple[DomainRule, ...]:
        """Return rules of a specific category."""
        return tuple(r for r in self.rules if r.category == category)

    def by_authority(self, authority: RuleAuthority) -> tuple[DomainRule, ...]:
        """Return rules of a specific authority."""
        return tuple(r for r in self.rules if r.authority == authority)

    def by_status(self, status: RuleStatus) -> tuple[DomainRule, ...]:
        """Return rules of a specific status."""
        return tuple(r for r in self.rules if r.status == status)

    @property
    def rule_ids(self) -> tuple[str, ...]:
        """Return all rule IDs in deterministic order."""
        return tuple(r.rule_id for r in self.rules)

    @property
    def count(self) -> int:
        """Total number of rules in the registry."""
        return len(self.rules)