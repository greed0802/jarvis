"""KnowledgeResolver — Answers knowledge-related queries."""

import logging
from datetime import datetime

from jarvis.engines.assistant.resolvers.base import Resolver, ResolutionResult
from jarvis.domain.intent import Intent
from jarvis.core.capability.models import ExecutionContext
from jarvis.core.workspace.runtime import WorkspaceRuntime

logger = logging.getLogger(__name__)


class KnowledgeResolver(Resolver):
    """Resolves knowledge-related queries using KnowledgeRegistry.
    
    Handles:
    - QUERY / Knowledge / List (e.g., "What knowledge items exist?")
    - QUERY / Knowledge / Describe (e.g., "Show registered documents")
    """

    def __init__(self, workspace_runtime: WorkspaceRuntime):
        self.workspace_runtime = workspace_runtime

    def can_resolve(self, intent: Intent) -> bool:
        """Check if this intent targets knowledge."""
        if not intent.semantics:
            # Fallback: keyword matching
            goal_lower = intent.goal.lower()
            return any(keyword in goal_lower for keyword in [
                "knowledge", "registered document", "knowledge item"
            ])
        
        return intent.semantics.target == "Knowledge"

    def resolve(self, intent: Intent, context: ExecutionContext) -> ResolutionResult:
        """Resolve knowledge queries deterministically."""
        start_time = datetime.now()
        
        try:
            result = self._list_knowledge_items(context)
            
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
                resolution_chain=["KnowledgeResolver"]
            )
            
        except Exception as e:
            logger.error(f"KnowledgeResolver error: {e}")
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            return ResolutionResult(
                resolved=False,
                source="Knowledge",
                confidence="Low",
                payload=f"Error resolving knowledge query: {str(e)}",
                grounded=True,
                execution_time_ms=execution_time,
                reason=str(e),
                resolution_chain=["KnowledgeResolver"]
            )

    def _list_knowledge_items(self, context: ExecutionContext) -> ResolutionResult:
        """List all knowledge items in the registry."""
        knowledge_items = list(self.workspace_runtime.knowledge_registry._knowledge.values())
        
        if not knowledge_items:
            return ResolutionResult(
                resolved=True,
                source="Knowledge",
                confidence="High",
                payload="No knowledge items registered.",
                grounded=True,
                reason="No knowledge items found in registry"
            )
        
        knowledge_lines = ["Registered Knowledge Items:"]
        evidence = []
        
        for item in knowledge_items:
            knowledge_lines.append(f"  - {item.title} ({item.knowledge_type})")
            evidence.append(f"{item.title} ({item.knowledge_type})")
        
        return ResolutionResult(
            resolved=True,
            source="Knowledge",
            confidence="High",
            payload="\n".join(knowledge_lines),
            evidence=evidence,
            grounded=True,
            reason=f"Found {len(knowledge_items)} knowledge item(s)"
        )
