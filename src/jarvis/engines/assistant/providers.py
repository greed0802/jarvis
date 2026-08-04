"""Generation providers for the Grounded AI Assistant.

Implements GenerationProvider protocol implementations.

Per C1.13: This module SHALL NOT import CheckMateEngine, ExecutionOutcome,
RuleSnapshot, RuleRegistry, or CheckMateRule.
"""

from __future__ import annotations

from dataclasses import dataclass

from jarvis.contracts.assistant import DraftResponse, GenerationProvider, GroundingContext

# =============================================================================
# MockGenerationProvider — Deterministic reference implementation (AC-6)
# =============================================================================

@dataclass
class MockGenerationProvider:
    """Deterministic reference GenerationProvider for testing and offline use.

    Per AC-6: This provider generates identical output given identical
    GroundingContext, making it predictable and testable.

    Per AC-1: Receives only GroundingContext — never raw ProjectUnderstanding
    or engine models.
    """

    _provider_name: str = "mock-provider"
    _provider_version: str = "1.0.0"
    seed_text: str = "Based on the provided context, "

    @property
    def provider_name(self) -> str:
        return self._provider_name

    @property
    def provider_version(self) -> str:
        return self._provider_version

    def generate_draft(self, context: GroundingContext) -> DraftResponse:
        count = len(context.retrieved_context.relevant_findings)
        evidence_count = len(context.retrieved_evidence)

        if count == 0:
            response = (
                "I could not find any relevant findings in the project "
                "understanding database for this query. Please check if "
                "the project has been analyzed or rephrase your query."
            )
        else:
            parts = [f"{self.seed_text}I found {count} relevant finding(s)"]
            if evidence_count > 0:
                parts.append(f" supported by {evidence_count} evidence reference(s).")
            else:
                parts.append(". No direct evidence was located for these findings.")

            parts.append("\n\nSummary of findings:")
            for f in context.retrieved_context.relevant_findings[:3]:
                parts.append(
                    f"\n  - [{f.category.value}] {f.severity}: {f.risk_statement}"
                    f" — {f.remediation}"
                )
            response = "".join(parts)

        return DraftResponse(
            provider_name=self._provider_name,
            provider_version=self._provider_version,
            response_text=response,
            generation_metadata={
                "findings_matched": str(count),
                "evidence_available": str(evidence_count),
                "generator": "mock",
            },
        )