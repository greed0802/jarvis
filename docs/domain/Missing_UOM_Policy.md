# Missing UOM Policy

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

This document defines when a BOQ item UOM (Unit of Measure) is mandatory, when omissions are permitted, and how detection should behave.

This policy governs the D-003 domain rule (Missing UOM Detection).

---

## When UOM Is Mandatory

A UOM is **mandatory** for:

| Row Type | Mandatory? | Rationale |
|----------|:----------:|-----------|
| **Item** | ✅ Yes | Every priced or measured item requires a UOM to interpret its quantity. Without a UOM, the quantity is meaningless. |
| **Head** | ❌ No | Headers have UOMs like "Head1", "Head2" etc. per the CostX export format. These are structural markers, not measurement units. They are populated by the parser. A missing header UOM would be an extraction error, not a domain rule. |
| **Note** | ❌ No | Notes have no quantity and do not need UOMs. |
| **Section** | ❌ No | Section rows have no quantity. |
| **Other** | ❌ No | Unclassified rows. |

---

## Permitted Omissions

The following are **not** considered missing UOMs:

| Exception | Rationale |
|-----------|-----------|
| **Zero-quantity items** | An Item with `quantity == 0.0` and `uom == None` is a provisional sum or placeholder. Flag as INFO, not WARNING. |
| **Items with only description** | An Item with `description` set, `quantity == None`, and `uom == None` may be a descriptive annotation. Flag as INFO. |
| **Header/Note/Section/Other** | See "When UOM Is Mandatory" above. |

---

## Detection Rules

| Rule | Behavior |
|------|----------|
| **Missing UOM on Item with quantity** | Flag as WARNING. Item has a measured quantity but no UOM. This is a data quality issue. |
| **Missing UOM on Item with zero quantity** | Flag as INFO. Provisional sum or placeholder. |
| **UOM present but contains classification marker** | Not an error. UOMs like "Head1", "Head2" are classification markers, not measurement units. These are valid on Header rows. |
| **Empty string vs. None** | Both `uom = None` and `uom = ""` (empty string) are treated as missing. |
| **Whitespace-only** | `uom = "   "` is treated as missing — stripped value is empty. |

---

## Examples

### Missing UOM (should be detected)

```
row_type: "Item", code: "CONC-001", quantity: 150.0, uom: None
```
→ Missing UOM. Item with quantity but no unit.

```
row_type: "Item", code: "CONC-001", quantity: 150.0, uom: ""
```
→ Missing UOM. Empty string.

```
row_type: "Item", code: "CONC-001", quantity: 150.0, uom: "   "
```
→ Missing UOM. Whitespace-only.

### Not a missing UOM

```
row_type: "Item", code: "CONC-001", quantity: 150.0, uom: "m3"
```
→ Not missing. UOM is present and valid.

```
row_type: "Item", code: "PROV-001", quantity: 0.0, uom: None
```
→ Not missing (INFO only). Zero-quantity provisional sum.

```
row_type: "Head", uom: "Head1"
```
→ Not missing. Header UOM is a classification marker, not a measurement unit.

```
row_type: "Note", quantity: None, uom: None
```
→ Not missing. Notes are exempt.

---

## Authority

| Field | Value |
|-------|-------|
| **Owner** | Project Owner (QS Authority) |
| **Authority Source** | `docs/domain/02_BOQ_Structure.md` — BOQ hierarchy rules |
| **Effective** | 2026-07-22 |
| **Rule ID** | D-003 |
| **Rule Status** | APPROVED |

---

## Document History

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-07-22 | Initial missing UOM policy. Sprint CB-0003. |