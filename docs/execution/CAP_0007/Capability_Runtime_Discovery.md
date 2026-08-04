# Capability Runtime Discovery

## Existing Capability Artifacts
- **Contracts:** `src/jarvis/contracts/capabilities.py` contains `FindingReport`, `Finding`, and public interface definitions `CapabilityHost`. It heavily centers around CheckMate legacy logic (ADR-0030 / 0031).
- **Execution:** `src/jarvis/domain/executor.py` operates manually on pure pure-function mapping (`execute_domain_rules`).
- **Domain Placeholder:** `src/jarvis/domain/capability.py` was established in CAP-0002 as `CapabilityDefinition` metadata.

## Required Action
We need an agnostic generic Capability Registration mapping. `src/jarvis/engines/checkmate` already has strong rule-eval capabilities. The goal is to wrap `execute_domain_rules` or the existing `BOQIntelligence` system beneath the new `CapabilityRuntime`.
