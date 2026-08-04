"""WorkspaceResolver — Answers workspace-related queries."""

import logging
from datetime import datetime
from typing import Optional

from jarvis.engines.assistant.resolvers.base import Resolver, ResolutionResult
from jarvis.domain.intent import Intent, IntentSemantics
from jarvis.core.capability.models import ExecutionContext
from jarvis.core.workspace.runtime import WorkspaceRuntime

logger = logging.getLogger(__name__)


class WorkspaceResolver(Resolver):
    """Resolves workspace-related queries using WorkspaceRuntime.
    
    Handles:
    - QUERY / Workspace / Describe (e.g., "What workspace am I in?")
    - QUERY / Workspace / List (e.g., "List workspaces")
    - QUERY / Project / Describe (e.g., "What project am I working on?")
    - QUERY / Session / Describe (e.g., "What session is active?")
    """

    def __init__(self, workspace_runtime: WorkspaceRuntime):
        self.workspace_runtime = workspace_runtime

    def can_resolve(self, intent: Intent) -> bool:
        """Check if this intent targets workspace domain."""
        if not intent.semantics:
            # Fallback: keyword matching for unclassified intents
            goal_lower = intent.goal.lower()
            return any(keyword in goal_lower for keyword in [
                "workspace", "project", "session", "working on"
            ])
        
        # Semantic matching
        return intent.semantics.target in ["Workspace", "Project", "Session"]

    def resolve(self, intent: Intent, context: ExecutionContext) -> ResolutionResult:
        """Resolve workspace queries deterministically."""
        start_time = datetime.now()
        
        try:
            # Determine what's being asked
            goal_lower = intent.goal.lower()
            
            if "workspace" in goal_lower:
                result = self._resolve_workspace_query(intent, context)
            elif "project" in goal_lower:
                result = self._resolve_project_query(intent, context)
            elif "session" in goal_lower:
                result = self._resolve_session_query(intent, context)
            else:
                # Generic workspace context
                result = self._resolve_workspace_context(intent, context)
            
            # Add execution timing
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            return ResolutionResult(
                resolved=result.resolved,
                source=result.source,
                confidence=result.confidence,
                payload=result.payload,
                evidence=result.evidence,
                grounded=result.grounded,
                execution_time_ms=execution_time,
                reason=result.reason,
                resolution_chain=["WorkspaceResolver"]
            )
            
        except Exception as e:
            logger.error(f"WorkspaceResolver error: {e}")
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            return ResolutionResult(
                resolved=False,
                source="Workspace",
                confidence="Low",
                payload=f"Error resolving workspace query: {str(e)}",
                grounded=True,
                execution_time_ms=execution_time,
                reason=str(e),
                resolution_chain=["WorkspaceResolver"]
            )

    def _resolve_workspace_query(self, intent: Intent, context: ExecutionContext) -> ResolutionResult:
        """Answer questions about the active workspace."""
        workspace = self.workspace_runtime.workspace_manager.get_active()
        
        if not workspace:
            return ResolutionResult(
                resolved=True,
                source="Workspace",
                confidence="High",
                payload="No active workspace. Create one with 'create-workspace <name>'.",
                grounded=True,
                reason="No active workspace found"
            )
        
        return ResolutionResult(
            resolved=True,
            source="Workspace",
            confidence="High",
            payload=f"Active workspace: {workspace.name} (ID: {workspace.workspace_id})",
            evidence=[f"Workspace: {workspace.name}", f"Created: {workspace.created_at}"],
            grounded=True,
            reason="Active workspace retrieved"
        )

    def _resolve_project_query(self, intent: Intent, context: ExecutionContext) -> ResolutionResult:
        """Answer questions about the active project."""
        project = self.workspace_runtime.project_manager.get_active()
        
        if not project:
            return ResolutionResult(
                resolved=True,
                source="Workspace",
                confidence="High",
                payload="No active project. Create one with 'create-project <name>'.",
                grounded=True,
                reason="No active project found"
            )
        
        return ResolutionResult(
            resolved=True,
            source="Workspace",
            confidence="High",
            payload=f"Active project: {project.name} (ID: {project.project_id})",
            evidence=[f"Project: {project.name}", f"Type: {project.project_type}"],
            grounded=True,
            reason="Active project retrieved"
        )

    def _resolve_session_query(self, intent: Intent, context: ExecutionContext) -> ResolutionResult:
        """Answer questions about the active session."""
        session = self.workspace_runtime.session_manager.get_active()
        
        if not session:
            return ResolutionResult(
                resolved=True,
                source="Workspace",
                confidence="High",
                payload="No active session.",
                grounded=True,
                reason="No active session found"
            )
        
        return ResolutionResult(
            resolved=True,
            source="Workspace",
            confidence="High",
            payload=f"Active session: {session.session_id}",
            evidence=[f"Session: {session.session_id}"],
            grounded=True,
            reason="Active session retrieved"
        )

    def _resolve_workspace_context(self, intent: Intent, context: ExecutionContext) -> ResolutionResult:
        """Provide comprehensive workspace context."""
        workspace = self.workspace_runtime.workspace_manager.get_active()
        project = self.workspace_runtime.project_manager.get_active()
        session = self.workspace_runtime.session_manager.get_active()
        
        context_lines = ["Workspace Context:"]
        evidence = []
        
        if workspace:
            context_lines.append(f"  Workspace: {workspace.name}")
            evidence.append(f"Workspace: {workspace.name}")
        else:
            context_lines.append("  Workspace: None")
        
        if project:
            context_lines.append(f"  Project: {project.name} ({project.project_type})")
            evidence.append(f"Project: {project.name}")
        else:
            context_lines.append("  Project: None")
        
        if session:
            context_lines.append(f"  Session: {session.session_id}")
            evidence.append(f"Session: {session.session_id}")
        else:
            context_lines.append("  Session: None")
        
        return ResolutionResult(
            resolved=True,
            source="Workspace",
            confidence="High",
            payload="\n".join(context_lines),
            evidence=evidence if evidence else None,
            grounded=True,
            reason="Workspace context assembled"
        )
