"""CapabilityResolver — Handles capability queries and execution."""

import logging
from datetime import datetime

from jarvis.engines.assistant.resolvers.base import Resolver, ResolutionResult
from jarvis.domain.intent import Intent
from jarvis.core.capability.models import ExecutionContext
from jarvis.core.capability.runtime import CapabilityRuntime

logger = logging.getLogger(__name__)


class CapabilityResolver(Resolver):
    """Resolves capability-related queries and executes capabilities.
    
    Handles:
    - QUERY / Capability / List (e.g., "What capabilities exist?")
    - EXECUTE / Capability / Run (e.g., "Run BOQ Intelligence")
    """

    def __init__(self, capability_runtime: CapabilityRuntime):
        self.capability_runtime = capability_runtime

    def can_resolve(self, intent: Intent) -> bool:
        """Check if this intent targets capabilities."""
        if not intent.semantics:
            # Fallback: keyword matching
            goal_lower = intent.goal.lower()
            return any(keyword in goal_lower for keyword in [
                "capability", "capabilit", "run", "execute"
            ])
        
        return intent.semantics.target == "Capability"

    def resolve(self, intent: Intent, context: ExecutionContext) -> ResolutionResult:
        """Resolve capability queries or execute capabilities."""
        start_time = datetime.now()
        
        try:
            goal_lower = intent.goal.lower()
            
            # Check if this is a capability execution request
            if "run" in goal_lower or "execute" in goal_lower:
                result = self._execute_capability(intent, context)
            else:
                # List capabilities
                result = self._list_capabilities(context)
            
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
                resolution_chain=["CapabilityResolver"]
            )
            
        except Exception as e:
            logger.error(f"CapabilityResolver error: {e}")
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            return ResolutionResult(
                resolved=False,
                source="Capability",
                confidence="Low",
                payload=f"Error resolving capability query: {str(e)}",
                grounded=True,
                execution_time_ms=execution_time,
                reason=str(e),
                resolution_chain=["CapabilityResolver"]
            )

    def _list_capabilities(self, context: ExecutionContext) -> ResolutionResult:
        """List all registered capabilities."""
        capabilities = self.capability_runtime.registry.list_all()
        
        if not capabilities:
            return ResolutionResult(
                resolved=True,
                source="Capability",
                confidence="High",
                payload="No capabilities registered.",
                grounded=True,
                reason="No capabilities found in registry"
            )
        
        cap_lines = ["Registered Capabilities:"]
        evidence = []
        
        for cap in capabilities:
            cap_lines.append(f"  - {cap.name}: {cap.description}")
            evidence.append(f"{cap.name}")
        
        return ResolutionResult(
            resolved=True,
            source="Capability",
            confidence="High",
            payload="\n".join(cap_lines),
            evidence=evidence,
            grounded=True,
            reason=f"Found {len(capabilities)} capability(ies)"
        )

    def _execute_capability(self, intent: Intent, context: ExecutionContext) -> ResolutionResult:
        """Execute a capability and return results with evidence."""
        goal_words = intent.goal.lower().split()
        filtered_words = [w for w in goal_words if w not in ["run", "execute", "the"]]
        capability_name_guess = " ".join(filtered_words).title()
        
        capabilities = self.capability_runtime.registry.list_all()
        matching_cap = None
        
        for cap in capabilities:
            if capability_name_guess.lower() in cap.name.lower():
                matching_cap = cap
                break
        
        if not matching_cap:
            return ResolutionResult(
                resolved=False,
                source="Capability",
                confidence="Low",
                payload=f"No capability found matching '{capability_name_guess}'.",
                grounded=True,
                reason=f"No matching capability for '{capability_name_guess}'"
            )
        
        try:
            result = self.capability_runtime.execute(matching_cap.name, context)
            
            return ResolutionResult(
                resolved=True,
                source="Capability",
                confidence="High",
                payload=f"Capability '{matching_cap.name}' executed.\n\n{result.output}",
                evidence=[f"Capability: {matching_cap.name}", f"Status: {result.status}"],
                grounded=True,
                reason=f"Capability '{matching_cap.name}' executed"
            )
        except Exception as e:
            return ResolutionResult(
                resolved=False,
                source="Capability",
                confidence="Low",
                payload=f"Error executing '{matching_cap.name}': {str(e)}",
                grounded=True,
                reason=f"Execution failed: {str(e)}"
            )
