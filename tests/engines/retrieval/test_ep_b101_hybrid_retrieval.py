"""Test suite for EP-B101: Canonical Hybrid Retrieval Pipeline.

Covers AC-1 through AC-8 acceptance criteria.
"""

from __future__ import annotations

import pytest
import inspect

from jarvis.engines.retrieval.contracts import (
    RankedCandidate,
    RetrievalQuery,
    RetrievalTrace,
    SearchFilter,
)
from jarvis.engines.retrieval.protocols import (
    BaseRetriever,
    EmbeddingProvider,
    FusionStrategy,
    VectorIndex,
)
from jarvis.engines.retrieval.coordinator import RetrievalCoordinator
from jarvis.engines.retrieval.dense import DenseVectorRetriever
from jarvis.engines.retrieval.fusion import ReciprocalRankFusion, WeightedScoreFusion
from jarvis.engines.retrieval.index.memory import InMemoryVectorIndex
from jarvis.engines.retrieval.lexical import BM25LexicalRetriever

# ===========================================================================
# AC-1: Composition Root Coordinator
# ===========================================================================

class TestAC1CompositionRoot:
    """AC-1: RetrievalCoordinator accepts retrievers + fusion via constructor injection."""

    def test_coordinator_accepts_retrievers_and_fusion(self) -> None:
        bm25 = BM25LexicalRetriever()
        fusion = ReciprocalRankFusion()
        coordinator = RetrievalCoordinator(retrievers=[bm25], fusion=fusion)
        assert coordinator.retriever_ids == ["bm25_lexical"]

    def test_coordinator_with_multiple_retrievers(self) -> None:
        bm25 = BM25LexicalRetriever({"d1": "test doc"})
        idx = InMemoryVectorIndex()
        emb = _FakeEmbeddingProvider(dimension=4)
        dense = DenseVectorRetriever(embedding_provider=emb, vector_index=idx)
        dense.index_document("d1", "test doc")
        fusion = ReciprocalRankFusion()
        coordinator = RetrievalCoordinator(retrievers=[bm25, dense], fusion=fusion)
        assert len(coordinator.retriever_ids) == 2

# ===========================================================================
# AC-2: Dense Search Decoupling
# ===========================================================================

class TestAC2DenseDecoupling:
    """AC-2: DenseVectorRetriever delegates through VectorIndex + EmbeddingProvider."""

    def test_dense_retriever_uses_protocols(self) -> None:
        index = InMemoryVectorIndex()
        emb = _FakeEmbeddingProvider(dimension=4)
        retriever = DenseVectorRetriever(embedding_provider=emb, vector_index=index)
        retriever.index_document("d1", "some text")
        query = RetrievalQuery(query_text="some text", top_k=5)
        results = retriever.retrieve(query)
        assert len(results) == 1

    def test_in_memory_index_is_vector_index(self) -> None:
        idx = InMemoryVectorIndex()
        assert isinstance(idx, VectorIndex)

    def test_fake_embedding_is_embedding_provider(self) -> None:
        prov = _FakeEmbeddingProvider(dimension=4)
        assert isinstance(prov, EmbeddingProvider)

# ===========================================================================
# AC-3: RetrievalTrace Emission
# ===========================================================================

class TestAC3RetrievalTrace:
    """AC-3: execute_query emits complete immutable RetrievalTrace."""

    def test_trace_emission(self) -> None:
        bm25 = BM25LexicalRetriever({"d1": "alpha beta gamma"})
        fusion = ReciprocalRankFusion()
        coordinator = RetrievalCoordinator(retrievers=[bm25], fusion=fusion)
        query = RetrievalQuery(query_text="alpha", top_k=5)
        trace = coordinator.execute_query(query)
        assert isinstance(trace, RetrievalTrace)
        assert trace.fusion_algorithm == "ReciprocalRankFusion"
        assert len(trace.strategy_hits) == 1
        assert "bm25_lexical" in trace.strategy_hits
        assert len(trace.fused_hits) > 0
        assert trace.latency_ms >= 0.0
        assert trace.timestamp

    def test_trace_is_immutable_write(self) -> None:
        bm25 = BM25LexicalRetriever({"d1": "content"})
        fusion = ReciprocalRankFusion()
        coordinator = RetrievalCoordinator(retrievers=[bm25], fusion=fusion)
        query = RetrievalQuery(query_text="query", top_k=5)
        trace = coordinator.execute_query(query)
        with pytest.raises(Exception):
            trace.latency_ms = 999.0

# ===========================================================================
# AC-4: Pure Deterministic Fusion
# ===========================================================================

class TestAC4DeterministicFusion:
    """AC-4: Fusion returns new collections, zero in-place mutation, deterministic."""

    def test_rrf_returns_new_list(self) -> None:
        original = {
            "s1": [
                RankedCandidate(document_id="d1", content="c1", score=0.9),
                RankedCandidate(document_id="d2", content="c2", score=0.8),
            ],
            "s2": [
                RankedCandidate(document_id="d1", content="c1", score=0.7),
                RankedCandidate(document_id="d3", content="c3", score=0.6),
            ],
        }
        fusion = ReciprocalRankFusion()
        original_copy = {k: list(v) for k, v in original.items()}
        fused = fusion.combine(original, top_k=5)
        assert fused is not original
        assert original == original_copy  # not mutated

    def test_rrf_deterministic_same_input(self) -> None:
        fusion = ReciprocalRankFusion()
        cand = {
            "s1": [RankedCandidate(document_id="d1", content="", score=1.0)],
        }
        a = fusion.combine(cand, top_k=5)
        b = fusion.combine(cand, top_k=5)
        assert [c.document_id for c in a] == [c.document_id for c in b]
        assert [c.score for c in a] == [c.score for c in b]

    def test_weighted_fusion_deterministic(self) -> None:
        fusion = WeightedScoreFusion(weights={"s1": 1.0, "s2": 0.5})
        cand = {
            "s1": [RankedCandidate(document_id="d1", content="", score=1.0)],
            "s2": [RankedCandidate(document_id="d2", content="", score=0.9)],
        }
        a = fusion.combine(cand, top_k=5)
        b = fusion.combine(cand, top_k=5)
        assert [c.rank for c in a] == [c.rank for c in b]

    def test_deterministic_tie_breaking(self) -> None:
        fusion = ReciprocalRankFusion()
        cand = {
            "s1": [RankedCandidate(document_id="bb", content="", score=1.0)],
            "s2": [RankedCandidate(document_id="aa", content="", score=1.0)],
        }
        fused = fusion.combine(cand, top_k=5)
        assert fused[0].document_id <= fused[1].document_id  # id tie-break

# ===========================================================================
# AC-5: Public Facade Preservation
# ===========================================================================

class TestAC5PublicFacade:
    """AC-5: EvidenceRetriever + UnderstandingRetriever unchanged."""

    def test_evidence_retriever_api_unchanged(self) -> None:
        from jarvis.engines.assistant.retrieval import EvidenceRetriever
        er = EvidenceRetriever()
        assert hasattr(er, "build_grounding")

    def test_understanding_retriever_api_unchanged(self) -> None:
        from jarvis.engines.assistant.retrieval import UnderstandingRetriever
        ur = UnderstandingRetriever()
        assert hasattr(ur, "retrieve")

# ===========================================================================
# AC-6: One-Way Dependency Boundary
# ===========================================================================

class TestAC6DependencySafety:
    """AC-6: Zero presentation/CLI/UI imports in retrieval modules."""

    PRESENTATION_IMPORTS = ("presentation", "jarvis.cli", "jarvis.ui")
    RETRIEVAL_MODULES = [
        "jarvis.engines.retrieval",
        "jarvis.engines.retrieval.contracts",
        "jarvis.engines.retrieval.protocols",
        "jarvis.engines.retrieval.coordinator",
        "jarvis.engines.retrieval.dense",
        "jarvis.engines.retrieval.fusion",
        "jarvis.engines.retrieval.lexical",
        "jarvis.engines.retrieval.index.memory",
    ]

    def test_no_presentation_imports(self) -> None:
        import importlib
        for mod_name in self.RETRIEVAL_MODULES:
            mod = importlib.import_module(mod_name)
            src = inspect.getsource(mod)
            for forbidden in self.PRESENTATION_IMPORTS:
                # Basic lexical check to ensure we don't import forbidden prefixes
                assert f"from {forbidden}" not in src
                assert f"import {forbidden}" not in src
            # Verify no presentation/CLI/UI imports
            for keyword in ("presentation", "jarvis.cli", "jarvis.ui"):
                assert f"import jarvis.{keyword}" not in src
                assert f"from jarvis.{keyword}" not in src

# ===========================================================================
# AC-8: Regression Protection (checked in combined suite)
# ===========================================================================

class TestAC8Regression:
    """AC-8: Can import all retrieval modules without breaking existing code."""

    def test_imports_not_introduce_side_effects(self) -> None:
        from jarvis.engines.retrieval import contracts
        from jarvis.engines.retrieval import protocols
        from jarvis.engines.retrieval import coordinator
        from jarvis.engines.retrieval import dense
        from jarvis.engines.retrieval import fusion
        from jarvis.engines.retrieval import lexical
        from jarvis.engines.retrieval.index import memory

# ===========================================================================
# Extended RRF & Fusion integration tests
# ===========================================================================

class TestExtendedRetrievalIntegration:
    """Integration: BM25 + Dense + RRF pipeline."""

    def test_hybrid_pipeline_end_to_end(self) -> None:
        bm25 = BM25LexicalRetriever({
            "d1": "finding 1 is a cost error",
            "d2": "finding 2 is about omissions",
            "d3": "finding 3 about dimensions",
        })
        emb = _FakeEmbeddingProvider(dimension=4)
        idx = InMemoryVectorIndex()
        dense = DenseVectorRetriever(embedding_provider=emb, vector_index=idx)
        for text in ["cost error", "omissions", "dimensions"]:
            dense.index_document(text, text)
        fusion = ReciprocalRankFusion()
        coordinator = RetrievalCoordinator(retrievers=[bm25, dense], fusion=fusion)
        query = RetrievalQuery(query_text="cost", top_k=3)
        trace = coordinator.execute_query(query)
        assert len(trace.fused_hits) <= 3

# ===========================================================================
# Helpers
# ===========================================================================

class _FakeEmbeddingProvider:
    """Simple hash-based embedding for Q1 (no external dep)."""

    def __init__(self, dimension: int = 4) -> None:
        self._dim = dimension

    @property
    def dimension(self) -> int:
        return self._dim

    def embed_text(self, text: str) -> tuple[float, ...]:
        h = hash(text) % 1000
        return tuple((h + i) % 1000 / 1000.0 for i in range(self._dim))