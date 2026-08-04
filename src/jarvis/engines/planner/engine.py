"""Intent Planner Engine."""
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from jarvis.contracts.lifecycle import LifecycleAware
from jarvis.domain.intent import Intent
from jarvis.domain.planner import Plan
from jarvis.domain.capability import CapabilityDefinition
from jarvis.core.capability.runtime import CapabilityRuntime

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class PlannerResult:
    plan: Plan
    is_valid: bool
    error: Optional[str] = None

class IntentPlanner(LifecycleAware):
    """Generates execution plans based on capability metadata."""

    def __init__(self, capability_runtime: CapabilityRuntime):
        self.capability_runtime = capability_runtime

    def _match_capabilities(self, goal: str) -> List[CapabilityDefinition]:
        """Trivial mock router logic selecting capabilities by name/description."""
        matches = []
        for cap in self.capability_runtime.registry.list_all():
             if cap.name.lower() in goal.lower() or "analyze" in goal.lower():
                 matches.append(cap)
        return matches

    def generate_plan(self, intent: Intent) -> PlannerResult:
        """Converts an intent to an execution plan matching metadata specs."""
        logger.info(f"Planning execution for Intent '{intent.goal}'")
        
        matches = self._match_capabilities(intent.goal)
        if not matches:
             return PlannerResult(
                 plan=Plan(plan_id="void", intent_id=intent.intent_id, workflow_id="none", strategy="No match found."),
                 is_valid=False,
                 error="No capabilities discovered matching the requested intent."
             )
        
        # Single-step mock plan construction
        active_cap = matches[0]
        logger.info(f"Planner matched intent to '{active_cap.name}'")

        strategy = f"EXECUTE {active_cap.name}"
        plan = Plan(plan_id=f"plan-{intent.intent_id}", intent_id=intent.intent_id, workflow_id="wf-default", strategy=strategy)
        return PlannerResult(plan=plan, is_valid=True)

    async def initialize(self) -> None:
        logger.info("IntentPlanner initialized.")

    async def start(self) -> None:
        logger.info("IntentPlanner started.")

    async def shutdown(self) -> None:
        logger.info("IntentPlanner shutting down.")
