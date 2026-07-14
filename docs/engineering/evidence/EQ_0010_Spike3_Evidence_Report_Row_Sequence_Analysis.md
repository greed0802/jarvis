# EQ-0010 — Spike 3 — Evidence Report — Row Sequence Analysis

**Date:** 2026-07-14  
**Status:** Complete — Accepted with Amendments  
**Investigation:** EQ-0010 Deterministic BOQ Structural Intelligence  
**Governance:** Engineering_Governance.md v1.0

---

## Objective

Investigate whether Head1-5 indicator labels plus row sequences can deterministically define structural relationships from BOQRow data.

---

## Outcome: Determinism Verified

**Run 1 == Run 2: True**

All sequence observations are deterministic and reproducible.

---

## Scope of This Spike

This spike performs **sequence analysis only**: observation of adjacency between rows, transition frequencies, and row type patterns. It does **not** perform hierarchy reconstruction (building a tree from stack or equivalent algorithm). The following capabilities are recognized as requiring a separate reconstruction algorithm and remain under investigation:

- Hierarchy depth (requires tree reconstruction)
- Parent header identification (requires parent assignment algorithm)
- Heading tree structure (requires tree builder algorithm)

---

## Observation 1: Row Type Transitions

16 distinct row type transition patterns observed in the production data.

| From | To | Count |
|------|----|-------|
| Item | Item | 2428 |
| Head | Item | 1177 |
| Item | Head | 1119 |
| Head | Head | 687 |
| Note | Note | 374 |
| Head | Note | 144 |
| Note | Head | 144 |
| Other | Other | 135 |
| Section | Head | 15 |
| Other | Section | 14 |

**Finding:** Row type transitions are deterministic patterns computable from adjacent rows.

---

## Observation 2: Head Numeric Adjacency

The Head UOM strings contain numeric suffixes (1-5). Adjacent Head transitions can be counted:

| From | To | Count |
|------|----|-------|
| Head4 | Head4 | 366 |
| Head2 | Head3 | 276 |
| Head3 | Head4 | 259 |
| Head3 | Head3 | 194 |
| Head1 | Head1 | 155 |
| Head4 | Head3 | 147 |
| Head1 | Head2 | 137 |
| Head3 | Head2 | 125 |
| Head4 | Head2 | 79 |
| Head2 | Head1 | 63 |
| Head2 | Head2 | 52 |
| Head3 | Head1 | 49 |
| Head5 | Head5 | 42 |
| Head4 | Head1 | 26 |
| Head4 | Head5 | 18 |
| Head5 | Head4 | 9 |
| Head5 | Head3 | 8 |
| Head1 | Head3 | 2 |
| Head2 | Head4 | 2 |
| Head5 | Head2 | 1 |

**Finding:** Adjacent transitions show patterns of numeric progression (N→N+1), numeric regression (N→N-1), and same-level (N→N). These are observed adjacency frequencies only. No tree structure is inferred.

**Numeric progression types (based on digit extracted from Head string):**

| Transition Pattern | Count |
|-------------------|-------|
| same_level (N→N) | 809 |
| deepen (N→N+1) | 690 |
| backtrack (N→N-1) | 344 |
| skip_backtrack (N→N-2 or more) | 163 |
| skip_deepen (N→N+2 or more) | 4 |

**Finding:** Adjacent numeric patterns are deterministically computable. N→N+1 is the most common directional pattern (690 occurrences). N→N is the most common overall pattern (809). These are sequence observations only.

---

## Observation 3: Head Adjacency → Next Row Type

| Head UOM | Head | Note | Item | Other |
|----------|------|------|------|-------|
| Head5 | 0 | 0 | 60 | 0 |
| Head4 | 18 | 0 | 618 | 0 |
| Head3 | 257 | 2 | 368 | 0 |
| Head2 | 273 | 41 | 80 | 0 |
| Head1 | 139 | 101 | 51 | 3 |

**Finding:** Lower-numbered Head strings (Head1, Head2) are more likely adjacent to another Head. Higher-numbered Head strings (Head4, Head5) are more likely adjacent to an Item. This is a sequence-frequency observation only.

---

## Observation 4: Empty Header Detection

A header is **empty** when zero Item rows follow it before the next Header, Section, or end of data.

| Head UOM | Empty Count | Total | Empty % |
|----------|------------|-------|---------|
| Head1 | 243 | 294 | 82.7% |
| Head2 | 314 | 394 | 79.7% |
| Head3 | 259 | 627 | 41.3% |
| Head4 | 18 | 636 | 2.8% |
| Head5 | 0 | 60 | 0.0% |
| **Total** | **834** | **2011** | **41.5%** |

**Finding:** Empty header detection is Derivable via a deterministic algorithm: scan forward from each Head row until the next Head, Section, or end; if no Item rows are encountered, the header is empty.

---

## Observation 5: Head-to-Item Immediate Adjacency

| Head UOM | Item Immediate | Total Head | Immediate % |
|----------|---------------|-----------|-------------|
| Head5 | 60 | 60 | 100.0% |
| Head4 | 618 | 636 | 97.2% |
| Head3 | 368 | 627 | 58.7% |
| Head2 | 80 | 394 | 20.3% |
| Head1 | 51 | 294 | 17.3% |

**Finding:** The adjacency frequency between Head strings and Item rows varies by Head numeric suffix. Head5 is adjacent to an Item in all 60 occurrences. This is an adjacency frequency observation only.

---

## Observation 6: Items Under Each Head UOM

| Head UOM | Item | m2 | no | m | m3 | t | item |
|----------|------|----|----|----|----|----|------|
| Head1 | 349 | 13 | 3 | 4 | 5 | 2 | 0 |
| Head2 | 2 | 56 | 168 | 26 | 7 | 0 | 0 |
| Head3 | 0 | 413 | 302 | 221 | 47 | 86 | 6 |
| Head4 | 0 | 695 | 431 | 203 | 358 | 93 | 0 |
| Head5 | 0 | 40 | 4 | 0 | 44 | 27 | 0 |

**Finding:** The distribution of Item UOMs varies by the Head UOM that precedes them. This spike records the observed frequencies only. No structural interpretation is applied.

---

## Capability State Transitions

| Candidate Engineering Capability | Previous State | New State | Evidence |
|----------------------------------|---------------|-----------|----------|
| Row type transitions | Unknown | **Derivable** | 16 deterministic patterns from adjacent rows |
| Empty header detection | Unknown | **Derivable** | Algorithm: zero Item rows before next Head/Section |
| Heading statistics | Unknown | **Derivable** | Deterministic counts and frequencies |

The following capabilities remain **Unknown** as they require hierarchy reconstruction (tree builder algorithm), not yet demonstrated in this spike:

| Candidate Engineering Capability | Reason for Unknown | Evidence |
|----------------------------------|-------------------|----------|
| Hierarchy depth | Requires tree reconstruction algorithm; numeric labels alone do not prove depth | Adjacent sequence patterns observed, but depth requires parent assignment |
| Parent header identification | Requires parent assignment algorithm (e.g., stack-based); adjacency alone does not assign parentage | Head adjacency frequencies observed, but no parent→child algorithm demonstrated |
| Heading tree structure | Requires tree builder; sequence adjacency is not a tree structure | Adjacent progression recorded, but no tree reconstructed |

---

## Production Applicability

**Derivable capabilities (ready for implementation):**
- **Row type transitions:** Validate structural flow (e.g., Section must precede Head)
- **Empty header detection:** Identify headers without measurable items
- **Heading statistics:** Counts per Head string, items per Head, empty counts

**Pending capabilities (require reconstruction algorithm):**
- Hierarchy depth — wait for reconstruction demonstration
- Parent header identification — wait for parent assignment algorithm
- Heading tree structure — wait for tree builder

---

## Tool

This spike was executed via `tools/eq0010_spike3_row_sequence_analysis.py`.

---

## Evidence Immutability

This evidence report is frozen. No modifications permitted after publication.