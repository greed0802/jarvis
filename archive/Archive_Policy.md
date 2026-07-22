# Archive Policy — Jarvis Repository

**Version**: 1.0
**Effective Date**: 2026-07-22
**Part of**: Repository Foundation Freeze

---

## Core Principle

**Nothing is deleted. Ever.**

Historical engineering artifacts are permanent evidence. If something is obsolete, superseded, or no longer actively referenced, it is archived — never removed.

This policy ensures the repository preserves its complete engineering history for future investigation, audit, and reference.

---

## Classification System

Every repository artifact (file, directory, dataset) shall be classified into one of these categories:

### Active
- **Definition**: Currently used, maintained, and relied upon.
- **Location**: Stays in its original position in the repository.
- **Examples**: app.py, AGENTS.md, src/jarvis/**, tests/**, tools/quality/*
- **Modification**: May be modified as part of normal engineering work.

### Historical Evidence
- **Definition**: Engineering artifacts from completed work that remain valuable for reference.
- **Location**: Moved to `archive/reports/` (for reports) or `archive/` with original directory structure preserved.
- **Examples**: Milestone status reports from prior eras, architecture sync reviews, old investigation summaries.
- **Modification**: Never modified. Immutable engineering history.

### Archive
- **Definition**: Superseded material no longer relevant to current or future work.
- **Location**: `archive/` with original directory structure preserved.
- **Examples**: Old release notes for superseded versions, deprecated configuration files.
- **Modification**: Never modified. Frozen historical reference.

### Deprecated
- **Definition**: Still present in the repository but no longer recommended for use. Has a documented replacement.
- **Location**: Stays in original location with deprecation notice. May be archived in a future sprint.
- **Examples**: Code pending migration, old API versions still in active use.
- **Modification**: May only be moved to archive/. No enhancements.

### Temporary
- **Definition**: Created for a specific transient purpose; no longer needed.
- **Location**: Moved to `archive/temporary/`.
- **Examples**: Debug scripts, one-off experiments, draft notes that have been resolved.
- **Modification**: May be deleted only if explicitly superseded by another artifact.

---

## Archive Directory Structure

```
archive/
├── Archive_Policy.md               ← This policy document
├── Archive_Inventory.md            ← Complete inventory of all archived items
│
├── reports/                        ← Historical reports and status documents
│   ├── [original filename].md
│
├── docs/                           ← Archived documentation (future use)
│   └── [original path structure preserved]
│
├── planning/                       ← Archived planning artifacts (future use)
│   └── [original path structure preserved]
│
├── prompts/                        ← Archived AI prompts (future use)
│   └── [original path structure preserved]
│
├── temporary/                      ← Temporary artifacts awaiting classification
│   └── [original path structure preserved]
```

### Archiving Rules

1. **Preserve original directory structure** where practical. A file originally at `docs/old/report.md` should be archived at `archive/docs/old/report.md`.

2. **Always record in Archive_Inventory.md.** Every archived artifact shall be recorded with: original path, classification, reason for archival, and date archived.

3. **Only archive non-production files.** Production code (`src/jarvis/`), tests (`tests/`), and quality tools (`tools/quality/`) are never archived while the repository is active.

4. **Check consumers before archiving .** If any active document references the artifact being considered for archive, update the reference before moving.

5. **Never archive without a freeze assessment.** Archiving is a sprint activity, not an implied thing during daily work.

---

## What May NOT Be Archived

The following are permanently active and shall not be archived:

- Production source code (src/jarvis/)
- Tests (tests/)
- Quality verification tools (tools/quality/)
- ADRs (docs/decisions/)
- Contract files (docs/contracts/)
- Source of truth architecture documents (docs/00-05_*)
- AGENTS.md (root)
- README.md (root)
- version.py (src/jarvis/version.py)
- pytest.ini
- requirements.txt
- .gitignore
- LICENSE

---

## Current Archive Inventory

As of 2026-07-22, the archive contains:

### archive/reports/ — Historical Evidence

| File | Original Location | Classification | Reason |
|---|---|---|---|
| ARCHITECTURE_STATUS.md | Root | Historical Evidence | M7-era status; superseded by docs/26_Implementation_Status.md |
| ARCHITECTURE_SYNC_REVIEW.md | Root | Historical Evidence | Comprehensive architecture sync audit (2026-07-08); findings captured in knowledge base |
| ARCHITECTURE_SYNC_SUMMARY.md | Root | Historical Evidence | Executive summary of ARCHITECTURE_SYNC_REVIEW.md |
| RELEASE_v0.0.1-alpha.9.md | Root | Archive | Superseded release notes |

---

## Future Archive Process

When new artifacts need to be archived:

1. **Identify**: Determine which files are no longer active
2. **Classify**: Apply one of the 5 classification categories
3. **Assess**: Check for consumers (are any active documents referencing this file?)
4. **Document**: Update Archive_Inventory.md
5. **Execute**: Move the file(s) to the appropriate archive location
6. **Verify**: Ensure no broken references remain in active documents

---

## Deletion Policy

**Default: DELETE.**

Exceptions require Products Owner. Valid reasons:
- Temporary artifacts that served their purpose and have no historical value
- Automatically generated files that can be regenerated
- Accidental duplicates created in error

Even in these cases, deletion should be confirmed by Project Owner.

---

## Audit Schedule

The archive shall be reviewed:
- At each Foundation Freeze milestone
- When preparing for a major release
- When repository restructuring is planned

---

**Policy Adopted**: 2026-07-22
**Next Review**: At next foundation-level milestone