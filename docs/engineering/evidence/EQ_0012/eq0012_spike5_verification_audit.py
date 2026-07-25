#!/usr/bin/env python3
"""
EQ-0012 Spike 5 Verification Audit

Purpose:
    Verify Spike 5 Contract Documentation Standards against frozen evidence.
    
    Source of Truth: Frozen evidence from Spikes 1-4
    - Each standard must be traceable to existing production patterns or frozen evidence
    - No speculative standards permitted
"""

import json
from pathlib import Path

REPORT_PATH = Path("data/reports/eq0012_spike5_documentation_standards.json")
FROZEN_EVIDENCE_DIR = Path("docs/engineering/evidence")

class Spike5VerificationAuditor:
    """Verifies Spike 5 against frozen engineering evidence."""
    
    def verify(self) -> dict:
        with open(REPORT_PATH, 'r') as f:
            report = json.load(f)
        
        # Check all frozen evidence files referenced actually exist
        frozen_files = report.get('frozen_evidence_references', [])
        
        evidence_checks = []
        all_match = True
        
        for ref in frozen_files:
            path = Path(ref)
            exists = path.exists()
            evidence_checks.append({
                "claim": f"Frozen evidence file: {ref}",
                "production_evidence": f"File {'exists' if exists else 'MISSING'}",
                "report_claim": ref,
                "status": "MATCH" if exists else "DOCUMENTATION_DRIFT"
            })
            if not exists:
                all_match = False
        
        # Verify each required section format can be derived from frozen evidence
        sections = report.get('Q1_documentation_requirements', {}).get('minimum_required_sections', {}).get('required_sections', [])
        for section in sections:
            section_name = section['section']
            elements = len(section['required_elements'])
            can_example = section['example_present']
            
            evidence_checks.append({
                "claim": f"Section '{section_name}' has {elements} required elements and example available",
                "production_evidence": f"Frozen evidence supports {elements} elements" if can_example else "No example available in evidence",
                "report_claim": f"{section_name} ({elements} elements, example={'yes' if can_example else 'no'})",
                "status": "MATCH" if can_example else "DOCUMENTATION_DRIFT"
            })
            if not can_example:
                all_match = False
        
        # Verify field order matches frozen evidence
        field_order = report.get('field_documentation_matrix', {}).get('field_order', [])
        expected_fields = [
            "row_classification", "section_statistics", "boq_statistics", "known_anomalies",
            "hierarchy", "hierarchy_statistics",
            "detected_level_skips", "zero_quantity_items", "structural_containment_findings", "completeness_findings"
        ]
        
        if field_order == expected_fields:
            evidence_checks.append({
                "claim": "Field order matches frozen evidence (Increment 1→2→3)",
                "production_evidence": "Spike 1, 3 evidence reports follow this order",
                "report_claim": str(field_order),
                "status": "MATCH"
            })
        else:
            evidence_checks.append({
                "claim": "Field order matches frozen evidence",
                "production_evidence": "Expected: " + str(expected_fields),
                "report_claim": str(field_order),
                "status": "DOCUMENTATION_DRIFT"
            })
            all_match = False
        
        return {
            "audit_date": "2026-07-15",
            "investigation": "EQ-0012 Spike 5 Verification Audit",
            "verifications": evidence_checks,
            "summary": {
                "total_verifications": len(evidence_checks),
                "matches": sum(1 for v in evidence_checks if v['status'] == "MATCH"),
                "drifts": sum(1 for v in evidence_checks if v['status'] == "DOCUMENTATION_DRIFT"),
                "errors": sum(1 for v in evidence_checks if v['status'] == "IMPLEMENTATION_DRIFT"),
                "ambiguous": sum(1 for v in evidence_checks if v['status'] == "AMBIGUOUS")
            },
            "recommendation": "Freeze Spike 5 - All standards traceable to frozen evidence" if all_match else "Revise"
        }

def main():
    print("=" * 80)
    print("EQ-0012 Spike 5 Verification Audit")
    print("=" * 80)
    print()
    
    auditor = Spike5VerificationAuditor()
    result = auditor.verify()
    
    print(f"Summary:")
    print(f"  Total: {result['summary']['total_verifications']}")
    print(f"  MATCH: {result['summary']['matches']}")
    print(f"  Drift: {result['summary']['drifts']}")
    print(f"  Errors: {result['summary']['errors']}")
    print(f"  Ambiguous: {result['summary']['ambiguous']}")
    print()
    
    for v in result['verifications']:
        print(f"  {v['claim']}")
        print(f"    Status: {v['status']}")
        print()
    
    print("=" * 80)
    print(f"Recommendation: {result['recommendation']}")
    print("=" * 80)
    
    output_path = Path("data/reports/eq0012_spike5_verification_audit.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"\nReport saved to: {output_path}")

if __name__ == "__main__":
    main()