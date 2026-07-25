# EQ-0017 — Trade Classification Authority Investigation

## Status
OPEN

## Purpose

Determine the deterministic authority for trade classification across arbitrary BOQ formats.

## Background

### Current Implementation (CB-0005)

CB-0005 implemented trade classification using Item Code prefixes from CostX fixture analysis:

- **Scope**: Item-Code-based BOQs (CostX format)
- **Method**: Prefix matching (A-Z, AA-AZ, BA-BH patterns)
- **Status**: Production-ready for supported formats
- **Limitation**: Not universal across all BOQ formats

### Architectural Gap

**Problem**: Item Codes are not present in all BOQ formats and vary by client/consultant/office/project.

**Impact**: Current implementation cannot classify trades in BOQs without recognizable Item Code patterns.

## Engineering Question

**What is the deterministic authority for universal trade classification across arbitrary BOQ formats?**

## Investigation Scope

### Evidence Sources to Analyze

1. **Section Headings**
   - Trade-related keywords in section names
   - Hierarchical section patterns
   - Section grouping conventions

2. **Hierarchy Patterns**
   - Parent-child relationships
   - Level-based classification
   - Structural containment

3. **Description Text**
   - Keyword extraction
   - Pattern matching
   - Trade-specific terminology

4. **Item Codes** (where present)
   - Extended prefix patterns
   - Alternative coding systems
   - Client-specific conventions

5. **Workbook Metadata**
   - Workbook properties
   - Custom properties
   - Document structure

6. **Combined Strategies**
   - Multi-source evidence fusion
   - Fallback mechanisms
   - Confidence scoring

### Research Questions

1. **Section Analysis**: Can section headings provide reliable trade classification?
2. **Hierarchy Patterns**: Do structural relationships indicate trade categories?
3. **Description Patterns**: Are there deterministic text patterns by trade?
4. **Alternative Codes**: What other coding systems exist beyond Item Codes?
5. **Fallback Strategies**: How to handle BOQs with insufficient evidence?
6. **Combined Authority**: Can multiple evidence sources provide universal coverage?

## Methodology

### Evidence Collection

1. **Fixture Analysis**: Analyze additional BOQ fixtures beyond CostX
2. **Pattern Discovery**: Identify trade-related patterns in each evidence source
3. **Coverage Assessment**: Determine what percentage of BOQs each method can classify
4. **Conflict Resolution**: Define rules for conflicting evidence sources

### Analysis Approach

1. **Deterministic Only**: No ML, no probabilistic methods
2. **Evidence-First**: Base decisions on actual fixture data
3. **Pattern Documentation**: Record all discovered patterns
4. **Coverage Metrics**: Measure classification success rates

## Deliverables

### Required Outputs

1. **Pattern Catalog**: Documented patterns for each evidence source
2. **Coverage Analysis**: Classification success rates by method
3. **Authority Recommendation**: Primary evidence source for universal classification
4. **Fallback Strategy**: Handling of unclassifiable items
5. **Implementation Plan**: Roadmap for universal classifier

### Success Criteria

✅ **Pattern Discovery**: Identified deterministic patterns in ≥1 alternative evidence source
✅ **Coverage Improvement**: Achieve >50% classification coverage beyond Item Codes
✅ **Universal Strategy**: Defined approach for arbitrary BOQ formats
✅ **No Speculation**: All recommendations based on fixture evidence

## Out of Scope

❌ **Implementation**: This EQ defines requirements, not solutions
❌ **ML/AI**: No machine learning or probabilistic methods
❌ **User Preferences**: No subjective classification rules
❌ **Recommendations**: No engineering advice beyond evidence

## Timeline

### Estimated Duration: 2-4 weeks

1. **Week 1**: Fixture collection and preliminary analysis
2. **Week 2**: Pattern discovery and documentation
3. **Week 3**: Coverage assessment and conflict resolution
4. **Week 4**: Recommendation formulation and reporting

## Stakeholders

- **Architecture Team**: Authority assessment
- **Engineering Team**: Pattern analysis
- **QS Domain Experts**: Trade classification validation
- **CheckMate Team**: Consumer requirements

## Dependencies

- **Fixture Access**: Additional BOQ samples for analysis
- **Domain Expertise**: QS input on trade patterns
- **ADR-0006**: Architectural context

## Risks

1. **Insufficient Patterns**: May not find deterministic patterns in alternative sources
2. **Limited Coverage**: Universal solution may still have gaps
3. **Complexity**: Combined strategies may increase implementation complexity
4. **Performance**: Multi-source analysis may impact processing speed

## Mitigation Strategies

1. **Expand Fixture Set**: Analyze more diverse BOQ samples
2. **Fallback Planning**: Define graceful degradation strategies
3. **Modular Design**: Allow incremental pattern adoption
4. **Performance Budget**: Set acceptable processing limits

## Next Steps

1. **Fixture Collection**: Gather additional BOQ samples
2. **Preliminary Analysis**: Quick assessment of pattern potential
3. **Detailed Investigation**: Systematic pattern discovery
4. **Report Findings**: Document patterns and recommendations

## Conclusion

EQ-0017 will provide the evidence-based foundation for universal trade classification. The investigation follows Jarvis principles of deterministic, evidence-first engineering while acknowledging the architectural limitations of the current Item-Code-based implementation.

**Status**: Ready for engineering investigation
**Priority**: High (blocks universal trade classification)
**Impact**: Architectural (defines future classification authority)