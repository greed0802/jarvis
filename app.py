#!/usr/bin/env python3
"""Jarvis Platform Bootstrap Entry Point.

This module provides the minimal entry point for the Jarvis platform.
The Application class handles all startup orchestration.
"""

import asyncio

from jarvis import __version__
from jarvis.application import Application
from jarvis.configuration import Configuration


async def main() -> None:
    """Main entry point for the Jarvis platform."""
    print(f"Jarvis Platform v{__version__}")
    print("Application Runtime v0.1")

    config = Configuration()
    app = Application(config)

    await app.run()


if __name__ == "__main__":
    asyncio.run(main())