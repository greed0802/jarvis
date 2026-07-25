# Fixture Archives

## Purpose

This directory preserves original fixture archives for provenance and historical reference. Archives are retained when:

1. **Provenance Preservation**: Original download format must be maintained
2. **Batch Imports**: Multiple fixtures received in single archive
3. **Historical Reference**: Significant repository milestones
4. **Deprecation**: Obsolete fixtures moved from active use

## Current Archives

| Archive | Contents | Purpose | Date |
|---------|----------|---------|------|
| new_fixture.zip | 23 CostX fixtures (Base_* and full_boq_*) | Original batch import | 2026-07-23 |

## Archive Policy

### When to Archive

✅ **Original Downloads**: Preserve ZIP/RAR format from source
✅ **Batch Imports**: Multiple related fixtures in single archive
✅ **Historical Snapshots**: Major repository versions
✅ **Deprecated Fixtures**: Replaced by corrected versions

❌ **Individual Fixtures**: Should be extracted to platform directories
❌ **Temporary Files**: Working files, not final fixtures
❌ **Corrupted Files**: Remove entirely, document in manifest

### Extraction Rules

1. **Extract for Use**: Active fixtures should be in platform directories
2. **Preserve Original**: Keep archive for provenance
3. **Document Contents**: List files in archive README
4. **No Nested Archives**: Extract all levels for accessibility

## Future Archives

When creating new archives:

```bash
# Create archive with timestamp
zip fixtures_$(date +%Y%m%d).zip *.xlsx

# Move to archives/
mv fixtures_*.zip archives/

# Document in archives/README.md
```

## Related Documents

- FIXTURE_MANIFEST.md (authoritative catalogue)
- Repository structure documentation