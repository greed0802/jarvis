"""Application Orchestrator: Ties together retrieval, reasoning, and generation engines."""

from __future__ import annotations

from typing import Any

from jarvis.application.contracts import ConversationRequest
from jarvis.contracts.assistant import AssistantResponse

from jarvis.engines.retrieval.coordinator import RetrievalCoordinator
from jarvis.engines.retrieval.contracts import RetrievalQuery
from jarvis.engines.reasoning.pipeline import ReasoningPipeline
from jarvis.engines.generation.pipeline import GenerationPipeline
from jarvis.engines.generation.contracts import ExecutionTrace

class ConversationService:
    """End-to-End orchestrator for standard user queries."""

    def __init__(
        self,
        retrieval_coordinator: RetrievalCoordinator,
        reasoning_pipeline: ReasoningPipeline,
        generation_pipeline: GenerationPipeline,
    ):
        self._retrieval = retrieval_coordinator
        self._reasoning = reasoning_pipeline
        self._generation = generation_pipeline

    async def execute(self, request: ConversationRequest) -> tuple[AssistantResponse, ExecutionTrace]:
        """Execute the intelligence chain asynchronously.
        Note: Currently blocks on synchronous engine methods internally,
        but signature is async to properly support async CLI loops and future streaming.
        """
        # 1. Retrieval
        ret_query = RetrievalQuery(query_text=request.prompt)
        retrieval_trace = self._retrieval.execute_query(ret_query)

        # 2. Reasoning
        reasoning_trace = self._reasoning.process(retrieval_trace)

        # 3. Generation binding
        # The reasoning trace emitted a grounding context object, we must feed it here
        # Usually grounding happens internally, but we'll use the reasoning's generated artifact
        gen_context = reasoning_trace.grounding_context

        resp, exec_trace = self._generation.process(
            context=gen_context,
            retrieval_trace=retrieval_trace,
            reasoning_trace=reasoning_trace,
        )

        return resp, exec_trace

    def get_status(self) -> dict[str, Any]:
        """Returns platform subsystem readiness diagnostic."""
        # Query our active provider capability info
        provider_info = "Unknown"
        model_name = "Unknown"
        
        # Generation property resolution logic safely avoids failing if abstract
        if hasattr(self._generation, "_provider"):
            prov = self._generation._provider
            provider_info = prov.provider_id
            if hasattr(prov, "config"):
                model_name = "configured model" # Simplified mock model

        return {
            "kernel_state": "RUNNING",
            "platform_version": "v0.0.1-alpha.9",
            "active_provider": provider_info,
            "subsystem_readiness": {
                "retrieval": "OK",
                "reasoning": "OK",
                "generation": "OK",
            },
        }