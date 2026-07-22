"""Validation Engine Regression Suite.

Tests cover:
  - Deterministic equality (excluding execution_timestamp per SE-FR-01)
  - All 18 rules (V-001 through V-018)
  - Rejected rules skipped (V-801, V-802, V-901, V-902)
  - Optional evidence fields return None correctly
  - Contract verification (finding structure matches contract)
  - Edge cases: empty evidence, total_rows=0, hierarchy=None, empty anomalies
  - Invalid input handling
  - Repeated execution consistency
  - Ordered findings (alphanumeric sort)
  - finding_type correctness (HD-004: explicit from registry)

Authority: HD-005 — Repository Hardening Sprint (Post EQ-0013)
"""

import sys

# Ensure src/ is on sys.path for imports (runs at module load)
if "src" not in sys.path:
    sys.path.insert(0, "src")

import pytest
from dataclasses import dataclass


# ---------- Mock Evidence ----------
@dataclass(frozen=True)
class MockEvidence:
    """Simulates BOQIntelligenceResult for testing."""
    row_classification: dict
    section_statistics: dict
    boq_statistics: dict
    known_anomalies: list
    hierarchy: tuple | None
    hierarchy_statistics: dict | None
    detected_level_skips: tuple | None
    zero_quantity_items: tuple | None
    structural_containment_findings: tuple | None
    completeness_findings: tuple | None


def make_evidence(with_hierarchy=False, with_detection=False):
    """Construct a mock BOQIntelligenceResult with known values."""
    return MockEvidence(
        row_classification={"Head": 3, "Note": 1, "Section": 2, "Item": 10, "Other": 0},
        section_statistics={"S1": {"item_count": 10, "quantity_count": 5}},
        boq_statistics={
            "total_rows": 16,
            "code_rows": 12,
            "description_rows": 7,
            "quantity_rows": 6,
        },
        known_anomalies=[{"row_number": 5, "type": "missing_code"}],
        hierarchy=None if not with_hierarchy else (),
        hierarchy_statistics=None if not with_hierarchy else {"root_headers": 1, "min_depth": 1, "max_depth": 3},
        detected_level_skips=None if not with_detection else ({"from_level": 1, "to_level": 3, "skip_levels": 2},),
        zero_quantity_items=None if not with_detection else ({"row_number": 8, "quantity": 0},),
        structural_containment_findings=None if not with_detection else ({"parent_level": 2, "child_level": 4},),
        completeness_findings=None if not with_detection else ({"section": "S2", "item_count": 0},),
    )


def make_empty_evidence():
    """Evidence with all fields empty/zero."""
    return MockEvidence(
        row_classification={},
        section_statistics={},
        boq_statistics={"total_rows": 0, "code_rows": 0, "description_rows": 0, "quantity_rows": 0},
        known_anomalies=[],
        hierarchy=None,
        hierarchy_statistics=None,
        detected_level_skips=None,
        zero_quantity_items=None,
        structural_containment_findings=None,
        completeness_findings=None,
    )


def make_missing_fields_evidence():
    """Evidence with some required fields set to None.

    boq_statistics is kept as a valid dict (not None) because
    Evidence Contract v1.0 guarantees it is always present.
    section_statistics=None exercises the V-001 missing-field path.
    """
    return MockEvidence(
        row_classification={"Head": 1},
        section_statistics=None,  # missing — triggers V-001
        boq_statistics={"total_rows": 1, "code_rows": 1, "description_rows": 1, "quantity_rows": 1},
        known_anomalies=[],
        hierarchy=None,
        hierarchy_statistics=None,
        detected_level_skips=None,
        zero_quantity_items=None,
        structural_containment_findings=None,
        completeness_findings=None,
    )


# ---------- Fixture ----------
@pytest.fixture(scope="module")
def engine():
    from jarvis.engines.validation.engine import (
        ValidationFinding,
        ValidationFindings,
        validate,
        ENGINE_VERSION,
        CONTRACT_VERSION,
    )
    return {
        "ValidationFinding": ValidationFinding,
        "ValidationFindings": ValidationFindings,
        "validate": validate,
        "ENGINE_VERSION": ENGINE_VERSION,
        "CONTRACT_VERSION": CONTRACT_VERSION,
    }


# ============================================================
# Tests — Deterministic Equality
# ============================================================

class TestDeterminism:
    """SE-FR-01: Same evidence + same rules → same finding fields."""

    def test_repeated_execution_identical_findings(self, engine):
        evidence = make_evidence(with_hierarchy=True, with_detection=True)
        f1 = engine["validate"](evidence, "all")
        f2 = engine["validate"](evidence, "all")

        assert f1.engine_version == f2.engine_version
        assert f1.contract_version == f2.contract_version
        assert len(f1.findings) == len(f2.findings)

        for a, b in zip(f1.findings, f2.findings):
            assert a.rule_id == b.rule_id
            assert a.rule_version == b.rule_version
            assert a.category == b.category
            assert a.finding_type == b.finding_type
            assert a.finding_value == b.finding_value
            assert a.evidence_fields == b.evidence_fields

    def test_different_evidence_produces_different_findings(self, engine):
        e1 = make_evidence(with_hierarchy=True, with_detection=True)
        e2 = make_evidence(with_hierarchy=False, with_detection=False)
        f1 = engine["validate"](e1, "all")
        f2 = engine["validate"](e2, "all")

        map1 = {f.rule_id: f for f in f1.findings}
        map2 = {f.rule_id: f for f in f2.findings}
        assert map1["V-010"].finding_value is True
        assert map2["V-010"].finding_value is False

    def test_specific_rules_produce_consistent_results(self, engine):
        evidence = make_evidence(with_hierarchy=True, with_detection=True)
        f_all = engine["validate"](evidence, "all")
        f_subset = engine["validate"](evidence, ["V-001", "V-007", "V-014"])

        map_all = {f.rule_id: f for f in f_all.findings}
        map_sub = {f.rule_id: f for f in f_subset.findings}

        assert map_sub["V-001"].finding_value == map_all["V-001"].finding_value
        assert map_sub["V-007"].finding_value == map_all["V-007"].finding_value
        assert map_sub["V-014"].finding_value == map_all["V-014"].finding_value


# ============================================================
# Tests — All 18 Rules Execute
# ============================================================

class TestAllRulesExecute:

    def test_all_18_rules_produce_findings(self, engine):
        evidence = make_evidence(with_hierarchy=True, with_detection=True)
        findings = engine["validate"](evidence, "all")
        expected = {f"V-{i:03d}" for i in range(1, 19)}
        produced = {f.rule_id for f in findings.findings}
        assert produced == expected, f"Missing: {expected - produced}, Extra: {produced - expected}"

    def test_finding_count_is_exactly_18(self, engine):
        evidence = make_evidence(with_hierarchy=True, with_detection=True)
        findings = engine["validate"](evidence, "all")
        assert len(findings.findings) == 18


# ============================================================
# Tests — Rejected Rules Skipped
# ============================================================

class TestRejectedRules:

    def test_rejected_rules_not_in_all(self, engine):
        evidence = make_evidence()
        findings = engine["validate"](evidence, "all")
        produced = {f.rule_id for f in findings.findings}
        rejected = {"V-801", "V-802", "V-901", "V-902"}
        assert produced.isdisjoint(rejected), f"Rejected rules found: {produced & rejected}"

    def test_requesting_rejected_rule_produces_no_finding(self, engine):
        evidence = make_evidence()
        findings = engine["validate"](evidence, ["V-901"])
        assert len(findings.findings) == 0

    def test_requesting_unknown_rule_produces_no_finding(self, engine):
        evidence = make_evidence()
        findings = engine["validate"](evidence, ["V-999"])
        assert len(findings.findings) == 0


# ============================================================
# Tests — Optional Evidence Handling
# ============================================================

class TestOptionalEvidence:

    def test_hierarchy_rules_none_when_unavailable(self, engine):
        evidence = make_evidence(with_hierarchy=False, with_detection=False)
        findings = engine["validate"](evidence, "all")
        map_f = {f.rule_id: f for f in findings.findings}

        assert map_f["V-010"].finding_value is False
        assert map_f["V-011"].finding_value is None
        assert map_f["V-012"].finding_value is None

    def test_detection_rules_none_when_unavailable(self, engine):
        evidence = make_evidence(with_hierarchy=False, with_detection=False)
        findings = engine["validate"](evidence, "all")
        map_f = {f.rule_id: f for f in findings.findings}

        assert map_f["V-013"].finding_value is False
        assert map_f["V-014"].finding_value is None
        assert map_f["V-015"].finding_value is None
        assert map_f["V-016"].finding_value is None
        assert map_f["V-017"].finding_value is None
        assert map_f["V-018"].finding_value is None

    def test_hierarchy_rules_populated_when_available(self, engine):
        evidence = make_evidence(with_hierarchy=True, with_detection=False)
        findings = engine["validate"](evidence, "all")
        map_f = {f.rule_id: f for f in findings.findings}

        assert map_f["V-010"].finding_value is True
        assert map_f["V-011"].finding_value == 1
        assert map_f["V-012"].finding_value == {"min_depth": 1, "max_depth": 3}


# ============================================================
# Tests — Contract Verification
# ============================================================

class TestContractCompliance:

    def test_every_finding_has_required_fields(self, engine):
        evidence = make_evidence(with_hierarchy=True, with_detection=True)
        findings = engine["validate"](evidence, "all")

        for f in findings.findings:
            assert isinstance(f.rule_id, str) and f.rule_id
            assert isinstance(f.rule_version, str) and f.rule_version
            assert isinstance(f.category, str) and f.category
            assert isinstance(f.finding_type, str) and f.finding_type
            assert isinstance(f.evidence_fields, tuple)

    def test_findings_tuple_never_none(self, engine):
        evidence = make_evidence()
        findings = engine["validate"](evidence, "all")
        assert findings.findings is not None
        assert isinstance(findings.findings, tuple)

    def test_engine_metadata_fields(self, engine):
        evidence = make_evidence()
        findings = engine["validate"](evidence, "all")

        assert findings.engine_version == engine["ENGINE_VERSION"]
        assert findings.contract_version == engine["CONTRACT_VERSION"]
        assert findings.execution_timestamp is not None
        assert "T" in findings.execution_timestamp

    def test_frozen_dataclass_field_reassignment_blocked(self, engine):
        evidence = make_evidence()
        findings = engine["validate"](evidence, "all")

        with pytest.raises(Exception):
            findings.findings = ()  # type: ignore

        with pytest.raises(Exception):
            findings.engine_version = "2.0.0"  # type: ignore

    def test_findings_are_hashable(self, engine):
        """SI-FR-04: frozen dataclasses are hashable when values are hashable.
        
        Note: Some finding_values contain dicts/lists, making full
        ValidationFindings unhashable. This is accepted per HD-002
        investigation (field-level immutability, not deep immutability).
        Individual ValidationFinding instances with scalar values are hashable.
        """
        evidence = make_evidence()
        findings = engine["validate"](evidence, "all")
        # V-007 finding_value is float 0.75 — hashable
        v007 = [f for f in findings.findings if f.rule_id == "V-007"][0]
        h = hash(v007)
        assert isinstance(h, int)

    def test_no_recommendations_or_assessments(self, engine):
        evidence = make_evidence(with_hierarchy=True, with_detection=True)
        findings = engine["validate"](evidence, "all")

        for f in findings.findings:
            for field_name in ("rule_id", "category", "finding_type"):
                val = getattr(f, field_name)
                assert "recommend" not in str(val).lower()
                assert "assess" not in str(val).lower()
                assert "severity" not in str(val).lower()

    def test_findings_ordered_by_rule_id(self, engine):
        evidence = make_evidence(with_hierarchy=True, with_detection=True)
        findings = engine["validate"](evidence, "all")
        rule_ids = [f.rule_id for f in findings.findings]
        assert rule_ids == sorted(rule_ids)


# ============================================================
# Tests — Edge Cases
# ============================================================

class TestEdgeCases:

    def test_empty_evidence_all_fields_zero(self, engine):
        evidence = make_empty_evidence()
        findings = engine["validate"](evidence, "all")
        map_f = {f.rule_id: f for f in findings.findings}
        assert map_f["V-007"].finding_value == 0.0
        assert map_f["V-008"].finding_value == 0.0

    def test_missing_required_fields(self, engine):
        """V-001 detects when required fields are None.

        Tests that V-001 correctly reports missing fields.
        All guaranteed fields (boq_statistics, row_classification)
        are non-None per Evidence Contract v1.0.
        """
        evidence = MockEvidence(
            row_classification={"Head": 1},
            section_statistics=None,  # None triggers V-001
            boq_statistics={"total_rows": 1, "code_rows": 0, "description_rows": 0, "quantity_rows": 0},
            known_anomalies=[],
            hierarchy=None, hierarchy_statistics=None,
            detected_level_skips=None, zero_quantity_items=None,
            structural_containment_findings=None, completeness_findings=None,
        )
        # Only execute V-001 to avoid cascading failures from other rules
        findings = engine["validate"](evidence, ["V-001"])
        assert len(findings.findings) == 1
        assert findings.findings[0].finding_value == ["section_statistics"]

    def test_total_rows_zero(self, engine):
        evidence = make_empty_evidence()
        findings = engine["validate"](evidence, "all")
        map_f = {f.rule_id: f for f in findings.findings}
        assert map_f["V-007"].finding_value == 0.0
        assert map_f["V-008"].finding_value == 0.0
        assert map_f["V-009"].finding_value == 0.0

    def test_no_known_anomalies(self, engine):
        base = make_evidence(with_hierarchy=True, with_detection=True)
        evidence = MockEvidence(
            row_classification=base.row_classification,
            section_statistics=base.section_statistics,
            boq_statistics=base.boq_statistics,
            known_anomalies=[],
            hierarchy=base.hierarchy,
            hierarchy_statistics=base.hierarchy_statistics,
            detected_level_skips=base.detected_level_skips,
            zero_quantity_items=base.zero_quantity_items,
            structural_containment_findings=base.structural_containment_findings,
            completeness_findings=base.completeness_findings,
        )
        findings = engine["validate"](evidence, "all")
        map_f = {f.rule_id: f for f in findings.findings}
        assert map_f["V-006"].finding_value == []

    def test_negative_row_classification_value(self, engine):
        evidence = MockEvidence(
            row_classification={"Head": -3, "Note": 1, "Section": 2, "Item": 10, "Other": 0},
            section_statistics={"S1": {"item_count": 10, "quantity_count": 5}},
            boq_statistics={"total_rows": 10, "code_rows": 5, "description_rows": 3, "quantity_rows": 2},
            known_anomalies=[],
            hierarchy=None, hierarchy_statistics=None,
            detected_level_skips=None, zero_quantity_items=None,
            structural_containment_findings=None, completeness_findings=None,
        )
        findings = engine["validate"](evidence, "all")
        map_f = {f.rule_id: f for f in findings.findings}
        assert map_f["V-003"].finding_value == {"Head": -3}

    def test_anomaly_out_of_range(self, engine):
        evidence = MockEvidence(
            row_classification={"Head": 1, "Note": 0, "Section": 1, "Item": 8, "Other": 0},
            section_statistics={},
            boq_statistics={"total_rows": 10, "code_rows": 8, "description_rows": 6, "quantity_rows": 4},
            known_anomalies=[{"row_number": 15}, {"row_number": 0}],
            hierarchy=None, hierarchy_statistics=None,
            detected_level_skips=None, zero_quantity_items=None,
            structural_containment_findings=None, completeness_findings=None,
        )
        findings = engine["validate"](evidence, "all")
        map_f = {f.rule_id: f for f in findings.findings}
        assert 15 in map_f["V-006"].finding_value
        assert 0 in map_f["V-006"].finding_value

    def test_skip_magnitudes_with_no_skips(self, engine):
        base = make_evidence(with_hierarchy=True, with_detection=True)
        evidence = MockEvidence(
            row_classification=base.row_classification,
            section_statistics=base.section_statistics,
            boq_statistics=base.boq_statistics,
            known_anomalies=base.known_anomalies,
            hierarchy=base.hierarchy,
            hierarchy_statistics=base.hierarchy_statistics,
            detected_level_skips=(),
            zero_quantity_items=base.zero_quantity_items,
            structural_containment_findings=base.structural_containment_findings,
            completeness_findings=base.completeness_findings,
        )
        findings = engine["validate"](evidence, "all")
        map_f = {f.rule_id: f for f in findings.findings}
        assert map_f["V-014"].finding_value == 0
        assert map_f["V-015"].finding_value == {"min_magnitude": None, "max_magnitude": None}


# ============================================================
# Tests — finding_type Correctness (HD-004)
# ============================================================

class TestFindingType:
    EXPECTED_TYPES = {
        "V-001": "list", "V-002": "list", "V-003": "list",
        "V-004": "difference", "V-005": "list", "V-006": "list",
        "V-007": "ratio", "V-008": "ratio", "V-009": "ratio",
        "V-010": "presence", "V-011": "count", "V-012": "value",
        "V-013": "presence", "V-014": "count", "V-015": "value",
        "V-016": "count", "V-017": "count", "V-018": "count",
    }

    def test_all_finding_types_match_registry(self, engine):
        evidence = make_evidence(with_hierarchy=True, with_detection=True)
        findings = engine["validate"](evidence, "all")

        for f in findings.findings:
            expected = self.EXPECTED_TYPES.get(f.rule_id, "value")
            assert f.finding_type == expected, (
                f"{f.rule_id}: expected '{expected}', got '{f.finding_type}'"
            )

    def test_no_heuristic_inference(self, engine):
        from jarvis.engines.validation import engine as eng_module
        assert not hasattr(eng_module, "_classify_finding_type"), (
            "HD-004: heuristic _classify_finding_type should be removed"
        )


# ============================================================
# Tests — Specific Rule Values
# ============================================================

class TestSpecificRuleValues:

    def test_v001_required_fields_all_present(self, engine):
        evidence = make_evidence()
        findings = engine["validate"](evidence, "all")
        map_f = {f.rule_id: f for f in findings.findings}
        assert map_f["V-001"].finding_value == []

    def test_v002_classification_keys_valid(self, engine):
        evidence = make_evidence()
        findings = engine["validate"](evidence, "all")
        map_f = {f.rule_id: f for f in findings.findings}
        assert map_f["V-002"].finding_value["missing_keys"] == []
        assert map_f["V-002"].finding_value["unexpected_keys"] == []

    def test_v003_nonnegative(self, engine):
        evidence = make_evidence()
        findings = engine["validate"](evidence, "all")
        map_f = {f.rule_id: f for f in findings.findings}
        assert map_f["V-003"].finding_value == {}

    def test_v004_row_sum_consistency(self, engine):
        evidence = make_evidence()
        findings = engine["validate"](evidence, "all")
        map_f = {f.rule_id: f for f in findings.findings}
        assert map_f["V-004"].finding_value["difference"] == 0

    def test_v007_code_completeness(self, engine):
        evidence = make_evidence()
        findings = engine["validate"](evidence, "all")
        map_f = {f.rule_id: f for f in findings.findings}
        assert map_f["V-007"].finding_value == 0.75

    def test_v014_level_skip_count(self, engine):
        evidence = make_evidence(with_detection=True)
        findings = engine["validate"](evidence, "all")
        map_f = {f.rule_id: f for f in findings.findings}
        assert map_f["V-014"].finding_value == 1

    def test_v016_zero_quantity_count(self, engine):
        evidence = make_evidence(with_detection=True)
        findings = engine["validate"](evidence, "all")
        map_f = {f.rule_id: f for f in findings.findings}
        assert map_f["V-016"].finding_value == 1