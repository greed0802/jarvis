"""Tests for Milestone 4 - Runtime Assembly.

Verifies:
- successful lifecycle
- component registration
- initialize()
- start()
- shutdown()
- invalid registration
- initialization failure
- startup failure
"""

import pytest

from jarvis.configuration import Configuration
from jarvis.contracts.lifecycle import LifecycleState
from jarvis.core.jarvis.kernel import Kernel
from jarvis.application import Application
from jarvis.services import LoggingService


class FailingInitService:
    """Test double that fails during initialization."""

    def __init__(self) -> None:
        self._state = LifecycleState.UNINITIALIZED

    @property
    def state(self) -> LifecycleState:
        return self._state

    async def initialize(self) -> None:
        self._state = LifecycleState.INITIALIZING
        raise RuntimeError("Initialization failed")

    async def start(self) -> None:
        self._state = LifecycleState.RUNNING

    async def shutdown(self) -> None:
        self._state = LifecycleState.SHUTDOWN


class FailingStartService:
    """Test double that fails during startup."""

    def __init__(self) -> None:
        self._state = LifecycleState.UNINITIALIZED

    @property
    def state(self) -> LifecycleState:
        return self._state

    async def initialize(self) -> None:
        self._state = LifecycleState.READY

    async def start(self) -> None:
        raise RuntimeError("Start failed")

    async def shutdown(self) -> None:
        self._state = LifecycleState.SHUTDOWN


class TestLoggingServiceLifecycle:
    """Test LoggingService lifecycle behavior."""

    def test_initial_state(self) -> None:
        """LoggingService starts in UNINITIALIZED state."""
        config = Configuration()
        service = LoggingService(config)
        assert service.state == LifecycleState.UNINITIALIZED

    def test_logger_property_returns_logger(self) -> None:
        """LoggingService provides logger property."""
        config = Configuration()
        service = LoggingService(config)
        assert service.logger is not None

    @pytest.mark.asyncio
    async def test_successful_initialize(self) -> None:
        """LoggingService initializes successfully."""
        config = Configuration()
        service = LoggingService(config)

        await service.initialize()

        assert service.state == LifecycleState.READY

    @pytest.mark.asyncio
    async def test_successful_start(self) -> None:
        """LoggingService starts successfully after initialization."""
        config = Configuration()
        service = LoggingService(config)

        await service.initialize()
        await service.start()

        assert service.state == LifecycleState.RUNNING

    @pytest.mark.asyncio
    async def test_successful_shutdown(self) -> None:
        """LoggingService shuts down successfully."""
        config = Configuration()
        service = LoggingService(config)

        await service.initialize()
        await service.start()
        await service.shutdown()

        assert service.state == LifecycleState.SHUTDOWN


class TestKernelLifecycle:
    """Test Platform Kernel lifecycle management."""

    @pytest.mark.asyncio
    async def test_kernel_initial_state(self) -> None:
        """Kernel starts in UNINITIALIZED state."""
        kernel = Kernel()
        assert kernel.state == LifecycleState.UNINITIALIZED

    @pytest.mark.asyncio
    async def test_successful_lifecycle(self) -> None:
        """Kernel drives components through complete lifecycle."""
        config = Configuration()
        kernel = Kernel(config)
        service = LoggingService(config)
        kernel.register_component(service)

        await kernel.initialize()
        assert kernel.state == LifecycleState.READY
        assert service.state == LifecycleState.READY

        await kernel.start()
        assert kernel.state == LifecycleState.RUNNING
        assert service.state == LifecycleState.RUNNING

        await kernel.shutdown()
        assert kernel.state == LifecycleState.SHUTDOWN
        assert service.state == LifecycleState.SHUTDOWN

    def test_register_component_before_initialization(self) -> None:
        """Components can be registered in UNINITIALIZED state."""
        kernel = Kernel()
        service = LoggingService(Configuration())

        kernel.register_component(service)

        assert len(kernel._components) == 1

    def test_register_after_initialize_raises(self) -> None:
        """Registration after initialization begins is rejected."""
        kernel = Kernel()
        service = LoggingService(Configuration())
        kernel.register_component(service)

        # Simulate entering INITIALIZING state
        kernel._state = LifecycleState.INITIALIZING

        with pytest.raises(RuntimeError, match="Cannot register components after lifecycle"):
            kernel.register_component(LoggingService(Configuration()))

    def test_register_after_ready_raises(self) -> None:
        """Registration after initialization is complete is rejected."""
        kernel = Kernel()
        service = LoggingService(Configuration())
        kernel.register_component(service)

        # Simulate completing initialization
        kernel._state = LifecycleState.READY

        with pytest.raises(RuntimeError, match="Cannot register components after lifecycle"):
            kernel.register_component(LoggingService(Configuration()))

    def test_register_after_running_raises(self) -> None:
        """Registration after startup is rejected."""
        kernel = Kernel()
        service = LoggingService(Configuration())
        kernel.register_component(service)

        # Simulate running state
        kernel._state = LifecycleState.RUNNING

        with pytest.raises(RuntimeError, match="Cannot register components after lifecycle"):
            kernel.register_component(LoggingService(Configuration()))

    @pytest.mark.asyncio
    async def test_initialize_failure_transitions_to_shutdown(self) -> None:
        """Initialization failure transitions platform to SHUTDOWN."""
        kernel = Kernel()
        kernel.register_component(FailingInitService())

        with pytest.raises(RuntimeError, match="Failed to initialize"):
            await kernel.initialize()

        assert kernel.state == LifecycleState.SHUTDOWN

    @pytest.mark.asyncio
    async def test_start_failure_triggers_emergency_shutdown(self) -> None:
        """Startup failure triggers emergency shutdown of started components."""
        kernel = Kernel()
        good_service = LoggingService(Configuration())
        failing_service = FailingStartService()

        kernel.register_component(good_service)
        kernel.register_component(failing_service)

        await kernel.initialize()
        assert kernel.state == LifecycleState.READY

        with pytest.raises(RuntimeError, match="Failed to start"):
            await kernel.start()

        assert kernel.state == LifecycleState.SHUTDOWN
        assert good_service.state == LifecycleState.SHUTDOWN


class TestApplicationLifecycle:
    """Test Application as Composition Root."""

    def test_application_creates_kernel(self) -> None:
        """Application creates Kernel as composition root."""
        app = Application()
        assert app.kernel is not None
        assert isinstance(app.kernel, Kernel)

    def test_application_creates_logging_service(self) -> None:
        """Application creates LoggingService and registers it."""
        app = Application()
        assert app.logging_service is not None
        assert isinstance(app.logging_service, LoggingService)

    def test_logging_service_registered_with_kernel(self) -> None:
        """LoggingService is registered with the Kernel."""
        app = Application()

        # The logging service should be in the kernel's components
        component_types = [type(c).__name__ for c in app.kernel._components]
        assert "LoggingService" in component_types

    @pytest.mark.asyncio
    async def test_application_full_lifecycle(self) -> None:
        """Application orchestrates complete lifecycle."""
        app = Application()

        await app.initialize()
        assert app.state == LifecycleState.READY

        await app.start()
        assert app.state == LifecycleState.RUNNING

        await app.shutdown()
        assert app.state == LifecycleState.SHUTDOWN

    @pytest.mark.asyncio
    async def test_application_uses_config_for_logging_service(self) -> None:
        """LoggingService receives configuration from Application."""
        config = Configuration(log_level="DEBUG")
        app = Application(config)

        # Verify the logging service was created with the configuration
        assert app.logging_service._config.log_level == "DEBUG"