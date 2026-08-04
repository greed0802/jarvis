"""Workspace Assistant & Knowledge-Driven Resolution Orchestration."""

import hashlib
import logging
import os
import uuid
from datetime import datetime
from typing import Optional, Any, List

from jarvis.contracts.lifecycle import LifecycleAware
from jarvis.core.workspace.runtime import WorkspaceRuntime
from jarvis.engines.knowledge.engine import KnowledgeAcquisitionEngine
from jarvis.engines.airuntime.engine import AIRuntime
from jarvis.engines.airuntime.models import AIRequest, AIMessage
from jarvis.engines.planner.engine import IntentPlanner
from jarvis.domain.intent import Intent
from jarvis.domain.workspace import Workspace
from jarvis.domain.knowledge import KnowledgeItem
from jarvis.core.capability.runtime import CapabilityRuntime
from jarvis.core.capability.models import ExecutionContext, CapabilityInput
from jarvis.core.pipeline.engine import ExecutionPipeline
from jarvis.core.pipeline.models import PipelineContext
from jarvis.core.artifact.models import ArtifactType
from jarvis.core.artifact.repository import ArtifactRepository
from jarvis.core.memory.engine import WorkspaceMemoryService

# Import resolver architecture
from jarvis.engines.assistant.resolvers import (
    WorkspaceResolver,
    ArtifactResolver,
    KnowledgeResolver,
    MemoryResolver,
    CapabilityResolver,
    AIResolver,
    ResolverChain,
    ResolutionResult,
)
from jarvis.engines.assistant.grounding import GroundingEngine

logger = logging.getLogger(__name__)

# Legacy coordinators (will be replaced/removed as resolver architecture matures)
class ContextAssembler:
    """Combines logical elements into AI Context."""
    def __init__(self, workspace_runtime: WorkspaceRuntime):
        self.workspace_runtime = workspace_runtime

class AttachmentCoordinator:
    """Manages file ingestion routing to Knowledge Engine."""
    def __init__(self, knowledge_engine: KnowledgeAcquisitionEngine):
        self.knowledge_engine = knowledge_engine

class ToolInvocationCoordinator:
    """Routes deterministic functions."""
    pass

class ConversationManager:
    """Tracks state and mutates Session arrays natively."""
    def __init__(self, workspace_runtime: WorkspaceRuntime):
        self.workspace_runtime = workspace_runtime

class WorkspaceAssistant(LifecycleAware):
    """Knowledge-Driven Engineering Assistant.
    
    The Assistant routes user requests through a ResolverChain:
    1. WorkspaceResolver (workspace/project/session queries)
    2. ArtifactResolver (file/document queries)
    3. KnowledgeResolver (knowledge item queries)
    4. MemoryResolver (execution history queries)
    5. CapabilityResolver (capability queries and execution)
    6. AIResolver (fallback with grounding)
    
    Deterministic platform knowledge is consulted FIRST.
    AI is invoked LAST, only when deterministic systems cannot answer.
    """
    
    def __init__(
        self,
        workspace_runtime: WorkspaceRuntime,
        knowledge_engine: KnowledgeAcquisitionEngine,
        ai_runtime: AIRuntime
    ) -> None:
        self.workspace_runtime = workspace_runtime
        self.knowledge_engine = knowledge_engine
        self.ai_runtime = ai_runtime
        self.intent_planner: Optional[IntentPlanner] = None
        self.capability_runtime: Optional[CapabilityRuntime] = None
        self.execution_pipeline: Optional[ExecutionPipeline] = None
        self.memory_service: Optional[Any] = None
        self.artifact_repository: Optional[Any] = None
        self._resolver_chain: Optional[ResolverChain] = None
        
        # Legacy coordinators (for backward compatibility)
        self.context_assembler = ContextAssembler(self.workspace_runtime)
        self.attachment_coordinator = AttachmentCoordinator(self.knowledge_engine)
        self.conversation_manager = ConversationManager(self.workspace_runtime)
        self.tool_coordinator = ToolInvocationCoordinator()
        
        logger.info("WorkspaceAssistant initialized (resolver chain built lazily on first resolve())")

    def _ensure_resolver_chain(self) -> None:
        """Lazily build the resolver chain once all dependencies are wired."""
        if self._resolver_chain is not None:
            return
        
        if self.capability_runtime is None:
            raise RuntimeError("CapabilityRuntime not wired to WorkspaceAssistant")
        if self.artifact_repository is None:
            raise RuntimeError("ArtifactRepository not wired to WorkspaceAssistant")
        if self.memory_service is None:
            raise RuntimeError("WorkspaceMemoryService not wired to WorkspaceAssistant")
        
        grounding_engine = GroundingEngine(
            workspace_runtime=self.workspace_runtime,
            artifact_repository=self.artifact_repository,
            memory_service=self.memory_service,
        )
        
        self._resolver_chain = ResolverChain([
            WorkspaceResolver(self.workspace_runtime),
            ArtifactResolver(self.artifact_repository),
            KnowledgeResolver(self.workspace_runtime),
            MemoryResolver(self.memory_service),
            CapabilityResolver(self.capability_runtime),
            AIResolver(self.ai_runtime, grounding_engine),
        ])
        logger.info("ResolverChain built: 6 resolvers (deterministic first, AI last)")

    def resolve(self, question: str, session_id: str) -> ResolutionResult:
        """Resolve user request through knowledge-driven resolver chain.
        
        This is the primary entry point. Deterministic resolvers fire first;
        AI is invoked only as a last resort with full platform grounding.
        """
        logger.info(f"resolve(session={session_id}, question='{question}')")
        self._ensure_resolver_chain()
        
        try:
            intent_id = f"int-{uuid.uuid4().hex[:8]}"
            workspace = self.workspace_runtime.workspace_manager.get_active()
            workspace_id = workspace.workspace_id if workspace else "default"
            
            intent = Intent(
                intent_id=intent_id,
                context_id=session_id,
                goal=question,
                parameters={},
                semantics=None,
            )
            
            ctx = ExecutionContext(
                workspace_id=workspace_id,
                session_id=session_id,
                inputs=CapabilityInput(parameters={"question": question}),
            )
            
            return self._resolver_chain.resolve(intent, ctx)
        
        except Exception as exc:
            logger.error("WorkspaceAssistant.resolve() failed: %s", exc, exc_info=True)
            return ResolutionResult(
                resolved=False,
                source="Assistant",
                confidence="Low",
                payload=f"Resolution error: {str(exc)}",
                grounded=False,
                reason=str(exc),
                resolution_chain=["WorkspaceAssistant"],
            )

    def chat(self, question: str, session_id: str) -> str:
        """Legacy convenience wrapper – returns the payload string.
        
        DEPRECATED: prefer resolve() for full ResolutionResult metadata.
        """
        result = self.resolve(question, session_id)
        return str(result.payload)

    async def initialize(self) -> None:
        logger.info("WorkspaceAssistant initialized.")

    async def start(self) -> None:
        logger.info("WorkspaceAssistant started.")

    async def shutdown(self) -> None:
        logger.info("WorkspaceAssistant shutting down.")

    # ── Public Shell API ─────────────────────────────────────────────

    _EXTENSION_MAP: dict[str, ArtifactType] = {
        ".pdf": ArtifactType.GENERAL_DOCUMENT,
        ".xlsx": ArtifactType.BOQ,
        ".xls": ArtifactType.BOQ,
        ".csv": ArtifactType.BOQ,
        ".dwg": ArtifactType.DRAWING,
        ".dxf": ArtifactType.DRAWING,
        ".png": ArtifactType.IMAGE,
        ".jpg": ArtifactType.IMAGE,
        ".jpeg": ArtifactType.IMAGE,
        ".doc": ArtifactType.GENERAL_DOCUMENT,
        ".docx": ArtifactType.GENERAL_DOCUMENT,
        ".txt": ArtifactType.GENERAL_DOCUMENT,
        ".md": ArtifactType.GENERAL_DOCUMENT,
    }

    def create_workspace(self, name: str) -> Workspace:
        """Create a new workspace and register it with the runtime."""
        workspace_id = f"ws-{name.lower().replace(' ', '-')}"
        workspace = Workspace(
            workspace_id=workspace_id,
            name=name,
            created_at=datetime.now(),
        )
        self.workspace_runtime.workspace_manager.register(workspace)
        logger.info(f"Created workspace: {workspace_id} ({name})")
        return workspace

    def open_workspace(self, name: str) -> Optional[Workspace]:
        """Set the active workspace by name."""
        workspace_id = f"ws-{name.lower().replace(' ', '-')}"
        mgr = self.workspace_runtime.workspace_manager
        if workspace_id not in mgr._workspaces:
            return None
        mgr.set_active(workspace_id)
        logger.info(f"Activated workspace: {workspace_id}")
        return mgr.get_active()

    def list_workspaces(self) -> List[Workspace]:
        """Return all registered workspaces."""
        return list(
            self.workspace_runtime.workspace_manager._workspaces.values()
        )

    def get_active_workspace(self) -> Optional[Workspace]:
        """Return the currently active workspace, or None."""
        return self.workspace_runtime.workspace_manager.get_active()

    def upload_document(self, file_path: str) -> dict[str, Any]:
        """Validate a file, detect its type, and register it as an artifact.

        Returns a metadata dict describing what was registered.
        """
        path = os.path.abspath(file_path)
        if not os.path.isfile(path):
            raise FileNotFoundError(f"File not found: {path}")

        workspace = self.get_active_workspace()
        if workspace is None:
            raise ValueError(
                "No active workspace. Open or create a workspace first."
            )

        _, ext = os.path.splitext(path)
        artifact_type = self._EXTENSION_MAP.get(
            ext.lower(), ArtifactType.GENERAL_DOCUMENT
        )

        size_bytes = os.path.getsize(path)
        with open(path, "rb") as fh:
            content_hash = hashlib.sha256(fh.read()).hexdigest()

        if self.artifact_repository is None:
            raise RuntimeError("ArtifactRepository not available.")

        artifact = self.artifact_repository.register_artifact(
            workspace_id=workspace.workspace_id,
            name=os.path.basename(path),
            artifact_type=artifact_type,
            content_hash=content_hash,
            size_bytes=size_bytes,
            created_by="shell-user",
        )

        knowledge_item = KnowledgeItem(
            knowledge_id=f"ki-{artifact.artifact_id}",
            project_id="default",
            resource_uri=path,
            content_hash=content_hash,
            added_at=datetime.now(),
        )
        self.workspace_runtime.knowledge_registry.register(knowledge_item)

        logger.info(
            f"Uploaded document: {artifact.name} -> {artifact.artifact_id}"
        )
        return {
            "artifact_id": artifact.artifact_id,
            "name": artifact.name,
            "type": artifact_type.name,
            "size_bytes": size_bytes,
            "content_hash": content_hash[:16] + "...",
            "knowledge_id": knowledge_item.knowledge_id,
        }

    def list_documents(self) -> List[dict[str, Any]]:
        """Return all knowledge items as dicts."""
        items = self.workspace_runtime.knowledge_registry._knowledge
        return [
            {
                "knowledge_id": ki.knowledge_id,
                "project_id": ki.project_id,
                "resource_uri": ki.resource_uri,
                "added_at": ki.added_at.isoformat(),
            }
            for ki in items.values()
        ]

    def get_memory_summary(self) -> List[dict[str, Any]]:
        """Return all workspace memory entries."""
        if self.memory_service is None:
            return []
        return [
            {
                "entry_id": e.entry_id,
                "category": e.category,
                "workspace_id": e.workspace_id,
                "created_at": e.created_at.isoformat(),
            }
            for e in self.memory_service._entries.values()
        ]

    def get_artifacts_summary(self) -> List[dict[str, Any]]:
        """Return all registered artifacts."""
        if self.artifact_repository is None:
            return []
        return [
            {
                "artifact_id": a.artifact_id,
                "name": a.name,
                "type": a.artifact_type.name,
                "workspace_id": a.workspace_id,
                "versions": len(a.versions),
            }
            for a in self.artifact_repository._artifacts.values()
        ]

    def list_capabilities(self) -> List[dict[str, str]]:
        """Return all registered capability definitions."""
        if self.capability_runtime is None:
            return []
        return [
            {"name": d.name, "description": d.description}
            for d in self.capability_runtime.registry.list_all()
        ]

    def run_capability(
        self, capability_name: str, session_id: str
    ) -> dict[str, Any]:
        """Execute a named capability and return the result."""
        if self.capability_runtime is None:
            raise RuntimeError("CapabilityRuntime not available.")
        workspace = self.get_active_workspace()
        ws_id = workspace.workspace_id if workspace else "default"
        ctx = ExecutionContext(
            workspace_id=ws_id,
            session_id=session_id,
            inputs=CapabilityInput(parameters={}),
        )
        result = self.capability_runtime.execute(capability_name, ctx)
        return {"status": result.status, "output": result.output}

    def get_platform_status(self) -> dict[str, Any]:
        """Assemble a comprehensive platform status report."""
        workspace = self.get_active_workspace()
        caps = self.capability_runtime.registry.list_all() if self.capability_runtime else []
        return {
            "workspace": workspace.name if workspace else "(none)",
            "workspace_id": workspace.workspace_id if workspace else None,
            "workspaces_count": len(
                self.workspace_runtime.workspace_manager._workspaces
            ),
            "knowledge_items": len(
                self.workspace_runtime.knowledge_registry._knowledge
            ),
            "capabilities": len(caps),
            "memory_entries": (
                len(self.memory_service._entries)
                if self.memory_service
                else 0
            ),
            "artifacts": (
                len(self.artifact_repository._artifacts)
                if self.artifact_repository
                else 0
            ),
        }

