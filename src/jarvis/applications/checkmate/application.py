"""CheckMate Application — Composition Root and Public Entry Point.

This module contains the composition root that:
- Accepts immutable inputs
- Creates runtime objects
- Initializes application state
- Coordinates execution
- Exposes the public run() entry point

No service locator. Explicit dependency wiring only.

No business interpretation. No Presentation Model. No review workflow.

Authority:
  - EQ-0021 (Permanently Frozen)
  - Application Architecture Principles v1.0
  - IP-0003 — CheckMate Application Foundation
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

from jarvis.applications.checkmate.config import CheckMateConfig
from jarvis.applications.checkmate.state import CheckMateRuntimeState, CheckMateStatus
from jarvis.applications.checkmate.errors import (
    CheckMateError,
    ConfigurationError,
    ContractViolationError,
    ApplicationRuntimeError,
    InternalError,
)
from jarvis.applications.checkmate.result import CheckMateResult
from jarvis.parsers.costx.boq_intelligence import BOQIntelligenceResult
from jarvis.engines.validation.engine import ValidationFindings

logger = logging.getLogger(__name__)

# ============================================================================
# Required evidence fields (Evidence Contract v1.1.0)
# ============================================================================
_REQUIRED_EVIDENCE_FIELDS: frozenset[str] = frozenset({
    "row_classification",
    "section_statistics",
    "boq_statistics",
    "known_anomalies",
})

# ============================================================================
# Required findings fields (Validation Findings Contract v1.0.0)
# ============================================================================
_REQUIRED_FINDINGS_FIELDS: frozenset[str] = frozenset({
    "findings",
    "engine_version",
    "contract_version",
})


def _validate_evidence(evidence: BOQIntelligenceResult) -> None:
    """Validate that evidence satisfies the contract.

    Args:
        evidence: The BOQIntelligenceResult to validate.

    Raises:
        ContractViolationError: If evidence is missing required fields.
    """
    missing = _REQUIRED_EVIDENCE_FIELDS - set(evidence.__dict__.keys())
    if missing:
        raise ContractViolationError(
            f"Evidence missing required fields: {', '.join(sorted(missing))}"
        )


def _validate_findings(findings: ValidationFindings) -> None:
    """Validate that findings satisfy the contract.

    Args:
        findings: The ValidationFindings to validate.

    Raises:
        ContractViolationError: If findings are missing required fields.
    """
    missing = _REQUIRED_FINDINGS_FIELDS - set(findings.__dict__.keys())
    if missing:
        raise ContractViolationError(
            f"Findings missing required fields: {', '.join(sorted(missing))}"
        )


def _create_logger(config: CheckMateConfig) -> logging.Logger:
    """Create a configured logger for the application.

    Args:
        config: Application configuration.

    Returns:
        Configured logger instance.
    """
    handler = logging.StreamHandler()
    handler.setLevel(config.log_level.upper())
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    handler.setFormatter(formatter)

    app_logger = logging.getLogger("checkmate")
    app_logger.setLevel(config.log_level.upper())
    app_logger.addHandler(handler)

    return app_logger


def run(
    evidence: BOQIntelligenceResult,
    findings: ValidationFindings,
    config: CheckMateConfig | None = None,
) -> CheckMateResult:
    """Execute the CheckMate application with the given inputs.

    This is the single public entry point for the CheckMate application.
    It accepts immutable platform inputs and returns an execution result.

    Args:
        evidence: BOQ Intelligence evidence (frozen, read-only).
        findings: Validation findings (frozen, read-only).
        config: Optional application configuration. Uses defaults if None.

    Returns:
        CheckMateResult indicating successful execution or failure.

    Raises:
        ConfigurationError: If configuration is invalid.
        ContractViolationError: If inputs violate the contract.
        CheckMateRuntimeError: If a recoverable runtime error occurs.
        InternalError: If an unexpected internal failure occurs.

    Example:
        >>> result = run(evidence, findings)
        >>> result.success
        True
    """
    # ========================================================================
    # Stage 1: Composition — Create runtime objects with explicit wiring
    # ========================================================================
    resolved_config = config or CheckMateConfig()
    app_logger = _create_logger(resolved_config)
    state = CheckMateRuntimeState(config=resolved_config)

    app_logger.info("CheckMate Application Foundation v1.0")
    app_logger.info("Status: %s", state.status.value)

    # ========================================================================
    # Stage 2: Initialize — Validate configuration
    # ========================================================================
    try:
        if resolved_config.validate_inputs:
            # Configuration validation happens at dataclass creation,
            # but we verify it explicitly here as a deterministic step.
            _ = CheckMateConfig(
                log_level=resolved_config.log_level,
                validate_inputs=resolved_config.validate_inputs,
                enable_diagnostics=resolved_config.enable_diagnostics,
                max_errors=resolved_config.max_errors,
            )

        state.transition_to(CheckMateStatus.INITIALIZED)
        app_logger.info("Status: %s", state.status.value)

    except ValueError as e:
        raise ConfigurationError(str(e)) from e

    # ========================================================================
    # Stage 3: Input Validation — Validate contracts
    # ========================================================================
    try:
        if resolved_config.validate_inputs:
            _validate_evidence(evidence)
            _validate_findings(findings)

        state.has_evidence = True
        state.has_findings = True
        state.transition_to(CheckMateStatus.INPUT_READY)
        app_logger.info("Status: %s", state.status.value)

    except ContractViolationError:
        state.transition_to(CheckMateStatus.FAILED)
        raise
    except Exception as e:
        state.transition_to(CheckMateStatus.FAILED)
        raise ContractViolationError(f"Input validation failed: {e}") from e

    # ========================================================================
    # Stage 4: Execute — Run the application pipeline
    # ========================================================================
    state.started_at = datetime.now(timezone.utc)

    try:
        state.transition_to(CheckMateStatus.RUNNING)
        app_logger.info("Status: %s", state.status.value)

        # ----------------------------------------------------------------
        # IP-0004: Interpretation Engine — Convert evidence and findings
        # into interpreted application state. Interpretation occurs
        # exactly once.
        # ----------------------------------------------------------------
        from jarvis.applications.checkmate.context import ApplicationContext
        from jarvis.applications.checkmate.interpretation.engine import interpret
        from jarvis.applications.checkmate.interpretation.models import InterpretationSummary

        context = ApplicationContext(
            evidence=evidence,
            findings=findings,
            config=resolved_config,
        )
        app_logger.info("ApplicationContext created: %s", context.runtime_id)

        interpretation_summary: InterpretationSummary = interpret(context)
        app_logger.info(
            "Interpretation complete: %d findings, %d severity categories, %d recommendations",
            interpretation_summary.statistics.total_findings,
            interpretation_summary.statistics.categories,
            interpretation_summary.statistics.total_recommendations,
        )
        state.has_interpretation = True

        if resolved_config.enable_diagnostics:
            state.diagnostics["interpretation"] = {
                "total_findings": interpretation_summary.statistics.total_findings,
                "high": interpretation_summary.statistics.high_count,
                "medium": interpretation_summary.statistics.medium_count,
                "low": interpretation_summary.statistics.low_count,
                "recommendations": interpretation_summary.statistics.total_recommendations,
            }

        # ----------------------------------------------------------------
        # IP-0005: Presentation Model
        # IP-0006: Review Workflow
        # IP-0007: Reporting & Export
        # ----------------------------------------------------------------

        state.transition_to(CheckMateStatus.COMPLETE)
        app_logger.info("Status: %s", state.status.value)

    except CheckMateError:
        state.transition_to(CheckMateStatus.FAILED)
        raise
    except Exception as e:
        state.transition_to(CheckMateStatus.FAILED)
        raise InternalError(f"Unexpected internal failure: {e}") from e

    finally:
        state.completed_at = datetime.now(timezone.utc)
        elapsed = state.elapsed_seconds
        if elapsed is not None:
            app_logger.info("Execution time: %.3f seconds", elapsed)

    # ========================================================================
    # Stage 5: Return Result
    # ========================================================================
    success = state.status == CheckMateStatus.COMPLETE

    if resolved_config.enable_diagnostics:
        state.diagnostics["evidence_summary"] = {
            "row_classification": dict(evidence.row_classification),
            "boq_statistics": dict(evidence.boq_statistics),
        }
        state.diagnostics["findings_summary"] = {
            "finding_count": len(findings.findings),
            "engine_version": findings.engine_version,
        }

    return CheckMateResult(
        success=success,
        state=state,
    )