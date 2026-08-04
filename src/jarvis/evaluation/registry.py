"""Evaluation Registry for M11.0 — manages evaluator discovery and lifecycle.

Per AC-2: Registry decouples evaluator plugins from the runner.
Evaluators are registered manually and held via a dict with category grouping.
"""

from __future__ import annotations

from jarvis.evaluation.contracts import Evaluator

# =============================================================================
# EvaluationRegistry
# =============================================================================

class EvaluationRegistry:
    """Registry for evaluator plugins.

    Manages evaluator registration, retrieval, and filtering by category.
    """

    def __init__(self, evaluators: list[Evaluator] | None = None) -> None:
        """Initialize the registry with an optional list of evaluators."""
        self._evaluators: dict[str, Evaluator] = {}
        self._category_index: dict[str, list[str]] = {}
        if evaluators:
            for evaluator in evaluators:
                self.register(evaluator)

    def register(self, evaluator: Evaluator) -> None:
        """Register a single evaluator with the registry.

        Args:
            evaluator: An object satisfying the Evaluator Protocol.
        """
        eid = evaluator.evaluator_id
        self._evaluators[eid] = evaluator
        cat = evaluator.category
        if cat not in self._category_index:
            self._category_index[cat] = []
        if eid not in self._category_index[cat]:
            self._category_index[cat].append(eid)

    @property
    def evaluator_ids(self) -> list[str]:
        """Return a list of all registered evaluator IDs."""
        return list(self._evaluators.keys())

    def get(self, evaluator_id: str) -> Evaluator | None:
        """Retrieve an evaluator by its ID.

        Args:
            evaluator_id: The evaluator's unique identifier.

        Returns:
            An Evaluator or None if not found.
        """
        return self._evaluators.get(evaluator_id)

    def get_category(self, category: str) -> list[Evaluator]:
        """Return all evaluators in a specific category (EVA-1 through EVA-5).

        Args:
            category: Domain category string (e.g., 'EVA-1').

        Returns:
            List of Evaluator objects in that category.
        """
        evaluators = []
        eids = self._category_index.get(category, [])
        for eid in eids:
            if eid in self._evaluators:
                evaluators.append(self._evaluators[eid])
        return evaluators

    def get_all(self) -> list[Evaluator]:
        """Return all registered evaluators."""
        return list(self._evaluators.values())

    def get_categories(self) -> list[str]:
        """Return a list of all registered category labels."""
        return list(self._category_index.keys())