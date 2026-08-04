"""Platform Bootstrap — host entry point for the Interactive Shell.

Separates the hosting concern from the Application (composition root).
Future hosts (Desktop, Web, API, Test) will have their own bootstrap
modules; ``main.py`` remains a thin delegator.
"""

from __future__ import annotations

import asyncio
import logging

from jarvis.configuration import Configuration
from jarvis.application import Application
from jarvis.ui.shell.shell import WorkspaceShell

logger = logging.getLogger(__name__)


async def _run_interactive(
    developer_mode: bool = False,
) -> None:
    """Full platform lifecycle with interactive shell."""
    from jarvis.version import __version__

    config = Configuration()
    app = Application(config)

    await app.initialize()
    await app.start()

    logger.info("Platform is RUNNING — launching interactive shell.")

    shell = WorkspaceShell(
        application=app,
        developer_mode=developer_mode,
    )

    try:
        await shell.run()
    finally:
        await app.shutdown()
        logger.info("Platform shutdown complete.")


def bootstrap(developer_mode: bool = False) -> None:
    """Synchronous entry point invoked by ``main.py``."""
    asyncio.run(_run_interactive(developer_mode=developer_mode))
