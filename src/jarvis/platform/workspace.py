"""Workspace initialization and evidence binding per ADR-0032.

A workspace is a local directory that provides:
- Evidence context: mutable during setup, immutable after binding.
- Journal storage: dedicated directory for execution journals (ADR-0029 stub).
- Configuration metadata: workspace identity and creation data.

Invariants from C1.4 (Evidence Immutability), C1.12 (Contract Compatibility).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from jarvis.contracts.capabilities import EvidenceBindingFrozenError

WORKSPACE_METADATA_FILENAME = ".jarvis_workspace.json"
WORKSPACE_SUBDIRS = ["evidence", "journal"]


@dataclass
class WorkspaceMetadata:
    """Metadata written to the workspace directory on initialization."""

    workspace_id: str
    created_at: str
    version: str = "1.0.0"
    name: str = ""


@dataclass
class EvidenceBinding:
    """A concrete workspace-side evidence context per ADR-0032.

    Once evidence is bound, the context becomes immutable.
    Attempted re-binding raises EvidenceBindingFrozenError (C1.4 invariant).
    """

    _workspace_path: Path
    _bound_path: str | None = field(default=None, init=False)
    _bound: bool = field(default=False, init=False)

    @property
    def is_bound(self) -> bool:
        """Whether the workspace evidence context is already sealed."""
        return self._bound

    @property
    def evidence_path(self) -> str | None:
        """Return the absolute path to the bound evidence directory, or None."""
        return self._bound_path

    def bind(self, evidence_path: str) -> list[str]:
        """Bind an evidence directory and freeze this context.

        Args:
            evidence_path: Path to the directory containing evidence files.

        Returns:
            List of absolute paths to the evidence files discovered.

        Raises:
            EvidenceBindingFrozenError: If evidence has already been bound.
            FileNotFoundError: If the evidence directory does not exist.
        """
        if self._bound:
            raise EvidenceBindingFrozenError(
                "Evidence context is already bound and immutable."
            )
        resolved = Path(evidence_path).resolve()
        if not resolved.exists():
            raise FileNotFoundError(f"Evidence path not found: {resolved}")
        artifacts = sorted([str(p) for p in resolved.iterdir() if p.is_file()])
        self._bound_path = str(resolved)
        self._bound = True
        return artifacts


@dataclass
class Workspace:
    """A local workspace initialized with evidence/journal structure.

    This is the runtime representation of a workspace directory.
    It is created by initialize_workspace().
    """

    root_path: Path
    workspace_id: str
    evidence_binding: EvidenceBinding
    journal_path: Path


def initialize_workspace(root: Path | str, name: str = "") -> Workspace:
    """Initialize a local workspace directory structure.

    Creates:
      - evidence/         (empty, ready for evidence import)
      - journal/          (ADR-0029 stub; empty directory in M10.1)
      - .jarvis_workspace.json (metadata)

    Args:
        root: Root directory for the workspace.
        name: Optional human-readable workspace name.

    Returns:
        Workspace instance with initialized directory structure.

    Raises:
        FileExistsError: If workspace metadata already exists at root.
    """
    root_path = Path(root).resolve()
    root_path.mkdir(parents=True, exist_ok=True)
    metadata_file = root_path / WORKSPACE_METADATA_FILENAME
    if metadata_file.exists():
        raise FileExistsError(
            f"Workspace already initialized at {root_path} "
            f"({WORKSPACE_METADATA_FILENAME} exists)."
        )

    workspace_id = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    metadata = WorkspaceMetadata(
        workspace_id=workspace_id,
        created_at=datetime.now(timezone.utc).isoformat(),
        name=name,
    )

    for subdir in WORKSPACE_SUBDIRS:
        (root_path / subdir).mkdir(exist_ok=True)

    metadata_file.write_text(
        json.dumps(metadata.__dict__, indent=2, default=str), encoding="utf-8"
    )

    evidence_binding = EvidenceBinding(_workspace_path=root_path / "evidence")
    return Workspace(
        root_path=root_path,
        workspace_id=workspace_id,
        evidence_binding=evidence_binding,
        journal_path=root_path / "journal",
    )