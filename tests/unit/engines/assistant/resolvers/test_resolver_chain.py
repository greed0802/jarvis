"""Acceptance tests for the Knowledge-Driven Assistant (PROD-0003).

Venue: tests/unit/engines/assistant/resolvers/
"""

import pytest
from typing import Optional

from jarvis.engines.assistant.resolvers.base import ResolutionResult
from jarvis.engines.assistant.resolvers.workspace import WorkspaceResolver
from jarvis.engines.assistant.resolvers.artifact import ArtifactResolver
from jarvis.engines.assistant.resolvers.knowledge import KnowledgeResolver
from jarvis.engines.assistant.resolvers.memory import MemoryResolver
from jarvis.engines.assistant.resolvers.capability import CapabilityResolver
from jarvis.engines.assistant.resolvers.chain import ResolverChain
from jarvis.domain.intent import Intent, IntentSemantics
from jarvis.core.capability.models import ExecutionContext, CapabilityInput


def _make_intent(goal: str, semantics: Optional[IntentSemantics] = None) -> Intent:
    return Intent(intent_id="t1", context_id="s1", goal=goal, parameters={}, semantics=semantics)

def _make_context(ws: str = "ws-1", sess: str = "s1") -> ExecutionContext:
    return ExecutionContext(workspace_id=ws, session_id=sess, inputs=CapabilityInput(parameters={}))


class TestResolutionResult:
    def test_contract(self):
        r = ResolutionResult(resolved=True, source="Test", confidence="High", payload="ok",
                             evidence=["e1"], grounded=True, execution_time_ms=1.2,
                             reason="ok", resolution_chain=["TestResolver"])
        assert r.resolved is True
        assert r.source == "Test"
        assert r.confidence == "High"
        assert r.payload == "ok"
        assert r.evidence == ["e1"]
        assert r.grounded is True
        assert r.execution_time_ms == 1.2

    def test_frozen(self):
        r = ResolutionResult(resolved=False, source="?", confidence="Low", payload=None)
        with pytest.raises(Exception):
            r.resolved = True  # type: ignore[misc]


class TestWorkspaceResolver:
    def test_can_resolve_by_keyword(self, workspace_runtime):
        r = WorkspaceResolver(workspace_runtime)
        assert r.can_resolve(_make_intent("what project am I working on")) is True
        assert r.can_resolve(_make_intent("show session")) is True
        assert r.can_resolve(_make_intent("launch rocket")) is False

    def test_no_active_workspace(self, workspace_runtime):
        r = WorkspaceResolver(workspace_runtime)
        res = r.resolve(_make_intent("what workspace"), _make_context())
        assert res.resolved is True
        assert "No active workspace" in str(res.payload) or "Active workspace" in str(res.payload)

    def test_source_attribution(self, workspace_runtime):
        r = WorkspaceResolver(workspace_runtime)
        res = r.resolve(_make_intent("what workspace"), _make_context())
class TestArtifactResolver:
    def test_can_resolve(self, artifact_repository):
        r = ArtifactResolver(artifact_repository)
        assert r.can_resolve(_make_intent("list uploaded files")) is True
        assert r.can_resolve(_make_intent("what documents exist")) is True
        assert r.can_resolve(_make_intent("launch rocket")) is False

    def test_no_artifacts(self, artifact_repository):
        r = ArtifactResolver(artifact_repository)
        res = r.resolve(_make_intent("list files"), _make_context())
        assert "No artifact" in str(res.payload)


class TestKnowledgeResolver:
    def test_no_items(self, workspace_runtime):
        r = KnowledgeResolver(workspace_runtime)
        res = r.resolve(_make_intent("what knowledge items exist"), _make_context())
        assert "No knowledge items" in str(res.payload)


class TestMemoryResolver:
    def test_no_entries(self, memory_service):
        r = MemoryResolver(memory_service)
        res = r.resolve(_make_intent("what is in memory"), _make_context())
        assert "No memory entries" in str(res.payload)


class TestCapabilityResolver:
    def test_can_resolve(self, capability_runtime):
        r = CapabilityResolver(capability_runtime)
        assert r.can_resolve(_make_intent("run boq intelligence")) is True

    def test_list_capabilities(self, capability_runtime):
        r = CapabilityResolver(capability_runtime)
        res = r.resolve(_make_intent("what capabilities exist"), _make_context())
        assert res.resolved is True


class TestResolverChain:
    def test_chain_resolves(self, capability_runtime):
        chain = ResolverChain([WorkspaceResolver(capability_runtime.workspace_runtime)])
        res = chain.resolve(_make_intent("what workspace"), _make_context())
        assert res.resolved is True
        assert res.source == "Workspace"
        assert "WorkspaceResolver" in res.resolution_chain