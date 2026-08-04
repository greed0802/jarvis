# Capability Metrics

Version: 1.0

---

## Approval Metadata

| Field | Value |
|-------|-------|
| **Status** | Accepted |
| **Owner** | Project Owner |
| **Effective** | 2026-07-22 |
| **Supersedes** | None |
| **Sprint Reference** | CB-0001 |

---

## Purpose

This document defines objectively measurable metrics for every Jarvis capability.

Metrics exist to:
- Assess readiness
- Detect regression
- Compare capabilities on shared criteria
- Avoid subjective descriptions of progress

Metrics are never "aspirational." Every metric defined here can be calculated programmatically from the repository's current state.

---

## Metric Categories

### 1. Capability Maturity

| Metric | Definition | Measurement |
|--------|------------|-------------|
| **Lifecycle State** | Current state of the capability in the Capability Register lifecycle | String: `Active`, `Frozen Sub-capability`, `Deferred`, `Historical`, etc. |
| **Classification** | Position in the strategic portfolio | String: `Strategic`, `Supporting`, `Deferred`, `Historical` |
| **Approval Date** | Date capability was approved by Project Owner | ISO 8601 date or `None` |
| **Last Increment Date** | Date of the most recent completed increment | ISO 8601 date or `None` |
| **State Duration** | Days in current lifecycle state | days, calculated from last state change date |

### 2. Test Coverage and Regression

| Metric | Definition | Measurement |
|--------|------------|-------------|
| **Production Test Count** | Number of tests that exercise production code for this capability | integer count |
| **Test Result Status** | Current pass/fail/skip counts | `(passes, fails, skips)` tuple |
| **Regression Delta** | New tests introduced in the most recent increment | integer count (tests after increment minus tests before increment) |
| **Fixture Count** | Number of fixture files consumed by tests | integer count |
| **Fixture Integrity** | SHA-256 digest of authoritative fixture matches registered digest | boolean (verified/not verified) |

### 3. Evidence Completeness

| Metric | Definition | Measurement |
|--------|------------|-------------|
| **Engineering Questions Open** | Number of open EQs within capability scope | integer count |
| **Engineering Questions Answered** | Number off answered/frozen EQs within scope | integer count |
| **Evidence Reports Frozen** | Number of evidence reports (spike reports) approved | integer count |
| **Rule Provenance Coverage** | Fraction of capability rules that trace to ENGINEERING Evidence or Domain Standard | ratio (`traced / total`) |
| **Evidence Gaps** | Number of acceptance criteria that lack evidence traceability | integer count |

### 4. Contract Stability

| Metric | Definition | Measurement |
|--------|------------|-------------|
| **Public Contract Version** | Version string of the Frozen Contract (if any) | semver (e.g. `1.0.0`) or `None` |
| **Contract Status** | Lifecycle state of the public contract | `Candidate` / `Frozen` |
| **Contract Invariants Count** | Number of structural + structual invariants verified | integer (e.g. 43 + 34 = 77) |
| **Contract Verification Rate** | % of contract elements verified via automated tooling | percentage (e.g. 63/63 = 100%) |
| **Consumer Count** | How many distinct consumers depend on this contract | integer count |

### 5. Determinism

| Metric | Definition | Measurement |
|--------|------------|-------------|
| **Deterministic Output** | Whether capability output is deterministic (same input same output) | binary (yes/no) or percentage across N runs |
| **Unique Output Count** | Number of unique outputs across N runs with identical inputs | integer: 1 =xic, */deterministic |
| **Timestamps** | If timestamps are present, are they UTC and isolated from semantic | boolean (UTC and isolated `True`/`False`)* |

### 6. Architecture Impact

| Metric | Definition | Measurement |
|--------|------------|-------------|
| **New Engines Introduced** | Did this capability introduce a new engine? | integer count |
| **New ADRs Required** | Did this capability require a new Architectural Decision Record? | integer count |
| **Existing Modules Modified** | Number of pre-existing production modules modified | integer count |
| **Pure Function Count** | How many production functions are pure (stateless, deterministic)? | integer count |

---

## Current Metrics (2026-07-22)

### BOQ Intelligence

| Metric | Value |
|--------|-------|
| Lifecycle State | Active |
| Classification | Strategic |
| Approval Date | 2026-07-13 |
| Last Increment Date | 2026-07-14 |
| Production Test Count | 73 |
| Test Result | (73, 0, 8) — 73 pass, 0 fail, 8 skipped (historical) |
| Regression Delta | +26 tests (from Increment 1) |
| Fixture Count | 1 primary fixture (`full_boq.xlsx`) |
| EQs Open | 0 (within current increment scope) |
| EQs Answered | 3 (EQ-0007, EQ-0010, EQ-0011) |
| EQs Supporting Contract | EQ-0012 (Frozen) |
| Evidence Reports Frozen | 6 (EQ-0012 Spikes 1-6) |
| Domain Rule Coverage | Partial (further domain rules needed) |
| Public Contract | v1.0.0 Frozen |
| Contract Invariants | 77 (43 structural + 34 semantic) |
| Contract Verification | 63/63 MATCH (100%) |
| Consumer Count | 1 (Validation Engine) |
| Deterministic Output | Verified |
| New Architecture | None |
| New ADRs Required | 0 |
| Existing Modules Modified | 0 |

### Validation Engine

| Metric | Value |
|--------|-------|
| Lifecycle State | Frozen Sub-capability |
| Classification | Supporting |
| Approval Date | 2026-07-15 |
| Last Increment Date | 2026-07-15 |
| Production Test Count | 8 smoke tests |
| Increment | (8, 0, 0) |
| EQs Answered | EQ-0013 (Frozen) |
| Evidence Reports | 4 (Spikes 1-4) |
| Public Contract | v1.0.0 Frozen |
| Contract Verification | 100% |
| Consumer Count | 1 (CheckMate pending) |
| Deterministic Output | Verified (3 runs, 1 unique) |
| New Architecture | Engine added |
| New ADRs Required | 0 |
| Existing Modules Modified | 0 |

### CheckMate

| Metric | Value |
|--------|-------|
| Lifecycle State | Deferred |
| Classification | Deferred |
| Approval Date | N/A |
| Last Increment Date | N/A |
| Production Test Count | 0 |
| EQs Open | 0 |
| Public Contract | None |
| Consumer Count | 0 |
| Reason Deferred | Depends on BOQ Intelligence maturity + domain rule catalog |

### Formatter

| Metric | Value |
|--------|-------|
| Lifecycle State | Deferred |
| Classification | Deferred |
| Approval Date | N/A |
| Last Increment Date | N/A |
| Production Test Count | 0 |
| EQs Open | 0 |
| Public Contract | None |
| Consumer Count | 0 |
| Reason Deferred | Depends on BOQ Intelligence trusted validation |

### Cubit Parser

| Metric | Value |
|--------|-------|
| Lifecycle State | Deferred |
| Classification | Deferred |
| Approval Date | N/A |
| Fixture Count | 0 |
| EQs Open | 0 |
| Reason Deferred | Awaiting Cubit export fixtures |

### PDF Parser

| Metric | Value |
|--------|-------|
| Lifecycle State | Deferred |
| Classification | Deferred |
| Approval Date | N/A |
| Fixture Count | 0 |
| Reason Deferred | Insufficient evidence; fundamentally different extraction approach needed |

### AI-Assisted Estimation

| Metric | Value |
|--------|-------|
| Lifecycle State | Deferred |
| Classification | Deferred |
| Approval Date | N/A |
| Reason Deferred | Long-term strategic; multiple prerequisite foundations missing |

---

## Metric Computation

All metrics are present at the user-level in repository state:

- Test counts: parsed from `pytest --collect-only` or test directory file counting
- Fixture integrity: calculated by SHA-256 comparison between registered and actual fixture files
- EQS counts: parsed from `docs/reference/Engineering_Questions.md` or the `EQ_*` file list
- Contract status: parsed from Contract `.md` front matter or verification tool output
- Determinism: verified by the capability's own verification tool chain (e.g. `tools/eq0012_spike6_contract_verification.py`)
- Module changes: `git diff` over production files

No metric requires subjective human assessment.

---

## Metrics Dashboard (Notional)

Once an automated metrics dashboard exists, it would display:

| Capability | State | Tests | EQs | Contract | Consumers | Deterministic |
|------------|------:|:------:|:---:|:--------:|:---------:|:------------:|
| BOQ Intelligence | Active | 73 pass | 3 answered | v1.0.0 Frozen | 1 | Verified |
| Validation Engine | Frozen | 8 pass | 1 answered | v1.0.0 Frozen | 1 | Verified |
| CheckMate | Deferred | 0 | 0 | — | 0 | — |
| Formatter | Deferred | 0 | 0 | — | 0 | — |
| Cubit Parser | Deferred | 0 | 0 | — | 0 | — |
| PDF Parser | Deferred | 0 | 0 | — | 0 | — |
| AI-Assisted Estimation | Deferred | 0 | 0 | — | 0 | — |

---

## Metrics Governance

- Metrics are reported, not interpreted.
- A drop in test coverage is an observation, not a conclusion.
- An increase in EQS is a signal, not a crisis.
- Metrics inform human decisions; they do not replace them.

---

## Document History

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-07-22 | Initial metric framework and current values for all 8 capabilities. Sprint CB-0001. |