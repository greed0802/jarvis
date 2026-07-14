# EQ-0010: Structural Capability Matrix

**Engineering Question:** EQ-0010 Deterministic BOQ Structural Intelligence  
**Status:** Investigation Complete — All 5 Spikes Executed  
**Date Created:** 2026-07-14  
**Governance:** Engineering_Governance.md v1.0  
**Template:** Capability_Matrix_Template.md v1.0

---

## Purpose

This matrix tracks the discovery of deterministic structural intelligence capabilities from production BOQRow data.

Each capability transitions from "Unknown" to **Observable**, **Derivable**, **Domain Dependent**, or **Not Determinable** as investigation spikes collect evidence.

---

## Five-State Model

| State | Meaning |
|-------|---------|
| **Observable** | Directly available in BOQRow fields |
| **Derivable** | Deterministically computable from BOQRow |
| **Domain Dependent** | Requires Domain Knowledge Layer validation |
| **Not Determinable** | Cannot be determined from current BOQRow structure |
| **Unknown** | Evidence not yet collected |

---

## Structural Capability Matrix — Final State

### Structural Properties

| Candidate Engineering Capability | Obs | Der | Domain | Not Det | Unk | Consumer(s) | Evidence |
|----------------------------------|-----|-----|--------|---------|-----|-------------|----------|
| Row type | ✓ | | | | | All | Spike 1: Direct BOQRow.row_type field |
| Row number | ✓ | | | | | All | Spike 1: Direct BOQRow.row_number field |
| Code presence | ✓ | | | | | All | Spike 1: Direct BOQRow.code field |
| Description presence | ✓ | | | | | All | Spike 1: Direct BOQRow.description field |
| Quantity value | ✓ | | | | | All | Spike 1: Direct BOQRow.quantity field |
| UOM value | ✓ | | | | | All | Spike 1: Direct BOQRow.uom field |
| Section context | ✓ | | | | | All | Spike 1: Direct BOQRow.section field |
| Row type transitions | | ✓ | | | | CheckMate | Spike 3: 16 patterns from adjacent rows |
| Hierarchy indicator (Head1-5 labels) | ✓ | | | | | Formatter, CheckMate | Spike 2: Direct BOQRow.uom field values |
| Hierarchy depth | | ✓ | | | | Formatter, CheckMate | Spike 4: Stack algorithm computes depth |
| Parent header identification | | ✓ | | | | Formatter, CheckMate | Spike 4: Stack pop assigns parent |
| Empty header detection | | ✓ | | | | CheckMate | Spike 3: Zero Items before next Head |
| Orphan item detection | | ✓ | | | | CheckMate | Spike 5: Proposed taxonomy established |
| Level progression validation | | | ✓ | | | CheckMate | Spike 5: V-003 requires QS judgment |
| Section integrity validation | | | | | ✓ | CheckMate | Not investigated |
| Heading tree structure | | ✓ | | | | Formatter, Reporting | Spike 4: Tree built from stack |
| Heading statistics | | ✓ | | | | Reporting | Spike 3: Counts per Head, items, empties |
| Items-per-header ratio | | ✓ | | | | Reporting | Spike 4: Avg items from tree |

### Domain-Linked Capabilities

| Candidate Engineering Capability | Obs | Der | Domain | Not Det | Unk | Consumer(s) | Evidence |
|----------------------------------|-----|-----|--------|---------|-----|-------------|----------|
| Parent existence (V-001) | | ✓ | | | | CheckMate | Spike 5: Every non-root header has parent |
| Orphan detection (V-002) | | ✓ | | | | CheckMate | Spike 5: All items precede a Head |
| Level progression (V-003) | | | ✓ | | | CheckMate | Spike 5: 12 skip violations; domain rule required |
| Scope containment (V-004) | | | ✓ | | | CheckMate | Spike 5: Semantic rule; parent-level consistency is Derivable |
| Completeness (V-005) | | | ✓ | | | CheckMate | Spike 5: Full QS completeness requires domain |
| Sections never measure (SEM-001) | | ✓ | | | | CheckMate | Spike 5: 0 sections with quantities |
| Headers provide context (SEM-002) | | ✓ | | | | CheckMate | Spike 5: 0 headers with quantities |
| Items always quantify (SEM-003) | | | ✓ | | | CheckMate | Spike 5: 5 zero-quantity items; domain rule required |
| Inheritance (SEM-004) | | | | | ✓ | CheckMate | Assessment only; outside scope of EQ-0010 |
| Semantic completeness (SEM-005) | | | | | ✓ | CheckMate | Assessment only; outside scope of EQ-0010 |

---

## Update History

### 2026-07-14 — Spike 5 Final (Amended)

**Status:** Investigation Complete

**Determinism:** Verified (Run 1 == Run 2: True)

**Capability Transitions:**
- Orphan item detection: Unknown → **Derivable** (proposed taxonomy)
- V-001, V-002, SEM-001, SEM-002: Unknown → **Derivable** (algorithmically validated)
- V-003, V-004, V-005, SEM-003: Unknown → **Domain Dependent** (require QS interpretation)
- SEM-004, SEM-005: Assessment only; outside investigation scope

**Reconstruction algorithm assessment:** The deterministic stack-based reconstruction algorithm was evaluated against the investigated production fixture and the assessed domain rules. It remains a viable production candidate following domain reconciliation.

---

## Final Capability State Summary

| State | Count | % |
|-------|-------|---|
| **Observable** | **8** | **36%** |
| **Derivable** | **10** | **46%** |
| **Domain Dependent** | **4** | **18%** |
| Not Determinable | 0 | 0% |
| Unknown | 0 | 0% |
| **Total scoped** | **22** | **100%** |
| *Assessment only (outside scope)* | *2* | *Dispositioned* |
| *Not investigated* | *1* | *Dispositioned* |

---

## Investigation Conclusion

EQ-0010 determined that deterministic structural intelligence is achievable from BOQRow data. 

- **8 capabilities Observable** (directly available in BOQRow fields)
- **10 capabilities Derivable** (deterministically computable via proven algorithms)
- **4 capabilities Domain Dependent** (require Domain Knowledge Layer integration)

**Canonical algorithm:** The reconstruction algorithm is **not** claimed to be canonical. It is the current candidate algorithm, viable following domain reconciliation.

**Architecture Impact:** None. All capabilities are pure functions over `list[BOQRow]` following the Increment 1 pattern.

---

## Document Control

**Version:** 2.0 (Final)  
**Last Updated:** 2026-07-14  
**Owner:** Project Owner  
**Status:** Investigation Complete