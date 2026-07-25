# Fixture Repository Manifest

**Last Updated**: 2026-07-23
**Total Fixtures**: 32
**Total Categories**: 4

## Repository Structure

```
tests/fixtures/
├── archives/              # Archived fixtures (ZIP format)
├── costx/                 # CostX estimating platform exports
├── cubit/                 # Cubit estimating platform exports (future)
├── generic/               # Generic/unknown platform exports
├── FIXTURE_MANIFEST.md    # This file (authoritative catalogue)
├── FIXTURE_METADATA.py    # Verification API
├── fixtures.json          # Hash registry (integrity verification)
└── README.md              # Repository documentation
```

## Fixture Taxonomy

### Platform Categories

1. **CostX** - CostX estimating software exports
2. **Cubit** - Cubit estimating software exports (future)
3. **Generic** - Unknown or mixed platform exports
4. **Archives** - Original ZIP archives (provenance preservation)

### Export Types

1. **Full BOQ** - Complete Bill of Quantities export
2. **Partial BOQ** - Trade-specific or filtered exports
3. **Formula Workbook** - Export with calculation formulas
4. **Dimension Export** - Raw measurement data
5. **Structural Only** - Structural elements only

### Project Types

1. **Complete Project** - Full project BOQ
2. **Trade Breakdown** - Single trade or package
3. **Structural** - Structural elements only
4. **Finishes** - Architectural finishes
5. **Services** - MEP services

## Fixture Inventory

### CostX Platform (28 fixtures)

| Filename | Platform | Export Type | Project Type | Item Codes | Hierarchy | Headings | Sheet Trade Context | Engineering Use |
|----------|----------|-------------|--------------|------------|-----------|----------|---------------------|------------------|
| full_boq.xlsx | CostX | Full BOQ | Complete Project | ✅ Yes | ❌ No | ❌ No | ❌ No | Primary regression testing (EQ-0007, EQ-0009) |
| full_boq_corrected.xlsx | CostX | Full BOQ | Complete Project | ✅ Yes | ❌ No | ❌ No | ❌ No | Corrected version for edge cases |
| formula_workbook.xlsx | CostX | Formula Workbook | Complete Project | ✅ Yes | ❌ No | ❌ No | ❌ No | Formula validation (M5 analysis) |
| dimensions_export.xlsx | CostX | Dimension Export | Complete Project | ❌ No | ❌ No | ❌ No | ❌ No | Measurement validation |
| Structural Reinforcement Only.xlsx | CostX | Partial BOQ | Structural | ✅ Yes | ❌ No | ❌ No | ❌ No | Structural trade testing |
| full_boq_2.xlsx | CostX | Full BOQ | Complete Project | ✅ Yes | ❌ No | ❌ No | ❌ No | Additional regression coverage |
| full_boq_3.xlsx | CostX | Full BOQ | Complete Project | ✅ Yes | ❌ No | ❌ No | ❌ No | Additional regression coverage |
| full_boq_4.xlsx | CostX | Full BOQ | Complete Project | ✅ Yes | ❌ No | ❌ No | ❌ No | Additional regression coverage |
| full_boq_5.xlsx | CostX | Full BOQ | Complete Project | ✅ Yes | ❌ No | ❌ No | ❌ No | Additional regression coverage |
| full_boq_6.xlsx | CostX | Full BOQ | Complete Project | ✅ Yes | ❌ No | ❌ No | ❌ No | Additional regression coverage |
| Base_Ceiling_BOQ_CostX.xlsx | CostX | Partial BOQ | Finishes | ✅ Yes | ❌ No | ❌ No | ❌ No | Ceiling trade testing |
| Base_Demolition_CostX.xlsx | CostX | Partial BOQ | Services | ✅ Yes | ❌ No | ❌ No | ❌ No | Demolition trade testing |
| Base_Doors_and_Windows_CostX.xlsx | CostX | Partial BOQ | Finishes | ✅ Yes | ❌ No | ❌ No | ❌ No | Door/window trade testing |
| Base_External_Wall_Finishes_CostX.xlsx | CostX | Partial BOQ | Finishes | ✅ Yes | ❌ No | ❌ No | ❌ No | External wall trade testing |
| Base_FFE_CostX.xlsx | CostX | Partial BOQ | Services | ✅ Yes | ❌ No | ❌ No | ❌ No | FF&E trade testing |
| Base_Floor_Finishes_CostX.xlsx | CostX | Partial BOQ | Finishes | ✅ Yes | ❌ No | ❌ No | ❌ No | Floor finishes trade testing |
| Base_Interior_Wall_Finishes_CostX.xlsx | CostX | Partial BOQ | Finishes | ✅ Yes | ❌ No | ❌ No | ❌ No | Interior wall trade testing |
| Base_Joinery_CostX.xlsx | CostX | Partial BOQ | Finishes | ✅ Yes | ❌ No | ❌ No | ❌ No | Joinery trade testing |
| Base_Landscape_CostX.xlsx | CostX | Partial BOQ | Services | ✅ Yes | ❌ No | ❌ No | ❌ No | Landscape trade testing |
| Base_Metal_Works_CostX.xlsx | CostX | Partial BOQ | Services | ✅ Yes | ❌ No | ❌ No | ❌ No | Metal works trade testing |
| Base_Roofing_CostX.xlsx | CostX | Partial BOQ | Services | ✅ Yes | ❌ No | ❌ No | ❌ No | Roofing trade testing |
| Base_Signage_CostX.xlsx | CostX | Partial BOQ | Services | ✅ Yes | ❌ No | ❌ No | ❌ No | Signage trade testing |
| Base_Site_Preparation_Civil_Earthworks_and_Demolition_CostX.xlsx | CostX | Partial BOQ | Services | ✅ Yes | ❌ No | ❌ No | ❌ No | Civil/earthworks trade testing |
| Base_Structural_CostX.xlsx | CostX | Partial BOQ | Structural | ✅ Yes | ❌ No | ❌ No | ❌ No | Structural trade testing |
| Base_Structural_Steel_CostX.xlsx | CostX | Partial BOQ | Structural | ✅ Yes | ❌ No | ❌ No | ❌ No | Structural steel trade testing |
| Base_Wall_Types_CostX.xlsx | CostX | Partial BOQ | Structural | ✅ Yes | ❌ No | ❌ No | ❌ No | Wall types trade testing |
| Preambles_CostX.xlsx | CostX | Partial BOQ | Services | ✅ Yes | ❌ No | ❌ No | ❌ No | Preambles/testing |
| reinforcement_only_2.xlsx | CostX | Partial BOQ | Structural | ✅ Yes | ❌ No | ❌ No | ❌ No | Reinforcement trade testing |

### Cubit Platform (0 fixtures)

*No fixtures with confirmed Cubit provenance. Reserved for future discoveries.*

### Generic Platform (3 fixtures)

| Filename | Platform | Export Type | Project Type | Item Codes | Hierarchy | Headings | Sheet Trade Context | Engineering Use |
|----------|----------|-------------|--------------|------------|-----------|----------|---------------------|------------------|
| client_trade_breadown_1.xlsx | Unknown | Partial BOQ | Trade Breakdown | ❓ Unknown | ❓ Unknown | ❓ Unknown | ❓ Unknown | Client-specific format analysis |
| client_trade_breakdown_2.xlsx | Unknown | Partial BOQ | Trade Breakdown | ❓ Unknown | ❓ Unknown | ❓ Unknown | ❓ Unknown | Client-specific format analysis |
| Structural_Steel_Program_09012024.xlsx | Unknown | Partial BOQ | Structural | ❓ Unknown | ❓ Unknown | ❓ Unknown | ❓ Unknown | Generic structural analysis |

### Archives (1 archive)

| Filename | Contents | Purpose |
|----------|----------|---------|
| new_fixture.zip | Original CostX fixtures (23 files) | Provenance preservation |

## Metadata Fields

### Required Fields
- **Filename**: Exact filename including extension
- **Platform**: Estimating software platform (CostX, Cubit, Generic, Unknown)
- **Export Type**: Type of export (Full BOQ, Partial BOQ, Formula Workbook, etc.)
- **Project Type**: Project classification (Complete Project, Trade Breakdown, Structural, etc.)
- **Item Codes**: ✅ Yes / ❌ No / ❓ Unknown
- **Hierarchy**: ✅ Yes / ❌ No / ❓ Unknown
- **Headings**: ✅ Yes / ❌ No / ❓ Unknown
- **Sheet Trade Context**: ✅ Yes / ❌ No / ❓ Unknown
- **Engineering Use**: Primary purpose in testing/validation

### Optional Fields
- **Acquisition Date**: When fixture was added to repository
- **SHA-256 Hash**: For integrity verification (in fixtures.json)
- **Evidence References**: Related Engineering Questions or ADRs
- **Notes**: Additional context or limitations

## Adding New Fixtures

### Registration Process
1. **Place fixture** in appropriate platform subdirectory
2. **Run registration tool**:
   ```bash
   python tools/register_fixture.py <path_to_fixture> --description "Purpose"
   ```
3. **Update manifest** with metadata
4. **Verify integrity** with existing tests

### Naming Convention
- **CostX**: `Base_<Trade>_CostX.xlsx` or `full_boq_<N>.xlsx`
- **Cubit**: `cubit_<project>_<type>.xlsx` (when available)
- **Generic**: `client_<description>.xlsx` or `<project>_<date>.xlsx`
- **Archives**: Original filenames preserved

### Directory Structure Rules
- **Platform first**: `costx/`, `cubit/`, `generic/`
- **Purpose-based subdirectories**: Only if evidence supports (e.g., `costx/structural/`)
- **Flat structure preferred**: Avoid unnecessary nesting
- **README.md**: Each platform directory should have documentation

## Future Maintenance

### Category Expansion
When adding new platform categories:
1. Create evidence-based directory (e.g., `cubit/` when Cubit fixtures available)
2. Update this manifest with platform-specific metadata
3. Add platform to README.md structure documentation
4. Ensure registration tool supports new category

### Deprecation Policy
- **Obsolete fixtures**: Move to `archives/` with deprecation notice
- **Corrupted fixtures**: Remove and update manifest
- **Duplicate fixtures**: Keep one, archive others with cross-reference

### Integrity Verification
```python
from tests.fixtures.FIXTURE_METADATA import verify_fixture

# Verify fixture exists and hash matches
fixture_path = verify_fixture("full_boq.xlsx")
```

## Governance

### Principles
- **Evidence-first**: Categories based on observed fixtures
- **Deterministic**: No manual metadata modification
- **Traceable**: All changes documented in manifest
- **Single source**: This file is authoritative catalogue

### Version History
- **2026-07-23**: Initial manifest creation (EQ-0016 reorganization)
- **2026-07-14**: Original fixtures.json registry established
- **2026-07-08**: Repository structure documented

**Next Review**: When new platform category is added or major reorganization occurs