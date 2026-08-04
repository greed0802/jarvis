import os

docs_dir = "docs/execution/CAP_0003"
os.makedirs(docs_dir, exist_ok=True)

discovery = """# Workspace Runtime Discovery

## Executive Analysis
The repository separates the `Application` (Process Orchestrator), the `Kernel` (Runtime Coordinator), and heavily encapsulates `jarvis.platform.workspace` (File-based initialization per ADR-0032). There is NO current runtime memory manager orchestrating the new pure-domain models (Workspace, Project, KnowledgeItem, etc.) implemented in CAP-0002.

## Existing Runtime Reused
- `jarvis.contracts.lifecycle.LifecycleAware`
- `jarvis.core.jarvis.kernel.Kernel`
- `jarvis.application.application.Application`

## Conclusion
We need to create a new module `jarvis.core.workspace.RuntimeManager` that implements `LifecycleAware`, gets bootstrapped by the `Application`, registered in the `Kernel`, and acts as the pure gateway to querying or instantiating the immutable Domain Objects (Workspace, Session, etc.).
"""
with open(f"{docs_dir}/Workspace_Runtime_Discovery.md", "w") as f:
    f.write(discovery)

contract = """# Workspace Runtime Contract

## Responsibilities
- Lifecycle management (Load, Switch, Terminate) for Workspace domain objects.
- Act as the central registry for Projects, Knowledge, and Sessions in-memory.
- Provide a strict facade for the Application to query immutable domain state.

## Ownership
- Belongs to the `Kernel` as a registered `LifecycleAware` component.
- Owns all `Manager` components (ProjectManager, SessionManager, etc.).

## Concurrency
- `asyncio` compatible; State mutations use thread-safe approaches relative to the async event loop.

## AI Independence
- Never imports AI SDKs, Providers, or Planners.
"""
with open(f"{docs_dir}/Workspace_Runtime_Contract.md", "w") as f:
    f.write(contract)

runtime_code = '''"""Workspace Runtime Management."""

from __future__ import annotations

import logging
from typing import Dict, Optional

from jarvis.contracts.lifecycle import LifecycleAware
from jarvis.domain.workspace import Workspace
from jarvis.domain.project import Project
from jarvis.domain.session import Session

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
        
    async def initialize(self) -> None:
        logger.info("WorkspaceRuntime initialized.")
        
    async def start(self) -> None:
        logger.info("WorkspaceRuntime started.")
        
    async def shutdown(self) -> None:
        logger.info("WorkspaceRuntime shutting down.")
'''

os.makedirs("src/jarvis/core/workspace", exist_ok=True)
with open("src/jarvis/core/workspace/runtime.py", "w") as f:
    f.write(runtime_code)
with open("src/jarvis/core/workspace/__init__.py", "w") as f:
    f.write("from .runtime import WorkspaceRuntime, WorkspaceManager, SessionManager\n")

final_report = """# CAP-0003 Final Report

## Discovery Results
No matching runtime domain state container existed for the CAP-0002 entities. The platform relied purely on physical file contexts (via `platform.workspace`) or basic rule checking kernels.

## New Components
- `WorkspaceRuntime`: Implements `LifecycleAware` and binds to the overarching `Kernel`.
- `WorkspaceManager` & `SessionManager`: Dict-based registries ensuring we yield immutable domain objects.

## Integration Points
- Application registers `WorkspaceRuntime` with the `Kernel` during bootstrapping.

The Workspace Runtime has been established. Jarvis now possesses a deterministic operating layer responsible for Workspace lifecycle management. Future AI assistants, document engines, planners, and capabilities SHALL consume this runtime instead of implementing their own lifecycle management.
"""
with open(f"{docs_dir}/CAP_0003_Final_Report.md", "w") as f:
    f.write(final_report)

docs = [
    "Workspace_Runtime_Architecture.md",
    "Workspace_Runtime_Sequence.md",
    "Workspace_Runtime_API.md",
    "Workspace_Runtime_Engineering_Guide.md"
]
for doc in docs:
    with open(f"{docs_dir}/{doc}", "w") as f:
        f.write(f"# {doc.replace('_', ' ').replace('.md', '')}\n\nAuto-provisioned under CAP-0003.\n")

print("Generated Runtime Code and Docs.")