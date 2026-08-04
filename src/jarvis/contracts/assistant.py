"""Grounded AI Assistant public and internal contracts for M10.5.

Defines the public AssistantResponse contract alongside internal contracts
(RetrievedContext, GroundingContext, DraftResponse) and the GenerationProvider
protocol.

Architecture conformance: ADR-0030 (C1.1, C1.3), ADR-0031 (C1.13, C1.14, C1.15),
ADR-0032 (C1.4, C1.9, C1.11).

Strict boundary: This module SHALL NOT import ExecutionOutcome, CheckMateEngine,
RuleSnapshot, RuleRegistry, or CheckMateRule.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Protocol, runtime_checkable
from uuid import uuid4

from jarvis.contracts.capabilities import EvidenceReference
from jarvis.contracts.understanding import UnderstandingFinding


# =============================================================================
# GroundingStatus — Outcome classification for assistant responses
# =============================================================================


class GroundingStatus(StrEnum):
    """Status indicating how well a response is supported by evidence.

    FULLY_GROUNDED: All factual assertions trace to cited evidence.
    PARTIALLY_GROUNDED: Some assertions verified, some unsourced.
    UNSUPPORTED: No evidence or understanding available for the query.
    """

    FULLY_GROUNDED = "FULLY_GROUNDED"
    PARTIALLY_GROUNDED = "PARTIALLY_GROUNDED"
    UNSUPPORTED = "UNSUPPORTED"


# =============================================================================
# AssistantResponse — Public Contract (C1.15)
# =============================================================================


@dataclass(frozen=True)
class AssistantResponse:
    """Immutable public contract returned by the Grounded Assistant pipeline.

    This is the ONLY public output consumed by M10.6 (Workbench UI) and
    external integrations. All internal pipeline models are hidden behind
    this contract.

    Per C1.15: Frozen and immutable. No partial composition.
    """

    response_id: str
    query_text: str
    response_text: str
    grounding_status: GroundingStatus
    cited_evidence: list[EvidenceReference] = field(default_factory=list)
    understanding_provenance_id: str = ""
    confidence_score: float = 0.0
    suggested_followups: list[str] = field(default_factory=list)

    def __post_init__(self):
        if self.confidence_score < 0.0 or self.confidence_score > 1.0:
            raise ValueError(
                f"confidence_score must be in [0.0, 1.0], got {self.confidence_score}"
            )


# =============================================================================
# RetrievedContext — Internal Contract
# =============================================================================


@dataclass(frozen=True)
class RetrievedContext:
    """Internal contract: query interpretation + matched understanding findings.

    Produced by UnderstandingRetriever after querying ProjectUnderstandingService.
    Used by EvidenceRetriever to resolve specific evidence references.
    """

    query_id: str
    intent_category: str
    relevant_findings: list[UnderstandingFinding] = field(default_factory=list)
    query_terms: list[str] = field(default_factory=list)


# =============================================================================
# GroundingContext — Internal Contract (Grounding Firewall)
# =============================================================================


@dataclass(frozen=True)
class GroundingContext:
    """Fully resolved context passed to GenerationProvider.

    This is the grounding firewall — GenerationProvider receives ONLY this
    data structure, not raw ProjectUnderstanding or engine models.

    Contains resolved understanding findings, resolved evidence references,
    and a pre-formatted prompt payload for the provider.
    """

    context_id: str
    retrieved_context: RetrievedContext
    retrieved_evidence: list[EvidenceReference] = field(default_factory=list)
    formatted_prompt_payload: str = ""


# =============================================================================
# DraftResponse — Internal Contract
# =============================================================================


@dataclass(frozen=True)
class DraftResponse:
    """Raw output from a GenerationProvider before grounding validation.

    Contains the provider's draft text and generation metadata. This is NOT
    a public contract — GroundingValidator transforms it into AssistantResponse.
    """

    provider_name: str
    provider_version: str
    response_text: str
    generation_metadata: dict[str, str] = field(default_factory=dict)


# =============================================================================
# GenerationProvider Protocol (AC-1 — Understanding Isolation)
# =============================================================================


@runtime_checkable
class GenerationProvider(Protocol):
    """Protocol for pluggable generation providers.

    Per AC-1: Providers receive strictly GroundingContext — never raw
    ProjectUnderstanding or engine models. The grounding firewall ensures
    providers operate on verified, evidence-backed data.
    """

    @property
    def provider_name(self) -> str: ...
    @property
    def provider_version(self) -> str: ...

    def generate_draft(self, context: GroundingContext) -> DraftResponse:
        """Generate a draft response from grounded context.

        Args:
            context: Fully resolved, evidence-backed GroundingContext.
                     SHALL NOT contain raw Engine or Understanding internals.

        Returns:
            A DraftResponse containing the provider response and metadata.
        """
        ...