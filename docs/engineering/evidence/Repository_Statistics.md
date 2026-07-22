# Repository Statistics — Foundation Freeze

**Generated**: 2026-07-22
**Part of**: Repository Foundation Freeze & Knowledge Consolidation

---

## Document Statistics

| Category | Count |
|---|---|
| Architecture Decision Records (ADRs) | 26 (all Accepted) |
| Engineering Questions (EQs) | 6 |
| Frozen EQs (Gate 3) | 4 (EQ-0010 through EQ-0013) |
| Completed EQs | 2 (EQ-0014, EQ-0015) |
| Spike Investigations | 30 total (across all EQs) |
| Evidence Reports (spike) | 30 |
| Evidence Reports (milestones) | 5 (M9, M10×2, Foundation Freeze, Verification Summary) |
| Frozen Public Contracts | 2 |
| Capability Matrices | 3 |

## Documentation Statistics

| Area | Count |
|---|---|
| Source of truth architecture docs (00-05) | 6 |
| Speculative framework docs (06-25) | 20 |
| Active status tracker (26) | 1 |
| Domain knowledge files | 13 |
| Planning documents | 5 |
| Design specifications | 3 |
| Implementation documents | 2 |
| Reference documents | 10 |
| Retrospectives | 4 |
| Diagrams | 7 |
| Ontology core concept files | 11 |
| Ontology observation files | 9 |
| Knowledge base documents | 16 (11 core + 5 appendices) |
| Engineering governance docs | 8 |
| Engineering questions | 6 |
| Engineering evidence reports | 35+ |
| Contract files | 2 |
| Supporting docs (ROOT) | 7 (AI_COLLABORATION, CONTRIBUTING, JARVIS_SPEC, LANGUAGE, etc.) |

**Total documentation files**: ~140+

## Quality Pipeline

| Tool | File | Lines |
|---|---|---|
| verify_all.py | tools/quality/verify_all.py | 127 |
| verify_versions.py | tools/quality/verify_versions.py | 105 |
| verify_registry.py | tools/quality/verify_registry.py | 129 |
| verify_contracts.py | tools/quality/verify_contracts.py | 99 |
| verify_imports.py | tools/quality/verify_imports.py | 91 |
| verify_tests.py | tools/quality/verify_tests.py | 131 |
| verify_documentation.py | tools/quality/verify_documentation.py | 128 |
| **Total** | | **810 lines** |

## Production Code

| Module | Files | Approx. Lines |
|---|---|---|
| Application (app.py + application.py) | 2 | ~50 |
| Configuration (configuration.py) | 2 | ~50 |
| Kernel (kernel.py) | 2 | ~40 |
| Domain models (12 files) | 12 | ~300 |
| Validation Engine (engine.py + data/) | 3 | ~200 |
| BOQ Parser (4 files) | 5 | ~800 |
| Observation models | 2 | ~150 |
| Services (logging_service.py) | 2 | ~30 |
| Other | 5 | ~80 |
| **Total** | **~35** | **~1,700** |

## Tests

| Category | Files | Tests |
|---|---|---|
| Parser tests | 6 | ~90 |
| Validation tests | 1 | ~30 |
| Lifecycle tests | 1 | ~20 |
| Reference evidence | 1 | ~10 |
| **Total** | **9** | **158** (150 pass, 8 skip) |

## Spike Tools

| EQ | Spike Count | Tool Files |
|---|---|---|
| EQ-0010 | 5 | eq0010_spike1-5*.py |
| EQ-0011 | 5 | eq0011_spike1-5*.py |
| EQ-0012 | 6 | eq0012_spike1-6*.py |
| EQ-0013 | 5 | eq0013_spike1-4*.py + registry_validator.py |
| EQ-0014 | 2 | eq0014_spike1-2*.py |
| EQ-0015 | 4 | eq0015_spike1-4*.py |
| Utility | 7 | build_docs.py, generate_*.py, boq_row_analysis.py, workbook_inspector.py, context_discovery_spike.py, register_fixture.py |
| **Total** | 34 | **34 spike tools** |

## Spike Data Reports

| EQ | Data Files |
|---|---|
| EQ-0011 | 5 (eq0011_spike1-5_results.json) |
| EQ-0012 | 10 (eq0012_spike1-6 various) |
| EQ-0013 | 9 (eq0013_spike1-4 various) |
| EQ-0014 | 2 (eq0014_spike1-2.json) |
| EQ-0015 | 4 (eq0015_spike1-4.json) |
| Other | 1 (Repository_Quality_Report.md) |
| **Total** | **31 data reports** |

## Test Fixtures

| Category | Files |
|---|---|
| BOQ Excel workbooks | 5 (.xlsx files) |
| Fixture metadata/config | 2 (.py + .json) |
| Fixture README | 2 |

## Empty Scaffolding

| Category | Directories |
|---|---|
| Empty src/jarvis subdirs | 21 |
| Empty data/ subdirs | 7 |
| Empty third_party/ subdirs | 4 |
| Empty configs/ + scripts/ + workflows/* | 6 |
| Empty docs/ subdirs | 3 |
| **Total empty scaffold dirs** | **41** |

## Repository Totals

| Metric | Count |
|---|---|
| Total committed files | ~280+ |
| Total directories active code | 56 |
| Empty scaffold directories | 41 |
| Production Python files | ~35 |
| Test Python files | ~9 |
| Quality verification tools | 8 |
| Spike tools | 34 |
| Documentation files | ~140+ |
| ADRs | 26 |
| Frozen EQs | 6 |
| Frozen contracts | 2 |
| Data reports | 31 |
| Lines of production code | ~1,700 |
| Lines of test code | ~1,400 |
| Lines of quality tools | 810 |
| Pytest results | 150 passed, 8 skipped |
| verify_all.py | PASS |
| Version | 0.0.1-alpha |
| Latest commit | 81c3944d |
| Archived files | 4 |

---

## Documentation Health

| Metric | Value |
|---|---|
| Project Owner Verified documents | 3.6% |
| Evidence-Backed documents | 25.0% |
| Implementation-Backed documents | 2.1% |
| AI-Generated, Pending review | 46.4% |
| Speculative (planned, not implemented) | 12.9% |
| Obsolete | 2.9% |
| Unknown | 7.1% |
| **Trustworthy baseline** | **~31%** |

---

## Archive Statistics

| Category | Count |
|---|---|
| Files archived | 4 |
| Historical Evidence | 3 reports |
| Archive (superseded) | 1 release note |
| Empty directories (staying in place) | 41 |
| Archive reserve directories | 5 |

---

**Generated**: 2026-07-22 | **Part of**: Repository Foundation Freeze