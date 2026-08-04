"""Unified AI Request and Response Models."""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

@dataclass(frozen=True)
class AITool:
    """Provider-agnostic tool definition."""
    name: str
    description: str
    parameters_schema: Dict[str, Any]

@dataclass(frozen=True)
class AIMessage:
    """A single turn in the conversation."""
    role: str
    content: str
    tool_calls: Optional[List[Dict[str, Any]]] = None

@dataclass(frozen=True)
class AIRequest:
    """Unified AI Provider Request."""
    messages: List[AIMessage]
    model: str
    system_prompt: Optional[str] = None
    tools: List[AITool] = field(default_factory=list)
    temperature: float = 0.7
    stream: bool = False

@dataclass(frozen=True)
class AIResponse:
    """Unified AI Provider Response."""
    content: str
    model_used: str
    tool_calls: Optional[List[Dict[str, Any]]] = None
    usage: Dict[str, int] = field(default_factory=dict)
