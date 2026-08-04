"""ResolverChain — Ordered execution of resolvers until one resolves."""

import logging
from typing import List

from jarvis.engines.assistant.resolvers.base import Resolver, ResolutionResult
from jarvis.domain.intent import Intent
from jarvis.core.capability.models import ExecutionContext

logger = logging.getLogger(__name__)


class ResolverChain:
    """Walks a chain of resolvers until one successfully resolves the intent.
    
    Chain priority (deterministic first, AI last):
    1. WorkspaceResolver
    2. ArtifactResolver
    3. KnowledgeResolver
    4. MemoryResolver
    5. CapabilityResolver
    6. AIResolver (always resolves with grounding)
    """

    def __init__(self, resolvers: List[Resolver]):
        """Initialize resolver chain.
        
        Args:
            resolvers: Ordered list of resolvers to consult
        """
        self.resolvers = resolvers
        logger.info(f"ResolverChain initialized with {len(resolvers)} resolver(s)")

    def resolve(self, intent: Intent, context: ExecutionContext) -> ResolutionResult:
        """Walk the resolver chain until one successfully resolves.
        
        Args:
            intent: The user intent to resolve
            context: Execution context
            
        Returns:
            ResolutionResult from the first resolver that can handle the intent
        """
        resolution_chain = []
        
        for resolver in self.resolvers:
            resolver_name = resolver.__class__.__name__
            
            # Check if resolver can handle this intent
            if resolver.can_resolve(intent):
                logger.info(f"ResolverChain: {resolver_name} can resolve intent")
                resolution_chain.append(resolver_name)
                
                # Attempt resolution
                result = resolver.resolve(intent, context)
                
                # Update resolution chain in result
                result = ResolutionResult(
                    resolved=result.resolved,
                    source=result.source,
                    confidence=result.confidence,
                    payload=result.payload,
                    evidence=result.evidence,
                    grounded=result.grounded,
                    execution_time_ms=result.execution_time_ms,
                    reason=result.reason,
                    resolution_chain=resolution_chain
                )
                
                if result.resolved:
                    logger.info(f"ResolverChain: {resolver_name} resolved successfully")
                    return result
                else:
                    logger.info(f"ResolverChain: {resolver_name} could not resolve, continuing chain")
            else:
                logger.debug(f"ResolverChain: {resolver_name} cannot resolve intent")
        
        # Should never reach here if AIResolver is in the chain (it always resolves)
        logger.warning("ResolverChain: No resolver could resolve the intent")
        return ResolutionResult(
            resolved=False,
            source="Unknown",
            confidence="Low",
            payload="No resolver could handle this request.",
            grounded=False,
            reason="No matching resolver in chain",
            resolution_chain=resolution_chain
        )
