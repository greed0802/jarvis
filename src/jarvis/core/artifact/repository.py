"""Engineering Artifact Repository."""
import logging
from datetime import datetime
from typing import Dict, List, Optional

from jarvis.contracts.lifecycle import LifecycleAware
from .models import Artifact, ArtifactType, ArtifactMetadata, ArtifactVersion

logger = logging.getLogger(__name__)

class ArtifactRepository(LifecycleAware):
    """Authoritative asset catalog for engineering drawings, BOQs, and specs."""

    def __init__(self):
        self._artifacts: Dict[str, Artifact] = {}

    def register_artifact(
        self,
        workspace_id: str,
        name: str,
        artifact_type: ArtifactType,
        content_hash: str,
        size_bytes: int,
        created_by: str
    ) -> Artifact:
        artifact_id = f"art-{len(self._artifacts) + 1}"
        
        metadata = ArtifactMetadata(
            created_by=created_by,
            file_size_bytes=size_bytes,
            content_hash=content_hash
        )
        
        version = ArtifactVersion(
            version_id=f"{artifact_id}-v1",
            artifact_id=artifact_id,
            version_number=1,
            created_at=datetime.now(),
            metadata=metadata
        )

        artifact = Artifact(
            artifact_id=artifact_id,
            workspace_id=workspace_id,
            name=name,
            artifact_type=artifact_type,
            versions=[version]
        )
        
        self._artifacts[artifact_id] = artifact
        logger.info(f"Registered artifact: {artifact_id} ({name}) type={artifact_type.name}")
        return artifact

    def get(self, artifact_id: str) -> Optional[Artifact]:
        return self._artifacts.get(artifact_id)

    async def initialize(self) -> None:
        logger.info("ArtifactRepository initialized.")

    async def start(self) -> None:
        logger.info("ArtifactRepository started.")

    async def shutdown(self) -> None:
        logger.info("ArtifactRepository shutting down.")
