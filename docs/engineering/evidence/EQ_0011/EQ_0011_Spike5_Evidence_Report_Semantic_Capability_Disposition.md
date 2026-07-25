# EQ-0011 — Spike 5 — Evidence Report — Semantic Capability Disposition

**Date:** 2026-07-14  
**Status:** Complete — Investigation Concluded  
**Investigation:** EQ-0011 BOQ Semantic Intelligence Boundary  
**Governance:** Engineering_Governance.md v1.0  
**Principle:** Evidence Before Abstraction

---

## Objective

Close the investigation with final classifications, implementation boundary, and recommendations for Increment 3. This spike produces no new evidence. All conclusions are synthesized from Spikes 1-4 frozen evidence.

---

## Investigation Conclusion

### Core Question Answered

**"Where is the engineering boundary between deterministic structural evidence and professional QS judgment, and how should that boundary define the scope of future validation capabilities?"**

**Answer:** The boundary is defined by 7 engineering principles (P-001 through P-007), 5 first principles (FP-001 through FP-005), and 6 responsibility boundaries. Detection of structural facts is always deterministic. Assessment of meaning, legitimacy, and acceptability is either Semantically Deterministic (requiring formalized rules via new Engineering Question) or Professional Judgment (cannot be automated with current evidence).

---

## Final Capability Dispositions

### V-003: Level Progression Validation

| Dimension | Classification |
|-----------|---------------|
| **Evidence** | Structurally Deterministic |
| **Assessment** | Professional Judgment |
| **Confidence** | High |
| **Implementation** | **Not Permitted** |

**Detection Responsibility:** Detect and report level skip magnitude and location.  
**Decision Responsibility:** Determine whether skip is legitimate (QS judgment).  
**Constraint:** Engineering may detect and report skips but must not assess legitimacy. FP-003.

### SEM-003: Items Always Quantify

| Dimension | Classification |
|-----------|---------------|
| **Evidence** | Structurally Deterministic |
| **Assessment** | Professional Judgment |
| **Confidence** | High |
| **Implementation** | **Not Permitted** |

**Detection Responsibility:** Detect and report items with quantity == 0.0.  
**Decision Responsibility:** Determine whether zero is error or acceptable (QS judgment).  
**Constraint:** Engineering may detect and report zero-quantity items but must not assess acceptability. FP-003.

### V-004: Scope Containment (Semantic)

| Dimension | Classification |
|-----------|---------------|
| **Evidence** | Structurally Deterministic |
| **Assessment** | Semantically Deterministic (future) OR Professional Judgment |
| **Confidence** | Medium |
| **Implementation** | **Contingent** |

**Detection Responsibility:** Verify child_level <= parent_level (structural containment).  
**Decision Responsibility:** Determine semantic scope alignment (domain rules or QS judgment).  
**Constraint:** Structural containment detection is permitted. Semantic assessment requires formal domain rules via new Engineering Question. FP-004.

### V-005: Completeness (Full QS)

| Dimension | Classification |
|-----------|---------------|
| **Evidence** | Structurally Deterministic |
| **Assessment** | Semantically Deterministic (future) OR Professional Judgment |
| **Confidence** | Medium |
| **Implementation** | **Contingent** |

**Detection Responsibility:** Verify each section contains at least one measurable item.  
**Decision Responsibility:** Determine whether all required work is represented (domain rules or QS judgment).  
**Constraint:** Basic completeness detection is permitted. Full QS completeness assessment requires project scope definitions via new Engineering Question. FP-004.

---

## Increment 3 Scope

### Permitted (5 capabilities)

1. Level skip detection (evidence component of V-003)
2. Zero-quantity item detection (evidence component of SEM-003)
3. Structural containment check (evidence component of V-004)
4. Section-has-items basic completeness check (evidence component of V-005)
5. Structural evidence presentation for all observed facts

### Contingent (2 capabilities — require EQ + formal rules)

1. Semantic scope containment (V-004) — requires formal scope taxonomy via new EQ
2. Full QS completeness (V-005) — requires project scope definitions via new EQ

### Not Permitted (6 capabilities)

1. V-003: Skip legitimacy assessment (Professional Judgment)
2. SEM-003: Zero-quantity acceptability assessment (Professional Judgment)
3. V-004: Semantic scope containment without formal rules (FP-004)
4. V-005: Full completeness without project scope definitions (FP-004)
5. Any automated inference of professional intent (FP-001, P-005)
6. Any 'should' conclusion without formalized rules (FP-005)

---

## EQ-0011 Lessons Learned

### What Worked Well

1. **Boundary-first methodology** — Organizing the investigation around "where does deterministic computation stop?" produced a more enduring result than asking "can these rules be automated?"

2. **Falsification approach (Spike 3)** — Attempting to disprove the hypothesis rather than confirm it yielded higher confidence in the conclusions.

3. **Vocabulary analysis (Spike 1)** — The vocabulary itself revealed the boundary. Terms like "legitimate" and "acceptable" signal judgment requirements.

4. **Detection/Decision decomposition (Spike 2)** — Every capability cleanly separated into detection (deterministic) and decision (requires rules/judgment).

5. **Evidence Before Abstraction** — No architecture proposals ensured evidence drove conclusions, not design preferences.

### What Could Be Improved

1. **Fixture section-name matching** — V-005 evidence collection was limited by section-name format differences between this spike's tool and the production fixture.

2. **Medium confidence for V-004/V-005** — The "could be formalized" classification requires follow-up investigation. The engineering question for this formalization was identified but not scoped.

### Engineering Methodology Recognition

EQ-0011 confirmed the emerging engineering methodology:

```
Evidence → Capability → Investigation → Implementation Boundary → Validation
```

This is a reusable process applicable beyond BOQ intelligence.

---

## Non-Goals Restated

This investigation did **not**:
- Convert professional QS judgment into deterministic rules
- Propose architecture (no Evidence Engine, Assessment Engine, etc.)
- Implement any production code
- Design CheckMate or any validation engine

Every conclusion is traceable to EQ-0010 or EQ-0011 frozen evidence.

---

## Recommendations for Increment 3

### Build detection capabilities only

Increment 3 should implement the 5 permitted detection capabilities:

1. Level skip detection (structural)
2. Zero-quantity item detection (structural)
3. Structural containment check (structural)
4. Section-has-items basic completeness check (structural)
5. Evidence presentation functionality

### Do not attempt semantic assessment

V-003 and SEM-003 assessment components must remain Professional Judgment unless new evidence demonstrates otherwise.

### File new Engineering Question if formalizing V-004/V-005

Per P-006: "Any future attempt to formalize these semantic rules requires its own Engineering Question and evidence package before implementation."

### Follow FP-001 through FP-005

All five First Principles from Spike 4 govern any future implementation:

| Principle | Rule |
|-----------|------|
| FP-001 | Evidence before inference |
| FP-002 | Never conflate detection with decision |
| FP-003 | Do not automate Professional Judgment |
| FP-004 | Semantic determinism requires explicit rules + new EQ |
| FP-005 | Distinguish 'never' (deterministic) from 'should' (judgment) |

---

## Tool

**Spike Implementation:** `tools/eq0011_spike5_semantic_capability_disposition.py`  
**Results:** `data/reports/eq0011_spike5_results.json`

---

## Spike 5 Conclusion — Investigation Complete

EQ-0011 has answered its core engineering question. The boundary between deterministic structural evidence and professional QS judgment has been defined, classified, and validated against production evidence.

**Investigation Status:** Complete — Ready for Gate 2 review

**Gate 2 Deliverables:**
1. ✅ EQ-0011 Engineering Question
2. ✅ Semantic Capability Matrix (finalized)
3. ✅ 5 Evidence Reports (Spikes 1-5)
4. ✅ Engineering Boundary Report (Spike 4 synthesis)
5. ✅ Detection vs Decision architectural pattern (Spikes 2-4)
6. ✅ Increment 3 Scope Recommendation (this document)

---

## Document Control

**Version:** 1.0 (Final)  
**Status:** Complete — Investigation Concluded  
**Last Updated:** 2026-07-14  
**Owner:** Project Owner  
**Authority:** EQ-0011 BOQ Semantic Intelligence Boundary