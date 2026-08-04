"""GroundingEngine — Assembles comprehensive platform context for AI."""

import logging
from typing import Dict, Any

from jarvis.domain.intent import Intent
from jarvis.core.capability.models import ExecutionContext
from jarvis.core.workspace.runtime import WorkspaceRuntime
from jarvis.core.artifact.repository import ArtifactRepository
from jarvis.core.memory.engine import WorkspaceMemoryService

logger = logging.getLogger(__name__)


class GroundingEngine:
    """Assembles comprehensive platform context for AI fallback.
    
    When deterministic resolvers cannot answer, this engine collects:
    - Active workspace details
    - Registered artifacts
    - Knowledge items
    - Memory entries
    - Recent capability results
    - Conversation history (future)
    
    The assembled context grounds AI responses in platform knowledge.
    """

    def __init__(
        self,
        workspace_runtime: WorkspaceRuntime,
        artifact_repository: ArtifactRepository,
        memory_service: WorkspaceMemoryService
    ):
        self.workspace_runtime = workspace_runtime
        self.artifact_repository = artifact_repository
        self.memory_service = memory_service

    def assemble_context(self, intent: Intent, context: ExecutionContext) -> str:
        """Assemble comprehensive platform context for AI reasoning.
        
        Args:
            intent: The user intent being resolved
            context: Execution context
            
        Returns:
            Formatted context string for AI consumption
        """
        context_parts = []
        
        # 1. Workspace Context
        workspace_ctx = self._collect_workspace_context()
        if workspace_ctx:
            context_parts.append("=== WORKSPACE CONTEXT ===")
            context_parts.append(workspace_ctx)
        
        # 2. Artifact Catalog
        artifact_ctx = self._collect_artifact_context(context.workspace_id)
        if artifact_ctx:
            context_parts.append("\n=== ARTIFACT CATALOG ===")
            context_parts.append(artifact_ctx)
        
        # 3. Knowledge Registry
        knowledge_ctx = self._collect_knowledge_context()
        if knowledge_ctx:
            context_parts.append("\n=== KNOWLEDGE REGISTRY ===")
            context_parts.append(knowledge_ctx)
        
        # 4. Memory Traces
        memory_ctx = self._collect_memory_context(context.workspace_id)
        if memory_ctx:
            context_parts.append("\n=== WORKSPACE MEMORY ===")
            context_parts.append(memory_ctx)
        
        # 5. User Intent
        context_parts.append("\n=== USER INTENT ===")
        context_parts.append(f"Question: {intent.goal}")
        
        return "\n".join(context_parts)

    def _collect_workspace_context(self) -> str:
        """Collect active workspace, project, and session info."""
        workspace = self.workspace_runtime.workspace_manager.get_active()
        project = self.workspace_runtime.project_manager.get_active()
        session = self.workspace_runtime.session_manager.get_active()
        
        lines = []
        if workspace:
            lines.append(f"Workspace: {workspace.name} ({workspace.workspace_id})")
        if project:
            lines.append(f"Project: {project.name} ({project.project_type})")
        if session:
            lines.append(f"Session: {session.session_id}")
        
        return "\n".join(lines) if lines else ""

    def _collect_artifact_context(self, workspace_id: str) -> str:
        """Collect artifact catalog."""
        all_artifacts = list(self.artifact_repository._artifacts.values())
        
        if not all_artifacts:
            return ""
        
        lines = [f"Artifacts ({len(all_artifacts)}):"]
        for artifact in all_artifacts[:10]:  # Limit to recent 10
            lines.append(f"  - {artifact.name} ({artifact.artifact_type.name})")
        
        if len(all_artifacts) > 10:
            lines.append(f"  ... and {len(all_artifacts) - 10} more")
        
        return "\n".join(lines)

    def _collect_knowledge_context(self) -> str:
        """Collect knowledge registry."""
        knowledge_items = list(self.workspace_runtime.knowledge_registry._knowledge.values())
        
        if not knowledge_items:
            return ""
        
        lines = [f"Knowledge Items ({len(knowledge_items)}):"]
        for item in knowledge_items[:10]:
            lines.append(f"  - {item.title} ({item.knowledge_type})")
        
        if len(knowledge_items) > 10:
            lines.append(f"  ... and {len(knowledge_items) - 10} more")
        
        return "\n".join(lines)

    def _collect_memory_context(self, workspace_id: str) -> str:
        """Collect memory traces."""
        entries = [e for e in self.memory_service._entries.values() 
                   if e.workspace_id == workspace_id]
        
        if not entries:
            return ""
        
        lines = [f"Memory Entries ({len(entries)}):"]
        for entry in entries[:5]:  # Limit to recent 5
            lines.append(f"  - [{entry.category}] {entry.entry_id}")
        
        if len(entries) > 5:
            lines.append(f"  ... and {len(entries) - 5} more")
        
        return "\n".join(lines)
