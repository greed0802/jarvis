"""Jarvis reasoning pipeline — Track B2: Canonical Reasoning."""

from jarvis.engines.reasoning.contracts import (
    ReRankedCandidate,
    CompressionSpanMap,
    CompressedContext,
    EvidenceNode,
    EvidenceEdge,
    EvidenceGraph,
    ReasoningTrace,
)
from jarvis.engines.reasoning.protocols import (
    BaseReRanker,
    ContextCompressor,
    MultiDocumentSynthesizer,
)
from jarvis.engines.reasoning.pipeline import ReasoningPipeline
from jarvis.engines.reasoning.reranker import HeuristicReRanker, ModelReRanker
from jarvis.engines.reasoning.compressor import TokenWindowCompressor, DeduplicatingCompressor
from jarvis.engines.reasoning.synthesizer import GraphSynthesizer

__all__ = [
    "ReRankedCandidate",
    "CompressionSpanMap",
    "CompressedContext",
    "EvidenceNode",
    "EvidenceEdge",
    "EvidenceGraph",
    "ReasoningTrace",
    "BaseReRanker",
    "ContextCompressor",
    "MultiDocumentSynthesizer",
    "ReasoningPipeline",
    "HeuristicReRanker",
    "ModelReRanker",
    "TokenWindowCompressor",
    "DeduplicatingCompressor",
    "GraphSynthesizer",
]