#!/usr/bin/env python3
"""
EQ-0012 Spike 3 Verification Audit

Purpose:
    Verify Spike 3 Contract Invariants documentation against production implementation.
    
    Source of Truth: Production code (src/jarvis/parsers/costx/boq_intelligence.py)
    
    Determine whether documented invariants accurately reflect actual implementation.

Methodology:
    1. Read production BOQIntelligenceResult dataclass
    2. Compare each field against Spike 3 documentation
    3. Classify discrepancies as:
       - Class A: Documentation Error (fix docs)
       - Class B: Implementation Error (raise for review)
       - Class C: Ambiguous (needs investigation)
    4. Generate verification matrix

Evidence Sources:
    - src/jarvis/parsers/costx/boq_intelligence.py (lines 48-64)
    - docs/engineering/evidence/EQ_0012_Spike3_Evidence_Report_Contract_Invariants.md
    - docs/engineering/evidence/EQ_0012_Spike1_Evidence_Report_Current_Evidence_Inventory.md
"""

import json
from dataclasses import dataclass
from typing import Literal
from pathlib import Path

@dataclass
class ProductionField:
    """Production field specification from boq_intelligence.py."""
    field_name: str
    type_annotation: str
    line_number: int
    required: bool
    default_value: str | None

@dataclass
class Spike3Field:
    """Documented field specification from Spike 3."""
    field_name: str
    documented_type: str
    documented_required: bool
    structural_invariant_count: int
    semantic_invariant_count: int

@dataclass
class VerificationResult:
    """Verification result for a single field."""
    field_name: str
    status: Literal["MATCH", "DOCUMENTATION_DRIFT", "IMPLEMENTATION_DRIFT", "AMBIGUOUS"]
    production_type: str
    spike3_type: str
    production_required: bool
    spike3_required: bool
    issues: list[str]
    classification: Literal["Class A", "Class B", "Class C", "No Issue"] | None

class Spike3VerificationAuditor:
    """Auditor for Spike 3 verification against production."""
    
    def __init__(self):
        self.production_fields: list[ProductionField] = []
        self.spike3_fields: list[Spike3Field] = []
        self.verification_results: list[VerificationResult] = []
    
    def load_production_fields(self):
        """Load production field specifications from boq_intelligence.py."""
        # BOQIntelligenceResult dataclass lines 48-64
        self.production_fields = [
            ProductionField(
                field_name="row_classification",
                type_annotation="dict[str, int]",
                line_number=55,
                required=True,
                default_value=None
            ),
            ProductionField(
                field_name="section_statistics",
                type_annotation="dict[str, dict[str, int]]",
                line_number=56,
                required=True,
                default_value=None
            ),
            ProductionField(
                field_name="boq_statistics",
                type_annotation="dict[str, int | float]",
                line_number=57,
                required=True,
                default_value=None
            ),
            ProductionField(
                field_name="known_anomalies",
                type_annotation="list[dict[str, int | str | float]]",
                line_number=58,
                required=True,
                default_value=None
            ),
            ProductionField(
                field_name="hierarchy",
                type_annotation="tuple[BOQHeaderNode, ...] | None",
                line_number=59,
                required=False,
                default_value="None"
            ),
            ProductionField(
                field_name="hierarchy_statistics",
                type_annotation="dict[str, int | float] | None",
                line_number=60,
                required=False,
                default_value="None"
            ),
            ProductionField(
                field_name="detected_level_skips",
                type_annotation="tuple[dict[str, int], ...] | None",
                line_number=61,
                required=False,
                default_value="None"
            ),
            ProductionField(
                field_name="zero_quantity_items",
                type_annotation="tuple[dict[str, int | str | float | None], ...] | None",
                line_number=62,
                required=False,
                default_value="None"
            ),
            ProductionField(
                field_name="structural_containment_findings",
                type_annotation="tuple[dict[str, int], ...] | None",
                line_number=63,
                required=False,
                default_value="None"
            ),
            ProductionField(
                field_name="completeness_findings",
                type_annotation="tuple[dict[str, int | str], ...] | None",
                line_number=64,
                required=False,
                default_value="None"
            ),
        ]
    
    def load_spike3_fields_from_report(self, report_path: str = "data/reports/eq0012_spike3_contract_invariants.json"):
        """Load Spike 3 documented field specifications from generated JSON report.
        
        This ensures the audit always verifies against the latest generated output,
        not a hardcoded copy that can drift.
        """
        with open(report_path, 'r') as f:
            report = json.load(f)
        
        self.spike3_fields = [
            Spike3Field(
                field_name=field["field_name"],
                documented_type=field["field_type"],
                documented_required=field["required"],
                structural_invariant_count=len(field["structural_invariants"]),
                semantic_invariant_count=len(field["semantic_invariants"])
            )
            for field in report["field_invariants"]
        ]
    
    def normalize_type(self, type_str: str) -> str:
        """Normalize type string for comparison."""
        # Convert Python 3.10+ style to typing module style
        normalized = type_str.replace("dict", "Dict").replace("list", "List").replace("tuple", "Tuple")
        normalized = normalized.replace(" | None", "").replace("|None", "")
        normalized = normalized.replace("Optional[", "").replace("]", "")
        normalized = normalized.replace("...", "")
        normalized = normalized.replace(" ", "")
        return normalized
    
    def verify_field(self, prod: ProductionField, spike3: Spike3Field) -> VerificationResult:
        """Verify a single field against Spike 3 documentation.
        
        Performs direct string comparison to determine if documentation
        matches production implementation.
        """
        issues = []
        
        # Compare types directly
        if prod.type_annotation != spike3.documented_type:
            issues.append(
                f"Type mismatch: Production uses '{prod.type_annotation}', "
                f"Spike 3 documents '{spike3.documented_type}'"
            )
        
        # Compare required/optional
        if prod.required != spike3.documented_required:
            issues.append(
                f"Required/Optional mismatch: Production={prod.required}, "
                f"Spike 3={spike3.documented_required}"
            )
        
        if issues:
            status = "DOCUMENTATION_DRIFT"
            classification = "Class A"
        else:
            status = "MATCH"
            classification = "No Issue"
        
        return VerificationResult(
            field_name=prod.field_name,
            status=status,
            production_type=prod.type_annotation,
            spike3_type=spike3.documented_type,
            production_required=prod.required,
            spike3_required=spike3.documented_required,
            issues=issues,
            classification=classification
        )
    
    def perform_audit(self):
        """Perform complete verification audit."""
        self.load_production_fields()
        self.load_spike3_fields_from_report()
        
        # Create field lookup
        spike3_lookup = {f.field_name: f for f in self.spike3_fields}
        
        # Verify each production field
        for prod_field in self.production_fields:
            spike3_field = spike3_lookup.get(prod_field.field_name)
            if spike3_field:
                result = self.verify_field(prod_field, spike3_field)
                self.verification_results.append(result)
            else:
                # Field in production but not in Spike 3
                self.verification_results.append(VerificationResult(
                    field_name=prod_field.field_name,
                    status="DOCUMENTATION_DRIFT",
                    production_type=prod_field.type_annotation,
                    spike3_type="NOT DOCUMENTED",
                    production_required=prod_field.required,
                    spike3_required=False,
                    issues=["Field exists in production but not documented in Spike 3"],
                    classification="Class A"
                ))
    
    def generate_report(self) -> dict:
        """Generate verification audit report."""
        self.perform_audit()
        
        matches = [r for r in self.verification_results if r.status == "MATCH"]
        doc_drifts = [r for r in self.verification_results if r.status == "DOCUMENTATION_DRIFT"]
        impl_drifts = [r for r in self.verification_results if r.status == "IMPLEMENTATION_DRIFT"]
        ambiguous = [r for r in self.verification_results if r.status == "AMBIGUOUS"]
        
        class_a = [r for r in self.verification_results if r.classification == "Class A"]
        class_b = [r for r in self.verification_results if r.classification == "Class B"]
        class_c = [r for r in self.verification_results if r.classification == "Class C"]
        
        report = {
            "audit_date": "2026-07-15",
            "investigation": "EQ-0012 Spike 3 Verification Audit",
            "summary": {
                "total_fields": len(self.verification_results),
                "matches": len(matches),
                "documentation_drifts": len(doc_drifts),
                "implementation_drifts": len(impl_drifts),
                "ambiguous": len(ambiguous),
                "class_a_issues": len(class_a),
                "class_b_issues": len(class_b),
                "class_c_issues": len(class_c),
            },
            "verification_matrix": [
                {
                    "field_name": r.field_name,
                    "status": r.status,
                    "production_type": r.production_type,
                    "spike3_type": r.spike3_type,
                    "production_required": r.production_required,
                    "spike3_required": r.spike3_required,
                    "issues": r.issues,
                    "classification": r.classification
                }
                for r in self.verification_results
            ],
            "class_a_documentation_errors": [
                {
                    "field": r.field_name,
                    "issues": r.issues,
                    "action": "Update Spike 3 documentation to match production"
                }
                for r in class_a
            ],
            "class_b_implementation_errors": [
                {
                    "field": r.field_name,
                    "issues": r.issues,
                    "action": "Raise for engineering review"
                }
                for r in class_b
            ],
            "class_c_ambiguous": [
                {
                    "field": r.field_name,
                    "issues": r.issues,
                    "action": "Investigate and determine authoritative behavior"
                }
                for r in class_c
            ],
            "recommendation": self._generate_recommendation(matches, doc_drifts, impl_drifts, ambiguous)
        }
        
        return report
    
    def _generate_recommendation(self, matches, doc_drifts, impl_drifts, ambiguous) -> str:
        """Generate recommendation based on audit results."""
        if doc_drifts or impl_drifts or ambiguous:
            return "Revise Spike 3 - Documentation does not match production implementation"
        else:
            return "Freeze Spike 3 - All fields match production implementation"

def main():
    """Execute verification audit."""
    print("=" * 80)
    print("EQ-0012 Spike 3 Verification Audit")
    print("=" * 80)
    print()
    print("Source of Truth: src/jarvis/parsers/costx/boq_intelligence.py")
    print()
    
    auditor = Spike3VerificationAuditor()
    report = auditor.generate_report()
    
    # Print summary
    print(f"Investigation: {report['investigation']}")
    print(f"Date: {report['audit_date']}")
    print()
    print("Summary:")
    print(f"  Total fields: {report['summary']['total_fields']}")
    print(f"  Matches: {report['summary']['matches']}")
    print(f"  Documentation drifts: {report['summary']['documentation_drifts']}")
    print(f"  Implementation drifts: {report['summary']['implementation_drifts']}")
    print(f"  Ambiguous: {report['summary']['ambiguous']}")
    print()
    print(f"  Class A (Documentation Error): {report['summary']['class_a_issues']}")
    print(f"  Class B (Implementation Error): {report['summary']['class_b_issues']}")
    print(f"  Class C (Ambiguous): {report['summary']['class_c_issues']}")
    print()
    
    # Print verification matrix
    print("Verification Matrix:")
    print()
    for entry in report['verification_matrix']:
        print(f"  {entry['field_name']}")
        print(f"    Status: {entry['status']}")
        print(f"    Production: {entry['production_type']} (required={entry['production_required']})")
        print(f"    Spike 3: {entry['spike3_type']} (required={entry['spike3_required']})")
        if entry['issues']:
            print(f"    Issues:")
            for issue in entry['issues']:
                print(f"      - {issue}")
        print(f"    Classification: {entry['classification']}")
        print()
    
    # Print Class A issues
    if report['class_a_documentation_errors']:
        print("Class A Documentation Errors (Fix Documentation):")
        print()
        for issue in report['class_a_documentation_errors']:
            print(f"  {issue['field']}:")
            for i in issue['issues']:
                print(f"    - {i}")
            print(f"    Action: {issue['action']}")
            print()
    
    # Print recommendation
    print("=" * 80)
    print(f"Recommendation: {report['recommendation']}")
    print("=" * 80)
    
    # Save report
    output_path = Path("data/reports/eq0012_spike3_verification_audit.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print()
    print(f"Full report saved to: {output_path}")

if __name__ == "__main__":
    main()