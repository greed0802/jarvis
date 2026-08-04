"""Execution Pipeline Contracts."""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime

@dataclass(frozen=True)
class PipelineStage:
    stage_id: str
    capability_name: str
    parameters: dict[str, Any]

@dataclass(frozen=True)
class PipelineContext:
    workspace_id: str
    session_id: str
    stage_outputs: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class StageExecutionTrace:
    stage_id: str
    capability_name: str
    start_time: datetime
    end_time: datetime
    status: str
    duration_ms: float
    output: Any
    error: Optional[str] = None

@dataclass(frozen=True)
class PipelineResult:
    pipeline_id: str
    status: str  # e.g., SUCCESS, FAILED
    traces: List[StageExecutionTrace] = field(default_factory=list)
    final_output: Optional[Any] = None
    error: Optional[str] = None
