"""CheckMate Engine — deterministic rule execution runner.

Implements ADR-0032:
  - C1.5: Deterministic Non-Evaluation (UNEVALUABLE on missing evidence).
  - C1.9: Rule Determinism (same input → same output).
  - C1.12: Contract Compatibility Boundary.

Per C1.1: CheckMateEngine consumes an EvidenceRepository, not raw files.

ED-007 (Engine Execution Provenance): Engine now emits ExecutionProvenance
alongside the outcome vector. The provenance block is owned by the engine,
not post-hoc synthesized by the assembler.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from jarvis.contracts.capabilities import EvidenceRepository
from jarvis.contracts.execution import (
    ExecutionOutcome,
    ExecutionProvenance,
)
from jarvis.engines.checkmate.registry import RuleSnapshot


@dataclass
class EngineExecutionResult:
    """Result of a single engine execution run.

    Contains the outcome vector for each rule in the snapshot, alongside
    the engine-owned provenance block (ED-007).
    """

    outcomes: list[ExecutionOutcome] = field(default_factory=list)
    provenance: ExecutionProvenance | None = None


@dataclass
class CheckMateEngine:
    """Deterministic rule evaluation engine.

    Executes a frozen RuleSnapshot against an EvidenceRepository,
    producing a vector of ExecutionOutcome records (C1.7) alongside
    an ExecutionProvenance block (ED-007).

    Per C1.5, C1.9, C1.12: missing evidence or unsatisfied contract
    boundaries yield UNEVALUABLE_MISSING_EVIDENCE, not crashes.
    """

    _repository: EvidenceRepository | None = None

    def bind_evidence(self, repository: EvidenceRepository) -> None:
        """Supply the evidence repository for the engine run."""
        self._repository = repository

    def execute(self, snapshot: RuleSnapshot) -> EngineExecutionResult:
        """Execute all rules in the snapshot against the bound evidence repository.

        Args:
            snapshot: An immutable RuleSnapshot from the rule registry.

        Returns:
            EngineExecutionResult containing the outcome vector and
            engine provenance block (ED-007).

        Per C1.9: Same snapshot + same evidence = same outcome vector every time.
        Per C1.5: Missing evidence causes UNEVALUABLE, not crash.
        """
        if self._repository is None:
            raise RuntimeError(
                "Evidence repository must be bound before execution."
            )

        outcomes: list[ExecutionOutcome] = []
        for rule in snapshot.rules:
            evidence_ids = self._resolve_evidence(rule.rule_id)
            outcome = rule.evaluate(evidence_ids=evidence_ids)
            outcomes.append(outcome)

        # ED-007: Engine provenance — computed by the engine, not the assembler
        provenance = self._build_provenance(snapshot, outcomes)

        return EngineExecutionResult(outcomes=outcomes, provenance=provenance)

    def _resolve_evidence(self, rule_id: str) -> list[str]:
        """Resolve available evidence IDs for a rule.

        In the vertical slice, resolve returns all evidence record IDs
        from the repository. Production implementations would match based
        on rule domain and minimum granularity requirements.
        """
        if self._repository is None:
            return []

        all_refs = self._repository.list()
        return [ref.evidence_id for ref in all_refs]

    def _build_provenance(
        self,
        snapshot: RuleSnapshot,
        outcomes: list[ExecutionOutcome],
    ) -> ExecutionProvenance:
        """Build the engine provenance block from execution context (ED-007).

        Computes execution_id from outcome+evidence tuple hashes,
        evidence_fingerprint from all evidence IDs referenced across outcomes,
        and embeds the snapshot content hash for replay verification.

        This is the source of truth for provenance — not the assembler.
        """
        all_rule_ids = sorted(
            {outcome.rule_id for outcome in outcomes}
        )
        all_eids = sorted(
            {eid for outcome in outcomes for eid in outcome.evidence_ids}
        )
        execution_id = f"exec-{hash(tuple(all_rule_ids))}-{hash(tuple(all_eids))}"
        evidence_fingerprint = (
            str(hash(tuple(all_eids))) if all_eids else "0"
        )

        return ExecutionProvenance(
            execution_id=execution_id,
            evidence_fingerprint=evidence_fingerprint,
            snapshot_hash=snapshot.snapshot_hash,
            capability_version=snapshot.metadata.capability_version,
        )