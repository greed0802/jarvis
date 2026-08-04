#!/usr/bin/env python3
"""Modular Professional Intelligence Platform - Canonical Production Entry Point.

This module provides the singular bootstrap entry point for the Jarvis platform.
It delegates to the core application runtime when run without arguments, extending
support for existing CLI execution patterns via `jarvis.cli` if arguments are present.
"""

import sys
import os

# Ensure src namespace resolves correctly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


def main() -> None:
    """Bootstrap root-level execution via single composition root."""
    if len(sys.argv) > 1 and sys.argv[1] not in ("--developer",):
        # Delegate to the established headless CLI router
        from jarvis.cli.main import main as cli_main
        sys.exit(cli_main())
    else:
        # Delegate to the interactive shell host
        developer_mode = "--developer" in sys.argv
        from jarvis.application.bootstrap import bootstrap
        bootstrap(developer_mode=developer_mode)


if __name__ == "__main__":
    main()