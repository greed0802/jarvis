# Engineering Debt Register

**Purpose:** Persistent repository-wide engineering debt tracking.
**Created:** 2026-07-16 — Repository Hardening Sprint (Post EQ-0013)
**Governance:** Quality_Assurance_Constitution.md

---

## Active Debt Items

| Debt ID | Source Review | Description | Root Cause | Severity | Blocks Release | Planned Resolution | Status |
|---|---|---|---|---|---|---|---|
| HD-011 | Internal | Repository Drift Audit — root cause of all documentation, version, implementation, contract, knowledge, and test drift | No systematic drift detection exists; each drift item found independently by reviewers | High | **Yes** (Gate 4 mandatory) | Produce `Repository_Drift_Report.md` after all other debt resolved | Open |

---

## Resolved Debt Items

| Debt ID | Resolution | Date Resolved | Verification |
|---|---|---|---|
| HD-001 | Outcome B — Contract clarification: SE-FR-01 amended to exclude `execution_timestamp` from determinism guarantee. SI-FR-07 already consistent. No code change. | 2026-07-16 | Contract updated; determinism tests verify fields (not timestamp) |
| HD-002 | Outcome B — Contract clarification: SI-FR-01 and SI-FR-04 amended to specify field-level immutability. Deep immutability not required. | 2026-07-16 | Contract updated; field reassignment tests verify frozen=True blocks |
| HD-003 | Registry JSON embedded in package (`src/jarvis/engines/validation/data/rule_registry.json`). `_load_rule_registry()` uses `Path(__file__).parent / "data" / "rule_registry.json"` instead of hardcoded `data/reports/` path. | 2026-07-16 | Engine loads from package; smoke test passes (8/8); regression suite passes (34/34) |
| HD-004 | `finding_type` field added to all 22 rules in registry. `_classify_finding_type()` heuristic function removed. Engine reads `finding_type` directly from registry. | 2026-07-16 | HD-005 tests verify all 18 types match registry. Test verifies heuristic function absent. |
| HD-005 | Committed pytest suite created at `tests/validation/test_engine.py` with 34 tests covering determinism, all rules, rejected rules, optional evidence, contract compliance, edge cases, finding_type correctness, specific values. | 2026-07-16 | 34/34 PASS; existing tests unaffected (127 PASS, 20 pre-existing failures unrelated to validation) |
| HD-006 | Registry validator created at `tools/eq0013_registry_validator.py`. Validates schema, IDs, lifecycle, versions, categories, boundary classes, duplicates, required fields. Registry also fixed: 6 rules had invalid `boundary_class` or null `rule_version`. | 2026-07-16 | Validator passes: ✓ Registry is valid |
| HD-007 | `docs/knowledge/07_Capabilities.md` fixed: input corrected from `list[BOQRow]` to `BOQIntelligenceResult`, output corrected from `list[ValidationFinding]` to `ValidationFindings`, "7 finding fields, 7 severity levels, 4 rule tiers" corrected to "6 finding fields per finding, no severity levels, no rule tiers". | 2026-07-16 | Knowledge doc matches implementation and contract |
| HD-008 | Knowledge base drift: `docs/knowledge/07_Capabilities.md` Validation Engine entry synchronized with actual frozen contract and implementation. Capability Register already accurate. | 2026-07-16 | Drift eliminated |
| HD-009 | EQ-0013 question version reference corrected: `v0.0.1-alpha.10` → `v0.0.1-alpha.9` to match official RELEASE document. | 2026-07-16 | Version consistent across all repository references |
| HD-010 | Created `tools/eq0013_registry_validator.py`, `docs/engineering/Engineering_Verification_Pipeline.md`, `docs/engineering/capability_matrices/EQ_0013_Validation_Engine_Capability_Matrix.md`. Quality Gate 4 added to QA Constitution. | 2026-07-16 | All artifacts created and verified |

---

## Debt Severity Definitions

| Severity | Meaning |
|---|---|
| Trivial | Cosmetic; no functional or documentation impact |
| Low | Minor quality issue; does not block release |
| Medium | Significant quality issue; should resolve before next EQ |
| High | Blocks release or violates mandatory Quality Gates |

---

## Debt Lifecycle

```
Open → In Progress → Resolved → Verified → Closed
```

All debt items SHALL be tracked in this register until closed.

---

**End of Engineering Debt Register**