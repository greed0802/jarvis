"""Workspace Runtime Management."""

from __future__ import annotations

import logging
from typing import Dict, Optional

from jarvis.contracts.lifecycle import LifecycleAware
from jarvis.domain.workspace import Workspace
from jarvis.domain.project import Project
from jarvis.domain.session import Session
from jarvis.domain.knowledge import KnowledgeItem


logger = logging.getLogger(__name__)

class WorkspaceManager:
    """Manages Workspace immutable entities."""
    def __init__(self) -> None:
        self._workspaces: Dict[str, Workspace] = {}
        self._active_workspace_id: Optional[str] = None

    def register(self, workspace: Workspace) -> None:
        self._workspaces[workspace.workspace_id] = workspace

    def get_active(self) -> Optional[Workspace]:
        if not self._active_workspace_id:
            return None
        return self._workspaces.get(self._active_workspace_id)

    def set_active(self, workspace_id: str) -> None:
        if workspace_id in self._workspaces:
            self._active_workspace_id = workspace_id


class ProjectManager:
    """Manages Project immutable entities."""
    def __init__(self) -> None:
        self._projects: Dict[str, Project] = {}
        
    def register(self, project: Project) -> None:
        self._projects[project.project_id] = project

class KnowledgeRegistry:
    """Manages KnowledgeItem immutable entities."""
    def __init__(self) -> None:
        self._knowledge: Dict[str, KnowledgeItem] = {}
        
    def register(self, knowledge: KnowledgeItem) -> None:
        self._knowledge[knowledge.knowledge_id] = knowledge

class SessionManager:
    """Manages User Interaction Sessions."""
    def __init__(self) -> None:
        self._sessions: Dict[str, Session] = {}

    def register(self, session: Session) -> None:
        self._sessions[session.session_id] = session

    def get(self, session_id: str) -> Optional[Session]:
        return self._sessions.get(session_id)

class WorkspaceRuntime(LifecycleAware):
    """The Runtime Coordinator for the Workspace Domain."""

    def __init__(self) -> None:
        self.workspace_manager = WorkspaceManager()
        self.session_manager = SessionManager()
        self.project_manager = ProjectManager()
        self.knowledge_registry = KnowledgeRegistry()
        
    async def initialize(self) -> None:
        logger.info("WorkspaceRuntime initialized.")
        
    async def start(self) -> None:
        logger.info("WorkspaceRuntime started.")
        
    async def shutdown(self) -> None:
        logger.info("WorkspaceRuntime shutting down.")
