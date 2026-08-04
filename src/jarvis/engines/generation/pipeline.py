"""Composition root for Generation Architecture."""

from __future__ import annotations

import time
from uuid import uuid4

from jarvis.engines.retrieval.contracts import RetrievalTrace
from jarvis.engines.reasoning.contracts import ReasoningTrace
from jarvis.contracts.assistant import GroundingContext
from jarvis.engines.generation.protocols import BaseGenerationProvider
from jarvis.contracts.assistant import AssistantResponse
from jarvis.engines.generation.contracts import ExecutionTrace, GenerationTrace

class GenerationPipeline:
    """Canonical Generation Pipeline orchestrating providers and execution trace."""

    def __init__(self, provider: BaseGenerationProvider):
        """Inject any BaseGenerationProvider."""
        self._provider = provider

    def process(
        self,
        context: GroundingContext,
        retrieval_trace: RetrievalTrace,
        reasoning_trace: ReasoningTrace,
    ) -> tuple[AssistantResponse, ExecutionTrace]:
        """Executes generation and wraps the response inside an ExecutionTrace observer."""
        start = time.time()
        session_id = f"exec_{uuid4().hex[:12]}"

        # BaseGenerationProvider implements generate() according to protocols
        # It handles normalizing raw outputs -> AssistantResponse & GenerationTrace
        resp, gen_trace = self._provider.generate(context)

        end = time.time()
        # Create observer aggregating these traces strictly, no mutation occurs
        exec_trace = ExecutionTrace(
            session_id=session_id,
            retrieval_trace=retrieval_trace,
            reasoning_trace=reasoning_trace,
            generation_trace=gen_trace,
            total_latency_ms=round((end - start) * 1000, 1),
            timestamp=str(int(start)),
        )

        return resp, exec_trace
