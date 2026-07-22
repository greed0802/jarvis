"""Platform Configuration - Strongly typed configuration for Jarvis Platform.

This is intentionally minimal per YAGNI. Only fields actively used by the platform
are included. Configuration is frozen (immutable) to prevent runtime modifications.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Configuration:
    """
    Strongly typed platform configuration.

    Holds Control Plane configuration values that affect platform behavior.
    Uses frozen=True for immutability - configuration should not change
    after platform initialization.

    Per the architecture, Configuration contains only platform settings:
    - log_level: Controls logging verbosity

    This is intentionally minimal. Additional fields will be added
    as they become necessary (YAGNI).
    """

    log_level: str = "INFO"