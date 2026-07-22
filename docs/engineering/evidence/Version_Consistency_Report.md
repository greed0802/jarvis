# Version Consistency Report

**Date:** 2026-07-22
**Authority:** Engineering Authority — Priority of Truth
**Canonical Version:** `0.0.1-alpha` (from `src/jarvis/version.py` — Production code, Authority #1)

---

## Methodology

Per the Evidence Hierarchy:
1. Production Source Code (Authority #1)
2. Frozen Contracts (Authority #2)
3. Frozen Engineering Evidence (Authority #3)
4. Engineering Questions (Authority #4)
5. Knowledge Base (Authority #5)
6. Architecture Documents (Authority #6)
7. Planning Documents (Authority #7)
8. Historical Documents (Authority #8)

The canonical version is extracted from `src/jarvis/version.py` (`__version__ = "0.0.1-alpha"`), which is production source code (highest authority). Lower-authority documents are updated to match when they diverge.

---

## Full Version Reference Inventory

### Production Code

| File | Version | Notes |
|------|---------|-------|
| `src/jarvis/version.py` | `0.0.1-alpha` | **CANONICAL.** `__version__ = "0.0.1-alpha"`. Comment: "Platform version - aligns with architecture version v0.0.1-alpha" |
| `src/jarvis/__init__.py` | — | Imports `__version__` from `version.py`. No independent version string. |
| `app.py` | — | No version string. |

### Frozen Contracts (Independent Semver)

| File | Version | Notes |
|------|---------|-------|
| `docs/contracts/BOQ_Intelligence_Public_Evidence_Contract_v1.0.md` | `1.0.0` | Contract version, not software version. Independent semver. |
| `docs/contracts/Validation_Findings_Contract_v1.0.md` | `1.0.0` | Contract version. Independent semver. |

### Documentation

| File | Version | Type | Match Canonical? |
|------|---------|------|-----------------|
| `README.md` | `0.0.1-alpha` | Software version | ✓ |
| `docs/26_Implementation_Status.md` | `0.0.1-alpha` (Software Version, line 27) | Software version | ✓ |
| `docs/26_Implementation_Status.md` | `0.1` (Document Version, line 3) | Document version | N/A — not software |

### Quality Tools / Infrastructure

| File | Version | Notes |
|------|---------|-------|
| `tools/quality/Tool_Registry.md` | `1.0` | Registry document version. Not a software version. |
| `tools/manifest.json` | — | No version field. Schema version not yet needed. |

### Historical

| File | Version | Notes |
|------|---------|-------|
| `RELEASE_v0.0.1-alpha.9.md` | `v0.0.1-alpha.9` | Historical release note. Version identifies the release, not current state. Correctly preserved. |

### Engineering Evidence (Frozen)

| File | Version | Notes |
|------|---------|-------|
| `docs/engineering/questions/EQ_0013_Validation_Engine.md` | `v0.0.1-alpha.9` | Historical context reference. Correct for when EQ was authored. |
| `docs/engineering/evidence/EQ_0013_Spike3_Evidence_Report_Engine_Scope_and_Responsibilities.md` | `v0.0.1-alpha.10` | Historical. Predated M10 version sync. Lower authority. |
| `docs/engineering/evidence/M9_Freeze_Report.md` | References `v0.0.1-alpha.9` | Historical. Documents M9 freeze state. |
| `docs/engineering/evidence/EQ_0013_Final_Freeze_Report.md` | `v0.0.1-alpha.11` | Historical. Documents EQ-0013 freeze tag. |
| `docs/engineering/evidence/M10_Maintenance_Report.md` | `0.0.1-alpha` | Documents the resolution. |

---

## verify_versions.py Tool Output

```json
{
  "tool": "verify_versions",
  "overall_pass": true,
  "sources": {
    "README.md": "0.0.1-alpha",
    "src/jarvis/version.py": "0.0.1-alpha",
    "docs/contracts/BOQ_Intelligence_Public_Evidence_Contract_v1.0.md": "1.0.0",
    "docs/contracts/Validation_Findings_Contract_v1.0.md": "1.0.0",
    "RELEASE_v0.0.1-alpha.9.md": "0.0.1-alpha.9"
  },
  "mismatches": []
}
```

---

## Resolution Actions (Previously Applied in M10)

| File | Before | After | Reason |
|------|--------|-------|--------|
| `README.md` | `v0.0.1-alpha.9` | `0.0.1-alpha` | Match canonical production version |
| `docs/26_Implementation_Status.md` | `0.0.1-alpha.11` (Software Version) | `0.0.1-alpha` | Match canonical production version |
| `tools/quality/verify_versions.py` | Included RELEASE_* in app version comparison | Excludes RELEASE_* from app version comparison | Release notes are historical records, not current version sources |

### Not Changed (Correctly Preserved)
- `src/jarvis/version.py` — Production code, highest authority, no change needed
- `RELEASE_v0.0.1-alpha.9.md` — Historical release note, version in name identifies the release
- `docs/contracts/*.md` — Contracts use independent semver (`1.0.0`), not software version
- All historical evidence reports — Frozen engineering evidence, correctly reflect their era

---

## Remaining Notes

1. **`docs/26_Implementation_Status.md` line 3: "Version: 0.1"** — This is the document's own version metadata (document version), not the software version. The software version is correctly listed at line 27 as `0.0.1-alpha`. No change needed.

2. **Contract versions (`1.0.0`)** — Contracts use semantic versioning independent of software version. This is correct and intentional per ADR-0012 (Repository Structure) and the contract design.

3. **Historical evidence versions** — Frozen engineering evidence files reference the software version current at their creation time (e.g., `v0.0.1-alpha.9`, `v0.0.1-alpha.10`, `v0.0.1-alpha.11`). These are accurate historical markers and should not be modified.

---

## Conclusion

All repository version references are consistent with the canonical production version `0.0.1-alpha`. The verify_versions quality tool reports zero mismatches. No version drift is present.