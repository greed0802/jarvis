"""Ollama high-level provider adapter enforcing platform constraints."""

import time
from uuid import uuid4

from jarvis.contracts.assistant import AssistantResponse, GroundingContext, GroundingStatus
from jarvis.engines.generation.contracts import (
    ProviderCapabilities,
    ProviderMetadata,
    TokenUsage,
    GenerationTrace,
)
from jarvis.engines.generation.clients.base import BaseProviderClient

class OllamaProvider:
    """Enforces Ollama message schemas and output isolation."""

    def __init__(self, client: BaseProviderClient):
        self._client = client
        self.config = {"temperature": 0.0, "max_tokens": 1500}

    @property
    def provider_id(self) -> str:
        return "ollama"

    @property
    def capabilities(self) -> ProviderCapabilities:
        return ProviderCapabilities(
            supports_streaming=True,
            supports_tools=False,
            supports_images=False,
            supports_json=True,
            supports_system_prompt=True,
        )

    def generate(self, context: GroundingContext) -> tuple[AssistantResponse, GenerationTrace]:
        start = time.time()
        trace_id = f"gen_{uuid4().hex[:8]}"

        raw = self._client.send_request(
            prompt=context.formatted_prompt_payload,
            system_prompt="Ollama instructions",
            config=self.config
        )

        resp = AssistantResponse(
            response_id=f"resp_{trace_id}",
            query_text="", 
            response_text=raw["text"],
            grounding_status=GroundingStatus.PARTIALLY_GROUNDED,
            cited_evidence=context.retrieved_evidence,
            confidence_score=0.70,
        )

        usage = TokenUsage(
            prompt_tokens=raw["usage"]["prompt_tokens"],
            completion_tokens=raw["usage"]["completion_tokens"],
            total_tokens=raw["usage"]["total_tokens"],
        )

        end = time.time()
        trace = GenerationTrace(
            trace_id=trace_id,
            provider_metadata=ProviderMetadata(
                provider_name="ollama",
                model_name="llama3",
                capabilities=self.capabilities,
                temperature=self.config["temperature"],
                max_tokens=self.config["max_tokens"],
            ),
            token_usage=usage,
            finish_reason=raw["finish_reason"],
            latency_ms=round((end - start)*1000, 1),
            timestamp=str(int(start))
        )
        return resp, trace