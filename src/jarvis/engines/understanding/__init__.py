"""Project Understanding domain — M10.4.

Provides the Project Understanding capability: Importer, Store, and Service
that consume FindingReport contracts and expose ProjectUnderstanding
for downstream consumers (M10.5 AI Assistant, M10.6 Workbench UI).

Strict boundary: This package SHALL NOT import CheckMateEngine,
ExecutionOutcome, RuleSnapshot, RuleRegistry, or CheckMateRule.
"""

from __future__ import annotations

from jarvis.engines.understanding.store import ProjectUnderstandingStore
from jarvis.engines.understanding.importer import ProjectUnderstandingImporter
from jarvis.engines.understanding.service import ProjectUnderstandingService

__all__ = [
    "ProjectUnderstandingStore",
    "ProjectUnderstandingImporter",
    "ProjectUnderstandingService",
]