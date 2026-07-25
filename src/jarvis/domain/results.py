"""Domain Rule Execution Results data models.

Defines the immutable dataclasses for representing the output
of executed domain rules.

No inheritance hierarchy.
No runtime registration framework.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto
from typing import Any

from jarvis.domain.models import DomainRule, RuleSeverity

class DomainRuleFindingType(Enum):
    """Classification of a domain rule finding."""

    DUPLICATE_ITEM_CODE = auto()
    MISSING_DESCRIPTION = auto()
    MISSING_UOM = auto()
    TRADE_CLASSIFICATION = auto()
    # Add other domain-specific finding types here as rules are added

@dataclass(frozen=True)
class DomainRuleFinding:
    """A single deterministic finding from a domain rule execution.

    Represents an observed condition, violation, or insight.
    Immutable dataclass with explicit fields.
    """

    rule_id: str
    """The ID of the rule that produced this finding (e.g., D-001)."""

    finding_type: DomainRuleFindingType
    """The specific type of finding (e.g., DUPLICATE_ITEM_CODE)."""

    severity: RuleSeverity
    """Severity of the finding (INFO, WARNING, ERROR, CRITICAL)."""

    message: str
    """Human-readable explanation of the finding."""

    row_number: int | None = None
    """1-based row number in the original BOQ data where the finding occurred.
    None if the finding is aggregated or not tied to a specific row."""

    field_name: str | None = None
    """The specific field (e.g., 'item_code', 'description', 'uom') related to the finding.
    None if not applicable."""

    context: dict[str, Any] = field(default_factory=dict)
    """Additional context or data related to the finding (e.g., affected_codes, original_value)."""

    def __post_init__(self) -> None:
        """Validate finding invariants after construction."""
        if not self.rule_id:
            raise ValueError("rule_id must not be empty")
        if not self.message:
            raise ValueError("message must not be empty")

@dataclass(frozen=True)
class DomainRuleExecutionResult:
    """The complete result of executing a set of domain rules.

    Contains all findings and metadata about the execution.
    Immutable dataclass.
    """

    execution_timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    """UTC timestamp when the rules were executed."""

    executed_rules: tuple[DomainRule, ...] = field(default_factory=tuple)
    """The specific rules that were executed to produce this result, sorted by rule_id."""

    findings: tuple[DomainRuleFinding, ...] = field(default_factory=tuple)
    """All findings generated during execution, sorted for determinism."""

    metadata: dict[str, Any] = field(default_factory=dict)
    """Additional metadata about the execution (e.g., BOQ hash, parser version)."""

    def __post_init__(self) -> None:
        """Validate result invariants after construction."""
        # Ensure executed_rules are sorted by rule_id for determinism
        rule_ids = [r.rule_id for r in self.executed_rules]
        if rule_ids != sorted(rule_ids):
            raise ValueError("executed_rules must be sorted by rule_id")

        # Ensure findings are sorted for determinism (e.g., by rule_id, then row_number, then message)
        # This requires a custom sort key if findings are complex
        # For now, a simple sort based on rule_id and message is sufficient if row_number is optional
        if self.findings:
            sorted_findings = sorted(self.findings, key=lambda f: (f.rule_id, f.row_number or 0, f.message))
            if list(self.findings) != sorted_findings:
                raise ValueError("findings must be sorted for determinism")

    @property
    def info_count(self) -> int:
        """Number of INFO findings."""
        return sum(1 for f in self.findings if f.severity == RuleSeverity.INFO)

    @property
    def warning_count(self) -> int:
        """Number of WARNING findings."""
        return sum(1 for f in self.findings if f.severity == RuleSeverity.WARNING)

    @property
    def error_count(self) -> int:
        """Number of ERROR findings."""
        return sum(1 for f in self.findings if f.severity == RuleSeverity.ERROR)

    @property
    def critical_count(self) -> int:
        """Number of CRITICAL findings."""
        return sum(1 for f in self.findings if f.severity == RuleSeverity.CRITICAL)

    @property
    def total_findings(self) -> int:
        """Total number of findings."""
        return len(self.findings)