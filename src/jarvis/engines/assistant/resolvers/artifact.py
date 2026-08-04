"""ArtifactResolver — Answers artifact-related queries."""

import logging
from datetime import datetime

from jarvis.engines.assistant.resolvers.base import Resolver, ResolutionResult
from jarvis.domain.intent import Intent
from jarvis.core.capability.models import ExecutionContext
from jarvis.core.artifact.repository import ArtifactRepository

logger = logging.getLogger(__name__)


class ArtifactResolver(Resolver):
    """Resolves artifact-related queries using ArtifactRepository.
    
    Handles:
    - QUERY / Artifact / List (e.g., "List uploaded files", "What documents exist?")
    - QUERY / Artifact / Describe (e.g., "Show artifact details")
    """

    def __init__(self, artifact_repository: ArtifactRepository):
        self.artifact_repository = artifact_repository

    def can_resolve(self, intent: Intent) -> bool:
        """Check if this intent targets artifacts."""
        if not intent.semantics:
            # Fallback: keyword matching
            goal_lower = intent.goal.lower()
            return any(keyword in goal_lower for keyword in [
                "file", "document", "artifact", "upload", "drawing", "boq", "spec"
            ])
        
        return intent.semantics.target == "Artifact"

    def resolve(self, intent: Intent, context: ExecutionContext) -> ResolutionResult:
        """Resolve artifact queries deterministically."""
        start_time = datetime.now()
        
        try:
            goal_lower = intent.goal.lower()
            
            if "list" in goal_lower or "what" in goal_lower:
                result = self._list_artifacts(context)
            else:
                result = self._list_artifacts(context)
            
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            return ResolutionResult(
                resolved=result.resolved,
                source=result.source,
                confidence=result.confidence,
                payload=result.payload,
                evidence=result.evidence,
                grounded=result.grounded,
                execution_time_ms=execution_time,
                reason=result.reason,
                resolution_chain=["ArtifactResolver"]
            )
            
        except Exception as e:
            logger.error(f"ArtifactResolver error: {e}")
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            return ResolutionResult(
                resolved=False,
                source="Artifact",
                confidence="Low",
                payload=f"Error resolving artifact query: {str(e)}",
                grounded=True,
                execution_time_ms=execution_time,
                reason=str(e),
                resolution_chain=["ArtifactResolver"]
            )

    def _list_artifacts(self, context: ExecutionContext) -> ResolutionResult:
        """List all artifacts in the current workspace."""
        workspace_id = context.workspace_id
        # List all artifacts (internal access — public API is get() only)
        all_artifacts = list(self.artifact_repository._artifacts.values())
        
        if not all_artifacts:
            return ResolutionResult(
                resolved=True,
                source="Artifact",
                confidence="High",
                payload="No artifacts registered. Upload files with 'upload <path>'.",
                grounded=True,
                reason="No artifacts found in workspace"
            )
        
        artifact_lines = ["Registered Artifacts:"]
        evidence = []
        
        for artifact in all_artifacts:
            artifact_lines.append(f"  - {artifact.name} ({artifact.artifact_type.name})")
            evidence.append(f"{artifact.name} ({artifact.artifact_type.name})")
        
        return ResolutionResult(
            resolved=True,
            source="Artifact",
            confidence="High",
            payload="\n".join(artifact_lines),
            evidence=evidence,
            grounded=True,
            reason=f"Found {len(all_artifacts)} artifact(s) in workspace"
        )
