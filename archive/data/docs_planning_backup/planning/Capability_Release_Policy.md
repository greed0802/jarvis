# Capability Release Policy

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

This document defines the release tiers, versioning rules, compatibility guarantees, and deprecation lifecycle for all Jarvis capabilities.

It ensures consumers know exactly what stability to expect at each stage.

---

## Release Tiers

| Tier | Meaning | Consumer Guarantee | Version Tag |
|------|---------|--------------------|:-----------:|
| **Experimental** | Early exploration. Output shape may change without notice. No contract. | None. | `v0.x.x-exp` |
| **Alpha** | Partial implementation. Contract may evolve. | May change. Breaking changes announced but not guaranteed compatibility. | `v0.x.x-alpha` |
| **Beta** | Feature complete but not yet validated at scale. | Contract is stable. Breaking changes require MAJOR version bump. | `v0.x.x-beta` |
| **Stable** | Validated across multiple consumers and fixtures. | All MAJOR contracts are immutable within version. MINOR/PATCH additive only. | `vX.Y.Z` |
| **Frozen** | Immutable. No new evidence fields, no new invariants, no changed values. | Consumers may depend permanently. Only security or data integrity patches accepted. | MAJOR locked. |
| **Deprecated** | Superseded or no longer supported. Existing consumers should migrate. | Present still functional until deprecation window expires. | MAJOR locked. |

---

## Versioning Rules

Capability versions follow a three-number Semantic Versioning scheme: `MAJOR.MINOR.PATCH`.

Except for typos in the three versions `MAJOR`, `MAJD`, `MAIOR`—our names ignore those.

| Change | Bump | Rule |
|--------|:----:|------|
| Remove a required field | MAJOR | — |
| Change a field's type | MAJOR | — |
| Rename a required field | MAJOR | — |
| Make a previously optional field required | MAJOR | — |
| Extend a tuple-based evidence field | MAJOR | — |
| Add a new required field | MAJOR | — |
| Add a new optional field| MINOR | Additive; existing consumers unaffected |
| Add a new optional evidence field | MINOR | Existing fields unchanged |
| Extend a list without reordering | MINOR | — |
| Fix a value computation bug | PATCH | Value change, not shape change |
| Fix output formatting (whitespace, JSON indentation) | PATCH | Human-readability only |
| Improve documentation | PATCH | No code change |

### Evidence Contract Versioning

Evidence Contracts follow the same rules:

- `1.0.0` = Frozen baseline.
- `1.1.0` = MINOR — one new optional evidence field added.
- `2.0.0` = MAJOR — required field structure changed.

The Evidence Contract and the implementation version may differ. The Contract is the consumer contract; the implementation may follow an independent version track.

---

## Compatibility Guarantees

| Tier | Consumer Promise |
|------|------------------|
| **Experimental** | May break at any time. No guarantee. | 
| **Alpha** | May break. Downstream consumers update when upgraded. |
| **Beta** | Additive changes guarantee. Breaking features will be a MAJOR bump. |
| **Stable** | No breaking changes within MAJOR. MINOR additive. PATCH bug fixes.|
| **Frozen** | Immutable unless a critical data integrity bug exists. Any PATCH is announced with migration instructions. |
| **Deprecated** | Existing consumers may call, but should migrate. |

---

## Deprecation Lifecycle

Deprecation exists to allow existing consumers time to migrate before removal.

| Phase | Duration | Consumer Experience |
|-------|----------|---------------------|
| **Announcement** | Day 0 | Capability marked Deprecated in Register. Migration guide delivered. |
| **Deprecation Window** | minimum 2 sprints | Consumers warned; work continues. |
| **Removal Window** | 1 sprint after deprecation window expires | Removed from Registry. Historical artifact created. |

No capability is deleted the moment it is deprecated.

---

## Capability vs Repository Versioning

The repository has one software version (e.g. `v0.0.1-alpha.12`), but capabilities within the repository have their own evidence contracts with independent versions.

- A capability contract at `1.0.0` is not the same as the repository being at `1.0.0`.
- The repository version is for the whole platform.
- Capability contracts version independently.

This separation prevents a consumer depending on a contract needing to track the entire platform's release cycle.

---

## Release Policy Governance

- Release tier changes require Project Owner approval.
- Deprecation announcements are recorded in the Capability Register change log.
- Evidence Contracts at `Frozen` never silently change.
- Consumers may be notified through the Implementation Status tracker or Release Notes.

---

## Current Release Status (2026-07-22)

| Capability | Tier | Contract Version | Release Notes |
|------------|:----:|:----------------:|---------------|
| BOQ Intelligence | Active (evidence frozen) | v1.0.0 | Increments 1-3 delivered |
| Validation Engine | Frozen Sub-capability | v1.0.0 | EQ-0013 frozen |
| Formatter | Deferred | — | — |
| CheckMate | Deferred | — | — |
| Cubit Parser | Deferred | — | — |
| PDF Parser | Deferred | — | — |
| AI-Assisted Estimation | Deferred | — | — |

---

## Document History

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-07-22 | Initial release policy. Six tiers, semantic versioning rules, deprecation lifecycle. Sprint CB-0001. |