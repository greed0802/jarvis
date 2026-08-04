"""Resolver Architecture for Knowledge-Driven Assistant."""

from .base import Resolver, ResolutionResult
from .workspace import WorkspaceResolver
from .artifact import ArtifactResolver
from .knowledge import KnowledgeResolver
from .memory import MemoryResolver
from .capability import CapabilityResolver
from .ai import AIResolver
from .chain import ResolverChain

__all__ = [
    "Resolver",
    "ResolutionResult",
    "WorkspaceResolver",
    "ArtifactResolver",
    "KnowledgeResolver",
    "MemoryResolver",
    "CapabilityResolver",
    "AIResolver",
    "ResolverChain",
]
