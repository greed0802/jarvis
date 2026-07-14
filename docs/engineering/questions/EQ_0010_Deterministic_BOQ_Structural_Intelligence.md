# EQ-0010: Deterministic BOQ Structural Intelligence

**Status:** Investigation Phase — Approved and Authorized (Gate 1)  
**Date:** 2026-07-14  
**Governance:** Engineering_Governance.md v1.0  
**Owner:** Project Owner

---

## Problem Statement

BOQ Intelligence Increment 1 delivers row classification, statistics, section analysis, and anomaly detection. These capabilities operate on individual rows or simple aggregations.

The next engineering question is: **What deterministic structural intelligence can be derived from the production BOQRow data structure?**

Structural intelligence includes hierarchical relationships, parent-child associations, organizational patterns, and structural integrity validation. These capabilities would enable:
- CheckMate to validate BOQ structural rules (V-001 through V-005 from Domain doc 02)
- Formatter to produce hierarchy-aware exports with proper indentation and context
- Reporting to summarize BOQ organization and completeness

However, the extent to which structural relationships are **Observable, Derivable, or Not Determinable** from BOQRow alone is currently unknown.

This investigation will determine which structural capabilities are achievable with deterministic engineering and which require additional data, domain integration, or are fundamentally not determinable.

---

## Research Question

**What deterministic structural information can be derived from `list[BOQRow]` extracted by the production parser?**

Specifically:
1. Which structural properties are **Observable** (directly available in BOQRow fields)?
2. Which structural properties are **Derivable** (deterministically computable from BOQRow)?
3. Which structural properties are **Domain Dependent** (require Domain Knowledge Layer validation)?
4. Which structural properties are **Not Determinable** (cannot be determined from current data structure)?

---

## Scope

### In Scope

**Data Source:**
- Production BOQRow extracted from `full_boq.xlsx` via extract_boq()
- BOQRow structure: `row_number`, `code`, `description`, `quantity`, `uom`, `row_type`, `section`

**Investigation Methodology:**
- Evidence-first: observe production data, then characterize patterns
- Compare observations against Domain Knowledge Layer (docs/domain/02_BOQ_Structure.md)
- Identify what is Observable, Derivable, Domain Dependent, or Not Determinable
- Deterministic analysis only (no AI, no heuristics, no NLP)

**Candidate Structural Analyses:**
- Hierarchy depth detection
- Parent-child relationships
- Orphan item detection
- Empty header detection
- Hierarchy continuity validation
- Section integrity validation
- Level progression validation
- Heading tree structure
- Heading statistics
- Items-per-header ratios

**Consumer Analysis:**
- CheckMate (structural validation)
- Formatter (hierarchy-aware output)
- Reporting (structural summaries)
- Future deterministic capabilities

**Architecture Impact:**
- Assessment whether any architecture changes are required
- Expected: None (following Increment 1 pattern of pure functions over list[BOQRow])

### Out of Scope

**Explicitly Excluded:**
- Parser modifications (parser responsibilities frozen)
- Runtime architecture changes (no new engines, frameworks, components)
- AI or machine learning approaches
- Heuristic pattern matching
- NLP or text analysis
- Implementation code (investigation only)
- Multi-fixture generalization (single fixture: `full_boq.xlsx`)
- Cubit, PDF, or other parser formats
- CheckMate implementation (consumer, not part of this investigation)
- Formatter implementation (consumer, not part of this investigation)

---

## Non-Goals

This investigation does **not**:
- Implement BOQ Intelligence Increment 2 (that follows after investigation approval)
- Define CheckMate's rule engine or validation architecture
- Design Formatter's export capabilities
- Propose new runtime components or abstractions
- Modify the production parser or extraction logic
- Introduce speculative features based on assumed future requirements
- Generalize across multiple fixtures (single-fixture investigation)

---

## Investigation Plan

The investigation consists of five evidence-first spikes, each designed to move capabilities from "Unknown" to evidenced states in the Capability Matrix.

### Spike 1: Direct Field Observation

**Objective:** Establish what is **Observable** from BOQRow fields alone.

**Method:**
- Extract BOQRow list from `full_boq.xlsx`
- Enumerate all fields: `row_number`, `code`, `description`, `quantity`, `uom`, `row_type`, `section`
- Produce field presence statistics
- Document field value distributions

**Expected Output:**
- Observable capability classifications
- Baseline statistics for comparison
- Evidence: Direct BOQRow field inspection

**Production Applicability:**
Observable capabilities can be used immediately for reporting, export, and display.

---

### Spike 2: UOM Pattern Analysis

**Objective:** Investigate whether hierarchy depth is **Observable, Derivable, or Not Determinable**.

**Hypothesis:** UOM values (Head1, Head2, Head3, Head4) may encode hierarchy depth.

**Method:**
- Extract all UOM values from production data
- Analyze UOM pattern distribution
- Test whether UOM reliably indicates hierarchy level
- Compare against Domain Knowledge Layer expectations (Head1-4 hierarchy)

**Possible Outcomes:**
1. **Observable:** UOM directly encodes hierarchy depth (Head1 = level 1, etc.)
2. **Derivable:** UOM pattern can be used with additional analysis to infer depth
3. **Not Determinable:** UOM does not reliably indicate hierarchy depth

**Expected Output:**
- Hierarchy depth capability classification
- Evidence: UOM pattern analysis
- UOM vocabulary completeness assessment

**Production Applicability:**
If Observable or Derivable, enables hierarchy-aware formatting and validation.

---

### Spike 3: Row Sequence Analysis

**Objective:** Investigate whether parent-child relationships are **Derivable**.

**Hypothesis:** Row sequences may reveal structural relationships (Head → Item, Head1 → Head2 progression).

**Method:**
- Analyze row_type transitions (what follows what)
- Identify structural patterns (Head before Item, consecutive Heads, etc.)
- Test whether parent headers can be deterministically identified from sequence
- Quantify pattern reliability

**Possible Outcomes:**
1. **Derivable:** Parent-child relationships can be computed from row sequences
2. **Not Determinable:** Row sequences insufficient for parent determination

**Expected Output:**
- Parent header capability classification
- Row sequence patterns documented
- Transition matrix (row type A → row type B frequencies)

**Production Applicability:**
If Derivable, enables structural validation (orphan detection, continuity checking).

---

### Spike 4: Structural Pattern Detection

**Objective:** Test specific **Derivable** hypotheses for structural patterns.

**Patterns to Test:**
1. **Empty headers:** Head row with no subsequent Items before next Head/Section
2. **Orphan items:** Items without proper Head parent
3. **Level progression:** Head1 → Head2 → Head3 continuity
4. **Section integrity:** OMISSION/ADDITION boundary consistency

**Method:**
- Implement deterministic detection algorithms for each pattern
- Run against production fixture
- Quantify instances found
- Verify determinism (repeated runs produce identical results)

**Expected Output:**
- Classification of each pattern (Derivable or Not Determinable)
- Instance counts from production fixture
- Evidence: Pattern detection algorithms + verification

**Production Applicability:**
Derivable patterns become CheckMate validation rules.

---

### Spike 5: Domain Reconciliation

**Objective:** Map **Domain Dependent** capabilities to Domain Knowledge Layer documents.

**Method:**
- Review Domain Knowledge Layer (docs/domain/02_BOQ_Structure.md)
- Identify structural rules requiring domain knowledge
- Map each rule to Observable/Derivable/Domain/Not Determinable classification
- Document which domain rules are validatable with current data

**Domain Rules to Assess:**
- V-001: Parent Exists (every Level 2 must have Level 1 parent)
- V-002: No Orphans (no elements float without parent)
- V-003: Level Progression (levels increment by 1)
- V-004: Scope Containment (children fit within parent scope)
- V-005: Completeness (every section has measured items)
- SEM-001 through SEM-005 (semantic validation rules)

**Expected Output:**
- Domain Dependent capability classifications
- Mapping to specific domain documents
- Assessment of which domain rules require additional fixture data

**Production Applicability:**
Identifies domain integration requirements for CheckMate.

---

## Candidate Engineering Capabilities

Initial list of capabilities to be investigated. All begin in "Unknown" state.

The investigation will move each capability to: **Observable**, **Derivable**, **Domain Dependent**, or **Not Determinable**.

### Structural Properties

| Capability | Initial State | Expected Consumer |
|------------|---------------|-------------------|
| Row type | Unknown | All |
| Row number | Unknown | All |
| Code presence | Unknown | All |
| Description presence | Unknown | All |
| Quantity value | Unknown | All |
| UOM value | Unknown | All |
| Section context | Unknown | All |
| Hierarchy depth | Unknown | Formatter, CheckMate |
| Parent header | Unknown | Formatter, CheckMate |
| Row type transitions | Unknown | CheckMate |
| Empty header detection | Unknown | CheckMate |
| Orphan item detection | Unknown | CheckMate |
| Level progression validation | Unknown | CheckMate |
| Section integrity validation | Unknown | CheckMate |
| Heading tree structure | Unknown | Formatter, Reporting |
| Heading statistics | Unknown | Reporting |
| Items-per-header ratio | Unknown | Reporting |

### Domain-Linked Validations

| Capability | Initial State | Expected Consumer | Domain Reference |
|------------|---------------|-------------------|------------------|
| Parent existence validation (V-001) | Unknown | CheckMate | Domain doc 02 |
| Orphan detection (V-002) | Unknown | CheckMate | Domain doc 02 |
| Level progression validation (V-003) | Unknown | CheckMate | Domain doc 02 |
| Scope containment (V-004) | Unknown | CheckMate | Domain doc 02 |
| Completeness validation (V-005) | Unknown | CheckMate | Domain doc 02 |
| Sections never measure (SEM-001) | Unknown | CheckMate | Domain doc 02 |
| Headers provide context (SEM-002) | Unknown | CheckMate | Domain doc 02 |
| Items always quantify (SEM-003) | Unknown | CheckMate | Domain doc 02 |

---

## Consumer Analysis

### How Capabilities Map to Consumers

**Observable Capabilities:**
- **All Consumers:** Direct reading, reporting, export, display
- Low implementation cost, immediate value

**Derivable Capabilities:**
- **BOQ Intelligence Increment 2:** Structural analysis functions
- **CheckMate:** Structural validation rules
- **Formatter:** Hierarchy-aware export with indentation and context
- **Reporting:** Structural summaries, organization metrics

**Domain Dependent Capabilities:**
- **CheckMate:** Professional validation rules requiring domain knowledge
- **Learning:** Training data for domain rule learning (future)
- Requires Domain Knowledge Layer integration

**Not Determinable Capabilities:**
- **None:** Explicitly excluded from automated analysis
- Requires human professional judgment or cannot be determined from current data

### Consumer Decision Tree

```
Is capability Observable?
  Yes → All consumers can use immediately
  No ↓
  
Is capability Derivable?
  Yes → BOQ Intelligence, CheckMate, Formatter can use
  No ↓
  
Is capability Domain Dependent?
  Yes → Requires domain integration strategy
  No ↓
  
Capability is Not Determinable
  → Excluded from automation
```

---

## Architecture Impact

### Expected Impact: None

This investigation follows the pattern established by BOQ Intelligence Increment 1:
- Pure functions over `list[BOQRow]`
- No new engines, frameworks, or runtime components
- No parser modifications
- No kernel changes
- No service container modifications
- No new ADRs required

### Verification Criteria

The investigation will explicitly verify:
1. No new runtime abstractions required
2. No changes to existing production components
3. No architectural expansion needed
4. Pattern matches Increment 1 (pure functions + tests)

### If Architecture Changes Are Needed

If investigation discovers that architectural changes are required:
1. Document the evidence that demonstrates necessity
2. Propose ADR for Project Owner review
3. Do NOT proceed with implementation
4. Return to Project Owner for disposition

The investigation itself should not require architecture changes. The investigation **discovers** what is possible within current architecture.

---

## Success Criteria

The investigation is successful when:

1. **All capabilities classified:** Every candidate capability has transitioned from "Unknown" to Observable/Derivable/Domain/Not Determinable
2. **Evidence documented:** Each classification is supported by production evidence
3. **Capability Matrix complete:** Final state shows all evidenced classifications
4. **Domain reconciliation complete:** Domain Knowledge Layer mapped to capability classifications
5. **Consumer analysis complete:** Clear understanding of how each capability type is consumed
6. **Architecture impact assessed:** Explicit verification that no architecture changes required
7. **Production applicability clear:** Smallest meaningful Increment 2 identified

---

## Evidence Required

### Production Evidence

- Executed against registered fixture: `full_boq.xlsx` (SHA-256 verified)
- Deterministic results (reproducible on repeated execution)
- Quantified observations (counts, distributions, patterns)
- Pattern verification (algorithms proven against production data)

### Domain Evidence

- Mapping to Domain Knowledge Layer documents
- Alignment or deviation from documented QS semantics
- Identification of domain rules requiring integration

### Consumer Evidence

- Clear mapping from capability states to consumer needs
- Demonstration that capability supports consumer use case
- No speculative "might be useful" capabilities

---

## Exit Criteria

The investigation may conclude when:

1. **All spikes executed:** 5 spikes completed with documented evidence
2. **Capability Matrix finalized:** All capabilities have evidenced classifications or documented deferrals
3. **Evidence Report written:** Findings, conclusions, and production recommendation documented
4. **Architecture verification complete:** Confirmed no architecture changes required

**Early Exit Condition:**
If investigation discovers that Increment 2 scope is infeasible (all meaningful capabilities Not Determinable), document findings and recommend alternative investigation direction. Do not proceed with unproductive investigation.

---

## Decision Framework

After evidence collection, the production recommendation will be based on:

### Capability Prioritization

1. **Observable capabilities:** Highest priority (immediate value, lowest cost)
2. **Proven Derivable capabilities:** High priority (deterministic, valuable)
3. **Domain Dependent capabilities:** Medium priority (requires integration strategy)
4. **Not Determinable capabilities:** Excluded (not achievable from current data)

### Increment 2 Selection Criteria

Apply:
- **Documentation First:** Capability must be clearly documentable
- **Evidence Before Abstraction:** No speculative patterns
- **Rule of Three:** Don't generalize until third use case
- **YAGNI:** No features without clear consumer need
- **Deterministic Engineering:** Proven algorithm required

### Minimum Viable Increment 2

The smallest production implementation that:
- Delivers meaningful engineering value to at least one consumer
- Consists of proven Observable or Derivable capabilities
- Requires no architecture changes
- Can be fully tested against production fixtures
- Sets foundation for future structural intelligence

**Not a Goal:** Deliver all discovered capabilities in Increment 2. Deliver the smallest meaningful subset and defer the rest.

---

## Risks

### Investigation Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| UOM pattern unreliable | Hierarchy depth not determinable | Spike 2 explicitly tests reliability |
| Row sequences insufficient | Parent relationships not determinable | Spike 3 quantifies pattern coverage |
| Domain rules unvalidatable | Domain integration complex | Spike 5 maps what's achievable vs. theoretical |
| Fixture-specific patterns | Findings don't generalize | Document single-fixture limitation explicitly |

### Production Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Over-engineering Increment 2 | Speculative features, wasted effort | Apply YAGNI and Rule of Three strictly |
| Under-scoping Increment 2 | Insufficient value delivered | Capability Matrix identifies minimum viable set |
| Premature domain integration | Architecture expansion before evidence | Explicitly defer Domain Dependent capabilities |

---

## Relationship to Existing Work

### Foundation

- **EQ-0007 (Answered):** Production BOQ extraction established
- **BOQ Intelligence Increment 1 (Delivered):** Row classification, statistics, section analysis, anomaly detection
- **Domain Knowledge Layer (Frozen):** docs/domain/02_BOQ_Structure.md provides QS semantic understanding

### Continuation

This investigation builds on the production pipeline:
```
WorkbookParser → extract_boq() → list[BOQRow] → BOQ Intelligence Increment 1
                                                          ↓
                                                  (EQ-0010 investigation)
                                                          ↓
                                                  BOQ Intelligence Increment 2
```

### Future Dependencies

- **CheckMate:** Depends on structural validation capabilities discovered here
- **Formatter:** Depends on hierarchy-aware capabilities discovered here
- **EQ-0011 (Future):** Rule capability matrix may extend findings from this investigation

---

## References

### Production Evidence

- `tests/fixtures/costx/full_boq.xlsx` — Primary production fixture
- `tests/fixtures/FIXTURE_METADATA.py` — Fixture verification
- `src/jarvis/parsers/costx/boq_extraction.py` — Production extraction logic
- `src/jarvis/parsers/costx/boq_intelligence.py` — Increment 1 implementation

### Domain Knowledge

- `docs/domain/02_BOQ_Structure.md` — BOQ hierarchical structure semantics
- `docs/domain/01_QS_Office_Standards.md` — Office quality standards
- `docs/domain/05_UOM_Standards.md` — Unit of measurement conventions

### Engineering Governance

- `docs/engineering/Engineering_Governance.md` — Investigation methodology (v1.0)
- `docs/templates/Capability_Matrix_Template.md` — Matrix usage guidelines
- `docs/retrospectives/BOQ_Intelligence_Increment_1.md` — Lessons from Increment 1

### Related Investigations

- `docs/reference/EQ_0007_Production_Extraction_Report.md` — Extraction evidence
- `docs/reference/EQ_0009_Context_Discovery_Report.md` — Context investigation

---

## Document Control

**Version:** 1.1  
**Date:** 2026-07-14  
**Owner:** Project Owner  
**Status:** Investigation Phase — Spikes Authorized

**Approval Gate:** Investigation Authorization (Gate 1) — Approved 2026-07-14

**Next Steps:**
1. Gate 1 approved by Project Owner
2. Begin Spike 1: Direct Field Observation
3. Execute remaining spikes sequentially
4. Update Capability Matrix after each spike
5. Produce Evidence Report upon investigation completion
6. Present to Project Owner for implementation disposition (Gate 2)

---

## Notes

This investigation is intentionally narrow:
- Single fixture (`full_boq.xlsx`)
- Deterministic analysis only
- No implementation code
- Evidence collection phase only

The goal is to discover what is possible, not to build it yet. The Evidence Report (created after investigation) will recommend the smallest meaningful Increment 2 based on collected evidence.