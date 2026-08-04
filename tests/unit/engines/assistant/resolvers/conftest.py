"""Shared fixtures for resolver tests (PROD-0003)."""

import pytest

from jarvis.core.workspace.runtime import WorkspaceRuntime
from jarvis.core.artifact.repository import ArtifactRepository
from jarvis.core.memory.engine import WorkspaceMemoryService
from jarvis.core.capability.runtime import CapabilityRuntime
from jarvis.core.capability.models import CapabilityInput


@pytest.fixture
def workspace_runtime() -> WorkspaceRuntime:
    return WorkspaceRuntime()


@pytest.fixture
def artifact_repository() -> ArtifactRepository:
    return ArtifactRepository()


@pytest.fixture
def memory_service() -> WorkspaceMemoryService:
    return WorkspaceMemoryService()


@pytest.fixture
def capability_runtime(workspace_runtime: WorkspaceRuntime) -> CapabilityRuntime:
    return CapabilityRuntime(workspace_runtime)