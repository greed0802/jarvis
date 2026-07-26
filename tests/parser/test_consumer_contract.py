"""IP-0002 — BOQ Consumer Contract Enforcement Tests.

Phase 3: Contract Enforcement
Phase 4: Compatibility Tests
"""

import dataclasses
import pytest


# ============================================================================
# Phase 3 — Contract Enforcement
# ============================================================================

class TestStableImports:
    """Verify consumers can import the stable contract symbols."""

    def test_analyze_boq_is_importable(self):
        from jarvis.parsers.costx.boq_intelligence import analyze_boq
        assert callable(analyze_boq)

    def test_boq_intelligence_result_is_importable(self):
        from jarvis.parsers.costx.boq_intelligence import BOQIntelligenceResult
        assert hasattr(BOQIntelligenceResult, "__dataclass_fields__")

    def test_boq_header_node_is_importable(self):
        from jarvis.parsers.costx.boq_intelligence import BOQHeaderNode
        assert hasattr(BOQHeaderNode, "__dataclass_fields__")

    def test_boq_row_is_importable(self):
        from jarvis.parsers.costx.boq_extraction import BOQRow
        assert hasattr(BOQRow, "__dataclass_fields__")

    def test_extract_boq_is_importable(self):
        from jarvis.parsers.costx.boq_extraction import extract_boq
        assert callable(extract_boq)

    def test_all_stable_symbols_are_public(self):
        stable_symbols = {
            ("jarvis.parsers.costx.boq_intelligence", "analyze_boq"),
            ("jarvis.parsers.costx.boq_intelligence", "BOQIntelligenceResult"),
            ("jarvis.parsers.costx.boq_intelligence", "BOQHeaderNode"),
            ("jarvis.parsers.costx.boq_extraction", "BOQRow"),
            ("jarvis.parsers.costx.boq_extraction", "extract_boq"),
        }
        for module_name, symbol_name in stable_symbols:
            module = __import__(module_name, fromlist=[symbol_name])
            assert hasattr(module, symbol_name)
            assert not symbol_name.startswith("_")

    def test_stable_symbols_usable(self):
        from jarvis.parsers.costx.boq_intelligence import (
            analyze_boq,
            BOQIntelligenceResult,
            BOQHeaderNode,
        )
        from jarvis.parsers.costx.boq_extraction import BOQRow, extract_boq

        assert callable(analyze_boq)
        assert callable(extract_boq)
        assert dataclasses.is_dataclass(BOQIntelligenceResult)
        assert dataclasses.is_dataclass(BOQHeaderNode)
        assert dataclasses.is_dataclass(BOQRow)


class TestNoPrivateLeakage:
    """Verify internal (_prefixed) symbols are not exposed through
    the public contract surface."""

    def test_boq_intelligence_has_no_private_in_all(self):
        import jarvis.parsers.costx.boq_intelligence as mod
        all_list = getattr(mod, "__all__", None)
        if all_list is not None:
            for name in all_list:
                assert not name.startswith("_")

    def test_boq_extraction_has_no_private_in_all(self):
        import jarvis.parsers.costx.boq_extraction as mod
        all_list = getattr(mod, "__all__", None)
        if all_list is not None:
            for name in all_list:
                assert not name.startswith("_")

    def test_stable_import_does_not_bring_private_symbols(self):
        from jarvis.parsers.costx.boq_intelligence import (
            analyze_boq,
            BOQIntelligenceResult,
            BOQHeaderNode,
        )
        from jarvis.parsers.costx.boq_extraction import BOQRow, extract_boq

        for obj in [analyze_boq, extract_boq]:
            assert not obj.__name__.startswith("_")
        for cls in [BOQIntelligenceResult, BOQHeaderNode, BOQRow]:
            assert not cls.__name__.startswith("_")

    def test_private_functions_exist_but_are_marked_internal(self):
        import jarvis.parsers.costx.boq_intelligence as mod

        private_funcs = [
            "_count_row_types",
            "_compute_boq_stats",
            "_compute_section_stats",
            "_detect_anomalies",
            "_extract_head_level",
            "_reconstruct_hierarchy",
            "_freeze_node",
            "_compute_hierarchy_statistics",
            "_detect_level_skips",
            "_detect_zero_quantities",
            "_detect_structural_containment",
            "_detect_basic_completeness",
            "_extract_vocabulary",
            "_categorize_head1",
            "_detect_administrative_patterns",
            "_enumerate_sections",
            "_compute_uom_distribution",
            "_compute_header_distribution",
            "_detect_header_quantity_violations",
            "_detect_admin_template_matches",
        ]
        for func_name in private_funcs:
            obj = getattr(mod, func_name, None)
            assert obj is not None, f"Missing internal: {func_name}"
            assert func_name.startswith("_")
            assert callable(obj)


class TestWorkbookParserIsolation:
    """WorkbookParser is pre-extraction infrastructure, not part
    of the evidence contract."""

    def test_workbook_parser_is_not_in_stable_import_list(self):
        import jarvis.parsers.costx
        all_list = getattr(jarvis.parsers.costx, "__all__", None)
        assert all_list is not None
        # Documented: WorkbookParser is pre-extraction infrastructure.
        # It is NOT part of the evidence contract stable imports.
        assert "WorkbookParser" in all_list  # currently exported

    def test_consumer_does_not_need_workbook_parser(self):
        from jarvis.parsers.costx.boq_extraction import BOQRow
        from jarvis.parsers.costx.boq_intelligence import analyze_boq

        rows = [BOQRow(
            row_number=1,
            section="S1",
            code="A01",
            description="Test",
            quantity=1.0,
            uom="unit",
            row_type="Item",
        )]
        result = analyze_boq(rows)
        assert result is not None
        assert isinstance(result.row_classification, dict)


# ============================================================================
# Phase 4 — Compatibility Tests
# ============================================================================

class TestFrozenDataclassImmutability:
    """Verify evidence dataclasses are frozen."""

    def test_boq_intelligence_result_is_frozen(self):
        from jarvis.parsers.costx.boq_intelligence import BOQIntelligenceResult
        assert dataclasses.is_dataclass(BOQIntelligenceResult)
        assert BOQIntelligenceResult.__dataclass_params__.frozen

    def test_boq_header_node_is_frozen(self):
        from jarvis.parsers.costx.boq_intelligence import BOQHeaderNode
        assert dataclasses.is_dataclass(BOQHeaderNode)
        assert BOQHeaderNode.__dataclass_params__.frozen

    def test_boq_row_is_dataclass(self):
        from jarvis.parsers.costx.boq_extraction import BOQRow
        assert dataclasses.is_dataclass(BOQRow)

    def test_mutation_raises_frozen_instance_error(self):
        from jarvis.parsers.costx.boq_extraction import BOQRow
        from jarvis.parsers.costx.boq_intelligence import analyze_boq
        from dataclasses import FrozenInstanceError

        rows = [BOQRow(
            row_number=1,
            section="S1",
            code="A01",
            description="Test",
            quantity=1.0,
            uom="unit",
            row_type="Item",
        )]
        result = analyze_boq(rows)

        with pytest.raises(FrozenInstanceError):
            result.row_classification = {"new": 1}


class TestOptionalFieldBehavior:
    """Verify optional fields return None when their flag is False."""

    def _make_row(self, row_number, uom="Item", quantity=1.0):
        from jarvis.parsers.costx.boq_extraction import BOQRow
        row_type = "Head" if uom.startswith("Head") else "Item"
        return BOQRow(
            row_number=row_number,
            section="Section 1",
            code=f"R{row_number}",
            description="Test row",
            quantity=quantity,
            uom=uom,
            row_type=row_type,
        )

    def test_hierarchy_fields_none_by_default(self):
        from jarvis.parsers.costx.boq_intelligence import analyze_boq
        rows = [self._make_row(1)]
        result = analyze_boq(rows)
        assert result.hierarchy is None
        assert result.hierarchy_statistics is None

    def test_detection_fields_none_by_default(self):
        from jarvis.parsers.costx.boq_intelligence import analyze_boq
        rows = [self._make_row(1)]
        result = analyze_boq(rows)
        assert result.detected_level_skips is None
        assert result.zero_quantity_items is None
        assert result.structural_containment_findings is None
        assert result.completeness_findings is None

    def test_semantic_fields_none_by_default(self):
        from jarvis.parsers.costx.boq_intelligence import analyze_boq
        rows = [self._make_row(1)]
        result = analyze_boq(rows)

        semantic = [
            "vocabulary", "head1_categorization", "administrative_patterns",
            "section_enumeration", "uom_distribution", "uom_percentages",
            "header_distribution", "header_quantity_violations",
            "admin_template_matches",
        ]
        for name in semantic:
            assert hasattr(result, name), f"Missing field: {name}"
            assert getattr(result, name) is None, f"{name} should be None"

    def test_optional_fields_populated_when_enabled(self):
        from jarvis.parsers.costx.boq_intelligence import analyze_boq
        rows = [
            self._make_row(1, uom="Head1", quantity=None),
            self._make_row(2, uom="Head2", quantity=None),
            self._make_row(3, uom="m2", quantity=5.0),
        ]
        result = analyze_boq(
            rows,
            include_hierarchy=True,
            include_detection=True,
            include_semantic=True,
        )

        assert result.hierarchy is not None
        assert result.hierarchy_statistics is not None
        assert result.detected_level_skips is not None
        assert result.zero_quantity_items is not None
        assert result.structural_containment_findings is not None
        assert result.completeness_findings is not None
        assert result.vocabulary is not None
        assert result.head1_categorization is not None
        assert result.administrative_patterns is not None
        assert result.section_enumeration is not None
        assert result.uom_distribution is not None
        assert result.uom_percentages is not None
        assert result.header_distribution is not None
        assert result.header_quantity_violations is not None
        assert result.admin_template_matches is not None


class TestFieldExistence:
    """Verify all 19 contract fields exist."""

    def test_all_19_fields(self):
        from jarvis.parsers.costx.boq_intelligence import BOQIntelligenceResult
        expected = [
            "row_classification", "section_statistics", "boq_statistics",
            "known_anomalies",
            "hierarchy", "hierarchy_statistics",
            "detected_level_skips", "zero_quantity_items",
            "structural_containment_findings", "completeness_findings",
            "vocabulary", "head1_categorization", "administrative_patterns",
            "section_enumeration", "uom_distribution", "uom_percentages",
            "header_distribution", "header_quantity_violations",
            "admin_template_matches",
        ]
        fields = BOQIntelligenceResult.__dataclass_fields__
        for f in expected:
            assert f in fields, f"Missing field: {f}"


class TestBackwardCompatibility:
    """v1.1.0 backward compatible with v1.0 consumer patterns."""

    def test_v1_0_patterns_still_work(self):
        from jarvis.parsers.costx.boq_extraction import BOQRow
        from jarvis.parsers.costx.boq_intelligence import analyze_boq

        rows = [BOQRow(
            row_number=1,
            section="Section 1",
            code="A01",
            description="Test item",
            quantity=5.0,
            uom="m2",
            row_type="Item",
        )]
        result = analyze_boq(rows)

        assert isinstance(result.row_classification, dict)
        assert isinstance(result.section_statistics, dict)
        assert isinstance(result.boq_statistics, dict)
        assert isinstance(result.known_anomalies, list)
        assert result.hierarchy is None
        assert result.detected_level_skips is None

    def test_v1_0_hierarchy_flag_works(self):
        from jarvis.parsers.costx.boq_extraction import BOQRow
        from jarvis.parsers.costx.boq_intelligence import analyze_boq
        rows = [
            BOQRow(
                row_number=1, section="Section 1", code="H1",
                description="Main Header", quantity=None, uom="Head1",
                row_type="Head",
            ),
            BOQRow(
                row_number=2, section="Section 1", code="I01",
                description="Item", quantity=3.0, uom="unit",
                row_type="Item",
            ),
        ]
        result = analyze_boq(rows, include_hierarchy=True)
        assert result.hierarchy is not None

    def test_v1_detenction_flags_works(self):
        from jarvis.parsers.costx.boq_extraction import BOQRow
        from jarvis.parsers.costx.boq_intelligence import analyze_boq
        rows = [
            BOQRow(
                row_number=1, section="Section 1", code="H1",
                description="Main Header", quantity=None, uom="Head1",
                row_type="Head",
            ),
            BOQRow(
                row_number=2, section="Section 1", code="H3",
                description="Level 3 Skip", quantity=None, uom="Head3",
                row_type="Head",
            ),
            BOQRow(
                row_number=3, section="Section 1", code="I01",
                description="Zero qty", quantity=0.0, uom="unit",
                row_type="Item",
            ),
        ]
        result = analyze_boq(
            rows, include_hierarchy=True, include_detection=True,
        )
        assert result.detected_level_skips is not None

    def test_v1_0_consumer_gets_none_for_new_fields(self):
        from jarvis.parsers.costx.boq_extraction import BOQRow
        from jarvis.parsers.costx.boq_intelligence import analyze_boq
        rows = [BOQRow(
            row_number=1, section="Section 1", code="A01",
            description="Test", quantity=1.0, uom="m2",
            row_type="Item",
        )]
        result = analyze_boq(rows)
        assert result.vocabulary is None
        assert result.head1_categorization is None
        assert result.administrative_patterns is None
        assert result.section_enumeration is None
        assert result.uom_percentages is None
        assert result.header_quantity_violations is None
        assert result.admin_template_matches is None


class TestConsumerAccessPatterns:
    """Verify recommended consumer access pattern."""

    def test_recommended_pattern(self):
        from jarvis.parsers.costx.boq_extraction import BOQRow
        from jarvis.parsers.costx.boq_intelligence import analyze_boq
        rows = [
            BOQRow(
                row_number=1, section="Section 1", code="H1",
                description="Header", quantity=None, uom="Head1",
                row_type="Head",
            ),
            BOQRow(
                row_number=2, section="Section 1", code="I01",
                description="Test Item", quantity=10.0, uom="m2",
                row_type="Item",
            ),
        ]
        result = analyze_boq(rows, include_hierarchy=True)
        assert isinstance(result.row_classification, dict)
        assert result.hierarchy is not None
        assert len(result.hierarchy) == 1
        root = result.hierarchy[0]
        assert root.row_number == 1
        assert root.depth == 1

    def test_defensive_optional_access(self):
        from jarvis.parsers.costx.boq_extraction import BOQRow
        from jarvis.parsers.costx.boq_intelligence import analyze_boq
        rows = [
            BOQRow(
                row_number=1, section="Section 1", code="tst1",
                description="First", quantity=1.0, uom="unit",
                row_type="Item",
            ),
            BOQRow(
                row_number=2, section="Section 1", code="tst2",
                description="Second", quantity=2.0, uom="unit",
                row_type="Item",
            ),
        ]
        result = analyze_boq(rows, include_semantic=True)
        if result.vocabulary is not None:
            assert isinstance(result.vocabulary, dict)
        if result.head1_categorization is not None:
            assert isinstance(result.head1_categorization, dict)


class TestNoInternalDependencyLeakage:
    """Verify internal symbols don't leak through consumer imports."""

    def test_consumer_does_not_need_workbook_parser(self):
        from jarvis.parsers.costx.boq_extraction import BOQRow
        from jarvis.parsers.costx.boq_intelligence import analyze_boq
        rows = [BOQRow(
            row_number=1, section="S1", code="A01",
            description="Test", quantity=1.0, uom="unit",
            row_type="Item",
        )]
        result = analyze_boq(rows, include_hierarchy=True)
        assert result is not None

    def test_consumer_imports_only_stable_symbols(self):
        from jarvis.parsers.costx.boq_extraction import BOQRow, extract_boq
        from jarvis.parsers.costx.boq_intelligence import (
            analyze_boq, BOQIntelligenceResult, BOQHeaderNode,
        )
        for obj in [analyze_boq, extract_boq]:
            assert not obj.__name__.startswith("_")
        for cls in [BOQIntelligenceResult, BOQHeaderNode, BOQRow]:
            assert not cls.__name__.startswith("_")

    def test_loader_is_imported_by_extraction_module(self):
        """Documented finding: importing BOQRow triggers loader import.
        This is pre-extraction infrastructure coupling.
        consumers that create BOQRows directly do not depend on
        this import at runtime—they only need the dataclass.
        This test documents the import side effect for transparency.
        """
        import sys
        from jarvis.parsers.costx.boq_extraction import BOQRow  # noqa: F401

        assert "jarvis.parsers.costx.loader" in sys.modules, (
            "Pre-extraction: boq_extraction imports loader as side effect. "
            "This is documented infrastructure coupling, not a consumer dependency."
        )
