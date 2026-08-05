# -*- coding: utf-8 -*-
import os
import re
import openpyxl
from typing import List, Dict, Any, Optional
from jarvis.domain.document.models import (
    Document, DocumentClassification, DocumentLifecycle, DocumentMetadata,
    DocumentRelationship, DocumentCompleteness, CapabilityRequirement
)
from jarvis.core.artifact.repository import ArtifactRepository

class DocumentRegistry:
    """Stores and catalogs document entities."""
    def __init__(self) -> None:
        self._documents: Dict[str, Document] = {}

    def register(self, doc: Document) -> None:
        self._documents[doc.document_id] = doc

    def get(self, doc_id: str) -> Optional[Document]:
        return self._documents.get(doc_id)

    def list_by_workspace(self, workspace_id: str) -> List[Document]:
        return [d for d in self._documents.values() if d.workspace_id == workspace_id]


class ClassificationEngine:
    """Executes evidence-based document classification with deterministic precedence."""
    
    def classify(self, filename: str, file_path: str, ext: str) -> DocumentClassification:
        # Precedence 1: Extension
        ext_lower = ext.lower()
        if ext_lower in [".zip", ".tar", ".gz", ".7z"]:
            return DocumentClassification.ARCHIVE
        if ext_lower in [".eml", ".msg"]:
            return DocumentClassification.EMAIL
        if ext_lower in [".png", ".jpg", ".jpeg"]:
            return DocumentClassification.PHOTO if "site" in filename.lower() or "photo" in filename.lower() else DocumentClassification.IMAGE

        # Precedence 2: Parser Signature / Workbook Structure (Excel structure signature)
        if ext_lower in [".xlsx", ".xls"] and os.path.exists(file_path):
            try:
                wb = openpyxl.load_workbook(file_path, read_only=True)
                sheets = wb.sheetnames
                wb.close()
                
                # Check for CostX BOQ sheets or structure
                if "README" in sheets and "Routes" in sheets and "Decisions" in sheets:
                    return DocumentClassification.BOQ  # Source Of Truth
                if any(s in sheets for s in ["OMISSION", "ADDITION", "Takeoff", "BOQ", "Quantities"]):
                    return DocumentClassification.BOQ
                if any("checklist" in s.lower() or "check" in s.lower() for s in sheets):
                    return DocumentClassification.CHECKLIST
                return DocumentClassification.SPREADSHEET
            except Exception:
                pass  # Fall back if file is locked or cannot be read

        # Precedence 3: Filename patterns
        name_lower = filename.lower()
        
        # Check drawings (Precedence 3 / Filename markers)
        if ext_lower in [".dwg", ".dxf", ".pdf"] or "drawing" in name_lower:
            if re.search(r'\b(a|ar)-\d+', name_lower) or "architectural" in name_lower or "arch" in name_lower:
                return DocumentClassification.ARCHARCHITECTURAL_DRAWING if False else DocumentClassification.ARCHITECTURAL_DRAWING
            if re.search(r'\b(s|st)-\d+', name_lower) or "structural" in name_lower or "struct" in name_lower:
                return DocumentClassification.STRUCTURAL_DRAWING
            if re.search(r'\b(c|ci)-\d+', name_lower) or "civil" in name_lower or "civ" in name_lower:
                return DocumentClassification.CIVIL_DRAWING
            if re.search(r'\b(m|e|h|f|services)-\d+', name_lower) or any(k in name_lower for k in ["mech", "elec", "plumb", "services", "fire"]):
                return DocumentClassification.SERVICES_DRAWING

        # Specifications
        if "spec" in name_lower or "specification" in name_lower:
            return DocumentClassification.SPECIFICATION

        # BOQ
        if "boq" in name_lower or "bill of quantities" in name_lower:
            return DocumentClassification.BOQ

        # Checklist
        if "checklist" in name_lower or "checks" in name_lower:
            return DocumentClassification.CHECKLIST

        # Schedules / Programs
        if "schedule" in name_lower or "program" in name_lower:
            return DocumentClassification.SCHEDULE

        # Calculations
        if "calc" in name_lower or "calculation" in name_lower:
            return DocumentClassification.CALCULATION

        # Reports
        if "report" in name_lower or "summary" in name_lower:
            return DocumentClassification.REPORT

        return DocumentClassification.UNKNOWN

class RelationshipEngine:
    """Evaluates and links document relationships based on codes, versioning, and rules."""
    
    def _extract_base_name(self, filename: str) -> str:
        # e.g., A-01-RevB -> a-01, structural_layout_v2 -> structural_layout
        name = filename.lower()
        name = re.sub(r'[-_]rev[a-z0-9]+', '', name)
        name = re.sub(r'[-_]v\d+', '', name)
        name = os.path.splitext(name)[0]
        return name

    def detect_relationships(self, docs: List[Document]) -> List[DocumentRelationship]:
        relationships = []
        bases: Dict[str, List[Document]] = {}
        for doc in docs:
            base = self._extract_base_name(doc.name)
            bases.setdefault(base, []).append(doc)
            
        for base, group in bases.items():
            if len(group) > 1:
                def get_sort_key(d: Document):
                    nums = re.findall(r'v(\d+)|rev([a-z0-9]+)', d.name.lower())
                    if nums:
                        return str(nums[-1])
                    return d.name.lower()
                sorted_group = sorted(group, key=get_sort_key)
                for i in range(len(sorted_group) - 1):
                    relationships.append(DocumentRelationship(
                        from_doc_id=sorted_group[i+1].document_id,
                        to_doc_id=sorted_group[i].document_id,
                        rel_type="supersedes"
                    ))

        specifications = [d for d in docs if d.classification == DocumentClassification.SPECIFICATION]
        drawings = [d for d in docs if d.classification in [
            DocumentClassification.ARCHITECTURAL_DRAWING, DocumentClassification.STRUCTURAL_DRAWING,
            DocumentClassification.CIVIL_DRAWING, DocumentClassification.SERVICES_DRAWING
        ]]
        boqs = [d for d in docs if d.classification == DocumentClassification.BOQ]
        checklists = [d for d in docs if d.classification == DocumentClassification.CHECKLIST]

        for spec in specifications:
            for dwg in drawings:
                relationships.append(DocumentRelationship(from_doc_id=spec.document_id, to_doc_id=dwg.document_id, rel_type="governs"))
        for dwg in drawings:
            for boq in boqs:
                relationships.append(DocumentRelationship(from_doc_id=dwg.document_id, to_doc_id=boq.document_id, rel_type="supports"))
        for chk in checklists:
            for boq in boqs:
                relationships.append(DocumentRelationship(from_doc_id=chk.document_id, to_doc_id=boq.document_id, rel_type="validates"))
        return relationships


class CompletenessEngine:
    """Evaluates project document completeness scoring."""
    
    def evaluate(self, docs: List[Document], project_type: str = "General") -> DocumentCompleteness:
        expected = [
            DocumentClassification.ARCHITECTURAL_DRAWING,
            DocumentClassification.STRUCTURAL_DRAWING,
            DocumentClassification.SPECIFICATION,
            DocumentClassification.BOQ,
            DocumentClassification.CHECKLIST
        ]
        actual_set = {d.classification for d in docs if d.classification in expected}
        actual_list = list(actual_set)
        missing = [t for t in expected if t not in actual_set]
        score = len(actual_list) / len(expected) if expected else 1.0
        return DocumentCompleteness(
            project_type=project_type, expected_types=expected, actual_types=actual_list, missing_types=missing, score=score
        )

class RecommendationEngine:
    """Computes deterministic engineering recommendations based on manifest items."""
    
    def generate(self, completeness: DocumentCompleteness, docs: List[Document], relationships: List[DocumentRelationship]) -> List[str]:
        recommendations = []
        for missing_type in completeness.missing_types:
            if missing_type == DocumentClassification.STRUCTURAL_DRAWING:
                recommendations.append("Missing Structural Drawings: Please upload structural layout/detail drawings (e.g., S-01.dwg) to verify concrete and steel quantities.")
            elif missing_type == DocumentClassification.ARCHITECTURAL_DRAWING:
                recommendations.append("Missing Architectural Drawings: Please upload architectural layout drawings (e.g., A-01.dwg) to verify wall and door quantities.")
            elif missing_type == DocumentClassification.SPECIFICATION:
                recommendations.append("Missing Specification: Please upload project specification document to align materials, tolerances, and quality requirements with takeoff items.")
            elif missing_type == DocumentClassification.BOQ:
                recommendations.append("Missing Bill of Quantities (BOQ): Please upload BOQ spreadsheet or CostX workbook to enable quantity takeoff validation.")
            elif missing_type == DocumentClassification.CHECKLIST:
                recommendations.append("Missing QA Checklist: Please upload takeoff checklist to validate BOQ items and verification gates.")

        has_boq = any(d.classification == DocumentClassification.BOQ for d in docs)
        has_checklist = any(d.classification == DocumentClassification.CHECKLIST for d in docs)
        
        if has_boq:
            recommendations.append("BOQ Uploaded: Recommend running 'ask what files do you support' or invoke BOQ Intelligence to validate quantities.")
        if has_checklist:
            recommendations.append("Checklist Inputted: Recommend running 'verify' or invoking validation capability.")

        supersedes_rels = [r for r in relationships if r.rel_type == "supersedes"]
        for rel in supersedes_rels:
            from_doc = next((d for d in docs if d.document_id == rel.from_doc_id), None)
            to_doc = next((d for d in docs if d.document_id == rel.to_doc_id), None)
            if from_doc and to_doc:
                recommendations.append(f"Outdated Revision detected: Document '{to_doc.name}' has been superseded by newer revision '{from_doc.name}'. Recommend replacing it in active task assignments.")
        return recommendations

class DocumentIntelligenceEngine:
    """Central orchestrator for the Document Intelligence Layer (PROD-0004)."""
    
    def __init__(self, artifact_repo: ArtifactRepository) -> None:
        self.artifact_repo = artifact_repo
        self.registry = DocumentRegistry()
        self.classification_engine = ClassificationEngine()
        self.relationship_engine = RelationshipEngine()
        self.completeness_engine = CompletenessEngine()
        self.recommendation_engine = RecommendationEngine()
        
        self.capability_reqs = [
            CapabilityRequirement(
                capability_name="BOQIntelligence",
                required_types=[DocumentClassification.BOQ],
                optional_types=[DocumentClassification.CHECKLIST, DocumentClassification.SPECIFICATION]
            ),
            CapabilityRequirement(
                capability_name="PDFTakeoff",
                required_types=[DocumentClassification.ARCHITECTURAL_DRAWING],
                optional_types=[DocumentClassification.SPECIFICATION]
            ),
            CapabilityRequirement(
                capability_name="RevisionTracking",
                required_types=[DocumentClassification.STRUCTURAL_DRAWING, DocumentClassification.ARCHITECTURAL_DRAWING],
                optional_types=[]
            )
        ]

    def _sync_registry(self, workspace_id: str) -> List[Document]:
        """Reads physical artifacts for a workspace, runs classification elements, and registers docs."""
        artifacts = []
        if hasattr(self.artifact_repo, "list_artifacts"):
            try:
                artifacts = self.artifact_repo.list_artifacts(workspace_id)
            except Exception:
                pass
        if not artifacts and hasattr(self.artifact_repo, "_artifacts"):
            artifacts = [art for art in self.artifact_repo._artifacts.values() if art.workspace_id == workspace_id]
            
        docs = []
        for art in artifacts:
            doc_id = f"doc-{art.artifact_id}"
            
            size = 0
            hash_val = ""
            created_by = "shell-user"
            custom_props = {}
            if art.versions:
                latest_ver = art.versions[-1]
                size = latest_ver.metadata.file_size_bytes
                hash_val = latest_ver.metadata.content_hash
                created_by = latest_ver.metadata.created_by
                custom_props = latest_ver.metadata.custom_properties
            
            filename = art.name
            _, ext = os.path.splitext(filename)
            class_type = self.classification_engine.classify(filename, file_path=filename, ext=ext)
            
            lifecycle = DocumentLifecycle.UPLOADED
            if hash_val:
                lifecycle = DocumentLifecycle.REGISTERED
            if class_type != DocumentClassification.UNKNOWN:
                lifecycle = DocumentLifecycle.CLASSIFIED
            if ext.lower() in [".xlsx", ".xls", ".csv"] and class_type == DocumentClassification.BOQ:
                lifecycle = DocumentLifecycle.PARSED
            
            metadata = DocumentMetadata(
                file_path=filename,
                extension=ext,
                file_size_bytes=size,
                content_hash=hash_val,
                workspace_context=workspace_id,
                custom_properties=custom_props
            )
            
            doc = Document(
                document_id=doc_id,
                workspace_id=workspace_id,
                name=filename,
                classification=class_type,
                lifecycle=lifecycle,
                metadata=metadata
            )
            self.registry.register(doc)
            docs.append(doc)
            
        return docs

    def analyze_workspace(self, workspace_id: str) -> Dict[str, Any]:
        """Perform recursive verification, links detection, completeness scoring, and recommendations build."""
        docs = self._sync_registry(workspace_id)
        relationships = self.relationship_engine.detect_relationships(docs)
        for doc in docs:
            doc.relationships = [r for r in relationships if r.from_doc_id == doc.document_id or r.to_doc_id == doc.document_id]
            
        completeness = self.completeness_engine.evaluate(docs)
        recommendations = self.recommendation_engine.generate(completeness, docs, relationships)
        for doc in docs:
            doc.recommendations = [rec for rec in recommendations if doc.name.lower() in rec.lower()]

        capability_statuses = {}
        for req in self.capability_reqs:
            has_required = all(any(d.classification == req_type for d in docs) for req_type in req.required_types)
            missing_reqs = [t.value for t in req.required_types if not any(d.classification == t for d in docs)]
            capability_statuses[req.capability_name] = {
                "executable": has_required,
                "missing_requirements": missing_reqs,
                "optional_provided": [t.value for t in req.optional_types if any(d.classification == t for d in docs)]
            }
            
        return {
            "documents": docs,
            "relationships": relationships,
            "completeness": completeness,
            "recommendations": recommendations,
            "capabilities": capability_statuses
        }

