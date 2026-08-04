#!/usr/bin/env python3
"""Jarvis Platform Legacy Hook.

This file acts purely as a backward-compatibility wrapper.
The canonical production entry point is `main.py`.
"""

import sys
from main import main

if __name__ == "__main__":
    sys.exit(main())