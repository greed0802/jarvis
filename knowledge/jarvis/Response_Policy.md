# Response Policy

This document outlines the canonical formatting and metadata injection policy for all Jarvis assistant responses.

## Response Signature
Every assistant response must map to a `ResolutionResult` containing:
1. **Source**: The exact platform system that answered (Workspace, Artifact, Knowledge, Memory, Capability, AI).
2. **Confidence**: `"High"`, `"Medium"`, or `"Low"`.
3. **Grounded**: `True` if checked against platform state.
4. **Evidence**: List of factual strings (e.g. workspace IDs, active project attributes, registry entries).
5. **Resolution Chain**: ordered trace of resolvers checked.

## Metadata Guidelines
- Non-developer mode: Display clear payload, source, confidence, and evidence.
- Developer mode: Append the execution time and the complete `Resolution Chain` trace. For example:
  `Chain: SelfKnowledgeResolver -> WorkspaceResolver`
- **Support Log Suppression**: Telemetry diagnostics and support logs are suppressed and kept hidden from users when transaction verbs (Preview, Approved, Create, Proceed, Run Preview, etc.) are executing. This improves client-side console clean-up and blocks diagnostic information leaks from appearing in message balloons. *Source Code Alignment: LK_S0012*

*Lightweight Source References: LK_S0012*
