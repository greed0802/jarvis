"""Execution Pipeline Implementation."""
import logging
from typing import List
from datetime import datetime

from jarvis.contracts.lifecycle import LifecycleAware
from jarvis.core.capability.runtime import CapabilityRuntime
from jarvis.core.memory.engine import WorkspaceMemoryService
from jarvis.core.artifact.repository import ArtifactRepository
from jarvis.core.artifact.models import ArtifactType
from jarvis.core.capability.models import ExecutionContext, CapabilityInput
from jarvis.domain.planner import Plan
from .models import PipelineStage, PipelineContext, StageExecutionTrace, PipelineResult

logger = logging.getLogger(__name__)

class ExecutionPipeline(LifecycleAware):
    """Orchestrates sequential execution of capabilities, propagating results."""

    def __init__(self, capability_runtime: CapabilityRuntime, memory_service: WorkspaceMemoryService, artifact_repository: ArtifactRepository):
        self.capability_runtime = capability_runtime
        self.memory_service = memory_service
        self.artifact_repository = artifact_repository

    def execute_plan(self, plan: Plan, context: PipelineContext) -> PipelineResult:
        logger.info(f"Running pipeline execution for plan {plan.plan_id}")

        stages = []
        if "EXECUTE" in plan.strategy:
             target = plan.strategy.split("EXECUTE ")[1]
             stages.append(PipelineStage(stage_id="stage-1", capability_name=target, parameters={}))

        traces = []
        accumulated_outputs = dict(context.stage_outputs)

        for stage in stages:
             start_time = datetime.now()
             logger.info(f"Pipeline Stage execution: {stage.capability_name}")

             # Inject prior outputs as stage inputs for propagation
             merged_params = {}
             merged_params.update(stage.parameters)
             merged_params.update(accumulated_outputs)

             exec_ctx = ExecutionContext(
                  workspace_id=context.workspace_id,
                  session_id=context.session_id,
                  inputs=CapabilityInput(parameters=merged_params)
             )

             try:
                 cap_res = self.capability_runtime.execute(stage.capability_name, exec_ctx)
                 end_time = datetime.now()
                 duration = (end_time - start_time).total_seconds() * 1000.0

                 trace = StageExecutionTrace(
                     stage_id=stage.stage_id,
                     capability_name=stage.capability_name,
                     start_time=start_time,
                     end_time=end_time,
                     status=cap_res.status,
                     duration_ms=duration,
                     output=cap_res.output
                 )
                 traces.append(trace)

                 if cap_res.status != "SUCCESS":
                      return PipelineResult(
                           pipeline_id=f"run-{plan.plan_id}",
                           status="FAILED",
                           traces=traces,
                           error=f"Stage {stage.capability_name} failed with status {cap_res.status}."
                      )

                 accumulated_outputs[stage.capability_name] = cap_res.output

             except Exception as e:
                 logger.exception(f"Unhandled pipeline error on {stage.capability_name}")
                 end_time = datetime.now()
                 duration = (end_time - start_time).total_seconds() * 1000.0
                 trace = StageExecutionTrace(
                     stage_id=stage.stage_id,
                     capability_name=stage.capability_name,
                     start_time=start_time,
                     end_time=end_time,
                     status="ERROR",
                     duration_ms=duration,
                     output=None,
                     error=str(e)
                 )
                 traces.append(trace)
                 return PipelineResult(
                      pipeline_id=f"run-{plan.plan_id}",
                      status="ERROR",
                      traces=traces,
                      error=str(e)
                 )

        final_out = accumulated_outputs.get(stages[-1].capability_name) if stages else None
        res = PipelineResult(
            pipeline_id=f"run-{plan.plan_id}",
            status="SUCCESS",
            traces=traces,
            final_output=final_out
        )
        self.memory_service.store_entry(context.workspace_id, "execution_pipeline", {"plan_id": plan.plan_id, "status": "SUCCESS"})
        self.artifact_repository.register_artifact(
            workspace_id=context.workspace_id,
            name=f"report-{plan.plan_id}",
            artifact_type=ArtifactType.ENGINEERING_REPORT,
            content_hash="mock",
            size_bytes=1024,
            created_by="ExecutionPipeline"
        )
        return res

    async def initialize(self) -> None:
        logger.info("ExecutionPipeline initialized.")

    async def start(self) -> None:
        logger.info("ExecutionPipeline started.")

    async def shutdown(self) -> None:
        logger.info("ExecutionPipeline shutting down.")
