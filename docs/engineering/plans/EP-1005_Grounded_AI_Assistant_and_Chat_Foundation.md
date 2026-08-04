# EP-1005: M10.5 — Grounded AI Assistant & Chat Foundation

**Status:** OPEN
**Date:** 2026-07-29
**Milestone:** M10.5
**Authors:** Product Engineering
**Frozen ADR Baseline:** ADR-0030, ADR-0031, ADR-0032
**Playbook Reference:** `docs/engineering/Engineering_Execution_Playbook.md`

---

## 1. Objective

Execute two coordinated workstreams:

1. **Workstream A (Contracts & Boundaries):** Define the `AssistantResponse` public contract alongside internal contracts (`RetrievedContext`, `GroundingContext`, `DraftResponse`) and the `GenerationProvider` protocol.
2. **Workstream B (Grounded Assistant Pipeline):** Build the retrieval components (`UnderstandingRetriever`, `EvidenceRetriever`), pluggable `GenerationProvider`, `GroundingValidator`, and `GroundedAssistantService` orchestrator.

This EP builds the first downstream consumer of the `ProjectUnderstanding` public contract from M10.4, establishing the end-to-end acyclic capability chain from evidence through to AI-generated responses with grounding verification.

---

## 2. Scope & Deliverables

### Workstream A — Contracts & Boundaries

| # | Deliverable | Description |
|---|-------------|-------------|
| A1 | `AssistantResponse` public contract | Immutable frozen dataclass: `response_id`, `query_text`, `response_text`, `grounding_status` (FULLY_GROUNDED/PARTIALLY_GROUNDED/UNSUPPORTED), `cited_evidence` (list of `EvidenceReference`), `understanding_provenance_id`, `confidence_score` (float), `suggested_followups` (list[str]) |
| A2 | `RetrievedContext` internal contract | Frozen dataclass: `query_id`, `intent_category`, `relevant_findings` (list[UnderstandingFinding]), `query_terms` (list[str]) |
| A3 | `GroundingContext` internal contract | Frozen dataclass: `context_id`, `retrieved_context` (RetrievedContext), `retrieved_evidence` (list[EvidenceReference]), `formatted_prompt_payload` (str) |
| A4 | `DraftResponse` internal contract | Frozen dataclass: `provider_name`, `provider_version`, `response_text`, `generation_metadata` (dict[str, str]) |
| A5 | `GenerationProvider` protocol | Runtime-checkable protocol: `generate_draft(context: GroundingContext) -> DraftResponse` |

### Workstream B — Grounded Assistant Pipeline

| # | Deliverable | Description |
|---|-------------|-------------|
| B1 | `QuestionInterpreter` | Analyzes raw query text, extracts search terms and intent categories |
| B2 | `UnderstandingRetriever` | Queries ProjectUnderstandingService for matching UnderstandingFinding records, produces RetrievedContext |
| B3 | `EvidenceRetriever` | Resolves EvidenceReference objects from EvidenceRepository using finding evidence counts/context, produces GroundingContext |
| B4 | `MockGenerationProvider` | Deterministic reference implementation of GenerationProvider protocol for offline testing |
| B5 | `GroundingValidator` | Consumes DraftResponse + GroundingContext; verifies claims against evidence; computes confidence_score; assigns GroundingStatus |
| B6 | `GroundedAssistantService` | Main orchestrator: retrieval → provider draft → validation → response emission |

---

## 3. Architecture Traceability Matrix

| ADR Reference | Decision / Invariant | Implemented In | Verification |
|---------------|---------------------|---------------|--------------|
| ADR-0030 | C1.1 — Evidence Primacy | EvidenceRetriever resolves EvidenceRef from EvidenceRepository | Test: cited_evidence in AssistantResponse originates strictly from EvidenceRepository |
| ADR-0030 | C1.3 — Scope Boundary | Assistant domain SHALL NOT import ExecutionOutcome, CheckMateEngine, RuleSnapshot, RuleRegistry, CheckMateRule | Test: automated boundary check verifies zero cross-imports |
| ADR-0031 | C1.13 — Public Contract Decoupling | GenerationProvider receives strictly GroundingContext (never raw ProjectUnderstanding or engine models) | Test: provider.generate_draft() is called with GroundingContext parameter type |
| ADR-0031 | C1.14 — FindingReport Version Provenance | understanding_provenance_id links back to FindingReport provenance | Test: response references correct understanding report provenance |
| ADR-0031 | C1.15 — Report Completeness & Integrity | AssistantResponse is frozen, immutable dataclass | Test: dataclass(frozen=True); post-creation mutation raises |
| ADR-0032 | C1.4 — Evidence Immutability | GroundingContext carries resolved EvidenceReference objects (immutable refs) | Test: evidence refs inside cited_evidence match repository originals |
| ADR-0032 | C1.9 — Rule Determinism | MockGenerationProvider produces identical outputs given identical GroundingContext | Test: repeated calls with same context yield identical DraftResponse |
| ADR-0032 | C1.11 — Bound sovereignty | GroundingValidator independently computes confidence_score; generation providers SHALL NOT self-report scores | Test: validator confidence differs from provider metadata when provider erroneously reports confidence |

---

## 4. Acyclic Capability Chain

```text
EvidenceRepository (M10.2)
        │
        ▼
CheckMateEngine → ExecutionOutcome[ ] → FindingReportAssembler → FindingReport (M10.3)
                                                                          │
                                                                          ▼
                                                               ProjectUnderstandingImporter
                                                                          │
                                                                          ▼
                                                                  ProjectUnderstandingStore
                                                                          │
                                                                          ▼
                                                                 ProjectUnderstandingService
                                                                          │
                                                                          ▼
                                                                 ProjectUnderstanding (M10.4)
                                                                          │
                                                              ┌───────────┴───────────┐
                                                              ▼                       ▼
                                                      UnderstandingRetriever    EvidenceRetriever
                                                              │                       │
                                                              ▼                       ▼
                                                              RetrievedContext    +   EvidenceReference[ ]
                                                                          │
                                                                          ▼
                                                                   GroundingContext
                                                                          │
                                                                          ▼
                                                                   GenerationProvider
                                                                          │
                                                                          ▼
                                                                     DraftResponse
                                                                          │
                                                                          ▼
                                                                   GroundingValidator
                                                                          │
                                                                          ▼
                                                                   AssistantResponse (Public Contract)
                                                                          │
                                                              ┌───────────┴───────────┐
                                                              ▼                       ▼
                                                      M10.6 Workbench UI         External Integration
```

**Strict Boundary Rules:**
- `GenerationProvider` MUST receive strictly `GroundingContext`—it SHALL NOT receive raw `ProjectUnderstanding` or engine models.
- `GroundingValidator` strictly owns `grounding_status` and `confidence_score` — generation providers SHALL NOT self-report or compute these values.
- Internal engine types (`ExecutionOutcome`, `CheckMateEngine`, `RuleSnapshot`, `RuleRegistry`, `CheckMateRule`) SHALL NOT be imported anywhere in the assistant domain.

---

## 5. Key Design Decisions

### 5.1 Grounding Before Generation

The `GenerationProvider` interface exists behind a grounding firewall. It receives `GroundingContext` — a fully resolved, evidence-backed data structure — not raw `ProjectUnderstanding` or retrieval results. This prevents providers from operating on unverified data.

### 5.2 Independent Validation

`GroundingValidator` operates independently of the provider. It verifies assertions against actual evidence and computes `confidence_score` based on coverage and retrieval match ratios, NOT on provider self-reported confidence.

### 5.3 Deterministic Mock Provider

`MockGenerationProvider` provides a controlled deterministic reference that responses identically given the same `GroundingContext`. This enables offline testing and ensures provider interchangeability.

---

## 6. Acceptance Criteria

| # | Criterion | Pass Condition |
|---|-----------|---------------|
| **AC-1** | `GenerationProvider` receives strictly `GroundingContext`, never raw `ProjectUnderstanding` or engine models | Provider interface only exposes `generate_draft(GroundingContext)` |
| **AC-2** | Evidence citations in `AssistantResponse.cited_evidence` originate strictly from `EvidenceRepository` | Citation objects match references resolvable from the repository |
| **AC-3** | Automated import-line audit verifies zero imports of engine internal types | Boundary check: zero imports of ExecutionOutcome, CheckMateEngine, RuleSnapshot, RuleRegistry, CheckMateRule |
| **AC-4** | Queries outside the scope of bound `ProjectUnderstanding` yield `UNSUPPORTED` grounding status | Query with no matching retrievals produces UNSUPPORTED |
| **AC-5** | `AssistantResponse`, `RetrievedContext`, `GroundingContext`, `DraftResponse` are frozen dataclasses | Mutation attempts raise FrozenInstanceError |
| **AC-6** | `GroundedAssistantService` operates identically regardless of backing `GenerationProvider` | Two different providers produce results through same service pipeline |
| **AC-7** | `GroundingValidator` computes `confidence_score` and `grounding_status` independently of provider | Validator confidence differs from provider metadata when tampered |

---

## 7. Quality Gates

**Tier 1 — Mandatory (MUST pass before promotion):**
- Unit test suite (`python -m pytest tests/applications/`)
- Documentation verifier (`python tools/quality/verify_documentation.py`)

**Tier 2 — Extended (DEFERRED):**
- Static type checker (DEFERRED)
- Import boundary analysis tool (DEFERRED)

---

## 8. Evidence Packages

This EP pairs with:
- **EV-1005:** `docs/engineering/evidence/EV-1005_Grounded_AI_Assistant_and_Chat_Foundation.md`

Per the Engineering Execution Playbook §3 Step 5: all promotions are governed by the EV-1005 record, not raw code changes or this plan alone.

---

## 9. Completion Record

| Field | Value |
|-------|-------|
| **Completed Date** | |
| **ADR Baseline Verified** | ADR-0030, ADR-0031, ADR-0032 |
| **Quality Gate Result** | |