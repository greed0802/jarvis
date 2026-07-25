# Cubit Fixture Category

## Purpose

This directory contains BOQ fixtures exported from the Cubit estimating platform. These fixtures are used for:

- Cubit format compatibility testing
- Cross-platform pattern analysis
- Trade classification validation
- Format-specific regression testing

## Current Fixtures

| Fixture | Description | Notes |
|---------|-------------|-------|
| client_trade_breadown_1.xlsx | University of Sydney - Ross Street Teaching and Learning Hub | Project tender summary with trade breakdowns |
| client_trade_breakdown_2.xlsx | SINSW - New Primary School in Calderwood | Tender schedules with trade breakdowns |
| Structural_Steel_Program_09012024.xlsx | Structural steel program | Dated 2024-01-09, for import to CostX |

## Usage Guidelines

### Analysis Priority

1. **Format Characterization**: Document Cubit-specific patterns
2. **Cross-Platform Comparison**: Compare with CostX exports
3. **Trade Classification**: Validate trade patterns across platforms
4. **Regression Testing**: Add to test suite when format is stable

### Testing Considerations

- **Cubit Format**: May differ from CostX in structure and patterns
- **Manual Review**: Some fixtures require human analysis
- **Format Evolution**: Cubit exports may change between versions
- **Research Use**: Primarily for engineering investigations

## Related Documents

- FIXTURE_MANIFEST.md (authoritative catalogue)
- EQ-0016 (Trade Classification Authority Investigation)
- ADR-0026 (Trade Classification Authority)