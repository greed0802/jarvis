"""Protocol interfaces decoupling generation pipeline components."""

from __future__ import annotations

from typing import Protocol, runtime_checkable, Any

from jarvis.contracts.assistant import AssistantResponse, GroundingContext
from jarvis.engines.generation.contracts import ProviderCapabilities, GenerationTrace

@runtime_checkable
class BaseProviderClient(Protocol):
    """Low-level SDK/network wrapper. Defines the generic execution boundary."""

    def send_request(
        self, prompt: str, system_prompt: str | None, config: dict[str, Any]
    ) -> dict[str, Any]:
        """Execute text generation synchronously against an external endpoint."""
        ...

@runtime_checkable
class BaseGenerationProvider(Protocol):
    """High-level provider adapter enforcing platform constraints."""

    @property
    def provider_id(self) -> str:
        """Vendor-specific identifier for the adapter."""
        ...

    @property
    def capabilities(self) -> ProviderCapabilities:
        """Statically declared implementation capabilities."""
        ...

    def generate(self, context: GroundingContext) -> tuple[AssistantResponse, GenerationTrace]:
        """Produce highly constrained AssistantResponse wrapping low-level client."""
        ...