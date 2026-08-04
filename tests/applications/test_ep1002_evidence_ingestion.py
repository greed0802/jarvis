"""EP-1002 Verification Tests: Evidence Ingestion & Store.

Tests verify compliance with AC-1 through AC-6 defined in EP-1002.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from jarvis.contracts.capabilities import (
    EvidenceSourceType,
)
from jarvis.platform.evidence import (
    ContractMismatchError,
    EvidenceImporter,
    EvidenceStore,
    FileEvidenceRepository,
)

# =============================================================================
# AC-1: EvidenceImporter imports validated payload
# =============================================================================

def test_importer_produces_reference() -> None:
    """AC-1: EvidenceImporter creates 7-field EvidenceReference."""
    importer = EvidenceImporter()
    payload = {
        "document_id": "BOQ-2026-001",
        "sheet": "Concrete",
        "evidence_id": "E001",
        "source_type": "cell",
        "granularity": "atomic",
        "page": 3,
    }
    result = importer.import_payload(payload)
    ref = result.reference
    assert ref.document_id == "BOQ-2026-001"
    assert ref.sheet == "Concrete"
    assert ref.evidence_id == "E001"
    assert ref.source_type == EvidenceSourceType.CELL
    assert ref.page == 3

def test_importer_rejects_missing_fields() -> None:
    """AC-1: Importer raises ContractMismatchError on missing fields."""
    importer = EvidenceImporter()
    with pytest.raises(ContractMismatchError):
        importer.import_payload({"evidence_id": "E1"})

def test_importer_rejects_invalid_enum_values() -> None:
    """AC-1: Importer rejects invalid source_type/granularity."""
    importer = EvidenceImporter()
    bad_source = {
        "document_id": "D1", "sheet": "S1", "evidence_id": "E1",
        "source_type": "invalid_type", "granularity": "atomic",
    }
    with pytest.raises(ContractMismatchError):
        importer.import_payload(bad_source)
    bad_grain = {
        "document_id": "D1", "sheet": "S1", "evidence_id": "E1",
        "source_type": "cell", "granularity": "invalid_grain",
    }
    with pytest.raises(ContractMismatchError):
        importer.import_payload(bad_grain)

# =============================================================================
# AC-2, AC-5: EvidenceStore accepts & persists, immutability
# =============================================================================

def test_store_accepts_and_persists() -> None:
    """AC-2: Store preserves records after writes."""
    importer = EvidenceImporter()
    store = EvidenceStore()
    payload = {
        "document_id": "D1", "sheet": "S1", "evidence_id": "E1",
        "source_type": "cell", "granularity": "atomic",
    }
    result = importer.import_payload(payload)
    store.append(result)
    assert store.count == 1

def test_store_immutability_blocks_second_append() -> None:
    """AC-5: Frozen store blocks further writes."""
    importer = EvidenceImporter()
    store = EvidenceStore()
    payload = {
        "document_id": "D1", "sheet": "S1", "evidence_id": "E1",
        "source_type": "cell", "granularity": "atomic",
    }
    result = importer.import_payload(payload)
    store.append(result)
    store.freeze()
    from jarvis.contracts.capabilities import EvidenceBindingFrozenError
    with pytest.raises(EvidenceBindingFrozenError):
        store.append(result)

# =============================================================================
# AC-3, AC-4: Repository query facade and granularity classification
# =============================================================================

def test_repository_query_facade() -> None:
    """AC-3: Repository returns correct records from store."""
    store = EvidenceStore()
    importer = EvidenceImporter()
    for i in range(3):
        payload = {
            "document_id": "DOC-001", "sheet": "S1",
            "evidence_id": f"E00{i}",
            "source_type": "cell", "granularity": "atomic",
        }
        store.append(importer.import_payload(payload))
    repo = FileEvidenceRepository()
    repo.load_from_store(store)
    assert repo.get("E00") is None
    assert repo.get("E000") is not None
    assert repo.get("E000").evidence_id == "E000"
    assert len(repo.find_by_document("DOC-001")) == 3
    assert len(repo.find_by_sheet("DOC-001", "S1")) == 3

def test_repo_find_by_source_type() -> None:
    """find_by_source_type returns correct subset."""
    store = EvidenceStore()
    importer = EvidenceImporter()
    for i in range(2):
        store.append(importer.import_payload({
            "document_id": "D", "sheet": "S", "evidence_id": f"E0{i}",
            "source_type": "cell", "granularity": "atomic",
        }))
    store.append(importer.import_payload({
        "document_id": "D", "sheet": "S", "evidence_id": "E002",
        "source_type": "row", "granularity": "structural",
    }))
    repo = FileEvidenceRepository()
    repo.load_from_store(store)
    cells = repo.find_by_source_type(EvidenceSourceType.CELL)
    assert len(cells) == 2

def test_file_roundtrip() -> None:
    """Repository saves and loads correctly."""
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "evidence.jsonl"
        repoA = FileEvidenceRepository()
        repoA.save_to_file(path)
        repoB = FileEvidenceRepository()
        repoB.load_from_file(path)
        assert len(repoB.list()) == 0
