"""EP-1001 Verification Tests: App Shell & Workspace.

Tests verify compliance with AC-1 through AC-8 defined in EP-1001.
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest

from jarvis.contracts.capabilities import (
    CapabilityHost,
    EvidenceBindingFrozenError,
    EvidenceReference,
    EvidenceSourceType,
    Finding,
    FindingReport,
    ReportProvenance,
    Severity,
    TelemetrySummary,
)


def test_capability_host_protocol_defined() -> None:
    """AC-4: CapabilityHost interface is defined."""
    class SampleCapability:
        @property
        def capability_id(self) -> str:
            return "test.ep1001"
        async def initialize(self) -> None:
            pass
        async def dispose(self) -> None:
            pass
    assert isinstance(SampleCapability(), CapabilityHost)


def test_findingreport_conforms_to_adr_0031() -> None:
    """AC-5: FindingReport matches ADR-0031 schema."""
    provenance = ReportProvenance(
        execution_id="test-001",
        evidence_fingerprint="abc",
        rule_snapshot_hash="def",
        capability_version="1.0.0",
    )
    report = FindingReport(
        provenance=provenance,
        telemetry_summary=TelemetrySummary(rule_count_total=5),
        findings=[],
    )
    assert report.provenance.execution_id == "test-001"


def test_workspace_initialize_creates_structure() -> None:
    """AC-2: Workspace creates directories on first run."""
    from jarvis.platform.workspace import initialize_workspace

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "ws_test"
        ws = initialize_workspace(root, name="test")
        assert ws.root_path.exists()
        assert (ws.root_path / "evidence").is_dir()
        assert (ws.root_path / "journal").is_dir()
        meta = json.loads((ws.root_path / ".jarvis_workspace.json").read_text(encoding="utf-8"))
        assert meta["name"] == "test"


def test_workspace_refuses_reinit() -> None:
    """AC-2: Workspace refuses re-init when metadata exists."""
    from jarvis.platform.workspace import initialize_workspace

    with tempfile.TemporaryDirectory() as d:
        root = Path(d) / "ws"
        initialize_workspace(root)
        with pytest.raises(FileExistsError):
            initialize_workspace(root)


def test_evidence_binding_immutability() -> None:
    """AC-6: Post-binding evidence throws EvidenceBindingFrozenError."""
    from jarvis.platform.workspace import EvidenceBinding

    with tempfile.TemporaryDirectory() as d:
        p = Path(d)
        (p / "f.json").write_text("{}")
        binding = EvidenceBinding(_workspace_path=p)
        binding.bind(str(p))
        assert binding.is_bound
        with pytest.raises(EvidenceBindingFrozenError):
            binding.bind(str(p))


def test_evidence_binding_rejects_missing_path() -> None:
    """Evidence binding raises FileNotFoundError."""
    from jarvis.platform.workspace import EvidenceBinding

    binding = EvidenceBinding(_workspace_path=Path("/dev/null"))
    with pytest.raises(FileNotFoundError):
        binding.bind("/no/such/path/at/all")


def test_finding_requires_evidence() -> None:
    """C1.2: Finding without evidence raises ValueError."""
    with pytest.raises(ValueError):
        Finding(rule_id="r", severity=Severity.MAJOR,
                risk_statement="x", remediation="y")


def test_finding_requires_risk_and_remediation() -> None:
    """C1.6: Finding without risk/remediation raises ValueError."""
    ref = EvidenceReference(
        document_id="d1", sheet="s1", evidence_id="e1",
        source_type=EvidenceSourceType.CELL,
    )
    with pytest.raises(ValueError):
        Finding(rule_id="r1", severity=Severity.MAJOR, evidence=[ref],
                risk_statement="", remediation="fix")
    with pytest.raises(ValueError):
        Finding(rule_id="r2", severity=Severity.MAJOR, evidence=[ref],
                risk_statement="risk", remediation="")