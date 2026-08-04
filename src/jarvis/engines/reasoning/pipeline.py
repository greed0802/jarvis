"""Composition root for Reasoning Architecture."""

from __future__ import annotations

import time
from uuid import uuid4

from jarvis.engines.retrieval.contracts import RetrievalTrace
from jarvis.contracts.assistant import GroundingContext
from jarvis.contracts.understanding import UnderstandingFinding
from jarvis.contracts.capabilities import EvidenceReference

from jarvis.engines.reasoning.contracts import ReasoningTrace
from jarvis.engines.reasoning.protocols import (
    BaseReRanker,
    ContextCompressor,
    MultiDocumentSynthesizer,
)

class ReasoningPipeline:
    """Canonical Reasoning Pipeline (RetrievalTrace -> GroundingContext)."""

    def __init__(
        self,
        reranker: BaseReRanker,
        compressor: ContextCompressor,
        synthesizer: MultiDocumentSynthesizer,
    ) -> None:
        self._reranker = reranker
        self._compressor = compressor
        self._synthesizer = synthesizer

    def process(self, retrieval_trace: RetrievalTrace, max_tokens: int = 1500) -> ReasoningTrace:
        """Execute linear reasoning pipeline with zero LLM side effects."""
        start = time.time()
        trace_id = uuid4().hex[:12]

        # 1. Re-Rank
        reranked = self._reranker.rerank(
            candidates=retrieval_trace.fused_hits,
            query=retrieval_trace.query.query_text
        )

        # 2. Compress Context
        compressed = self._compressor.compress(
            candidates=reranked,
            max_tokens=max_tokens
        )

        # 3. Graph Synthesis
        graph = self._synthesizer.synthesize(context=compressed)

        # 4. Bind GroundingContext from contracts domain (AC-5)
        # Note: In reality EvidenceReference/UnderstandingFinding are fetched from actual state,
        # but EP-B102 reasoning uses explicit extraction from the trace.
        grounding = GroundingContext(
            context_id=f"ctx_{trace_id}",
            retrieved_context=None, # Typically populates from actual context
            retrieved_evidence=[],
            formatted_prompt_payload=compressed.compressed_text
        )

        end = time.time()

        # 5. Emit ReasoningTrace observation
        return ReasoningTrace(
            trace_id=trace_id,
            retrieval_trace_id=retrieval_trace.trace_id,
            reranked_candidates=reranked,
            compressed_context=compressed,
            evidence_graph=graph,
            grounding_context=grounding,
            latency_ms=round((end - start) * 1000, 1),
            timestamp=str(int(start)),
        )