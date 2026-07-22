"""Platform Kernel - Runtime Coordinator for Jarvis Platform.

The Platform Kernel is the Control Plane of the Jarvis Platform.
It creates, manages, protects, and maintains the execution environment
for all platform components.

The Kernel does NOT perform business logic, planning, workflow execution,
or skill execution. It provides the runtime ecosystem for those components.
"""

from __future__ import annotations

import logging
from typing import Any

from jarvis.configuration import Configuration
from jarvis.contracts.lifecycle import LifecycleAware, LifecycleState

logger = logging.getLogger(__name__)


class Kernel:
    """
    Platform Kernel - central runtime coordinator.

    Manages platform lifecycle, component registration, and service provisioning.
    One Kernel exists per platform instance for its entire lifetime.
    """

    def __init__(self, config: Configuration | None = None) -> None:
        """
        Initialize the Kernel with optional configuration.

        Args:
            config: Platform configuration instance. If None, uses defaults.
        """
        self._config = config or Configuration()
        self._state: LifecycleState = LifecycleState.UNINITIALIZED
        self._components: list[LifecycleAware] = []
        self._services: dict[str, Any] = {}

    @property
    def state(self) -> LifecycleState:
        """Get the current lifecycle state (read-only)."""
        return self._state

    @property
    def is_running(self) -> bool:
        """Check if the platform is currently running."""
        return self._state == LifecycleState.RUNNING

    @property
    def config(self) -> Configuration:
        """Get platform configuration (read-only)."""
        return self._config

    def register_component(self, component: LifecycleAware) -> None:
        """
        Register a lifecycle-aware component with the platform.

        Components are initialized and started in registration order.
        Registration can only occur before initialization begins.

        Args:
            component: A component implementing LifecycleAware protocol.

        Raises:
            RuntimeError: If called after initialization has begun.
        """
        if self._state != LifecycleState.UNINITIALIZED:
            raise RuntimeError(
                f"Cannot register components after lifecycle has begun. "
                f"Current state: {self._state}"
            )
        self._components.append(component)
        logger.debug(f"Registered component: {type(component).__name__}")

    def get_service(self, name: str) -> Any:
        """
        Retrieve a registered platform service.

        Args:
            name: The service name to retrieve.

        Returns:
            The service instance.

        Raises:
            KeyError: If service is not registered.
        """
        if name not in self._services:
            raise KeyError(f"Service not found: {name}")
        return self._services[name]

    def register_service(self, name: str, service: Any) -> None:
        """
        Register a platform service.

        Services are shared runtime capabilities used by multiple
        components (e.g., Event Bus, Security Service).

        Args:
            name: The service name.
            service: The service instance.
        """
        self._services[name] = service
        logger.debug(f"Registered service: {name}")

    async def initialize(self) -> None:
        """
        Initialize the platform and all registered components.

        This transitions the platform from UNINITIALIZED to READY state.
        All registered components are initialized in order.
        """
        if self._state != LifecycleState.UNINITIALIZED:
            raise RuntimeError(
                f"Cannot initialize from state: {self._state}"
            )

        self._state = LifecycleState.INITIALIZING
        logger.info("Initializing platform kernel...")

        for component in self._components:
            try:
                await component.initialize()
            except Exception as e:
                self._state = LifecycleState.SHUTDOWN
                raise RuntimeError(
                    f"Failed to initialize component {type(component).__name__}: {e}"
                ) from e

        self._state = LifecycleState.READY
        logger.info("Platform kernel initialized successfully")

    async def start(self) -> None:
        """
        Start the platform and all initialized components.

        This transitions the platform from READY to RUNNING state.
        All components are started in order.
        """
        if self._state != LifecycleState.READY:
            raise RuntimeError(
                f"Cannot start from state: {self._state}"
            )

        self._state = LifecycleState.RUNNING
        logger.info("Starting platform kernel...")

        for component in self._components:
            try:
                await component.start()
            except Exception as e:
                # Shut down already-started components in reverse order
                for started_component in reversed(self._components):
                    try:
                        await started_component.shutdown()
                    except Exception:
                        logger.exception(
                            "Error during emergency shutdown of %s",
                            type(started_component).__name__
                        )
                self._state = LifecycleState.SHUTDOWN
                raise RuntimeError(
                    f"Failed to start component {type(component).__name__}: {e}"
                ) from e

        logger.info("Platform kernel started successfully")

    async def shutdown(self) -> None:
        """
        Shutdown the platform and all running components.

        This transitions the platform from RUNNING to SHUTDOWN state.
        Components are shut down in reverse order.
        """
        if self._state not in (
            LifecycleState.RUNNING,
            LifecycleState.READY,
        ):
            logger.warning(f"Shutdown called in unexpected state: {self._state}")
            return

        if self._state == LifecycleState.SHUTDOWN:
            return

        self._state = LifecycleState.SHUTTING_DOWN
        logger.info("Shutting down platform kernel...")

        # Shutdown in reverse order
        for component in reversed(self._components):
            try:
                await component.shutdown()
            except Exception as e:
                logger.error(
                    f"Error shutting down component {type(component).__name__}: {e}"
                )

        self._state = LifecycleState.SHUTDOWN
        logger.info("Platform kernel shutdown complete")