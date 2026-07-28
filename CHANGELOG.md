# Changelog

All notable changes to the Jarvis repository are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## v0.0.1-alpha.16

### Repository Governance

- Completed Repository Governance Harmonization
- Completed Repository Governance Finalization
- Resolved Engineering Question identifier collisions
- Separated Knowledge Engineering into an independent workstream
- Established register-driven repository governance
- Created Workstream Governance Charter
- Updated Engineering Register
- Repository prepared for Execution Architecture

**No production code changes.**

---

## v0.0.1-alpha.15

### Knowledge Engineering

- Established Knowledge Engineering Foundation (KE-0001)
- Created knowledge workspace (`knowledge/`) and inbox (`knowledge_inbox/`)
- Created Knowledge Storage Policy (`docs/knowledge/Knowledge_Storage_Policy.md`)
- Created knowledge inventory tooling (`tools/knowledge/create_knowledge_inventory.py`)
- Documented 1,856 knowledge assets (24.16 GB)

**No production code changes. No architecture changes.**

---

## v0.0.1-alpha.14

### CheckMate Application

- Implemented CP-0001 — CheckMate (BOQ Consumer Application)
- Completed EQ-0020 — BOQ Intelligence Consumer Architecture (Frozen)
- Completed EQ-0021 — CheckMate Application Architecture (PERMANENTLY FROZEN)
- Added `src/jarvis/applications/checkmate/` (47 production files)
- Added `tests/applications/checkmate/` (33 test files)
- Total repository tests: 944 passing (8 skipped)

---

## v0.0.1-alpha.13

### BOQ Intelligence Increment 4

- Implemented IP-0001 — 8 semantic capabilities (PERMANENTLY FROZEN)
- SEM-PROD-01/02/04/05/06/07/09/12 implemented
- Extended BOQ Intelligence with `include_semantic` flag
- Added 53 tests (98 total BOQ Intelligence tests)
- Added Implementation Governance v1.0

---

## v0.0.1-alpha.12

### Governance Automation v1.0

- Completed EQ-0017 — Repository Governance Automation
- Created shared governance library (`tools/quality/shared_governance.py`)
- Created 5 governance validators
- Added manifest-driven discovery (`tools/manifest.json`)
- Added unified orchestration (`tools/quality/verify_all.py`)

---

## v0.0.1-alpha.11

### Validation Engine

- Completed EQ-0013 — Validation Engine (Frozen)
- Implemented 18 validation rules
- Created Validation Findings Contract v1.0
- Added validation engine (`src/jarvis/engines/validation/engine.py`)

---

## v0.0.1-alpha.10

### Public Evidence Contract

- Completed EQ-0012 — BOQ Intelligence Public Evidence Contract (Frozen v1.0.0)
- 857-line contract with 77 invariants and 16 consumer guarantees
- 63/63 MATCH verification against production
- 5 stable import paths documented
- MAJOR/MINOR/PATCH versioning policy

---

## v0.0.1-alpha.9

### BOQ Intelligence Increment 1

- Implemented first approved Capability (BOQ Intelligence)
- Pure functions over `list[BOQRow]`
- 26 acceptance tests verifying against EQ-0007 evidence
- 7/7 known anomalies correctly detected
- No architectural expansion

---