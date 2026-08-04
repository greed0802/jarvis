"""CheckMate rule evaluation engine — M10.3.

Provides the deterministic rule evaluation engine, rule registry,
RuleSnapshot manifest, and FindingReportAssembler per ADR-0030/31/32.
"""

from __future__ import annotations

from jarvis.engines.checkmate.registry import RuleRegistry, RuleSnapshot
from jarvis.engines.checkmate.rules import (
    CheckMateRule,
    DomainCategory,
    QuantityValidationRule,
    StandardsAdherenceRule,
    ConformanceCheckRule,
    CrossReferenceCheckRule,
    DataCompletenessRule,
)
from jarvis.engines.checkmate.runner import CheckMateEngine, EngineExecutionResult
from jarvis.engines.checkmate.assembler import FindingReportAssembler

__all__ = [
    "RuleRegistry",
    "RuleSnapshot",
    "CheckMateRule",
    "DomainCategory",
    "QuantityValidationRule",
    "StandardsAdherenceRule",
    "ConformanceCheckRule",
    "CrossReferenceCheckRule",
    "DataCompletenessRule",
    "CheckMateEngine",
    "EngineExecutionResult",
    "FindingReportAssembler",
]