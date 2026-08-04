"""Test suite for EP-B102: Canonical Reasoning Architecture."""

from __future__ import annotations

import inspect
import pytest

from jarvis.engines.retrieval.contracts import RankedCandidate, RetrievalQuery, RetrievalTrace
from jarvis.contracts.assistant import GroundingContext
from jarvis.engines.reasoning.contracts import (
    ReRankedCandidate,
    CompressionSpanMap,
    CompressedContext,
    EvidenceGraph,
    ReasoningTrace,
)
from jarvis.engines.reasoning.protocols import BaseReRanker, ContextCompressor, MultiDocumentSynthesizer
from jarvis.engines.reasoning.pipeline import ReasoningPipeline
from jarvis.engines.reasoning.reranker import HeuristicReRanker, ModelReRanker
from jarvis.engines.reasoning.compressor import TokenWindowCompressor, DeduplicatingCompressor
from jarvis.engines.reasoning.synthesizer import GraphSynthesizer

# ===========================================================================
# AC-1: Composition Root Coordinator
# ===========================================================================

class TestAC1CompositionRoot:
    """ReasoningPipeline takes implementations via injection, executes without LLM."""

    def test_pipeline_composition(self) -> None:
        reranker = HeuristicReRanker()
        compressor = TokenWindowCompressor()
        synthesizer = GraphSynthesizer()
        pipeline = ReasoningPipeline(reranker, compressor, synthesizer)
        assert pipeline._reranker is reranker
        assert pipeline._compressor is compressor
        assert pipeline._synthesizer is synthesizer

# ===========================================================================
# AC-2: Model-Neutral Re-Ranker Protocol
# ===========================================================================

class TestAC2ReRanker:
    """Implementations adhere to BaseReRanker protocol and return correct artifacts."""

    def test_heuristic_reranker_adherence(self) -> None:
        rr = HeuristicReRanker()
        assert isinstance(rr, BaseReRanker)
        cands = (RankedCandidate("d1", "test content match", 0.5, 1, "test"),)
        res = rr.rerank(cands, "test match")
        assert len(res) == 1
        assert isinstance(res[0], ReRankedCandidate)
        assert res[0].rerank_score > 0.5  # density added

    def test_model_reranker_adherence(self) -> None:
        mr = ModelReRanker()
        assert isinstance(mr, BaseReRanker)
        cands = (RankedCandidate("d1", "content", 0.5, 1, "test"),)
        res = mr.rerank(cands, "")
        assert res[0].rerank_score == 0.5 * 1.5

# ===========================================================================
# AC-3: Span Provenance Tracking
# ===========================================================================

class TestAC3SpanProvenance:
    """Compressors maintain accurate CompressionSpanMap provenance."""

    def test_token_window_compressor_provenance(self) -> None:
        comp = TokenWindowCompressor()
        rc1 = ReRankedCandidate(RankedCandidate("d1", "A simple sent. Another sent.", 1.0), 1.0, 1)
        rc2 = ReRankedCandidate(RankedCandidate("d2", "Third sent.", 0.9), 0.9, 2)

        res = comp.compress((rc1, rc2), 10)
        assert isinstance(res, CompressedContext)
        # Should contain mapping for sentences from both docs
        assert len(res.span_mappings) > 1
        assert res.span_mappings[0].evidence_id == "d1"
        assert res.span_mappings[-1].evidence_id == "d2"
        assert "A simple sent." in res.span_mappings[0].original_span
        assert set(res.preserved_evidence_ids) == {"d1", "d2"}

    def test_dedup_compressor_filters_overlap(self) -> None:
        comp = DeduplicatingCompressor(threshold=0.5)
        # Duplicate sets of words
        rc1 = ReRankedCandidate(RankedCandidate("d1", "Important cost finding.", 1.0), 1.0, 1)
        rc2 = ReRankedCandidate(RankedCandidate("d2", "Finding about cost important.", 0.9), 0.9, 2)

        res = comp.compress((rc1, rc2), 20)
        # Should deduplicate rc2's content due to overlap
        assert len(res.span_mappings) == 1
        assert res.span_mappings[0].evidence_id == "d1"

# ===========================================================================
# AC-4: Immutable Graph-Based Synthesis
# ===========================================================================

class TestAC4EvidenceGraph:
    """GraphSynthesizer creates frozen tuple-based graph representations."""

    def test_graph_synthesis_is_immutable(self) -> None:
        comp_context = CompressedContext(
            target_max_tokens=100,
            compressed_text="test text",
            span_mappings=(
                CompressionSpanMap("s1", "s1", "d1"),
                CompressionSpanMap("s2", "s2", "d2"),
            ),
            preserved_evidence_ids=("d1", "d2")
        )
        synth = GraphSynthesizer()
        graph = synth.synthesize(comp_context)

        assert isinstance(graph, EvidenceGraph)
        assert len(graph.nodes) == 2
        # Edges assert co-occurrence
        assert len(graph.edges) == 1

        with pytest.raises(Exception):
            # Graph immutability check
            graph.nodes = ()

# ===========================================================================
# AC-5: Grounding Context Import
# ===========================================================================

class TestAC5GroundingContextImport:
    def test_grounding_context_comes_from_contracts(self) -> None:
        # Asserts we are using the external contract, not defining our own
        import jarvis.contracts.assistant as asst
        import jarvis.engines.reasoning.pipeline as pipe
        assert pipe.GroundingContext is asst.GroundingContext

# ===========================================================================
# AC-6: Immutable ReasoningTrace Emission
# ===========================================================================

class TestAC6ReasoningTrace:
    def test_pipeline_trace_is_complete_and_immutable(self) -> None:
        pipeline = ReasoningPipeline(HeuristicReRanker(), TokenWindowCompressor(), GraphSynthesizer())

        ret_trace = RetrievalTrace(
            trace_id="rt_1",
            query=RetrievalQuery("test"),
            strategy_hits={},
            fused_hits=(RankedCandidate("d1", "test data", 1.0),),
            fusion_algorithm="None",
            latency_ms=1.0,
            timestamp="1"
        )

        trace = pipeline.process(ret_trace)
        assert isinstance(trace, ReasoningTrace)
        assert trace.retrieval_trace_id == "rt_1"
        assert trace.compressed_context.compressed_text
        assert trace.evidence_graph.nodes
        assert isinstance(trace.grounding_context, GroundingContext)

        with pytest.raises(Exception):
            trace.latency_ms = 0.0

# ===========================================================================
# AC-7: One-Way Dependency Boundary
# ===========================================================================

class TestAC7DependencyBoundary:
    def test_no_presentation_imports_in_reasoning(self) -> None:
        forbidden_imports = ("presentation", "jarvis.cli", "jarvis.ui")
        modules = [
            "jarvis.engines.reasoning",
            "jarvis.engines.reasoning.contracts",
            "jarvis.engines.reasoning.protocols",
            "jarvis.engines.reasoning.reranker",
            "jarvis.engines.reasoning.compressor",
            "jarvis.engines.reasoning.synthesizer",
            "jarvis.engines.reasoning.pipeline",
        ]

        import importlib
        for mod_name in modules:
            mod = importlib.import_module(mod_name)
            src = inspect.getsource(mod)
            for forbidden in forbidden_imports:
                assert f"from {forbidden}" not in src
                assert f"import jarvis.{forbidden}" not in src

# ===========================================================================
# AC-9: Byte-for-Byte Reproducibility
# ===========================================================================

class TestAC9Reproducibility:
    def test_intermediate_reproducibility(self) -> None:
        # Same input and configs MUST produce identical byte-for-byte structures
        ret_trace = RetrievalTrace(
            trace_id="rt_tied",
            query=RetrievalQuery("duplicate check"),
            strategy_hits={},
            fused_hits=(
                RankedCandidate("doc_A", "identical score", 0.5),
                RankedCandidate("doc_B", "identical score", 0.5),
            ),
            fusion_algorithm="None",
            latency_ms=1.0,
            timestamp="1"
        )

        pipeline1 = ReasoningPipeline(HeuristicReRanker(), TokenWindowCompressor(), GraphSynthesizer())
        pipeline2 = ReasoningPipeline(HeuristicReRanker(), TokenWindowCompressor(), GraphSynthesizer())

        t1 = pipeline1.process(ret_trace)
        t2 = pipeline2.process(ret_trace)

        # Re-Ranking order identical?
        assert [r.candidate.document_id for r in t1.reranked_candidates] == \
               [r.candidate.document_id for r in t2.reranked_candidates]

        # Compression maps identical?
        assert t1.compressed_context.compressed_text == t2.compressed_context.compressed_text

        # Graph identical?
        assert [n.node_id for n in t1.evidence_graph.nodes] == \
               [n.node_id for n in t2.evidence_graph.nodes]

        # Everything byte-for-byte matches except timestamps/uuids.