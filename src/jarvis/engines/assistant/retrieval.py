"""Retrieval pipeline components for M10.5 Grounded Assistant.

Contains:
- QuestionInterpreter: parses raw queries into search terms + intent.
- UnderstandingRetriever: queries ProjectUnderstandingService, produces RetrievedContext.
- EvidenceRetriever: resolves EvidenceReference from EvidenceRepository, produces GroundingContext.

Per C1.13: This module SHALL NOT import CheckMateEngine, ExecutionOutcome,
RuleSnapshot, RuleRegistry, or CheckMateRule.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from uuid import uuid4

from jarvis.contracts.assistant import GroundingContext, RetrievedContext
from jarvis.contracts.capabilities import EvidenceReference
from jarvis.contracts.understanding import UnderstandingFinding
from jarvis.engines.understanding.service import ProjectUnderstandingService

# =============================================================================
# QuestionInterpreter
# =============================================================================

@dataclass
class QuestionInterpreter:
    """Analyzes raw user query text and extracts search terms and intent."""

    def interpret(self, query: str) -> tuple[str, list[str]]:
        """Parse query text into intent category and search terms."""
        intent = self._classify_intent(query.lower())
        terms = self._extract_terms(query.lower())
        return intent, terms

    def _classify_intent(self, normalized: str) -> str:
        if any(w in normalized for w in ("measure", "estimate", "quantity", "takeoff")):
            return "measurement_query"
        if any(w in normalized for w in ("spec", "specification", "requirement")):
            return "specification_query"
        if any(w in normalized for w in ("coordinate", "alignment", "grid", "location")):
            return "coordination_query"
        if any(w in normalized for w in ("compliance", "violation", "verify", "validate")):
            return "compliance_query"
        if any(w in normalized for w in ("document", "reference", "version", "trace")):
            return "documentation_query"
        if any(w in normalized for w in ("policy", "rule", "guideline", "procedure")):
            return "policy_query"
        return "general_query"

    def _extract_terms(self, normalized: str) -> list[str]:
        words = re.findall(r"[a-z_]+", normalized)
        stopwords = {
            "the", "a", "an", "is", "are", "was", "were", "of", "in", "to",
            "for", "on", "and", "or", "not", "it", "its", "be", "has", "have",
            "what", "how", "why", "when", "where", "which", "who", "can", "does",
            "about", "this", "that", "from", "with", "by", "at", "as", "into",
        }
        return [w for w in words if w not in stopwords]


# =============================================================================
# UnderstandingRetriever
# =============================================================================

@dataclass
class UnderstandingRetriever:
    """Queries ProjectUnderstandingService for relevant findings.

    Produces RetrievedContext containing matched UnderstandingFinding records
    for the given query terms and intent.
    """

    understanding_service: ProjectUnderstandingService = field(
        default_factory=ProjectUnderstandingService
    )

    def retrieve(
        self, query: str, intent_category: str, query_terms: list[str]
    ) -> RetrievedContext:
        query_id = f"q-{uuid4().hex[:8]}"
        matched: list[UnderstandingFinding] = []

        all_records = self.understanding_service.list_all()
        for record in all_records:
            for finding in record.findings:
                for term in query_terms:
                    if term in finding.risk_statement.lower() or term in finding.remediation.lower():
                        matched.append(finding)
                        break

        return RetrievedContext(
            query_id=query_id,
            intent_category=intent_category,
            relevant_findings=matched,
            query_terms=query_terms,
        )


# =============================================================================
# EvidenceRetriever
# =============================================================================

@dataclass
class EvidenceRetriever:
    """Resolves EvidenceReference objects and builds GroundingContext.

    Consumes RetrievedContext and an evidence lookup function to resolve
    specific evidence references for the matched findings.
    """

    def build_grounding(
        self,
        retrieved: RetrievedContext,
        evidence_refs: list[EvidenceReference],
    ) -> GroundingContext:
        context_id = f"ctx-{uuid4().hex[:8]}"
        payload_lines = [f"Query Intent: {retrieved.intent_category}", ""]

        if retrieved.relevant_findings:
            payload_lines.append("Relevant Findings:")
            for f in retrieved.relevant_findings:
                payload_lines.append(
                    f"  - [{f.category}] {f.severity}: {f.risk_statement}"
                )
        else:
            payload_lines.append("No relevant findings matched.")

        payload_lines.append("")
        payload_lines.append(f"Evidence References: {len(evidence_refs)}")
        for ref in evidence_refs[:5]:
            payload_lines.append(
                f"  - {ref.document_id}/{ref.sheet}/{ref.evidence_id}"
            )

        formatted = "\n".join(payload_lines)

        return GroundingContext(
            context_id=context_id,
            retrieved_context=retrieved,
            retrieved_evidence=evidence_refs,
            formatted_prompt_payload=formatted,
        )