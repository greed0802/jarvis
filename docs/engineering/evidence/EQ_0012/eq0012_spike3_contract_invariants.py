#!/usr/bin/env python3
"""
EQ-0012 Spike 3: Contract Invariants

Purpose:
    Document invariants for each evidence field in the BOQ Intelligence Public Evidence Contract.
    
    Distinguishes between:
    - Structural Invariants: Shape, presence, type, ordering, immutability
    - Semantic Invariants: Meaning, determinism, provenance, boundary, reproducibility

Investigation Questions:
    1. What structural invariants apply to each evidence field?
    2. What semantic invariants apply to each evidence field?
    3. How should invariant violations be detected?
    4. How should invariant violations be handled?

Methodology:
    - Review Spike 1 evidence inventory
    - Analyze BOQIntelligenceResult implementation
    - Document invariants per field
    - Define verification approach
    - Define violation handling strategy

Evidence Sources:
    - docs/engineering/evidence/EQ_0012_Spike1_Evidence_Report_Current_Evidence_Inventory.md
    - src/jarvis/parsers/costx/boq_intelligence.py
    - Spike 2 versioning policy
"""

import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from pathlib import Path

@dataclass
class StructuralInvariant:
    """Structural invariant specification."""
    invariant_id: str
    category: str  # presence, type, ordering, immutability, shape
    description: str
    verification: str
    violation_impact: str

@dataclass
class SemanticInvariant:
    """Semantic invariant specification."""
    invariant_id: str
    category: str  # meaning, determinism, provenance, boundary, reproducibility
    description: str
    verification: str
    violation_impact: str

@dataclass
class FieldInvariants:
    """Complete invariant specification for an evidence field."""
    field_name: str
    field_type: str
    required: bool
    structural_invariants: List[StructuralInvariant]
    semantic_invariants: List[SemanticInvariant]
    cross_field_dependencies: List[str]

class ContractInvariantAnalyzer:
    """Analyzes and documents contract invariants."""
    
    def __init__(self):
        self.field_invariants: List[FieldInvariants] = []
    
    def analyze_increment_1_observation_fields(self):
        """Analyze Increment 1 observation evidence fields."""
        
        # row_classification
        self.field_invariants.append(FieldInvariants(
            field_name="row_classification",
            field_type="dict[str, int]",
            required=True,
            structural_invariants=[
                StructuralInvariant(
                    invariant_id="SI-RC-01",
                    category="presence",
                    description="Field must always exist and never be None",
                    verification="Assert field is not None",
                    violation_impact="MAJOR - consumer code expects field"
                ),
                StructuralInvariant(
                    invariant_id="SI-RC-02",
                    category="type",
                    description="Field must be dict[str, int]",
                    verification="Assert isinstance(field, dict) and all(isinstance(k, str) and isinstance(v, int) for k, v in field.items())",
                    violation_impact="MAJOR - type mismatch breaks consumers"
                ),
                StructuralInvariant(
                    invariant_id="SI-RC-03",
                    category="immutability",
                    description="Evidence is immutable after creation",
                    verification="Dataclass frozen=True",
                    violation_impact="MAJOR - consumers depend on immutability"
                ),
                StructuralInvariant(
                    invariant_id="SI-RC-04",
                    category="shape",
                    description="Keys are row type strings ('Head', 'Note', 'Section', 'Item', 'Other'), values are integer counts",
                    verification="Assert set(field.keys()) == {'Head', 'Note', 'Section', 'Item', 'Other'}",
                    violation_impact="MAJOR - shape contract violated"
                )
            ],
            semantic_invariants=[
                SemanticInvariant(
                    invariant_id="SE-RC-01",
                    category="determinism",
                    description="Same worksheet produces same classifications",
                    verification="Run analysis twice, compare results",
                    violation_impact="MAJOR - non-determinism breaks consumer trust"
                ),
                SemanticInvariant(
                    invariant_id="SE-RC-02",
                    category="boundary",
                    description="Classification is observation only - no decision language",
                    verification="Check RowType enum values against EQ-0011 forbidden terms",
                    violation_impact="MAJOR - engineering boundary violation"
                ),
                SemanticInvariant(
                    invariant_id="SE-RC-03",
                    category="provenance",
                    description="Classification traceable to Increment 1 engineering evidence",
                    verification="Assert classification logic matches EQ-0007 specification",
                    violation_impact="MAJOR - untraceable evidence"
                ),
                SemanticInvariant(
                    invariant_id="SE-RC-04",
                    category="reproducibility",
                    description="Classification reproducible from worksheet observation alone",
                    verification="Assert no external state dependencies",
                    violation_impact="MAJOR - non-reproducible evidence"
                )
            ],
            cross_field_dependencies=["section_statistics", "boq_statistics"]
        ))
        
        # section_statistics
        self.field_invariants.append(FieldInvariants(
            field_name="section_statistics",
            field_type="dict[str, dict[str, int]]",
            required=True,
            structural_invariants=[
                StructuralInvariant(
                    invariant_id="SI-SS-01",
                    category="presence",
                    description="Field must always exist and never be None",
                    verification="Assert field is not None",
                    violation_impact="MAJOR - consumer code expects field"
                ),
                StructuralInvariant(
                    invariant_id="SI-SS-02",
                    category="type",
                    description="Field must be dict[str, dict[str, int]]",
                    verification="Assert isinstance(field, dict) and all(isinstance(v, dict) for v in field.values())",
                    violation_impact="MAJOR - type mismatch breaks consumers"
                ),
                StructuralInvariant(
                    invariant_id="SI-SS-03",
                    category="shape",
                    description="Outer dict: section name → section stats dict. Inner dict keys: 'negative_qty', 'positive_qty' → integer counts",
                    verification="For each section dict, assert set(section.keys()).issubset({'negative_qty', 'positive_qty'})",
                    violation_impact="MAJOR - shape contract violated"
                ),
                StructuralInvariant(
                    invariant_id="SI-SS-04",
                    category="immutability",
                    description="Evidence is immutable after creation",
                    verification="Dataclass frozen=True",
                    violation_impact="MAJOR - consumers depend on immutability"
                )
            ],
            semantic_invariants=[
                SemanticInvariant(
                    invariant_id="SE-SS-01",
                    category="determinism",
                    description="Same worksheet produces same section statistics",
                    verification="Run analysis twice, compare results",
                    violation_impact="MAJOR - non-determinism breaks consumer trust"
                ),
                SemanticInvariant(
                    invariant_id="SE-SS-02",
                    category="meaning",
                    description="Section statistics represent structural observation only",
                    verification="Verify no decision semantics in keys or values",
                    violation_impact="MAJOR - engineering boundary violation"
                ),
                SemanticInvariant(
                    invariant_id="SE-SS-03",
                    category="provenance",
                    description="Statistics traceable to Increment 1 engineering evidence",
                    verification="Assert logic matches EQ-0007 specification",
                    violation_impact="MAJOR - untraceable evidence"
                )
            ],
            cross_field_dependencies=["row_classification", "boq_statistics"]
        ))
        
        # boq_statistics
        self.field_invariants.append(FieldInvariants(
            field_name="boq_statistics",
            field_type="dict[str, int | float]",
            required=True,
            structural_invariants=[
                StructuralInvariant(
                    invariant_id="SI-BS-01",
                    category="presence",
                    description="Field must always exist and never be None",
                    verification="Assert field is not None",
                    violation_impact="MAJOR - consumer code expects field"
                ),
                StructuralInvariant(
                    invariant_id="SI-BS-02",
                    category="type",
                    description="Field must be dict[str, int | float]",
                    verification="Assert isinstance(field, dict) and all(isinstance(v, (int, float)) for v in field.values())",
                    violation_impact="MAJOR - type mismatch breaks consumers"
                ),
                StructuralInvariant(
                    invariant_id="SI-BS-03",
                    category="shape",
                    description="Required keys: 'total_rows', 'code_rows', 'description_rows', 'quantity_rows', 'uom_rows', 'section_rows' → int or float values",
                    verification="Assert set(field.keys()) == {'total_rows', 'code_rows', 'description_rows', 'quantity_rows', 'uom_rows', 'section_rows'}",
                    violation_impact="MAJOR - shape contract violated"
                ),
                StructuralInvariant(
                    invariant_id="SI-BS-04",
                    category="immutability",
                    description="Evidence is immutable after creation",
                    verification="Dataclass frozen=True",
                    violation_impact="MAJOR - consumers depend on immutability"
                )
            ],
            semantic_invariants=[
                SemanticInvariant(
                    invariant_id="SE-BS-01",
                    category="determinism",
                    description="Same worksheet produces same BOQ statistics",
                    verification="Run analysis twice, compare results",
                    violation_impact="MAJOR - non-determinism breaks consumer trust"
                ),
                SemanticInvariant(
                    invariant_id="SE-BS-02",
                    category="meaning",
                    description="BOQ statistics represent quantitative observation only",
                    verification="Verify no decision semantics in keys or values",
                    violation_impact="MAJOR - engineering boundary violation"
                ),
                SemanticInvariant(
                    invariant_id="SE-BS-03",
                    category="provenance",
                    description="Statistics traceable to Increment 1 engineering evidence",
                    verification="Assert logic matches EQ-0007 specification",
                    violation_impact="MAJOR - untraceable evidence"
                )
            ],
            cross_field_dependencies=["row_classification", "section_statistics"]
        ))
        
        # known_anomalies
        self.field_invariants.append(FieldInvariants(
            field_name="known_anomalies",
            field_type="list[dict[str, int | str | float]]",
            required=True,
            structural_invariants=[
                StructuralInvariant(
                    invariant_id="SI-KA-01",
                    category="presence",
                    description="Field must always exist (may be empty list)",
                    verification="Assert field is not None",
                    violation_impact="MAJOR - consumer code expects field"
                ),
                StructuralInvariant(
                    invariant_id="SI-KA-02",
                    category="type",
                    description="Field must be list[dict[str, int | str | float]]",
                    verification="Assert isinstance(field, list) and all(isinstance(x, dict) for x in field)",
                    violation_impact="MAJOR - type mismatch breaks consumers"
                ),
                StructuralInvariant(
                    invariant_id="SI-KA-03",
                    category="shape",
                    description="Each anomaly dict contains keys: 'row_number' (int), 'code' (str), 'quantity' (float), 'section' (str)",
                    verification="For each anomaly, assert set(anomaly.keys()) == {'row_number', 'code', 'quantity', 'section'}",
                    violation_impact="MAJOR - shape contract violated"
                ),
                StructuralInvariant(
                    invariant_id="SI-KA-04",
                    category="immutability",
                    description="Evidence is immutable after creation",
                    verification="Dataclass frozen=True",
                    violation_impact="MAJOR - consumers depend on immutability"
                )
            ],
            semantic_invariants=[
                SemanticInvariant(
                    invariant_id="SE-KA-01",
                    category="determinism",
                    description="Same worksheet produces same anomaly list",
                    verification="Run analysis twice, compare results",
                    violation_impact="MAJOR - non-determinism breaks consumer trust"
                ),
                SemanticInvariant(
                    invariant_id="SE-KA-02",
                    category="boundary",
                    description="Anomalies describe observations only - no decision language",
                    verification="Check strings against EQ-0011 forbidden terms",
                    violation_impact="MAJOR - engineering boundary violation"
                ),
                SemanticInvariant(
                    invariant_id="SE-KA-03",
                    category="provenance",
                    description="Anomalies traceable to Increment 1 engineering evidence",
                    verification="Assert logic matches EQ-0007 specification",
                    violation_impact="MAJOR - untraceable evidence"
                )
            ],
            cross_field_dependencies=[]
        ))
    
    def analyze_increment_2_hierarchy_fields(self):
        """Analyze Increment 2 hierarchy evidence fields."""
        
        # hierarchy
        self.field_invariants.append(FieldInvariants(
            field_name="hierarchy",
            field_type="tuple[BOQHeaderNode, ...] | None",
            required=False,
            structural_invariants=[
                StructuralInvariant(
                    invariant_id="SI-H-01",
                    category="presence",
                    description="Field may be None (controlled by include_hierarchy parameter)",
                    verification="Assert field is None or isinstance(field, tuple)",
                    violation_impact="MINOR - optional field behavior"
                ),
                StructuralInvariant(
                    invariant_id="SI-H-02",
                    category="type",
                    description="When present, must be tuple[BOQHeaderNode, ...]",
                    verification="If not None, assert isinstance(field, tuple) and all(isinstance(n, BOQHeaderNode) for n in field)",
                    violation_impact="MAJOR - type mismatch breaks consumers"
                ),
                StructuralInvariant(
                    invariant_id="SI-H-03",
                    category="immutability",
                    description="Evidence is immutable after creation (tuple + frozen BOQHeaderNode)",
                    verification="Dataclass frozen=True, tuple immutable, BOQHeaderNode frozen",
                    violation_impact="MAJOR - consumers depend on immutability"
                )
            ],
            semantic_invariants=[
                SemanticInvariant(
                    invariant_id="SE-H-01",
                    category="determinism",
                    description="Same worksheet produces same hierarchy when include_hierarchy=True",
                    verification="Run analysis twice with same parameters, compare results",
                    violation_impact="MAJOR - non-determinism breaks consumer trust"
                ),
                SemanticInvariant(
                    invariant_id="SE-H-02",
                    category="meaning",
                    description="Hierarchy represents structural relationships only",
                    verification="Verify no decision semantics in node attributes",
                    violation_impact="MAJOR - engineering boundary violation"
                ),
                SemanticInvariant(
                    invariant_id="SE-H-03",
                    category="provenance",
                    description="Hierarchy traceable to Increment 2 engineering evidence",
                    verification="Assert logic matches increment 2 specification",
                    violation_impact="MAJOR - untraceable evidence"
                )
            ],
            cross_field_dependencies=["hierarchy_statistics"]
        ))
        
        # hierarchy_statistics
        self.field_invariants.append(FieldInvariants(
            field_name="hierarchy_statistics",
            field_type="dict[str, int | float] | None",
            required=False,
            structural_invariants=[
                StructuralInvariant(
                    invariant_id="SI-HS-01",
                    category="presence",
                    description="Field may be None (controlled by include_hierarchy parameter)",
                    verification="Assert field is None or isinstance(field, dict)",
                    violation_impact="MINOR - optional field behavior"
                ),
                StructuralInvariant(
                    invariant_id="SI-HS-02",
                    category="type",
                    description="When present, must be dict[str, int | float]",
                    verification="If not None, assert isinstance(field, dict) and all(isinstance(v, (int, float)) for v in field.values())",
                    violation_impact="MAJOR - type mismatch breaks consumers"
                ),
                StructuralInvariant(
                    invariant_id="SI-HS-03",
                    category="shape",
                    description="Required keys: 'total_headers', 'root_headers', 'depth_distribution', 'items_per_header_by_uom' → int or float values",
                    verification="If not None, assert set(field.keys()) == {'total_headers', 'root_headers', 'depth_distribution', 'items_per_header_by_uom'}",
                    violation_impact="MAJOR - shape contract violated"
                ),
                StructuralInvariant(
                    invariant_id="SI-HS-04",
                    category="immutability",
                    description="Evidence is immutable after creation",
                    verification="Dataclass frozen=True",
                    violation_impact="MAJOR - consumers depend on immutability"
                )
            ],
            semantic_invariants=[
                SemanticInvariant(
                    invariant_id="SE-HS-01",
                    category="determinism",
                    description="Same worksheet produces same hierarchy statistics when include_hierarchy=True",
                    verification="Run analysis twice with same parameters, compare results",
                    violation_impact="MAJOR - non-determinism breaks consumer trust"
                ),
                SemanticInvariant(
                    invariant_id="SE-HS-02",
                    category="meaning",
                    description="Statistics represent quantitative hierarchy observation only",
                    verification="Verify no decision semantics in keys or values",
                    violation_impact="MAJOR - engineering boundary violation"
                ),
                SemanticInvariant(
                    invariant_id="SE-HS-03",
                    category="provenance",
                    description="Statistics traceable to Increment 2 engineering evidence",
                    verification="Assert logic matches increment 2 specification",
                    violation_impact="MAJOR - untraceable evidence"
                )
            ],
            cross_field_dependencies=["hierarchy"]
        ))
    
    def analyze_increment_3_detection_fields(self):
        """Analyze Increment 3 detection evidence fields."""
        
        # detected_level_skips
        self.field_invariants.append(FieldInvariants(
            field_name="detected_level_skips",
            field_type="tuple[dict[str, int], ...] | None",
            required=False,
            structural_invariants=[
                StructuralInvariant(
                    invariant_id="SI-DLS-01",
                    category="presence",
                    description="Field may be None (controlled by include_detection parameter)",
                    verification="Assert field is None or isinstance(field, tuple)",
                    violation_impact="MINOR - optional field behavior"
                ),
                StructuralInvariant(
                    invariant_id="SI-DLS-02",
                    category="type",
                    description="When present, must be tuple[dict[str, int], ...]",
                    verification="If not None, assert isinstance(field, tuple) and all(isinstance(x, dict) for x in field)",
                    violation_impact="MAJOR - type mismatch breaks consumers"
                ),
                StructuralInvariant(
                    invariant_id="SI-DLS-03",
                    category="shape",
                    description="Each skip dict contains keys: 'parent_row_number', 'parent_level', 'child_row_number', 'child_level', 'skip_magnitude' → int values",
                    verification="For each skip, verify all keys present and all values are int",
                    violation_impact="MAJOR - shape contract violated"
                ),
                StructuralInvariant(
                    invariant_id="SI-DLS-04",
                    category="immutability",
                    description="Evidence is immutable after creation (tuple immutability)",
                    verification="Dataclass frozen=True, tuple immutable",
                    violation_impact="MAJOR - consumers depend on immutability"
                )
            ],
            semantic_invariants=[
                SemanticInvariant(
                    invariant_id="SE-DLS-01",
                    category="determinism",
                    description="Same worksheet produces same level skips when include_detection=True",
                    verification="Run analysis twice with same parameters, compare results",
                    violation_impact="MAJOR - non-determinism breaks consumer trust"
                ),
                SemanticInvariant(
                    invariant_id="SE-DLS-02",
                    category="boundary",
                    description="Detections describe patterns only - no decision language",
                    verification="Check field keys/values against EQ-0011 forbidden terms",
                    violation_impact="MAJOR - engineering boundary violation"
                ),
                SemanticInvariant(
                    invariant_id="SE-DLS-03",
                    category="provenance",
                    description="Detections traceable to Increment 3 engineering evidence",
                    verification="Assert logic matches increment 3 specification",
                    violation_impact="MAJOR - untraceable evidence"
                )
            ],
            cross_field_dependencies=["hierarchy"]
        ))
        
        # zero_quantity_items
        self.field_invariants.append(FieldInvariants(
            field_name="zero_quantity_items",
            field_type="tuple[dict[str, int | str | float | None], ...] | None",
            required=False,
            structural_invariants=[
                StructuralInvariant(
                    invariant_id="SI-ZQI-01",
                    category="presence",
                    description="Field may be None (controlled by include_detection parameter)",
                    verification="Assert field is None or isinstance(field, tuple)",
                    violation_impact="MINOR - optional field behavior"
                ),
                StructuralInvariant(
                    invariant_id="SI-ZQI-02",
                    category="type",
                    description="When present, must be tuple[dict[str, int | str | float | None], ...]",
                    verification="If not None, assert isinstance(field, tuple) and all(isinstance(x, dict) for x in field)",
                    violation_impact="MAJOR - type mismatch breaks consumers"
                ),
                StructuralInvariant(
                    invariant_id="SI-ZQI-03",
                    category="shape",
                    description="Each item dict contains keys: 'row_number', 'code', 'description', 'section', 'quantity', 'uom'",
                    verification="For each item, verify all keys present",
                    violation_impact="MAJOR - shape contract violated"
                ),
                StructuralInvariant(
                    invariant_id="SI-ZQI-04",
                    category="immutability",
                    description="Evidence is immutable after creation (tuple immutability)",
                    verification="Dataclass frozen=True, tuple immutable",
                    violation_impact="MAJOR - consumers depend on immutability"
                )
            ],
            semantic_invariants=[
                SemanticInvariant(
                    invariant_id="SE-ZQI-01",
                    category="determinism",
                    description="Same worksheet produces same zero quantity items when include_detection=True",
                    verification="Run analysis twice with same parameters, compare results",
                    violation_impact="MAJOR - non-determinism breaks consumer trust"
                ),
                SemanticInvariant(
                    invariant_id="SE-ZQI-02",
                    category="boundary",
                    description="Detections describe patterns only - no decision language",
                    verification="Check field keys/values against EQ-0011 forbidden terms",
                    violation_impact="MAJOR - engineering boundary violation"
                ),
                SemanticInvariant(
                    invariant_id="SE-ZQI-03",
                    category="provenance",
                    description="Detections traceable to Increment 3 engineering evidence",
                    verification="Assert logic matches increment 3 specification",
                    violation_impact="MAJOR - untraceable evidence"
                )
            ],
            cross_field_dependencies=["row_classification"]
        ))
        
        # structural_containment_findings
        self.field_invariants.append(FieldInvariants(
            field_name="structural_containment_findings",
            field_type="tuple[dict[str, int], ...] | None",
            required=False,
            structural_invariants=[
                StructuralInvariant(
                    invariant_id="SI-SCF-01",
                    category="presence",
                    description="Field may be None (controlled by include_detection parameter)",
                    verification="Assert field is None or isinstance(field, tuple)",
                    violation_impact="MINOR - optional field behavior"
                ),
                StructuralInvariant(
                    invariant_id="SI-SCF-02",
                    category="type",
                    description="When present, must be tuple[dict[str, int], ...]",
                    verification="If not None, assert isinstance(field, tuple) and all(isinstance(x, dict) for x in field)",
                    violation_impact="MAJOR - type mismatch breaks consumers"
                ),
                StructuralInvariant(
                    invariant_id="SI-SCF-03",
                    category="shape",
                    description="Each finding dict contains keys: 'parent_row_number', 'parent_level', 'child_row_number', 'child_level' → int values",
                    verification="For each finding, verify all keys present and all values are int",
                    violation_impact="MAJOR - shape contract violated"
                ),
                StructuralInvariant(
                    invariant_id="SI-SCF-04",
                    category="immutability",
                    description="Evidence is immutable after creation (tuple immutability)",
                    verification="Dataclass frozen=True, tuple immutable",
                    violation_impact="MAJOR - consumers depend on immutability"
                )
            ],
            semantic_invariants=[
                SemanticInvariant(
                    invariant_id="SE-SCF-01",
                    category="determinism",
                    description="Same worksheet produces same structural findings when include_detection=True",
                    verification="Run analysis twice with same parameters, compare results",
                    violation_impact="MAJOR - non-determinism breaks consumer trust"
                ),
                SemanticInvariant(
                    invariant_id="SE-SCF-02",
                    category="boundary",
                    description="Findings describe patterns only - no decision language",
                    verification="Check field keys/values against EQ-0011 forbidden terms",
                    violation_impact="MAJOR - engineering boundary violation"
                ),
                SemanticInvariant(
                    invariant_id="SE-SCF-03",
                    category="provenance",
                    description="Findings traceable to Increment 3 engineering evidence",
                    verification="Assert logic matches increment 3 specification",
                    violation_impact="MAJOR - untraceable evidence"
                )
            ],
            cross_field_dependencies=["hierarchy", "row_classification"]
        ))
        
        # completeness_findings
        self.field_invariants.append(FieldInvariants(
            field_name="completeness_findings",
            field_type="tuple[dict[str, int | str], ...] | None",
            required=False,
            structural_invariants=[
                StructuralInvariant(
                    invariant_id="SI-CF-01",
                    category="presence",
                    description="Field may be None (controlled by include_detection parameter)",
                    verification="Assert field is None or isinstance(field, tuple)",
                    violation_impact="MINOR - optional field behavior"
                ),
                StructuralInvariant(
                    invariant_id="SI-CF-02",
                    category="type",
                    description="When present, must be tuple[dict[str, int | str], ...]",
                    verification="If not None, assert isinstance(field, tuple) and all(isinstance(x, dict) for x in field)",
                    violation_impact="MAJOR - type mismatch breaks consumers"
                ),
                StructuralInvariant(
                    invariant_id="SI-CF-03",
                    category="shape",
                    description="Each finding dict contains keys: 'section' (str), 'item_count' (int)",
                    verification="For each finding, assert set(finding.keys()) == {'section', 'item_count'}",
                    violation_impact="MAJOR - shape contract violated"
                ),
                StructuralInvariant(
                    invariant_id="SI-CF-04",
                    category="immutability",
                    description="Evidence is immutable after creation (tuple immutability)",
                    verification="Dataclass frozen=True, tuple immutable",
                    violation_impact="MAJOR - consumers depend on immutability"
                )
            ],
            semantic_invariants=[
                SemanticInvariant(
                    invariant_id="SE-CF-01",
                    category="determinism",
                    description="Same worksheet produces same completeness findings when include_detection=True",
                    verification="Run analysis twice with same parameters, compare results",
                    violation_impact="MAJOR - non-determinism breaks consumer trust"
                ),
                SemanticInvariant(
                    invariant_id="SE-CF-02",
                    category="boundary",
                    description="Findings describe patterns only - no decision language",
                    verification="Check field keys/values against EQ-0011 forbidden terms",
                    violation_impact="MAJOR - engineering boundary violation"
                ),
                SemanticInvariant(
                    invariant_id="SE-CF-03",
                    category="provenance",
                    description="Findings traceable to Increment 3 engineering evidence",
                    verification="Assert logic matches increment 3 specification",
                    violation_impact="MAJOR - untraceable evidence"
                )
            ],
            cross_field_dependencies=["row_classification", "section_statistics"]
        ))
    
    def analyze_all_fields(self):
        """Analyze all evidence fields."""
        self.analyze_increment_1_observation_fields()
        self.analyze_increment_2_hierarchy_fields()
        self.analyze_increment_3_detection_fields()
    
    def define_verification_approach(self) -> Dict[str, any]:
        """Define how invariants should be verified."""
        return {
            "verification_strategy": {
                "structural_verification": {
                    "approach": "Static type checking + runtime assertions",
                    "tools": ["mypy", "pytest assertions", "dataclass validation"],
                    "frequency": "Every test run",
                    "scope": "All fields, all tests"
                },
                "semantic_verification": {
                    "approach": "Determinism tests + boundary tests + provenance tests",
                    "tools": ["pytest", "frozen engineering evidence", "EQ-0011 term checker"],
                    "frequency": "Every test run + regression suite",
                    "scope": "All fields, comprehensive test matrix"
                }
            },
            "verification_phases": {
                "phase_1_development": {
                    "description": "Verification during development",
                    "actions": [
                        "Type checker (mypy) on every file save",
                        "Unit tests on every commit",
                        "Determinism tests in CI pipeline"
                    ]
                },
                "phase_2_integration": {
                    "description": "Verification during integration",
                    "actions": [
                        "Full test suite execution",
                        "Historical fixture regression tests",
                        "Cross-field dependency validation"
                    ]
                },
                "phase_3_release": {
                    "description": "Verification before release",
                    "actions": [
                        "Complete evidence inventory validation",
                        "Provenance traceability check",
                        "Boundary compliance audit"
                    ]
                }
            }
        }
    
    def define_violation_handling(self) -> Dict[str, any]:
        """Define how invariant violations should be handled."""
        return {
            "violation_handling_policy": {
                "structural_violations": {
                    "detection": "Immediate - fail fast at analysis time",
                    "handling": "Raise InvariantViolationError with diagnostic details",
                    "recovery": "None - structural violations are fatal",
                    "consumer_impact": "Analysis fails, no evidence produced"
                },
                "semantic_violations": {
                    "detection": "Test-time detection via assertions",
                    "handling": "Raise InvariantViolationError with evidence trace",
                    "recovery": "None - semantic violations indicate implementation defect",
                    "consumer_impact": "No impact (caught in testing before release)"
                }
            },
            "error_reporting": {
                "required_details": [
                    "Invariant ID violated",
                    "Field name",
                    "Expected behavior",
                    "Actual behavior",
                    "Input that triggered violation",
                    "Engineering evidence reference"
                ],
                "format": "Structured error with full diagnostic context",
                "logging": "Error logged with full trace for debugging"
            },
            "governance": {
                "on_violation_discovery": [
                    "Create Engineering Question to investigate",
                    "Classify as defect or specification gap",
                    "If defect: fix implementation",
                    "If specification gap: update engineering evidence and contract",
                    "Add regression test",
                    "Update contract documentation if needed"
                ],
                "version_impact": {
                    "structural_fix": "PATCH if no behavior change, MAJOR if behavior change",
                    "semantic_fix": "PATCH if clarification, MAJOR if meaning change"
                }
            }
        }
    
    def generate_report(self) -> Dict[str, any]:
        """Generate complete invariant analysis report."""
        self.analyze_all_fields()
        
        report = {
            "investigation": "EQ-0012 Spike 3: Contract Invariants",
            "date": "2026-07-15",
            "summary": {
                "total_fields": len(self.field_invariants),
                "required_fields": sum(1 for f in self.field_invariants if f.required),
                "optional_fields": sum(1 for f in self.field_invariants if not f.required),
                "total_structural_invariants": sum(
                    len(f.structural_invariants) for f in self.field_invariants
                ),
                "total_semantic_invariants": sum(
                    len(f.semantic_invariants) for f in self.field_invariants
                )
            },
            "field_invariants": [
                {
                    "field_name": f.field_name,
                    "field_type": f.field_type,
                    "required": f.required,
                    "structural_invariants": [
                        {
                            "invariant_id": si.invariant_id,
                            "category": si.category,
                            "description": si.description,
                            "verification": si.verification,
                            "violation_impact": si.violation_impact
                        }
                        for si in f.structural_invariants
                    ],
                    "semantic_invariants": [
                        {
                            "invariant_id": si.invariant_id,
                            "category": si.category,
                            "description": si.description,
                            "verification": si.verification,
                            "violation_impact": si.violation_impact
                        }
                        for si in f.semantic_invariants
                    ],
                    "cross_field_dependencies": f.cross_field_dependencies
                }
                for f in self.field_invariants
            ],
            "verification_approach": self.define_verification_approach(),
            "violation_handling": self.define_violation_handling()
        }
        
        return report

def main():
    """Execute Spike 3 analysis."""
    print("=" * 80)
    print("EQ-0012 Spike 3: Contract Invariants Analysis")
    print("=" * 80)
    print()
    
    analyzer = ContractInvariantAnalyzer()
    report = analyzer.generate_report()
    
    # Print summary
    print(f"Investigation: {report['investigation']}")
    print(f"Date: {report['date']}")
    print()
    print("Summary:")
    print(f"  Total fields analyzed: {report['summary']['total_fields']}")
    print(f"  Required fields: {report['summary']['required_fields']}")
    print(f"  Optional fields: {report['summary']['optional_fields']}")
    print(f"  Total structural invariants: {report['summary']['total_structural_invariants']}")
    print(f"  Total semantic invariants: {report['summary']['total_semantic_invariants']}")
    print()
    
    # Print field-by-field breakdown
    print("Field Invariants:")
    print()
    for field in report['field_invariants']:
        print(f"  {field['field_name']} ({field['field_type']})")
        print(f"    Required: {field['required']}")
        print(f"    Structural invariants: {len(field['structural_invariants'])}")
        print(f"    Semantic invariants: {len(field['semantic_invariants'])}")
        if field['cross_field_dependencies']:
            print(f"    Dependencies: {', '.join(field['cross_field_dependencies'])}")
        print()
    
    # Print invariant categories
    structural_categories = {}
    semantic_categories = {}
    
    for field in report['field_invariants']:
        for si in field['structural_invariants']:
            structural_categories[si['category']] = structural_categories.get(si['category'], 0) + 1
        for si in field['semantic_invariants']:
            semantic_categories[si['category']] = semantic_categories.get(si['category'], 0) + 1
    
    print("Structural Invariant Categories:")
    for category, count in sorted(structural_categories.items()):
        print(f"  {category}: {count}")
    print()
    
    print("Semantic Invariant Categories:")
    for category, count in sorted(semantic_categories.items()):
        print(f"  {category}: {count}")
    print()
    
    # Save report
    output_path = Path("data/reports/eq0012_spike3_contract_invariants.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"Full report saved to: {output_path}")
    print()
    print("=" * 80)
    print("Analysis Complete")
    print("=" * 80)

if __name__ == "__main__":
    main()
