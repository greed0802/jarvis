#!/usr/bin/env python3
"""
EQ-0012 Spike 5: Contract Documentation Standards

Purpose:
    Define documentation requirements for the BOQ Intelligence Public Evidence Contract.
    
    Source of Truth: Production code at src/jarvis/parsers/costx/
    Previous Spikes: Spikes 1-4 (all frozen)

Engineering Questions:
    Q1: What documentation is required for each evidence field?
    Q2: How are field semantics specified?
    Q3: How are data structure invariants documented?
    Q4: How are evidence constraints described?
    Q5: How is evidence traceability maintained?
    Q6: What format should the contract document follow?

Investigation Rules:
    - Every statement must trace to production implementation
    - Every standard must trace to frozen engineering evidence
    - Never infer; if evidence doesn't exist, record "No engineering evidence available"
"""

import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class DocumentationSection:
    """A section specification for the contract document."""
    name: str
    purpose: str
    required_elements: List[str]
    format: str
    example_present: bool  # Whether an example can be derived from production


@dataclass
class EvidenceFieldDoc:
    """Documentation specification for a single evidence field."""
    field_name: str
    required_sections: List[str]
    type_format: str
    semantics_format: str
    invariant_format: str
    traceability_format: str


class DocumentationStandardsAnalyzer:
    """Analyzes and defines contract documentation standards."""
    
    def collect_requirements(self) -> Dict:
        """Collect documentation requirements based on frozen evidence."""
        
        sections = self._define_document_sections()
        field_docs = self._define_field_documentation()
        format_spec = self._define_format_specification()
        traceability = self._define_traceability_standards()
        
        return {
            "investigation": "EQ-0012 Spike 5: Contract Documentation Standards",
            "date": "2026-07-15",
            "source_of_truth": "src/jarvis/parsers/costx/",
            "frozen_evidence_references": [
                "docs/engineering/evidence/EQ_0012_Spike1_Evidence_Report_Current_Evidence_Inventory.md",
                "docs/engineering/evidence/EQ_0012_Spike2_Evidence_Report_Contract_Versioning_Policy.md",
                "docs/engineering/evidence/EQ_0012_Spike3_Evidence_Report_Contract_Invariants.md",
                "docs/engineering/evidence/EQ_0012_Spike4_Evidence_Report_Consumer_Access_Patterns.md"
            ],
            
            "Q1_documentation_requirements": {
                "question": "What documentation is required for each evidence field?",
                "evidence": "Based on analysis of 10 evidence fields from Spike 1, verification patterns from Spike 3",
                "minimum_required_sections": sections
            },
            
            "Q2_semantics_specification": {
                "question": "How are field semantics specified?",
                "evidence": "Based on EQ-0010, EQ-0011 engineering evidence and production field meanings",
                "format": format_spec['semantics_format']
            },
            
            "Q3_invariant_documentation": {
                "question": "How are data structure invariants documented?",
                "evidence": "Based on 70 invariants documented in Spike 3",
                "format": format_spec['invariant_format']
            },
            
            "Q4_constraint_description": {
                "question": "How are evidence constraints described?",
                "evidence": "Based on production implementation constraints (optionality, dependencies, determinism)",
                "format": format_spec['constraint_format']
            },
            
            "Q5_traceability_maintenance": {
                "question": "How is evidence traceability maintained?",
                "evidence": "Based on engineering evidence chain from EQ-0007 through EQ-0012",
                "standards": traceability
            },
            
            "Q6_contract_document_format": {
                "question": "What format should the contract document follow?",
                "evidence": "Based on existing documentation patterns and Spike 2 versioning policy",
                "format": sections
            },
            
            "field_documentation_matrix": field_docs,
            
            "recommendation": self._generate_recommendation()
        }
    
    def _define_document_sections(self) -> Dict:
        """Q6 & Q1: Define required document sections."""
        return {
            "required_sections": [
                {
                    "section": "Contract Header",
                    "purpose": "Establish contract identity, version, status, and authority",
                    "required_elements": [
                        "Contract title: 'BOQ Intelligence Public Evidence Contract vX.Y.Z'",
                        "Version number (MAJOR.MINOR.PATCH)",
                        "Status (Candidate/Approved/Deprecated)",
                        "Date of last revision",
                        "Engineering Question reference (EQ-0012)",
                        "Governance document reference (Engineering_Governance.md v1.0)",
                        "Principle statement"
                    ],
                    "format": "Markdown heading + metadata block",
                    "example_present": True
                },
                {
                    "section": "Contract Overview",
                    "purpose": "Describe contract purpose, scope, and relationship to BOQ Intelligence",
                    "required_elements": [
                        "Contract purpose statement",
                        "Scope boundaries (what is in/out of scope)",
                        "Relationship to BOQ Intelligence Increments 1-3",
                        "Consumer architecture context (Evidence Producer → Contract → Consumer)",
                        "First principle statement"
                    ],
                    "format": "Markdown prose with bullet points",
                    "example_present": True
                },
                {
                    "section": "Versioning Policy",
                    "purpose": "Document versioning scheme and compatibility rules",
                    "required_elements": [
                        "Version identity (Semantic Versioning MAJOR.MINOR.PATCH)",
                        "MAJOR breaking changes list",
                        "MINOR non-breaking additions list",
                        "PATCH internal corrections list",
                        "Policy notes on required fields and tuples",
                        "16 consumer guarantees (G-01 through G-16)"
                    ],
                    "format": "Table-based format as defined in Spike 2",
                    "example_present": True
                },
                {
                    "section": "Deprecation Lifecycle",
                    "purpose": "Document how obsolete fields are retired",
                    "required_elements": [
                        "Three-phase model (Announcement → Notice → Removal)",
                        "Governance gate requirements",
                        "Minimum deprecation period (one full MAJOR version)"
                    ],
                    "format": "Flow diagram + prose",
                    "example_present": True
                },
                {
                    "section": "Consumer Access Patterns",
                    "purpose": "Document how consumers should import and use the contract",
                    "required_elements": [
                        "5 stable import paths",
                        "9 must-not-import symbols",
                        "Recommended access pattern with code example",
                        "Consumer usage flow"
                    ],
                    "format": "Code blocks + prose",
                    "example_present": True
                },
                {
                    "section": "Evidence Field Specifications",
                    "purpose": "Document each evidence field with type, semantics, invariants, and traceability",
                    "required_elements": [
                        "For each of 10 evidence fields:",
                        "  - Field name and type annotation (from production)",
                        "  - Required or optional status",
                        "  - Evidence classification (Observation/Hierarchy/Detection)",
                        "  - Semantics description",
                        "  - Structural invariants table",
                        "  - Semantic invariants table",
                        "  - Cross-field dependencies",
                        "  - Traceability to engineering evidence",
                        "  - Engineering boundary statement"
                    ],
                    "format": "Per-field template (see Field Documentation Template below)",
                    "example_present": True
                },
                {
                    "section": "BOQHeaderNode Specification",
                    "purpose": "Document the BOQHeaderNode frozen dataclass used by hierarchy evidence",
                    "required_elements": [
                        "Field-by-field specification",
                        "Structural invariants",
                        "Semantic meaning"
                    ],
                    "format": "Table-based",
                    "example_present": True
                },
                {
                    "section": "Contract Invariants Summary",
                    "purpose": "Summarize all contract invariants across all fields",
                    "required_elements": [
                        "Total invariant count (70: 39 structural, 31 semantic)",
                        "Universal invariants (immutability, determinism, provenance)",
                        "Structural invariant categories (presence, type, shape, immutability)",
                        "Semantic invariant categories (determinism, provenance, boundary, meaning, reproducibility)",
                        "Violation handling policy"
                    ],
                    "format": "Summary tables + prose",
                    "example_present": True
                }
            ],
            "total_required_sections": 8
        }
    
    def _define_field_documentation(self) -> Dict:
        """Define per-field documentation template."""
        return {
            "per_field_template": {
                "field_specification": {
                    "field_name": "string",
                    "type_annotation": "Exact production type from boq_intelligence.py",
                    "required": "boolean",
                    "classification": "string (Observation/Hierarchy/Detection)",
                    "production_line": "Line number in boq_intelligence.py",
                    "increment": "integer (1, 2, or 3)"
                },
                "semantics": {
                    "description": "Human-readable description of field meaning",
                    "engineering_boundary": "Statement confirming observation/detection only, no decision language"
                },
                "structural_invariants": [
                    {
                        "invariant_id": "string (e.g., SI-RC-01)",
                        "category": "string (presence/type/shape/immutability)",
                        "description": "string",
                        "verification": "string (assertion method)",
                        "violation_impact": "string (MAJOR/MINOR)"
                    }
                ],
                "semantic_invariants": [
                    {
                        "invariant_id": "string (e.g., SE-RC-01)",
                        "category": "string (determinism/provenance/boundary/meaning/reproducibility)",
                        "description": "string",
                        "verification": "string",
                        "violation_impact": "string (MAJOR/MINOR)"
                    }
                ],
                "cross_field_dependencies": ["string"],
                "traceability": {
                    "engineering_evidence": "Reference to frozen EQ report",
                    "production_location": "File and line number",
                    "previous_eq": "Engineering Question that established this evidence"
                }
            },
            "field_order": [
                "row_classification",
                "section_statistics",
                "boq_statistics",
                "known_anomalies",
                "hierarchy",
                "hierarchy_statistics",
                "detected_level_skips",
                "zero_quantity_items",
                "structural_containment_findings",
                "completeness_findings"
            ],
            "note": "Field order follows Increment structure: 1 (observation) → 2 (hierarchy) → 3 (detection)"
        }
    
    def _define_format_specification(self) -> Dict:
        """Q2-Q4: Define format specifications."""
        return {
            "semantics_format": {
                "format": "Template-based per field",
                "required_components": [
                    {
                        "component": "Description",
                        "format": "Single paragraph (2-3 sentences)",
                        "example": "Maps row type strings ('Head', 'Note', 'Section', 'Item', 'Other') to their integer counts within the BOQ worksheet. Provides a summary of row type distribution."
                    },
                    {
                        "component": "Meaning",
                        "format": "Bullet points explaining what each key/value represents",
                        "example": "- Keys: row type identifiers; Values: occurrence counts",
                        "evidence": "Spike 3 SI-RC-04"
                    },
                    {
                        "component": "Engineering Boundary",
                        "format": "Single sentence confirming classification",
                        "example": "This field represents observation only — no decision language or assessment.",
                        "evidence": "EQ-0011"
                    }
                ]
            },
            "invariant_format": {
                "format": "Table-based per field",
                "required_columns": [
                    "ID",
                    "Category",
                    "Description",
                    "Verification",
                    "Violation Impact"
                ],
                "example_row": "| SI-RC-01 | presence | Field must always exist and never be None | Assert field is not None | MAJOR |",
                "note": "Tables are split into structural and semantic sections, following Spike 3 format"
            },
            "constraint_format": {
                "format": "Inline within field specification",
                "required_components": [
                    {
                        "component": "Optionality",
                        "format": "Required or Optional (with parameter controlling presence)",
                        "example": "Required (always present)",
                        "example_optional": "Optional (controlled by include_detection parameter)"
                    },
                    {
                        "component": "Field Relationships",
                        "format": "List of cross-field dependencies",
                        "example": "Dependencies: hierarchy, row_classification"
                    },
                    {
                        "component": "Version Stability",
                        "format": "Reference to versioning classification",
                        "example": "MAJOR version-locked (per Spike 2 policy)"
                    }
                ]
            }
        }
    
    def _define_traceability_standards(self) -> Dict:
        """Q5: Define traceability standards."""
        return {
            "traceability_requirements": {
                "per_field": [
                    {
                        "requirement": "Engineering Evidence Reference",
                        "format": "Reference to frozen EQ evidence report",
                        "example": "Evidence: EQ-0010 Spike 4 (hierarchy reconstruction algorithm)",
                        "evidence": "boq_intelligence.py docstrings follow this pattern"
                    },
                    {
                        "requirement": "Production Location",
                        "format": "File path and line numbers",
                        "example": "Production: boq_intelligence.py lines 48-64",
                        "evidence": "Spike 3 verification methodology"
                    },
                    {
                        "requirement": "Previous EQ Reference",
                        "format": "EQ identifier that established this evidence",
                        "example": "Authority: EQ-0007 (Increment 1)",
                        "evidence": "boq_intelligence.py module docstring"
                    },
                    {
                        "requirement": "Contract Reference",
                        "format": "Spike/Evidence report where documented",
                        "example": "Contract Documentation: Spike 1, Spike 3",
                        "evidence": "This investigation"
                    }
                ],
                "document_level": [
                    {
                        "requirement": "Source of Truth Statement",
                        "format": "Explicit statement in contract header",
                        "example": "Source of Truth: src/jarvis/parsers/costx/boq_intelligence.py"
                    },
                    {
                        "requirement": "Governance Reference",
                        "format": "Governance document version",
                        "example": "Governance: Engineering_Governance.md v1.0"
                    },
                    {
                        "requirement": "Verification Audit Record",
                        "format": "Reference to verification audit finding",
                        "example": "Verification: 10 MATCH (see Spike 3 Verification Audit)"
                    }
                ]
            },
            "traceability_chain": {
                "description": "Every contract field must trace through this chain:",
                "chain": [
                    "Engineering Question (EQ-0007, EQ-0010, EQ-0011)",
                    "→ Spike Investigation Reports",
                    "→ Production Implementation (boq_intelligence.py)",
                    "→ Frozen Evidence Report (Spike 1-4)",
                    "→ Evidence Contract v1.0 (this document)",
                    "→ Verification Audit"
                ],
                "principle": "Documentation never defines production. Production defines documentation."
            }
        }
    
    def _generate_recommendation(self) -> Dict:
        """Generate final recommendation."""
        return {
            "recommendation": "Adopt documented template standards for Evidence Contract v1.0",
            "rationale": "All required format elements are derivable from existing frozen evidence. No speculative formats needed.",
            "key_requirements": [
                "8 required document sections covering all contract aspects",
                "Per-field template with 5 required specification blocks (field spec, semantics, structural invariants, semantic invariants, traceability)",
                "10 evidence fields documented in increment order",
                "70 invariants documented per table-based format",
                "5 stable import paths documented with code examples",
                "All claims must include traceability to production or engineering evidence"
            ],
            "evidence": "Spikes 1-4 frozen evidence, boq_intelligence.py production code"
        }

def main():
    """Execute Spike 5 analysis."""
    print("=" * 80)
    print("EQ-0012 Spike 5: Contract Documentation Standards")
    print("=" * 80)
    print()
    
    analyzer = DocumentationStandardsAnalyzer()
    findings = analyzer.collect_requirements()
    
    print(f"Investigation: {findings['investigation']}")
    print(f"Date: {findings['date']}")
    print()
    
    print("Q1 - Documentation Requirements:")
    print(f"  Required sections: {findings['Q1_documentation_requirements']['minimum_required_sections']['total_required_sections']}")
    for section in findings['Q1_documentation_requirements']['minimum_required_sections']['required_sections']:
        print(f"    - {section['section']}")
        print(f"      Elements: {len(section['required_elements'])}")
    print()
    
    print("Q5 - Traceability Standards:")
    print(f"  Per-field trace requirements: {len(findings['Q5_traceability_maintenance']['standards']['traceability_requirements']['per_field'])}")
    print(f"  Document-level trace requirements: {len(findings['Q5_traceability_maintenance']['standards']['traceability_requirements']['document_level'])}")
    print()
    
    print("Field Documentation Template:")
    template = findings['field_documentation_matrix']['per_field_template']
    print(f"  Field specification: {len(template['field_specification'])} fields")
    print(f"  Structural invariants: table format, 4 columns")
    print(f"  Semantic invariants: table format, 4 columns")
    print(f"  Cross-field dependencies: list format")
    print(f"  Traceability: 3 required references")
    print()
    
    print("=" * 80)
    print(f"Recommendation: {findings['recommendation']['recommendation']}")
    print(f"Rationale: {findings['recommendation']['rationale']}")
    print("=" * 80)
    
    # Save report
    output_path = Path("data/reports/eq0012_spike5_documentation_standards.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(findings, f, indent=2)
    
    print(f"\nFull report saved to: {output_path}")

if __name__ == "__main__":
    main()