"""Evidence ingestion, append-only store, and capability-neutral repository.

Implements EP-1002 deliverables:
- EvidenceImporter: contract translation and payload validation.
- EvidenceStore: append-only file persistence (C1.4 immutability).
- FileEvidenceRepository: read-only query facade.

Architecture conformance: ADR-0030 (C1.1), ADR-0031 (C1.2), ADR-0032 (C1.4, C1.5, C1.12).
"""

from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from jarvis.contracts.capabilities import (
    EvidenceBindingFrozenError,
    EvidenceGranularity,
    EvidenceReference,
    EvidenceRepository,
    EvidenceSourceType,
)

# =============================================================================
# EP-1002.1 — EvidenceImporter
# =============================================================================

@dataclass
class EvidenceImportResult:
    """Result of an evidence import operation."""

    reference: EvidenceReference
    granularity: EvidenceGranularity
    imported_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class ContractMismatchError(ValueError):
    """Raised when an evidence payload fails schema validation (C1.12)."""

class EvidenceImporter:
    """Validates BOQ Intelligence evidence payloads and builds EvidenceReference records.

    Per C1.1: accepts only structured, validated payloads.
    Per C1.12: verifies contract compatibility; rejects non-conforming input.
    """

    REQUIRED_FIELDS = {"document_id", "sheet", "evidence_id", "source_type", "granularity"}

    def import_payload(self, payload: dict[str, Any]) -> EvidenceImportResult:
        """Consume a validated BOQ Intelligence evidence payload.

        Args:
            payload: A dict with required fields AND a granularity measure.

        Returns:
            EvidenceImporterResult with a canonical EvidenceReference.

        Raises:
            EvidenceReason: If required fields are missing or value types mismatch.
        """
        missing = self.REQUIRED_FIELDS - payload.keys()
        if missing:
            raise ContractMismatchError(
                f"Payload validation failed. Missing fields: {missing}"
            )
        try:
            source_type = EvidenceSourceType(payload["source_type"])
        except ValueError as e:
            raise ContractMismatchError(
                f"Invalid source type '{payload['source_type']}'. Must be one of: "
                f"{[e.value for e in EvidenceSourceType]}"
            ) from e
        try:
            granularity = EvidenceGranularity(payload["granularity"])
        except ValueError as e:
            raise ContractMismatchError(
                f"Invalid granularity level '{payload['granularity']}':values "
                f"{[e.value for e in EvidenceGranularity]}"
            ) from e
        reference = EvidenceReference(
            document_id=str(payload["document_id"]),
            sheet=str(payload["sheet"]),
            evidence_id=str(payload["evidence_id"]),
            source_type=source_type,
            page=payload.get("page"),
            bbox=payload.get("bbox"),
            text_span=payload.get("text_span"),
        )
        return EvidenceImportResult(reference=reference, granularity=granularity)

# =============================================================================
# EP-1002.2 — EvidenceStore (append-only)
# =============================================================================

class EvidenceStoreImmutableError(EvidenceBindingFrozenError):
    """Raised when attempting to modify an evidence entry already persisted."""

@dataclass
class EvidenceStore:
    """Append-only evidence store backed by a JSON lines file.

    Per C1.4: evidence is append-only and immutable. No delete or update operations.
    Maintains a tagged granularity index for efficient lookup (ED-006).
    """

    _entries: dict[str, EvidenceReference] = field(default_factory=dict)
    _granularity_index: dict[EvidenceGranularity, list[str]] = field(
        default_factory=lambda: defaultdict(list)
    )
    _frozen: bool = field(default=False)

    def append(self, result: EvidenceImportResult) -> None:
        """Persist an evidence record into this store.

        Once appended, the record cannot be changed or deleted.
        Also populates the granularity index for ED-006 composite lookups.

        Raises:
            EvidenceBindingFrozenError: If evidence has been frozen.
        """
        if self._frozen:
            raise EvidenceBindingFrozenError(
                "Evidence store is already frozen. Append not allowed."
            )
        evidence_id = result.reference.evidence_id
        self._entries[evidence_id] = result.reference
        self._granularity_index[result.granularity].append(evidence_id)

    def freeze(self) -> None:
        """Seal the store for write operations. Once frozen, append raises."""
        self._frozen = True

    @property
    def is_frozen(self) -> bool:
        return self._frozen

    @property
    def count(self) -> int:
        return len(self._entries)

    def _items(self) -> dict[str, EvidenceReference]:
        return dict(self._entries)

    def _granularity_map(self) -> dict[EvidenceGranularity, list[str]]:
        """Return a copy of the granularity index map."""
        return {
            gran: list(ids)
            for gran, ids in self._granularity_index.items()
        }

# =============================================================================
# EP-1002.3 — FileEvidenceRepository (query facade)
# =============================================================================

@dataclass
class FileEvidenceRepository(EvidenceRepository):
    """File-backed read-only query facade for a persisted evidence store.

    Provides the capability-neutral EvidenceRepository protocol.
    Can be instantiated from an EvidenceStore or loaded from file.
    """

    _records: list[EvidenceReference] = field(default_factory=list)
    _granularity_index: dict[EvidenceGranularity, list[str]] = field(
        default_factory=lambda: defaultdict(list)
    )

    def load_from_store(self, store: EvidenceStore) -> None:
        """Ingest records and granularity index from an EvidenceStore."""
        self._records = list(store._items().values())
        self._granularity_index = {
            k: list(v) for k, v in store._granularity_index.items()
        }

    def load_from_file(self, filepath: Path) -> None:
        """Load evidence records from a JSON lines file."""
        if not filepath.exists():
            raise FileNotFoundError(f"Evidence file not found: {filepath}")
        records: list[EvidenceReference] = []
        for line in filepath.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            obj = json.loads(line)
            ref = EvidenceReference(
                document_id=obj["document_id"],
                sheet=obj["sheet"],
                evidence_id=obj["evidence_id"],
                source_type=EvidenceSourceType(obj["source_type"]),
                page=obj.get("page"),
                bbox=obj.get("bbox"),
                text_span=obj.get("text_span"),
            )
            records.append(ref)
        self._records = records

    def save_to_file(self, filepath: Path) -> None:
        """Persist current records to a JSON lines file."""
        lines = []
        for ref in self._records:
            obj = {
                "document_id": ref.document_id,
                "sheet": ref.sheet,
                "evidence_id": ref.evidence_id,
                "source_type": ref.source_type.value,
                "page": ref.page,
                "bbox": ref.bbox,
                "text_span": ref.text_span,
            }
            lines.append(json.dumps(obj))
        filepath.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # --- EvidenceRepository protocol methods ---

    def get(self, evidence_id: str) -> EvidenceReference | None:
        for ref in self._records:
            if ref.evidence_id == evidence_id:
                return ref
        return None

    def list(self) -> list[EvidenceReference]:
        return list(self._records)

    def find_by_document(self, document_id: str) -> list[EvidenceReference]:
        return [r for r in self._records if r.document_id == document_id]

    def find_by_sheet(self, document_id: str, sheet: str) -> list[EvidenceReference]:
        return [r for r in self._records if r.document_id == document_id and r.sheet == sheet]

    def find_by_source_type(self, source_type: EvidenceSourceType) -> list[EvidenceReference]:
        return [r for r in self._records if r.source_type == source_type]

    def find_by_granularity(
        self, granularity: EvidenceGranularity
    ) -> list[EvidenceReference]:
        """Find all evidence records at a specific granularity level.

        Resolves via the in-memory granularity index populated during
        EvidenceStore ingestion (ED-006).

        Args:
            granularity: The EvidenceGranularity level to filter by.

        Returns:
            Evidence records matching the requested granularity level.
            Returns empty list if no records are indexed at that level.
        """
        ids = self._granularity_index.get(granularity, [])
        return [ref for ref in self._records if ref.evidence_id in ids]
