"""Context compressor logic mapping compressed strings to source evidence."""

from __future__ import annotations

import re

from jarvis.engines.reasoning.contracts import (
    ReRankedCandidate,
    CompressionSpanMap,
    CompressedContext,
)

class TokenWindowCompressor:
    """Takes leading sentences up to max_tokens (approx words)."""

    def compress(self, candidates: tuple[ReRankedCandidate, ...], max_tokens: int) -> CompressedContext:
        token_count = 0
        final_text = []
        span_mappings = []
        evidence_ids = set()

        for rcand in candidates:
            if token_count >= max_tokens:
                break
            
            cand = rcand.candidate
            sentences = [s.strip() + "." for s in re.split(r"(?<=[.!?]) +", cand.content) if s.strip()]
            
            for sentence in sentences:
                words = len(sentence.split())
                if token_count + words > max_tokens:
                    break
                
                final_text.append(sentence)
                token_count += words
                
                # Full sentence mapping
                span_mappings.append(CompressionSpanMap(
                    original_span=sentence,
                    compressed_span=sentence,
                    evidence_id=cand.document_id,
                ))
                evidence_ids.add(cand.document_id)

        compressed_text = " ".join(final_text)
        return CompressedContext(
            target_max_tokens=max_tokens,
            compressed_text=compressed_text,
            span_mappings=tuple(span_mappings),
            preserved_evidence_ids=tuple(sorted(evidence_ids)),
        )

class DeduplicatingCompressor:
    """Compresses by discarding sentences with heavily overlapping words (Jaccard similarity)."""

    def __init__(self, threshold: float = 0.6):
        self.threshold = threshold

    def compress(self, candidates: tuple[ReRankedCandidate, ...], max_tokens: int) -> CompressedContext:
        token_count = 0
        final_text = []
        span_mappings = []
        evidence_ids = set()
        seen_vocab_sets = []

        for rcand in candidates:
            if token_count >= max_tokens:
                break
            cand = rcand.candidate
            sentences = [s.strip() + "." for s in re.split(r"(?<=[.!?]) +", cand.content) if s.strip()]

            for sentence in sentences:
                words = sentence.split()
                if token_count + len(words) > max_tokens:
                    break

                # Deduplication logic
                # Clean punctuation for fairer vocab comparison
                clean_words = []
                for w in words:
                    cleaned = re.sub(r'[^\w\s]', '', w.lower())
                    if cleaned:
                        clean_words.append(cleaned)
                        
                vocab = set(clean_words)
                is_duplicate = False
                for seen in seen_vocab_sets:
                    union = len(vocab | seen)
                    intersection = len(vocab & seen)
                    if union > 0 and (intersection / union) > self.threshold:
                        is_duplicate = True
                        break
                
                if not is_duplicate:
                    seen_vocab_sets.append(vocab)
                    final_text.append(sentence)
                    token_count += len(words)
                    
                    span_mappings.append(CompressionSpanMap(
                        original_span=sentence,
                        compressed_span=sentence,
                        evidence_id=cand.document_id,
                    ))
                    evidence_ids.add(cand.document_id)

        compressed_text = " ".join(final_text)
        return CompressedContext(
            target_max_tokens=max_tokens,
            compressed_text=compressed_text,
            span_mappings=tuple(span_mappings),
            preserved_evidence_ids=tuple(sorted(evidence_ids)),
        )