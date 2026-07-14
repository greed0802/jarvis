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

## Current Fixtures

### CostX (`costx/`)

| Fixture | Description | Evidence |
|---------|-------------|----------|
| `full_boq.xlsx` | Primary CostX BOQ export | EQ-0007, EQ-0009 |
| `formula_workbook.xlsx` | CostX export with formulas | M5 analysis |
| `dimensions_export.xlsx` | CostX dimension export | M5 analysis |

## Future Fixture Categories

When adding new fixture categories:

1. Create subdirectory (e.g., `cubit/`, `pdf/`)
2. Place fixture file in subdirectory
3. Register via `tools/register_fixture.py`
4. Update this README with category description

**Note:** Registry keys currently use filenames. If multiple categories introduce filename collisions (e.g., `costx/full_boq.xlsx` and `cubit/full_boq.xlsx`), the registry key should be promoted to the relative path. See TODO in `tools/register_fixture.py`.

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