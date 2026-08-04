import os
import shutil
from pathlib import Path

REPO_ROOT = Path("d:/Jarvis")
REPORTS_DIR = REPO_ROOT / "temp/reconciliation/reports"
CONFLICTS_DIR = REPO_ROOT / "temp/reconciliation/conflict_resolution"
EXEC_DIR = REPO_ROOT / "docs/execution/RR_0002"
FEDORA_ROOT = REPO_ROOT / "temp/reconciliation/fedora_snapshot"

def run():
    # Phase 2: Move records
    EXEC_DIR.mkdir(parents=True, exist_ok=True)
    
    for d in [REPORTS_DIR, CONFLICTS_DIR]:
        if not d.exists():
            continue
        for item in d.glob("*"):
            if item.is_file():
                dest = EXEC_DIR / item.name
                shutil.copy2(item, dest)
                print(f"Copied {item.name} to {EXEC_DIR}")

    # Phase 6: Fedora Snapshot README
    readme_path = FEDORA_ROOT / "README.md"
    content = """# Fedora Snapshot

**Origin:** Copied from the Fedora development environment during RR-0001 (Repository Reconciliation).
**Purpose:** Provided as a read-only historical reference of the Fedora engineering workspace state prior to canonicalization.
**Status:** Reconciliation completed successfully.
**Note:** This directory is retained ONLY for historical provenance and artifact tracking. Do not use any of the files within as runtime dependencies or source truth.
"""
    readme_path.write_text(content, encoding="utf-8")
    print(f"Created {readme_path}")

if __name__ == "__main__":
    run()