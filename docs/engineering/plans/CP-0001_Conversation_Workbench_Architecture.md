# CP-0001: Conversation Workbench Architecture

**Status:** Active
**Date:** 2026-07-30
**Milestone:** Track C - Presentation Adapter
**Paired Spec:** CS-0001
**Paired Evidence:** CV-0001
**Owner:** Capability Engineering

---

## 1. Objective

Build the platform's first end-to-end interactive CLI environment to orchestrate the internal pipelines seamlessly without leaking engine state to the user layer. Implement graceful shutdown and system diagnostics checking.

---

## 2. Architecture

```
User -> InteractiveCLIWorkbench [CLI]
      -> ConversationService.execute [Application]
          -> RetrievalCoordinator [Engine]
          -> ReasoningPipeline [Engine]
          -> GenerationPipeline [Engine]
      -> CLIFormatter.render [Presentation Mapping]
      -> Output text to terminal
```

## 3. Acceptance Criteria

| AC | Criterion |
|----|-----------|
| AC-1 | Application Orchestration: `ConversationService` uses `ConversationRequest`. |
| AC-2 | Passive CLI Adapter: `InteractiveCLIWorkbench` does not invoke core engines directly. |
| AC-3 | Renderer Protocol Compliance: Output strictly driven by `BaseResponseRenderer`. |
| AC-4 | Citation & Metric Display: Output traces format beautifully in ANSI terminal. |
| AC-5 | Slash Commands: Implements /help, /status, /trace, /clear, /exit. |
| AC-6 | Kernel Diagnostics: /status output is correctly gathered from system properties. |
| AC-7 | Graceful Signal Handling: `Ctrl+C` cancels without killing immediately. |
| AC-8 | Architecture Boundary Protection: `jarvis.cli` never imported by core domain. |
| AC-9 | Batch / Non-Interactive Mode: Pipe ingestion supported for evaluators. |
| AC-10 | Zero Production Regression: 1,186 internal tests passing unchanged. |