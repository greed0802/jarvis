# Generic Fixture Category

## Purpose

This directory contains BOQ fixtures from unknown or mixed estimating platforms. These fixtures are used for:

- Analyzing non-standard BOQ formats
- Testing format compatibility
- Identifying universal patterns
- Client-specific format validation

## Current Fixtures

### Client-Specific Formats

| Fixture | Description | Notes |
|---------|-------------|-------|
| client_trade_breadown_1.xlsx | Client trade breakdown format | Unknown platform, requires analysis |
| client_trade_breakdown_2.xlsx | Client trade breakdown format | Unknown platform, requires analysis |
| Structural_Steel_Program_09012024.xlsx | Structural steel program | Unknown platform, dated 2024-01-09 |

## Usage Guidelines

### Analysis Priority

1. **Format Identification**: Determine estimating platform if possible
2. **Pattern Extraction**: Identify trade classification patterns
3. **Compatibility Testing**: Validate with existing parsers
4. **Documentation**: Record findings in manifest

### Testing Considerations

- **Unknown Formats**: May not work with existing parsers
- **Manual Review**: Often requires human analysis
- **Limited Automation**: Not suitable for regression testing without characterization
- **Research Use**: Primarily for engineering investigations

## Future Work

- **Platform Identification**: Determine originating software
- **Pattern Documentation**: Record observed structures
- **Classification**: Move to specific platform category when identified
- **Characterization**: Add to manifest with full metadata

## Related Documents

- FIXTURE_MANIFEST.md (authoritative catalogue)
- EQ-0016 (Trade Classification Authority Investigation)
- ADR-0026 (Trade Classification Authority)