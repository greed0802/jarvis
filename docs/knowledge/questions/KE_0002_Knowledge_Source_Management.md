# KE-0002: Knowledge Source Management

## 1. Engineering Question
How can we establish a deterministic, verifiable, and provenance-preserving knowledge source management system that scales to tens of thousands of engineering documents without manual fragility or data loss?

**Status:** In Progress
**Engineering Stream:** Knowledge Engineering
**Date:** 2026-07-27

## 2. Background
KE-0001 established the structural boundaries and storage governance for the Knowledge Engineering (KE) workstream. Currently, the repository contains a staging area (`knowledge_inbox/`) holding 1,856 raw engineering documents (24.16 GB), and an initial draft `knowledge_inventory.csv`.

However, the current inventory is only a raw path listing. It does not fulfill the mandatory metadata requirements defined in `KNOWLEDGE_REGISTER.md`, nor does it provide deterministic identity (cryptographic provenance), continuous duplication detection, or automated state verification.

## 3. Gap Analysis
Review of the current repository state reveals the following gaps:

1. **Identity & Provenance:** Existing `DOC-XXXXX` identifiers are dynamically assigned by script position during `os.walk()`. They are not deterministic or stable across script runs. Cryptographic hashes (SHA-256) are missing in the inventory.
2. **Metadata Compliance:** The current CSV lacks mandatory fields defined in `KNOWLEDGE_REGISTER.md` (Authority, State, Version, OCR Required).
3. **Registry Format:** CSV is insufficient for complex metadata evolution. A structured format (JSON/JSONL) with explicit schema validation is needed for automated verification.
4. **Validation Tooling:** No mechanisms exist to automatically verify that the registry matches physical file states, detect missing files, or identify duplicate blobs.

## 4. Engineering Proposal
To fulfill the KE-0001 constitutional principles of immutability and determinism, KE-0002 proposes the following infrastructure improvements:

### 4.1. Registry Architecture
- **Format:** Migrate from simple CSV to a strongly-typed JSON schema (`knowledge_manifest.json` or `.jsonl`) accompanied by a formal JSON schema definition.
- **Identity (Primary Key):** Implement a UUID v5 derived deterministically from the file's SHA-256 hash or a permanent `KN-XXXX` registry sequence.
- **Integrity:** Every registered asset must embed its SHA-256 hash.

### 4.2. Governance Additions
- **Naming Standard:** Create `knowledge/governance/NAMING_STANDARD.md` to define how categorized folders and assets are labeled before final promotion.
- **Validation Rules:** Create `knowledge/governance/VALIDATION_RULES.md` documenting the invariants the registry must pass (e.g., file existence, hash match, mandatory metadata).

### 4.3. Tooling
Introduce deterministic tooling under `tools/knowledge/`:
1. `validate_sources.py`: Scans the registry against the filesystem, verifying file existence and cryptographic hashes.
2. `register_asset.py` / `build_registry.py`: Deterministically registers new assets, assigning permanent IDs and extracting baseline metadata (size, hash, extension) without modifying the source files.

## 5. Risk Assessment & Impact Classification

Per the **Repository Preservation Rule**, the proposed operations are classified as follows:

- **Creating Governance Docs:** Additive (Safe)
- **Creating Tools:** Additive (Safe)
- **Generating/Updating Manifests:** Transformative (Modifies KE metadata in `knowledge/registry/` only)
- **Touching Source Documents:** Read-Only (Safe - Generating hashes/stats)

**Risk Profile:** Very Low
**Justification:** All proposed implementations manipulate *metadata* and *tools* strictly within repository boundaries (`knowledge/registry/`, `tools/knowledge/`, `docs/`). Zero source files (`.pdf`, `.xlsx`, `.cbx`) will be moved, deleted, renamed, or modified.

## 6. Execution Plan
1. Define the Registry JSON Schema & Naming Standards in `knowledge/governance/`.
2. Implement deterministic knowledge tooling (Hashing, Registration, Validation).
3. Convert the existing `knowledge_inventory.csv` into a compliant `knowledge_manifest.json`.
4. Run validation checks to prove integrity.
5. Create Final Implementation Report.

## Governance Note

This Knowledge Engineering item was relocated from `docs/engineering/questions/` to `docs/knowledge/questions/` during the Repository Governance Harmonization Sprint (2026-07-28) to enforce the workstream separation rule: Knowledge Engineering (KE) is an independent governance stream, not an Engineering Question (EQ). Content remains unchanged. The original date and status are preserved for traceability.