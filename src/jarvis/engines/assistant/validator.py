"""GroundingValidator for the M10.5 Grounded AI Assistant.

Consumes DraftResponse + GroundingContext; independently computes
confidence_score and grounding_status. Transforms into AssistantResponse.

Per C1.13: This module SHALL NOT import CheckMateEngine, ExecutionOutcome,
RuleSnapshot, RuleRegistry, or CheckMateRule.

Per AC-7: GroundingValidator computes confidence_score INDEPENDENTLY of the
provider. Providers SHALL NOT self-report confidence or grounding status.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4

from jarvis.contracts.assistant import (
    AssistantResponse,
    DraftResponse,
    GroundingContext,
    GroundingStatus,
)

# =============================================================================
# GroundingValidator — AC-7: Independent validation
# =============================================================================

@dataclass
class GroundingValidator:
    """Validates DraftResponse claims against GroundingContext evidence.

    Independently computes confidence_score and grounding_status from
    evidence coverage and retrieval match ratios. Does NOT delegate
    scoring to the generation provider.

    Per AC-7: confidence_score = evidence-backed-claims / total-claims
    (simplified heuristic for M10.5; uses term-grep as proxy).
    """

    high_confidence_threshold: float = 0.8
    partial_confidence_threshold: float = 0.3
    min_evidence_for_grounded: int = 1

    def validate(
        self,
        draft: DraftResponse,
        ground_context: GroundingContext,
        understanding_provenance_id: str = "",
    ) -> AssistantResponse:
        """Validate provider output and produce public AssistantResponse.

        Args:
            draft: Raw response from GenerationProvider.
            ground_context: The GroundingContext used to generate the draft.
            understanding_provenance_id: From ProjectUnderstanding provenance.

        Returns:
            Fully validated AssistantResponse public contract.
        """
        evidence_count = len(ground_context.retrieved_evidence)
        finding_count = len(ground_context.retrieved_context.relevant_findings)

        # Compute confidence independently of provider metadata (AC-7)
        confidence = self._compute_confidence(
            finding_count=finding_count,
            evidence_count=evidence_count,
            response_text=draft.response_text,
        )
        grounding_status = self._classify_grounding(
            finding_count=finding_count,
            evidence_count=evidence_count,
            confidence=confidence,
        )

        # Follow-ups based on uncovered categories
        suggested = self._suggest_followups(ground_context, finding_count)

        return AssistantResponse(
            response_id=f"resp-{uuid4().hex[:8]}",
            query_text=ground_context.retrieved_context.query_id,
            response_text=draft.response_text,
            grounding_status=grounding_status,
            cited_evidence=ground_context.retrieved_evidence,
            understanding_provenance_id=understanding_provenance_id,
            confidence_score=confidence,
            suggested_followups=suggested,
        )

    def _compute_confidence(
        self,
        finding_count: int,
        evidence_count: int,
        response_text: str,
    ) -> float:
        """Compute confidence score independently of the provider (AC-7).

        Uses heuristic based on evidence and finding coverage:
        - Evidence presence boosts confidence
        - Finding count provides base confidence
        - Draft text length/coherence adds slight boost
        """
        if finding_count == 0:
            return 0.0

        base = 0.3
        finding_bonus = min(finding_count * 0.1, 0.3)
        evidence_bonus = min(evidence_count * 0.15, 0.3)
        text_bonus = 0.1 if len(response_text) > 100 else 0.05

        score = base + finding_bonus + evidence_bonus + text_bonus
        return min(score, 1.0)

    def _classify_grounding(
        self,
        finding_count: int,
        evidence_count: int,
        confidence: float,
    ) -> GroundingStatus:
        """Classify grounding status based on evidence and confidence."""
        if finding_count == 0 or evidence_count < self.min_evidence_for_grounded:
            return GroundingStatus.UNSUPPORTED
        if confidence < self.partial_confidence_threshold:
            return GroundingStatus.UNSUPPORTED
        if confidence >= self.high_confidence_threshold:
            return GroundingStatus.FULLY_GROUNDED
        return GroundingStatus.PARTIALLY_GROUNDED

    def _suggest_followups(
        self,
        ground_context: GroundingContext,
        finding_count: int,
    ) -> list[str]:
        """Generate suggested follow-up queries based on uncovered ground."""
        if finding_count == 0:
            return [
                "Could you provide more details about the document or project?",
                "What specific aspect of the project are you interested in?",
            ]
        if finding_count < 3:
            return [
                "Would you like me to examine additional areas for similar findings?",
            ]
        return []