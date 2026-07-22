"""
EQ-0011 Spike 2: Evidence vs Assessment Decomposition

Objective:
For each of the four Domain Dependent capabilities (V-003, V-004, V-005, SEM-003),
decompose into:
1. Deterministic evidence obtainable from BOQRow + reconstructed hierarchy
2. Assessment required beyond that evidence
3. Whether assessment could become semantically deterministic or remains professional judgment

This spike produces evidence only. No architecture, engines, or abstractions.
Every conclusion must be traceable to EQ-0010, Domain Knowledge Layer, or production fixture.

Authority: EQ-0011 BOQ Semantic Intelligence Boundary
Governance: Engineering_Governance.md v1.0
Principle: Evidence Before Abstraction
"""

import json
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Dict, List

@dataclass(frozen=True)
class EvidenceComponent:
    """Deterministic evidence obtainable from structure."""
    capability: str
    evidence_description: str
    data_source: str
    computation: str
    example_from_fixture: str
    traceability: str

@dataclass(frozen=True)
class AssessmentComponent:
    """Assessment required beyond structural evidence."""
    capability: str
    assessment_description: str
    why_not_deterministic: str
    context_required: str
    could_formalize: str  # 'yes_with_rules', 'no_requires_judgment'
    formalization_prerequisite: str
    traceability: str

@dataclass(frozen=True)
class CapabilityDecomposition:
    """Complete decomposition of one capability."""
    capability_id: str
    capability_name: str
    evidence: EvidenceComponent
    assessment: AssessmentComponent
    boundary_statement: str

def decompose_v003() -> CapabilityDecomposition:
    """
    Decompose V-003: Level Progression Validation
    
    Evidence Source: EQ-0010 Spike 5 (12 skip violations detected)
    Domain Source: docs/domain/02_BOQ_Structure.md (Valid Hierarchy Patterns)
    """
    
    evidence = EvidenceComponent(
        capability="V-003",
        evidence_description="Level skip detection: identify when child level > parent level + 1",
        data_source="BOQRow.uom field + reconstructed hierarchy parent relationships",
        computation="For each header: extract level from UOM (Head1→1, Head2→2, etc.), compare child_level to parent_level, flag if gap > 1",
        example_from_fixture="Row 1661: Head3 under Head1 (skip=2), Rows 5709-5745: 7× Head4 under Head2 (skip=2)",
        traceability="EQ-0010 Spike 5: 12 skip violations detected deterministically"
    )
    
    assessment = AssessmentComponent(
        capability="V-003",
        assessment_description="Determine whether detected skip is legitimate organizational pattern or structural error",
        why_not_deterministic="Domain rule states levels 'should' progress sequentially but allows 'additional subdivision as required by project complexity'",
        context_required="Understanding of: (1) project organizational requirements, (2) whether skip serves legitimate purpose, (3) QS office standards for this project type",
        could_formalize="no_requires_judgment",
        formalization_prerequisite="Would require: (1) project-specific organizational rules, (2) client-specific hierarchy standards, (3) definition of 'legitimate' for each context. These vary per project and cannot be pre-formalized.",
        traceability="Domain Layer: 'Hierarchy Level N: Additional subdivision levels as required by project complexity' — 'as required' signals judgment"
    )
    
    boundary = (
        "Evidence: Skip detection is Structurally Deterministic (gap computation over hierarchy). "
        "Assessment: Skip legitimacy requires Professional Judgment (project-specific context)."
    )
    
    return CapabilityDecomposition("V-003", "Level Progression Validation", evidence, assessment, boundary)

def decompose_sem003() -> CapabilityDecomposition:
    """
    Decompose SEM-003: Items Always Quantify
    
    Evidence Source: EQ-0010 Spike 5 (5 zero-quantity items detected)
    Domain Source: docs/domain/02_BOQ_Structure.md (SEM-003 rule)
    """
    
    evidence = EvidenceComponent(
        capability="SEM-003",
        evidence_description="Zero-quantity detection: identify items where quantity field == 0",
        data_source="BOQRow.quantity field for rows where row_type == 'Item'",
        computation="For each Item row: check if quantity == 0.0, flag if true",
        example_from_fixture="Rows 5698, 6088, 6091, 6130, 6133: all have quantity=0.0",
        traceability="EQ-0010 Spike 5: 5 zero-quantity items detected deterministically"
    )
    
    assessment = AssessmentComponent(
        capability="SEM-003",
        assessment_description="Determine whether zero quantity is data entry error, incomplete takeoff, or legitimate placeholder",
        why_not_deterministic="Domain rule states items 'always' quantify but zero-quantity items exist in production. Disposition depends on QS intent and project stage.",
        context_required="Understanding of: (1) whether item is placeholder for future measurement, (2) whether takeoff is complete, (3) whether zero is intentional (e.g., omission item)",
        could_formalize="no_requires_judgment",
        formalization_prerequisite="Would require: (1) project stage tracking (draft vs final), (2) QS intent capture (placeholder vs error), (3) omission/addition context. These are project-state dependent and require QS interpretation.",
        traceability="Domain Layer: 'SEM-003: Items must have quantity and UOM' — production evidence shows 5 zero-quantity items; rule cannot be absolute without context"
    )
    
    boundary = (
        "Evidence: Zero-quantity detection is Structurally Deterministic (field value comparison). "
        "Assessment: Zero-quantity acceptability requires Professional Judgment (QS intent and project state)."
    )
    
    return CapabilityDecomposition("SEM-003", "Items Always Quantify", evidence, assessment, boundary)

def decompose_v004() -> CapabilityDecomposition:
    """
    Decompose V-004: Scope Containment
    
    Evidence Source: EQ-0010 Spike 5 (parent-level consistency checked)
    Domain Source: docs/domain/02_BOQ_Structure.md (Hierarchy semantic rules)
    """
    
    evidence = EvidenceComponent(
        capability="V-004",
        evidence_description="Parent-level consistency: verify child_level <= parent_level (structural containment)",
        data_source="Reconstructed hierarchy with level assignments",
        computation="For each parent-child pair: compare levels, flag if child_level > parent_level (structural inversion)",
        example_from_fixture="EQ-0010 Spike 5: 0 structural inversions detected (all parent-level relationships consistent)",
        traceability="EQ-0010 Spike 5: Parent-level consistency classified as Derivable"
    )
    
    assessment = AssessmentComponent(
        capability="V-004",
        assessment_description="Determine whether child work scope semantically fits within parent scope (semantic containment)",
        why_not_deterministic="Structural containment ensures level consistency but not scope alignment. Requires understanding what each header represents, not just its level.",
        context_required="Understanding of: (1) semantic meaning of parent header, (2) semantic meaning of child header, (3) whether child scope is subset of parent scope",
        could_formalize="yes_with_rules",
        formalization_prerequisite="Would require: (1) explicit scope definitions for standard headers (e.g., 'SUBSTRUCTURE' contains foundation work), (2) scope taxonomy (trade-based, location-based, element-based), (3) containment rules (e.g., 'Concrete Work' contains 'Reinforcement'). These could be formalized as Semantic Rules for standard BOQ patterns.",
        traceability="Domain Layer: 'Hierarchy - Semantic Inheritance: Child elements inherit meaning from parents' — requires understanding meaning, not just observing structure"
    )
    
    boundary = (
        "Evidence: Parent-level consistency is Structurally Deterministic (already confirmed in EQ-0010). "
        "Assessment: Semantic scope containment could become Semantically Deterministic with formalized scope rules, "
        "otherwise requires Professional Judgment for non-standard structures."
    )
    
    return CapabilityDecomposition("V-004", "Scope Containment", evidence, assessment, boundary)

def decompose_v005() -> CapabilityDecomposition:
    """
    Decompose V-005: Completeness
    
    Evidence Source: EQ-0010 Spike 5 (section-has-items checked)
    Domain Source: docs/domain/02_BOQ_Structure.md (Completeness definition)
    """
    
    evidence = EvidenceComponent(
        capability="V-005",
        evidence_description="Section-has-items: verify each section contains at least one measurable item",
        data_source="BOQRow section field + row_type field",
        computation="Group rows by section, count Item rows per section, flag sections with 0 items",
        example_from_fixture="EQ-0010 Spike 5: All sections contain at least one Item row (basic completeness satisfied)",
        traceability="EQ-0010 Spike 5: Section-has-measurable-items classified as Derivable"
    )
    
    assessment = AssessmentComponent(
        capability="V-005",
        assessment_description="Determine whether all required work for project scope is represented (full QS completeness)",
        why_not_deterministic="Structural completeness (section has items) does not prove scope completeness (all required work present). Requires knowledge of project requirements.",
        context_required="Understanding of: (1) project scope and deliverables, (2) work breakdown structure requirements, (3) trade/element coverage expectations, (4) client-specific completeness criteria",
        could_formalize="yes_with_rules",
        formalization_prerequisite="Would require: (1) project scope definition (deliverables, trades, elements), (2) completeness checklist per project type, (3) required work packages mapped to BOQ structure. These could be formalized as Semantic Rules for standard project types, but vary per project and client.",
        traceability="Domain Layer: 'Completeness: No missing work, all required measurable work represented' — 'required work' is project-specific and cannot be determined from BOQ structure alone"
    )
    
    boundary = (
        "Evidence: Section-has-items is Structurally Deterministic (already confirmed in EQ-0010). "
        "Assessment: Full completeness could become Semantically Deterministic with project scope definitions, "
        "otherwise requires Professional Judgment based on project knowledge."
    )
    
    return CapabilityDecomposition("V-005", "Completeness", evidence, assessment, boundary)

def analyze_formalization_potential() -> Dict[str, any]:
    """
    Analyze which assessments could become semantically deterministic.
    
    Evidence-only analysis — no architecture proposals.
    """
    
    return {
        "potentially_formalizable": {
            "V-004": {
                "capability": "Scope Containment (semantic)",
                "evidence": "Parent-level consistency already deterministic",
                "formalization_path": "Define scope taxonomy + containment rules for standard BOQ patterns",
                "prerequisite": "Explicit scope definitions and containment mappings",
                "caveat": "Non-standard organizational patterns still require judgment",
                "classification_if_formalized": "Semantically Deterministic"
            },
            "V-005": {
                "capability": "Completeness (full QS)",
                "evidence": "Section-has-items already deterministic",
                "formalization_path": "Define required work packages per project type",
                "prerequisite": "Project scope definition and completeness checklists",
                "caveat": "Project-specific requirements vary; formalization limited to standard project types",
                "classification_if_formalized": "Semantically Deterministic (for standard projects)"
            }
        },
        "not_formalizable": {
            "V-003": {
                "capability": "Level Progression (skip legitimacy)",
                "evidence": "Skip detection already deterministic",
                "why_not_formalizable": "Legitimacy depends on project-specific organizational decisions that vary per project and cannot be pre-defined",
                "classification": "Professional Judgment"
            },
            "SEM-003": {
                "capability": "Items Always Quantify (zero acceptability)",
                "evidence": "Zero-quantity detection already deterministic",
                "why_not_formalizable": "Acceptability depends on QS intent, project stage, and whether zero is error or placeholder — context-specific interpretation required",
                "classification": "Professional Judgment"
            }
        }
    }

def run_spike() -> Dict[str, any]:
    """Execute Spike 2: Evidence vs Assessment Decomposition."""
    
    print("EQ-0011 Spike 2: Evidence vs Assessment Decomposition")
    print("=" * 60)
    print()
    
    # Decompose each capability
    v003 = decompose_v003()
    sem003 = decompose_sem003()
    v004 = decompose_v004()
    v005 = decompose_v005()
    
    decompositions = [v003, sem003, v004, v005]
    
    # Display decompositions
    for decomp in decompositions:
        print(f"{decomp.capability_id}: {decomp.capability_name}")
        print(f"  Evidence: {decomp.evidence.evidence_description}")
        print(f"  Assessment: {decomp.assessment.assessment_description}")
        print(f"  Boundary: {decomp.boundary_statement}")
        print()
    
    # Analyze formalization potential
    formalization = analyze_formalization_potential()
    
    print("Formalization Potential:")
    print(f"  Potentially formalizable: {len(formalization['potentially_formalizable'])} capabilities (V-004, V-005)")
    print(f"  Not formalizable: {len(formalization['not_formalizable'])} capabilities (V-003, SEM-003)")
    print()
    
    print("KEY FINDING:")
    print("Evidence components: All 4 capabilities have Structurally Deterministic evidence")
    print("Assessment components:")
    print("  - 2 capabilities: Could become Semantically Deterministic (V-004, V-005)")
    print("  - 2 capabilities: Remain Professional Judgment (V-003, SEM-003)")
    print()
    
    # Compile results
    results = {
        "decompositions": [
            {
                "capability_id": d.capability_id,
                "capability_name": d.capability_name,
                "evidence": asdict(d.evidence),
                "assessment": asdict(d.assessment),
                "boundary_statement": d.boundary_statement
            }
            for d in decompositions
        ],
        "formalization_analysis": formalization,
        "summary": {
            "evidence_classification": "All 4 evidence components: Structurally Deterministic",
            "assessment_classification": {
                "semantically_deterministic_potential": ["V-004", "V-005"],
                "professional_judgment": ["V-003", "SEM-003"]
            },
            "key_distinction": (
                "Evidence (what is) vs Assessment (what it means). "
                "Evidence is always structural and deterministic. "
                "Assessment requires either formalized semantic rules or professional judgment."
            )
        }
    }
    
    # Save results
    output_path = Path("data/reports/eq0011_spike2_results.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Results saved to: {output_path}")
    print()
    print("Spike 2 Complete")
    
    return results

if __name__ == "__main__":
    run_spike()