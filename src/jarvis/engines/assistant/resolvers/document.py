# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Any, List
from jarvis.engines.assistant.resolvers.base import Resolver, ResolutionResult
from jarvis.domain.intent import Intent
from jarvis.core.capability.models import ExecutionContext
from jarvis.core.document.engine import DocumentIntelligenceEngine

class DocumentResolver(Resolver):
    """Resolves document intelligence queries using the DocumentIntelligenceEngine (PROD-0004)."""

    def __init__(self, doc_intel_engine: DocumentIntelligenceEngine) -> None:
        self.doc_intel_engine = doc_intel_engine

    def can_resolve(self, intent: Intent) -> bool:
        goal_lower = intent.goal.lower()
        keywords = [
            "what documents exist",
            "what documents are missing",
            "what should i upload", 
            "what can i do with this drawing",
            "what capabilities are available",
            "what is the current project state",
            "project state",
            "document relationship",
            "document completeness"
        ]
        return any(k in goal_lower for k in keywords) or (intent.semantics and intent.semantics.target == "Document")

    def resolve(self, intent: Intent, context: ExecutionContext) -> ResolutionResult:
        start_time = datetime.now()
        workspace_id = context.workspace_id
        
        analysis = self.doc_intel_engine.analyze_workspace(workspace_id)
        docs = analysis["documents"]
        relationships = analysis["relationships"]
        completeness = analysis["completeness"]
        recommendations = analysis["recommendations"]
        capabilities = analysis["capabilities"]
        
        goal_lower = intent.goal.lower()
        payload = ""
        evidence = []
        
        if "what documents exist" in goal_lower or "list" in goal_lower:
            if not docs:
                payload = "No documents found in this workspace context."
            else:
                lines = ["Documents registered in this project:"]
                for d in docs:
                    lines.append(f"- Name: {d.name} | Type: {d.classification.value} | Lifecycle: {d.lifecycle.value}")
                    evidence.append(d.name)
                payload = "\n".join(lines)
                
        elif "what documents are missing" in goal_lower:
            if not completeness.missing_types:
                payload = f"All expected document types are present. Completeness Score: {completeness.score * 100:.0f}%"
            else:
                lines = [
                    f"Checking Project Completeness for checklist '{completeness.project_type}':",
                    f"- Completeness Score: {completeness.score * 100:.0f}%",
                    "Missing Document Types (Gaps):"
                ]
                for missing in completeness.missing_types:
                    lines.append(f"  * {missing.value}")
                    evidence.append(missing.value)
                payload = "\n".join(lines)
                
        elif "what should i upload" in goal_lower or "upload next" in goal_lower or "upload first" in goal_lower:
            if not recommendations:
                payload = "Project is complete! No uploads required."
            else:
                lines = ["Recommended next actions (Deterministic Registry Checklist):"]
                for rec in recommendations:
                    if "missing" in rec.lower() or "upload" in rec.lower():
                        lines.append(f"- {rec}")
                        evidence.append(rec)
                payload = "\n".join(lines)
                
        elif "what can i do with this drawing" in goal_lower or "options" in goal_lower:
            lines = ["Drawing capabilities available in the platform:"]
            for cap_name, status in capabilities.items():
                if "PDFTakeoff" in cap_name or "RevisionTracking" in cap_name:
                    lines.append(f"- Capability: {cap_name} | Executable: {status['executable']}")
                    if not status['executable']:
                        lines.append(f"  * Missing required: {', '.join(status['missing_requirements'])}")
            payload = "\n".join(lines)
            
        elif "capabilities" in goal_lower:
            lines = ["Active Capability catalog requirements status:"]
            for cap_name, status in capabilities.items():
                lines.append(f"- {cap_name} | Executable: {status['executable']}")
                if not status['executable']:
                    lines.append(f"  * Missing required: {', '.join(status['missing_requirements'])}")
                if status['optional_provided']:
                    lines.append(f"  * Optional input detected: {', '.join(status['optional_provided'])}")
            payload = "\n".join(lines)
            
        else: # "current project state" or overall dashboard
            lines = [
                "==================================================",
                "       JARVIS ENGINEERING INTELLIGENCE DASHBOARD   ",
                "==================================================",
                f"Workspace Context ID: {workspace_id}",
                f"Completeness Level:   {completeness.score * 100:.0f}%",
                f"Active Documents:     {len(docs)} files",
                f"Links Detected:       {len(relationships)} relationships",
                "",
                "Document Registry Status:"
            ]
            for d in docs:
                lines.append(f"  - {d.name} ({d.classification.value}) [{d.lifecycle.value}]")
                evidence.append(d.name)
            
            if relationships:
                lines.append("\nTraceability Links:")
                for r in relationships:
                    lines.append(f"  * {r.from_doc_id} --({r.rel_type})--> {r.to_doc_id}")
            
            if recommendations:
                lines.append("\nRecommendations:")
                for rec in recommendations:
                    lines.append(f"  - {rec}")
            
            payload = "\n".join(lines)
            
        execution_time = (datetime.now() - start_time).total_seconds() * 1000
        return ResolutionResult(
            resolved=True,
            source="Workspace",
            confidence="High",
            payload=payload,
            evidence=evidence,
            grounded=True,
            execution_time_ms=execution_time,
            resolution_chain=["DocumentResolver"]
        )
