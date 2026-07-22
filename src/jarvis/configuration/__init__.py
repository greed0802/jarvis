"""Platform Configuration - Strongly typed configuration for Jarvis Platform.

This module provides the Configuration dataclass for platform settings.
Configuration is owned by the Platform Kernel and represents Control Plane information only.

Per the architecture (04_Platform_Kernel.md):
- Configuration holds platform settings (log_level, debug mode, etc.)
- It does NOT contain user data, business logic, or runtime data
- This is intentionally minimal and follows YAGNI principles
"""

from jarvis.configuration.configuration import Configuration

__all__ = ["Configuration"]