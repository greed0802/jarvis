"""EP-1004 Acceptance Criterion-verification tests for Platform Hardening & Project Understanding Foundation.

Covers AC-1 through AC-6 per the EP-1004 plan.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from jarvis.contracts.capabilities import (
    EvidenceReference,
    EvidenceSourceType,
)
from jarvis.contracts.execution import (
    ExecutionOutcome,
    ExecutionOutcomeStatus,
    ExecutionProvenance,
)
from jarvis.contracts.understanding import (
    FindingCategory,
    ProjectUnderstanding,
)
from jarvis.engines.checkmate.assembler import FindingReportAssembler
from jarvis.engines.checkmate.registry import RuleRegistry
from jarvis.engines.checkmate.rules import QuantityValidationRule, StandardsAdherenceRule
from jarvis.engines.checkmate.runner import CheckMateEngine
from jarvis.engines.understanding.importer import ProjectUnderstandingImporter
from jarvis.engines.understanding.service import ProjectUnderstandingService
from jarvis.platform.evidence import (
    EvidenceGranularity,
    EvidenceImporter,
    EvidenceStore,
    FileEvidenceRepository,
)

# =============================================================================
# Helpers
# =============================================================================

def _make_two_granularity_repo():
    """Create a repository with evidence at two granularity levels."""
    importer = EvidenceImporter()
    store = EvidenceStore()

    atomic_payload = {
        "document_id": "doc-1",
        "sheet": "Sheet1",
        "evidence_id": "ev-atomic-1",
        "source_type": "cell",
        "granularity": "atomic",
    }
    derived_payload = {
        "document_id": "doc-2",
        "sheet": "Sheet2",
        "evidence_id": "ev-derived-1",
        "source_type": "computed",
        "granularity": "derived",
    }

    store.append(importer.import_payload(atomic_payload))
    store.append(importer.import_payload(derived_payload))
    store.freeze()

    repo = FileEvidenceRepository()
    repo.load_from_store(store)
    return repo

def _make_multi_granularity_repo():
    """Create a repository with evidence at all 4 granularity levels."""
    importer = EvidenceImporter()
    store = EvidenceStore()

    for i, gran in enumerate(["atomic", "structural", "aggregate", "derived"]):
        payload = {
            "document_id": f"doc-{i}",
            "sheet": "Sheet1",
            "evidence_id": f"ev-{gran}-{i}",
            "source_type": "row",
            "granularity": gran,
        }
        store.append(importer.import_payload(payload))

    store.freeze()
    repo = FileEvidenceRepository()
    repo.load_from_store(store)
    return repo

def _make_finding_report():
    """Helper: create a FindingReport with PASS + FAIL outcomes."""
    outcomes = [
        ExecutionOutcome(
            rule_id="r1",
            status=ExecutionOutcomeStatus.PASS,
            domain_category="MEASUREMENT",
            evidence_ids=["e1"],
        ),
        ExecutionOutcome(
            rule_id="r2",
            status=ExecutionOutcomeStatus.FAIL,
            domain_category="COMPLIANCE",
            evidence_ids=["e2"],
            message="Non-standard material detected.",
        ),
    ]

    provenance = ExecutionProvenance(
        execution_id="exec-test",
        evidence_fingerprint="fp-1",
        snapshot_hash="a" * 64,
        capability_version="0.1.0",
    )
    assembler = FindingReportAssembler()
    return assembler.assemble(outcomes, provenance)

# =============================================================================
# AC-1: find_by_granularity returns correctly indexed evidence
# =============================================================================

class TestAC1_GranularityIndexing:
    """AC-1: find_by_granularity returns evidence at requested level."""

    def test_find_by_granularity_atomic(self):
        repo = _make_multi_granularity_repo()
        results = repo.find_by_granularity(EvidenceGranularity.ATOMIC)
        assert len(results) >= 1
        assert all(r.evidence_id.startswith("ev-atomic") for r in results)

    def test_find_by_granularity_all_four_levels(self):
        repo = _make_multi_granularity_repo()
        for gran in EvidenceGranularity:
            results = repo.find_by_granularity(gran)
            assert len(results) >= 1, f"Missing results for {gran}"
            assert all(isinstance(r, EvidenceReference) for r in results)

    def test_find_by_granularity_empty_when_no_match(self):
        repo = _make_two_granularity_repo()
        # "structural" not populated in the two-granularity repo
        results = repo.find_by_granularity(EvidenceGranularity.STRUCTURAL)
        assert results == []

    def test_importer_populates_store_index(self):
        importer = EvidenceImporter()
        store = EvidenceStore()

        result = importer.import_payload({
            "document_id": "d1",
            "sheet": "s1",
            "evidence_id": "ev-idx",
            "source_type": "row",
            "granularity": "aggregate",
        })
        store.append(result)
        store.freeze()

        repo = FileEvidenceRepository()
        repo.load_from_store(store)

        assert len(repo.find_by_granularity(EvidenceGranularity.AGGREGATE)) == 1

# =============================================================================
# AC-2: CheckMateEngine emits native provenance
# =============================================================================

class TestAC2_EngineProvenance:
    """AC-2: Engine produces provenance; assembler consumes it."""

    def test_engine_emits_provenance_on_execute(self):
        engine = CheckMateEngine()
        store = EvidenceStore()
        ref = EvidenceReference(
            document_id="d1", sheet="s1",
            evidence_id="e1", source_type=EvidenceSourceType.ROW,
        )
        store._entries["e1"] = ref
        store.freeze()
        repo = FileEvidenceRepository()
        repo.load_from_store(store)
        engine.bind_evidence(repo)

        registry = RuleRegistry()
        registry.register(QuantityValidationRule())
        snapshot = registry.compile_snapshot()

        result = engine.execute(snapshot)
        assert result.provenance is not None
        assert result.provenance.execution_id != ""
        assert result.provenance.evidence_fingerprint != ""

    def test_assembler_consumes_engine_provenance(self):
        outcomes = [
            ExecutionOutcome(
                rule_id="r1",
                status=ExecutionOutcomeStatus.PASS,
                domain_category="MEASUREMENT",
                evidence_ids=["e1"],
            ),
        ]
        provenance = ExecutionProvenance(
            execution_id="exec-123",
            evidence_fingerprint="abc123",
            snapshot_hash="d" * 64,
            capability_version="0.1.0",
        )
        report = FindingReportAssembler().assemble(outcomes, provenance)

        assert report.provenance.execution_id == "exec-123"
        assert report.provenance.evidence_fingerprint == "abc123"
        assert report.provenance.rule_snapshot_hash == "d" * 64

    def test_assembler_provenance_matches_engine(self):
        """End-to-end: engine.provenance feeds directly into report.provenance."""
        engine = CheckMateEngine()
        store = EvidenceStore()
        ref = EvidenceReference(
            document_id="d1", sheet="s1",
            evidence_id="e1", source_type=EvidenceSourceType.ROW,
        )
        store._entries["e1"] = ref
        store.freeze()
        repo = FileEvidenceRepository()
        repo.load_from_store(store)
        engine.bind_evidence(repo)

        registry = RuleRegistry()
        registry.register(QuantityValidationRule())
        snapshot = registry.compile_snapshot()

        result = engine.execute(snapshot)
        report = FindingReportAssembler().assemble(result.outcomes, result.provenance)

        assert report.provenance.execution_id == result.provenance.execution_id
        assert report.provenance.evidence_fingerprint == result.provenance.evidence_fingerprint

# =============================================================================
# AC-3: ProjectUnderstandingImporter consumes only FindingReport
# =============================================================================

class TestAC3_Importer:
    """AC-3: Importer ingests FindingReport and produces ProjectUnderstanding."""

    def test_importer_produces_understanding_from_report(self):
        report = _make_finding_report()
        importer = ProjectUnderstandingImporter()
        understanding = importer.import_report(report)
        assert isinstance(understanding, ProjectUnderstanding)
        assert understanding.total_rules_executed > 0
        assert understanding.summary != ""

    def test_importer_creates_understanding_findings(self):
        report = _make_finding_report()
        importer = ProjectUnderstandingImporter()
        understanding = importer.import_report(report)

        assert len(understanding.findings) > 0
        for finding in understanding.findings:
            assert isinstance(finding.category, FindingCategory)
            assert finding.severity in ("MAJOR", "MINOR", "CRITICAL", "INFORMATIONAL")
            assert finding.risk_statement != ""
            assert finding.evidence_count > 0

    def test_importer_categorizes_findings(self):
        report = _make_finding_report()
        importer = ProjectUnderstandingImporter()
        understanding = importer.import_report(report)

        assert len(understanding.findings_by_category) >= 1
        assert "measurement" in understanding.findings_by_category
        assert understanding.findings_by_category["measurement"] == 1

# =============================================================================
# AC-4: Service exposes read/query interface
# =============================================================================

class TestAC4_ServiceInterface:
    """Service queries return immutable ProjectUnderstanding contracts."""

    def test_service_ingest_and_retrieve(self):
        service = ProjectUnderstandingService()
        report = _make_finding_report()
        understanding = service.ingest(report)

        assert isinstance(understanding, ProjectUnderstanding)
        retrieved = service.get_understanding(understanding.report_id)
        assert retrieved is not None
        assert retrieved.report_id == understanding.report_id

    def test_service_list_all(self):
        service = ProjectUnderstandingService()
        report = _make_finding_report()
        service.ingest(report)
        service.ingest(report)

        all_records = service.list_all()
        assert len(all_records) == 2

    def test_service_find_by_category(self):
        service = ProjectUnderstandingService()
        report = _make_finding_report()
        service.ingest(report)

        results = service.find_by_category("measurement")
        assert len(results) >= 1

    def test_service_retrieves_summary_statistics(self):
        service = ProjectUnderstandingService()
        report = _make_finding_report()
        service.ingest(report)

        stats = service.get_summary_statistics()
        assert stats["total_reports"] == 1
        assert stats["total_rules_executed"] > 0

    def test_service_is_not_empty_after_ingest(self):
        service = ProjectUnderstandingService()
        assert service.is_empty

        report = _make_finding_report()
        service.ingest(report)
        assert not service.is_empty

# =============================================================================
# AC-5: Boundary Verification — zero CheckMateEngine imports in Understanding
# =============================================================================

class TestAC5_BoundaryVerification:
    """AC-5: ProjectUnderstanding domain has zero imports of CheckMate internals."""

    def _read_module_source(self, module_path: str) -> str:
        """Read the source of a module file."""
        path = Path(module_path)
        return path.read_text(encoding="utf-8") if path.exists() else ""

    def _check_boundary(self, module_name: str, forbidden: list[str]) -> None:
        """Verify a module has no import statements referencing forbidden names.

        Excludes comment/docstring mentions of forbidden names.
        """
        import importlib
        mod = importlib.import_module(module_name)
        assert mod.__file__ is not None
        source = Path(mod.__file__).read_text(encoding="utf-8")

        # Only check import lines, not docstrings or comments
        import_lines = [
            line for line in source.splitlines()
            if line.strip().startswith(("import ", "from "))
        ]

        for name in forbidden:
            for line in import_lines:
                assert name not in line, (
                    f"BOUNDARY VIOLATION: {module_name} imports {name} at: {line.strip()}"
                )

    def test_understanding_store_no_import(self):
        self._check_boundary(
            "jarvis.engines.understanding.store",
            ["CheckMateEngine", "ExecutionOutcome", "RuleSnapshot", "RuleRegistry"],
        )

    def test_understanding_importer_no_checkmate_internals(self):
        self._check_boundary(
            "jarvis.engines.understanding.importer",
            ["CheckMateEngine", "ExecutionOutcome", "RuleSnapshot"],
        )

    def test_understanding_service_no_import(self):
        self._check_boundary(
            "jarvis.engines.understanding.service",
            ["CheckMateEngine", "ExecutionOutcome", "RuleSnapshot", "RuleRegistry"],
        )

# =============================================================================
# AC-6: Integration — full end-to-end pipeline
# =============================================================================

class TestAC6_Integration:
    """Full pipeline: FindingReport → ProjectUnderstanding → Service queries."""

    def test_full_end_to_end_pipeline(self):
        """Engine → FindingReport → Importer → Service → Query."""
        engine = CheckMateEngine()

        store = EvidenceStore()
        ref = EvidenceReference(
            document_id="doc-1", sheet="Sheet1",
            evidence_id="e1", source_type=EvidenceSourceType.ROW,
        )
        store._entries["e1"] = ref
        store.freeze()
        repo = FileEvidenceRepository()
        repo.load_from_store(store)
        engine.bind_evidence(repo)

        registry = RuleRegistry()
        registry.register(QuantityValidationRule())
        registry.register(StandardsAdherenceRule())
        snapshot = registry.compile_snapshot()

        result = engine.execute(snapshot)
        report = FindingReportAssembler().assemble(result.outcomes, result.provenance)

        service = ProjectUnderstandingService()
        understanding = service.ingest(report)

        assert understanding.total_rules_executed == 2
        assert isinstance(understanding.findings, list)
        assert understanding.summary != ""

    def test_platform_hardening_full_integration(self):
        """ED-006, ED-007, ED-008 full pipeline from indexing through service."""
        # 1. Granularity indexing works (ED-006)
        importer = EvidenceImporter()
        store = EvidenceStore()
        for gran in ["atomic", "atomic", "structural", "derived"]:
            payload = {
                "document_id": "final",
                "sheet": "S1",
                "evidence_id": f"ev-{gran}-{len(store._entries)}",
                "source_type": "row",
                "granularity": gran,
            }
            store.append(importer.import_payload(payload))

        repo = FileEvidenceRepository()
        repo.load_from_store(store)
        atomic_evidence = repo.find_by_granularity(EvidenceGranularity.ATOMIC)
        assert len(atomic_evidence) == 2

        # 2. Engine runs and emits provenance (ED-007)
        engine = CheckMateEngine()
        engine.bind_evidence(repo)

        registry = RuleRegistry()
        registry.register(QuantityValidationRule())
        snapshot = registry.compile_snapshot()
        result = engine.execute(snapshot)

        assert result.provenance is not None
        assert result.provenance.snapshot_hash == snapshot.snapshot_hash

        # 3. Assembler consumes engine provenance (ED-007)
        report = FindingReportAssembler().assemble(result.outcomes, result.provenance)
        assert report.provenance.execution_id == result.provenance.execution_id

        # 4. Understanding pipeline
        service = ProjectUnderstandingService()
        understanding = service.ingest(report)
        assert understanding.total_rules_executed > 0