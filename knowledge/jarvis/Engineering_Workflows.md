# Engineering Workflows

This document defines standard engineering and quantity surveying workflows supported by the Jarvis Platform.

## Supported Workflows

### 1. New Project Setup
- **Objective**: Bootstrap workspace state.
- **Workflow**: Initialize workspace, register project, create interaction session, upload base documents.

### 2. Drawing Review
- **Objective**: Index and verify vectors.
- **Workflow**: Catalog drawing revisions, match layer schemas, extract properties (future), and mark revisions.

### 3. Specification Review
- **Objective**: Index requirements.
- **Workflow**: Parse specification files (future) and index standard clauses (materials, tolerances, rules).

### 4. BOQ Review & Validation
- **Objective**: Match and validate quantities against cost taxonomy.
- **Workflow**: Upload BOQ artifact (CSV/CostX), execute trade class Match, run trade validation rules (such as structural containment), check rates consistency.

### 5. Quantity Takeoff
- **Objective**: Calculate quantities.
- **Workflow**: Measure dimensions from vectors, map to BOQ line items.

### 6. RFI Generation
- **Objective**: Flag ambiguities.
- **Workflow**: Detect gaps in specs or drawings and compile structured RFI documents.

### 7. Engineering QA
- **Objective**: Validate evidence contracts.
- **Workflow**: Confirm checkmate integrity, verify validation engine findings.

## Advanced Execution Workflows

### 8. Workflows Continuity
- **Active Setup Continuity**: Plan amendment operations layer modifications as clean delta structures upon the active workspace. Levels mappings and zone configs are preserved during trade shifts rather than forcing a configuration wipe. *Source Code Alignment: LK_S0002*
- **Parser Reducer range expansion**: Shorthand level instructions expand sequentially (e.g. GF to L11) and support custom mezzanine abbreviations. Level reducers prevent early termination on auxiliary descriptors. *Source Code Alignment: LK_S0005*
- **Multiline Zone Value parsing boundaries**: Multiline description strings stop parsing before a newline followed by a next-zone indicator ('Zone N:'), preventing value runaway. *Source Code Alignment: LK_S0007*
- **Task state & URL rehydration**: Browser reloads query active databases to restore finished states ('export_ready') and rehydrate output file download links directly to the recovery panel. *Source Code Alignment: LK_S0011*

*Lightweight Source References: LK_S0002, LK_S0005, LK_S0007, LK_S0011*
