"""Application - Composition Root for Jarvis Platform.

The Application class serves as the composition root and entry point orchestrator.
It manages the complete platform lifecycle: create -> initialize -> start -> shutdown.

This layer separates concerns:
- Application handles process lifecycle and orchestration
- Kernel remains pure Control Plane (runtime coordinator)
"""

from __future__ import annotations

import asyncio
import logging
import signal

from jarvis.configuration import Configuration
from jarvis.contracts.lifecycle import LifecycleState
from jarvis.core.jarvis.kernel import Kernel
from jarvis.core.workspace.runtime import WorkspaceRuntime
from jarvis.engines.knowledge.engine import KnowledgeAcquisitionEngine
from jarvis.engines.airuntime.engine import AIRuntime
from jarvis.engines.assistant.orchestrator import WorkspaceAssistant
from jarvis.core.capability.runtime import CapabilityRuntime
from jarvis.core.capability.reference import BOQIntelligenceCapability
from jarvis.engines.planner.engine import IntentPlanner
from jarvis.core.pipeline.engine import ExecutionPipeline
from jarvis.core.memory.engine import WorkspaceMemoryService
from jarvis.core.artifact.repository import ArtifactRepository
from jarvis.services import LoggingService

logger = logging.getLogger(__name__)


class Application:
    """
    Application - Composition root and lifecycle orchestrator.

    The Application is responsible for:
    - Creating and owning the Kernel (composition root)
    - Creating platform services and registering them with the Kernel
    - Initializing the platform
    - Starting the platform
    - Handling graceful shutdown via signal handlers

    The Kernel remains focused on being the pure Control Plane,
    managing components and services without process-level concerns.
    """

    def __init__(self, config: Configuration | None = None) -> None:
        """
        Initialize the Application with optional configuration.

        The Application is the Composition Root. It creates platform components
        and registers them with the Kernel.

        Args:
            config: Platform configuration instance. If None, uses defaults.
        """
        self._config = config or Configuration()
        self._kernel = Kernel(config=self._config)
        self._logging_service = LoggingService(config=self._config)
        self._workspace_runtime = WorkspaceRuntime()
        self._knowledge_engine = KnowledgeAcquisitionEngine(self._workspace_runtime)
        self._ai_runtime = AIRuntime()
        self._workspace_assistant = WorkspaceAssistant(
            workspace_runtime=self._workspace_runtime,
            knowledge_engine=self._knowledge_engine,
            ai_runtime=self._ai_runtime
        )
        self._kernel.register_component(self._logging_service)
        self._kernel.register_component(self._workspace_runtime)
        self._kernel.register_component(self._knowledge_engine)
        self._kernel.register_component(self._ai_runtime)
        self._kernel.register_component(self._workspace_assistant)
        
        # CAP-0007 Capability Hookup
        self._capability_runtime = CapabilityRuntime(self._workspace_runtime)
        self._capability_runtime.registry.register(BOQIntelligenceCapability())
        self._kernel.register_component(self._capability_runtime)

        self._intent_planner = IntentPlanner(self._capability_runtime)
        self._kernel.register_component(self._intent_planner)

        # Memory, Artifact, Pipeline services
        self._memory_service = WorkspaceMemoryService()
        self._kernel.register_component(self._memory_service)

        self._artifact_repository = ArtifactRepository()
        self._kernel.register_component(self._artifact_repository)

        self._execution_pipeline = ExecutionPipeline(
            self._capability_runtime, self._memory_service, self._artifact_repository
        )
        self._kernel.register_component(self._execution_pipeline)

        # Bind back-references safely
        self._workspace_assistant.intent_planner = self._intent_planner
        self._workspace_assistant.capability_runtime = self._capability_runtime
        self._workspace_assistant.execution_pipeline = self._execution_pipeline
        self._workspace_assistant.memory_service = self._memory_service
        self._workspace_assistant.artifact_repository = self._artifact_repository
        self._shutdown_event = asyncio.Event()

    @property
    def kernel(self) -> Kernel:
        """Get the platform kernel (read-only)."""
        return self._kernel

    @property
    def logging_service(self) -> LoggingService:
        """Get the platform logging service (read-only)."""
        return self._logging_service

    @property
    def workspace_runtime(self) -> WorkspaceRuntime:
        """Get the platform workspace runtime (read-only)."""
        return self._workspace_runtime

    @property
    def knowledge_engine(self) -> KnowledgeAcquisitionEngine:
        """Get the platform knowledge runtime (read-only)."""
        return self._knowledge_engine


    @property
    def ai_runtime(self) -> AIRuntime:
        """Get the platform AI runtime (read-only)."""
        return self._ai_runtime

    @property
    def workspace_assistant(self) -> WorkspaceAssistant:
        return self._workspace_assistant

    @property
    def capability_runtime(self) -> CapabilityRuntime:
        return self._capability_runtime

    @property
    def artifact_repository(self) -> ArtifactRepository:
        return self._artifact_repository

    @property
    def memory_service(self) -> WorkspaceMemoryService:
        return self._memory_service

    @property
    def intent_planner(self) -> IntentPlanner:
        return self._intent_planner

    @property
    def execution_pipeline(self) -> ExecutionPipeline:
        return self._execution_pipeline
        
    @property
    def state(self) -> LifecycleState:
        """Get the current kernel lifecycle state (read-only)."""
        return self._kernel.state

    def _handle_shutdown(self, sig: int, frame: object) -> None:
        """Handle interrupt signal for graceful shutdown."""
        logger.info("Shutdown signal received...")
        self._shutdown_event.set()

    def _register_signal_handlers(self) -> None:
        """Register signal handlers for graceful shutdown."""
        signal.signal(signal.SIGINT, self._handle_shutdown)
        signal.signal(signal.SIGTERM, self._handle_shutdown)

    async def initialize(self) -> None:
        """
        Initialize the platform kernel.

        Transitions platform to READY state.
        """
        await self._kernel.initialize()

    async def start(self) -> None:
        """
        Start the platform kernel.

        Transitions platform to RUNNING state.
        """
        self._register_signal_handlers()
        await self._kernel.start()

    async def shutdown(self) -> None:
        """Shutdown the platform kernel gracefully."""
        await self._kernel.shutdown()

    async def run(self) -> None:
        """
        Run the complete platform lifecycle.

        This orchestrates: initialize -> start -> wait for shutdown signal -> shutdown.
        """
        try:
            await self.initialize()
            logger.info("Kernel state: %s", self._kernel.state)

            await self.start()
            logger.info("Kernel state: %s", self._kernel.state)

            # Platform is now running - wait for shutdown signal
            logger.info("Platform is running. Press Ctrl+C to shutdown.")
            await self._shutdown_event.wait()

        except Exception as e:
            logger.error("Platform error: %s", e)
            raise

        finally:
            await self.shutdown()
            logger.info("Kernel state: %s", self._kernel.state)
            logger.info("Platform shutdown complete.")