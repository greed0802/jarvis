#!/usr/bin/env python3
"""
validate_sources.py

Knowledge Asset Integrity Validator

Validates a Knowledge manifest against the physical file system to ensure:
1. Physical Existence
2. Cryptographic Integrity (SHA-256 match)
3. Schema constraints

If this tool returns exit code 0, the repository boundary is in a deterministic, trusted state.
"""

import os
import json
import hashlib
import sys
import argparse

def calculate_sha256(filepath: str) -> str:
    """Calculates the SHA-256 hash of a file deterministically."""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def validate_manifest(manifest_path: str, base_dir: str) -> bool:
    print(f"Loading manifest: {manifest_path}")

    if not os.path.exists(manifest_path):
        print(f"ERROR: Manifest missing at {manifest_path}")
        return False

    with open(manifest_path, 'r', encoding='utf-8') as f:
        try:
            manifest = json.load(f)
        except json.JSONDecodeError as e:
            print(f"ERROR: Manifest is not valid JSON. {e}")
            return False

    assets = manifest.get('assets', [])
    print(f"Loaded {len(assets)} assets for verification.")

    errors = []
    seen_hashes = {}
    duplicates = []

    for idx, asset in enumerate(assets):
        asset_id = asset.get('id', f'UNKNOWN-{idx}')
        rel_path = asset.get('source_path')
        expected_hash = asset.get('hash_sha256')

        if not rel_path or not expected_hash:
            errors.append(f"{asset_id}: Missing source_path or hash_sha256 in manifest.")
            continue

        # Convert forward slashes back to OS specific
        physical_path = os.path.normpath(os.path.join(base_dir, rel_path))

        # Check existence
        if not os.path.exists(physical_path):
            errors.append(f"MISSING: {asset_id} -> {physical_path}")
            continue

        # Check integrity
        try:
            actual_hash = calculate_sha256(physical_path)
            if actual_hash != expected_hash:
                errors.append(f"CORRUPTION: {asset_id} -> Hash mismatch!\nExpected: {expected_hash}\nActual:   {actual_hash}")
                continue

            # Check duplicates (warning only)
            if actual_hash in seen_hashes:
                duplicates.append(f"DUPLICATE BLOBS: {asset_id} && {seen_hashes[actual_hash]} share hash {actual_hash}")
            else:
                seen_hashes[actual_hash] = asset_id

        except Exception as e:
            errors.append(f"READ ERROR: {asset_id} -> {e}")

    # Report results
    print("\n--- Validation Results ---")
    if duplicates:
        print(f"WARNING: Found {len(duplicates)} duplicate physical binary blobs (identical hashes).")
        # In a real run, we might want to log duplicates, but they don't break determinism per se.

    if errors:
        print(f"FAILED: {len(errors)} assertions failed.")
        for err in errors[:20]:  # Only print first 20 errors to avoid spam
            print(err)
        if len(errors) > 20:
            print(f"...and {len(errors) - 20} more errors.")
        return False
    else:
        print(f"SUCCESS: All {len(assets)} assets verified correctly.")
        print("Integrity: MATCH")
        print("Existence: MATCH")
        return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Knowledge Registry Validator")
    parser.add_argument("--manifest", default="knowledge/registry/source_manifest.json", help="Path to manifest JSON")
    parser.add_argument("--base-dir", default=".", help="Base directory (usually repository root, where 'knowledge_inbox' is located)")

    args = parser.parse_args()

    success = validate_manifest(args.manifest, args.base_dir)
    sys.exit(0 if success else 1)