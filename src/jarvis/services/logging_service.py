"""Platform Logging Service.

The Logging Service is a Platform Service defined in the System Blueprint.
It participates in the platform lifecycle without performing business logic.
"""

from __future__ import annotations

import logging

from jarvis.configuration import Configuration
from jarvis.contracts.lifecycle import LifecycleAware, LifecycleState

LOGGER_NAME = "jarvis"


class LoggingService(LifecycleAware):
    """Platform logging service.

    This service manages platform logging infrastructure.
    It participates in the lifecycle to configure logging during
    initialization and cleanup during shutdown.

    One platform owns exactly one LoggingService, constructed by the
    Application (Composition Root) using the platform Configuration.
    The service is then registered with the Platform Kernel, which
    manages its lifecycle.
    """

    def __init__(self, config: Configuration) -> None:
        """Initialize the logging service with platform configuration.

        Args:
            config: Platform configuration containing log_level setting.
        """
        self._state: LifecycleState = LifecycleState.UNINITIALIZED
        self._config = config
        self._logger: logging.Logger | None = None

    @property
    def state(self) -> LifecycleState:
        """Get the current lifecycle state (read-only)."""
        return self._state

    @property
    def logger(self) -> logging.Logger:
        """Get the configured platform logger.

        Future-proof property for rotating handlers, JSON logging,
        file logging, and structured logging without changing callers.
        """
        if self._logger is None:
            self._logger = logging.getLogger(LOGGER_NAME)
        return self._logger

    async def initialize(self) -> None:
        """Initialize the logging service.

        Configure logging level from Configuration.
        Called once during platform startup, in registration order.
        """
        self._state = LifecycleState.INITIALIZING
        self.logger.setLevel(self._config.log_level)
        self._state = LifecycleState.READY

    async def start(self) -> None:
        """Start the logging service.

        Called after all components are initialized, in registration order.
        """
        self._state = LifecycleState.RUNNING

    async def shutdown(self) -> None:
        """Shutdown the logging service gracefully.

        Called once during platform shutdown, in reverse registration order.
        """
        self._state = LifecycleState.SHUTTING_DOWN
        self._state = LifecycleState.SHUTDOWN