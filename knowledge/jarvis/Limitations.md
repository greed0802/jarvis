# Platform Limitations

This registry outlines the current constraints and functional limitations of the Jarvis Platform.

## Stability Status

| Component | Status | Support Level | Deterministic? |
|-----------|--------|---------------|:--------------:|
| **Workspace Manager** | Stable | Fully functional | Yes |
| **Artifact Repository**| Stable | Metadata catalog only | Yes |
| **Validation Engine** | Stable | Rule-based checker | Yes |
| **Capability Engine** | Stable | Local registry and execution | Yes |
| **Memory Engine** | Stable | Context stores and graphs | Yes |
| **AIRuntime** | Experimental| Stub provider; mocked calls | No |
| **Knowledge Engine** | Stub | Ingestion placeholders | Yes |
| **Intent Planner** | Stub | Simple keyword matches | Yes |

## Constraints
- **Self-Knowledge**: All identity, roadmap, file, and limit queries are resolved deterministically from `knowledge/jarvis/` documents.
- **AI Dependence**: Conversational queries fallback to AI. Dynamic grounding is enabled, but AI answers are considered advisory.
- **Form-factors**: Shell (CLI) is the primary baseline interface. Desktop GUI/Web UIs are planned.
- **Unsafe Preview Export Gating**: The platform blocks workbook exportation parameters when compilation previews return validation failure flags (`safe_to_export: false`). Under this state, the UI disables all export/download actions and intercepts command calls to run export routines. All formula integrity issues are shown directly to the user in the preview drawer. *Source Code Alignment: LK_S0006*

*Lightweight Source References: LK_S0006*
