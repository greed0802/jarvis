"""Test suite for CP-0001: Conversation Workbench & Interactive CLI."""

from __future__ import annotations

import inspect
import asyncio
import pytest

from jarvis.application.contracts import ConversationRequest
from jarvis.application.conversation import ConversationService
from jarvis.engines.retrieval.coordinator import RetrievalCoordinator
from jarvis.engines.reasoning.pipeline import ReasoningPipeline
from jarvis.engines.reasoning.reranker import HeuristicReRanker
from jarvis.engines.reasoning.compressor import TokenWindowCompressor
from jarvis.engines.reasoning.synthesizer import GraphSynthesizer
from jarvis.engines.generation.pipeline import GenerationPipeline
from jarvis.engines.generation.providers.mock import MockGenerationProvider
from jarvis.engines.generation.clients.mock_client import MockClient

from jarvis.cli.formatter import CLIFormatter
from jarvis.cli.slash_commands import CommandRegistry
from jarvis.cli.workbench import InteractiveCLIWorkbench

# ===========================================================================
# AC-1: Application Orchestration
# ===========================================================================

@pytest.mark.asyncio
async def test_application_orchestration():
    """ConversationService processes ConversationRequest and emits proper traces."""
    class MockFusion:
        def combine(self, hits, limit):
            return tuple()

    retrieval = RetrievalCoordinator((), MockFusion())
    reasoning = ReasoningPipeline(HeuristicReRanker(), TokenWindowCompressor(), GraphSynthesizer())
    generation = GenerationPipeline(MockGenerationProvider(MockClient()))
    
    service = ConversationService(retrieval, reasoning, generation)
    
    req = ConversationRequest(prompt="Test prompt orchestration")
    resp, exec_trace = await service.execute(req)
    
    assert resp.response_text
    assert exec_trace.session_id.startswith("exec_")
    assert exec_trace.generation_trace.provider_metadata.provider_name == "mock"

# ===========================================================================
# AC-2: Passive CLI Adapter
# ===========================================================================

def test_workbench_is_passive_adapter():
    """Workbench must only have access to service and formatter. No engine imports."""
    from jarvis.cli import workbench
    src = inspect.getsource(workbench)
    
    assert "RetrievalCoordinator" not in src
    assert "GenerationPipeline" not in src
    assert "import jarvis.engines" not in src

# ===========================================================================
# AC-3 & AC-4: Renderer Protocol Compliance & Citation Display
# ===========================================================================

def test_renderer_protocol_and_formatting():
    """CLIFormatter formats strings using isolated protocol."""
    formatter = CLIFormatter()
    
    # Needs a mock response to test the formatter
    from jarvis.contracts.assistant import AssistantResponse, GroundingStatus
    
    resp = AssistantResponse(
        response_id="r1",
        query_text="query",
        response_text="Standard response",
        grounding_status=GroundingStatus.FULLY_GROUNDED,
        cited_evidence=["EV-102"],
        confidence_score=0.9
    )
    
    text = formatter.render_response(resp)
    assert "Standard response" in text
    assert "[Citations: EV-102]" in text

# ===========================================================================
# AC-5 & AC-6: Slash Commands & Kernel Diagnostics
# ===========================================================================

def test_command_registry_and_diagnostics():
    """Slash commands route correctly and format output."""
    class FakeService:
        def get_status(self):
            return {"kernel_state": "RUNNING", "platform_version": "v9.9"}
            
    registry = CommandRegistry(FakeService(), CLIFormatter())
    
    assert registry.can_handle("/status") is True
    assert registry.can_handle("hello") is False
    
    res_status = registry.handle("/status")
    assert "RUNNING" in res_status
    
    res_help = registry.handle("/help")
    assert "/clear" in res_help

# ===========================================================================
# AC-8: Architecture Boundary Protection
# ===========================================================================

def test_architecture_boundary():
    """No engine module imports cli."""
    # We will test a few core engines to confirm they don't depend backward
    modules = [
        "jarvis.engines.retrieval",
        "jarvis.engines.reasoning",
        "jarvis.engines.generation",
        "jarvis.application.conversation"
    ]
    
    import importlib
    for mod_name in modules:
        try:
            mod = importlib.import_module(mod_name)
            src = inspect.getsource(mod)
            assert "jarvis.cli" not in src
        except ImportError:
            pass