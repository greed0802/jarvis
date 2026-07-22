"""Jarvis Platform - Modular Intelligence Platform.

This package provides the core Jarvis platform implementation including
the Application, Platform Kernel, lifecycle management, and contract definitions.
"""

from jarvis.version import __version__
from jarvis.contracts import LifecycleAware, LifecycleState
from jarvis.core.jarvis.kernel import Kernel
from jarvis.application import Application
from jarvis.configuration import Configuration

__all__ = [
    "__version__",
    "Kernel",
    "LifecycleAware",
    "LifecycleState",
    "Application",
    "Configuration",
]