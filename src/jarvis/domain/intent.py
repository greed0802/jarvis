"""Intent Domain Model."""
from dataclasses import dataclass, field
from typing import Any, Optional

@dataclass(frozen=True)
class IntentSemantics:
    """Structured semantic classification of user intent.
    
    Every user request is classified into:
    - intent_type: What kind of operation (QUERY, EXECUTE, CREATE, etc.)
    - target: What domain or entity (Workspace, Artifact, Knowledge, etc.)
    - action: What specific action (Describe, List, Run, etc.)
    - object: Optional specific object being referenced
    
    Examples:
        "What project am I working on?"
        → QUERY / Workspace / Describe / project
        
        "List uploaded files"
        → QUERY / Artifact / List / files
        
        "Run BOQ Intelligence"
        → EXECUTE / Capability / Run / BOQ Intelligence
    """
    intent_type: str  # QUERY, EXECUTE, CREATE, UPDATE, DELETE, EXPLAIN, SEARCH, SUMMARIZE
    target: str       # Workspace, Artifact, Knowledge, Memory, Capability, AI
    action: str       # Describe, List, Show, Run, Create, Update, Delete, etc.
    object: Optional[str] = None  # Specific object being referenced


@dataclass(frozen=True)
class Intent:
    """Consumes Context. Structured understanding of user's objective."""
    intent_id: str
    context_id: str
    goal: str
    parameters: dict[str, Any] = field(default_factory=dict)
    semantics: Optional[IntentSemantics] = None  # Added for semantic routing
