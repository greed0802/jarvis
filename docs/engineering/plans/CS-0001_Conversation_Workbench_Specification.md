# CS-0001: Conversation Workbench Specification

**Status:** Active
**Date:** 2026-07-30
**Paired Plan:** CP-0001
**Evidence:** CV-0001
**Owner:** Capability Engineering

---

## 1. CLI Formatter Constraints

All CLI outputs MUST be explicitly formatted using the `BaseResponseRenderer` protocol.
This isolates ANSI formatting logic and `colorama`/`rich` dependency boundaries from the standard workbench orchestration layer.

## 2. Command Signal Processing

1. `KeyboardInterrupt (Ctrl+C)` during prompt execution: Cancel active task and return to generic REPL.
2. `KeyboardInterrupt (Ctrl+C)` at REPL standby: Prompt termination. Second interrupt force kills smoothly.

## 3. Platform Health Diagnostic

The `/status` command will summarize:
- Active model
- Core active pipelines
- Latency records mapping
- Trace availability