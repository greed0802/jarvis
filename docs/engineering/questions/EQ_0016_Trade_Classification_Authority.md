# EQ-0016: Trade Classification Authority Investigation

**Status:** Investigation Phase — Proposed
**Date:** 2026-07-23
**Governance:** Engineering_Governance.md v1.0
**Owner:** Project Owner

---

## Problem Statement

CB-0005 implemented deterministic trade classification using Item Code prefixes from CostX fixture analysis. The current evidence supports Item-Code-based classification for the analyzed fixture. However, the applicability to arbitrary BOQ formats has not yet been established.

The current implementation correctly classifies trades for BOQs with recognizable Item Code patterns (A-Z, AA-AZ, BA-BH). However, many BOQs contain no Item Codes or use different identification systems that vary by client, consultant, office, or project.

This investigation will determine what deterministic trade classification authority exists beyond Item Codes.

---

## Research Question

**What alternative evidence sources can provide deterministic trade classification for BOQs without recognizable Item Code patterns?**

Specifically:
1. Which structural properties are **Observable** in section headings?
2. Which hierarchical patterns are **Derivable** from BOQ structure?
3. Which trade-specific keywords exist in description text?
4. What combined strategies could provide broader coverage?

---

## Scope

### In Scope

**Data Sources:**
- Production BOQRow structure: `row_number`, `code`, `description`, `quantity`, `uom`, `row_type`, `section`
- Additional BOQ fixtures beyond CostX format
- Section heading patterns
- Hierarchical relationships
- Description text analysis

**Investigation Methodology:**
- Evidence-first: observe production data, then characterize patterns
- Compare observations against Domain Knowledge Layer
- Identify what is Observable, Derivable, or Not Determinable
- Document all discovered patterns systematically

### Out of Scope

- Implementation of universal classifier
- Machine learning or probabilistic methods
- User preference-based classification
- Recommendations beyond evidence findings

---

## Deliverables

### Required Outputs

1. **Pattern Catalog**: Documented patterns for each evidence source
2. **Coverage Analysis**: Classification success rates by method
3. **Authority Recommendation**: Evidence-based proposal for universal classification
4. **Fallback Strategy**: Handling of unclassifiable items

### Success Criteria

✅ Identified deterministic patterns in ≥1 alternative evidence source
✅ Achieved measurable coverage improvement beyond Item Codes
✅ Defined approach for arbitrary BOQ formats
✅ All recommendations based on fixture evidence

---

## Timeline

**Estimated Duration:** 2-4 weeks

1. **Week 1**: Fixture collection and preliminary analysis
2. **Week 2**: Pattern discovery and documentation
3. **Week 3**: Coverage assessment and validation
4. **Week 4**: Recommendation formulation and reporting

---

## Next Steps

1. **Fixture Collection**: Gather additional BOQ samples
2. **Preliminary Analysis**: Quick assessment of pattern potential
3. **Detailed Investigation**: Systematic pattern discovery
4. **Report Findings**: Document patterns and recommendations

---

## Related Documents

- docs/domain/Trade_Taxonomy.md
- data/reports/eq0016_trade_classification_evidence.md
- docs/decisions/ADR_0026_Trade_Classification_Authority.md