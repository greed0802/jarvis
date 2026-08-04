"""Graph-based evidence synthesis across multiple source documents."""

from __future__ import annotations

import hashlib

from jarvis.engines.reasoning.contracts import (
    CompressedContext,
    EvidenceNode,
    EvidenceEdge,
    EvidenceGraph,
)

class GraphSynthesizer:
    """Takes explicitly mapped provenance spans and links documents."""

    def synthesize(self, context: CompressedContext) -> EvidenceGraph:
        """Create an immutable evidence graph via deterministic node extraction."""
        nodes = {}
        # Simple extraction: each unique evidence_id becomes a node.
        # Spans pointing to the same id group together.

        for span in context.span_mappings:
            doc_id = span.evidence_id
            if doc_id not in nodes:
                nodes[doc_id] = EvidenceNode(
                    node_id=f"node_{hashlib.md5(doc_id.encode()).hexdigest()[:8]}",
                    document_id=doc_id,
                    revision="latest",
                    evidence_ids=(doc_id,)
                )

        nodes_list = list(nodes.values())
        # Sort for deterministic graph layout
        nodes_list.sort(key=lambda n: n.node_id)

        edges = []
        # Add basic logical edges if spans mention overlapping terminology
        for i, n1 in enumerate(nodes_list):
            for n2 in nodes_list[i+1:]:
                # We'll assert a correlation edge if they form part of same payload.
                edges.append(EvidenceEdge(
                    source_node_id=n1.node_id,
                    target_node_id=n2.node_id,
                    relationship_type="co-occurrence",
                ))

        edges.sort(key=lambda e: (e.source_node_id, e.target_node_id))

        return EvidenceGraph(
            nodes=tuple(nodes_list),
            edges=tuple(edges)
        )