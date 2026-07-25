# Test Fixtures

This directory contains authoritative test fixtures used for regression testing and acceptance verification.

## Structure

```
tests/fixtures/
├── fixtures.json          # Authoritative fixture metadata (single source of truth)
├── FIXTURE_METADATA.py    # Verification API (loads from fixtures.json)
├── README.md              # This file
├── costx/                 # CostX export fixtures
│   ├── full_boq.xlsx      # Primary BOQ export (EQ-0007, EQ-0009)
│   ├── formula_workbook.xlsx
│   ├── dimensions_export.xlsx
│   └── README.md
└── [future categories]    # cubit/, pdf/, etc.
```

## Fixture Integrity Verification

All fixtures are registered with SHA-256 hashes in `fixtures.json`.

**Tests verify fixture integrity before execution:**

```python
from tests.fixtures.FIXTURE_METADATA import verify_fixture

def test_something():
    fixture_path = verify_fixture("full_boq.xlsx")
    # Use fixture_path...
```

If a fixture is modified or corrupted, tests fail immediately with a hash mismatch error.

## Registering New Fixtures

Fixture registration is an **explicit engineering action** performed via the registration tool.

**Usage:**

```bash
python tools/register_fixture.py <path_to_fixture> [--description DESC]
```

**Example:**

```bash
python tools/register_fixture.py tests/fixtures/cubit/new_export.xlsx --description "Cubit BOQ export for testing"
```

The tool:
1. Computes SHA-256 hash
2. Checks for duplicates (name, hash, path)
3. Adds entry to `fixtures.json` with acquisition date
4. Sorts entries for deterministic git diffs

**Registration principles:**
- Tests verify fixtures, never modify metadata
- Registration is deliberate, not automatic
- Each fixture has unique name, hash, and path
- Acquisition date is recorded automatically

## Fixture Metadata Schema

Each fixture entry in `fixtures.json` contains:

```json
{
  "filename.xlsx": {
    "path": "category/filename.xlsx",
    "sha256": "hex_digest",
    "description": "Purpose and context",
    "acquired": "YYYY-MM-DD"
  }
}
```

**Fields:**
- `path`: Relative path from `tests/fixtures/` (forward slashes)
- `sha256`: SHA-256 hash of fixture file
- `description`: Human-readable purpose
- `acquired`: Date fixture was registered (ISO 8601)

## Current Fixture Categories

### CostX (`costx/`)

Primary CostX estimating software exports used for regression testing and validation.

**Fixtures**: 28 files including full BOQs, trade breakdowns, and specialized exports
**Documentation**: See `costx/README.md` for detailed descriptions
**Evidence**: EQ-0007, EQ-0009, M5 analysis

### Generic (`generic/`)

Unknown or mixed platform exports for format compatibility analysis.

**Fixtures**: 3 files from client-specific or unknown formats
**Documentation**: See `generic/README.md` for analysis guidelines
**Status**: Requires platform identification and characterization

### Cubit (`cubit/`)

Reserved for future Cubit estimating platform exports.

**Fixtures**: 0 (placeholder directory)
**Status**: Will be populated when Cubit fixtures with confirmed provenance become available

### Archives (`archives/`)

Original fixture archives preserved for provenance.

**Contents**: 1 archive (new_fixture.zip) containing original CostX batch
**Documentation**: See `archives/README.md` for archive policy

## Adding New Fixtures

### Registration Process
1. **Place fixture** in appropriate platform subdirectory
2. **Run registration tool**:
   ```bash
   python tools/register_fixture.py <path_to_fixture> --description "Purpose"
   ```
3. **Update manifest** (`FIXTURE_MANIFEST.md`) with metadata
4. **Verify integrity** with existing tests

### Category Expansion Rules
When adding new platform categories:

1. **Evidence-based**: Create directory only when fixtures exist
2. **Documentation**: Add platform README.md with purpose and guidelines
3. **Manifest update**: Add category to `FIXTURE_MANIFEST.md`
4. **README update**: Update this file with category description

**Example**:
```bash
mkdir -p tests/fixtures/cubit
echo "# Cubit Fixtures" > tests/fixtures/cubit/README.md
# Add fixtures and update manifest
```

### Naming Conventions
- **CostX**: `Base_<Trade>_CostX.xlsx` or `full_boq_<N>.xlsx`
- **Cubit**: `cubit_<project>_<type>.xlsx` (when available)
- **Generic**: `client_<description>.xlsx` or `<project>_<date>.xlsx`
- **Archives**: Original filenames preserved with dates

## Repository Organization

**Authoritative Catalogue**: `FIXTURE_MANIFEST.md`
**Integrity Verification**: `fixtures.json` (SHA-256 hashes)
**Platform Documentation**: Each category has README.md
**Addition Process**: Explicit registration required

See `FIXTURE_MANIFEST.md` for complete inventory and metadata fields.

## Engineering Principles

- **Deterministic:** Running pytest never modifies fixture metadata
- **Explicit:** Registration requires deliberate action
- **Verifiable:** SHA-256 hashes ensure fixture integrity
- **Traceable:** Acquisition dates and descriptions provide context
- **Single source of truth:** `fixtures.json` is the authoritative registry

## References

- EQ-0007: Production Extraction Report
- EQ-0009: Context Discovery Report
- Capability Evaluation 001: BOQ Intelligence approval
- Amendment A4: Fixture integrity verification requirement