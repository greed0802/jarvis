from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
from enum import Enum

class DocumentClassification(Enum):
    ARCHITECTURAL_DRAWING = "Architectural Drawing"
    STRUCTURAL_DRAWING = "Structural Drawing"
    CIVIL_DRAWING = "Civil Drawing"
    SERVICES_DRAWING = "Services Drawing"
    SPECIFICATION = "Specification"
    BOQ = "BOQ"
    CHECKLIST = "Checklist"
    SCHEDULE = "Schedule"
    IMAGE = "Image"
    PHOTO = "Photo"
    SPREADSHEET = "Spreadsheet"
    CALCULATION = "Calculation"
    REPORT = "Report"
    EMAIL = "Email"
    ARCHIVE = "Archive"
    UNKNOWN = "Unknown"

class DocumentLifecycle(Enum):
    UPLOADED = "Uploaded"
    REGISTERED = "Registered"
    CLASSIFIED = "Classified"
    PARSED = "Parsed"
    INDEXED = "Indexed"
    LINKED = "Linked"
    VALIDATED = "Validated"
    READY = "Ready"
    ARCHIVED = "Archived"

@dataclass(frozen=True)
class CapabilityRequirement:
    capability_name: str
    required_types: List[DocumentClassification]
    optional_types: List[DocumentClassification] = field(default_factory=list)

@dataclass(frozen=True)
class DocumentRelationship:
    from_doc_id: str
    to_doc_id: str
    rel_type: str  # "supports", "governs", "supersedes", "validates"

@dataclass(frozen=True)
class DocumentMetadata:
    file_path: str
    extension: str
    file_size_bytes: int
    content_hash: str
    workspace_context: str
    revision_ver: Optional[str] = None
    custom_properties: Dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class DocumentCompleteness:
    project_type: str
    expected_types: List[DocumentClassification]
    actual_types: List[DocumentClassification]
    missing_types: List[DocumentClassification]
    score: float

@dataclass
class Document:
    document_id: str
    workspace_id: str
    name: str
    classification: DocumentClassification
    lifecycle: DocumentLifecycle
    metadata: DocumentMetadata
    relationships: List[DocumentRelationship] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
