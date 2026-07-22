"""
EQ-0013 Spike 1: Validation Capability Discovery

Purpose: Discover all deterministic validation capabilities possible using
         the frozen Public Evidence Contract v1.0.

Authority: EQ-0013 (Validation Engine Investigation)
Contract: BOQ Intelligence Public Evidence Contract v1.0.0
Boundary: EQ-0011 (Observe/Reconstruct/Detect, never Judge/Recommend/Assess)

This tool enumerates validation rules derivable from frozen evidence,
establishes the Validation Rule Registry, and classifies each rule.
"""

import json
from dataclasses import dataclass, field
from typing import Literal

# Evidence Contract v1.0.0 - 10 fields from Increments 1-3
EVIDENCE_FIELDS = {
    # Increment 1 - Observation
    "row_classification": {
        "type": "dict[str, int]",
        "required": True,
        "classification": "Observation",
        "increment": 1,
        "keys": ["Head", "Note", "Section", "Item", "Other"],
    },
    "section_statistics": {
        "type": "dict[str, dict[str, int]]",
        "required": True,
        "classification": "Observation",
        "increment": 1,
        "inner_keys": ["negative_qty", "positive_qty"],
    },
    "boq_statistics": {
        "type": "dict[str, int | float]",
        "required": True,
        "classification": "Observation",
        "increment": 1,
        "keys": ["total_rows", "code_rows", "description_rows", "quantity_rows", "uom_rows", "section_rows"],
    },
    "known_anomalies": {
        "type": "list[dict[str, int | str | float]]",
        "required": True,
        "classification": "Observation",
        "increment": 1,
        "element_keys": ["row_number", "code", "quantity", "section"],
    },
    # Increment 2 - Hierarchy
    "hierarchy": {
        "type": "tuple[BOQHeaderNode, ...] | None",
        "required": False,
        "classification": "Hierarchy",
        "increment": 2,
    },
    "hierarchy_statistics": {
        "type": "dict[str, int | float] | None",
        "required": False,
        "classification": "Hierarchy",
        "increment": 2,
        "keys": ["total_headers", "root_headers", "depth_distribution", "items_per_header_by_uom"],
    },
    # Increment 3 - Detection
    "detected_level_skips": {
        "type": "tuple[dict[str, int], ...] | None",
        "required": False,
        "classification": "Detection",
        "increment": 3,
        "element_keys": ["parent_row_number", "parent_level", "child_row_number", "child_level", "skip_magnitude"],
    },
    "zero_quantity_items": {
        "type": "tuple[dict[str, int | str | float | None], ...] | None",
        "required": False,
        "classification": "Detection",
        "increment": 3,
        "element_keys": ["row_number", "code", "description", "section", "quantity", "uom"],
    },
    "structural_containment_findings": {
        "type": "tuple[dict[str, int], ...] | None",
        "required": False,
        "classification": "Detection",
        "increment": 3,
        "element_keys": ["parent_row_number", "parent_level", "child_row_number", "child_level"],
    },
    "completeness_findings": {
        "type": "tuple[dict[str, int | str], ...] | None",
        "required": False,
        "classification": "Detection",
        "increment": 3,
        "element_keys": ["section", "item_count"],
    },
}

# Rule Status
RuleStatus = Literal["Candidate", "Approved", "Deprecated", "Retired"]

# Rule Classification
RuleClassification = Literal[
    "Supported",  # Can be implemented with current evidence
    "Multiple Fields",  # Requires multiple evidence fields
    "Insufficient Evidence",  # Cannot be implemented - missing evidence
    "Boundary Violation",  # Crosses EQ-0011 boundary
    "Speculative",  # Not backed by frozen evidence
]

# Boundary Classification
BoundaryClass = Literal[
    "Observation",  # Pure observation check
    "Detection",  # Pattern detection check
    "Relationship",  # Cross-field relationship check
    "Violation",  # Crosses EQ-0011 boundary (Judge/Recommend/Assess)
]

@dataclass
class ValidationRule:
    """Validation rule with complete provenance."""
    
    rule_id: str
    category: str
    description: str
    evidence_fields: list[str]
    boundary_class: BoundaryClass
    classification: RuleClassification
    introduced_by: str  # EQ number and spike
    contract_version: str
    status: RuleStatus
    deterministic_finding: str
    rationale: str
    eq_source: str  # EQ-0010, EQ-0011, or EQ-0012

def discover_validation_capabilities():
    """
    Discover all validation capabilities from Evidence Contract v1.0.
    
    Returns validation rules organized by:
    - Supported (can be implemented)
    - Multiple Fields (requires cross-field logic)
    - Insufficient Evidence (cannot be implemented)
    - Boundary Violations (crosses EQ-0011)
    - Speculative (not evidence-backed)
    """
    
    rules = []
    
    # ========================================
    # CATEGORY 1: STRUCTURAL VALIDATIONS
    # (Single-field presence/type/shape checks)
    # ========================================
    
    # V-001: Required Field Presence
    rules.append(ValidationRule(
        rule_id="V-001",
        category="Structural",
        description="Verify all required evidence fields are present",
        evidence_fields=["row_classification", "section_statistics", "boq_statistics", "known_anomalies"],
        boundary_class="Observation",
        classification="Supported",
        introduced_by="EQ-0013 Spike 1",
        contract_version="1.0.0",
        status="Candidate",
        deterministic_finding="Lists missing required fields (empty if all present)",
        rationale="Contract guarantees required fields always present (G-01, G-02)",
        eq_source="EQ-0012",
    ))
    
    # V-002: Row Classification Shape
    rules.append(ValidationRule(
        rule_id="V-002",
        category="Structural",
        description="Verify row_classification contains exactly 5 expected keys",
        evidence_fields=["row_classification"],
        boundary_class="Observation",
        classification="Supported",
        introduced_by="EQ-0013 Spike 1",
        contract_version="1.0.0",
        status="Candidate",
        deterministic_finding="Reports missing or unexpected keys",
        rationale="Contract invariant SI-RC-04 guarantees 5 keys",
        eq_source="EQ-0012",
    ))
    
    # V-003: Row Classification Non-Negative
    rules.append(ValidationRule(
        rule_id="V-003",
        category="Structural",
        description="Verify row_classification values are non-negative integers",
        evidence_fields=["row_classification"],
        boundary_class="Observation",
        classification="Supported",
        introduced_by="EQ-0013 Spike 1",
        contract_version="1.0.0",
        status="Candidate",
        deterministic_finding="Reports negative count values",
        rationale="Counts represent observed row frequencies, cannot be negative",
        eq_source="EQ-0010",
    ))
    
    # ========================================
    # CATEGORY 2: CONSISTENCY VALIDATIONS
    # (Cross-field arithmetic/logical consistency)
    # ========================================
    
    # V-004: Total Rows Consistency
    rules.append(ValidationRule(
        rule_id="V-004",
        category="Consistency",
        description="Verify sum of row_classification equals boq_statistics['total_rows']",
        evidence_fields=["row_classification", "boq_statistics"],
        boundary_class="Relationship",
        classification="Multiple Fields",
        introduced_by="EQ-0013 Spike 1",
        contract_version="1.0.0",
        status="Candidate",
        deterministic_finding="Reports discrepancy magnitude if sums don't match",
        rationale="Classification counts must sum to total (cross-field dependency documented)",
        eq_source="EQ-0010",
    ))
    
    # V-005: Section Statistics Coverage
    rules.append(ValidationRule(
        rule_id="V-005",
        category="Consistency",
        description="Verify all sections in section_statistics have non-negative quantity counts",
        evidence_fields=["section_statistics"],
        boundary_class="Observation",
        classification="Supported",
        introduced_by="EQ-0013 Spike 1",
        contract_version="1.0.0",
        status="Candidate",
        deterministic_finding="Reports sections with invalid (negative) counts",
        rationale="Quantity counts represent observed frequencies",
        eq_source="EQ-0010",
    ))
    
    # V-006: Anomaly Row Numbers Within Range
    rules.append(ValidationRule(
        rule_id="V-006",
        category="Consistency",
        description="Verify known_anomalies row_numbers are within [1, total_rows]",
        evidence_fields=["known_anomalies", "boq_statistics"],
        boundary_class="Relationship",
        classification="Multiple Fields",
        introduced_by="EQ-0013 Spike 1",
        contract_version="1.0.0",
        status="Candidate",
        deterministic_finding="Reports anomalies with out-of-range row numbers",
        rationale="Row numbers reference BOQ rows, must be within observed range",
        eq_source="EQ-0010",
    ))
    
    # ========================================
    # CATEGORY 3: COMPLETENESS VALIDATIONS
    # (Data completeness relative to total)
    # ========================================
    
    # V-007: Code Column Completeness
    rules.append(ValidationRule(
        rule_id="V-007",
        category="Completeness",
        description="Calculate ratio of code_rows to total_rows",
        evidence_fields=["boq_statistics"],
        boundary_class="Observation",
        classification="Supported",
        introduced_by="EQ-0013 Spike 1",
        contract_version="1.0.0",
        status="Candidate",
        deterministic_finding="Reports completeness ratio (0.0 to 1.0)",
        rationale="Observes code column population density",
        eq_source="EQ-0010",
    ))
    
    # V-008: Description Column Completeness
    rules.append(ValidationRule(
        rule_id="V-008",
        category="Completeness",
        description="Calculate ratio of description_rows to total_rows",
        evidence_fields=["boq_statistics"],
        boundary_class="Observation",
        classification="Supported",
        introduced_by="EQ-0013 Spike 1",
        contract_version="1.0.0",
        status="Candidate",
        deterministic_finding="Reports completeness ratio (0.0 to 1.0)",
        rationale="Observes description column population density",
        eq_source="EQ-0010",
    ))
    
    # V-009: Quantity Column Completeness
    rules.append(ValidationRule(
        rule_id="V-009",
        category="Completeness",
        description="Calculate ratio of quantity_rows to total_rows",
        evidence_fields=["boq_statistics"],
        boundary_class="Observation",
        classification="Supported",
        introduced_by="EQ-0013 Spike 1",
        contract_version="1.0.0",
        status="Candidate",
        deterministic_finding="Reports completeness ratio (0.0 to 1.0)",
        rationale="Observes quantity column population density",
        eq_source="EQ-0010",
    ))
    
    # ========================================
    # CATEGORY 4: HIERARCHY VALIDATIONS
    # (Hierarchy structure checks - optional evidence)
    # ========================================
    
    # V-010: Hierarchy Availability
    rules.append(ValidationRule(
        rule_id="V-010",
        category="Structural",
        description="Check if hierarchy evidence is available (not None)",
        evidence_fields=["hierarchy"],
        boundary_class="Observation",
        classification="Supported",
        introduced_by="EQ-0013 Spike 1",
        contract_version="1.0.0",
        status="Candidate",
        deterministic_finding="Reports whether hierarchy was reconstructed",
        rationale="Hierarchy is optional evidence (include_hierarchy parameter)",
        eq_source="EQ-0010",
    ))
    
    # V-011: Root Header Count
    rules.append(ValidationRule(
        rule_id="V-011",
        category="Structural",
        description="Report number of root headers in hierarchy",
        evidence_fields=["hierarchy_statistics"],
        boundary_class="Observation",
        classification="Supported",
        introduced_by="EQ-0013 Spike 1",
        contract_version="1.0.0",
        status="Candidate",
        deterministic_finding="Reports root_headers count or None if unavailable",
        rationale="Observes hierarchy structure",
        eq_source="EQ-0010",
    ))
    
    # V-012: Hierarchy Depth Range
    rules.append(ValidationRule(
        rule_id="V-012",
        category="Structural",
        description="Report min/max depth in hierarchy",
        evidence_fields=["hierarchy_statistics"],
        boundary_class="Observation",
        classification="Supported",
        introduced_by="EQ-0013 Spike 1",
        contract_version="1.0.0",
        status="Candidate",
        deterministic_finding="Reports (min_depth, max_depth) or None if unavailable",
        rationale="Observes hierarchy depth distribution",
        eq_source="EQ-0010",
    ))
    
    # ========================================
    # CATEGORY 5: DETECTION VALIDATIONS
    # (Detection evidence checks - optional)
    # ========================================
    
    # V-013: Level Skip Detection Availability
    rules.append(ValidationRule(
        rule_id="V-013",
        category="Detection",
        description="Check if level skip detection is available",
        evidence_fields=["detected_level_skips"],
        boundary_class="Detection",
        classification="Supported",
        introduced_by="EQ-0013 Spike 1",
        contract_version="1.0.0",
        status="Candidate",
        deterministic_finding="Reports whether level skips were detected",
        rationale="Detection is optional evidence (include_detection parameter)",
        eq_source="EQ-0011",
    ))
    
    # V-014: Level Skip Count
    rules.append(ValidationRule(
        rule_id="V-014",
        category="Detection",
        description="Count number of detected level skips",
        evidence_fields=["detected_level_skips"],
        boundary_class="Detection",
        classification="Supported",
        introduced_by="EQ-0013 Spike 1",
        contract_version="1.0.0",
        status="Candidate",
        deterministic_finding="Reports skip count or None if unavailable",
        rationale="Observes level skip pattern frequency",
        eq_source="EQ-0011",
    ))
    
    # V-015: Level Skip Magnitude Range
    rules.append(ValidationRule(
        rule_id="V-015",
        category="Detection",
        description="Report min/max skip magnitude",
        evidence_fields=["detected_level_skips"],
        boundary_class="Detection",
        classification="Supported",
        introduced_by="EQ-0013 Spike 1",
        contract_version="1.0.0",
        status="Candidate",
        deterministic_finding="Reports (min_magnitude, max_magnitude) or None",
        rationale="Observes skip magnitude distribution",
        eq_source="EQ-0011",
    ))
    
    # V-016: Zero Quantity Item Count
    rules.append(ValidationRule(
        rule_id="V-016",
        category="Detection",
        description="Count number of zero quantity items",
        evidence_fields=["zero_quantity_items"],
        boundary_class="Detection",
        classification="Supported",
        introduced_by="EQ-0013 Spike 1",
        contract_version="1.0.0",
        status="Candidate",
        deterministic_finding="Reports count or None if unavailable",
        rationale="Observes zero quantity pattern frequency",
        eq_source="EQ-0011",
    ))
    
    # V-017: Structural Containment Finding Count
    rules.append(ValidationRule(
        rule_id="V-017",
        category="Detection",
        description="Count structural containment findings",
        evidence_fields=["structural_containment_findings"],
        boundary_class="Detection",
        classification="Supported",
        introduced_by="EQ-0013 Spike 1",
        contract_version="1.0.0",
        status="Candidate",
        deterministic_finding="Reports finding count or None if unavailable",
        rationale="Observes structural inversion frequency",
        eq_source="EQ-0011",
    ))
    
    # V-018: Empty Section Count
    rules.append(ValidationRule(
        rule_id="V-018",
        category="Detection",
        description="Count sections with zero items (completeness findings)",
        evidence_fields=["completeness_findings"],
        boundary_class="Detection",
        classification="Supported",
        introduced_by="EQ-0013 Spike 1",
        contract_version="1.0.0",
        status="Candidate",
        deterministic_finding="Reports empty section count or None if unavailable",
        rationale="Observes section-level item completeness",
        eq_source="EQ-0011",
    ))
    
    # ========================================
    # BOUNDARY VIOLATION EXAMPLES
    # (These cross EQ-0011 boundary - documented but rejected)
    # ========================================
    
    # V-901: BOQ Quality Assessment (BOUNDARY VIOLATION)
    rules.append(ValidationRule(
        rule_id="V-901",
        category="Assessment",
        description="Assess overall BOQ quality based on completeness ratios",
        evidence_fields=["boq_statistics"],
        boundary_class="Violation",
        classification="Boundary Violation",
        introduced_by="EQ-0013 Spike 1",
        contract_version="1.0.0",
        status="Candidate",
        deterministic_finding="N/A - crosses boundary",
        rationale="REJECTED: Crosses EQ-0011 boundary (Assess/Judge)",
        eq_source="EQ-0011",
    ))
    
    # V-902: Level Skip Recommendation (BOUNDARY VIOLATION)
    rules.append(ValidationRule(
        rule_id="V-902",
        category="Recommendation",
        description="Recommend whether level skips should be corrected",
        evidence_fields=["detected_level_skips"],
        boundary_class="Violation",
        classification="Boundary Violation",
        introduced_by="EQ-0013 Spike 1",
        contract_version="1.0.0",
        status="Candidate",
        deterministic_finding="N/A - crosses boundary",
        rationale="REJECTED: Crosses EQ-0011 boundary (Recommend)",
        eq_source="EQ-0011",
    ))
    
    # ========================================
    # INSUFFICIENT EVIDENCE EXAMPLES
    # (Cannot be implemented with current evidence)
    # ========================================
    
    # V-801: Item Cost Validation (INSUFFICIENT EVIDENCE)
    rules.append(ValidationRule(
        rule_id="V-801",
        category="Financial",
        description="Verify item costs are reasonable",
        evidence_fields=[],
        boundary_class="Observation",
        classification="Insufficient Evidence",
        introduced_by="EQ-0013 Spike 1",
        contract_version="1.0.0",
        status="Candidate",
        deterministic_finding="N/A - no cost evidence",
        rationale="REJECTED: No cost/price evidence in Contract v1.0",
        eq_source="EQ-0012",
    ))
    
    # V-802: Drawing Reference Validation (INSUFFICIENT EVIDENCE)
    rules.append(ValidationRule(
        rule_id="V-802",
        category="Reference",
        description="Verify items reference valid drawings",
        evidence_fields=[],
        boundary_class="Relationship",
        classification="Insufficient Evidence",
        introduced_by="EQ-0013 Spike 1",
        contract_version="1.0.0",
        status="Candidate",
        deterministic_finding="N/A - no drawing evidence",
        rationale="REJECTED: No drawing reference evidence in Contract v1.0",
        eq_source="EQ-0012",
    ))
    
    return rules

def generate_validation_rule_registry(rules: list[ValidationRule]) -> dict:
    """Generate Validation Rule Registry."""
    return {
        "registry_version": "1.0.0",
        "contract_version": "1.0.0",
        "generated_by": "EQ-0013 Spike 1",
        "total_rules": len(rules),
        "rules": [
            {
                "rule_id": r.rule_id,
                "category": r.category,
                "description": r.description,
                "evidence_fields": r.evidence_fields,
                "boundary_class": r.boundary_class,
                "classification": r.classification,
                "introduced_by": r.introduced_by,
                "contract_version": r.contract_version,
                "status": r.status,
                "deterministic_finding": r.deterministic_finding,
                "rationale": r.rationale,
                "eq_source": r.eq_source,
            }
            for r in rules
        ],
    }

def classify_rules(rules: list[ValidationRule]) -> dict:
    """Classify rules by category."""
    classification_counts = {
        "Supported": [],
        "Multiple Fields": [],
        "Insufficient Evidence": [],
        "Boundary Violation": [],
        "Speculative": [],
    }
    
    for rule in rules:
        classification_counts[rule.classification].append(rule.rule_id)
    
    return classification_counts

def generate_evidence_to_rule_mapping(rules: list[ValidationRule]) -> dict:
    """Map evidence fields to rules that use them."""
    mapping = {}
    
    for rule in rules:
        for field in rule.evidence_fields:
            if field not in mapping:
                mapping[field] = []
            mapping[field].append({
                "rule_id": rule.rule_id,
                "category": rule.category,
                "boundary_class": rule.boundary_class,
                "classification": rule.classification,
            })
    
    return mapping

def main():
    """Generate Spike 1 outputs."""
    
    print("="*60)
    print("EQ-0013 Spike 1: Validation Capability Discovery")
    print("="*60)
    print()
    
    # Discover validation capabilities
    rules = discover_validation_capabilities()
    
    print(f"Discovered {len(rules)} validation rules")
    print()
    
    # Classify rules
    classifications = classify_rules(rules)
    print("Rule Classifications:")
    for classification, rule_ids in classifications.items():
        print(f"  {classification}: {len(rule_ids)} rules")
        if rule_ids:
            print(f"    {', '.join(rule_ids)}")
    print()
    
    # Generate registry
    registry = generate_validation_rule_registry(rules)
    
    # Save registry
    registry_path = "data/reports/eq0013_spike1_validation_rule_registry.json"
    with open(registry_path, "w") as f:
        json.dump(registry, f, indent=2)
    print(f"✓ Saved Validation Rule Registry: {registry_path}")
    
    # Generate evidence-to-rule mapping
    mapping = generate_evidence_to_rule_mapping(rules)
    mapping_path = "data/reports/eq0013_spike1_evidence_to_rule_mapping.json"
    with open(mapping_path, "w") as f:
        json.dump(mapping, f, indent=2)
    print(f"✓ Saved Evidence-to-Rule Mapping: {mapping_path}")
    
    # Generate classification summary
    summary = {
        "total_rules": len(rules),
        "classifications": {k: len(v) for k, v in classifications.items()},
        "boundary_classes": {},
        "evidence_coverage": {},
    }
    
    # Boundary class distribution
    for rule in rules:
        bc = rule.boundary_class
        if bc not in summary["boundary_classes"]:
            summary["boundary_classes"][bc] = 0
        summary["boundary_classes"][bc] += 1
    
    # Evidence field coverage
    for field in EVIDENCE_FIELDS.keys():
        field_rules = [r for r in rules if field in r.evidence_fields and r.classification in ["Supported", "Multiple Fields"]]
        summary["evidence_coverage"][field] = len(field_rules)
    
    summary_path = "data/reports/eq0013_spike1_classification_summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"✓ Saved Classification Summary: {summary_path}")
    
    print()
    print("="*60)
    print("Spike 1 Discovery Complete")
    print("="*60)
    print()
    print("Next: Create Spike 1 Evidence Report")

if __name__ == "__main__":
    main()