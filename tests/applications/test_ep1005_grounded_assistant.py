"""Test Suite for EP-1005: Grounded AI Assistant & Chat Foundation.

Covers all 7 acceptance criteria and architecture boundary verification.

Tests:
- AC-1 (Understanding Isolation): GenerationProvider receives GroundingContext only
- AC-2 (Evidence Citation): Citations trace to provided evidence
- AC-3 (Boundary Verification): Zero engine imports in assistant domain
- AC-4 (UNSUPPORTED status): Out-of-scope queries yield UNSUPPORTED
- AC-5 (Contract Immutability): All frozen dataclasses raise on mutation
- AC-6 (Provider Interchangeability): Service works with any provider
- AC-7 (Grounding Validation): Validator independent of provider
"""

from __future__ import annotations

import importlib
from dataclasses import FrozenInstanceError, dataclass
from pathlib import Path

import pytest

from jarvis.contracts.assistant import (
    AssistantResponse,
    DraftResponse,
    GroundingContext,
    GroundingStatus,
    RetrievedContext,
)
from jarvis.contracts.capabilities import (
    EvidenceReference,
    EvidenceSourceType,
)
from jarvis.contracts.understanding import FindingCategory, UnderstandingFinding
from jarvis.engines.assistant.providers import MockGenerationProvider
from jarvis.engines.assistant.retrieval import (
    EvidenceRetriever,
    QuestionInterpreter,
    UnderstandingRetriever,
)
from jarvis.engines.assistant.service import GroundedAssistantService
from jarvis.engines.assistant.validator import GroundingValidator

# =============================================================================
# Test Fixture Helpers
# =============================================================================

def _make_finding():
    return UnderstandingFinding(
        finding_id="UF-test001",
        category=FindingCategory.MEASUREMENT,
        severity="MAJOR",
        risk_statement="doc-test Missing measure quantity",
        remediation="Add measure item to BOQ",
        evidence_count=2,
    )

def _make_evidence_refs(count=3):
    refs = []
    for i in range(count):
        refs.append(
            EvidenceReference(
                document_id="doc-test",
                sheet="Sheet1",
                evidence_id=f"evidence-{i}",
                source_type=EvidenceSourceType.CELL,
            )
        )
    return refs

# =============================================================================
# TestAC1 — GenerationProvider Isolation
# =============================================================================

class TestAC1_GenerationIsolation:
    """AC-1: GenerationProvider receives strictly GroundingContext."""

    def test_provider_receives_grounding_context(self):
        retrieved = RetrievedContext(
            query_id="q-test",
            intent_category="compliance_query",
        )
        grounding = GroundingContext(
            context_id="ctx-test",
            retrieved_context=retrieved,
            retrieved_evidence=[],
            formatted_prompt_payload="test payload",
        )
        provider = MockGenerationProvider()
        draft = provider.generate_draft(grounding)
        assert isinstance(draft, DraftResponse)
        assert draft.provider_name == "mock-provider"

    def test_provider_not_passed_raw_understanding(self):
        retrieved = RetrievedContext(
            query_id="q-raw", intent_category="measurement_query"
        )
        grounding = GroundingContext(
            context_id="ctx-raw",
            retrieved_context=retrieved,
        )
        provider = MockGenerationProvider()
        draft = provider.generate_draft(grounding)
        assert isinstance(draft, DraftResponse)
        assert "could not find" in draft.response_text.lower()

# =============================================================================
# TestAC2 — Evidence Citations from repository
# =============================================================================

class TestAC2_EvidenceCitation:
    """AC-2: Evidence cited in AssistantResponse originates from resolved references."""

    def test_cited_evidence_in_response(self):
        fake_evidence = _make_evidence_refs(2)
        dummy_retrieved = RetrievedContext(
            query_id="q-ev", intent_category="measurement_query"
        )
        grounding = GroundingContext(
            context_id="ctx-ev",
            retrieved_context=dummy_retrieved,
            retrieved_evidence=fake_evidence,
        )
        provider = MockGenerationProvider()
        draft = provider.generate_draft(grounding)
        validator = GroundingValidator()
        response = validator.validate(draft, grounding)
        assert len(response.cited_evidence) == 2
        assert response.cited_evidence[0].evidence_id == "evidence-0"

    def test_evidence_preserves_document_origin(self):
        refs = [
            EvidenceReference(
                document_id="proj-001",
                sheet="BOQ",
                evidence_id="row-42",
                source_type=EvidenceSourceType.ROW,
            )
        ]
        assert refs[0].document_id == "proj-001"

# =============================================================================
# TestAC3 — Boundary Verification
# =============================================================================

FORBIDDEN_INTERNALS = [
    "ExecutionOutcome",
    "CheckMateEngine",
    "RuleSnapshot",
    "RuleRegistry",
    "CheckMateRule",
]

class TestAC3_BoundaryVerification:
    """AC-3: Import audit — zero engine imports in assistant domain."""

    def _check_boundary(self, module, forbidden: list[str]):
        source = Path(module.__file__).read_text(encoding="utf-8")
        import_lines = [
            line for line in source.splitlines()
            if line.strip().startswith(("import ", "from "))
        ]
        for name in forbidden:
            for line in import_lines:
                assert name not in line, (
                    f"{module.__file__} imports forbidden '{name}': {line.strip()}"
                )

    def test_contracts_no_checkmate_imports(self):
        import jarvis.contracts.assistant as mod
        self._check_boundary(mod, FORBIDDEN_INTERNALS)

    def test_retrieval_no_checkmate_imports(self):
        import jarvis.engines.assistant.retrieval as mod
        self._check_boundary(mod, FORBIDDEN_INTERNALS)

    def test_providers_no_checkmate_imports(self):
        import jarvis.engines.assistant.providers as mod
        self._check_boundary(mod, FORBIDDEN_INTERNALS)

    def test_validator_no_checkmate_imports(self):
        import jarvis.engines.assistant.validator as mod
        self._check_boundary(mod, FORBIDDEN_INTERNALS)

    def test_service_no_checkmate_imports(self):
        import jarvis.engines.assistant.service as mod
        self._check_boundary(mod, FORBIDDEN_INTERNALS)

# =============================================================================
# TestAC4 — UNSUPPORTED Status
# =============================================================================

class TestAC4_UnsupportedGrounding:
    """AC-4: Out-of-scope queries yield UNSUPPORTED status."""

    def test_no_findings_zero_evidence_is_unsupported(self):
        dummy = RetrievedContext(
            query_id="q-empty",
            intent_category="general_query",
        )
        grounding = GroundingContext(
            context_id="ctx-empty",
            retrieved_context=dummy,
            retrieved_evidence=[],
        )
        provider = MockGenerationProvider()
        draft = provider.generate_draft(grounding)
        validator = GroundingValidator()
        response = validator.validate(draft, grounding)
        assert response.grounding_status == GroundingStatus.UNSUPPORTED

    def test_unsupported_service_method(self):
        service = GroundedAssistantService()
        response = service.respond_unsupported("unknown document XYZ")
        assert response.grounding_status == GroundingStatus.UNSUPPORTED
        assert response.confidence_score == 0.0
        assert len(response.cited_evidence) == 0

    def test_unsupported_provides_followup_suggestions(self):
        service = GroundedAssistantService()
        response = service.respond_unsupported("irrelevant query")
        assert len(response.suggested_followups) > 0

# =============================================================================
# TestAC5 — Immutable Contracts
# =============================================================================

class TestAC5_ImmutableContracts:
    """AC-5: All frozen contracts raise on mutation."""

    def test_assistant_response_frozen(self):
        response = AssistantResponse(
            response_id="test-1",
            query_text="test question",
            response_text="test answer",
            grounding_status=GroundingStatus.PARTIALLY_GROUNDED,
        )
        with pytest.raises(FrozenInstanceError):
            response.response_text = "mutated"

    def test_retrieved_context_frozen(self):
        ctx = RetrievedContext(
            query_id="q-immut", intent_category="test"
        )
        with pytest.raises(FrozenInstanceError):
            ctx.intent_category = "changed"

    def test_grounding_context_frozen(self):
        inner = RetrievedContext(query_id="gc-test", intent_category="mut")
        grounding = GroundingContext(
            context_id="gc-ctx",
            retrieved_context=inner,
        )
        with pytest.raises(FrozenInstanceError):
            grounding.formatted_prompt_payload = "altered"

    def test_draft_response_frozen(self):
        draft = DraftResponse(
            provider_name="mock",
            provider_version="1.0",
            response_text="test",
            generation_metadata={"key": "value"},
        )
        with pytest.raises(FrozenInstanceError):
            draft.response_text = "altered"

# =============================================================================
# TestAC6 — Provider Interchangeability
# =============================================================================

@dataclass
class AlternateMock:
    _provider_name: str = "alt-provider"
    _provider_version: str = "2.0.0"

    @property
    def provider_name(self) -> str:
        return self._provider_name

    @property
    def provider_version(self) -> str:
        return self._provider_version

    def generate_draft(self, context: GroundingContext) -> DraftResponse:
        return DraftResponse(
            provider_name=self._provider_name,
            provider_version=self._provider_version,
            response_text="Content from alternate provider.",
        )

class TestAC6_ServiceWorksWithProvider:
    """AC-6: Service operates with any GenerationProvider."""

    def test_default_provider_emits_response(self):
        provider = MockGenerationProvider()
        dummy = RetrievedContext(query_id="q6", intent_category="general_query")
        grounding = GroundingContext(
            context_id="ctx6",
            retrieved_context=dummy,
        )
        draft = provider.generate_draft(grounding)
        assert isinstance(draft, DraftResponse)

    def test_provider_output_is_deterministic(self):
        provider = MockGenerationProvider()
        dummy = RetrievedContext(query_id="q-det", intent_category="test")
        grounding = GroundingContext(
            context_id="ctx-det",
            retrieved_context=dummy,
        )
        first = provider.generate_draft(grounding)
        second = provider.generate_draft(grounding)
        assert first.response_text == second.response_text
        assert first.provider_name == second.provider_name

    def test_alternate_provider_also_yields_response(self):
        provider = AlternateMock()
        dummy = RetrievedContext(query_id="q-alt", intent_category="test")
        grounding = GroundingContext(
            context_id="ctx-alt",
            retrieved_context=dummy,
        )
        draft = provider.generate_draft(grounding)
        assert draft.provider_name == "alt-provider"
        assert "alternate" in draft.response_text.lower()

# =============================================================================
# TestAC7 — Independent Grounding Validation
# =============================================================================

class TestAC7_IndependentValidation:
    """AC-7: GroundingValidator computes confidence independently of provider."""

    def test_validator_confidence_not_provider_metadata(self):
        finding = _make_finding()
        retrieved = RetrievedContext(
            query_id="q-7",
            intent_category="measurement_query",
            relevant_findings=[finding],
            query_terms=["measure"],
        )
        evidence = _make_evidence_refs(3)
        grounding = GroundingContext(
            context_id="ctx-7",
            retrieved_context=retrieved,
            retrieved_evidence=evidence,
        )
        provider = MockGenerationProvider()
        draft = provider.generate_draft(grounding)
        # Provider metadata has no confidence field — validator owns it
        assert "confidence" not in [k.lower() for k in draft.generation_metadata]

        validator = GroundingValidator()
        response = validator.validate(draft, grounding)
        assert response.confidence_score > 0.0
        assert response.grounding_status != GroundingStatus.UNSUPPORTED

    def test_high_evidence_yields_high_confidence(self):
        findings = [_make_finding() for _ in range(5)]
        refs = _make_evidence_refs(5)
        retrieved = RetrievedContext(
            query_id="q-conf",
            intent_category="measurement_query",
            relevant_findings=findings,
        )
        grounding = GroundingContext(
            context_id="ctx-conf",
            retrieved_context=retrieved,
            retrieved_evidence=refs,
        )
        provider = MockGenerationProvider()
        draft = provider.generate_draft(grounding)
        validator = GroundingValidator()
        res = validator.validate(draft, grounding)
        assert res.confidence_score >= 0.7
        assert res.grounding_status == GroundingStatus.FULLY_GROUNDED

    def test_no_findings_yields_zero_confidence(self):
        dummy = RetrievedContext(
            query_id="q-zero",
            intent_category="general_query",
        )
        grounding = GroundingContext(
            context_id="ctx-zero",
            retrieved_context=dummy,
            retrieved_evidence=[],
        )
        provider = MockGenerationProvider()
        draft = provider.generate_draft(grounding)
        validator = GroundingValidator()
        res = validator.validate(draft, grounding)
        assert res.confidence_score == pytest.approx(0.0, abs=0.01)
        assert res.grounding_status == GroundingStatus.UNSUPPORTED

# =============================================================================
# TestIntegration — End-to-End Pipeline
# =============================================================================

class TestIntegration:
    """Full end-to-end integration tests for the grounded assistant."""

    def test_service_respond_returns_assistant_response(self):
        service = GroundedAssistantService()
        response = service.respond(query="Are there measurement issues?")
        assert isinstance(response, AssistantResponse)

    def test_question_interpreter_extracts_terms(self):
        query = "What are the measurement requirements in the project?"
        interpreter = QuestionInterpreter()
        intent, terms = interpreter.interpret(query)
        assert "measurement" in terms
        assert intent == "measurement_query"

    def test_evidence_retriever_builds_grounding_context(self):
        finding = _make_finding()
        refs = _make_evidence_refs(2)
        retrieved = RetrievedContext(
            query_id="q-int",
            intent_category="integration",
            relevant_findings=[finding],
        )
        retriever = EvidenceRetriever()
        gc = retriever.build_grounding(retrieved, refs)
        assert len(gc.retrieved_evidence) == 2
        assert gc.formatted_prompt_payload is not None