"""AIResolver — AI fallback with grounding."""

import logging
from datetime import datetime

from jarvis.engines.assistant.resolvers.base import Resolver, ResolutionResult
from jarvis.domain.intent import Intent
from jarvis.core.capability.models import ExecutionContext
from jarvis.engines.airuntime.engine import AIRuntime
from jarvis.engines.assistant.grounding import GroundingEngine

logger = logging.getLogger(__name__)


class AIResolver(Resolver):
    """AI fallback resolver with comprehensive platform grounding.
    
    This resolver should ONLY activate when deterministic resolvers cannot answer.
    It receives grounded context from the GroundingEngine before invoking AI.
    """

    def __init__(self, ai_runtime: AIRuntime, grounding_engine: GroundingEngine):
        self.ai_runtime = ai_runtime
        self.grounding_engine = grounding_engine

    def can_resolve(self, intent: Intent) -> bool:
        """AIResolver can always attempt to resolve (acts as fallback)."""
        return True

    def resolve(self, intent: Intent, context: ExecutionContext) -> ResolutionResult:
        """Resolve using AI with comprehensive platform grounding."""
        start_time = datetime.now()
        
        try:
            # Assemble grounded context from platform
            grounded_context = self.grounding_engine.assemble_context(intent, context)
            
            # Create AI request with grounding
            # NOTE: AIRuntime currently returns mocked responses
            # Future implementation will send grounded_context to real AI provider
            
            logger.info(f"AIResolver invoked with grounded context: {len(grounded_context)} chars")
            
            # For now, return a placeholder indicating AI would be invoked
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            
            return ResolutionResult(
                resolved=True,
                source="AI",
                confidence="Medium",
                payload=f"AI reasoning would be invoked here with platform grounding.\n\nGrounded Context: {len(grounded_context)} characters\n\nQuestion: {intent.goal}",
                evidence=["Platform context assembled", f"Context size: {len(grounded_context)} chars"],
                grounded=True,
                execution_time_ms=execution_time,
                reason="AI fallback invoked with platform grounding",
                resolution_chain=["AIResolver"]
            )
            
        except Exception as e:
            logger.error(f"AIResolver error: {e}")
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            return ResolutionResult(
                resolved=False,
                source="AI",
                confidence="Low",
                payload=f"Error invoking AI resolver: {str(e)}",
                grounded=False,
                execution_time_ms=execution_time,
                reason=str(e),
                resolution_chain=["AIResolver"]
            )
