"""Test suite for EP-C101: Canonical Generation Architecture."""

from __future__ import annotations

import inspect
import pytest

from jarvis.contracts.assistant import GroundingContext
from jarvis.engines.retrieval.contracts import RetrievalTrace, RetrievalQuery, RankedCandidate
from jarvis.engines.reasoning.contracts import (
    ReasoningTrace, CompressedContext, EvidenceGraph, CompressionSpanMap, ReRankedCandidate
)
from jarvis.engines.generation.contracts import (
    ProviderCapabilities, ProviderMetadata, GenerationTrace, ExecutionTrace
)
from jarvis.engines.generation.protocols import BaseGenerationProvider, BaseProviderClient
from jarvis.engines.generation.pipeline import GenerationPipeline
from jarvis.engines.generation.providers import MockGenerationProvider, OpenAIProvider
from jarvis.engines.generation.clients import MockClient, OpenAIClient

# ===========================================================================
# Setup Fixtures
# ===========================================================================

@pytest.fixture
def sample_grounding_context() -> GroundingContext:
    from jarvis.contracts.assistant import RetrievedContext
    return GroundingContext(
        context_id="test_ctx",
        retrieved_context=RetrievedContext("q1", "test"),
        retrieved_evidence=[],
        formatted_prompt_payload="Sample prompt"
    )

@pytest.fixture
def mock_retrieval_trace() -> RetrievalTrace:
    return RetrievalTrace(
        trace_id="rt_1",
        query=RetrievalQuery("test"),
        strategy_hits={},
        fused_hits=(RankedCandidate("d1", "test", 1.0),),
        fusion_algorithm="None",
        latency_ms=1.1,
        timestamp="1"
    )

@pytest.fixture
def mock_reasoning_trace(sample_grounding_context: GroundingContext) -> ReasoningTrace:
    return ReasoningTrace(
        trace_id="reas_1",
        retrieval_trace_id="rt_1",
        reranked_candidates=(),
        compressed_context=CompressedContext(100, "", (), ()),
        evidence_graph=EvidenceGraph((), ()),
        grounding_context=sample_grounding_context,
        latency_ms=2.2,
        timestamp="1"
    )

# ===========================================================================
# Tests
# ===========================================================================

class TestAC1And2ArchitectureDecoupling:
    """Verifies pipeline injection and adapter/client split."""
    def test_pipeline_composition(self):
        client = MockClient()
        provider = MockGenerationProvider(client)
        pipeline = GenerationPipeline(provider)
        assert pipeline._provider is provider

    def test_client_decoupling(self):
        client = OpenAIClient()
        provider = OpenAIProvider(client)
        assert hasattr(provider, "_client")
        assert isinstance(provider._client, BaseProviderClient)
        # Calling raw send_request directly
        raw = client.send_request("hello", None, {})
        assert "usage" in raw

class TestAC3NeutralNormalization:
    """Verifies AssistantResponse format."""
    def test_assistant_response_neutrality(self, sample_grounding_context: GroundingContext):
        provider = MockGenerationProvider(MockClient())
        resp, trace = provider.generate(sample_grounding_context)
        # Verify schema objects
        from jarvis.contracts.assistant import AssistantResponse, GroundingStatus
        assert isinstance(resp, AssistantResponse)
        assert resp.grounding_status == GroundingStatus.FULLY_GROUNDED
        # Absolutely zero raw OpenAI/Anthropic SDK structures
        assert not hasattr(resp, "choices")
        assert not hasattr(resp, "message")

class TestAC4CapabilitiesMetadata:
    """Verifies semantic capability flags."""
    def test_provider_capabilities(self):
        provider = OpenAIProvider(OpenAIClient())
        caps = provider.capabilities
        assert isinstance(caps, ProviderCapabilities)
        assert caps.supports_json is True
        assert caps.supports_streaming is True

class TestAC7ObserverExecutionTrace:
    """Verifies pipeline trace emits properly without mutation."""
    def test_execution_trace_creation(
        self,
        sample_grounding_context: GroundingContext,
        mock_retrieval_trace: RetrievalTrace,
        mock_reasoning_trace: ReasoningTrace
    ):
        pipeline = GenerationPipeline(MockGenerationProvider(MockClient()))
        resp, exec_trace = pipeline.process(
            context=sample_grounding_context,
            retrieval_trace=mock_retrieval_trace,
            reasoning_trace=mock_reasoning_trace
        )
        assert isinstance(exec_trace, ExecutionTrace)
        assert exec_trace.retrieval_trace is mock_retrieval_trace
        assert exec_trace.reasoning_trace is mock_reasoning_trace
        assert isinstance(exec_trace.generation_trace, GenerationTrace)
        assert exec_trace.session_id.startswith("exec_")
        with pytest.raises(Exception):
            exec_trace.total_latency_ms = 0.0  # Immute Check

class TestAC8DependencySafety:
    """Strict boundaries."""
    def test_no_presentation_imports(self):
        forbidden_imports = ("presentation", "jarvis.cli", "jarvis.ui")
        modules = [
            "jarvis.engines.generation",
            "jarvis.engines.generation.contracts",
            "jarvis.engines.generation.protocols",
            "jarvis.engines.generation.pipeline",
            "jarvis.engines.generation.providers.mock",
        ]

        import importlib
        for mod_name in modules:
            mod = importlib.import_module(mod_name)
            src = inspect.getsource(mod)
            for forbidden in forbidden_imports:
                assert f"from {forbidden}" not in src
                assert f"import jarvis.{forbidden}" not in src

class TestAC9DeterministicMockProvider:
    """Reproducible generation testing structure."""
    def test_mock_determinism(self, sample_grounding_context: GroundingContext):
        provider = MockGenerationProvider(MockClient())
        # Identical contexts hit identical logic resulting in predictable lengths.
        r1, t1 = provider.generate(sample_grounding_context)
        assert "Simulated generation response" in r1.response_text
        assert t1.provider_metadata.provider_name == "mock"
        assert t1.token_usage.completion_tokens == 10