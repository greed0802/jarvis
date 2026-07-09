#!/usr/bin/env python3
"""Jarvis Platform Bootstrap Entry Point.

This module provides the minimal entry point for the Jarvis platform.
The Application class handles all startup orchestration.
"""

import asyncio

from jarvis import __version__
from jarvis.application import Application


async def main() -> None:
    """Main entry point for the Jarvis platform."""
    print(f"Jarvis Platform v{__version__}")
    print("Application Runtime v0.1")

    app = Application(config={"log_level": "INFO"})

    try:
        await app.run()
    except Exception as e:
        print(f"Platform error: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
