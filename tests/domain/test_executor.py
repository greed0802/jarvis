"""Domain Rule Executor tests.

Verifies deterministic execution of D-001, D-002, D-003.

Covers:
- Valid cases (no findings)
- Invalid cases (findings detected)
- Policy exceptions (OMISSION/ADDITION, zero-quantity)
- Edge cases (whitespace, case-sensitivity, None values)
- Deterministic ordering
- Immutability of outputs
"""

from __future__ import annotations

import sys
sys.path.insert(0, "src")

from dataclasses import dataclass
import pytest

from jarvis.domain.executor import (
    BOQRow,
    _detect_duplicate_item_codes,
    _detect_missing_descriptions,
    _detect_missing_uoms,
    _classify_trades,
    execute_domain_rules,
)
from jarvis.domain.models import (
    DomainRule,
    RuleAuthority,
    RuleCategory,
    RuleSeverity,
    RuleStatus,
)
from jarvis.domain.registry import load_registry
from jarvis.domain.results import (
    DomainRuleExecutionResult,
    DomainRuleFinding,
    DomainRuleFindingType,
)
from jarvis.domain.executor import classify_trade


# ─── Fixtures ────────────────────────────────────────────────────────────────

@pytest.fixture
def registry() -> object:
    return load_registry()


@pytest.fixture
def d001_rule() -> DomainRule:
    registry = load_registry()
    rule = registry.get("D-001")
    assert rule is not None
    return rule


@pytest.fixture
def d002_rule() -> DomainRule:
    registry = load_registry()
    rule = registry.get("D-002")
    assert rule is not None
    return rule


@pytest.fixture
def d003_rule() -> DomainRule:
    registry = load_registry()
    rule = registry.get("D-003")
    assert rule is not None
    return rule


# ─── Helpers ─────────────────────────────────────────────────────────────────

def make_row(
    row_number: int,
    row_type: str = "Item",
    item_code: str | None = None,
    description: str | None = None,
    quantity: float | None = None,
    uom: str | None = None,
    section: str | None = None,
) -> BOQRow:
    return BOQRow(
        row_number=row_number,
        row_type=row_type,
        item_code=item_code,
        description=description,
        quantity=quantity,
        uom=uom,
        section=section,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# D-001: Duplicate Item Code Detection
# ═══════════════════════════════════════════════════════════════════════════════

class TestDuplicateItemCodeDetection:
    """D-001 rule execution tests."""

    def test_no_duplicates(self, d001_rule: DomainRule) -> None:
        rows = [
            make_row(1, item_code="A-001"),
            make_row(2, item_code="A-002"),
            make_row(3, item_code="A-003"),
        ]
        findings = _detect_duplicate_item_codes(rows, d001_rule)
        assert len(findings) == 0

    def test_simple_duplicate_detected(self, d001_rule: DomainRule) -> None:
        rows = [
            make_row(1, item_code="CONC-001", quantity=150.0),
            make_row(2, item_code="CONC-001", quantity=150.0),
        ]
        findings = _detect_duplicate_item_codes(rows, d001_rule)
        assert len(findings) == 2
        for f in findings:
            assert f.rule_id == "D-001"
            assert f.finding_type == DomainRuleFindingType.DUPLICATE_ITEM_CODE
            assert f.severity == RuleSeverity.WARNING
        # Both findings reference the same duplicated code
        assert findings[0].context["duplicate_code"] == "CONC-001"
        assert findings[1].context["duplicate_code"] == "CONC-001"

    def test_case_sensitive_comparison(self, d001_rule: DomainRule) -> None:
        """Different case is NOT a duplicate."""
        rows = [
            make_row(1, item_code="A-001"),
            make_row(2, item_code="a-001"),
        ]
        findings = _detect_duplicate_item_codes(rows, d001_rule)
        assert len(findings) == 0

    def test_whitespace_stripping(self, d001_rule: DomainRule) -> None:
        """Trailing whitespace is stripped before comparison."""
        rows = [
            make_row(1, item_code="A-001"),
            make_row(2, item_code="A-001 "),
        ]
        findings = _detect_duplicate_item_codes(rows, d001_rule)
        assert len(findings) == 2

    def test_none_code_not_duplicate(self, d001_rule: DomainRule) -> None:
        rows = [
            make_row(1, item_code=None),
            make_row(2, item_code=None),
        ]
        findings = _detect_duplicate_item_codes(rows, d001_rule)
        assert len(findings) == 0

    def test_omission_addition_exception(self, d001_rule: DomainRule) -> None:
        """Same code in OMISSION and ADDITION with opposite sign quantities is NOT a duplicate."""
        rows = [
            make_row(1, item_code="CONC-001", section="OMISSION", quantity=-150.0, description="RC Column 400x400"),
            make_row(2, item_code="CONC-001", section="ADDITION", quantity=150.0, description="RC Column 400x400"),
        ]
        findings = _detect_duplicate_item_codes(rows, d001_rule)
        assert len(findings) == 0

    def test_omission_addition_not_matching_descriptions(self, d001_rule: DomainRule) -> None:
        """OMISSION/ADDITION with different descriptions IS a duplicate."""
        rows = [
            make_row(1, item_code="CONC-001", section="OMISSION", quantity=-150.0, description="RC Column 400x400"),
            make_row(2, item_code="CONC-001", section="ADDITION", quantity=150.0, description="RC Beam 300x600"),
        ]
        findings = _detect_duplicate_item_codes(rows, d001_rule)
        assert len(findings) == 2  # Not an exception, flagged as duplicate

    def test_omission_addition_case_insensitive_description(self, d001_rule: DomainRule) -> None:
        """OMISSION/ADDITION descriptions match case-insensitively."""
        rows = [
            make_row(1, item_code="CONC-001", section="OMISSION", quantity=-150.0, description="Rc Column 400x400"),
            make_row(2, item_code="CONC-001", section="ADDITION", quantity=150.0, description="RC COLUMN 400X400"),
        ]
        findings = _detect_duplicate_item_codes(rows, d001_rule)
        assert len(findings) == 0  # Descriptions match case-insensitively

    def test_non_item_rows_excluded(self, d001_rule: DomainRule) -> None:
        """Only Item-type rows are checked for duplicates."""
        rows = [
            make_row(1, row_type="Head", item_code="H-001"),
            make_row(2, row_type="Head", item_code="H-001"),
            make_row(3, row_type="Item", item_code="I-001"),
            make_row(4, row_type="Item", item_code="I-001"),
        ]
        findings = _detect_duplicate_item_codes(rows, d001_rule)
        # Only the Item rows should be flagged
        assert len(findings) == 2
        for f in findings:
            assert f.row_number in (3, 4)


# ═══════════════════════════════════════════════════════════════════════════════
# D-002: Missing Description Detection
# ═══════════════════════════════════════════════════════════════════════════════

class TestMissingDescriptionDetection:
    """D-002 rule execution tests."""

    def test_all_descriptions_present(self, d002_rule: DomainRule) -> None:
        rows = [
            make_row(1, description="RC Column 400x400", quantity=150.0),
            make_row(2, description="Steel Beam", quantity=200.0),
        ]
        findings = _detect_missing_descriptions(rows, d002_rule)
        assert len(findings) == 0

    def test_item_missing_description(self, d002_rule: DomainRule) -> None:
        rows = [
            make_row(1, item_code="CONC-001", description=None, quantity=150.0),
        ]
        findings = _detect_missing_descriptions(rows, d002_rule)
        assert len(findings) == 1
        f = findings[0]
        assert f.rule_id == "D-002"
        assert f.finding_type == DomainRuleFindingType.MISSING_DESCRIPTION
        assert f.severity == RuleSeverity.WARNING
        assert f.row_number == 1

    def test_item_empty_string_description(self, d002_rule: DomainRule) -> None:
        rows = [
            make_row(1, description="", quantity=150.0),
        ]
        findings = _detect_missing_descriptions(rows, d002_rule)
        assert len(findings) == 1

    def test_item_whitespace_only_description(self, d002_rule: DomainRule) -> None:
        rows = [
            make_row(1, description="   ", quantity=150.0),
        ]
        findings = _detect_missing_descriptions(rows, d002_rule)
        assert len(findings) == 1

    def test_header_missing_description(self, d002_rule: DomainRule) -> None:
        rows = [
            make_row(1, row_type="Head", description=None),
        ]
        findings = _detect_missing_descriptions(rows, d002_rule)
        assert len(findings) == 1
        f = findings[0]
        assert f.severity == RuleSeverity.INFO  # Headers are INFO, not WARNING
        assert f.finding_type == DomainRuleFindingType.MISSING_DESCRIPTION

    def test_note_exempt_from_missing_description(self, d002_rule: DomainRule) -> None:
        rows = [
            make_row(1, row_type="Note", description=None),
        ]
        findings = _detect_missing_descriptions(rows, d002_rule)
        assert len(findings) == 0

    def test_section_exempt(self, d002_rule: DomainRule) -> None:
        rows = [
            make_row(1, row_type="Section", description=None),
        ]
        findings = _detect_missing_descriptions(rows, d002_rule)
        assert len(findings) == 0

    def test_other_exempt(self, d002_rule: DomainRule) -> None:
        rows = [
            make_row(1, row_type="Other", description=None),
        ]
        findings = _detect_missing_descriptions(rows, d002_rule)
        assert len(findings) == 0

    def test_zero_quantity_provisional_sum_info(self, d002_rule: DomainRule) -> None:
        """Zero-quantity items are flagged as INFO, not WARNING."""
        rows = [
            make_row(1, description=None, quantity=0.0),
        ]
        findings = _detect_missing_descriptions(rows, d002_rule)
        assert len(findings) == 1
        f = findings[0]
        assert f.severity == RuleSeverity.INFO


# ═══════════════════════════════════════════════════════════════════════════════
# D-003: Missing UOM Detection
# ═══════════════════════════════════════════════════════════════════════════════

class TestMissingUOMDetection:
    """D-003 rule execution tests."""

    def test_all_uoms_present(self, d003_rule: DomainRule) -> None:
        rows = [
            make_row(1, uom="m3", quantity=150.0),
            make_row(2, uom="m2", quantity=200.0),
        ]
        findings = _detect_missing_uoms(rows, d003_rule)
        assert len(findings) == 0

    def test_item_missing_uom(self, d003_rule: DomainRule) -> None:
        rows = [
            make_row(1, item_code="CONC-001", uom=None, quantity=150.0),
        ]
        findings = _detect_missing_uoms(rows, d003_rule)
        assert len(findings) == 1
        f = findings[0]
        assert f.rule_id == "D-003"
        assert f.finding_type == DomainRuleFindingType.MISSING_UOM
        assert f.severity == RuleSeverity.WARNING
        assert f.row_number == 1

    def test_item_empty_string_uom(self, d003_rule: DomainRule) -> None:
        rows = [
            make_row(1, uom="", quantity=150.0),
        ]
        findings = _detect_missing_uoms(rows, d003_rule)
        assert len(findings) == 1

    def test_item_whitespace_only_uom(self, d003_rule: DomainRule) -> None:
        rows = [
            make_row(1, uom="   ", quantity=150.0),
        ]
        findings = _detect_missing_uoms(rows, d003_rule)
        assert len(findings) == 1

    def test_zero_quantity_provisional_sum_info(self, d003_rule: DomainRule) -> None:
        """Zero-quantity items with missing UOM are flagged as INFO."""
        rows = [
            make_row(1, uom=None, quantity=0.0),
        ]
        findings = _detect_missing_uoms(rows, d003_rule)
        assert len(findings) == 1
        f = findings[0]
        assert f.severity == RuleSeverity.INFO

    def test_head_exempt(self, d003_rule: DomainRule) -> None:
        rows = [
            make_row(1, row_type="Head", uom="Head1", quantity=None),
        ]
        findings = _detect_missing_uoms(rows, d003_rule)
        assert len(findings) == 0

    def test_note_exempt(self, d003_rule: DomainRule) -> None:
        rows = [
            make_row(1, row_type="Note", uom=None, quantity=None),
        ]
        findings = _detect_missing_uoms(rows, d003_rule)
        assert len(findings) == 0

    def test_section_exempt(self, d003_rule: DomainRule) -> None:
        rows = [
            make_row(1, row_type="Section", uom=None, quantity=None),
        ]
        findings = _detect_missing_uoms(rows, d003_rule)
        assert len(findings) == 0

    def test_other_exempt(self, d003_rule: DomainRule) -> None:
        rows = [
            make_row(1, row_type="Other", uom=None, quantity=None),
        ]
        findings = _detect_missing_uoms(rows, d003_rule)
        assert len(findings) == 0


# ═══════════════════════════════════════════════════════════════════════════════
# Integration: execute_domain_rules
# ═══════════════════════════════════════════════════════════════════════════════

class TestExecuteDomainRules:
    """Integration tests for execute_domain_rules."""

    def test_execute_all_approved_rules(self, registry: object) -> None:
        rows = [
            make_row(1, item_code="CONC-001", description="RC Column", quantity=150.0, uom="m3"),
            make_row(2, item_code="CONC-001", description="RC Column", quantity=150.0, uom="m3"),  # duplicate
            make_row(3, item_code="A-002", description=None, quantity=200.0, uom="m2"),  # missing description
            make_row(4, item_code="A-003", description="Steel Beam", quantity=300.0, uom=None),  # missing UOM
        ]
        result = execute_domain_rules(rows)
        assert isinstance(result, DomainRuleExecutionResult)
        assert len(result.executed_rules) == 4  # D-001, D-002, D-003, D-004
        assert result.error_count == 0
        assert result.critical_count == 0
        assert result.total_findings > 0
        # D-001: 2 findings (duplicate), D-002: 1 finding, D-003: 1 finding, D-004: 4 findings (trade classification)
        assert result.total_findings == 8

    def test_no_findings(self) -> None:
        rows = [
            make_row(1, item_code="A-001", description="Item A", quantity=150.0, uom="m3"),
            make_row(2, item_code="A-002", description="Item B", quantity=200.0, uom="m2"),
        ]
        result = execute_domain_rules(rows)
        # D-004 will generate trade classification findings for all items
        d004_findings = [f for f in result.findings if f.rule_id == "D-004"]
        assert len(d004_findings) == 2  # Trade classifications
        # No other findings (D-001, D-002, D-003)
        other_findings = [f for f in result.findings if f.rule_id != "D-004"]
        assert len(other_findings) == 0

    def test_specific_rules_only(self) -> None:
        registry = load_registry()
        d001 = registry.get("D-001")
        assert d001 is not None
        rows = [
            make_row(1, item_code="A-001", description="Item A", quantity=100.0, uom="m3"),
            make_row(2, item_code="A-001", description="Item A", quantity=100.0, uom="m3"),
        ]
        result = execute_domain_rules(rows, rules_to_execute=[d001])
        assert len(result.executed_rules) == 1
        assert result.executed_rules[0].rule_id == "D-001"
        assert result.total_findings == 2  # Duplicate

    def test_deterministic_ordering(self) -> None:
        """Multiple calls with same data produce identical results."""
        rows = [
            make_row(1, item_code="A-001", description="Item A", quantity=100.0, uom="m3"),
            make_row(2, item_code="A-001", description="Item A", quantity=100.0, uom="m3"),
        ]
        result1 = execute_domain_rules(rows)
        result2 = execute_domain_rules(rows)
        assert result1.executed_rules == result2.executed_rules
        assert result1.findings == result2.findings

    def test_immutability_of_findings(self) -> None:
        """Findings tuple should be immutable."""
        rows = []
        result = execute_domain_rules(rows)
        # Frozen dataclass + tuple — any mutation attempt should raise
        with pytest.raises(Exception):
            result.findings.append(None)
        with pytest.raises(Exception):
            result.executed_rules.append(None)

    def test_metadata_included(self) -> None:
        rows = []
        metadata = {"parser_version": "1.0.0", "source": "test"}
        result = execute_domain_rules(rows, metadata=metadata)
        assert result.metadata["parser_version"] == "1.0.0"
        assert result.metadata["source"] == "test"

    def test_execute_no_rules(self) -> None:
        """Passing an empty rules list executes nothing."""
        rows = [
            make_row(1, item_code="A-001"),
        ]
        result = execute_domain_rules(rows, rules_to_execute=[])
        assert len(result.executed_rules) == 0
        assert result.total_findings == 0


# ═══════════════════════════════════════════════════════════════════════════════
# DomainRuleFinding Construction
# ═══════════════════════════════════════════════════════════════════════════════

class TestDomainRuleFindingConstruction:
    """Verify DomainRuleFinding immutability and invariants."""

    def test_finding_immutable(self) -> None:
        finding = DomainRuleFinding(
            rule_id="D-001",
            finding_type=DomainRuleFindingType.DUPLICATE_ITEM_CODE,
            severity=RuleSeverity.WARNING,
            message="Test finding",
        )
        with pytest.raises(AttributeError):
            finding.message = "Changed"  # type: ignore[misc]

    def test_finding_empty_rule_id_raises(self) -> None:
        with pytest.raises(ValueError):
            DomainRuleFinding(
                rule_id="",
                finding_type=DomainRuleFindingType.DUPLICATE_ITEM_CODE,
                severity=RuleSeverity.WARNING,
                message="Test",
            )

    def test_finding_empty_message_raises(self) -> None:
        with pytest.raises(ValueError):
            DomainRuleFinding(
                rule_id="D-001",
                finding_type=DomainRuleFindingType.DUPLICATE_ITEM_CODE,
                severity=RuleSeverity.WARNING,
                message="",
            )


# ═══════════════════════════════════════════════════════════════════════════════
# DomainRuleExecutionResult Construction
# ═══════════════════════════════════════════════════════════════════════════════

class TestDomainRuleExecutionResultConstruction:
    """Verify DomainRuleExecutionResult immutability and invariants."""

    def test_result_immutable(self) -> None:
        result = DomainRuleExecutionResult(executed_rules=(), findings=())
        with pytest.raises(AttributeError):
            result.metadata = {"new": "data"}  # type: ignore[misc]

    def test_unsorted_rules_raises(self) -> None:
        registry = load_registry()
        d003 = registry.get("D-003")
        d001 = registry.get("D-001")
        d002 = registry.get("D-002")
        with pytest.raises(ValueError, match="sorted by rule_id"):
            DomainRuleExecutionResult(
                executed_rules=(d003, d001, d002),  # type: ignore[arg-type]
                findings=(),
            )

    def test_unsorted_findings_raises(self) -> None:
        finding_a = DomainRuleFinding(
            rule_id="D-001", finding_type=DomainRuleFindingType.DUPLICATE_ITEM_CODE,
            severity=RuleSeverity.WARNING, message="Z", row_number=10,
        )
        finding_b = DomainRuleFinding(
            rule_id="D-001", finding_type=DomainRuleFindingType.DUPLICATE_ITEM_CODE,
            severity=RuleSeverity.WARNING, message="A", row_number=5,
        )
        # D-001, row=10, msg="Z" vs D-001, row=5, msg="A"
        # Sorted should be: D-001, row=5, msg="A" first, then D-001, row=10, msg="Z"
        with pytest.raises(ValueError, match="findings must be sorted"):
            DomainRuleExecutionResult(
                executed_rules=(), findings=(finding_a, finding_b),
            )

    def test_property_counts(self) -> None:
        findings = (
            DomainRuleFinding(rule_id="D-001",
                              finding_type=DomainRuleFindingType.DUPLICATE_ITEM_CODE,
                              severity=RuleSeverity.WARNING, message="w1"),
            DomainRuleFinding(rule_id="D-002",
                              finding_type=DomainRuleFindingType.MISSING_DESCRIPTION,
                              severity=RuleSeverity.INFO, message="i1"),
            DomainRuleFinding(rule_id="D-003",
                              finding_type=DomainRuleFindingType.MISSING_UOM,
                              severity=RuleSeverity.WARNING, message="w2"),
        )
        result = DomainRuleExecutionResult(executed_rules=(), findings=findings)
        assert result.info_count == 1
        assert result.warning_count == 2
        assert result.error_count == 0
        assert result.critical_count == 0
        assert result.total_findings == 3

# ═══════════════════════════════════════════════════════════════════════════════
# D-004: Trade Classification
# ═══════════════════════════════════════════════════════════════════════════════

class TestTradeClassification:
    """D-004 rule execution tests."""

    def test_classify_trade_single_letter_prefixes(self) -> None:
        """Test single-letter prefixes (A-Y) map directly to their trade."""
        assert classify_trade("A/1") == "A"
        assert classify_trade("B/5") == "B"
        assert classify_trade("F/10") == "F"
        assert classify_trade("K/20") == "K"
        assert classify_trade("Z/1") == "Z"  # Z is valid single letter

    def test_classify_trade_z_prefixes(self) -> None:
        """Test Trade Z (SIGNAGE) has multiple prefixes: AA-AZ, BA-BH."""
        # AA-AZ pattern
        assert classify_trade("AA/1") == "Z"
        assert classify_trade("AC/5") == "Z"
        assert classify_trade("AZ/10") == "Z"

        # BA-BH pattern
        assert classify_trade("BA/1") == "Z"
        assert classify_trade("BC/5") == "Z"
        assert classify_trade("BH/10") == "Z"

    def test_classify_trade_unknown_patterns(self) -> None:
        """Test unknown patterns return UNKNOWN."""
        assert classify_trade(None) == "UNKNOWN"
        assert classify_trade("") == "UNKNOWN"
        assert classify_trade("UNKNOWN/1") == "UNKNOWN"
        assert classify_trade("CONC-001") == "UNKNOWN"  # No matching prefix
        assert classify_trade("X1/1") == "UNKNOWN"  # Not AA-AZ or BA-BH
        assert classify_trade("BI/1") == "UNKNOWN"  # Outside BA-BH range

    def test_classify_trade_case_insensitive(self) -> None:
        """Test classification is case-insensitive."""
        assert classify_trade("a/1") == "A"
        assert classify_trade("AA/1") == "Z"
        assert classify_trade("aa/1") == "Z"
        assert classify_trade("bh/1") == "Z"

    def test_classify_trade_with_whitespace(self) -> None:
        """Test classification handles whitespace correctly."""
        assert classify_trade(" A/1 ") == "A"
        assert classify_trade("  AA/1  ") == "Z"

    def test_classify_trade_complex_codes(self) -> None:
        """Test classification with complex code formats."""
        assert classify_trade("F-001/1") == "F"  # Prefix before dash
        assert classify_trade("AA-001/5") == "Z"  # Prefix before dash
        assert classify_trade("CONC-F/1") == "UNKNOWN"  # No matching prefix

    def test_trade_classification_execution(self) -> None:
        """Test D-004 execution with various item codes."""
        registry = load_registry()
        d004 = registry.get("D-004")
        assert d004 is not None

        rows = [
            make_row(1, item_code="A/1", description="GFA Item"),
            make_row(2, item_code="F/5", description="Concrete Item"),
            make_row(3, item_code="AA/10", description="Signage Item"),
            make_row(4, item_code="UNKNOWN/1", description="Unknown Item"),
            make_row(5, item_code=None, description="No Code Item"),
        ]

        findings = _classify_trades(rows, d004)

        # Should have 4 findings (one for each item with a code)
        assert len(findings) == 4

        # Verify each finding
        finding_a = findings[0]
        assert finding_a.rule_id == "D-004"
        assert finding_a.finding_type == DomainRuleFindingType.TRADE_CLASSIFICATION
        assert finding_a.severity == RuleSeverity.INFO
        assert "classified as trade 'A'" in finding_a.message
        assert finding_a.context["classified_trade"] == "A"

        finding_f = findings[1]
        assert finding_f.context["classified_trade"] == "F"

        finding_z = findings[2]
        assert finding_z.context["classified_trade"] == "Z"

        finding_unknown = findings[3]
        assert finding_unknown.context["classified_trade"] == "UNKNOWN"

    def test_trade_classification_non_item_rows(self) -> None:
        """Test that only Item rows are classified."""
        registry = load_registry()
        d004 = registry.get("D-004")
        assert d004 is not None

        rows = [
            make_row(1, row_type="Head", item_code="A/1"),
            make_row(2, row_type="Note", item_code="F/5"),
            make_row(3, row_type="Section", item_code="AA/10"),
            make_row(4, row_type="Item", item_code="K/20"),  # Only this should be classified
        ]

        findings = _classify_trades(rows, d004)
        assert len(findings) == 1
        assert findings[0].context["classified_trade"] == "K"

    def test_trade_classification_deterministic_ordering(self) -> None:
        """Test that trade classification results are deterministic."""
        registry = load_registry()
        d004 = registry.get("D-004")
        assert d004 is not None

        rows = [
            make_row(3, item_code="K/20"),
            make_row(1, item_code="A/1"),
            make_row(4, item_code="Z/1"),
            make_row(2, item_code="F/5"),
        ]

        findings1 = _classify_trades(rows, d004)
        findings2 = _classify_trades(rows, d004)

        assert len(findings1) == len(findings2)
        for f1, f2 in zip(findings1, findings2):
            assert f1.rule_id == f2.rule_id
            assert f1.row_number == f2.row_number
            assert f1.message == f2.message
            assert f1.context == f2.context

    def test_trade_classification_integration(self) -> None:
        """Test D-004 integration with execute_domain_rules."""
        rows = [
            make_row(1, item_code="A/1", description="GFA", quantity=100.0, uom="m2"),
            make_row(2, item_code="F/5", description="Concrete", quantity=200.0, uom="m3"),
            make_row(3, item_code="AA/10", description="Signage", quantity=50.0, uom="no"),
        ]

        result = execute_domain_rules(rows)

        # Should have D-004 findings
        d004_findings = [f for f in result.findings if f.rule_id == "D-004"]
        assert len(d004_findings) == 3

        # Verify trade classifications
        trades = [f.context["classified_trade"] for f in d004_findings]
        assert "A" in trades
        assert "F" in trades
        assert "Z" in trades

    def test_trade_classification_boundary_cases(self) -> None:
        """Test boundary cases for trade classification."""
        # Edge cases for Z trade prefixes
        assert classify_trade("AZ/1") == "Z"  # Last in AA-AZ range
        assert classify_trade("BH/1") == "Z"  # Last in BA-BH range
        assert classify_trade("BI/1") == "UNKNOWN"  # Just outside BA-BH range

        # All single letters A-Y should work
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXY":
            assert classify_trade(f"{letter}/1") == letter

        # Z should work as single letter
        assert classify_trade("Z/1") == "Z"

        # Empty and None cases
        assert classify_trade("") == "UNKNOWN"
        assert classify_trade("   ") == "UNKNOWN"
        assert classify_trade(None) == "UNKNOWN"
