# Assistant Discovery — PROD-0003

## Executive Summary

The Jarvis Platform has reached a critical milestone. The Interactive Workspace Shell is operational, users can create workspaces, register documents, and execute capabilities. However, the `WorkspaceAssistant` currently returns mocked responses.

This discovery document analyzes the existing platform architecture to understand how to transform the Assistant into a **Knowledge-Driven Engineering Assistant** that consults deterministic platform knowledge before falling back to AI reasoning.

---

## Current Architecture Analysis

### Core Components

#### 1. WorkspaceAssistant
**Location**: `src/jarvis/engines/assistant/orchestrator.py`

**Current State**:
```python
def chat(self, question: str, session_id: str) -> str:
    return f"Mock response: {question}"
```

**Dependencies**:
- `WorkspaceRuntime` - workspace, project, session, knowledge management
- `KnowledgeAcquisitionEngine` - knowledge ingestion
- `AIRuntime` - AI provider routing (currently mocked)
- `CapabilityRuntime` - capability registry and execution
- `ExecutionPipeline` - orchestrates capability execution
- `IntentPlanner` - generates execution plans

**Placeholder Coordinators**:
- `ContextAssembler` - combines context for AI
- `AttachmentCoordinator` - routes file ingestion
- `ToolInvocationCoordinator` - routes deterministic functions
- `ConversationManager` - tracks conversation state

---

#### 2. IntentPlanner
**Location**: `src/jarvis/engines/planner/engine.py`

**Current Capabilities**:
- Converts Intent to ExecutionPlan
- Matches capabilities by name/description (trivial routing)
- Returns `PlannerResult` with validity status

**Current Routing Logic**:
```python
def _match_capabilities(self, goal: str) -> List[CapabilityDefinition]:
    matches = []
    for cap in self.capability_runtime.registry.list_all():
        if cap.name.lower() in goal.lower() or "analyze" in goal.lower():
            matches.append(cap)
    return matches
```

**Observation**: Keyword-based matching. No semantic classification.

---

#### 3. ExecutionPipeline
**Location**: `src/jarvis/core/pipeline/engine.py`

**Current Capabilities**:
- Executes plans sequentially
- Propagates results between stages
- Returns `PipelineResult` with stage traces

**Current Flow**:
```python
def execute_plan(self, plan: Plan, context: PipelineContext) -> PipelineResult:
    # Parse strategy "EXECUTE <capability>"
    # Execute capability through CapabilityRuntime
    # Return results with traces
```

**Observation**: Designed for capability execution, not query resolution.

---

#### 4. WorkspaceRuntime
**Location**: `src/jarvis/core/workspace/runtime.py`

**Capabilities**:
- `WorkspaceManager` - manages workspace entities
- `ProjectManager` - manages project entities
- `SessionManager` - manages session entities
- `KnowledgeRegistry` - manages knowledge items

**Available Operations**:
- Get active workspace
- Get active project
- Get active session
- List/get knowledge items

**Observation**: All data readily accessible for deterministic queries.

---

#### 5. ArtifactRepository
**Location**: `src/jarvis/core/artifact/repository.py`

**Capabilities**:
- Register artifacts (drawings, BOQs, specs)
- List artifacts by workspace
- Get artifact by ID
- List artifact versions

**Observation**: Complete catalog available for deterministic queries.

---

#### 6. WorkspaceMemoryService
**Location**: `src/jarvis/core/memory/engine.py`

**Capabilities**:
- Store memory entries by category
- Query entries by category
- Maintain knowledge graph (nodes + edges)

**Observation**: Execution history accessible for deterministic queries.

---

#### 7. CapabilityRuntime
**Location**: `src/jarvis/core/capability/runtime.py`

**Capabilities**:
- `CapabilityRegistry` - stores registered capabilities
- `list_all()` - returns all capability definitions
- `execute()` - executes capability with context

**Observation**: Capability catalog and execution readily available.

---

#### 8. AIRuntime
**Location**: `src/jarvis/engines/airuntime/engine.py`

**Current State**:
```python
async def execute_request(self, request: AIRequest, provider: str = "openai") -> AIResponse:
    return AIResponse(
        content="Mocked response from Unified AI Runtime.",
        model_used=request.model,
        usage={...}
    )
```

**Observation**: Infrastructure exists but returns mocked responses.

---

### Shell Integration

#### AskCommand
**Location**: `src/jarvis/ui/shell/commands.py`

**Current Implementation**:
```python
class AskCommand(CommandHandler):
    name = "ask"
    
    def execute(self, args: list[str], ctx: ShellContext) -> str:
        question = " ".join(args)
        answer = ctx.assistant.chat(question, ctx.session_id)
        return f"\n{answer}\n"
```

**Observation**: Simple pass-through to `WorkspaceAssistant.chat()`.

---

## Platform Knowledge Sources

The following knowledge sources exist and are **immediately accessible**:

| Source | Platform Component | Sample Queries |
|--------|-------------------|----------------|
| **Workspace Context** | WorkspaceRuntime | "What workspace am I in?", "What project am I working on?" |
| **Artifacts** | ArtifactRepository | "List uploaded files", "What documents exist?" |
| **Knowledge Items** | KnowledgeRegistry | "What knowledge items exist?", "Show registered documents" |
| **Memory** | WorkspaceMemoryService | "What's in memory?", "Show execution history" |
| **Capabilities** | CapabilityRuntime | "What capabilities exist?", "List available capabilities" |
| **Capability Results** | ExecutionPipeline | "Run BOQ Intelligence" (generates evidence) |

---

## Architectural Opportunities

### 1. IntentPlanner as Central Router
The IntentPlanner should evolve from keyword matching to semantic intent classification:

```
"What project am I working on?"
    ↓
Intent: QUERY / Workspace / Describe
```

### 2. Resolver Architecture
Introduce independent resolvers for each knowledge domain:

```
WorkspaceResolver  → WorkspaceRuntime
ArtifactResolver   → ArtifactRepository
KnowledgeResolver  → KnowledgeRegistry
MemoryResolver     → WorkspaceMemoryService
CapabilityResolver → CapabilityRuntime
AIResolver         → AIRuntime + GroundingEngine
```

### 3. ResolverChain Execution
ExecutionPipeline should walk a resolver chain until one resolves the query:

```
IntentPlanner → ExecutionPlan → ExecutionPipeline → ResolverChain → ResolutionResult
```

### 4. Universal ResolutionResult
Every resolver returns the same contract:

```python
ResolutionResult(
    resolved=True,
    source="Workspace",
    confidence="High",
    payload="Project: Bridge Construction",
    evidence=[...],
    grounded=True,
    execution_time_ms=4
)
```

### 5. AI as Last Resort
AIResolver should only activate when deterministic resolvers cannot answer:

```
Question → ResolverChain → Deterministic Answer (if possible)
                        → GroundingEngine → AI Answer (if necessary)
```

---

## Success Criteria

The following commands must work deterministically (without AI):

```bash
ask what project am I working on        # → WorkspaceResolver
ask what workspace is active            # → WorkspaceResolver
ask list uploaded files                 # → ArtifactResolver
ask what documents exist                # → ArtifactResolver / KnowledgeResolver
ask what capabilities exist             # → CapabilityResolver
ask what is in memory                   # → MemoryResolver
```

The following commands must execute capabilities and return evidence:

```bash
ask run BOQ Intelligence                # → CapabilityResolver → Evidence
```

The following commands must fall back to AI with grounding:

```bash
ask summarize this workspace            # → AIResolver (with context)
ask explain this project                # → AIResolver (with context)
```

---

**Discovery Date**: 2026-08-04  
**Milestone**: PROD-0003  
**Status**: Complete  
**Next**: Implementation
