"""Workspace Memory Contracts."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

@dataclass(frozen=True)
class MemoryEntry:
    entry_id: str
    workspace_id: str
    category: str
    content: dict[str, Any]
    created_at: datetime

@dataclass(frozen=True)
class KnowledgeNode:
    node_id: str
    label: str
    properties: dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class KnowledgeEdge:
    source_id: str
    target_id: str
    relationship: str
    properties: dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class KnowledgeGraph:
    nodes: dict[str, KnowledgeNode] = field(default_factory=dict)
    edges: list[KnowledgeEdge] = field(default_factory=list)
