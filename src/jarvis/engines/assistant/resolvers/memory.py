"""MemoryResolver — Answers memory-related queries."""

import logging
from datetime import datetime

from jarvis.engines.assistant.resolvers.base import Resolver, ResolutionResult
from jarvis.domain.intent import Intent
from jarvis.core.capability.models import ExecutionContext
from jarvis.core.memory.engine import WorkspaceMemoryService

logger = logging.getLogger(__name__)


class MemoryResolver(Resolver):
    """Resolves memory-related queries using WorkspaceMemoryService.
    
    Handles:
    - QUERY / Memory / List (e.g., "What's in memory?")
    - QUERY / Memory / Describe (e.g., "Show execution history")
    """

    def __init__(self, memory_service: WorkspaceMemoryService):
        self.memory_service = memory_service

    def can_resolve(self, intent: Intent) -> bool:
        """Check if this intent targets memory."""
        if not intent.semantics:
            # Fallback: keyword matching
            goal_lower = intent.goal.lower()
            return any(keyword in goal_lower for keyword in [
                "memory", "history", "execution", "trace"
            ])
        
        return intent.semantics.target == "Memory"

    def resolve(self, intent: Intent, context: ExecutionContext) -> ResolutionResult:
        """Resolve memory queries deterministically."""
        start_time = datetime.now()
        
        try:
            result = self._list_memory_entries(context)
            
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
                resolution_chain=["MemoryResolver"]
            )
            
        except Exception as e:
            logger.error(f"MemoryResolver error: {e}")
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            return ResolutionResult(
                resolved=False,
                source="Memory",
                confidence="Low",
                payload=f"Error resolving memory query: {str(e)}",
                grounded=True,
                execution_time_ms=execution_time,
                reason=str(e),
                resolution_chain=["MemoryResolver"]
            )

    def _list_memory_entries(self, context: ExecutionContext) -> ResolutionResult:
        """List memory entries for the workspace."""
        workspace_id = context.workspace_id
        entries = [e for e in self.memory_service._entries.values() 
                   if e.workspace_id == workspace_id]
        
        if not entries:
            return ResolutionResult(
                resolved=True,
                source="Memory",
                confidence="High",
                payload="No memory entries stored.",
                grounded=True,
                reason="No memory entries found for workspace"
            )
        
        memory_lines = ["Workspace Memory:"]
        evidence = []
        
        for entry in entries[:10]:  # Limit to recent 10
            memory_lines.append(f"  - [{entry.category}] {entry.entry_id}")
            evidence.append(f"{entry.category}: {entry.entry_id}")
        
        if len(entries) > 10:
            memory_lines.append(f"  ... and {len(entries) - 10} more")
        
        return ResolutionResult(
            resolved=True,
            source="Memory",
            confidence="High",
            payload="\n".join(memory_lines),
            evidence=evidence,
            grounded=True,
            reason=f"Found {len(entries)} memory entry(ies)"
        )
