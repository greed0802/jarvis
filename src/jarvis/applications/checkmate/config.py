"""CheckMate Application Configuration.

Configuration is immutable and contains only runtime options.
No user preferences, no UI settings.

Authority:
  - EQ-0021 (Permanently Frozen)
  - Application Architecture Principles v1.0 (Principle 7 — Deterministic Applications)
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CheckMateConfig:
    """Immutable configuration for the CheckMate application.

    Contains only runtime options that affect application behavior.
    All configuration is frozen (immutable) after creation.

    Attributes:
        log_level: Logging level string (e.g., "INFO", "DEBUG", "WARNING").
        validate_inputs: If True, validate evidence and findings before processing.
        enable_diagnostics: If True, collect diagnostic information during execution.
        max_errors: Maximum number of non-fatal errors before aborting.
    """

    log_level: str = "INFO"
    validate_inputs: bool = True
    enable_diagnostics: bool = False
    max_errors: int = 10

    def __post_init__(self) -> None:
        """Validate configuration values after initialization."""
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if self.log_level.upper() not in valid_levels:
            raise ValueError(
                f"Invalid log_level: '{self.log_level}'. "
                f"Must be one of: {', '.join(sorted(valid_levels))}"
            )
        if self.max_errors < 1:
            raise ValueError(
                f"Invalid max_errors: {self.max_errors}. Must be >= 1."
            )