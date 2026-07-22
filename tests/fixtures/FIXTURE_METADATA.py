"""Authoritative fixture metadata for regression testing.

This module is the single source of truth for fixture identity verification.
All acceptance tests verify fixture integrity against this metadata before execution.

Metadata is stored in tests/fixtures/fixtures.json.
Fixture registration is an explicit engineering action performed via
tools/register_fixture.py. Running pytest never modifies any fixture metadata.

Maintained by: Senior Production Engineer
Last updated: 2026-07-14
"""

import hashlib
import json
from pathlib import Path

_FIXTURES_DIR = Path(__file__).parent
_METADATA_FILE = _FIXTURES_DIR / "fixtures.json"


def _load_metadata() -> dict:
    with open(_METADATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def verify_fixture(name: str) -> Path:
    """Verify fixture identity and return path.

    Args:
        name: Fixture filename (e.g., "full_boq.xlsx")

    Returns:
        Path to verified fixture file

    Raises:
        KeyError: If fixture is not registered
        FileNotFoundError: If fixture file does not exist
        ValueError: If fixture hash does not match registered value
    """
    metadata = _load_metadata()

    if name not in metadata:
        raise KeyError(
            f'Fixture "{name}" is not registered.\n'
            f"Register the fixture explicitly before using it in acceptance tests.\n"
            f"Use: python tools/register_fixture.py <path_to_fixture>"
        )

    entry = metadata[name]
    path = _FIXTURES_DIR / entry["path"]

    if not path.exists():
        raise FileNotFoundError(f"Fixture {name} not found at {path}")

    computed_hash = hashlib.sha256(path.read_bytes()).hexdigest()
    expected_hash = entry["sha256"]

    if computed_hash != expected_hash:
        raise ValueError(
            f"Fixture {name} hash mismatch.\n"
            f"Expected: {expected_hash}\n"
            f"Computed: {computed_hash}\n"
            f"The fixture may have been modified or is stale."
        )

    return path