#!/usr/bin/env python3
"""Modular Professional Intelligence Platform - Canonical Production Entry Point.

This module provides the singular bootstrap entry point for the Jarvis platform.
It delegates to the core application runtime when run without arguments, extending
support for existing CLI execution patterns via `jarvis.cli` if arguments are present.
"""

import sys
import os
import asyncio

# Ensure src namespace resolves correctly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from jarvis import __version__
from jarvis.application import Application
from jarvis.configuration import Configuration
from jarvis.cli.main import main as cli_main

async def run_server() -> None:
    """Orchestrate the platform core application lifecycle."""
    print(f"Jarvis Platform v{__version__}")
    print("Application Runtime v0.1")

    config = Configuration()
    app = Application(config)

    await app.run()

def main() -> None:
    """Bootstrap root-level execution via single composition root."""
    if len(sys.argv) > 1:
        # Delegate to the established headless CLI router
        sys.exit(cli_main())
    else:
        # Delegate to the orchestration Application layer
        asyncio.run(run_server())

if __name__ == "__main__":
    main()