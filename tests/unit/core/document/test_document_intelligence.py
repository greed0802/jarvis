import pytest
import os
from datetime import datetime
from jarvis.domain.document.models import (
    Document, DocumentClassification, DocumentLifecycle, DocumentMetadata,
    DocumentRelationship, DocumentCompleteness, CapabilityRequirement
)
from jarvis.core.document.engine import (
    ClassificationEngine, RelationshipEngine, CompletenessEngine,
    RecommendationEngine, DocumentIntelligenceEngine
)
from jarvis.core.artifact.models import Artifact, ArtifactVersion, ArtifactMetadata
from jarvis.core.artifact.repository import ArtifactRepository

def test_document_classification():
    engine = ClassificationEngine()
    
    # Test extension classification
    assert engine.classify("archive.zip", "archive.zip", ".zip") == DocumentClassification.ARCHIVE
    assert engine.classify("email.eml", "email.eml", ".eml") == DocumentClassification.EMAIL

    # Test filename keywords mapping
    assert engine.classify("a-01.dwg", "a-01.dwg", ".dwg") == DocumentClassification.ARCHITECTURAL_DRAWING
    assert engine.classify("architectural_layout.pdf", "architectural_layout.pdf", ".pdf") == DocumentClassification.ARCHITECTURAL_DRAWING
    assert engine.classify("S-203.dwg", "S-203.dwg", ".dwg") == DocumentClassification.STRUCTURAL_DRAWING
    assert engine.classify("structural_detail.dwg", "structural_detail.dwg", ".dwg") == DocumentClassification.STRUCTURAL_DRAWING
    
    assert engine.classify("c-01.dwg", "c-01.dwg", ".dwg") == DocumentClassification.CIVIL_DRAWING
    assert engine.classify("mech_services.dwg", "mech_services.dwg", ".dwg") == DocumentClassification.SERVICES_DRAWING
    assert engine.classify("project_specs.pdf", "project_specs.pdf", ".pdf") == DocumentClassification.SPECIFICATION
    assert engine.classify("estimate_boq.csv", "estimate_boq.csv", ".csv") == DocumentClassification.BOQ
    assert engine.classify("takeoff_checklist.xlsx", "takeoff_checklist.xlsx", ".xlsx") == DocumentClassification.CHECKLIST
    assert engine.classify("construction_program.xlsx", "construction_program.xlsx", ".xlsx") == DocumentClassification.SCHEDULE
    assert engine.classify("reinforcement_calc.xlsx", "reinforcement_calc.xlsx", ".xlsx") == DocumentClassification.CALCULATION
    assert engine.classify("site_photo.png", "site_photo.png", ".png") == DocumentClassification.PHOTO
    assert engine.classify("progress_report.pdf", "progress_report.pdf", ".pdf") == DocumentClassification.REPORT
    
def test_document_relationship_engine():
    engine = RelationshipEngine()
    
    # Setup mock documents
    m1 = DocumentMetadata("A-01-RevA.dwg", ".dwg", 100, "hash1", "ws1")
    d1 = Document("doc-1", "ws1", "A-01-RevA.dwg", DocumentClassification.ARCHITECTURAL_DRAWING, DocumentLifecycle.UPLOADED, m1)
    
    m2 = DocumentMetadata("A-01-RevB.dwg", ".dwg", 120, "hash2", "ws1")
    d2 = Document("doc-2", "ws1", "A-01-RevB.dwg", DocumentClassification.ARCHITECTURAL_DRAWING, DocumentLifecycle.UPLOADED, m2)
    
    m3 = DocumentMetadata("spec.pdf", ".pdf", 50, "hash3", "ws1")
    d3 = Document("doc-3", "ws1", "spec.pdf", DocumentClassification.SPECIFICATION, DocumentLifecycle.UPLOADED, m3)
    
    m4 = DocumentMetadata("boq.xlsx", ".xlsx", 200, "hash4", "ws1")
    d4 = Document("doc-4", "ws1", "boq.xlsx", DocumentClassification.BOQ, DocumentLifecycle.UPLOADED, m4)
    
    m5 = DocumentMetadata("checklist.xlsx", ".xlsx", 30, "hash5", "ws1")
    d5 = Document("doc-5", "ws1", "checklist.xlsx", DocumentClassification.CHECKLIST, DocumentLifecycle.UPLOADED, m5)
    
    docs = [d1, d2, d3, d4, d5]
    relationships = engine.detect_relationships(docs)
    
    # Assertions
    types = [r.rel_type for r in relationships]
    assert "supersedes" in types
    assert "governs" in types
    assert "supports" in types
    assert "validates" in types
    
def test_completeness_and_recommendations():
    c_engine = CompletenessEngine()
    r_engine = RecommendationEngine()
    
    # Setup expected types
    m1 = DocumentMetadata("A-01.dwg", ".dwg", 100, "hash1", "ws1")
    d1 = Document("doc-1", "ws1", "A-01.dwg", DocumentClassification.ARCHITECTURAL_DRAWING, DocumentLifecycle.UPLOADED, m1)
    
    m2 = DocumentMetadata("boq.xlsx", ".xlsx", 200, "hash2", "ws1")
    d2 = Document("doc-2", "ws1", "boq.xlsx", DocumentClassification.BOQ, DocumentLifecycle.UPLOADED, m2)
    
    docs = [d1, d2]
    completeness = c_engine.evaluate(docs)
    
    assert completeness.score == 0.4
    assert DocumentClassification.STRUCTURAL_DRAWING in completeness.missing_types
    assert DocumentClassification.SPECIFICATION in completeness.missing_types
    assert DocumentClassification.CHECKLIST in completeness.missing_types
    
    recs = r_engine.generate(completeness, docs, [])
    assert any("Missing Structural Drawings" in r for r in recs)
    assert any("Missing Specification" in r for r in recs)
    assert any("Missing QA Checklist" in r for r in recs)
    assert any("BOQ Uploaded" in r for r in recs)
