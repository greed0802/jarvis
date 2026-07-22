"""
generate_docs.py — Documentation Generation Entry Point

Primary entry point for repository documentation generation.
Delegates to generate_adr_index.py for ADR index generation.
Additional doc generation capabilities can be added here.

Replaces build_docs.py which is now a deprecation wrapper.

Usage: python tools/generate_docs.py
"""

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def main():
    print("generate_docs.py — Repository Documentation Generator")
    print("=" * 50)

    # Generate ADR index
    adr_tool = PROJECT_ROOT / "tools" / "generate_adr_index.py"
    if adr_tool.exists():
        print("\n[1/1] Generating ADR Index...")
        result = subprocess.run(
            [sys.executable, str(adr_tool)],
            capture_output=True,
            text=True,
            cwd=str(PROJECT_ROOT),
        )
        print(result.stdout)
        if result.returncode != 0:
            print(f"WARN: generate_adr_index.py returned {result.returncode}")
            print(result.stderr)
    else:
        print("WARN: generate_adr_index.py not found — skipping ADR index generation")

    print("\nDone.")

if __name__ == "__main__":
    main()