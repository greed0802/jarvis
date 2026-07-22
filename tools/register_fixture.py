"""Register a fixture in the authoritative fixture metadata.

Usage:
    python tools/register_fixture.py <path_to_fixture> [--description DESC]

Computes SHA-256 hash and adds the entry to tests/fixtures/fixtures.json.

Fixture registration is an explicit engineering action.
Running pytest never modifies fixture metadata.
"""

import argparse
import hashlib
import json
import sys
from datetime import date
from pathlib import Path


FIXTURES_DIR = Path(__file__).parent.parent / "tests" / "fixtures"
METADATA_FILE = FIXTURES_DIR / "fixtures.json"


def compute_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_metadata() -> dict:
    if not METADATA_FILE.exists():
        return {}
    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_metadata(metadata: dict) -> None:
    metadata = dict(sorted(metadata.items()))
    tmp = METADATA_FILE.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
        f.write("\n")
    tmp.replace(METADATA_FILE)


def check_duplicates(name: str, sha256: str, rel_path: str, metadata: dict) -> list[str]:
    errors = []
    if name in metadata:
        errors.append(f'Fixture "{name}" is already registered.')
    for existing_name, entry in metadata.items():
        if entry["sha256"] == sha256:
            errors.append(
                f'SHA-256 {sha256} matches existing fixture "{existing_name}".\n'
                f"  Identical fixtures should not be registered twice."
            )
        if entry["path"] == rel_path:
            errors.append(
                f'Path "{rel_path}" matches existing fixture "{existing_name}".\n'
                f"  This file is already registered."
            )
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Register a fixture in the authoritative fixture metadata."
    )
    parser.add_argument(
        "fixture_path",
        type=Path,
        help="Path to the fixture file (must be under tests/fixtures/)",
    )
    parser.add_argument(
        "--description",
        type=str,
        default="TODO: Add description",
        help="Description of the fixture (default: 'TODO: Add description')",
    )
    args = parser.parse_args()

    fixture_path = args.fixture_path.resolve()
    description = args.description

    if not fixture_path.exists():
        print(f"Error: {fixture_path} does not exist")
        sys.exit(1)

    try:
        rel_path = fixture_path.relative_to(FIXTURES_DIR)
    except ValueError:
        print(f"Error: {fixture_path} is not under {FIXTURES_DIR}")
        sys.exit(1)

    # TODO:
    # Registry keys currently use filenames because fixture names are unique.
    # If multiple fixture categories introduce filename collisions,
    # promote the registry key to the relative fixture path.
    name = fixture_path.name
    sha256 = compute_hash(fixture_path)
    rel_path_str = str(rel_path).replace("\\", "/")

    metadata = load_metadata()

    errors = check_duplicates(name, sha256, rel_path_str, metadata)
    if errors:
        print("Registration failed:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)

    metadata[name] = {
        "path": rel_path_str,
        "sha256": sha256,
        "description": description,
        "acquired": date.today().isoformat(),
    }

    save_metadata(metadata)

    print(f"Registered fixture: {name}")
    print(f"  Path:        {rel_path_str}")
    print(f"  SHA-256:     {sha256}")
    print(f"  Description: {description}")
    print(f"  Acquired:    {date.today().isoformat()}")
    print(f"\nUpdated {METADATA_FILE}")


if __name__ == "__main__":
    main()