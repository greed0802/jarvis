"""Workspace Memory Engine."""
import logging
from datetime import datetime
from typing import Dict, List, Optional

from jarvis.contracts.lifecycle import LifecycleAware
from .models import MemoryEntry, KnowledgeGraph, KnowledgeNode, KnowledgeEdge

logger = logging.getLogger(__name__)

class WorkspaceMemoryService(LifecycleAware):
    """Manages long term execution traces and data graph artifacts."""

    def __init__(self):
        self._entries: Dict[str, MemoryEntry] = {}
        self.graph = KnowledgeGraph()

    def store_entry(self, workspace_id: str, category: str, content: dict) -> MemoryEntry:
        entry_id = f"mem-{len(self._entries) + 1}"
        entry = MemoryEntry(
            entry_id=entry_id,
            workspace_id=workspace_id,
            category=category,
            content=content,
            created_at=datetime.now()
        )
        self._entries[entry_id] = entry
        logger.info(f"WorkspaceMemory stored entry: {entry_id} [{category}]")

        # Create corresponding node in graph
        self.graph.nodes[entry_id] = KnowledgeNode(node_id=entry_id, label=category, properties=content)
        return entry

    def query(self, category: str) -> List[MemoryEntry]:
        return [e for e in self._entries.values() if e.category == category]

    async def initialize(self) -> None:
        logger.info("WorkspaceMemoryService initialized.")

    async def start(self) -> None:
        logger.info("WorkspaceMemoryService started.")

    async def shutdown(self) -> None:
        logger.info("WorkspaceMemoryService shutting down.")
