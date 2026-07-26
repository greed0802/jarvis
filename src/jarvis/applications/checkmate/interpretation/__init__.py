"""CheckMate Interpretation Engine.

Single responsibility: convert platform evidence and findings into
interpreted application state. Interpretation occurs exactly once.

This package produces pre-Presentation Model structures:
- SeverityMap
- FindingGroups
- RecommendationSet
- InterpretationStatistics
- InterpretationSummary

No Presentation Model. No rendering. No reports. No exports.

Authority:
  - EQ-0021 (Permanently Frozen)
  - Application Architecture Principles v1.0
  - IP-0004 — CheckMate Interpretation Engine
"""

from jarvis.applications.checkmate.interpretation.engine import (
    interpret,
)
from jarvis.applications.checkmate.interpretation.models import (
    Severity,
    SeverityInfo,
    SeverityMap,
    FindingGroup,
    FindingGroups,
    Recommendation,
    RecommendationSet,
    InterpretationStatistics,
    InterpretationSummary,
)

__all__ = [
    "interpret",
    "Severity",
    "SeverityInfo",
    "SeverityMap",
    "FindingGroup",
    "FindingGroups",
    "Recommendation",
    "RecommendationSet",
    "InterpretationStatistics",
    "InterpretationSummary",
]