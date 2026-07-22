"""
build_docs.py — DEPRECATED. Use generate_docs.py instead.

This file is a compatibility wrapper that prints a deprecation notice
and delegates to generate_docs.py. It will be removed in a future
major version.
"""

import subprocess
import sys
from pathlib import Path

def main():
    print("=" * 60)
    print("DEPRECATION NOTICE")
    print("=" * 60)
    print()
    print("build_docs.py is deprecated.")
    print("Use generate_docs.py instead:")
    print("  python tools/generate_docs.py")
    print()
    print("Delegating to generate_docs.py...")
    print("=" * 60)

    generate_path = Path(__file__).parent / "generate_docs.py"
    result = subprocess.run(
        [sys.executable, str(generate_path)],
        cwd=str(Path(__file__).parent.parent),
    )
    sys.exit(result.returncode)

if __name__ == "__main__":
    main()