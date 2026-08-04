"""Engineering Artifact Contracts."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
from enum import Enum, auto

class ArtifactType(Enum):
    DRAWING = auto()
    BOQ = auto()
    SPECIFICATION = auto()
    CALCULATION = auto()
    ENGINEERING_REPORT = auto()
    FINDING_REPORT = auto()
    CODE_REFERENCE = auto()
    IMAGE = auto()
    SCHEDULE = auto()
    GENERAL_DOCUMENT = auto()

@dataclass(frozen=True)
class ArtifactMetadata:
    created_by: str
    file_size_bytes: int
    content_hash: str
    custom_properties: dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class ArtifactVersion:
    version_id: str
    artifact_id: str
    version_number: int
    created_at: datetime
    metadata: ArtifactMetadata

@dataclass(frozen=True)
class Artifact:
    artifact_id: str
    workspace_id: str
    name: str
    artifact_type: ArtifactType
    versions: list[ArtifactVersion] = field(default_factory=list)
