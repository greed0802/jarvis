# Repository Governance Manual

**Version:** 1.0.0  
**Status:** Approved

## 1. Governance Levels
The keywords "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119.
- **MUST**: Absolute requirement of the specification.
- **SHOULD**: Valid reasons may exist to ignore a particular item, but the full implications must be understood and carefully weighed.
- **MAY**: Truly optional.

## 2. Artifact Ontology
The structure of artifacts in the repository follows a strict hierarchical ontology:
`Repository → Domain → Workstream → Artifact Type → Identifier Policy`

## 3. Repository Mapping Table
Every artifact MUST be placed in its exact designated folder:

| Artifact Type | Target Folder |
| --- | --- |
| Engineering Questions (EQ) | `docs/engineering/questions/` |
| Architecture Reviews | `docs/architecture/reviews/` |
| Architecture Decision Records (ADR) | `docs/decisions/` |
| Governance Reports | `docs/governance/reports/` |
| Drift Reports | `docs/governance/reports/` |
| Architecture Conflict Reports | `docs/governance/reports/` |

## 4. Architecture Lifecycle
The architecture definition follows a strict progression:
1. **EQ**: Engineering Question (Problem discovery and spikes).
2. **Architecture Review**: Project Owner review of EQ findings.
3. **ADR**: Formalized and approved architectural decision (Architecture Decision Record).
4. **Capability Build**: Implementation of the specified architecture.
5. **Verification**: Mechanical verification and test execution.
6. **Release**: Deployment and release tagging.

## 5. Governance Decision Record (GDR) Schema
Before creating **ANY** file or directory, AI agents MUST output this block:

```markdown
# GOVERNANCE DECISION RECORD (GDR)
**Intent**: [Describe intent]
**Artifact Type**: [Type]
**Target Placement**: [Path]
**Verification**: [Criteria]
```

## 6. Repository Governance Quality Gate
Every task completion report MUST append this checklist:

```markdown
====================================================
REPOSITORY QUALITY GATE
====================================================
Architecture Compliance:         PASS / FAIL
Repository Boundary Check:       PASS / FAIL
Documentation Placement Check:   PASS / FAIL
Knowledge Boundary Check:        PASS / FAIL
Repository Governance Check:     PASS / FAIL
Repository Drift Check:          PASS / FAIL
Destructive Operations:          NONE / LIST
Files Created:                   [List paths]
Files Modified:                  [List paths]
Engineering Debt:                [List or state "None"]
Recommendation:                  [Freeze / Continue / EQ Required / ADR Required]
====================================================
```

## 7. Repository Evolution Policy
New root directories MUST NOT be created without an approved ADR. New subdirectories MUST be justified by a structural limitation of existing folders and proposed via a GDR.

## 8. Prohibited Placement Rules
- **MUST NOT** place execution or runtime code in `docs/` or `knowledge/`.
- **MUST NOT** place documentation in `src/` or `tests/`.
- **MUST NOT** place tools or operational scripts anywhere except `tools/` and `scripts/`.
- **MUST NOT** bypass the Repository Mapping Table for specified Artifact Types.