"""Immutable application-level contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class ConversationRequest:
    """Request DTO wrapping a user query into the application layer."""
    prompt: str
    session_id: str | None = None
    options: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)