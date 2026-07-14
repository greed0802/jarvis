# Capability Matrix Template

**Purpose:** Documents what engineering capabilities are Observable, Derivable, Domain Dependent, Unsupported, or Unknown based on production evidence.

**Governance:** Follows Engineering_Governance.md v1.0

---

## Five-State Model

Engineering capabilities are classified into one of five states:

| State | Meaning |
|-------|---------|
| **Observable** | Directly available in data structure fields |
| **Derivable** | Deterministically computable from available data |
| **Domain Dependent** | Requires Domain Knowledge Layer validation |
| **Not Determinable** | Cannot be determined from current data structure |
| **Unknown** | Evidence not yet collected |

---

## Matrix Format

| Candidate Engineering Capability | Obs | Der | Domain | Not Det | Unk | Consumer(s) | Evidence |
|----------------------------------|-----|-----|--------|---------|-----|-------------|----------|
| Example: Row type | ✓ | | | | | All | Direct BOQRow field |
| Example: Empty header detection | | ✓ | | | | CheckMate | Sequence analysis spike |
| Example: Parent header | | ✓ | | | | Formatter | Row sequence spike |
| Example: Trade validation | | | ✓ | | | CheckMate | Domain doc 03 |
| Example: Engineering intent | | | | ✓ | | None | Requires human judgment |
| Example: Hierarchy depth | | | | | ✓ | Formatter | Pending investigation |

---

## Column Definitions

### Candidate Engineering Capability

The engineering capability being evaluated.

Use descriptive names that clearly identify what is being assessed.

### Obs (Observable)

✓ if the capability is directly available in data structure fields.

Evidence: Reference the data structure field or property.

### Der (Derivable)

✓ if the capability is deterministically computable from available data.

Evidence: Reference the spike or algorithm that demonstrated derivability.

### Domain (Domain Dependent)

✓ if the capability requires Domain Knowledge Layer validation.

Evidence: Reference the specific domain document (e.g., `docs/domain/03_Trade_Schedule.md`).

### Not Det (Not Determinable)

✓ if the capability cannot be determined from current data structure.

Evidence: Explanation of what information is missing or why current evidence is insufficient.

### Unk (Unknown)

✓ if evidence has not yet been collected.

This is the initial state for most capabilities before investigation begins.

### Consumer(s)

Which capability or system will consume this engineering capability.

Examples: BOQ Intelligence, CheckMate, Formatter, Reporting

### Evidence

Reference to the evidence supporting the classification.

Examples:
- "Direct BOQRow field"
- "Spike 2: Row sequence analysis"
- "Domain doc 02: BOQ Structure"
- "Investigation demonstrated missing information"
- "Pending Spike 3"

---

## Usage Guidelines

### 1. Initialize Matrix

Begin with most capabilities in "Unknown" state.

```markdown
| Capability | Obs | Der | Domain | Unsup | Unk | Consumer(s) | Evidence |
|------------|-----|-----|--------|-------|-----|-------------|----------|
| Capability A | | | | | ✓ | Consumer | Pending investigation |
| Capability B | | | | | ✓ | Consumer | Pending investigation |
```

### 2. Conduct Investigation Spikes

Execute small, focused investigations to collect production evidence.

### 3. Update Matrix After Each Spike

Move capabilities from "Unknown" to evidenced states.

Document:
- What changed (state transition)
- What evidence was collected
- Which spike produced the evidence
- When the update occurred

### 4. Preserve Timeline

Track the evolution of the matrix over time.

Example:
```markdown
## Update History

**2026-07-14 — Initial State**
- 10 capabilities initialized as Unknown

**2026-07-15 — After Spike 1: Direct Field Observation**
- Row type: Unknown → Observable
- Row number: Unknown → Observable
- Code presence: Unknown → Observable
- (Evidence: Direct BOQRow field inspection)

**2026-07-16 — After Spike 2: Row Sequence Analysis**
- Parent header: Unknown → Derivable
- Empty header detection: Unknown → Derivable
- (Evidence: Sequence analysis demonstrated deterministic computation)
```

### 5. Final State

When investigation complete, all capabilities should be either:
- Classified (Observable, Derivable, Domain Dependent, Not Determinable)
- Explicitly deferred with documented justification (may remain Unknown)

Investigation concludes when all capabilities are either classified or deferred with justification.

---

## State Transition Rules

### Unknown → Observable

**Evidence Required:** Data structure inspection confirms field exists.

**Example:** BOQRow has `row_type` field → Observable

### Unknown → Derivable

**Evidence Required:** 
- Deterministic algorithm defined
- Algorithm verified against production fixture
- Results reproducible

**Example:** Row sequence analysis demonstrates parent-child relationships can be computed → Derivable

### Unknown → Domain Dependent

**Evidence Required:** Mapped to specific Domain Knowledge document.

**Example:** Trade validation requires office trade schedule (domain doc 03) → Domain Dependent

### Unknown → Not Determinable

**Evidence Required:** Investigation demonstrates required information unavailable in current data structure or that current evidence is insufficient.

**Example:** Engineering intent requires human judgment, not present in data → Not Determinable

---

## Examples

### Example 1: Simple Observable Capability

| Candidate Engineering Capability | Obs | Der | Domain | Not Det | Unk | Consumer(s) | Evidence |
|----------------------------------|-----|-----|--------|---------|-----|-------------|----------|
| Row type classification | ✓ | | | | | All | BOQRow.row_type field |

### Example 2: Derivable Capability

| Candidate Engineering Capability | Obs | Der | Domain | Not Det | Unk | Consumer(s) | Evidence |
|----------------------------------|-----|-----|--------|---------|-----|-------------|----------|
| Empty header detection | | ✓ | | | | CheckMate | Spike 3: Head row with no subsequent Items |

### Example 3: Domain Dependent Capability

| Candidate Engineering Capability | Obs | Der | Domain | Not Det | Unk | Consumer(s) | Evidence |
|----------------------------------|-----|-----|--------|---------|-----|-------------|----------|
| Trade sequence validation | | | ✓ | | | CheckMate | Domain doc 03: Trade Schedule |

### Example 4: Unsupported Capability

| Candidate Engineering Capability | Obs | Der | Domain | Not Det | Unk | Consumer(s) | Evidence |
|----------------------------------|-----|-----|--------|---------|-----|-------------|----------|
| Engineering intent | | | | ✓ | | None | Requires human professional judgment |

### Example 5: Unknown Capability (Before Investigation)

| Candidate Engineering Capability | Obs | Der | Domain | Not Det | Unk | Consumer(s) | Evidence |
|----------------------------------|-----|-----|--------|---------|-----|-------------|----------|
| Hierarchy depth | | | | | ✓ | Formatter | Pending Spike 2 |

---

## Future Applications

This template can be reused for multiple investigation types:

- **EQ-0010:** Structural capability matrix for BOQ structural intelligence
- **EQ-0011:** Rule capability matrix for CheckMate validation rules
- **EQ-0012:** Reporting capability matrix for output formatting
- **EQ-0015:** PDF capability matrix for PDF extraction feasibility
- **EQ-0018:** Cubit capability matrix for Cubit parser capabilities

Each investigation produces its own capability matrix using this template.

---

## References

- `docs/engineering/Engineering_Governance.md` — Investigation methodology
- `docs/engineering/README.md` — Engineering workflow overview

---

## Document Control

**Version:** 1.0  
**Date:** 2026-07-14  
**Owner:** Project Owner