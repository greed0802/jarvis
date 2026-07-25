# EQ-0010 — Spike 4 — Evidence Report — Hierarchy Reconstruction

**Date:** 2026-07-14  
**Status:** Complete — Revised (Accepted with Amendments)  
**Investigation:** EQ-0010 Deterministic BOQ Structural Intelligence  
**Governance:** Engineering_Governance.md v1.0

---

## Objective

Given a linear BOQRow sequence with Head1-5 labels, can a deterministic stack-based reconstruction algorithm build a heading tree from the sequence?

---

## Algorithm

**Deterministic stack-based reconstruction algorithm:**

1. When a Head row is encountered, extract its numeric level from the UOM string (Head1→1, Head2→2, etc.)
2. Pop headers from the stack while the top's level is ≥ the current header's level
3. If the stack is non-empty after popping, the new header becomes a child of the current stack top
4. If the stack is empty, the new header becomes a root-level tree entry
5. Push the new header onto the stack
6. When an Item row is encountered, add it to the current stack top's children

---

## Outcome: Determinism Verified

**Run 1 == Run 2: True**

The reconstruction algorithm produces identical trees on repeated execution.

---

## Scope of This Spike

This spike implements and tests the reconstruction algorithm. It does **not** validate the reconstructed tree against BOQ domain semantics. Algorithmic correctness (does the algorithm run deterministically?) is established. Semantic correctness (does the tree match Quantity Surveying intent?) is deferred to Spike 5 (Domain Reconciliation).

---

## Results

### 1. Reconstruction Statistics

| Measure | Value |
|---------|-------|
| Total headers placed in tree | 2011 |
| Root headers | 294 |
| Items with empty-stack stack-empty items | 0 |
| Algorithm runs deterministically | Yes (Run 1 == Run 2) |

**Finding:** The deterministic stack-based reconstruction algorithm successfully processes all 6,349 rows and places all 2011 Head rows into a tree structure. Zero items were encountered with an empty stack.

### 2. Depth Distribution (Computed by Algorithm)

| Computed Depth | Headers |
|----------------|---------|
| 1 | 294 |
| 2 | 397 |
| 3 | 639 |
| 4 | 621 |
| 5 | 60 |

Depth is a property of the reconstruction algorithm, not an independent observation. The algorithm assigns depth by counting stack depth when a header is pushed.

### 3. Label vs Computed Depth Cross-Reference

| Label | Depth 1 | Depth 2 | Depth 3 | Depth 4 | Depth 5 |
|-------|---------|---------|---------|---------|---------|
| Head1 | 294 | 0 | 0 | 0 | 0 |
| Head2 | 0 | 394 | 0 | 0 | 0 |
| Head3 | 0 | 3 | 624 | 0 | 0 |
| Head4 | 0 | 0 | 15 | 621 | 0 |
| Head5 | 0 | 0 | 0 | 0 | 60 |

**Finding:** The reconstruction algorithm computes depth from the label. The majority of cases follow label→depth expectation (Head1→D1, Head2→D2, Head3→D3, Head4→D4, Head5→D5). The exceptions (Head3 at depth 2: 3 occurrences; Head4 at depth 3: 15 occurrences) are notable because they occur when a header with a high numeric label appears immediately after a header with a lower numeric label at a sibling position — e.g., Head3 following Head2 at the same level rather than as a child. These exceptions reveal the algorithm's behavior under specific sequence patterns.

### 4. Parent-Child Mappings (Algorithmic Assignment)

The reconstruction algorithm assigns parent relationships under the stack rule:

| Parent Label | Child Labels (via algorithm) |
|--------------|------------------------------|
| Head1 | Head2, Head3 |
| Head2 | Head3, Head4 |
| Head3 | Head4 |
| Head4 | Head5 |

**Finding:** These are algorithmic parent assignments, not validated BOQ semantic relationships. The algorithm assigns a parent when a new header becomes a child of the current stack top. Whether these correspond to intended BOQ parent-child semantics is investigated in Spike 5.

### 5. Root Headers

Under the reconstruction algorithm, all 294 root headers are Head1. No Head2+ appears as a root-level entry under the algorithm's rule (stack empty = root).

### 6. Items Per Header (Average)

| Header | Avg Items | Total Items |
|--------|-----------|-------------|
| Head1 | 1.28 | 376 |
| Head2 | 0.66 | 259 |
| Head3 | 1.71 | 1075 |
| Head4 | 2.80 | 1780 |
| Head5 | 1.92 | 115 |

**Finding:** Items-per-header ratio is a deterministic computation from the reconstructed tree. The algorithm counts immediate Item children of each header node.

### 7. Tree Shape Diversity

The reconstruction algorithm produced 27 distinct patterns at the root level when characterized by (root Header UOM, number of direct child headers, number of immediate Items). This statistic describes algorithmic output variation only.

---

## Capability State Transitions

| Candidate Engineering Capability | Previous State | New State | Evidence |
|----------------------------------|---------------|-----------|----------|
| Hierarchy depth | Unknown | **Derivable** | Stack algorithm computes depth from label |
| Parent header identification | Unknown | **Derivable** | Stack pop rule assigns parent deterministically |
| Heading tree structure | Unknown | **Derivable** | Algorithm reconstructs a tree from the sequence |
| Items-per-header ratio | Unknown | **Derivable** | Deterministic tree traversal counts children |
| Orphan item detection | Unknown | **Unknown** | Stack-empty items = 0, but semantic orphan definition requires Spike 5 |

**Engineering finding:** The deterministic stack-based reconstruction algorithm is demonstrated to deterministically reconstruct a heading tree from BOQRow sequences. Subject to successful domain reconciliation (Spike 5), it is the current candidate reconstruction algorithm.

---

## Production Applicability

**Derivable capabilities (ready for implementation):**
- **Hierarchy depth:** Computable via stack depth during reconstruction
- **Parent header identification:** Assignable via stack pop rule
- **Heading tree structure:** Reconstructable via algorithm
- **Items-per-header ratio:** Deterministic from tree

**Pending capabilities (require Spike 5):**
- **Orphan item detection:** Semantic definition needed before algorithm can be validated

---

## Tool

This spike was executed via `tools/eq0010_spike4_hierarchy_reconstruction.py`.

---

## Evidence Immutability

This evidence report is frozen. No modifications permitted after publication.