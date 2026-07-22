# Engineering Fixtures

**Status:** Living Reference  
**Category:** Engineering Practice  
**Version:** 1.0

---

# Purpose

This document defines how engineering fixtures are managed within the Jarvis repository.

Engineering fixtures are repository assets used to answer Engineering Questions, validate deterministic implementations, reproduce Engineering Spikes, and support regression testing.

This document describes repository engineering practice only.

It is **not** an architectural specification.

---

# Definition

An Engineering Fixture is a reproducible input used to answer an Engineering Question.

Examples include:

- CostX workbook exports
- Cubit exports
- PDF drawing sets
- CSV datasets
- JSON payloads
- Images
- OCR samples

A fixture is engineering evidence.

It is not necessarily "correct" from a business or domain perspective.

---

# Engineering Principle

Engineering fixtures preserve the evidence that produced an engineering conclusion.

A fixture records what was observed.

It does not represent the ideal state of the source data.

---

# Fixture Lifecycle

```
Real-world source
        │
        ▼
Engineering Fixture
        │
        ▼
Engineering Spike
        │
        ▼
Engineering Evidence
        │
        ▼
Engineering Question
        │
        ▼
ADR / Production
```

Once a fixture becomes part of accepted engineering evidence, its role changes.

It becomes a reproducible evidence baseline.

---

# Fixture Immutability

A fixture SHALL be treated as immutable after it has been cited by any accepted engineering artifact, including:

- Engineering Spikes
- Engineering Questions
- ADRs
- Normative design documents
- Published engineering reports

Immutability preserves reproducibility.

Future engineers must be able to reproduce the same engineering evidence from the same repository state.

---

# Engineering Evidence

The purpose of a fixture is to answer questions such as:

> "Can this workbook be parsed deterministically?"

It is **not** intended to answer:

> "Is this workbook correct?"

Domain correctness and engineering reproducibility are independent concerns.

---

# Domain Errors

Engineering review may later identify mistakes within a fixture.

Examples include:

- incorrect quantities
- incorrect signs
- duplicated rows
- spelling mistakes
- invalid metadata
- missing information

Discovering a domain error does **not** invalidate the engineering evidence previously produced from that fixture.

The Engineering Question should determine whether the observed data can be processed correctly, not whether the underlying business document is correct.

---

# Correcting Fixtures

When corrected data is required:

1. Preserve the original fixture unchanged.
2. Create a new fixture containing the corrected data.
3. Document why the new fixture exists.
4. Reference the Engineering Question that required it.

The original fixture remains the historical engineering baseline.

---

# Regression Fixtures

Some fixtures intentionally contain known defects.

These fixtures are valuable because they verify deterministic detection of those conditions.

Examples:

- incorrect OMISSION sign
- duplicated BOQ row
- malformed workbook
- unsupported worksheet structure

Such fixtures SHALL remain unchanged.

---

# Relationship to Engineering Questions

Engineering Questions define:

- why a fixture exists
- which fixture is authoritative
- what behavior is expected

Fixtures do not define engineering intent.

Engineering Questions do.

---

# Repository History

Engineering evidence shall remain reproducible.

Repository history must not be rewritten to improve historical results.

If improved fixtures become available, they shall be added alongside historical fixtures rather than replacing them.

---

# Example

Engineering Spike #1 analysed:

```
tests/fixtures/costx/full_boq.xlsx
```

Subsequent QS review determined that seven OMISSION rows contained data-entry errors.

The fixture remains unchanged because:

- Spike #1
- EQ-0002
- EQ-0006
- ADR-0025

all reference observations made against that specific workbook.

If a corrected workbook is later required, it should be introduced as a separate fixture (for example, `full_boq_corrected.xlsx`) under a new Engineering Question or Engineering Spike.

---

# Summary

Engineering fixtures are historical engineering evidence.

They preserve observations.

They are not continuously corrected representations of business truth.

When business truth changes, new fixtures are introduced.

The engineering evidence remains reproducible.