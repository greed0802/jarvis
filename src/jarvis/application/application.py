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
        self._kernel.register_component(self._logging_service)
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