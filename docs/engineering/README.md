# Engineering Process

**Overview:** This directory contains active engineering investigations, capability matrices, and evidence collection for the Jarvis Platform.

**Governance:** All investigations follow `Engineering_Governance.md` v1.0

---

## Directory Structure

```
docs/engineering/
├── Engineering_Governance.md          # Investigation methodology (v1.0)
├── README.md                          # This file
│
├── questions/                         # Engineering Question documents
│   └── EQ_0010_Deterministic_BOQ_Structural_Intelligence.md
│
├── capability_matrices/               # Capability boundary definitions
│   └── EQ_0010_Structural_Capability_Matrix.md
│
└── evidence/                          # Investigation evidence and reports
    └── (created during/after investigations)
```

---

## Engineering Workflow

The repository follows a structured engineering investigation process:

```
1. Engineering Question (Specification)
   ↓
2. Project Owner Approval
   ↓
3. Capability Matrix (Initial state: mostly Unknown)
   ↓
4. Investigation Spikes (Evidence collection)
   ↓
5. Capability Matrix Updates (Evidence-based transitions)
   ↓
6. Evidence Report (Findings, conclusions, recommendation)
   ↓
7. Project Owner Disposition
   ↓
8. Implementation (if approved)
```

Detailed workflow: See `Engineering_Governance.md`

---

## Active Investigations

### EQ-0010: Deterministic BOQ Structural Intelligence

**Status:** Investigation Phase — Spike 4 Complete

**Purpose:** Investigate what deterministic structural information can be derived from BOQRow alone.

**Scope:** Observable, Derivable, and Domain Dependent structural analyses operating only on `list[BOQRow]`.

**Constraints:**
- No AI, no heuristics, no NLP
- No parser modifications
- No runtime changes
- No architecture proposals
- Investigation only (no implementation)

**Documents:**
- Investigation specification: `questions/EQ_0010_Deterministic_BOQ_Structural_Intelligence.md`
- Capability matrix: `capability_matrices/EQ_0010_Structural_Capability_Matrix.md`

**Completed Spikes:**
- ✅ Spike 1: Direct Field Observation (frozen)
- ✅ Spike 2: UOM Pattern Analysis (frozen)
- ✅ Spike 3: Row Sequence Analysis (frozen)
- ✅ Spike 4: Hierarchy Reconstruction (frozen)

**Capabilities Classified (16 of 25):**
- 8 Observable (row_type, row_number, code, description, quantity, uom, section, hierarchy indicator)
- 8 Derivable (row type transitions, empty header detection, heading statistics, hierarchy depth, parent header identification, heading tree structure, orphan item detection, items-per-header ratio)

**Next Step:** Spike 5: Domain Reconciliation

---

## Completed Investigations

None yet. This is the first Engineering Question under the new governance model.

---

## Five-Layer Governance Model

The repository uses five complementary governance layers:

| Layer | Purpose | Location |
|-------|---------|----------|
| **Principles** | Engineering philosophy | `docs/01_Principles.md` |
| **ADRs** | Architectural decisions | `docs/decisions/` |
| **Engineering Governance** | Investigation methodology | `Engineering_Governance.md` |
| **Engineering Questions** | Capability investigations | `questions/` |
| **Evidence Reports** | Implementation justification | `evidence/` |

Each layer has distinct responsibility with no overlap.

---

## Capability Matrix Lifecycle

Capability Matrices track the discovery of engineering capabilities through five states:

| State | Meaning |
|-------|---------|
| **Observable** | Directly available in data structure fields |
| **Derivable** | Deterministically computable from available data |
| **Domain Dependent** | Requires Domain Knowledge Layer validation |
| **Not Determinable** | Cannot be determined from current data structure |
| **Unknown** | Evidence not yet collected |

### Lifecycle Stages

1. **Initial State:** Most capabilities marked "Unknown"
2. **Investigation:** Spikes collect evidence, capabilities transition to evidenced states
3. **Final State:** All capabilities either classified or explicitly deferred with justification
4. **Timeline Preserved:** Document evolution tracked throughout investigation

Template: `docs/templates/Capability_Matrix_Template.md`

---

## Engineering Question Lifecycle

### Planning Phase

- Engineering Question document created
- Capability Matrix initialized
- Investigation plan defined
- Project Owner approval requested

### Investigation Phase

- Spikes executed (with approval)
- Evidence collected
- Capability Matrix updated after each spike
- Observations documented

### Conclusion Phase

- Evidence Report written
- Findings and conclusions documented
- Production recommendation made
- Project Owner disposition requested

### Implementation Phase (if approved)

- Production code developed
- Tests written
- Documentation updated
- Capability delivered

---

## Evidence Quality Standards

All engineering evidence must meet these standards:

**Deterministic:** Results must be reproducible. Same input produces same output every time.

**Production-Verified:** Evidence must come from registered production fixtures, not synthetic test data.

**Documented:** Evidence source, collection method, and interpretation must be clearly documented.

**Traceable:** Evidence must reference specific fixtures, spikes, or domain documents.

---

## Approval Gates

### Gate 1: Investigation Authorization

**Before:** Engineering Question created  
**After:** Investigation spikes may begin

**Approver:** Project Owner

**Criteria:**
- Problem statement clear and justified
- Investigation plan feasible
- Capability Matrix initialized
- Success criteria defined

### Gate 2: Implementation Authorization

**Before:** Evidence Report published  
**After:** Production implementation may begin

**Approver:** Project Owner

**Criteria:**
- Investigation complete (exit criteria met)
- Evidence collected and documented
- Recommendation justified by evidence
- Architecture impact assessed

---

## Artifact Ownership

| Artifact | Mutable? | Purpose |
|----------|----------|---------|
| **Engineering Question** | No (after approval) | Investigation specification |
| **Capability Matrix** | Yes (during investigation) | Investigation state tracking |
| **Spike Evidence** | No | Individual investigation results |
| **Evidence Report** | No (except corrections) | Findings and recommendation |

See `Engineering_Governance.md` for detailed ownership rules.

---

## Historical Engineering Preservation

The repository preserves engineering knowledge evolution:

**Preserved Artifacts:**
- All Engineering Questions (investigation specifications)
- All Capability Matrices (investigation state evolution)
- All Evidence Reports (findings and recommendations)
- All Spike Evidence (individual investigation results)

**Purpose:**
- Future engineers understand why decisions were made
- Evidence remains available for re-evaluation
- Methodology can be improved based on historical outcomes
- Prevents rediscovering known limitations

**Immutability:** Once published, artifacts should not be modified except for factual corrections.

---

## Related Documentation

### Governance
- `Engineering_Governance.md` — Investigation methodology (v1.0)
- `docs/01_Principles.md` — Engineering philosophy
- `docs/decisions/TEMPLATE.md` — ADR process

### Templates
- `docs/templates/Capability_Matrix_Template.md` — Reusable capability matrix template

### Reference
- `docs/reference/Engineering_Questions.md` — Historical registry of all EQs
- `docs/reference/Engineering_Fixtures.md` — Fixture governance

### Domain Knowledge
- `docs/domain/` — Professional QS knowledge layer

---

## FAQ

### When should I create an Engineering Question?

When you need to investigate an engineering problem with uncertain feasibility, scope, or approach. EQs provide structured investigation with evidence collection.

### What's the difference between an EQ and an ADR?

- **Engineering Question:** Investigates what is possible ("Can we detect hierarchy depth?")
- **ADR:** Documents architectural decisions ("We chose X over Y because...")

EQs may produce evidence that leads to ADRs, but they serve different purposes.

### Can I skip the investigation phase and go straight to implementation?

No. Engineering_Governance.md v1.0 requires investigation spikes to collect evidence before implementation authorization. This prevents speculative features and premature abstractions.

### What if I discover the investigation scope needs to change?

Document the scope change in the Capability Matrix update history. If the change is significant, consult Project Owner for disposition. The EQ remains immutable once approved, but the investigation can adapt based on evidence.

### How do I know when investigation is complete?

The Exit Criteria in the Engineering Question define completion. Typically: all capabilities have either transitioned from "Unknown" to evidenced states (Observable/Derivable/Domain/Not Determinable) or are explicitly deferred with documented justification.

---

## Contributing

When contributing to engineering investigations:

1. Read `Engineering_Governance.md` to understand the process
2. Check active investigations to avoid duplication
3. If proposing a new EQ, discuss with Project Owner first
4. Follow the five-state capability model for evidence classification
5. Preserve timeline in Capability Matrix updates
6. Document all evidence sources clearly

---

## Document Control

**Version:** 1.0  
**Date:** 2026-07-14  
**Owner:** Project Owner  
**Review:** Upon new EQ registration or governance updates