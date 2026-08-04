"""WorkbenchNavigationRouter for EP-1006.

Parses raw interaction events into strongly typed NavigationIntent objects
and maps bidirectional lookup routes between Evidence, Finding, and
Grounded Chat panels.

Per AC-3: Selecting an evidence citation produces a NavigationIntent routing
          to and highlighting the target EvidenceReference.
Per AC-4: Selecting a finding produces a NavigationIntent routing to highlight
          all associated EvidenceReferences and grounded chat explanations.
Per AC-7: The router produces NavigationIntent objects; it MUST NOT mutate
          WorkbenchState or WorkbenchViewModel directly.
"""

from __future__ import annotations

from jarvis.contracts.capabilities import EvidenceReference, Finding
from jarvis.contracts.understanding import UnderstandingFinding
from jarvis.contracts.assistant import AssistantResponse
from jarvis.presentation.navigation import (
    NavigationAction,
    NavigationIntent,
    NavigationOrigin,
)

class WorkbenchNavigationRouter:
    """Bidirectional navigation router for the integrated workbench.

    Maps user interaction events to strongly-typed NavigationIntent objects
    that carry full routing context. Supports three primary bidirectional
    navigation axes:

    1. Evidence -> Finding: clicking evidence highlights linked findings.
    2. Finding -> Evidence: clicking a finding highlights all linked evidence.
    3. Citation -> Evidence/Finding: clicking a chat citation navigates to source.

    The router maintains read-only indexes built from domain contracts at
    construction time. Index rebuilding requires a new router instance.

    Per AC-3/AC-4: Bidirectional routing is index-based (O(1) lookup).
    Per AC-7: The router NEVER writes to WorkbenchState or WorkbenchViewModel.
    """

    def __init__(
        self,
        findings: list[Finding] | None = None,
        evidence_items: list[EvidenceReference] | None = None,
        understanding_findings: list[UnderstandingFinding] | None = None,
        chat_responses: list[AssistantResponse] | None = None,
    ) -> None:
        """Initialize the router with current domain contract collections."""
        self._findings: list[Finding] = findings or []
        self._evidence_items: list[EvidenceReference] = evidence_items or []
        self._understanding_findings: list[UnderstandingFinding] = understanding_findings or []
        self._chat_responses: list[AssistantResponse] = chat_responses or []

        # Bidirectional indexes built at construction time
        self._evidence_to_findings: dict[str, list[str]] = {}
        self._finding_to_evidence: dict[str, list[str]] = {}
        self._citation_to_evidence: dict[str, str] = {}
        self._citation_to_finding: dict[str, str] = {}
        self._build_indexes()

    def _build_indexes(self) -> None:
        """Build bidirectional lookup indexes from current domain contracts."""
        # Finding -> Evidence and Evidence -> Finding
        for finding in self._findings:
            finding_id = finding.rule_id
            evidence_ids: list[str] = []
            for ev_ref in finding.evidence:
                eid = ev_ref.evidence_id
                evidence_ids.append(eid)
                if eid not in self._evidence_to_findings:
                    self._evidence_to_findings[eid] = []
                if finding_id not in self._evidence_to_findings[eid]:
                    self._evidence_to_findings[eid].append(finding_id)
            self._finding_to_evidence[finding_id] = evidence_ids

        # Citation -> Evidence (from AssistantResponse.cited_evidence)
        for response in self._chat_responses:
            for ev_ref in response.cited_evidence:
                eid = ev_ref.evidence_id
                self._citation_to_evidence[eid] = eid
            # Map response_id -> first finding for chat routing
            if response.cited_evidence and self._findings:
                first_eid = response.cited_evidence[0].evidence_id
                finding_ids = self._evidence_to_findings.get(first_eid, [])
                if finding_ids:
                    self._citation_to_finding[response.response_id] = finding_ids[0]

    def route_evidence_click(
        self,
        evidence_id: str,
        origin: NavigationOrigin = NavigationOrigin.EVIDENCE_VIEWER,
    ) -> NavigationIntent:
        """Produce NavigationIntent for evidence panel click.

        Per AC-3: Evidence selection routes to and highlights the target evidence,
        carrying linked finding_ids as metadata.
        """
        linked_finding_ids = self._evidence_to_findings.get(evidence_id, [])
        metadata: dict[str, str] = {}
        if linked_finding_ids:
            metadata["linked_finding_ids"] = ",".join(linked_finding_ids)
        return NavigationIntent(
            action=NavigationAction.SELECT_EVIDENCE,
            target_id=evidence_id,
            origin=origin,
            metadata=metadata,
        )

    def route_finding_click(
        self,
        finding_id: str,
        origin: NavigationOrigin = NavigationOrigin.INSPECTOR,
    ) -> NavigationIntent:
        """Produce NavigationIntent for finding inspector click.

        Per AC-4: Finding selection routes to and highlights all associated
        EvidenceReferences, carrying linked evidence_ids as metadata.
        """
        linked_evidence_ids = self._finding_to_evidence.get(finding_id, [])
        metadata: dict[str, str] = {}
        if linked_evidence_ids:
            metadata["linked_evidence_ids"] = ",".join(linked_evidence_ids)
        return NavigationIntent(
            action=NavigationAction.SELECT_FINDING,
            target_id=finding_id,
            origin=origin,
            metadata=metadata,
        )

    def route_citation_click(
        self,
        citation_id: str,
        origin: NavigationOrigin = NavigationOrigin.GROUNDED_CHAT,
    ) -> NavigationIntent:
        """Produce NavigationIntent for grounded chat citation click.

        Maps a citation link (evidence_id) to a NavigationIntent targeting
        the source evidence reference and carrying the source finding_id
        as metadata for cross-panel highlighting.
        """
        # The citation_id is an evidence_id from AssistantResponse.cited_evidence
        resolved_evidence_id = self._citation_to_evidence.get(citation_id, citation_id)
        linked_finding_ids = self._evidence_to_findings.get(resolved_evidence_id, [])
        metadata: dict[str, str] = {}
        if linked_finding_ids:
            metadata["linked_finding_ids"] = ",".join(linked_finding_ids)
        metadata["citation_source"] = citation_id
        return NavigationIntent(
            action=NavigationAction.NAVIGATE_CITATION,
            target_id=resolved_evidence_id,
            origin=origin,
            metadata=metadata,
        )

    def route_clear(
        self,
        origin: NavigationOrigin = NavigationOrigin.INSPECTOR,
    ) -> NavigationIntent:
        """Produce NavigationIntent for deselection (clear all)."""
        return NavigationIntent(
            action=NavigationAction.CLEAR_SELECTION,
            target_id="",
            origin=origin,
            metadata={},
        )

    # -------------------------------------------------------------------------
    # Index inspection helpers (for tests / orchestrator use)
    # -------------------------------------------------------------------------

    def get_linked_findings(self, evidence_id: str) -> list[str]:
        """Return all finding_ids linked to the given evidence_id."""
        return list(self._evidence_to_findings.get(evidence_id, []))

    def get_linked_evidence(self, finding_id: str) -> list[str]:
        """Return all evidence_ids linked to the given finding_id."""
        return list(self._finding_to_evidence.get(finding_id, []))