"""Immutable generation contracts, capabilities, and trace artifacts."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from jarvis.engines.retrieval.contracts import RetrievalTrace
from jarvis.engines.reasoning.contracts import ReasoningTrace

@dataclass(frozen=True)
class ProviderCapabilities:
    """Explicit capability semantics per ES-C101."""
    supports_streaming: bool
    supports_tools: bool
    supports_images: bool
    supports_json: bool
    supports_system_prompt: bool

@dataclass(frozen=True)
class ProviderMetadata:
    """Metadata describing the provider and execution parameters."""
    provider_name: str
    model_name: str
    capabilities: ProviderCapabilities
    temperature: float
    max_tokens: int

@dataclass(frozen=True)
class TokenUsage:
    """Standardized token cost reporting."""
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

@dataclass(frozen=True)
class GenerationTrace:
    """Immutable per-query generation execution record."""
    trace_id: str
    provider_metadata: ProviderMetadata
    token_usage: TokenUsage
    finish_reason: str
    latency_ms: float
    timestamp: str

@dataclass(frozen=True)
class ExecutionTrace:
    """Application-level observer aggregating all linear trace artifacts.
    Note: Promoted from the presentation mapping -> canonical lifecycle container.
    """
    session_id: str
    retrieval_trace: RetrievalTrace
    reasoning_trace: ReasoningTrace
    generation_trace: GenerationTrace
    total_latency_ms: float
    timestamp: str