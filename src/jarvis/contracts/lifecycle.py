"""Platform Kernel lifecycle contracts.

Defines the lifecycle interface for platform components.
This is a contract only - no implementation provided.
"""

from typing import Protocol, runtime_checkable
from enum import StrEnum


@runtime_checkable
class LifecycleAware(Protocol):
    """Protocol for components participating in platform lifecycle.
    
    Components implement these methods to receive lifecycle callbacks
    from the Platform Kernel during initialize, start, and shutdown phases.
    """

    @property
    def state(self) -> "LifecycleState":
        """Get the current lifecycle state (read-only)."""
        ...

    async def initialize(self) -> None:
        """Initialize the component. Called once during platform startup."""
        ...

    async def start(self) -> None:
        """Start the component. Called after all components are initialized."""
        ...

    async def shutdown(self) -> None:
        """Shutdown the component gracefully. Called once during platform shutdown."""
        ...


class LifecycleState(StrEnum):
    """Lifecycle state of a platform component.
    
    Uses StrEnum for natural string serialization in logging and configuration.
    """

    UNINITIALIZED = "uninitialized"
    INITIALIZING = "initializing"
    READY = "ready"
    RUNNING = "running"
    SHUTTING_DOWN = "shutting_down"
    SHUTDOWN = "shutdown"