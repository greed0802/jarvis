"""GroundedAssistantService — main orchestrator for M10.5.

Coordinates the full pipeline:
  1. Question interpretation → intent + search terms
  2. Understanding retrieval → matched findings
  3. Evidence resolution → grounding context
  4. Provider draft generation → raw response
  5. Validation → public AssistantResponse

Per C1.13: This module SHALL NOT import CheckMateEngine, ExecutionOutcome,
RuleSnapshot, RuleRegistry, or CheckMateRule.

Per AC-6: Service operates identically regardless of backing GenerationProvider.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from jarvis.contracts.assistant import (
    AssistantResponse,
    DraftResponse,
    GenerationProvider,
    GroundingContext,
    GroundingStatus,
)
from jarvis.contracts.capabilities import EvidenceReference, EvidenceSourceType
from jarvis.engines.assistant.providers import MockGenerationProvider
from jarvis.engines.assistant.retrieval import (
    EvidenceRetriever,
    QuestionInterpreter,
    UnderstandingRetriever,
)
from jarvis.engines.assistant.validator import GroundingValidator
from jarvis.engines.understanding.service import ProjectUnderstandingService

# =============================================================================
# GroundedAssistantService — AC-6: Provider Interchangeability
# =============================================================================

@dataclass
class GroundedAssistantService:
    """Main orchestrator for the Grounded AI Assistant pipeline.

    Coordinates retrieval, generation, and validation to produce
    grounded, evidence-backed AssistantResponse objects.

    Per AC-6: The service operates identically regardless of the backing
    GenerationProvider implementation — just swap the provider parameter.
    """

    understanding_service: ProjectUnderstandingService = field(
        default_factory=ProjectUnderstandingService
    )
    provider: GenerationProvider = field(
        default_factory=MockGenerationProvider
    )
    interpreter: QuestionInterpreter = field(
        default_factory=QuestionInterpreter
    )
    understanding_retriever: UnderstandingRetriever = field(
        default_factory=UnderstandingRetriever
    )
    evidence_retriever: EvidenceRetriever = field(
        default_factory=EvidenceRetriever
    )
    validator: GroundingValidator = field(
        default_factory=GroundingValidator
    )

    def respond(
        self,
        query: str,
        evidence_repository=None,
    ) -> AssistantResponse:
        """Execute the full grounded assistant pipeline for a user query.

        Args:
            query: Raw user query text.
            evidence_repository: Optional EvidenceRepository for evidence lookup.

        Returns:
            Immutable AssistantResponse public contract.
        """
        # Step 1: Interpret the query
        intent, terms = self.interpreter.interpret(query)

        # Step 2: Retrieve understanding findings
        retrieved = self.understanding_retriever.retrieve(
            query=query,
            intent_category=intent,
            query_terms=terms,
        )

        # Step 3: Resolve evidence references
        evidence_refs: list[EvidenceReference] = []
        if evidence_repository is not None and retrieved.relevant_findings:
            evidence_refs = evidence_repository.list()
        else:
            # Use evidence details from findings
            for f in retrieved.relevant_findings[:3]:
                if "doc-" in f.risk_statement:
                    evidence_refs.append(
                        EvidenceReference(
                            document_id=f"doc-{f.finding_id}",
                            sheet="unknown",
                            evidence_id=f.finding_id,
                            source_type=EvidenceSourceType.COMPUTED,
                        )
                    )

        # Set up UnderstandingRetriever's service for lookups
        self.understanding_retriever.understanding_service = self.understanding_service

        ground_context = self.evidence_retriever.build_grounding(
            retrieved=retrieved, evidence_refs=evidence_refs
        )

        # Step 4: Generate draft via provider (AC-1, AC-6)
        draft = self.provider.generate_draft(ground_context)

        # Step 5: Validate and produce public response (AC-7)
        provenance_id = (
            retrieved.query_id
            if not retrieved.relevant_findings
            else retrieved.relevant_findings[0].finding_id
        )

        response = self.validator.validate(
            draft=draft,
            ground_context=ground_context,
            understanding_provenance_id=provenance_id,
        )

        return response

    def respond_unsupported(self, query: str) -> AssistantResponse:
        """Produce an explicit UNSUPPORTED response for out-of-scope queries.

        Args:
            query: Query text that could not be matched.

        Returns:
            AssistantResponse with UNSUPPORTED status.
        """
        return AssistantResponse(
            response_id=f"resp-no-match-{abs(hash(query)) & 0xFFFFFFFF:08x}",
            query_text=query,
            response_text=(
                "I could not find relevant project understanding data for"
                " your query. The query may be outside the scope of the"
                " current project analysis. Please try rephrasing or"
                " ensure project data has been imported."
            ),
            grounding_status=GroundingStatus.UNSUPPORTED,
            cited_evidence=[],
            understanding_provenance_id="",
            confidence_score=0.0,
            suggested_followups=[
                "Could you rephrase your query with more specific details?",
                "What document or project are you referencing?",
            ],
        )