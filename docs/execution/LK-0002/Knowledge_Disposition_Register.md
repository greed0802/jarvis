# Knowledge Disposition Register

This register details the disposition decisions and targets for each atomic knowledge unit extracted from legacy staging.

| Unit ID | Title | Staged Candidate | Category | Proposed Disposition | Target Canonical Location |
|---|---|---|---|---|---|
| **LK_U0001** | Clarification Card Retention | `LK_S0001` | Behavior | **MERGE** | `Interaction_Policy.md` -> ## Clarification & Limits |
| **LK_U0002** | Metadata Delta Amendments | `LK_S0002` | Workflow | **MERGE** | `Engineering_Workflows.md` -> ## Advanced Execution Workflows |
| **LK_U0003** | Snapshot Immutable Runs | `LK_S0003` | Architecture | **MERGE** | `Architecture.md` -> ## Boundary Rules |
| **LK_U0004** | cached Fingerprint Signature | `LK_S0004` | Architecture | **ADOPT** | `Architecture.md` -> ## Boundary Rules |
| **LK_U0005** | Level range sequence Reducer | `LK_S0005` | Behavior | **MERGE** | `Engineering_Workflows.md` -> ## Advanced Execution Workflows |
| **LK_U0006** | export safety Checker gating | `LK_S0006` | Workflow | **MERGE** | `Limitations.md` -> ## Constraints |
| **LK_U0007** | multiline zone phrase Splitter | `LK_S0007` | Behavior | **MERGE** | `Engineering_Workflows.md` -> ## Advanced Execution Workflows |
| **LK_U0008** | static check evidence compilation | `LK_S0008` | Architecture | **ADOPT** | `Architecture.md` -> ## Boundary Rules |
| **LK_U0009** | release hygiene parameters gating | `LK_S0009` | Policy | **ADOPT** | `Version.md` -> ## Release Hygiene Verification Gates |
| **LK_U0010** | bidirectional abbreviation mapping | `LK_S0010` | Behavior | **MERGE** | `Interaction_Policy.md` -> ## Clarification & Limits |
| **LK_U0011** | session restore link rehydration | `LK_S0011` | Workflow | **MERGE** | `Engineering_Workflows.md` -> ## Advanced Execution Workflows |
| **LK_U0012** | Telemetry logs Suppress logic | `LK_S0012` | Policy | **MERGE** | `Response_Policy.md` -> ## Metadata Guidelines |

### Disposition Action Logics
* **ADOPT:** Add raw section directly to the destination document as defined.
* **MERGE:** Merge knowledge parameters into existing structures of the target document, rewriting sentences to preserve a single engineering style.
