"""Domain Rule Registry tests.

Verifies:
- Deterministic loading
- Unique Rule IDs
- Stable ordering
- Rule serialization
- Registry integrity
- Regression passes
"""

from __future__ import annotations

import json
import sys
from typing import Any

# Ensure src/ is on sys.path for imports (runs at module load)
if "src" not in sys.path:
    sys.path.insert(0, "src")

import pytest

from jarvis.domain.models import (
    DomainRule,
    RuleAuthority,
    RuleCategory,
    RuleSeverity,
    RuleStatus,
    RuleRegistry,
)
from jarvis.domain.registry import load_registry


# ============================================================
# Registry Loading
# ============================================================

class TestRegistryLoading:
    """Verify deterministic loading and singleton behavior."""

    def test_registry_loads_successfully(self) -> None:
        """Registry loads without errors."""
        registry = load_registry()
        assert registry is not None
        assert registry.count > 0

    def test_registry_is_singleton(self) -> None:
        """load_registry() returns the same instance on repeated calls."""
        registry1 = load_registry()
        registry2 = load_registry()
        assert registry1 is registry2

    def test_registry_has_rules(self) -> None:
        """Registry contains at least the required rules."""
        registry = load_registry()
        assert registry.count >= 22  # 18 engineering + 4 domain

    def test_engineering_rules_start_with_E_prefix(self) -> None:
        """All engineering rules use 'E-' prefix."""
        registry = load_registry()
        for rule in registry.by_authority(RuleAuthority.ENGINEERING):
            assert rule.rule_id.startswith("E-"), f"Rule {rule.rule_id} should start with 'E-'"

    def test_domain_rules_start_with_D_prefix(self) -> None:
        """All domain rules use 'D-' prefix."""
        registry = load_registry()
        for rule in registry.by_authority(RuleAuthority.DOMAIN):
            assert rule.rule_id.startswith("D-"), f"Rule {rule.rule_id} should start with 'D-'"


# ============================================================
# Unique Rule IDs
# ============================================================

class TestRuleIdUniqueness:
    """Verify all rule IDs are unique."""

    def test_all_rule_ids_are_unique(self) -> None:
        """No duplicate rule_id in the registry."""
        registry = load_registry()
        rule_ids = [r.rule_id for r in registry.rules]
        assert len(rule_ids) == len(set(rule_ids)), "Duplicate rule_ids found"

    def test_rule_ids_are_non_empty(self) -> None:
        """Every rule has a non-empty rule_id."""
        registry = load_registry()
        for rule in registry.rules:
            assert rule.rule_id, f"Rule has empty rule_id"


# ============================================================
# Stable Ordering
# ============================================================

class TestDeterministicOrdering:
    """Verify rules are sorted deterministically by rule_id."""

    def test_rules_are_sorted_by_id(self) -> None:
        """Rules appear in sorted order by rule_id."""
        registry = load_registry()
        rule_ids = list(r.rule_id for r in registry.rules)
        assert rule_ids == sorted(rule_ids), (
            f"Rules not sorted: got {rule_ids}, expected {sorted(rule_ids)}"
        )

    def test_order_is_stable_across_calls(self) -> None:
        """Multiple calls produce the same ordering."""
        registry = load_registry()
        order1 = list(r.rule_id for r in registry.rules)
        order2 = list(r.rule_id for r in load_registry().rules)
        assert order1 == order2

    def test_d_rules_come_before_e_rules(self) -> None:
        """Domain rules sort before engineering rules (D < E lexically)."""
        registry = load_registry()
        all_ids = list(r.rule_id for r in registry.rules)
        d_rules = [rid for rid in all_ids if rid.startswith("D-")]
        e_rules = [rid for rid in all_ids if rid.startswith("E-")]
        assert d_rules and e_rules
        assert all_ids.index(d_rules[-1]) < all_ids.index(e_rules[0])


# ============================================================
# Rule Validation
# ============================================================

class TestRuleValidation:
    """Verify every rule has required fields populated."""

    def test_all_rules_have_names(self) -> None:
        """Every rule has a non-empty name."""
        registry = load_registry()
        for rule in registry.rules:
            assert rule.name, f"Rule {rule.rule_id} has empty name"

    def test_all_rules_have_descriptions(self) -> None:
        """Every rule has a non-empty description."""
        registry = load_registry()
        for rule in registry.rules:
            assert rule.description, f"Rule {rule.rule_id} has empty description"

    def test_all_rules_have_authority(self) -> None:
        """Every rule has an authority classification."""
        registry = load_registry()
        for rule in registry.rules:
            assert rule.authority is not None, f"Rule {rule.rule_id} missing authority"

    def test_all_rules_have_category(self) -> None:
        """Every rule has a category."""
        registry = load_registry()
        for rule in registry.rules:
            assert rule.category is not None, f"Rule {rule.rule_id} missing category"

    def test_all_rules_have_severity(self) -> None:
        """Every rule has a severity."""
        registry = load_registry()
        for rule in registry.rules:
            assert rule.severity is not None, f"Rule {rule.rule_id} missing severity"

    def test_all_rules_have_status(self) -> None:
        """Every rule has a status."""
        registry = load_registry()
        for rule in registry.rules:
            assert rule.status is not None, f"Rule {rule.rule_id} missing status"

    def test_implemented_rules_have_eq_reference(self) -> None:
        """Implemented/verified engineering rules have EQ references."""
        registry = load_registry()
        for rule in registry.rules:
            if rule.authority == RuleAuthority.ENGINEERING and rule.status in (
                RuleStatus.IMPLEMENTED, RuleStatus.VERIFIED, RuleStatus.FROZEN
            ):
                assert rule.eq_reference, (
                    f"Engineering rule {rule.rule_id} with status {rule.status} "
                    f"missing EQ reference"
                )

    def test_engineered_rules_have_evidence_reference(self) -> None:
        """Implemented engineering rules have evidence references."""
        registry = load_registry()
        for rule in registry.rules:
            if rule.authority == RuleAuthority.ENGINEERING and rule.status in (
                RuleStatus.IMPLEMENTED, RuleStatus.VERIFIED, RuleStatus.FROZEN
            ):
                assert rule.evidence_reference, (
                    f"Engineering rule {rule.rule_id} missing evidence reference"
                )

    def test_implemented_rules_have_regression_test(self) -> None:
        """Implemented rules reference a regression test."""
        registry = load_registry()
        for rule in registry.rules:
            if rule.status in (RuleStatus.IMPLEMENTED, RuleStatus.VERIFIED, RuleStatus.FROZEN):
                assert rule.regression_test, (
                    f"Rule {rule.rule_id} with status {rule.status} "
                    f"missing regression_test reference"
                )

    def test_insufficient_evidence_rules_have_notes(self) -> None:
        """Rules with INSUFFICIENT_EVIDENCE have explanatory notes."""
        registry = load_registry()
        for rule in registry.rules:
            if rule.status == RuleStatus.INSUFFICIENT_EVIDENCE:
                assert rule.notes, (
                    f"Rule {rule.rule_id} has INSUFFICIENT_EVIDENCE but no notes"
                )


# ============================================================
# Rule Versioning
# ============================================================

class TestRuleVersioning:
    """Verify rule versioning consistency."""

    def test_implemented_rules_have_version_1_0_0(self) -> None:
        """Implemented rules start at 1.0.0."""
        registry = load_registry()
        for rule in registry.rules:
            if rule.status in (RuleStatus.IMPLEMENTED, RuleStatus.VERIFIED, RuleStatus.FROZEN):
                assert rule.rule_version == "1.0.0", (
                    f"Rule {rule.rule_id} with status {rule.status} "
                    f"has version {rule.rule_version}, expected 1.0.0"
                )

    def test_insufficient_evidence_rules_have_version_0_0_1(self) -> None:
        """Not-yet-implemented rules are at 0.0.1."""
        registry = load_registry()
        for rule in registry.rules:
            if rule.status == RuleStatus.INSUFFICIENT_EVIDENCE:
                assert rule.rule_version == "0.0.1", (
                    f"Rule {rule.rule_id} with status {rule.status} "
                    f"has version {rule.rule_version}, expected 0.0.1"
                )


# ============================================================
# Category Distribution
# ============================================================

class TestCategoryDistribution:
    """Verify each category has expected rules."""

    def test_evidence_integrity_category_exists(self) -> None:
        registry = load_registry()
        assert len(registry.by_category(RuleCategory.EVIDENCE_INTEGRITY)) >= 1

    def test_classification_category_exists(self) -> None:
        registry = load_registry()
        assert len(registry.by_category(RuleCategory.CLASSIFICATION)) >= 1

    def test_sign_convention_category_exists(self) -> None:
        registry = load_registry()
        assert len(registry.by_category(RuleCategory.SIGN_CONVENTION)) >= 1

    def test_structural_category_exists(self) -> None:
        registry = load_registry()
        assert len(registry.by_category(RuleCategory.STRUCTURAL)) >= 1

    def test_completeness_category_exists(self) -> None:
        registry = load_registry()
        assert len(registry.by_category(RuleCategory.COMPLETENESS)) >= 1

    def test_anomaly_detection_category_exists(self) -> None:
        registry = load_registry()
        assert len(registry.by_category(RuleCategory.ANOMALY_DETECTION)) >= 1

    def test_domain_quality_category_exists(self) -> None:
        registry = load_registry()
        assert len(registry.by_category(RuleCategory.DOMAIN_QUALITY)) >= 1

    def test_trade_category_exists(self) -> None:
        registry = load_registry()
        assert len(registry.by_category(RuleCategory.TRADE)) >= 1


# ============================================================
# Registry Search and Filter
# ============================================================

class TestRegistryQueries:
    """Verify registry query methods work correctly."""

    def test_get_returns_rule(self) -> None:
        registry = load_registry()
        rule = registry.get("E-001")
        assert rule is not None
        assert rule.rule_id == "E-001"

    def test_get_returns_none_for_unknown(self) -> None:
        registry = load_registry()
        rule = registry.get("Z-999")
        assert rule is None

    def test_by_authority_engineering(self) -> None:
        registry = load_registry()
        rules = registry.by_authority(RuleAuthority.ENGINEERING)
        assert len(rules) > 0
        for r in rules:
            assert r.authority == RuleAuthority.ENGINEERING

    def test_by_authority_domain(self) -> None:
        registry = load_registry()
        rules = registry.by_authority(RuleAuthority.DOMAIN)
        assert len(rules) > 0
        for r in rules:
            assert r.authority == RuleAuthority.DOMAIN

    def test_by_status_verified(self) -> None:
        registry = load_registry()
        rules = registry.by_status(RuleStatus.VERIFIED)
        assert len(rules) > 0
        for r in rules:
            assert r.status == RuleStatus.VERIFIED

    def test_by_status_approved(self) -> None:
        """by_status(APPROVED) returns only approved rules."""
        registry = load_registry()
        rules = registry.by_status(RuleStatus.APPROVED)
        # D-004 was changed from APPROVED to IMPLEMENTED in CB-0005
        # So there should be no APPROVED rules now
        assert len(rules) == 0
        for r in rules:
            assert r.status == RuleStatus.APPROVED


# ============================================================
# DomainRule Construction
# ============================================================

class TestDomainRuleConstruction:
    """Verify DomainRule creation invariants."""

    def test_rule_id_must_start_with_E_or_D(self) -> None:
        with pytest.raises(ValueError, match="rule_id must start with"):
            DomainRule(
                rule_id="X-001",
                name="Test Rule",
                description="A test rule.",
                authority=RuleAuthority.ENGINEERING,
                category=RuleCategory.EVIDENCE_INTEGRITY,
                severity=RuleSeverity.INFO,
                status=RuleStatus.CANDIDATE,
                eq_reference=None,
                evidence_reference=None,
                authority_reference=None,
            )

    def test_rule_id_must_not_be_empty(self) -> None:
        with pytest.raises(ValueError, match="rule_id must not be empty"):
            DomainRule(
                rule_id="",
                name="Test Rule",
                description="A test rule.",
                authority=RuleAuthority.ENGINEERING,
                category=RuleCategory.EVIDENCE_INTEGRITY,
                severity=RuleSeverity.INFO,
                status=RuleStatus.CANDIDATE,
                eq_reference=None,
                evidence_reference=None,
                authority_reference=None,
            )

    def test_rule_immutable(self) -> None:
        rule = DomainRule(
            rule_id="E-999",
            name="Test Immutability",
            description="A test rule.",
            authority=RuleAuthority.ENGINEERING,
            category=RuleCategory.EVIDENCE_INTEGRITY,
            severity=RuleSeverity.INFO,
            status=RuleStatus.CANDIDATE,
            eq_reference=None,
            evidence_reference=None,
            authority_reference=None,
        )
        with pytest.raises(AttributeError):
            rule.name = "Changed"

    def test_rule_string_representation(self) -> None:
        rule = DomainRule(
            rule_id="E-001",
            name="Test Rule",
            description="A test rule.",
            authority=RuleAuthority.ENGINEERING,
            category=RuleCategory.EVIDENCE_INTEGRITY,
            severity=RuleSeverity.INFO,
            status=RuleStatus.VERIFIED,
            eq_reference="EQ-0012",
            evidence_reference="Some spike",
            authority_reference="Some contract",
            inputs=("field_a",),
            consumers=("Validation Engine",),
        )
        assert "E-001" in repr(rule)
        assert "Test Rule" in repr(rule)
        assert "ENGINEERING" in repr(rule)

    def test_rule_ids_is_property(self) -> None:
        registry = load_registry()
        ids = registry.rule_ids
        assert isinstance(ids, tuple)
        assert len(ids) == registry.count
        assert list(ids) == sorted(ids)


# ============================================================
# Registry Integrity
# ============================================================

class TestRegistryIntegrity:
    """Verify registry invariants through RuleRegistry.__post_init__."""

    def test_empty_rules_raises_value_error(self) -> None:
        with pytest.raises(ValueError, match="must contain at least one rule"):
            RuleRegistry(rules=())

    def test_unsorted_rules_raises_value_error(self) -> None:
        rule_a = DomainRule(
            rule_id="E-005",
            name="Alpha",
            description="First rule.",
            authority=RuleAuthority.ENGINEERING,
            category=RuleCategory.EVIDENCE_INTEGRITY,
            severity=RuleSeverity.INFO,
            status=RuleStatus.CANDIDATE,
            eq_reference=None,
            evidence_reference=None,
            authority_reference=None,
        )
        rule_b = DomainRule(
            rule_id="E-003",
            name="Beta",
            description="Second rule.",
            authority=RuleAuthority.ENGINEERING,
            category=RuleCategory.EVIDENCE_INTEGRITY,
            severity=RuleSeverity.WARNING,
            status=RuleStatus.CANDIDATE,
            eq_reference=None,
            evidence_reference=None,
            authority_reference=None,
        )
        rule_c = DomainRule(
            rule_id="E-004",
            name="Gamma",
            description="Third rule.",
            authority=RuleAuthority.ENGINEERING,
            category=RuleCategory.EVIDENCE_INTEGRITY,
            severity=RuleSeverity.INFO,
            status=RuleStatus.CANDIDATE,
            eq_reference=None,
            evidence_reference=None,
            authority_reference=None,
        )
        with pytest.raises(ValueError, match="sorted by rule_id"):
            RuleRegistry(rules=(rule_a, rule_c, rule_b))

    def test_duplicate_rule_ids_raises_value_error(self) -> None:
        rule = DomainRule(
            rule_id="E-999",
            name="Duplicate",
            description="Duplicate rule.",
            authority=RuleAuthority.ENGINEERING,
            category=RuleCategory.EVIDENCE_INTEGRITY,
            severity=RuleSeverity.INFO,
            status=RuleStatus.CANDIDATE,
            eq_reference=None,
            evidence_reference=None,
            authority_reference=None,
        )
        with pytest.raises(ValueError, match="Duplicate rule_id"):
            RuleRegistry(rules=(rule, rule))


# ============================================================
# Rule-to-Validation Engine Mapping Integrity
# ============================================================

class TestRuleMappingIntegrity:
    """Verify that every implemented DomainRule maps to a Validation Engine rule."""

    def test_all_verified_rules_have_consumer(self) -> None:
        registry = load_registry()
        for rule in registry.by_status(RuleStatus.VERIFIED):
            assert len(rule.consumers) >= 1, (
                f"Rule {rule.rule_id} is VERIFIED but has no consumers"
            )

    def test_all_implemented_rules_have_inputs(self) -> None:
        """Every implemented/verified rule has at least one input field documented."""
        registry = load_registry()
        for rule in registry.rules:
            if rule.status in (RuleStatus.IMPLEMENTED, RuleStatus.VERIFIED, RuleStatus.FROZEN):
                assert len(rule.inputs) >= 1, (
                    f"Rule {rule.rule_id} with status {rule.status} has no inputs documented"
                )
