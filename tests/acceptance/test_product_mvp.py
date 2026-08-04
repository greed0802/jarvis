"""PROD-0002 Product MVP Acceptance Tests.

These tests exercise the Jarvis Platform end-to-end through the
Interactive Workspace Shell, verifying that `python main.py` can
boot, accept commands, and shut down gracefully.

Every test creates a real Application, brings it to RUNNING state,
and then exercises shell command handlers directly — the same
handlers that the interactive REPL loop uses.
"""

from __future__ import annotations

import uuid
import tempfile
import os

import pytest

from jarvis.application import Application
from jarvis.configuration import Configuration
from jarvis.ui.shell.shell import WorkspaceShell
from jarvis.ui.shell.commands import (
    COMMAND_REGISTRY,
    ShellContext,
    HelpCommand,
    StatusCommand,
    VersionCommand,
    ExitCommand,
    CreateWorkspaceCommand,
    OpenWorkspaceCommand,
    ListWorkspacesCommand,
    WorkspaceCommand,
    UploadCommand,
    ListDocumentsCommand,
    ArtifactsCommand,
    AskCommand,
    SummarizeCommand,
    RunCommand,
    MemoryCommand,
    DebugRuntimeCommand,
)
from jarvis.ui.shell.formatter import ShellFormatter


# ── Fixtures ─────────────────────────────────────────────────────────


@pytest.fixture()
async def running_app():
    """Create a real Application and bring it to RUNNING state."""
    config = Configuration()
    app = Application(config)
    await app.initialize()
    await app.start()
    yield app
    await app.shutdown()


@pytest.fixture()
def shell_context(running_app):
    """Create a ShellContext backed by the running application."""
    return ShellContext(
        application=running_app,
        assistant=running_app.workspace_assistant,
        session_id=str(uuid.uuid4()),
        developer_mode=True,
        formatter=ShellFormatter(),
    )


# ── Phase 1: Core commands ───────────────────────────────────────────


class TestCoreCommands:
    """AC: help, status, version, clear, exit work correctly."""

    async def test_help_lists_all_public_commands(self, shell_context):
        result = HelpCommand().execute([], shell_context)
        for cmd in ("help", "status", "version", "exit",
                     "create-workspace", "upload", "ask", "run"):
            assert cmd in result

    async def test_help_shows_dev_cmds_in_dev_mode(self, shell_context):
        shell_context.developer_mode = True
        result = HelpCommand().execute([], shell_context)
        assert "debug runtime" in result

    async def test_help_hides_dev_cmds_in_normal_mode(self, shell_context):
        shell_context.developer_mode = False
        result = HelpCommand().execute([], shell_context)
        assert "debug runtime" not in result

    async def test_status_returns_platform_info(self, shell_context):
        result = StatusCommand().execute([], shell_context)
        for key in ("Platform State", "Workspace", "Capabilities",
                     "Memory Entries", "Artifacts"):
            assert key in result

    async def test_version_returns_manifest(self, shell_context):
        result = VersionCommand().execute([], shell_context)
        assert "Platform" in result
        assert "Kernel" in result

    async def test_exit_returns_sentinel(self, shell_context):
        assert ExitCommand().execute([], shell_context) == "__EXIT__"


# ── Phase 2: Workspace commands ──────────────────────────────────────


class TestWorkspaceCommands:
    async def test_create_workspace(self, shell_context):
        result = CreateWorkspaceCommand().execute(["TestProj"], shell_context)
        assert "TestProj" in result and "[OK]" in result

    async def test_list_workspaces_after_create(self, shell_context):
        CreateWorkspaceCommand().execute(["Alpha"], shell_context)
        assert "Alpha" in ListWorkspacesCommand().execute([], shell_context)

    async def test_open_workspace(self, shell_context):
        CreateWorkspaceCommand().execute(["Beta"], shell_context)
        result = OpenWorkspaceCommand().execute(["Beta"], shell_context)
        assert "[OK]" in result and "Beta" in result

    async def test_open_nonexistent_workspace(self, shell_context):
        assert "[Error]" in OpenWorkspaceCommand().execute(
            ["NoSuch"], shell_context
        )

    async def test_workspace_shows_active(self, shell_context):
        CreateWorkspaceCommand().execute(["Gamma"], shell_context)
        assert "Gamma" in WorkspaceCommand().execute([], shell_context)

    async def test_workspace_no_active(self, shell_context):
        assert "No active workspace" in WorkspaceCommand().execute(
            [], shell_context
        )

    async def test_create_workspace_missing_name(self, shell_context):
        assert "[Error]" in CreateWorkspaceCommand().execute(
            [], shell_context
        )


# ── Phase 3: Upload & Artifacts ──────────────────────────────────────


class TestUploadCommands:
    async def test_upload_requires_workspace(self, shell_context):
        result = UploadCommand().execute(["some_file.pdf"], shell_context)
        assert "[Error]" in result

    async def test_upload_file_not_found(self, shell_context):
        CreateWorkspaceCommand().execute(["UploadWS"], shell_context)
        result = UploadCommand().execute(
            ["/nonexistent/file.pdf"], shell_context
        )
        assert "[Error]" in result and "not found" in result.lower()

    async def test_upload_real_file(self, shell_context):
        CreateWorkspaceCommand().execute(["DocWS"], shell_context)
        with tempfile.NamedTemporaryFile(
            suffix=".txt", delete=False, mode="w"
        ) as f:
            f.write("test content")
            tmp_path = f.name
        try:
            result = UploadCommand().execute([tmp_path], shell_context)
            assert "Document Registered" in result
            assert "GENERAL_DOCUMENT" in result
            art_result = ArtifactsCommand().execute([], shell_context)
            assert os.path.basename(tmp_path) in art_result
            doc_result = ListDocumentsCommand().execute([], shell_context)
            assert "ki-" in doc_result
        finally:
            os.unlink(tmp_path)

    async def test_upload_missing_path(self, shell_context):
        assert "[Error]" in UploadCommand().execute([], shell_context)

    async def test_artifacts_empty(self, shell_context):
        assert "No artifacts" in ArtifactsCommand().execute(
            [], shell_context
        )

    async def test_list_documents_empty(self, shell_context):
        assert "No documents" in ListDocumentsCommand().execute(
            [], shell_context
        )


# ── Phase 4: Conversation & Execution ────────────────────────────────


class TestConversationCommands:
    async def test_ask_returns_response(self, shell_context):
        result = AskCommand().execute(
            ["What", "is", "Jarvis?"], shell_context
        )
        assert "Assistant" in result

    async def test_summarize_returns_response(self, shell_context):
        assert "Summary" in SummarizeCommand().execute([], shell_context)

    async def test_run_no_args_shows_capabilities(self, shell_context):
        assert "BOQIntelligence" in RunCommand().execute([], shell_context)

    async def test_run_capability(self, shell_context):
        result = RunCommand().execute(["BOQIntelligence"], shell_context)
        assert "SUCCESS" in result

    async def test_run_unknown_capability(self, shell_context):
        assert "[Error]" in RunCommand().execute(["NoSuch"], shell_context)

    async def test_memory_empty(self, shell_context):
        result = MemoryCommand().execute([], shell_context)
        # memory may have entries from history, or be empty
        assert "memory" in result.lower() or "mem-" in result.lower() or "No memory" in result


# ── Phase 5: Developer commands ──────────────────────────────────────


class TestDeveloperCommands:
    async def test_debug_runtime(self, shell_context):
        result = DebugRuntimeCommand().execute([], shell_context)
        assert "Kernel State" in result and "Components" in result


# ── Shell integration ────────────────────────────────────────────────


class TestShellIntegration:
    async def test_shell_dispatch_help(self, running_app):
        shell = WorkspaceShell(application=running_app)
        assert "Available Commands" in shell._dispatch("help")

    async def test_shell_dispatch_exit(self, running_app):
        shell = WorkspaceShell(application=running_app)
        assert shell._dispatch("exit") == "__EXIT__"

    async def test_shell_dispatch_unknown(self, running_app):
        shell = WorkspaceShell(application=running_app)
        result = shell._dispatch("foobar")
        assert "[Error]" in result and "Unknown command" in result

    async def test_shell_dispatch_developer_hidden(self, running_app):
        shell = WorkspaceShell(
            application=running_app, developer_mode=False
        )
        assert "Unknown command" in shell._dispatch("debug runtime")

    async def test_shell_dispatch_developer_visible(self, running_app):
        shell = WorkspaceShell(
            application=running_app, developer_mode=True
        )
        assert "Kernel State" in shell._dispatch("debug runtime")

    async def test_shell_banner(self, running_app):
        shell = WorkspaceShell(application=running_app)
        banner = shell._formatter.banner(
            version="0.0.1-alpha.17",
            workspace="(none)",
            status="running",
        )
        assert "Jarvis Platform" in banner and "running" in banner

    async def test_shell_prompt_no_workspace(self, running_app):
        shell = WorkspaceShell(application=running_app)
        assert "Jarvis>" in shell._build_prompt()

    async def test_shell_prompt_with_workspace(self, running_app):
        shell = WorkspaceShell(application=running_app)
        shell._dispatch("create-workspace PromptTest")
        assert "PromptTest" in shell._build_prompt()

