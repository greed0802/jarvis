# Duplicate Code Policy

Version: 1.0

---

## Approval Metadata

| Field | Value |
|-------|-------|
| **Status** | Approved |
| **Owner** | Project Owner (QS Authority) |
| **Effective** | 2026-07-22 |
| **Supersedes** | None |
| **Sprint Reference** | CB-0003 |

---

## Purpose

This document defines what constitutes a duplicate BOQ item code, when duplicate codes are permitted, and how detection should behave.

This policy governs the D-001 domain rule (Duplicate Item Code Detection).

---

## What Constitutes a Duplicate

A duplicate is defined as:

> Two or more BOQ items share the same `item_code` value within a single BOQ (single workbook extraction).

This is a per-BOQ comparison. Cross-BOQ duplicate detection is not in scope.

### Match Rules

- Comparison is exact, case-sensitive string matching on the `item_code` field.
- Leading and trailing whitespace is stripped before comparison.
- A `null` / `None` code is not a duplicate — it is a missing code (handled by Missing Description / UOM rules).
- Code `"A-001"` and code `"A-001 "` (trailing space) match after stripping.
- Code `"A-001"` and code `"a-001"` do NOT match (case-sensitive).

---

## Exceptions

The following are **not** considered duplicates:

| Exception | Rationale |
|-----------|-----------|
| **OMISSION/ADDITION duplication** | A code appearing in both OMISSION and ADDITION sections is intentional. The same item appears in both revision contexts. |
| **Section-specific codes** | Codes that include a section prefix and appear across different sections are not duplicates if the section context differs. |
| **Zero-quantity placeholders** | Items with `quantity == 0.0` that share a code with a non-zero item are flagged as potential duplicates but may be legitimate (e.g., provisional sums). |
| **Duplicate over OMISSION/ADDITION only** | See first exception. OMISSION and ADDITION codes are distinct contexts and may legally overlap. |

---

## Allowed Duplicates

The only permitted duplicate scenario is:

1. The same code appears in both an OMISSION section and an ADDITION section.
2. The items have opposite sign quantities (negative in OMISSION, positive in ADDITION).
3. The descriptions match within case-insensitive comparison.

This is standard CostX BOQ practice for revision items.

---

## Detection Scope

| Dimension | Scope |
|-----------|-------|
| **Data source** | Single `list[BOQRow]` from a single `extract_boq()` call |
| **Field** | `item_code` (string) |
| **Item types** | Only `Item`-classified rows |
| **Excluded types** | `Head`, `Note`, `Section`, `Other` |

---

## Examples

### Duplicate (should be detected)

```
item_code: "CONC-001", section: "ADDITION", quantity: 150.0
item_code: "CONC-001", section: "ADDITION", quantity: 150.0
```
→ Duplicate. Same code, same section.

### Not a duplicate (OMISSION/ADDITION exception)

```
item_code: "CONC-001", section: "OMISSION", quantity: -150.0
item_code: "CONC-001", section: "ADDITION", quantity: 150.0
```
→ Not a duplicate. OMISSION/ADDITION exception applies.

### Not a duplicate (missing code)

```
item_code: null, description: "General allowance"
item_code: null, description: "Another allowance"
```
→ Not a duplicate. `null` codes are not compared.

---

## Authority

| Field | Value |
|-------|-------|
| **Owner** | Project Owner (QS Authority) |
| **Authority Source** | `docs/domain/02_BOQ_Structure.md` — BOQ hierarchy rules |
| **Effective** | 2026-07-22 |
| **Rule ID** | D-001 |
| **Rule Status** | APPROVED |

---

## Document History

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-07-22 | Initial duplicate code policy. Sprint CB-0003. |