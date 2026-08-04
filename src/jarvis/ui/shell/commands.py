"""Shell command handlers — each command is a handler class.

Every handler delegates to platform services via WorkspaceAssistant
or Application public APIs.  The Shell never contains business logic.
"""

from __future__ import annotations

import asyncio
import os
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional

from jarvis.ui.shell.formatter import ShellFormatter


@dataclass
class ShellContext:
    """Immutable bag of platform references available to every handler."""

    application: Any          # jarvis.application.Application
    assistant: Any            # jarvis.engines.assistant.orchestrator.WorkspaceAssistant
    session_id: str
    developer_mode: bool = False
    formatter: ShellFormatter = field(default_factory=ShellFormatter)


class CommandHandler(ABC):
    """Base class for all shell commands."""

    name: str = ""
    description: str = ""
    usage: str = ""
    developer_only: bool = False

    @abstractmethod
    def execute(self, args: list[str], ctx: ShellContext) -> str:
        """Execute the command and return displayable output."""
        ...


# ── Phase 1 — Core commands ─────────────────────────────────────────


class HelpCommand(CommandHandler):
    name = "help"
    description = "Display available commands"
    usage = "help"

    def execute(self, args: list[str], ctx: ShellContext) -> str:
        lines = ["\n  Available Commands", "  ─────────────────"]
        for handler in COMMAND_REGISTRY:
            if handler.developer_only and not ctx.developer_mode:
                continue
            lines.append(f"  {handler.name:<22} {handler.description}")
        return "\n".join(lines)


class StatusCommand(CommandHandler):
    name = "status"
    description = "Platform status summary"
    usage = "status"

    def execute(self, args: list[str], ctx: ShellContext) -> str:
        from jarvis.version import __version__
        app = ctx.application
        status = ctx.assistant.get_platform_status()
        data = {
            "Version": __version__,
            "Platform State": str(app.state),
            "Workspace": status["workspace"],
            "Workspaces": status["workspaces_count"],
            "Knowledge Items": status["knowledge_items"],
            "Capabilities": status["capabilities"],
            "Memory Entries": status["memory_entries"],
            "Artifacts": status["artifacts"],
        }
        return ctx.formatter.section(
            "Jarvis Platform Status", ctx.formatter.key_value(data)
        )


class VersionCommand(CommandHandler):
    name = "version"
    description = "Platform version manifest"
    usage = "version"

    def execute(self, args: list[str], ctx: ShellContext) -> str:
        from jarvis.version import __version__
        data = {
            "Platform": __version__,
            "Kernel": "1.0",
            "Shell": "1.0",
        }
        return ctx.formatter.section(
            "Version Manifest", ctx.formatter.key_value(data)
        )


class ClearCommand(CommandHandler):
    name = "clear"
    description = "Clear terminal screen"
    usage = "clear"

    def execute(self, args: list[str], ctx: ShellContext) -> str:
        os.system("cls" if os.name == "nt" else "clear")
        return ""


class ExitCommand(CommandHandler):
    name = "exit"
    description = "Shutdown the platform gracefully"
    usage = "exit"

    def execute(self, args: list[str], ctx: ShellContext) -> str:
        # Returning a sentinel value the Shell loop checks
        return "__EXIT__"


# ── Phase 2 — Workspace commands ─────────────────────────────────────


class CreateWorkspaceCommand(CommandHandler):
    name = "create-workspace"
    description = "Create a new workspace"
    usage = "create-workspace <name>"

    def execute(self, args: list[str], ctx: ShellContext) -> str:
        if not args:
            return ctx.formatter.error(
                "Usage: create-workspace <name>"
            )
        name = " ".join(args)
        ws = ctx.assistant.create_workspace(name)
        # Auto-activate the new workspace
        ctx.assistant.open_workspace(name)
        return ctx.formatter.success(
            f"Workspace '{ws.name}' created and activated. "
            f"(id: {ws.workspace_id})"
        )


class OpenWorkspaceCommand(CommandHandler):
    name = "open-workspace"
    description = "Set the active workspace"
    usage = "open-workspace <name>"

    def execute(self, args: list[str], ctx: ShellContext) -> str:
        if not args:
            return ctx.formatter.error(
                "Usage: open-workspace <name>"
            )
        name = " ".join(args)
        ws = ctx.assistant.open_workspace(name)
        if ws is None:
            return ctx.formatter.error(
                f"Workspace '{name}' not found. "
                "Use 'list-workspaces' to see available workspaces."
            )
        return ctx.formatter.success(
            f"Workspace '{ws.name}' is now active."
        )


class ListWorkspacesCommand(CommandHandler):
    name = "list-workspaces"
    description = "List all workspaces"
    usage = "list-workspaces"

    def execute(self, args: list[str], ctx: ShellContext) -> str:
        workspaces = ctx.assistant.list_workspaces()
        if not workspaces:
            return ctx.formatter.info("No workspaces created yet.")
        active = ctx.assistant.get_active_workspace()
        rows = []
        for ws in workspaces:
            marker = " *" if (active and active.workspace_id == ws.workspace_id) else ""
            rows.append([ws.workspace_id, ws.name + marker, ws.created_at.isoformat()])
        return ctx.formatter.table(
            ["ID", "Name", "Created"], rows
        )


class WorkspaceCommand(CommandHandler):
    name = "workspace"
    description = "Show active workspace details"
    usage = "workspace"

    def execute(self, args: list[str], ctx: ShellContext) -> str:
        ws = ctx.assistant.get_active_workspace()
        if ws is None:
            return ctx.formatter.info(
                "No active workspace. Use 'create-workspace <name>' "
                "or 'open-workspace <name>' first."
            )
        data = {
            "ID": ws.workspace_id,
            "Name": ws.name,
            "Created": ws.created_at.isoformat(),
        }
        return ctx.formatter.section(
            "Active Workspace", ctx.formatter.key_value(data)
        )

# ── Phase 3 — Knowledge & Artifact commands ──────────────────────────


class UploadCommand(CommandHandler):
    name = "upload"
    description = "Upload and register a document"
    usage = "upload <path>"

    def execute(self, args: list[str], ctx: ShellContext) -> str:
        if not args:
            return ctx.formatter.error("Usage: upload <path>")
        file_path = " ".join(args)
        try:
            meta = ctx.assistant.upload_document(file_path)
        except FileNotFoundError as exc:
            return ctx.formatter.error(str(exc))
        except ValueError as exc:
            return ctx.formatter.error(str(exc))
        return ctx.formatter.section(
            "Document Registered",
            ctx.formatter.key_value(meta),
        )


class ListDocumentsCommand(CommandHandler):
    name = "list-documents"
    description = "List knowledge items"
    usage = "list-documents"

    def execute(self, args: list[str], ctx: ShellContext) -> str:
        docs = ctx.assistant.list_documents()
        if not docs:
            return ctx.formatter.info("No documents registered yet.")
        rows = [
            [d["knowledge_id"], d["resource_uri"], d["added_at"]]
            for d in docs
        ]
        return ctx.formatter.table(
            ["ID", "Resource", "Added"], rows
        )


class ArtifactsCommand(CommandHandler):
    name = "artifacts"
    description = "List registered artifacts"
    usage = "artifacts"

    def execute(self, args: list[str], ctx: ShellContext) -> str:
        arts = ctx.assistant.get_artifacts_summary()
        if not arts:
            return ctx.formatter.info("No artifacts registered yet.")
        rows = [
            [a["artifact_id"], a["name"], a["type"], str(a["versions"])]
            for a in arts
        ]
        return ctx.formatter.table(
            ["ID", "Name", "Type", "Versions"], rows
        )


# ── Phase 4 — Conversation & Execution commands ─────────────────────


class AskCommand(CommandHandler):
    name = "ask"
    description = "Ask the workspace assistant a question"
    usage = 'ask "<question>"'

    def execute(self, args: list[str], ctx: ShellContext) -> str:
        if not args:
            return ctx.formatter.error('Usage: ask "<question>"')
        question = " ".join(args).strip('"').strip("'")
        
        try:
            # Use the new resolve() API to get ResolutionResult with attribution
            resolved = ctx.assistant.resolve(question, ctx.session_id)

            lines = []
            lines.append(ctx.formatter.info(str(resolved.payload)))
            lines.append("")
            lines.append(
                f"  {ctx.formatter.label('Source')}     {resolved.source}"
            )
            lines.append(
                f"  {ctx.formatter.label('Confidence')} {resolved.confidence}"
            )
            if resolved.grounded:
                lines.append(
                    f"  {ctx.formatter.label('Grounded')}   Yes"
                )
            if resolved.evidence:
                lines.append(
                    f"  {ctx.formatter.label('Evidence')}   {', '.join(resolved.evidence)}"
                )
            if ctx.developer_mode and resolved.resolution_chain:
                chain = " → ".join(resolved.resolution_chain)
                lines.append(
                    f"  {ctx.formatter.label('Chain')}      {chain}"
                )
            if resolved.execution_time_ms is not None:
                lines.append(
                    f"  {ctx.formatter.label('Time')}       {resolved.execution_time_ms:.1f} ms"
                )

            return "\n".join(lines)

        except Exception as exc:
            return ctx.formatter.error(f"Assistant error: {exc}")


class SummarizeCommand(CommandHandler):
    name = "summarize"
    description = "Summarize workspace context"
    usage = "summarize"

    def execute(self, args: list[str], ctx: ShellContext) -> str:
        prompt = "Summarize the current workspace context."
        resolved = ctx.assistant.resolve(prompt, ctx.session_id)
        return ctx.formatter.section("Summary", ctx.formatter.info(str(resolved.payload)))


class RunCommand(CommandHandler):
    name = "run"
    description = "Execute a registered capability"
    usage = "run <capability>"

    def execute(self, args: list[str], ctx: ShellContext) -> str:
        if not args:
            caps = ctx.assistant.list_capabilities()
            if not caps:
                return ctx.formatter.info("No capabilities registered.")
            rows = [[c["name"], c["description"]] for c in caps]
            return (
                ctx.formatter.error("Usage: run <capability>")
                + "\n\n"
                + ctx.formatter.table(["Capability", "Description"], rows)
            )
        cap_name = args[0]
        try:
            result = ctx.assistant.run_capability(
                cap_name, ctx.session_id
            )
        except ValueError as exc:
            return ctx.formatter.error(str(exc))
        except Exception as exc:
            return ctx.formatter.error(f"Capability error: {exc}")
        return ctx.formatter.section(
            f"Capability: {cap_name}",
            ctx.formatter.key_value(result),
        )


class MemoryCommand(CommandHandler):
    name = "memory"
    description = "Show workspace memory entries"
    usage = "memory"

    def execute(self, args: list[str], ctx: ShellContext) -> str:
        entries = ctx.assistant.get_memory_summary()
        if not entries:
            return ctx.formatter.info("No memory entries yet.")
        rows = [
            [e["entry_id"], e["category"], e["created_at"]]
            for e in entries
        ]
        return ctx.formatter.table(
            ["ID", "Category", "Created"], rows
        )


# ── Phase 5 — Developer commands ─────────────────────────────────────


class DebugRuntimeCommand(CommandHandler):
    name = "debug runtime"
    description = "Show runtime internal state"
    usage = "debug runtime"
    developer_only = True

    def execute(self, args: list[str], ctx: ShellContext) -> str:
        app = ctx.application
        data = {
            "Kernel State": str(app.kernel.state),
            "Components": len(app.kernel._components),
            "Services": len(app.kernel._services),
        }
        return ctx.formatter.section(
            "Runtime Debug", ctx.formatter.key_value(data)
        )


class DebugPlannerCommand(CommandHandler):
    name = "debug planner"
    description = "Show planner configuration"
    usage = "debug planner"
    developer_only = True

    def execute(self, args: list[str], ctx: ShellContext) -> str:
        planner = ctx.application.intent_planner
        caps = planner.capability_runtime.registry.list_all()
        data = {
            "Registered Capabilities": len(caps),
        }
        for c in caps:
            data[f"  {c.name}"] = c.description
        return ctx.formatter.section(
            "Planner Debug", ctx.formatter.key_value(data)
        )


class DebugMemoryCommand(CommandHandler):
    name = "debug memory"
    description = "Show memory graph details"
    usage = "debug memory"
    developer_only = True

    def execute(self, args: list[str], ctx: ShellContext) -> str:
        mem = ctx.application.memory_service
        data = {
            "Entries": len(mem._entries),
            "Graph Nodes": len(mem.graph.nodes),
            "Graph Edges": len(mem.graph.edges),
        }
        return ctx.formatter.section(
            "Memory Debug", ctx.formatter.key_value(data)
        )


class DebugCapabilitiesCommand(CommandHandler):
    name = "debug capabilities"
    description = "Show capability registry"
    usage = "debug capabilities"
    developer_only = True

    def execute(self, args: list[str], ctx: ShellContext) -> str:
        cap_rt = ctx.application.capability_runtime
        caps = cap_rt.registry.list_all()
        if not caps:
            return ctx.formatter.info("No capabilities registered.")
        rows = []
        for c in caps:
            rows.append([c.name, c.description, str(c.input_schema)])
        return ctx.formatter.table(
            ["Name", "Description", "Input Schema"], rows
        )


class DebugKnowledgeCommand(CommandHandler):
    name = "debug knowledge"
    description = "Show knowledge engine state"
    usage = "debug knowledge"
    developer_only = True

    def execute(self, args: list[str], ctx: ShellContext) -> str:
        ke = ctx.application.knowledge_engine
        data = {
            "Source Registry": type(ke.source_registry).__name__,
            "Parser Registry": type(ke.parser_registry).__name__,
            "Normalizer": type(ke.normalizer).__name__,
            "Validator": type(ke.validator).__name__,
        }
        return ctx.formatter.section(
            "Knowledge Engine Debug", ctx.formatter.key_value(data)
        )


# ── Command Registry ─────────────────────────────────────────────────

COMMAND_REGISTRY: list[CommandHandler] = [
    HelpCommand(),
    StatusCommand(),
    VersionCommand(),
    ClearCommand(),
    ExitCommand(),
    CreateWorkspaceCommand(),
    OpenWorkspaceCommand(),
    ListWorkspacesCommand(),
    WorkspaceCommand(),
    UploadCommand(),
    ListDocumentsCommand(),
    ArtifactsCommand(),
    AskCommand(),
    SummarizeCommand(),
    RunCommand(),
    MemoryCommand(),
    DebugRuntimeCommand(),
    DebugPlannerCommand(),
    DebugMemoryCommand(),
    DebugCapabilitiesCommand(),
    DebugKnowledgeCommand(),
]

