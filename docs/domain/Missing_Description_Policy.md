# Missing Description Policy

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

This document defines when a BOQ item description is mandatory, when omissions are permitted, and how detection should behave.

This policy governs the D-002 domain rule (Missing Description Detection).

---

## When a Description Is Mandatory

A description is **mandatory** for:

| Row Type | Mandatory? | Rationale |
|----------|:----------:|-----------|
| **Item** | ✅ Yes | Every priced or measured item must have a description to identify its scope. |
| **Head** | ✅ Yes | Headers describe the section or category of work. A header without a description is unusable. |
| **Note** | ❌ No | Notes may exist without a description (e.g., purely numeric annotations). |
| **Section** | ❌ No | Section boundaries may be blank. The section context is captured via the `section` field, not the description. |
| **Other** | ❌ No | Unclassified rows may lack descriptions. These should be flagged for inspection but not as missing description errors. |

---

## Exceptions

The following are **not** considered missing descriptions:

| Exception | Rationale |
|-----------|-----------|
| **OMISSION/ADDITION revision headers** | Standard CostX BOQ entries for revision context may have blank descriptions in the Header row. |
| **Section continuation** | A blank description on a row that follows a fully described header is not problematic. The header's description carries scope. |
| **Zero-quantity provisional sums** | A provisional sum item with `description = None` and `quantity = 0.0` is an edge case. Flag as INFO, not WARNING. |

---

## Detection Rules

| Rule | Behavior |
|------|----------|
| **Missing description on Item** | Flag as WARNING. Each Item row should have a description. |
| **Missing description on Head** | Flag as INFO. Headers ideally have descriptions, but are not critical. |
| **Empty string vs. None** | Both `description = None` and `description = ""` (empty string) are treated as missing. |
| **Whitespace-only** | `description = "   "` is treated as missing — stripped value is empty. |
| **Description too short** | Not in scope. Single-character descriptions are valid if meaningful. |

---

## Examples

### Missing description (should be detected)

```
row_type: "Item", code: "CONC-001", description: None, quantity: 150.0
```
→ Missing description. Item with quantity but no description.

```
row_type: "Item", code: "CONC-001", description: "", quantity: 150.0
```
→ Missing description. Empty string.

```
row_type: "Item", code: "CONC-001", description: "   ", quantity: 150.0
```
→ Missing description. Whitespace-only.

```
row_type: "Head", description: None, uom: "Head1"
```
→ Missing description (INFO). Header should have a description.

### Not a missing description

```
row_type: "Item", code: "CONC-001", description: "RC Column 400x400", quantity: 150.0
```
→ Not missing. Description is present and meaningful.

```
row_type: "Note", description: None
```
→ Not missing. Notes are exempt.

```
row_type: "Item", code: "PROV-001", description: None, quantity: 0.0
```
→ Not missing (INFO only). Zero-quantity provisional sum edge case.

---

## Authority

| Field | Value |
|-------|-------|
| **Owner** | Project Owner (QS Authority) |
| **Authority Source** | `docs/domain/02_BOQ_Structure.md` — BOQ hierarchy rules |
| **Effective** | 2026-07-22 |
| **Rule ID** | D-002 |
| **Rule Status** | APPROVED |

---

## Document History

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-07-22 | Initial missing description policy. Sprint CB-0003. |