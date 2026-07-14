"""
EQ-0011 Spike 1: Domain Vocabulary Discovery

Objective:
Extract and analyze domain vocabulary from BOQ Structure documentation to identify
terminology that distinguishes between:
- Structural facts (deterministic)
- Semantic interpretation (requires domain rules)
- Professional judgment (requires QS expertise)

This spike maps domain concepts to the Engineering Decision Classification taxonomy.

Authority: EQ-0011 BOQ Semantic Intelligence Boundary
Governance: Engineering_Governance.md v1.0
"""

import json
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Set

@dataclass(frozen=True)
class DomainTerm:
    """A domain vocabulary term with classification."""
    term: str
    definition: str
    source_section: str
    classification_hint: str  # 'structural', 'semantic', 'judgment', 'mixed'
    examples: tuple[str, ...]
    related_capabilities: tuple[str, ...]

@dataclass(frozen=True)
class VocabularyAnalysis:
    """Results of domain vocabulary discovery."""
    structural_terms: tuple[DomainTerm, ...]
    semantic_terms: tuple[DomainTerm, ...]
    judgment_terms: tuple[DomainTerm, ...]
    mixed_terms: tuple[DomainTerm, ...]
    validation_verbs: tuple[str, ...]
    detection_verbs: tuple[str, ...]
    rule_patterns: tuple[str, ...]
    boundary_indicators: tuple[str, ...]

def discover_vocabulary() -> VocabularyAnalysis:
    """
    Analyze domain vocabulary from BOQ Structure documentation.
    
    Evidence: Domain Layer docs/domain/02_BOQ_Structure.md
    
    Returns:
        VocabularyAnalysis with terms classified by decision type
    """
    
    # Structural terms: Observable from BOQRow + hierarchy
    structural_terms = (
        DomainTerm(
            term="Hierarchy Level",
            definition="Position in nested structure (Level 1, Level 2, etc.)",
            source_section="Definitions - Domain Concepts",
            classification_hint="structural",
            examples=("Head1", "Head2", "Head3", "Head4", "Head5"),
            related_capabilities=("V-003", "V-004")
        ),
        DomainTerm(
            term="Parent-Child Relationship",
            definition="Structural connection between header levels",
            source_section="Hierarchy - Properties",
            classification_hint="structural",
            examples=("Head2 under Head1", "Head3 under Head2"),
            related_capabilities=("V-001", "V-002", "V-003")
        ),
        DomainTerm(
            term="Measured Item",
            definition="A measurable quantity with description, UOM, and quantity",
            source_section="Definitions - Domain Concepts",
            classification_hint="structural",
            examples=("Plain concrete 20MPa to footings: m³: 12.50",),
            related_capabilities=("SEM-003",)
        ),
        DomainTerm(
            term="Header",
            definition="Hierarchy element that provides context but does not quantify",
            source_section="Hierarchy - Semantic Rules",
            classification_hint="structural",
            examples=("SUBSTRUCTURE", "Strip Footings", "Concrete Work"),
            related_capabilities=("SEM-001", "SEM-002")
        ),
        DomainTerm(
            term="Section",
            definition="Top-level organizational unit (Hierarchy Level 1)",
            source_section="Definitions - Domain Concepts",
            classification_hint="structural",
            examples=("SUBSTRUCTURE", "SUPERSTRUCTURE", "FINISHES"),
            related_capabilities=("SEM-001", "V-005")
        ),
    )
    
    # Semantic terms: Require understanding of meaning/intent
    semantic_terms = (
        DomainTerm(
            term="Semantic Inheritance",
            definition="Child elements inherit meaning from all parents",
            source_section="Hierarchy - Semantic Rules",
            classification_hint="semantic",
            examples=("Full item meaning = inherited context + item specification",),
            related_capabilities=("SEM-004", "SEM-005", "V-004")
        ),
        DomainTerm(
            term="Scope",
            definition="The work package or domain an element represents",
            source_section="Hierarchy - Semantic Rules",
            classification_hint="semantic",
            examples=("Scope: SUBSTRUCTURE", "Element: Strip Footings"),
            related_capabilities=("V-004",)
        ),
        DomainTerm(
            term="Completeness",
            definition="No missing work, all required measurable work represented",
            source_section="Semantic Validation Rules - SEM-005",
            classification_hint="semantic",
            examples=("All foundation work items present",),
            related_capabilities=("V-005",)
        ),
        DomainTerm(
            term="Context",
            definition="Semantic meaning provided by hierarchy structure",
            source_section="Hierarchy - Semantic Rules",
            classification_hint="semantic",
            examples=("Headers provide context only",),
            related_capabilities=("SEM-002", "V-004")
        ),
        DomainTerm(
            term="Logical Consistency",
            definition="BOQ structure remains meaningful and hierarchically sound",
            source_section="Definitions - Domain Concepts",
            classification_hint="semantic",
            examples=("Hierarchy follows logical decomposition",),
            related_capabilities=("V-003", "V-004")
        ),
    )
    
    # Judgment terms: Require professional QS interpretation
    judgment_terms = (
        DomainTerm(
            term="Legitimate",
            definition="Acceptable according to professional QS standards",
            source_section="(Implicit throughout domain rules)",
            classification_hint="judgment",
            examples=("Legitimate organizational pattern", "Legitimate placeholder"),
            related_capabilities=("V-003", "SEM-003")
        ),
        DomainTerm(
            term="Error",
            definition="Violation requiring correction",
            source_section="Semantic Validation Rules - Severity",
            classification_hint="judgment",
            examples=("Data entry error", "Structural violation"),
            related_capabilities=("V-003", "SEM-003")
        ),
        DomainTerm(
            term="Project Complexity",
            definition="Characteristics requiring deeper hierarchy",
            source_section="Definitions - Domain Concepts",
            classification_hint="judgment",
            examples=("Hierarchy Level N: Additional subdivision as required",),
            related_capabilities=("V-003", "V-005")
        ),
        DomainTerm(
            term="Required Work",
            definition="Work items mandated by project scope",
            source_section="Semantic Validation Rules - SEM-005",
            classification_hint="judgment",
            examples=("All required measurable work represented",),
            related_capabilities=("V-005",)
        ),
        DomainTerm(
            term="Acceptable",
            definition="Meeting professional QS standards",
            source_section="(Implicit in validation rules)",
            classification_hint="judgment",
            examples=("Acceptable level progression", "Acceptable zero quantity"),
            related_capabilities=("V-003", "SEM-003")
        ),
    )
    
    # Mixed terms: Both structural detection + semantic/judgment validation
    mixed_terms = (
        DomainTerm(
            term="Level Progression",
            definition="Sequence of hierarchy levels from parent to child",
            source_section="Valid Hierarchy Patterns",
            classification_hint="mixed",
            examples=("Head1 → Head2 → Head3", "Head1 → Head3 (skip)"),
            related_capabilities=("V-003",)
        ),
        DomainTerm(
            term="Orphan",
            definition="Item without proper hierarchical parent",
            source_section="(From EQ-0010 Spike 5 taxonomy)",
            classification_hint="mixed",
            examples=("Item with no preceding Head", "Item without quantity"),
            related_capabilities=("V-002", "SEM-003")
        ),
        DomainTerm(
            term="Quantify",
            definition="Assign numerical measurement value",
            source_section="Semantic Validation Rules - SEM-003",
            classification_hint="mixed",
            examples=("Items must have quantity and UOM", "quantity = 0.0"),
            related_capabilities=("SEM-003",)
        ),
        DomainTerm(
            term="Containment",
            definition="Child elements fit within parent scope",
            source_section="Semantic Validation Rules - V-004",
            classification_hint="mixed",
            examples=("Structural: child_level <= parent_level", "Semantic: work scope alignment"),
            related_capabilities=("V-004",)
        ),
    )
    
    # Validation verbs: Indicate assessment/judgment
    validation_verbs = (
        "validate", "verify", "check", "confirm", "ensure", 
        "must", "should", "require", "prohibit", "allow",
        "acceptable", "legitimate", "correct", "proper", "sound"
    )
    
    # Detection verbs: Indicate observation/measurement
    detection_verbs = (
        "detect", "observe", "identify", "measure", "count",
        "extract", "find", "locate", "determine", "calculate",
        "exists", "present", "absent", "equal", "matches"
    )
    
    # Rule patterns from domain documentation
    rule_patterns = (
        "never" + " measure/quantify",  # SEM-001, SEM-002
        "always" + " quantify",  # SEM-003
        "must" + " exist/have/be",  # V-001, V-002
        "should" + " follow/progress",  # V-003
        "fit within" + " scope",  # V-004
        "all" + " required work",  # V-005
    )
    
    # Boundary indicators: Terms suggesting judgment required
    boundary_indicators = (
        "legitimate",
        "acceptable",
        "proper",
        "as required",
        "project complexity",
        "professional standards",
        "QS judgment",
        "domain knowledge",
        "interpretation",
        "understanding",
    )
    
    return VocabularyAnalysis(
        structural_terms=structural_terms,
        semantic_terms=semantic_terms,
        judgment_terms=judgment_terms,
        mixed_terms=mixed_terms,
        validation_verbs=validation_verbs,
        detection_verbs=detection_verbs,
        rule_patterns=rule_patterns,
        boundary_indicators=boundary_indicators
    )

def analyze_v003_vocabulary(analysis: VocabularyAnalysis) -> Dict[str, any]:
    """Analyze V-003 Level Progression through vocabulary lens."""
    return {
        "capability": "V-003: Level Progression Validation",
        "detection_vocabulary": [
            "level skip detected",
            "Head1 → Head3 (no Head2)",
            "parent_level - child_level > 1"
        ],
        "judgment_vocabulary": [
            "legitimate organizational pattern",
            "project complexity requires",
            "acceptable level skip"
        ],
        "boundary_observation": (
            "Detection is structural (observable). "
            "Validation requires judging if skip is legitimate for this project context."
        )
    }

def analyze_sem003_vocabulary(analysis: VocabularyAnalysis) -> Dict[str, any]:
    """Analyze SEM-003 Items Always Quantify through vocabulary lens."""
    return {
        "capability": "SEM-003: Items Always Quantify",
        "detection_vocabulary": [
            "quantity == 0",
            "zero-quantity item",
            "measured item with no measurement"
        ],
        "judgment_vocabulary": [
            "legitimate placeholder",
            "data entry error",
            "incomplete takeoff",
            "acceptable zero quantity"
        ],
        "boundary_observation": (
            "Detection is structural (quantity field value). "
            "Validation requires judging whether zero is error or intentional placeholder."
        )
    }

def analyze_v004_vocabulary(analysis: VocabularyAnalysis) -> Dict[str, any]:
    """Analyze V-004 Scope Containment through vocabulary lens."""
    return {
        "capability": "V-004: Scope Containment",
        "detection_vocabulary": [
            "child_level <= parent_level",
            "structural parent-child relationship",
            "hierarchy level consistency"
        ],
        "judgment_vocabulary": [
            "semantic scope alignment",
            "work package containment",
            "project intent",
            "understanding header meaning"
        ],
        "boundary_observation": (
            "Structural containment is derivable (parent-level consistency). "
            "Semantic containment requires understanding what each header represents."
        )
    }

def analyze_v005_vocabulary(analysis: VocabularyAnalysis) -> Dict[str, any]:
    """Analyze V-005 Completeness through vocabulary lens."""
    return {
        "capability": "V-005: Completeness",
        "detection_vocabulary": [
            "section has measurable items",
            "at least one Item row",
            "non-empty section"
        ],
        "judgment_vocabulary": [
            "all required work represented",
            "no missing work",
            "project scope knowledge",
            "complete work package"
        ],
        "boundary_observation": (
            "Structural completeness is derivable (section has items). "
            "Full QS completeness requires knowing what work should be present."
        )
    }

def run_spike() -> Dict[str, any]:
    """Execute Spike 1: Domain Vocabulary Discovery."""
    
    print("EQ-0011 Spike 1: Domain Vocabulary Discovery")
    print("=" * 60)
    print()
    
    # Discover vocabulary
    analysis = discover_vocabulary()
    
    print(f"Structural Terms: {len(analysis.structural_terms)}")
    print(f"Semantic Terms: {len(analysis.semantic_terms)}")
    print(f"Judgment Terms: {len(analysis.judgment_terms)}")
    print(f"Mixed Terms: {len(analysis.mixed_terms)}")
    print()
    
    # Analyze each capability
    v003_analysis = analyze_v003_vocabulary(analysis)
    sem003_analysis = analyze_sem003_vocabulary(analysis)
    v004_analysis = analyze_v004_vocabulary(analysis)
    v005_analysis = analyze_v005_vocabulary(analysis)
    
    print("V-003 Boundary:")
    print(f"  {v003_analysis['boundary_observation']}")
    print()
    
    print("SEM-003 Boundary:")
    print(f"  {sem003_analysis['boundary_observation']}")
    print()
    
    print("V-004 Boundary:")
    print(f"  {v004_analysis['boundary_observation']}")
    print()
    
    print("V-005 Boundary:")
    print(f"  {v005_analysis['boundary_observation']}")
    print()
    
    # Key finding
    print("KEY FINDING:")
    print("All four capabilities exhibit Detection/Decision split:")
    print("- Detection: Structurally Deterministic")
    print("- Decision: Requires domain rules or professional judgment")
    print()
    
    # Compile results
    results = {
        "vocabulary_analysis": {
            "structural_terms": [asdict(t) for t in analysis.structural_terms],
            "semantic_terms": [asdict(t) for t in analysis.semantic_terms],
            "judgment_terms": [asdict(t) for t in analysis.judgment_terms],
            "mixed_terms": [asdict(t) for t in analysis.mixed_terms],
            "validation_verbs": list(analysis.validation_verbs),
            "detection_verbs": list(analysis.detection_verbs),
            "rule_patterns": list(analysis.rule_patterns),
            "boundary_indicators": list(analysis.boundary_indicators),
        },
        "capability_analyses": {
            "V-003": v003_analysis,
            "SEM-003": sem003_analysis,
            "V-004": v004_analysis,
            "V-005": v005_analysis,
        },
        "key_finding": (
            "All four Domain Dependent capabilities exhibit a Detection/Decision split. "
            "Detection is Structurally Deterministic (observable from BOQRow + hierarchy). "
            "Decision requires either Semantically Deterministic rules (if formalized) "
            "or Professional Judgment (if project-specific or contextual)."
        )
    }
    
    # Save results
    output_path = Path("data/reports/eq0011_spike1_results.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Results saved to: {output_path}")
    print()
    print("Spike 1 Complete")
    
    return results

if __name__ == "__main__":
    run_spike()