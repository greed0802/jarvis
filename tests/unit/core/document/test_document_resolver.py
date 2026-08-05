import pytest
import os
from jarvis.application.application import Application
from jarvis.ui.shell.commands import ShellContext
from jarvis.ui.shell.formatter import ShellFormatter
from jarvis.domain.intent import Intent
from jarvis.core.capability.models import ExecutionContext, CapabilityInput
from jarvis.core.artifact.models import ArtifactType

@pytest.mark.asyncio
async def test_document_resolver_conversation():
    app = Application()
    await app.initialize()
    
    # 1. Create and Open a workspace
    workspace = app.workspace_assistant.create_workspace("ProjX")
    app.workspace_assistant.workspace_runtime.workspace_manager.set_active(workspace.workspace_id)
    
    # 2. Assert initially empty
    analysis = app.workspace_assistant.doc_intel_engine.analyze_workspace(workspace.workspace_id)
    assert len(analysis["documents"]) == 0
    assert analysis["completeness"].score == 0.0
    
    # Register mock artifacts
    app.workspace_assistant.artifact_repository.register_artifact(
        workspace_id=workspace.workspace_id,
        name="A-01-Layout.dwg",
        artifact_type=ArtifactType.DRAWING,
        content_hash="hash_a",
        size_bytes=100,
        created_by="shell-user"
    )
    
    app.workspace_assistant.artifact_repository.register_artifact(
        workspace_id=workspace.workspace_id,
        name="project_boq.xlsx",
        artifact_type=ArtifactType.BOQ,
        content_hash="hash_b",
        size_bytes=200,
        created_by="shell-user"
    )
    
    # 3. Test assistant conversational questions routing
    res1 = app.workspace_assistant.resolve("What documents exist?", "sess-id")
    assert res1.resolved is True
    assert "A-01-Layout.dwg" in res1.payload
    assert "project_boq.xlsx" in res1.payload
    
    res2 = app.workspace_assistant.resolve("What documents are missing?", "sess-id")
    assert res2.resolved is True
    assert "Completeness Score: 40%" in res2.payload
    assert "Structural Drawing" in res2.payload
    
    res3 = app.workspace_assistant.resolve("What should I upload next?", "sess-id")
    assert res3.resolved is True
    assert "Missing Structural Drawings" in res3.payload
    
    res4 = app.workspace_assistant.resolve("What can I do with this drawing?", "sess-id")
    assert res4.resolved is True
    assert "PDFTakeoff" in res4.payload
    
    res5 = app.workspace_assistant.resolve("What is the current project state?", "sess-id")
    assert res5.resolved is True
    assert "Completeness Level:   40%" in res5.payload
    assert "A-01-Layout.dwg" in res5.payload
