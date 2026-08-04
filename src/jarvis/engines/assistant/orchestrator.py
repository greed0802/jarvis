"""Workspace Assistant & Conversation Orchestration."""

import logging
from typing import Optional, Any

from jarvis.contracts.lifecycle import LifecycleAware
from jarvis.core.workspace.runtime import WorkspaceRuntime
from jarvis.engines.knowledge.engine import KnowledgeAcquisitionEngine
from jarvis.engines.airuntime.engine import AIRuntime
from jarvis.engines.airuntime.models import AIRequest, AIMessage
from jarvis.engines.planner.engine import IntentPlanner
from jarvis.domain.intent import Intent
from jarvis.core.capability.runtime import CapabilityRuntime
from jarvis.core.capability.models import ExecutionContext, CapabilityInput
from jarvis.core.pipeline.engine import ExecutionPipeline
from jarvis.core.pipeline.models import PipelineContext

logger = logging.getLogger(__name__)

class ContextAssembler:
    """Combines logical elements into AI Context."""
    def __init__(self, workspace_runtime: WorkspaceRuntime):
        self.workspace_runtime = workspace_runtime

class AttachmentCoordinator:
    """Manages file ingestion routing to Knowledge Engine."""
    def __init__(self, knowledge_engine: KnowledgeAcquisitionEngine):
        self.knowledge_engine = knowledge_engine

class ToolInvocationCoordinator:
    """Routes deterministic functions."""
    pass

class ConversationManager:
    """Tracks state and mutates Session arrays natively."""
    def __init__(self, workspace_runtime: WorkspaceRuntime):
        self.workspace_runtime = workspace_runtime

class WorkspaceAssistant(LifecycleAware):
    """The unified interface coordinate AI, Knowledge, and Workspace."""
    
    def __init__(
        self,
        workspace_runtime: WorkspaceRuntime,
        knowledge_engine: KnowledgeAcquisitionEngine,
        ai_runtime: AIRuntime
    ) -> None:
        self.workspace_runtime = workspace_runtime
        self.knowledge_engine = knowledge_engine
        self.ai_runtime = ai_runtime
        self.intent_planner: Optional[IntentPlanner] = None
        self.capability_runtime: Optional[CapabilityRuntime] = None
        self.execution_pipeline: Optional[ExecutionPipeline] = None
        
        self.context_assembler = ContextAssembler(self.workspace_runtime)
        self.attachment_coordinator = AttachmentCoordinator(self.knowledge_engine)
        self.conversation_manager = ConversationManager(self.workspace_runtime)
        self.tool_coordinator = ToolInvocationCoordinator()

    async def chat(self, prompt: str, session_id: str) -> str:
        """High-level abstraction for answering a prompt within a session context."""
        logger.info(f"WorkspaceAssistant processing chat for session {session_id}")
        
        # In a concrete implementation, context_assembler would attach Workspace/Project info here.
        system_prompt = "You are Jarvis, a Workspace Operating System Assistant."
        
        # New Flow: Planning Phase
        if self.intent_planner and self.capability_runtime:
            logger.info("Drafting intent execution plan.")
            # Dummy parsed intent
            intent = Intent(intent_id="int-1", context_id="ctx-1", goal=prompt)
            plan_res = self.intent_planner.generate_plan(intent)
            
            if plan_res.is_valid and "EXECUTE" in plan_res.plan.strategy:
                cap_target = plan_res.plan.strategy.split("EXECUTE ")[1]
                logger.info(f"Planner delegated directly to CapabilityRuntime for {cap_target}")
                
                # Execute mapped Capability directly without LLM hallucination
                ctx = ExecutionContext(workspace_id="default", session_id=session_id, inputs=CapabilityInput(parameters={}))
                cap_res = self.capability_runtime.execute(cap_target, ctx)
                return f"Capability Execution Result: {cap_res.status}"
        
        # Fallback to direct conversational response
        logger.info("Planner determined no engineering capability mapping; routing to AIRuntime fallback pass.")
        messages = [AIMessage(role="user", content=prompt)]
        req = AIRequest(messages=messages, model="default", system_prompt=system_prompt)
        
        resp = await self.ai_runtime.execute_request(req)
        return resp.content

    async def initialize(self) -> None:
        logger.info("WorkspaceAssistant initialized.")

    async def start(self) -> None:
        logger.info("WorkspaceAssistant started.")

    async def shutdown(self) -> None:
        logger.info("WorkspaceAssistant shutting down.")
