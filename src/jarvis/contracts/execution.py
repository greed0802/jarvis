"""Internal execution contracts for the CheckMate rule engine.

Defines ExecutionOutcomeStatus, ExecutionOutcome, RuleSnapshotMetadata,
and ExecutionProvenance per ADR-0032 (C1.7, C1.9, C1.11).

These are INTERNAL engine models — public contracts (FindingReport, Finding)
live in capabilities.py.

Per C1.13: These models SHALL NOT propagate into the public FindingReport.

ED-007 (Engine Execution Provenance): Engine owns provenance generation.
ED-008 (Snapshot Identity vs Content Hash): snapshot_id vs hash distinction
added to RuleSnapshotMetadata.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from typing import Any


# =============================================================================
# Execution Outcome Status (C1.7 — Outcome Separation)
# =============================================================================


class ExecutionOutcomeStatus(StrEnum):
    """Telemetric outcome of a single rule evaluation.

    Per C1.7: Only FAIL outcomes MAY generate Findings.
    PASS and NOT_APPLICABLE are telemetric only.
    UNEVALUABLE_MISSING_EVIDENCE means the rule could not be evaluated
    due to missing evidence (C1.5).
    """

    PASS = "PASS"
    FAIL = "FAIL"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    UNEVALUABLE_MISSING_EVIDENCE = "UNEVALUABLE_MISSING_EVIDENCE"


# =============================================================================
# ExecutionOutcome (Internal, per C1.9 — Determinism)
# =============================================================================


@dataclass(frozen=True)
class ExecutionOutcome:
    """Immutable record of a single rule evaluation.

    This is an INTERNAL model. FindingReportAssembler converts FAIL
    outcomes to public Finding records (C1.13).
    """

    rule_id: str
    status: ExecutionOutcomeStatus
    domain_category: str
    evidence_ids: list[str] = field(default_factory=list)
    message: str = ""
    duration_ms: float = 0.0


# =============================================================================
# RuleSnapshotMetadata (C1.11 — Snapshot Sovereignty)
# =============================================================================


@dataclass(frozen=True)
class RuleSnapshotMetadata:
    """Metadata embedded in every RuleSnapshot for reproducibility (C1.14).

    Contains the ordered list of rule identifiers, versions, and contract
    versions that were active when the snapshot was captured.

    ED-008 (Snapshot Identity vs Content Hash):
    - `snapshot_id`   = persistent entity identity (constant across reruns)
    - `compute_hash()` → `snapshot_hash` = content fingerprint (SHA-256 over
      canonical JSON manifest; changes when rules/versions/capability_version
      changes)

    Use `snapshot_hash` for content integrity verification and deterministic
    replay. Use `snapshot_id` for entity identity tracking.
    """

    snapshot_id: str
    capability_version: str
    rule_ids: list[str] = field(default_factory=list)
    rule_versions: dict[str, str] = field(default_factory=dict)
    contract_versions: dict[str, str] = field(default_factory=dict)
    captured_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def compute_hash(self) -> str:
        """Compute a deterministic SHA-256 hash over the canonical JSON manifest.

        The manifest includes: capability_version, ordered rule_ids,
        rule_versions, and contract_versions. This hash is embedded in
        FindingReport.provenance.rule_snapshot_hash (C1.14).

        The snapshot_hash is a content fingerprint (ED-008). The snapshot_id
        remains unchanged across registry mutations; this hash changes.
        """
        manifest: dict[str, Any] = {
            "capability_version": self.capability_version,
            "rule_ids": sorted(self.rule_ids),
            "rule_versions": dict(sorted(self.rule_versions.items())),
            "contract_versions": dict(sorted(self.contract_versions.items())),
        }
        canonical_json = json.dumps(manifest, sort_keys=True, ensure_ascii=True)
        return hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()


# =============================================================================
# ExecutionProvenance (ED-007 — Engine owns provenance creation)
# =============================================================================


@dataclass(frozen=True)
class ExecutionProvenance:
    """Provenance block emitted by CheckMateEngine during execution.

    Per ED-007: The engine owns provenance creation. FindingReportAssembler
    consumes this block as a consumer, rather than computing it post-hoc
    from the outcome vector.

    Contains execution identifier, evidence fingerprint, and snapshot
    content hash — all computed at engine runtime.
    """

    execution_id: str
    evidence_fingerprint: str
    snapshot_hash: str
    capability_version: str