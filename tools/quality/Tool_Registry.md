# Tool Registry — `tools/quality/`

**Authority:** Quality Gate 2 (Architecture Verification)
**Owner:** Repository Engineering
**Version:** 1.0
**Status:** Active

---

## Purpose

This registry documents all permanent quality tools under `tools/quality/`. These tools provide repeatable, deterministic verification of repository engineering claims. They are composable for CI pipelines via the `verify_all.py` orchestrator.

---

## Tool Contract

Every tool SHALL support:

- `--help` — Self-documenting usage
- `--json` — JSON output to stdout
- `--strict` — Fail on any finding (non-zero exit)
- `--output <path>` — Write report to file (.json or .md)

Exit codes:
- `0` = PASS (no findings)
- `1` = FAIL (findings detected)
- `2` = INTERNAL ERROR (tool failed, not the target)

---

## Active Tools (Implemented)

| Tool | Purpose | Authority | Inputs | Outputs | Consumers | Migration Status |
|------|---------|-----------|--------|---------|-----------|-----------------|
| `verify_versions.py` | Version consistency across README, __version__, contracts | Quality Gate 5 | `README.md`, `src/jarvis/version.py`, `docs/contracts/` | `report.json`, `report.md` | `verify_all.py`, CI | New |
| `verify_registry.py` | Registry integrity checks (Capability Register, Tool Registry, Manifest) | Quality Gate 3 | `docs/planning/Capability_Register.md`, `tools/quality/Tool_Registry.md`, `tools/manifest.json` | `report.json`, `report.md` | `verify_all.py`, CI | Promoted from `eq0013_registry_validator.py` |
| `verify_contracts.py` | Contract presence verification and source file mapping | Quality Gate 2 | `docs/contracts/`, `src/` | `report.json`, `report.md` | `verify_all.py`, CI | Extracted from `eq0012_spike6_contract_verification.py` + `eq0012_spike3_contract_invariants.py` |
| `verify_imports.py` | Import boundary enforcement (production code must not depend on docs/, tools/, data/reports/) | Quality Gate 1 | `src/` | `report.json`, `report.md` | `verify_all.py`, CI | New |
| `verify_tests.py` | Test suite structural audit (file count, function count, skipped tests) | Quality Gate 1 | `tests/`, `pytest.ini` | `report.json`, `report.md` | `verify_all.py`, CI | Extracted from `eq0012_spike4_verification_audit.py` |
| `verify_documentation.py` | Documentation synchronization audit for key engineering documents | Quality Gate 5 | `README.md`, `docs/knowledge/00_Knowledge_Index.md`, `docs/26_Implementation_Status.md`, `AGENTS.md` | `report.json`, `report.md` | `verify_all.py`, CI | Extracted from `eq0012_spike5_verification_audit.py` |
| `verify_governance.py` | Comprehensive repository governance validation (Engineering Register, EQ packages, authority documents, evidence structure, tool placement) | Quality Gate 2 | `docs/engineering/Engineering_Register.md`, `docs/engineering/questions/`, `docs/engineering/evidence/`, `tools/` | `report.json`, `report.md` | `verify_all.py`, CI, Pull Request validation | New |
| `verify_links.py` | Automated markdown link validation (internal references, relative paths, cross-document links) | Quality Gate 1 | `docs/engineering/Engineering_Register.md`, `docs/engineering/evidence/`, `README.md` | `report.json`, `report.md` | `verify_all.py`, CI, Pull Request validation | New |
| `verify_evidence.py` | Engineering Question evidence validation (authority documents, evidence packages, completeness, orphaned/duplicate detection) | Quality Gate 2 | `docs/engineering/Engineering_Register.md`, `docs/engineering/questions/`, `docs/engineering/evidence/` | `report.json`, `report.md` | `verify_all.py`, CI, Pull Request validation | New |
| `verify_tools.py` | Tool classification and placement validation (reusable vs historical evidence with architectural justification) | Quality Gate 3 | `tools/quality/`, `tools/manifest.json`, `tools/quality/Tool_Registry.md` | `report.json`, `report.md` | `verify_all.py`, CI, Pull Request validation | New |
| `verify_register.py` | Engineering Register validation (unique EQ numbers, authority document existence, evidence package existence, valid paths, status values) | Quality Gate 3 | `docs/engineering/Engineering_Register.md`, `docs/engineering/questions/`, `docs/engineering/evidence/` | `report.json`, `report.md` | `verify_all.py`, CI, Pull Request validation | New |
| `verify_all.py` | Orchestrator — reads manifest.json, executes all tools + pytest, produces consolidated report | Quality Gate 5 | `tools/manifest.json`, all verify_*.py tools | `data/reports/Repository_Quality_Report.json`, `data/reports/Repository_Quality_Report.md` | CI, Release Candidate check | New |

## Planned Tools (Not Yet Implemented)

| Tool | Purpose | Authority | Planned Status |
|------|---------|-----------|----------------|
| `verify_determinism.py` | Determinism contract verification | Quality Gate 1 | Planned — no implementation exists |
| `verify_traceability.py` | Traceability matrix (EQ→spike→code→test→doc) | Quality Gate 2 | Planned — no implementation exists |
| `verify_capabilities.py` | Capability Register vs. implementation audit | Quality Gate 5 | Planned — no implementation exists |
| `verify_repository.py` | Cross-cutting repository consistency (directory structure, naming conventions, drift) | Quality Gate 5 | Planned — no implementation exists |

---

## Historical Evidence Tools (Unchanged)

The following tools remain at `tools/` root as immutable engineering evidence. They are NOT migrated to `tools/quality/`.

| Tool | EQ/Spike | Status |
|------|----------|--------|
| `eq0010_spike1_direct_field_observation.py` through `eq0010_spike5_domain_reconciliation.py` | EQ-0010 | Historical evidence |
| `eq0011_spike1_domain_vocabulary_discovery.py` through `eq0011_spike5_semantic_capability_disposition.py` | EQ-0011 | Historical evidence |
| `eq0012_spike1_current_evidence_inventory.py` through `eq0012_spike6_contract_verification.py` | EQ-0012 | Historical evidence |
| `eq0013_spike1_validation_capability_discovery.py` through `eq0013_spike4_verification_tool.py` | EQ-0013 | Historical evidence |
| `eq0014_spike1_parser_regression_investigation.py` + `eq0014_spike2_production_verification.py` | EQ-0014 | Historical evidence |
| `eq0015_spike1_production_behavior.py` through `eq0015_spike4_evidence_classification.py` | EQ-0015 | Historical evidence |

---

## Replacement History

| Old Tool | Replaced By | Date | Reason |
|----------|-------------|------|--------|
| `eq0013_registry_validator.py` | `tools/quality/verify_registry.py` | 2026-07-16 | Promoted reusable logic |
| `eq0012_spike6_contract_verification.py` + `eq0012_spike3_contract_invariants.py` | `tools/quality/verify_contracts.py` | 2026-07-16 | Logic extracted, originals preserved as historical |
| `eq0012_spike4_verification_audit.py` | `tools/quality/verify_tests.py` | 2026-07-16 | Logic extracted, original preserved as historical |
| `eq0012_spike5_verification_audit.py` | `tools/quality/verify_documentation.py` | 2026-07-16 | Logic extracted, original preserved as historical |