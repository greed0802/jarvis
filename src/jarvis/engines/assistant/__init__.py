"""Grounded AI Assistant engine for M10.5.

Pipeline: retrieval -> provider draft -> grounding validation -> response.

Per C1.13: This package SHALL NOT import CheckMateEngine, ExecutionOutcome,
RuleSnapshot, RuleRegistry, or CheckMateRule.
"""