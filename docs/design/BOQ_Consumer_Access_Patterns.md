# BOQ Consumer Access Patterns

## EQ-0020 — BOQ Intelligence Consumer Architecture

### Spike 4 — Consumer Access Patterns

**Status:** Complete
**Date:** 2026-07-25
**Authority:** EQ-0020 Spike 4

---

## 1. Purpose

Determine the preferred consumption model for BOQ Intelligence evidence. Evaluate:

- Direct dataclass access
- Contract interface
- Serialization
- Future API compatibility
- Version negotiation

---

## 2. Current Access Pattern

### 2.1 Stable Import Paths

The Evidence Contract v1.1.0 defines the following stable import paths (G-14, G-15, G-16):

```python
from jarvis.parsers.costx.boq_intelligence import analyze_boq
from jarvis.parsers.costx.boq_intelligence import BOQIntelligenceResult
from jarvis.parsers.costx.boq_intelligence import BOQHeaderNode
from jarvis.parsers.costx.boq_extraction import BOQRow
from jarvis.parsers.costx.boq_extraction import extract_boq
```

**Stability Classification:** HIGH — All symbols are public (no underscore prefix), frozen dataclass or public function, protected by frozen engineering evidence.

### 2.2 Unstable Imports (Prohibited)

All symbols beginning with `_` (underscore) are internal implementation. Consumers must NOT import:

```python
# Internal helpers - part of implementation, not contract:
from jarvis.parsers.costx.boq_intelligence import _count_row_types       # Internal
from jarvis.parsers.costx.boq_intelligence import _reconstruct_hierarchy  # Internal
from jarvis.parsers.costx.boq_intelligence import _freeze_node            # Internal
from jarvis.parsers.costx.boq_intelligence import _compute_hierarchy_statistics  # Internal
from jarvis.parsers.costx.boq_intelligence import _detect_level_skips     # Internal
from jarvis.parsers.costx.boq_intelligence import _detect_zero_quantities # Internal
from jarvis.parsers.costx.boq_intelligence import _detect_structural_containment  # Internal
from jarvis.parsers.costx.boq_intelligence import _detect_basic_completeness  # Internal
from jarvis.parsers.costx.boq_intelligence import _extract_vocabulary     # Internal
from jarvis.parsers.costx.boq_intelligence import _categorize_head1        # Internal
from jarvis.parsers.costx.boq_intelligence import _detect_administrative_patterns  # Internal
from jarvis.parsers.costx.boq_intelligence import _enumerate_sections     # Internal
from jarvis.parsers.costx.boq_intelligence import _compute_uom_distribution  # Internal
from jarvis.parsers.costx.boq_intelligence import _compute_header_distribution  # Internal
from jarvis.parsers.costx.boq_intelligence import _detect_header_quantity_violations  # Internal
from jarvis.parsers.costx.boq_intelligence import _detect_admin_template_matches  # Internal
from jarvis.parsers.costx.boq_extraction import _classify_row             # Internal
```

### 2.3 Current Access Pattern (Recommended)

**Direct immutable dataclass + public function** (current production pattern). No facade, no protocol, no contracts package, no wrapper, no adapter, no runtime abstraction.

```python
from jarvis.parsers.costx.boq_extraction import BOQRow, extract_boq
from jarvis.parsers.costx.boq_intelligence import analyze_boq, BOQIntelligenceResult, BOQHeaderNode

# 1. Extract rows from a validated CostX workbook
rows: list[BOQRow] = extract_boq(workbook)

# 2. Run intelligence analysis
result: BOQIntelligenceResult = analyze_boq(
    rows,
    include_hierarchy=True,    # Enable Increment 2 hierarchy evidence
    include_detection=True,    # Enable Increment 3 detection evidence
    include_semantic=True,     # Enable Increment 4 semantic evidence (v1.1.0)
)

# 3. Access evidence directly from the frozen dataclass
for row_type, count in result.row_classification.items():
    ...

# 4. Access hierarchy (when include_hierarchy=True)
if result.hierarchy is not None:
    for root in result.hierarchy:
        print(f"Root header: {root.description} (depth {root.depth})")

# 5. Access detection evidence (when include_detection=True)
if result.detected_level_skips is not None:
    for skip in result.detected_level_skips:
        print(f"Level skip: {skip['skip_magnitude']} levels")

# 6. Access semantic evidence (when include_semantic=True) — v1.1.0
if result.vocabulary is not None:
    for term, count in result.vocabulary.items():
        ...
```

### 2.4 Consumer Dependency Graph

```
Consumer
  └── jarvis.parsers.costx.boq_intelligence
        ├── analyze_boq (function)
        ├── BOQIntelligenceResult (frozen dataclass)
        └── BOQHeaderNode (frozen dataclass)

  └── jarvis.parsers.costx.boq_extraction
        ├── BOQRow (dataclass)
        └── extract_boq (function)
```

**Note:** `WorkbookParser` is a pre-extraction infrastructure concern (validation/loading). It is exported by `costx/__init__.py` but is not part of the evidence contract.

---

## 3. Access Pattern Evaluation

### 3.1 Direct Dataclass Access

**Evaluation:** ✅ RECOMMENDED

**Pros:**
- Simple, explicit, no abstraction overhead
- Type-safe (frozen dataclass with type annotations)
- Direct field access (no method calls)
- Immutable (frozen=True)
- Deterministic (same input → same output)
- No runtime overhead from facades or adapters
- Clear ownership (producer owns dataclass, consumers read)

**Cons:**
- Consumers depend on dataclass field names (but this is the contract)
- No runtime polymorphism (but not needed for evidence)

**Evidence:** This pattern is already in production (Validation Engine uses it). The EQ-0012 Spike 4 (Consumer Access Patterns) explicitly recommends this pattern.

### 3.2 Contract Interface (Protocol/Abstract Base Class)

**Evaluation:** ❌ NOT RECOMMENDED

**Pros:**
- Runtime polymorphism
- Decoupling from concrete implementation

**Cons:**
- Introduces abstraction without production use (violates YAGNI)
- Adds complexity without benefit (evidence is a frozen dataclass, not a service)
- Would require interface evolution alongside dataclass evolution
- No consumer has requested polymorphism
- AGENTS.md prohibits "Generic abstractions without production use"

**Evidence:** The EQ-0012 Spike 4 explicitly rejected this pattern: "No facade, no protocol, no contracts package, no wrapper, no adapter, no runtime abstraction."

### 3.3 Serialization (JSON, Pickle, etc.)

**Evaluation:** ❌ NOT RECOMMENDED for primary access

**Pros:**
- Language-agnostic
- Persistence capability
- Network transfer

**Cons:**
- Loss of type safety
- Deserialization overhead
- Not needed for in-process consumers
- Evidence is already a frozen dataclass (no serialization needed)
- Would introduce a second source of truth (serialized vs. live)

**Evidence:** No consumer has requested serialization. The Evidence Contract defines Python types, not serialization formats. Serialization may be needed for external consumers (future), but should be a separate concern.

### 3.4 Future API Compatibility

**Evaluation:** ✅ HANDLED by Contract Versioning Policy

The Evidence Contract v1.1.0 defines a clear versioning policy:

| Change Type | SemVer | Consumer Impact |
|-------------|--------|----------------|
| Add optional field | MINOR | Consumers opt-in; backward compatible |
| Add new dict keys | MINOR | Consumers iterating dynamically unaffected |
| Remove required field | MAJOR | Breaking change; consumers must update |
| Change field type | MAJOR | Breaking change; consumers must update |
| Rename field | MAJOR | Breaking change; consumers must update |

**Backward Compatibility Guarantees (G-01 through G-16):**
- G-01: All documented fields will exist for the promised contract version
- G-02: Required fields will never be None
- G-03: Optional fields will never be removed without formal deprecation
- G-04: Field types as documented will not change within a MAJOR version
- G-11: All evidence is deterministic
- G-12: All evidence is immutable
- G-14: Consumers may depend on the Evidence Contract directly
- G-15: Consumers may import evidence types without importing internal implementation
- G-16: Consumers will not need access to internal BOQ Intelligence functions

### 3.5 Version Negotiation

**Evaluation:** ✅ HANDLED by Optional Field Pattern

The Evidence Contract uses an optional field pattern for version negotiation:

```python
# Consumers check for None to determine if a field is available
if result.vocabulary is not None:
    # v1.1.0 semantic evidence available
    process_vocabulary(result.vocabulary)
else:
    # v1.0.0 — semantic evidence not available
    pass
```

**Version Negotiation Mechanism:**
1. Consumers call `analyze_boq()` with desired `include_*` parameters
2. Optional fields return `None` when disabled
3. Consumers check `is not None` before accessing optional fields
4. No runtime version negotiation needed — the contract version is implicit in field availability

**Future Extension:**
- New optional fields follow the same `None`-when-disabled pattern
- New contract versions (MAJOR) require explicit consumer migration
- Deprecation lifecycle (3-phase) provides migration window

---

## 4. Consumer Access Recommendations

### 4.1 For All Consumers

1. **Import only from stable contract paths** — Never import `_`-prefixed symbols
2. **Use defensive None-checking** — Always check `is not None` before accessing optional fields
3. **Do not modify evidence** — `BOQIntelligenceResult` is frozen; do not attempt mutation
4. **Do not depend on internal implementation** — Only depend on the Evidence Contract
5. **Handle contract evolution** — Follow the versioning policy for backward compatibility

### 4.2 For Validation Engine

1. **Consume `BOQIntelligenceResult` only** — Do not import from `boq_intelligence._*`
2. **Handle optional evidence gracefully** — Return `None` for unavailable optional fields
3. **Produce `ValidationFindings` only** — Do not produce recommendations or assessments
4. **Maintain determinism** — Same evidence + same rules → same findings

### 4.3 For CheckMate

1. **Consume both `BOQIntelligenceResult` and `ValidationFindings`**
2. **Apply interpretation layer** — Translate findings into application-specific meaning
3. **Own presentation** — Do not depend on engine presentation
4. **Enable human decision** — Present findings for human assessment, do not auto-assess

### 4.4 For Formatter

1. **Consume `BOQIntelligenceResult` for rendering**
2. **Consume `ValidationFindings` for finding rendering**
3. **Own output format rendering** — Do not depend on other consumers' presentation
4. **Handle optional fields** — Render `None` fields as "not available"

### 4.5 For Builder

1. **Consume `ValidationFindings` for CI/CD gates**
2. **Configure thresholds** — Define acceptable ranges in consumer, not engine
3. **Produce machine-readable output** — Do not produce human-readable presentation
4. **Fail on findings** — Gate on finding values, not assessments

### 4.6 For O&A

1. **Consume `BOQIntelligenceResult` for O&A analysis**
2. **Consume `ValidationFindings` for O&A-specific checks**
3. **Own O&A interpretation** — Apply domain-specific meaning to evidence
4. **Handle omission/addition sections** — Use `section_statistics` and `known_anomalies`

### 4.7 For Reporting

1. **Consume `BOQIntelligenceResult` for aggregated statistics**
2. **Consume `ValidationFindings` for finding summaries**
3. **Own report formatting** — Do not depend on other consumers' presentation
4. **Aggregate across evidence fields** — Combine multiple fields for summary reports

---

## 5. Access Pattern Summary

| Access Pattern | Recommendation | Rationale |
|----------------|----------------|-----------|
| Direct dataclass access | ✅ RECOMMENDED | Simple, type-safe, immutable, deterministic |
| Contract interface (Protocol) | ❌ NOT RECOMMENDED | No production use; violates YAGNI |
| Serialization | ❌ NOT RECOMMENDED (primary) | Loss of type safety; not needed in-process |
| Version negotiation | ✅ HANDLED by optional field pattern | None-checking provides implicit negotiation |
| Future API compatibility | ✅ HANDLED by versioning policy | MAJOR/MINOR/PATCH policy with guarantees |

---

## 6. Deliverable

This document is the **Consumer Access Recommendation** deliverable for EQ-0020 Spike 4.

---

## 7. Document Control

| Property | Value |
|----------|-------|
| **Document ID** | EQ-0020-S4-CONSUMER-ACCESS-PATTERNS |
| **EQ** | EQ-0020 |
| **Spike** | 4 |
| **Status** | Complete |
| **Date** | 2026-07-25 |
| **Owner** | Project Owner |
| **Authority** | EQ-0020 (BOQ Intelligence Consumer Architecture) |
| **References** | BOQ_Intelligence_Public_Evidence_Contract_v1.1.md §Consumer Access Patterns, EQ-0012 Spike 4 (Consumer Access Patterns), EQ-0013 Spike 3 (Engine Scope) |

---

**End of Consumer Access Patterns**
