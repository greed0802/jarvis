"""Test configuration — ensure src/ is on Python path.

Used by all test modules so they can import from jarvis.* packages.
"""
import sys
from pathlib import Path

_SRC = str(Path(__file__).resolve().parent.parent / "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)