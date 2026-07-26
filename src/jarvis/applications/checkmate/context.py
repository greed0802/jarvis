"""CheckMate Application Context.

Immutable runtime context providing the stable boundary for the
entire CheckMate application. Replaces expanding public API signatures.

The public run() API internally creates an ApplicationContext and passes
it through the application pipeline.

No Presentation Model. No Review State. No Reports. No Exports.

Authority:
  - EQ-0021 (Permanently Frozen)
  - Application Architecture Principles v1.0
  - IP-0004 — CheckMate Interpretation Engine
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone

from jarvis.applications.checkmate.config import CheckMateConfig
from jarvis.parsers.costx.boq_intelligence import BOQIntelligenceResult
from jarvis.engines.validation.engine import ValidationFindings


_APPLICATION_VERSION: str = "0.0.1-alpha.14"


@dataclass(frozen=True)
class ApplicationContext:
    """Immutable runtime context for the CheckMate application.

    Provides the stable boundary for all application processing.
    Evidence and Findings are read-only frozen dataclasses.
    Configuration is frozen.
    Metadata is immutable.

    No Presentation Model. No Review State. No Reports. No Exports.
    No business logic. No lifecycle behavior. Pure runtime context.

    Attributes:
        evidence: BOQ Intelligence evidence (frozen, read-only).
        findings: Validation findings (frozen, read-only).
        config: Application configuration (immutable).
        runtime_id: Unique identifier for this execution instance.
        application_version: CheckMate application version.
        execution_timestamp: UTC timestamp of when the context was created.
        enable_diagnostics: Whether diagnostic data collection is enabled.
    """

    evidence: BOQIntelligenceResult
    findings: ValidationFindings
    config: CheckMateConfig = field(default_factory=CheckMateConfig)
    runtime_id: str = field(
        default_factory=lambda: str(uuid.uuid4())
    )
    application_version: str = _APPLICATION_VERSION
    execution_timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    enable_diagnostics: bool = False

    def __post_init__(self) -> None:
        """Derive diagnostics flag from config after initialization."""
        object.__setattr__(self, "enable_diagnostics", self.config.enable_diagnostics)

    def to_dict(self) -> dict:
        """Convert context to a dictionary for diagnostic/logging purposes.

        Returns:
            Dictionary representation of the context metadata (not evidence/findings).
        """
        return {
            "runtime_id": self.runtime_id,
            "application_version": self.application_version,
            "execution_timestamp": self.execution_timestamp,
            "config": {
                "log_level": self.config.log_level,
                "validate_inputs": self.config.validate_inputs,
                "enable_diagnostics": self.enable_diagnostics,
                "max_errors": self.config.max_errors,
            },
        }