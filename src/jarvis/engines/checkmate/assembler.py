"""FindingReportAssembler — converts internal outcomes to public FindingReport.

Implements ADR-0031:
  - C1.7: Only FAIL outcomes generate Findings.
  - C1.13: Public contract decoupling (public FindingReport, not internal vectors).
  - C1.14: Provenance block with execution_id, evidence_fingerprint, snapshot_hash.
  - C1.15: Report completeness — single, immutable report per execution.

Per C1.3: The assembler produces ONLY FindingReport. No summary, chat, or rendering.

ED-007 (Engine Execution Provenance): Assembler now consumes the engine's
native ExecutionProvenance block rather than computing it post-hoc.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from jarvis.contracts.capabilities import (
    EvidenceReference,
    EvidenceSourceType,
    Finding,
    FindingReport,
    ReportProvenance,
    Severity,
    TelemetrySummary,
)
from jarvis.contracts.execution import (
    ExecutionOutcome,
    ExecutionOutcomeStatus,
    ExecutionProvenance,
)

# =============================================================================
# FindingReportAssembler
# =============================================================================

@dataclass
class FindingReportAssembler:
    """Builds the public FindingReport from engine outcomes and provenance.

    Sole bridge between engine internals and the capability boundary (C1.13).
    Consumers integrate against the assembled FindingReport, not ExecutionOutcome[].

    Per ED-007: Accepts engine-native ExecutionProvenance rather than computing
    provenance values from the raw outcome vector.
    """

    def assemble(
        self,
        outcomes: list[ExecutionOutcome],
        provenance: ExecutionProvenance,
    ) -> FindingReport:
        """Assemble a complete 4-tier Finding Report using engine provenance.

        - Accepts the engine's ExecutionProvenance block (ED-007).
        - Segregates telemetry: PASS, FAIL, UNEVALUABLE_MISSING_EVIDENCE counts.
        - Converts FAIL outcomes into public Finding objects with severity,
          evidence references, risk statement, and remedial guidance (C1.6).
        - Computes domain coverage percentage.

        Returns:
            Immutable FindingReport with provenance, telemetry, findings, and
            domain coverage.
        """
        # --- Provenance Block (C1.14) — sourced from engine (ED-007) ---
        report_provenance = ReportProvenance(
            execution_id=provenance.execution_id,
            evidence_fingerprint=provenance.evidence_fingerprint,
            rule_snapshot_hash=provenance.snapshot_hash,
            capability_version=provenance.capability_version,
        )

        # 2. Telemetry Summary (operational)
        total = len(outcomes)
        executed = len(
            [
                o
                for o in outcomes
                if o.status != ExecutionOutcomeStatus.UNEVALUABLE_MISSING_EVIDENCE
            ]
        )
        unevaluable = total - executed
        coverage = (executed / total * 100) if total > 0 else 0.0

        telemetry = TelemetrySummary(
            rule_count_total=total,
            rule_count_executed=executed,
            rule_count_unevaluable=unevaluable,
            execution_duration_ms=0.0,
            coverage_pct=coverage,
        )

        # 3. Actionable Findings (only FAIL => Finding) (C1.7)
        findings_data: list[Finding] = []
        for outcome in outcomes:
            if outcome.status == ExecutionOutcomeStatus.FAIL:
                ev_refs = [
                    EvidenceReference(
                        document_id=f"doc-{eid}",
                        sheet="Sheet1",
                        evidence_id=eid,
                        source_type=EvidenceSourceType.ROW,
                    )
                    for eid in outcome.evidence_ids
                ]
                finding = Finding(
                    rule_id=outcome.rule_id,
                    severity=Severity.MAJOR,
                    evidence=ev_refs,
                    risk_statement=(
                        f"Rule {outcome.rule_id} failed: {outcome.message}"
                    ),
                    remediation=(
                        f"Review and correct item flagged by rule {outcome.rule_id}. "
                        "Refer to specification and BOQ for adjustment."
                    ),
                )
                findings_data.append(finding)

        # 4. Domain Coverage
        domain_counts: dict[str, int] = {}
        for outcome in outcomes:
            domain_counts[outcome.domain_category] = (
                domain_counts.get(outcome.domain_category, 0) + 1
            )
        domain_coverage_pct: dict[str, float] = {
            domain: 0.0
            for domain in domain_counts
        }
        for outcome in outcomes:
            domain_coverage_pct[outcome.domain_category] += 1.0
        for dom in domain_coverage_pct:
            domain_coverage_pct[dom] = (
                domain_coverage_pct[dom] / total * 100.0 if total > 0 else 0.0
            )

        # Build immutable FindingReport
        report = FindingReport(
            provenance=report_provenance,
            telemetry_summary=telemetry,
            findings=findings_data,
            domain_coverage=domain_coverage_pct,
        )
        return report