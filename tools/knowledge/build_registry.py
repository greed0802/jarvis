#!/usr/bin/env python3
"""
build_registry.py

Deterministic Knowledge Artifact Registration Tool

This tool scans a target directory (e.g., knowledge_inbox/), reads each file,
calculates its SHA-256 hash, and generates a compliant JSON manifest mapping
to the knowledge/governance/registry_schema.json format.

Safety Guarantee: This tool operates STRICTLY in Read-Only mode on source files.
"""

import os
import json
import hashlib
from datetime import datetime, timezone
import sys
import argparse

# Categories matching KNOWLEDGE_REGISTER.md definitions
VALID_CATEGORIES = {
    'anzsmm': 'ANZSMM',
    'standards': 'Australian Standards',
    'ncc': 'NCC',
    'councils': 'Council Specifications',
    'specifications': 'Engineering Specifications',
    'reports': 'Engineering Reports',
    'projects': 'Historical Projects',
    'glossary': 'Glossary'
}

def calculate_sha256(filepath: str) -> str:
    """Calculates the SHA-256 hash of a file deterministically."""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        # Read in 4K chunks to handle large files (e.g., 200MB PDFs) efficiently
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def determine_category(filepath: str) -> str:
    """Determines the semantic category based on the file path."""
    path_lower = filepath.lower()
    
    # Simple heuristic matching path segments to approved categories
    if 'anzsmm' in path_lower:
        return 'ANZSMM'
    elif 'standards' in path_lower:
        return 'Australian Standards'
    elif 'specifications' in path_lower:
        return 'Engineering Specifications'
    elif 'projects' in path_lower:
        return 'Historical Projects'
    elif 'councils' in path_lower:
        return 'Council Specifications'
    elif 'reports' in path_lower:
        return 'Engineering Reports'
    elif 'ncc' in path_lower:
        return 'NCC'
    else:
        return 'Unknown'

def requires_ocr(ext: str) -> bool:
    """Determines if the extension typically requires OCR processing."""
    return ext.lower() in ['.pdf', '.png', '.jpg', '.jpeg']

def sanitize_title(filename: str, ext: str) -> str:
    """Creates a basic canonical title from the filename."""
    if ext:
        filename = filename[:-len(ext)]
    # Replace underscores/dashes with spaces and title case
    return filename.replace('_', ' ').replace('-', ' ').title().strip()

def build_manifest(source_dir: str, output_path: str):
    """Scans the source directory and creates a JSON schema-compliant manifest."""
    
    print(f"Safety Check: Scanning {source_dir} in READ-ONLY mode...")
    
    if not os.path.exists(source_dir):
        print(f"Error: Directory {source_dir} not found.")
        sys.exit(1)
        
    assets = []
    counter = 1
    
    # Sort walk to ensure deterministic processing order
    for root, dirs, files in sorted(os.walk(source_dir)):
        dirs.sort() # Deterministic subdirectories
        for file in sorted(files):
            filepath = os.path.join(root, file)
            # Use forward slashes for cross-platform deterministic paths
            relative_path = os.path.relpath(filepath, start=os.path.dirname(source_dir)).replace('\\', '/')
            
            filename = os.path.basename(filepath)
            _, ext = os.path.splitext(filename)
            ext = ext.lower()
            
            try:
                # 1. Gather stats (READ ONLY)
                stat = os.stat(filepath)
                size_bytes = stat.st_size
                
                # 2. Calculate cryptographic signature (READ ONLY)
                file_hash = calculate_sha256(filepath)
                
                # 3. Formulate Asset Record
                asset = {
                    "id": f"KN-{counter:06d}",
                    "title": sanitize_title(filename, ext),
                    "category": determine_category(relative_path),
                    "source_path": relative_path,
                    "filename": filename,
                    "extension": ext,
                    "hash_sha256": file_hash,
                    "size_bytes": size_bytes,
                    "state": "Draft",
                    "ocr_required": requires_ocr(ext),
                    "authority": None,
                    "document_version": None,
                    "notes": "Automatically registered via build_registry.py",
                    "acquired_date": datetime.now(timezone.utc).isoformat()
                }
                
                assets.append(asset)
                counter += 1
                
                if counter % 100 == 0:
                    print(f"Processed {counter} files...")
                    
            except Exception as e:
                print(f"Warning: Failed to process {filepath}: {e}")

    print(f"\nScan complete. Building manifest for {len(assets)} assets...")
    
    manifest = {
        "version": "1.0",
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "total_assets": len(assets),
        "assets": assets
    }
    
    # Ensure target directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    print(f"Writing manifest to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        
    print("Manifest generation complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deterministic Knowledge Asset Registry Builder")
    parser.add_argument("--source", default="knowledge_inbox", help="Directory to scan (default: knowledge_inbox)")
    parser.add_argument("--output", default="knowledge/registry/source_manifest.json", help="Output JSON path")
    
    args = parser.parse_args()
    build_manifest(args.source, args.output)