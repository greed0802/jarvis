"""Capability Execution Runtime."""
import logging
from typing import Any, Dict, Protocol, List

from jarvis.contracts.lifecycle import LifecycleAware
from jarvis.core.workspace.runtime import WorkspaceRuntime
from .models import CapabilityDefinition, CapabilityInput, CapabilityResult, ExecutionContext

logger = logging.getLogger(__name__)

class CapabilityInterface(Protocol):
    """How capabilities conform to the registry."""
    def get_definition(self) -> CapabilityDefinition: ...
    def execute(self, context: ExecutionContext) -> CapabilityResult: ...

class CapabilityRegistry:
    def __init__(self):
        self._capabilities: Dict[str, CapabilityInterface] = {}

    def register(self, capability: CapabilityInterface) -> None:
        defn = capability.get_definition()
        self._capabilities[defn.name] = capability
        logger.info(f"Registered Capability: {defn.name}")

    def get(self, name: str) -> CapabilityInterface | None:
        return self._capabilities.get(name)

    def list_all(self) -> List[CapabilityDefinition]:
        return [c.get_definition() for c in self._capabilities.values()]

class CapabilityRuntime(LifecycleAware):
    """Orchestrates Capability discovery and execution."""
    def __init__(self, workspace_runtime: WorkspaceRuntime):
        self.workspace_runtime = workspace_runtime
        self.registry = CapabilityRegistry()

    def execute(self, capability_name: str, context: ExecutionContext) -> CapabilityResult:
        capability = self.registry.get(capability_name)
        if not capability:
            raise ValueError(f"Capability '{capability_name}' not discovered.")
        
        logger.info(f"Executing capability: {capability_name}")
        return capability.execute(context)

    async def initialize(self) -> None:
        logger.info("CapabilityRuntime initialized.")

    async def start(self) -> None:
        logger.info("CapabilityRuntime started.")

    async def shutdown(self) -> None:
        logger.info("CapabilityRuntime shutting down.")
