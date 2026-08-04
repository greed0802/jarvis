"""EP-1003 Acceptance Criterion-verification tests for CheckMate Engine Core & Vertical Slice.

Covers AC-1 through AC-8 per the EP-1003 plan.
Updated for ED-007: engine.execute() now returns EngineExecutionResult.
"""

from __future__ import annotations

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
from jarvis.engines.checkmate.assembler import FindingReportAssembler
from jarvis.engines.checkmate.registry import RuleRegistry
from jarvis.engines.checkmate.rules import (
    CheckMateRule,
    ConformanceCheckRule,
    CrossReferenceCheckRule,
    DataCompletenessRule,
    DomainCategory,
    QuantityValidationRule,
    StandardsAdherenceRule,
)
from jarvis.engines.checkmate.runner import CheckMateEngine
from jarvis.platform.evidence import FileEvidenceRepository, EvidenceStore


# =============================================================================
# Helpers
# =============================================================================

def _make_empty_repo():
    """Create an empty FileEvidenceRepository (no records)."""
    store = EvidenceStore()
    store.freeze()
    repo = FileEvidenceRepository()
    repo.load_from_store(store)
    return repo


def _make_populated_repo():
    """Create a repository with one evidence record."""
    store = EvidenceStore()
    ref = EvidenceReference(
        document_id="doc-1",
        sheet="Sheet1",
        evidence_id="ev-01",
        source_type=EvidenceSourceType.ROW,
    )
    store._entries[ref.evidence_id] = ref
    store.freeze()
    repo = FileEvidenceRepository()
    repo.load_from_store(store)
    return repo


def _make_fake_provenance():
    """Create a minimal ExecutionProvenance for assembler tests."""
    return ExecutionProvenance(
        execution_id="exec-test-1",
        evidence_fingerprint="test-fingerprint",
        snapshot_hash="a" * 64,
        capability_version="0.1.0",
    )


# =============================================================================
# AC-1: Rule Protocol — Self-Contained Evaluation Units
# =============================================================================

class TestAC1_RuleProtocol:
    """AC-1: All 5 rules implement CheckMateRule protocol and register."""

    def test_all_five_rules_implement_checkmate_rule_protocol(self):
        rules = [
            QuantityValidationRule(),
            StandardsAdherenceRule(),
            ConformanceCheckRule(),
            CrossReferenceCheckRule(),
            DataCompletenessRule(),
        ]
        for rule in rules:
            assert isinstance(rule, CheckMateRule), (
                f"{rule.rule_id} does not satisfy CheckMateRule"
            )
            assert isinstance(rule.rule_id, str)
            assert isinstance(rule.domain, DomainCategory)
            assert isinstance(rule.version, str)
            assert hasattr(rule, "evaluate")

    def test_all_5_rules_cover_all_domains(self):
        """All 5 rules cover 5 distinct domain categories."""
        rules = [
            QuantityValidationRule(),
            StandardsAdherenceRule(),
            ConformanceCheckRule(),
            CrossReferenceCheckRule(),
            DataCompletenessRule(),
        ]
        domains = {rule.domain for rule in rules}
        assert DomainCategory.MEASUREMENT in domains
        assert DomainCategory.COMPLIANCE in domains
        assert DomainCategory.SPECIFICATION in domains
        assert DomainCategory.COORDINATION in domains
        assert DomainCategory.DOCUMENTATION_INTEGRITY in domains

    def test_registry_accepts_all_5_rules(self):
        registry = RuleRegistry()
        registry.register(QuantityValidationRule())
        registry.register(StandardsAdherenceRule())
        registry.register(ConformanceCheckRule())
        registry.register(CrossReferenceCheckRule())
        registry.register(DataCompletenessRule())
        assert registry.rule_count == 5

    def test_registry_rejects_duplicate_rule_id(self):
        registry = RuleRegistry()
        registry.register(QuantityValidationRule())
        with pytest.raises(ValueError):
            registry.register(QuantityValidationRule())


# =============================================================================
# AC-2: RuleRegistry compiles immutable RuleSnapshot with deterministic hash
# =============================================================================

class TestAC2_RegistrySnapshot:
    """AC-2: Immutable RuleSnapshot with SHA-256 hash."""

    def test_snapshot_has_hash_and_metadata(self):
        registry = RuleRegistry()
        registry.register(QuantityValidationRule())
        registry.register(StandardsAdherenceRule())
        registry.register(ConformanceCheckRule())

        snapshot = registry.compile_snapshot()
        assert snapshot.rule_count == 3
        assert snapshot.snapshot_hash is not None
        assert len(snapshot.snapshot_hash) == 64
        assert snapshot.metadata.capability_version == "0.1.0"
        assert "MEASUREMENT.001" in snapshot.metadata.rule_ids
        assert "COMPLIANCE_001" in snapshot.metadata.rule_ids
        assert "SPEC-002" in snapshot.metadata.rule_ids

    def test_snapshot_hash_is_deterministic(self):
        registry = RuleRegistry()
        registry.register(QuantityValidationRule())
        snap1 = registry.compile_snapshot()
        snap2 = registry.compile_snapshot()
        assert snap1.snapshot_hash == snap2.snapshot_hash

    def test_snapshot_hash_changes_after_mutation(self):
        registry = RuleRegistry()
        registry.register(QuantityValidationRule())
        hash_before = registry.compile_snapshot().snapshot_hash

        registry.register(StandardsAdherenceRule())
        hash_after = registry.compile_snapshot().snapshot_hash

        assert hash_before != hash_after

    def test_committed_snapshot_not_affected_by_later_additions(self):
        registry = RuleRegistry()
        registry.register(QuantityValidationRule())
        snapshot = registry.compile_snapshot()

        registry.register(StandardsAdherenceRule())
        assert snapshot.rule_count == 1  # snapshot was frozen at compile time


# =============================================================================
# AC-3: ExecutionOutcome reflects PASS, FAIL, UNEVALUABLE
# =============================================================================

class TestAC3_OutcomeReflection:
    """AC-3: Outcomes match specified rule behavior."""

    def test_quantity_validation_pass(self):
        rule = QuantityValidationRule()
        outcome = rule.evaluate(evidence_ids=["ev-1", "ev-2"])
        assert outcome.status == ExecutionOutcomeStatus.PASS
        assert outcome.rule_id == "MEASUREMENT.001"
        assert outcome.domain_category == DomainCategory.MEASUREMENT
        assert "ev-1" in outcome.evidence_ids

    def test_standards_adherence_fails(self):
        rule = StandardsAdherenceRule()
        outcome = rule.evaluate(evidence_ids=["ev-001", "ev-002"])
        assert outcome.status == ExecutionOutcomeStatus.FAIL
        assert "M25" in outcome.message

    def test_conformance_check_fails(self):
        rule = ConformanceCheckRule()
        outcome = rule.evaluate(evidence_ids=["ev-001"])
        assert outcome.status == ExecutionOutcomeStatus.FAIL
        assert "200mm" in outcome.message

    def test_cross_reference_fails(self):
        rule = CrossReferenceCheckRule()
        outcome = rule.evaluate(evidence_ids=["ev-001"])
        assert outcome.status == ExecutionOutcomeStatus.FAIL

    def test_data_completeness_unevaluable_when_empty(self):
        rule = DataCompletenessRule()
        outcome = rule.evaluate(evidence_ids=[])
        assert outcome.status == ExecutionOutcomeStatus.UNEVALUABLE_MISSING_EVIDENCE
        assert "cannot be evaluated" in outcome.message.lower()

    def test_data_completeness_pass_when_evidence(self):
        rule = DataCompletenessRule()
        outcome = rule.evaluate(evidence_ids=["ev-001"])
        assert outcome.status == ExecutionOutcomeStatus.PASS


# =============================================================================
# AC-4: Rule Determinism — same input → same output
# =============================================================================

class TestAC4Determinism:
    """AC-4: Deterministic rule evaluation."""

    def test_repeat_execution_deterministically(self):
        rule = QuantityValidationRule()
        ev = ["ev-1", "ev-2"]
        outcome1 = rule.evaluate(evidence_ids=ev)
        outcome2 = rule.evaluate(evidence_ids=ev)
        assert outcome1.status == outcome2.status
        assert outcome1.rule_id == outcome2.rule_id
        assert outcome1.message == outcome2.message

    def test_cross_reference_determinism(self):
        rule = CrossReferenceCheckRule()
        ev = ["ev-x"]
        out1 = rule.evaluate(evidence_ids=ev)
        out2 = rule.evaluate(evidence_ids=ev)
        assert out1.status == out2.status
        assert out1.message == out2.message


# =============================================================================
# AC-5: Outcome separation — only FAIL → Findings
# =============================================================================

class TestAC5OutcomeSeparation:
    """AC-5: PASS and UNEVALUABLE do NOT produce Findings."""

    def test_assemble_pass_does_not_generate_finding(self):
        outcomes = [
            ExecutionOutcome(
                rule_id="r1",
                status=ExecutionOutcomeStatus.PASS,
                domain_category="MEASUREMENT",
                evidence_ids=["ev-1"],
                message="Passed.",
            ),
        ]
        prov = _make_fake_provenance()
        report = FindingReportAssembler().assemble(outcomes, prov)
        assert len(report.findings) == 0

    def test_assemble_only_fail_enters_findings(self):
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
                message="Non-standard material.",
            ),
            ExecutionOutcome(
                rule_id="r3",
                status=ExecutionOutcomeStatus.UNEVALUABLE_MISSING_EVIDENCE,
                domain_category="DOCUMENTATION_INTEGRITY",
                evidence_ids=[],
                message="No data.",
            ),
        ]
        prov = _make_fake_provenance()
        report = FindingReportAssembler().assemble(outcomes, prov)
        assert len(report.findings) == 1
        assert report.findings[0].rule_id == "r2"


# =============================================================================
# AC-6: Missing evidence → UNEVALUABLE, not crash
# =============================================================================

class TestAC6MissingEvidence:
    """AC-6: Every rule returns UNEVALUABLE on empty evidence, not crash."""

    def test_quantity_validation(self):
        outcome = QuantityValidationRule().evaluate(evidence_ids=[])
        assert outcome.status == ExecutionOutcomeStatus.UNEVALUABLE_MISSING_EVIDENCE

    def test_standards_adherence_missing_evidence(self):
        outcome = StandardsAdherenceRule().evaluate(evidence_ids=[])
        assert outcome.status == ExecutionOutcomeStatus.UNEVALUABLE_MISSING_EVIDENCE

    def test_conformance_check_missing_evidence(self):
        outcome = ConformanceCheckRule().evaluate(evidence_ids=[])
        assert outcome.status == ExecutionOutcomeStatus.UNEVALUABLE_MISSING_EVIDENCE

    def test_cross_reference_missing_evidence(self):
        outcome = CrossReferenceCheckRule().evaluate(evidence_ids=[])
        assert outcome.status == ExecutionOutcomeStatus.UNEVALUABLE_MISSING_EVIDENCE

    def test_data_completeness_missing_evidence(self):
        outcome = DataCompletenessRule().evaluate(evidence_ids=[])
        assert outcome.status == ExecutionOutcomeStatus.UNEVALUABLE_MISSING_EVIDENCE


# =============================================================================
# AC-7: FindingReportAssembler produces complete 4-tier report
# =============================================================================

class TestAC7Assembler:
    """AC-7: Provenance, telemetry, findings, domain coverage."""

    def _prepare_5_outcomes(self):
        """Helper: 5 outcomes matching the 5 vertical-slice rules."""
        return [
            ExecutionOutcome(
                rule_id="MEASUREMENT.001",
                status=ExecutionOutcomeStatus.PASS,
                domain_category="MEASUREMENT",
                evidence_ids=["ev-1"],
                message="All quantities valid.",
            ),
            ExecutionOutcome(
                rule_id="COMPLIANCE_001",
                status=ExecutionOutcomeStatus.FAIL,
                domain_category="COMPLIANCE",
                evidence_ids=["ev-2"],
                message="Non-standard material.",
            ),
            ExecutionOutcome(
                rule_id="SPEC-002",
                status=ExecutionOutcomeStatus.FAIL,
                domain_category="SPECIFICATION",
                evidence_ids=["ev-3"],
                message="Specification deviation.",
            ),
            ExecutionOutcome(
                rule_id="COORD-003",
                status=ExecutionOutcomeStatus.FAIL,
                domain_category="COORDINATION",
                evidence_ids=["ev-4"],
                message="Cross-reference mismatch.",
            ),
            ExecutionOutcome(
                rule_id="DOCINT-004",
                status=ExecutionOutcomeStatus.UNEVALUABLE_MISSING_EVIDENCE,
                domain_category="DOCUMENTATION_INTEGRITY",
                evidence_ids=[],
                message="No evidence.",
            ),
        ]

    def test_report_has_provenance_block(self):
        outcomes = self._prepare_5_outcomes()
        prov = _make_fake_provenance()
        report = FindingReportAssembler().assemble(outcomes, prov)
        assert report.provenance is not None
        assert report.provenance.execution_id != ""
        assert report.provenance.capability_version == "0.1.0"

    def test_report_has_telemetry_summary(self):
        outcomes = self._prepare_5_outcomes()
        prov = _make_fake_provenance()
        report = FindingReportAssembler().assemble(outcomes, prov)
        assert report.telemetry_summary.rule_count_total == 5
        assert report.telemetry_summary.rule_count_executed >= 0

    def test_report_has_three_fail_findings(self):
        outcomes = self._prepare_5_outcomes()
        prov = _make_fake_provenance()
        report = FindingReportAssembler().assemble(outcomes, prov)
        assert len(report.findings) == 3

    def test_report_finding_has_evidence_references(self):
        outcomes = self._prepare_5_outcomes()
        prov = _make_fake_provenance()
        report = FindingReportAssembler().assemble(outcomes, prov)
        for finding in report.findings:
            assert len(finding.evidence) > 0, "Each FAIL Finding must have >=1 EvidenceReference"

    def test_report_finding_has_severity_and_remediation(self):
        outcomes = self._prepare_5_outcomes()
        prov = _make_fake_provenance()
        report = FindingReportAssembler().assemble(outcomes, prov)
        for finding in report.findings:
            assert finding.severity is not None
            assert finding.risk_statement != ""
            assert finding.remediation != ""

    def test_report_has_domain_coverage(self):
        outcomes = self._prepare_5_outcomes()
        prov = _make_fake_provenance()
        report = FindingReportAssembler().assemble(outcomes, prov)
        assert len(report.domain_coverage) >= 1


# =============================================================================
# AC-8: CheckMateEngine end-to-end integration
# =============================================================================

class TestCheckMateEngineIntegration:
    """End-to-end: engine runs snapshot against repository."""

    def test_engine_requires_bind_before_execute(self):
        engine = CheckMateEngine()
        registry = RuleRegistry()
        registry.register(QuantityValidationRule())
        snapshot = registry.compile_snapshot()

        with pytest.raises(RuntimeError, match="must be bound"):
            engine.execute(snapshot)

    def test_engine_executes_empty_repository(self):
        """Empty repository: all rules return UNEVALUABLE."""
        engine = CheckMateEngine()
        empty_repo = _make_empty_repo()
        engine.bind_evidence(empty_repo)

        registry = RuleRegistry()
        registry.register(QuantityValidationRule())
        registry.register(DataCompletenessRule())

        snapshot = registry.compile_snapshot()
        result = engine.execute(snapshot)
        outcomes = result.outcomes

        assert len(outcomes) == 2
        for outcome in outcomes:
            assert outcome.status == ExecutionOutcomeStatus.UNEVALUABLE_MISSING_EVIDENCE

    def test_engine_with_populated_repository(self):
        """Populated repo: PASS and FAIL outcomes."""
        engine = CheckMateEngine()
        populated = _make_populated_repo()
        engine.bind_evidence(populated)

        registry = RuleRegistry()
        registry.register(QuantityValidationRule())
        registry.register(StandardsAdherenceRule())

        snapshot = registry.compile_snapshot()
        result = engine.execute(snapshot)
        outcomes = result.outcomes

        assert len(outcomes) == 2
        result_ids = {o.rule_id: o.status for o in outcomes}
        assert result_ids["MEASUREMENT.001"] == ExecutionOutcomeStatus.PASS
        assert result_ids["COMPLIANCE_001"] == ExecutionOutcomeStatus.FAIL

    def test_engine_is_deterministic(self):
        """Same evidence + same snapshot → identical outcomes (C1.9)."""
        repo1 = _make_populated_repo()
        repo2 = _make_populated_repo()

        engine1 = CheckMateEngine()
        engine1.bind_evidence(repo1)
        engine2 = CheckMateEngine()
        engine2.bind_evidence(repo2)

        registry = RuleRegistry()
        registry.register(QuantityValidationRule())
        snapshot = registry.compile_snapshot()

        result1 = engine1.execute(snapshot)
        result2 = engine2.execute(snapshot)
        outcomes1 = result1.outcomes
        outcomes2 = result2.outcomes

        assert len(outcomes1) == len(outcomes2)
        for o1, o2 in zip(outcomes1, outcomes2):
            assert o1.status == o2.status
            assert o1.rule_id == o2.rule_id
            assert o1.message == o2.message

    def test_full_vertical_slice_integration(self):
        """Full end-to-end: 5 rules → engine → FindingReport."""
        engine = CheckMateEngine()
        engine.bind_evidence(_make_populated_repo())

        registry = RuleRegistry()
        registry.register(QuantityValidationRule())
        registry.register(StandardsAdherenceRule())
        registry.register(ConformanceCheckRule())
        registry.register(CrossReferenceCheckRule())
        registry.register(DataCompletenessRule())

        snapshot = registry.compile_snapshot()
        result = engine.execute(snapshot)
        outcomes = result.outcomes
        provenance = result.provenance

        assembler = FindingReportAssembler()
        report = assembler.assemble(outcomes, provenance)

        assert len(outcomes) == 5
        assert len(report.findings) == 3
        assert report.telemetry_summary.rule_count_total == 5
        assert report.telemetry_summary.coverage_pct > 0
        assert len(report.domain_coverage) >= 4

    def test_engine_provenance_contains_snapshot_hash(self):
        """ED-007: Engine provenance embeds snapshot content hash."""
        engine = CheckMateEngine()
        engine.bind_evidence(_make_populated_repo())

        registry = RuleRegistry()
        registry.register(QuantityValidationRule())
        snapshot = registry.compile_snapshot()

        result = engine.execute(snapshot)
        assert result.provenance is not None
        assert result.provenance.snapshot_hash == snapshot.snapshot_hash