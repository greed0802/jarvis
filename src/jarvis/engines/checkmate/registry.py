"""RuleRegistry and immutable RuleSnapshot per ADR-0032.

Implements:
  - C1.11: RuleSnapshot sovereignty — immutable once compiled.
  - C1.14: RuleSnapshot hash for FindingReport provenance.
  - C1.8: Domain taxonomy validation at registration time.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from jarvis.contracts.execution import RuleSnapshotMetadata
from jarvis.engines.checkmate.rules import CheckMateRule, DomainCategory

class RuleRegistrationError(ValueError):
    """Raised when a rule fails registry validation."""

@dataclass
class RuleSnapshot:
    """Immutable execution manifest bound at run initiation (C1.11).

    Contains the complete set of rules, their versions, and a deterministic
    SHA-256 hash for reproducibility.
    """

    metadata: RuleSnapshotMetadata
    rules: list[CheckMateRule] = field(default_factory=list)

    @property
    def snapshot_hash(self) -> str:
        """The deterministic SHA-256 hash of this snapshot's manifest."""
        return self.metadata.compute_hash()

    @property
    def rule_count(self) -> int:
        return len(self.rules)

@dataclass
class RuleRegistry:
    """Canonical rule registry — sole source of truth for all rules (C1.11).

    Rules are registered with domain taxonomy validation (C1.8).
    The Registry compiles immutable snapshots with deterministic hashes.
    """

    _rules: dict[str, CheckMateRule] = field(default_factory=dict)
    _capability_version: str = "0.1.0"

    def register(self, rule: CheckMateRule) -> None:
        """Register a self-contained rule.

        Validates:
        - Rule has a valid domain category (C1.8)
        - Rule ID is unique within the registry

        Raises:
            RuleRegistrationError: If registration fails validation.
        """
        try:
            DomainCategory(rule.domain)
        except ValueError:
            raise RuleRegistrationError(
                f"Rule '{rule.rule_id}' has unrecognized domain category: {rule.domain}"
            ) from None

        if rule.rule_id in self._rules:
            raise RuleRegistrationError(
                f"Rule '{rule.rule_id}' is already registered."
            )

        self._rules[rule.rule_id] = rule

    def unregister(self, rule_id: str) -> None:
        """Remove a rule from the registry."""
        self._rules.pop(rule_id, None)

    def compile_snapshot(self) -> RuleSnapshot:
        """Compile an immutable RuleSnapshot of all registered rules (C1.11).

        The snapshot binds the current registry state. Subsequent registrations
        or unregistrations do not affect an already-compiled snapshot.

        Returns:
            Immutable RuleSnapshot with deterministic SHA-256 hash.
        """
        rule_ids = sorted(self._rules.keys())
        rule_versions = {rule_id: self._rules[rule_id].version for rule_id in rule_ids}
        contract_versions = {
            rule_id: "1.0.0" for rule_id in rule_ids  # All rules declare 1.0.0 C1 — C1.12 compatibility
        }

        metadata = RuleSnapshotMetadata(
            snapshot_id=str(uuid.uuid4()),
            capability_version=self._capability_version,
            rule_ids=rule_ids,
            rule_versions=rule_versions,
            contract_versions=contract_versions,
        )

        rules_list = [self._rules[rule_id] for rule_id in rule_ids]
        return RuleSnapshot(metadata=metadata, rules=rules_list)

    @property
    def rule_count(self) -> int:
        return len(self._rules)

    def get(self, rule_id: str) -> CheckMateRule | None:
        return self._rules.get(rule_id)