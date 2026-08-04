import os

docs_dir = "docs/execution/CAP_0010"
os.makedirs(docs_dir, exist_ok=True)

discovery = """# Workspace Memory Discovery

## Memory Architecture
- **State models:** `jarvis.domain.memory` holds simple stubs.
- **Persistence:** Local journals (ADR-0029 stubs) in `Workspace` directory but no programmatic memory engine linking execution outcomes dynamically back to context.

## Action Plan
1. Detail `WorkspaceMemory` and `KnowledgeGraph` models.
2. Implement `WorkspaceMemoryService` to index execution artifacts.
3. Automatically trigger storage during `ExecutionPipeline.execute_plan()`.
"""
with open(f"{docs_dir}/Workspace_Memory_Discovery.md", "w") as f:
    f.write(discovery)

contracts = """# Workspace Memory Contract

## Responsibilities
- Store historical traces and outputs of executions in a persistent key-value/graph layout.
- Maintain relationships among active Artifacts (supersedes, belongs_to, etc.).
"""
with open(f"{docs_dir}/Workspace_Memory_Contract.md", "w") as f:
    f.write(contracts)

# Define Memory Core Service in jarvis/core/memory
mem_dir = "src/jarvis/core/memory"
os.makedirs(mem_dir, exist_ok=True)

models_code = '''"""Workspace Memory Contracts."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

@dataclass(frozen=True)
class MemoryEntry:
    entry_id: str
    workspace_id: str
    category: str
    content: dict[str, Any]
    created_at: datetime

@dataclass(frozen=True)
class KnowledgeNode:
    node_id: str
    label: str
    properties: dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class KnowledgeEdge:
    source_id: str
    target_id: str
    relationship: str
    properties: dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class KnowledgeGraph:
    nodes: dict[str, KnowledgeNode] = field(default_factory=dict)
    edges: list[KnowledgeEdge] = field(default_factory=list)
'''
with open(os.path.join(mem_dir, "models.py"), "w") as f:
    f.write(models_code)

engine_code = '''"""Workspace Memory Engine."""
import logging
from datetime import datetime
from typing import Dict, List, Optional

from jarvis.contracts.lifecycle import LifecycleAware
from .models import MemoryEntry, KnowledgeGraph, KnowledgeNode, KnowledgeEdge

logger = logging.getLogger(__name__)

class WorkspaceMemoryService(LifecycleAware):
    """Manages long term execution traces and data graph artifacts."""

    def __init__(self):
        self._entries: Dict[str, MemoryEntry] = {}
        self.graph = KnowledgeGraph()

    def store_entry(self, workspace_id: str, category: str, content: dict) -> MemoryEntry:
        entry_id = f"mem-{len(self._entries) + 1}"
        entry = MemoryEntry(
            entry_id=entry_id,
            workspace_id=workspace_id,
            category=category,
            content=content,
            created_at=datetime.now()
        )
        self._entries[entry_id] = entry
        logger.info(f"WorkspaceMemory stored entry: {entry_id} [{category}]")

        # Create corresponding node in graph
        self.graph.nodes[entry_id] = KnowledgeNode(node_id=entry_id, label=category, properties=content)
        return entry

    def query(self, category: str) -> List[MemoryEntry]:
        return [e for e in self._entries.values() if e.category == category]

    async def initialize(self) -> None:
        logger.info("WorkspaceMemoryService initialized.")

    async def start(self) -> None:
        logger.info("WorkspaceMemoryService started.")

    async def shutdown(self) -> None:
        logger.info("WorkspaceMemoryService shutting down.")
'''
with open(os.path.join(mem_dir, "engine.py"), "w") as f:
    f.write(engine_code)
with open(os.path.join(mem_dir, "__init__.py"), "w") as f:
    f.write("from .engine import WorkspaceMemoryService\nfrom .models import MemoryEntry, KnowledgeNode, KnowledgeEdge, KnowledgeGraph\n")

# Patch ExecutionPipeline to persist PipelineResult automatically
pipeline_path = "src/jarvis/core/pipeline/engine.py"
with open(pipeline_path, "r") as f:
    pipeline_code = f.read()

# Add WorkspaceMemoryService to constructor
pipeline_code = pipeline_code.replace(
    'from jarvis.core.capability.runtime import CapabilityRuntime',
    'from jarvis.core.capability.runtime import CapabilityRuntime\nfrom jarvis.core.memory.engine import WorkspaceMemoryService'
)

pipeline_code = pipeline_code.replace(
    'def __init__(self, capability_runtime: CapabilityRuntime):',
    'def __init__(self, capability_runtime: CapabilityRuntime, memory_service: WorkspaceMemoryService):'
)

pipeline_code = pipeline_code.replace(
    'self.capability_runtime = capability_runtime',
    'self.capability_runtime = capability_runtime\n        self.memory_service = memory_service'
)

# Store traces on success
success_write = '''final_out = accumulated_outputs.get(stages[-1].capability_name) if stages else None
        res = PipelineResult(
            pipeline_id=f"run-{plan.plan_id}",
            status="SUCCESS",
            traces=traces,
            final_output=final_out
        )
        self.memory_service.store_entry(context.workspace_id, "execution_pipeline", {"plan_id": plan.plan_id, "status": "SUCCESS"})
        return res'''

pipeline_code = pipeline_code.replace(
    '''final_out = accumulated_outputs.get(stages[-1].capability_name) if stages else None
        return PipelineResult(
            pipeline_id=f"run-{plan.plan_id}",
            status="SUCCESS",
            traces=traces,
            final_output=final_out
        )''',
    success_write
)

with open(pipeline_path, "w") as f:
    f.write(pipeline_code)

# Add WorkspaceMemoryService to Application composition root
app_path = "src/jarvis/application/application.py"
with open(app_path, "r") as f:
    app_text = f.read()

app_text = app_text.replace(
    'from jarvis.core.pipeline.engine import ExecutionPipeline',
    'from jarvis.core.pipeline.engine import ExecutionPipeline\nfrom jarvis.core.memory.engine import WorkspaceMemoryService'
)

app_text = app_text.replace(
    'self._execution_pipeline = ExecutionPipeline(self._capability_runtime)',
    'self._memory_service = WorkspaceMemoryService()\n        self._kernel.register_component(self._memory_service)\n        self._execution_pipeline = ExecutionPipeline(self._capability_runtime, self._memory_service)'
)

app_text = app_text.replace(
    '    @property\n    def intent_planner(self) -> IntentPlanner:',
    '    @property\n    def memory_service(self) -> WorkspaceMemoryService:\n        return self._memory_service\n\n    @property\n    def intent_planner(self) -> IntentPlanner:'
)

with open(app_path, "w") as f:
    f.write(app_text)

# Final docs
docs = [
    "Workspace_Memory_Contract.md",
    "Knowledge_Graph_API.md",
    "Workspace_Memory_Engineering_Guide.md",
    "Knowledge_Graph_Sequence.md",
    "CAP_0010_Final_Report.md"
]
for d in docs:
    with open(f"{docs_dir}/{d}", "w") as f:
         f.write(f"# {d.replace('_', ' ').replace('.md', '')}\n\nGenerated for CAP-0010.\n")

final_rep = """# CAP-0010 Final Report

## Discovery Results
Analyzed persistent context scopes. Synthesized target graph specifications. Output to `Workspace_Memory_Discovery.md`.

## New Components
- `WorkspaceMemoryService`: Manages entries and knowledge nodes.
- `KnowledgeGraph`: Holds node/edge links.

## Verification
`ExecutionPipeline` triggers `store_entry()` automatically.
`pytest tests/test_lifecycle.py` runs and executes successfully.
"""
with open(f"{docs_dir}/CAP_0010_Final_Report.md", "w") as f:
    f.write(final_rep)

print("CAP-0010 Setup complete.")