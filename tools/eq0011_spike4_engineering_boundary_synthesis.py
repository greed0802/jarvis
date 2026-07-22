"""
EQ-0011 Spike 4: Engineering Boundary Synthesis

Objective:
Using the validated evidence collected in Spikes 1-3, synthesize the engineering
principles that define the boundary between deterministic evidence and professional
assessment.

This is an engineering synthesis spike.
It is not another fixture analysis.
It is not an implementation spike.
It is not an architecture proposal.

Inputs:
- EQ-0010 frozen evidence
- EQ-0011 Spikes 1-3
- Domain Knowledge Layer (docs/domain/02_BOQ_Structure.md)

Constraints:
- Evidence Before Abstraction
- No new runtime architecture
- No new platform abstractions

Authority: EQ-0011 BOQ Semantic Intelligence Boundary
Governance: Engineering_Governance.md v1.0
"""

import json
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict

@dataclass(frozen=True)
class EngineeringPrinciple:
    """An engineering principle derived from evidence."""
    id: str
    name: str
    statement: str
    evidence_source: str
    authority: str
    applies_to: tuple[str, ...]

@dataclass(frozen=True)
class ResponsibilityBoundary:
    """Definition of where engineering responsibility transitions."""
    domain: str
    deterministic_responsibility: str
    judgment_responsibility: str
    boundary_rule: str
    example: str

@dataclass(frozen=True)
class BoundarySynthesis:
    """Complete engineering boundary synthesis."""
    principles: tuple[EngineeringPrinciple, ...]
    responsibilities: tuple[ResponsibilityBoundary, ...]
    first_principles: tuple[str, ...]
    what_engineering_may_conclude: tuple[str, ...]
    where_engineering_must_stop: tuple[str, ...]

def synthesize_principles() -> tuple[EngineeringPrinciple, ...]:
    """Synthesize engineering principles from EQ-0011 evidence."""
    
    return (
        EngineeringPrinciple(
            id="P-001",
            name="Evidence Before Inference",
            statement=(
                "Engineering evidence is permitted to detect facts, but it is not "
                "permitted to infer professional intent unless that inference has "
                "been demonstrated to be deterministic."
            ),
            evidence_source="EQ-0011 First Principle (approved by Project Owner)",
            authority="EQ-0011 Engineering Question",
            applies_to=("V-003", "V-004", "V-005", "SEM-003")
        ),
        EngineeringPrinciple(
            id="P-002",
            name="Structural Evidence Is Always Deterministic",
            statement=(
                "Any observation obtainable from BOQRow fields or reconstructed "
                "hierarchy is structurally deterministic. Row type, quantity value, "
                "UOM, section, parent-child relationships, hierarchy depth, and "
                "level progression gaps are always deterministically computable."
            ),
            evidence_source="EQ-0011 Spikes 1-3: All evidence components confirmed Structurally Deterministic",
            authority="EQ-0010 Capability Matrix v2.0, EQ-0011 Spikes 1-3",
            applies_to=("All capabilities")
        ),
        EngineeringPrinciple(
            id="P-003",
            name="Detection vs Decision Separation",
            statement=(
                "Every validation capability decomposes into detection (evidence) "
                "and decision (assessment). Detection is always structurally "
                "deterministic. The decision may be semantically deterministic "
                "(with formalized rules) or require professional judgment."
            ),
            evidence_source="EQ-0011 Spike 2: Evidence vs Assessment Decomposition confirmed for all 4 capabilities",
            authority="EQ-0011 Spike 2 Evidence Report",
            applies_to=("V-003", "V-004", "V-005", "SEM-003")
        ),
        EngineeringPrinciple(
            id="P-004",
            name="Judgment Terms Signal Boundary",
            statement=(
                "Domain vocabulary terms such as 'legitimate', 'acceptable', "
                "'required', 'proper', and 'as needed' signal where deterministic "
                "computation stops and professional interpretation begins. Rules "
                "using 'never' (absolute prohibition) are structurally deterministic. "
                "Rules using 'should' or 'always' (normative expectation) require "
                "judgment about context and intent."
            ),
            evidence_source="EQ-0011 Spike 1: Vocabulary analysis identified boundary indicators",
            authority="EQ-0011 Spike 1 Evidence Report",
            applies_to=("V-003", "SEM-003", "Domain rule definition")
        ),
        EngineeringPrinciple(
            id="P-005",
            name="Professional Judgment Cannot Be Formalized",
            statement=(
                "Certain assessments inherently require project-specific context, "
                "QS intent, or domain expertise that cannot be captured in "
                "pre-formalized rules. Level progression skip legitimacy (V-003) "
                "and zero-quantity acceptability (SEM-003) are Professional Judgment "
                "and must not be automated."
            ),
            evidence_source="EQ-0011 Spike 3: 0 counterexamples found; all 12 skips and 5 zero-quantity items require judgment",
            authority="EQ-0011 Spike 3 Evidence Report",
            applies_to=("V-003", "SEM-003")
        ),
        EngineeringPrinciple(
            id="P-006",
            name="Semantic Determinism Requires Explicit Rules",
            statement=(
                "Some assessments could become semantically deterministic if "
                "explicit domain rules are defined: (1) scope containment requires "
                "a formal scope taxonomy, (2) completeness requires project scope "
                "definitions. Without these rules, assessment remains Professional "
                "Judgment."
            ),
            evidence_source="EQ-0011 Spike 2: V-004 and V-005 could be formalized with rules; Spike 3: Medium confidence",
            authority="EQ-0011 Spikes 2-3 Evidence Reports",
            applies_to=("V-004", "V-005")
        ),
        EngineeringPrinciple(
            id="P-007",
            name="Evidence Cannot Answer 'Should' Questions",
            statement=(
                "BOQ structure reveals what work IS present but not what work "
                "SHOULD be present. Completeness, scope alignment, and correctness "
                "are assessment questions that require project context beyond "
                "structural observation."
            ),
            evidence_source="EQ-0011 Spike 3: Structural evidence reveals facts, not intent; Spike 1: Vocabulary analysis",
            authority="EQ-0011 Spikes 1, 3 Evidence Reports",
            applies_to=("V-004", "V-005")
        ),
    )

def synthesize_responsibilities() -> tuple[ResponsibilityBoundary, ...]:
    """Define engineering responsibility boundaries from evidence."""
    
    return (
        ResponsibilityBoundary(
            domain="Row Classification",
            deterministic_responsibility="Classify row type (Head, Item, Note, Section, Other) from BOQRow field",
            judgment_responsibility="N/A — fully deterministic",
            boundary_rule="Row type is observable, not assessed",
            example="Row with UOM 'Head1' → row_type='Head'"
        ),
        ResponsibilityBoundary(
            domain="Structural Observation",
            deterministic_responsibility="Extract and present structural facts from BOQRow + hierarchy",
            judgment_responsibility="N/A — fully deterministic",
            boundary_rule="Observation is always permitted; inference of meaning is not",
            example="Skip detected: Head1 → Head3 (gap = 2)"
        ),
        ResponsibilityBoundary(
            domain="Level Progression (V-003)",
            deterministic_responsibility="Detect and report level skip magnitude and location",
            judgment_responsibility="Determine whether skip is legitimate or violates project requirements",
            boundary_rule="Engineering detects skips; QS determines legitimacy",
            example="Engineering: 'Rows 5709-5745: Head4 under Head2 (skip=2)'. QS: 'This is acceptable due to work package structure.'"
        ),
        ResponsibilityBoundary(
            domain="Zero Quantity (SEM-003)",
            deterministic_responsibility="Detect and report items with quantity == 0.0",
            judgment_responsibility="Determine whether zero is error, placeholder, or intentional",
            boundary_rule="Engineering detects zeros; QS determines acceptability",
            example="Engineering: 'Row 5698: quantity=0.0'. QS: 'This is an omission placeholder — will be measured later.'"
        ),
        ResponsibilityBoundary(
            domain="Scope Containment (V-004)",
            deterministic_responsibility="Verify child_level <= parent_level (structural containment)",
            judgment_responsibility="Determine whether child work scope fits within parent scope semantically",
            boundary_rule="Engineering checks level consistency; QS assesses semantic alignment",
            example="Engineering: 'Level 3 under Level 2: structurally valid'. QS: 'Concrete Work under Floor Finishes: scope mismatch.'"
        ),
        ResponsibilityBoundary(
            domain="Completeness (V-005)",
            deterministic_responsibility="Verify each section contains at least one measurable item",
            judgment_responsibility="Determine whether all required work for project scope is represented",
            boundary_rule="Engineering checks structure; QS determines scope coverage",
            example="Engineering: 'Section 2.0 EXCAVATE AND FILL: 15 items present'. QS: 'Missing bulk excavation — only trench excavation shown.'"
        ),
    )

def synthesize_first_principles() -> tuple[str, ...]:
    """Core engineering principles governing future implementation."""
    
    return (
        "1. Engineering evidence is permitted to detect facts, but it is not "
        "permitted to infer professional intent unless that inference has been "
        "demonstrated to be deterministic.",
        
        "2. Every validation capability decomposes into detection (structurally "
        "deterministic) and decision (requires rules or judgment). These must "
        "never be conflated in implementation.",
        
        "3. Professional Judgment capabilities (V-003 skip legitimacy, SEM-003 "
        "zero acceptability) must not be automated. Engineering may detect and "
        "present evidence, but the decision belongs to the QS.",
        
        "4. Semantically Deterministic capabilities (V-004 semantic scope, V-005 "
        "full completeness) may be implemented only after explicit domain rules "
        "are formalized. Without formal rules, they remain Professional Judgment.",
        
        "5. 'Never' rules are structurally deterministic. 'Should' and 'always' "
        "rules require judgment about context and intent. Implementation must "
        "distinguish between absolute prohibitions and normative expectations.",
    )

def synthesize_what_engineering_may_conclude() -> tuple[str, ...]:
    """What engineering is permitted to assert based on evidence."""
    
    return (
        "Engineering may conclude: 'Row 1661: skip detected (Head1→Head3, gap=2)'",
        "Engineering may conclude: 'Row 5698: quantity = 0.0'",
        "Engineering may conclude: 'All parent-child relationships satisfy structural containment'",
        "Engineering may conclude: 'All sections have at least one measurable item'",
        "Engineering may conclude: 'Section X has Row type distribution: Head=x, Item=y'",
        "Engineering may conclude: 'Parent-level consistency is valid for all pairs'",
        "Engineering may conclude: 'Zero-quantity items detected: {list of rows}'",
        "Engineering may conclude: 'Level progression skips detected: {list of rows}'",
    )

def synthesize_where_engineering_must_stop() -> tuple[str, ...]:
    """Where engineering must stop and professional judgment begins."""
    
    return (
        "Engineering must stop before concluding: 'This skip is a mistake' "
        "(requires project context — Professional Judgment)",
        
        "Engineering must stop before concluding: 'This zero-quantity item is an error' "
        "(requires QS intent — Professional Judgment)",
        
        "Engineering must stop before concluding: 'This work package is out of scope' "
        "(requires project scope knowledge — Professional Judgment or Semantic Rules)",
        
        "Engineering must stop before concluding: 'This BOQ is incomplete' "
        "(requires project scope definition — Professional Judgment or Semantic Rules)",
        
        "Engineering must stop before concluding: 'The estimator made an error' "
        "(requires understanding of intent — Professional Judgment)",
    )

def run_spike() -> Dict[str, any]:
    """Execute Spike 4: Engineering Boundary Synthesis."""
    
    print("EQ-0011 Spike 4: Engineering Boundary Synthesis")
    print("=" * 60)
    print()
    
    # Synthesize from evidence
    principles = synthesize_principles()
    responsibilities = synthesize_responsibilities()
    first_principles = synthesize_first_principles()
    what_may_conclude = synthesize_what_engineering_may_conclude()
    where_must_stop = synthesize_where_engineering_must_stop()
    
    print(f"Synthesized: {len(principles)} engineering principles")
    print(f"Synthesized: {len(responsibilities)} responsibility boundaries")
    print(f"Synthesized: {len(first_principles)} first principles")
    print()
    
    print("ENGINEERING PRINCIPLES:")
    for p in principles:
        print(f"  {p.id}: {p.name}")
    print()
    
    print("RESPONSIBILITY BOUNDARIES:")
    for r in responsibilities:
        print(f"  {r.domain}:")
        print(f"    Deterministic: {r.deterministic_responsibility[:60]}...")
        print(f"    Judgment: {r.judgment_responsibility[:60]}...")
    print()
    
    print("FIRST PRINCIPLES:")
    for fp in first_principles:
        print(f"  {fp[:100]}...")
    print()
    
    print("WHAT ENGINEERING MAY CONCLUDE:")
    for c in what_may_conclude:
        print(f"  {c}")
    print()
    
    print("WHERE ENGINEERING MUST STOP:")
    for s in where_must_stop:
        print(f"  {s}")
    print()
    
    # Compile results
    results = {
        "principles": [asdict(p) for p in principles],
        "responsibilities": [asdict(r) for r in responsibilities],
        "first_principles": list(first_principles),
        "what_engineering_may_conclude": list(what_may_conclude),
        "where_engineering_must_stop": list(where_must_stop),
        "summary": {
            "total_principles": len(principles),
            "total_responsibility_boundaries": len(responsibilities),
            "total_first_principles": len(first_principles),
            "evidence_sources": [
                "EQ-0010 frozen evidence (all spikes)",
                "EQ-0011 Spike 1: Domain Vocabulary Discovery",
                "EQ-0011 Spike 2: Evidence vs Assessment Decomposition",
                "EQ-0011 Spike 3: Boundary Validation Against Production Evidence",
                "Domain Layer: docs/domain/02_BOQ_Structure.md"
            ]
        }
    }
    
    # Save results
    output_path = Path("data/reports/eq0011_spike4_results.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Results saved to: {output_path}")
    print()
    print("Spike 4 Complete")
    
    return results

if __name__ == "__main__":
    run_spike()