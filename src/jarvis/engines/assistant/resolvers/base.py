"""Base Resolver Contract and ResolutionResult."""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional, List
from datetime import datetime

from jarvis.domain.intent import Intent
from jarvis.core.capability.models import ExecutionContext


@dataclass(frozen=True)
class ResolutionResult:
    """Universal response contract returned by every resolver.
    
    Provides:
    - resolved: Whether the resolver successfully handled the intent
    - source: Which resolver or platform component answered
    - confidence: How confident the resolver is in the answer
    - payload: The actual answer content
    - evidence: Optional supporting evidence (e.g., from capabilities)
    - grounded: Whether the answer is grounded in platform knowledge
    - execution_time_ms: How long resolution took
    - reason: Optional explanation of why resolution succeeded/failed
    - resolution_chain: Resolvers consulted before this one
    """
    resolved: bool
    source: str  # "Workspace", "Artifact", "Knowledge", "Memory", "Capability", "AI"
    confidence: str  # "High", "Medium", "Low"
    payload: Any
    evidence: Optional[List[str]] = None
    grounded: bool = True
    execution_time_ms: Optional[float] = None
    reason: Optional[str] = None
    resolution_chain: List[str] = field(default_factory=list)


class Resolver(ABC):
    """Base contract for all resolvers.
    
    Constitutional Rules:
    1. Resolvers SHALL be read-only unless intent is explicitly mutating (CREATE, UPDATE, DELETE)
    2. Resolvers SHALL NEVER call each other
    3. Only IntentPlanner and ExecutionPipeline coordinate resolvers
    4. Every resolver returns ResolutionResult with attribution
    """

    @abstractmethod
    def can_resolve(self, intent: Intent) -> bool:
        """Determines if this resolver can handle the intent.
        
        Args:
            intent: The user intent to evaluate
            
        Returns:
            True if this resolver can handle the intent, False otherwise
        """
        ...

    @abstractmethod
    def resolve(self, intent: Intent, context: ExecutionContext) -> ResolutionResult:
        """Resolves the intent and returns a result.
        
        Args:
            intent: The user intent to resolve
            context: Execution context with workspace/session info
            
        Returns:
            ResolutionResult with answer, source, confidence, and attribution
        """
        ...
