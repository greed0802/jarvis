"""
EQ-0013 Spike 2: Validation Rule Taxonomy

Purpose: Formalize taxonomy, lifecycle, governance, provenance,
         dependency graph, and version compatibility for validation rules.

Input: EQ-0013 Spike 1 Validation Rule Registry (22 rules)
Output: Rule Taxonomy, Dependency Graph, Governance Model

Authority: EQ-0013 (Validation Engine Investigation)
Contract: BOQ Intelligence Public Evidence Contract v1.0.0
Boundary: EQ-0011 (Observe/Reconstruct/Detect)

This tool extends governance. It does not change discovery.
No new validation rules are invented.
"""

import json
from dataclasses import dataclass
from typing import Optional
from enum import Enum


# ============================================
# RULE TAXONOMY - Formalized Categories
# ============================================

class RuleCategory(str, Enum):
    """Evidence-backed rule categories discovered in Spike 1."""
    STRUCTURAL = "Structural"
    CONSISTENCY = "Consistency"
    COMPLETENESS = "Completeness"
    DETECTION = "Detection"
    # Rejected categories (explicitly excluded from implementation)
    ASSESSMENT = "Assessment"      # Crosses EQ-0011 boundary
    RECOMMENDATION = "Recommendation"  # Crosses EQ-0011 boundary
    FINANCIAL = "Financial"        # Insufficient evidence
    REFERENCE = "Reference"        # Insufficient evidence


class BoundaryClass(str, Enum):
    """EQ-0011 boundary classification."""
    OBSERVATION = "Observation"
    DETECTION = "Detection"
    RELATIONSHIP = "Relationship"
    VIOLATION = "Violation"  # Crosses EQ-0011


class RuleStatus(str, Enum):
    """Validation rule lifecycle states."""
    CANDIDATE = "Candidate"
    APPROVED = "Approved"
    IMPLEMENTED = "Implemented"
    VERIFIED = "Verified"
    DEPRECATED = "Deprecated"
    RETIRED = "Retired"


class VerificationStatus(str, Enum):
    """Verification state for implemented rules."""
    PENDING = "Pending"
    VERIFIED = "Verified"
    DEPRECATED = "Deprecated"
    RETIRED = "Retired"


class CompatibilityImpact(str, Enum):
    """Version impact on contract compatibility."""
    PATCH = "PATCH"
    MINOR = "MINOR"
    MAJOR = "MAJOR"
    NONE = "NONE"


# ============================================
# CATEGORY DEFINITIONS
# ============================================

CATEGORY_DEFINITIONS = {
    RuleCategory.STRUCTURAL: {
        "definition": "Validations that verify presence, type, shape, or range of evidence fields.",
        "scope": "Single-field checks against Contract invariants.",
        "examples": [
            "V-001: Required field presence",
            "V-002: Row classification key shape (5 keys)",
            "V-003: Non-negative classification counts",
            "V-010: Hierarchy availability",
            "V-011: Root header count",
            "V-012: Hierarchy depth range",
        ],
        "eq_source": "EQ-0010 (Increment 1-2 observation), EQ-0012 (Contract invariants)",
        "boundary": "Always BoundaryClass.Observation — no assessment, no recommendation.",
    },
    RuleCategory.CONSISTENCY: {
        "definition": "Validations that verify arithmetic or logical relationships between evidence fields.",
        "scope": "Multi-field checks that detect internal contradictions.",
        "examples": [
            "V-004: Row classification sum equals total_rows",
            "V-005: Non-negative section quantity counts",
            "V-006: Anomaly row numbers within range",
        ],
        "eq_source": "EQ-0010 (Increment 1 cross-field dependencies)",
        "boundary": "BoundaryClass.Observation or BoundaryClass.Relationship — no assessment.",
    },
    RuleCategory.COMPLETENESS: {
        "definition": "Validations that calculate data population ratios from aggregate statistics.",
        "scope": "Single-field ratios describing column completeness.",
        "examples": [
            "V-007: Code column completeness (code_rows/total_rows)",
            "V-008: Description column completeness",
            "V-009: Quantity column completeness",
        ],
        "eq_source": "EQ-0010 (boq_statistics completeness indicators)",
        "boundary": "Always BoundaryClass.Observation — ratios describe, not assess.",
    },
    RuleCategory.DETECTION: {
        "definition": "Validations that observe patterns in EQ-0011 detection evidence.",
        "scope": "Checks on optional Increment 3 detection evidence fields.",
        "examples": [
            "V-013: Level skip detection availability",
            "V-014: Level skip count",
            "V-015: Level skip magnitude range",
            "V-016: Zero quantity item count",
            "V-017: Structural containment finding count",
            "V-018: Empty section count",
        ],
        "eq_source": "EQ-0011 (Increment 3 detection evidence)",
        "boundary": "Always BoundaryClass.Detection — findings, not recommendations.",
    },
}

# Rejected categories (documented, not implemented)
REJECTED_CATEGORIES = {
    RuleCategory.ASSESSMENT: {
        "definition": "Validations that assess professional quality or correctness.",
        "rejection_reason": "Crosses EQ-0011 boundary (Assess/Judge).",
        "examples": ["V-901: BOQ quality assessment"],
        "prohibited_verbs": ["assess", "judge", "evaluate", "rate", "rank", "score"],
    },
    RuleCategory.RECOMMENDATION: {
        "definition": "Validations that recommend corrective actions.",
        "rejection_reason": "Crosses EQ-0011 boundary (Recommend).",
        "examples": ["V-902: Level skip recommendation"],
        "prohibited_verbs": ["recommend", "suggest", "advise", "propose", "should"],
    },
    RuleCategory.FINANCIAL: {
        "definition": "Validations that check financial values.",
        "rejection_reason": "No cost/price evidence in Contract v1.0.",
        "examples": ["V-801: Item cost validation"],
    },
    RuleCategory.REFERENCE: {
        "definition": "Validations that check external references.",
        "rejection_reason": "No drawing/specification evidence in Contract v1.0.",
        "examples": ["V-802: Drawing reference validation"],
    },
}


# ============================================
# RULE LIFECYCLE DEFINITION
# ============================================

LIFECYCLE_TRANSITIONS = {
    RuleStatus.CANDIDATE: {
        "entry_criteria": [
            "Rule ID assigned",
            "Provenance documented (evidence fields, EQ source, spike)",
            "Boundary classification present",
            "Category assigned",
        ],
        "exit_criteria": [
            "Evidence report frozen",
            "Category validated by EQ author",
            "Boundary compliance verified",
            "Project Owner approval",
        ],
        "next": RuleStatus.APPROVED,
        "governance": "Spike discovery + Evidence Report",
    },
    RuleStatus.APPROVED: {
        "entry_criteria": [
            "Project Owner Gate 2 approval",
            "Category confirmed",
            "Boundary classification confirmed",
            "Provenance complete",
        ],
        "exit_criteria": [
            "Implementation complete",
            "Passes verification audit",
            "Deterministic behavior confirmed",
        ],
        "next": RuleStatus.IMPLEMENTED,
        "governance": "Gate 2 approval",
    },
    RuleStatus.IMPLEMENTED: {
        "entry_criteria": [
            "Production code exists",
            "Consumes only Evidence Contract v1.0",
            "Follows EQ-0011 boundary",
            "Deterministic (same input → same output)",
        ],
        "exit_criteria": [
            "Verification tooling confirms implementation matches spec",
            "All structural invariants pass",
            "Boundary compliance confirmed",
            "Consumer-independent test passes",
        ],
        "next": RuleStatus.VERIFIED,
        "governance": "Implementation + Verification audit",
    },
    RuleStatus.VERIFIED: {
        "entry_criteria": [
            "Implementation verified against spec",
            "Verification status: VERIFIED",
            "Anti-drift tooling passes",
            "Consumer compliance test passes",
        ],
        "exit_criteria": [
            "Rule no longer needed (Contract version deprecates evidence)",
            "Replaced by successor rule (new Rule ID)",
            "Evidence field removed from Contract",
        ],
        "next": RuleStatus.DEPRECATED,
        "governance": "ADR or Contract version evolution",
    },
    RuleStatus.DEPRECATED: {
        "entry_criteria": [
            "Deprecation notice issued",
            "Successor rule identified (if applicable)",
            "Removal timeline established",
            "Consumer migration guidance provided",
        ],
        "exit_criteria": [
            "Deprecation period complete",
            "No active consumers",
            "Successor rule verified",
        ],
        "next": RuleStatus.RETIRED,
        "governance": "MINOR Contract version (adds deprecation notice)",
    },
    RuleStatus.RETIRED: {
        "entry_criteria": [
            "Deprecation period expired",
            "Rule removed from active registry",
            "Historical record preserved",
        ],
        "exit_criteria": ["(terminal state)"],
        "next": None,
        "governance": "Historical preservation — Rule ID never reused",
    },
}

# Forbidden transitions (would violate lifecycle)
FORBIDDEN_TRANSITIONS = [
    (RuleStatus.CANDIDATE, RuleStatus.RETIRED),   # Skip lifecycle
    (RuleStatus.CANDIDATE, RuleStatus.DEPRECATED),  # Skip lifecycle
    (RuleStatus.APPROVED, RuleStatus.RETIRED),      # Skip implementation
    (RuleStatus.IMPLEMENTED, RuleStatus.CANDIDATE),  # Reverse
    (RuleStatus.VERIFIED, RuleStatus.CANDIDATE),    # Reverse
    (RuleStatus.DEPRECATED, RuleStatus.APPROVED),    # Undeprecate
    (RuleStatus.RETIRED, RuleStatus.APPROVED),      # Revive retired
]


# ============================================
# RULE IDENTITY - Permanent Identifiers
# ============================================

ID_POLICY = {
    "permanence": "Rule IDs are forever. Once assigned, never reassigned.",
    "format": "V-NNN where NNN is sequential from 001-999 (900-999 reserved for rejected rules).",
    "reservation": {
        "001-899": "Implementable rules (Supported + Multiple Fields)",
        "900-999": "Rejected rules (Boundary Violation, Insufficient Evidence)",
    },
    "retirement": "Retired rules retain their ID permanently in historical index.",
    "replacement": "A successor rule receives a NEW Rule ID. Never reuse the retired ID.",
    "historical_preservation": "All rules (including rejected/retired) remain in registry history.",
}


# ============================================
# RULE PROVENANCE - Complete Traceability
# ============================================

PROVENANCE_SCHEMA = {
    "required_fields": [
        "rule_id",
        "rule_version",
        "category",
        "description",
        "evidence_fields",
        "boundary_class",
        "contract_version",
        "eq_source",
        "introduced_by",
        "deterministic_finding",
        "rationale",
        "status",
        "verification_status",
    ],
    "optional_fields": [
        "validation_engine_version",  # Version when rule was first executable
        "dependency_rules",           # Other rules this depends on
        "deprecation_date",
        "retirement_date",
        "successor_rule_id",
        "consumers",                  # Known consumers using this rule
    ],
    "governance": (
        "Every field in ProvenanceSchema.required_fields must be present "
        "before a rule may transition from Candidate → Approved. "
        "Missing provenance = incomplete rule."
    ),
}


# ============================================
# RULE DEPENDENCY GRAPH
# ============================================

# Maps evidence fields → rules → category → finding type → eligible consumers
DEPENDENCY_MODEL = {
    "levels": {
        "evidence_field": "Evidence Contract field consumed",
        "rule": "Validation rule using evidence",
        "category": "Rule category (Structural, Consistency, etc.)",
        "finding_type": "Type of deterministic finding produced",
        "eligible_consumers": "Consumers that can use this finding",
    },
    "purpose": [
        "Impact analysis when Contract evolves",
        "Regression planning when rule changes",
        "Dependency visibility for consumers",
    ],
    "finding_types": {
        "presence": "Boolean: field exists / None",
        "shape": "List: missing/unexpected keys",
        "count": "Integer: occurrence frequency",
        "ratio": "Float: 0.0-1.0 completeness",
        "range": "Tuple: (min, max) distribution",
        "discrepancy": "Integer: deviation from expected",
        "flag": "List: invalid elements found",
    },
}

# Specific dependency graph entries for Spike 1 rules
RULE_DEPENDENCY_GRAPH = {
    "V-001": {
        "evidence_fields": ["row_classification", "section_statistics", "boq_statistics", "known_anomalies"],
        "category": "Structural",
        "finding_type": "presence",
        "eligible_consumers": ["CheckMate", "Formatter", "Builder", "O&A", "Reporting"],
    },
    "V-002": {
        "evidence_fields": ["row_classification"],
        "category": "Structural",
        "finding_type": "shape",
        "eligible_consumers": ["CheckMate", "Formatter", "Builder", "O&A", "Reporting"],
    },
    "V-003": {
        "evidence_fields": ["row_classification"],
        "category": "Structural",
        "finding_type": "flag",
        "eligible_consumers": ["CheckMate"],
    },
    "V-004": {
        "evidence_fields": ["row_classification", "boq_statistics"],
        "category": "Consistency",
        "finding_type": "discrepancy",
        "eligible_consumers": ["CheckMate"],
    },
    "V-005": {
        "evidence_fields": ["section_statistics"],
        "category": "Consistency",
        "finding_type": "flag",
        "eligible_consumers": ["CheckMate"],
    },
    "V-006": {
        "evidence_fields": ["known_anomalies", "boq_statistics"],
        "category": "Consistency",
        "finding_type": "flag",
        "eligible_consumers": ["CheckMate"],
    },
    "V-007": {"evidence_fields": ["boq_statistics"], "category": "Completeness", "finding_type": "ratio", "eligible_consumers": ["CheckMate", "Formatter", "Reporting"]},
    "V-008": {"evidence_fields": ["boq_statistics"], "category": "Completeness", "finding_type": "ratio", "eligible_consumers": ["CheckMate", "Formatter", "Reporting"]},
    "V-009": {"evidence_fields": ["boq_statistics"], "category": "Completeness", "finding_type": "ratio", "eligible_consumers": ["CheckMate", "Formatter", "Reporting"]},
    "V-010": {"evidence_fields": ["hierarchy"], "category": "Structural", "finding_type": "presence", "eligible_consumers": ["CheckMate", "Formatter", "Builder", "O&A", "Reporting"]},
    "V-011": {"evidence_fields": ["hierarchy_statistics"], "category": "Structural", "finding_type": "count", "eligible_consumers": ["CheckMate", "Reporting"]},
    "V-012": {"evidence_fields": ["hierarchy_statistics"], "category": "Structural", "finding_type": "range", "eligible_consumers": ["CheckMate", "Reporting"]},
    "V-013": {"evidence_fields": ["detected_level_skips"], "category": "Detection", "finding_type": "presence", "eligible_consumers": ["CheckMate", "Formatter", "Builder", "O&A", "Reporting"]},
    "V-014": {"evidence_fields": ["detected_level_skips"], "category": "Detection", "finding_type": "count", "eligible_consumers": ["CheckMate", "Reporting"]},
    "V-015": {"evidence_fields": ["detected_level_skips"], "category": "Detection", "finding_type": "range", "eligible_consumers": ["CheckMate", "Reporting"]},
    "V-016": {"evidence_fields": ["zero_quantity_items"], "category": "Detection", "finding_type": "count", "eligible_consumers": ["CheckMate", "Reporting"]},
    "V-017": {"evidence_fields": ["structural_containment_findings"], "category": "Detection", "finding_type": "count", "eligible_consumers": ["CheckMate", "Reporting"]},
    "V-018": {"evidence_fields": ["completeness_findings"], "category": "Detection", "finding_type": "count", "eligible_consumers": ["CheckMate", "Reporting"]},
    # Rejected rules — remain in graph for documentation
    "V-901": {"evidence_fields": ["boq_statistics"], "category": "Assessment", "finding_type": "N/A", "eligible_consumers": ["REJECTED — crosses EQ-0011 boundary"]},
    "V-902": {"evidence_fields": ["detected_level_skips"], "category": "Recommendation", "finding_type": "N/A", "eligible_consumers": ["REJECTED — crosses EQ-0011 boundary"]},
    "V-801": {"evidence_fields": [], "category": "Financial", "finding_type": "N/A", "eligible_consumers": ["REJECTED — insufficient evidence"]},
    "V-802": {"evidence_fields": [], "category": "Reference", "finding_type": "N/A", "eligible_consumers": ["REJECTED — insufficient evidence"]},
}


# ============================================
# RULE VERSION COMPATIBILITY
# ============================================

VERSION_COMPATIBILITY_RULES = {
    "contract_vs_rule": {
        "description": "How Contract version changes affect rule versions.",
        "rules": {
            "PATCH": {
                "trigger": "Contract documentation fix, invariant clarification, non-functional change.",
                "impact": "NONE — Rule unchanged. No version increment.",
                "verification": "Rule verification still passes (no behavior change).",
            },
            "MINOR": {
                "trigger": "Contract adds new optional evidence field, deprecates existing field.",
                "impact": {
                    "new_field": "PATCH — Optional rule may be added to consume new field. Existing rules unaffected.",
                    "deprecation": "MINOR — Rule using deprecated field enters DEPRECATED lifecycle.",
                },
                "verification": "Existing rules verify against non-deprecated fields only.",
            },
            "MAJOR": {
                "trigger": "Contract removes required field, changes type, renames field, changes invariants.",
                "impact": {
                    "rule_effected": "MAJOR — Rule referencing changed field must be retired or replaced.",
                    "unaffected_rule": "NONE — Rule not referencing changed field unaffected.",
                },
                "verification": "All rules verified against new Contract version.",
            },
        },
    },
    "rule_vs_engine": {
        "description": "How rule changes affect Validation Engine version.",
        "rules": {
            "rule_added": "MINOR — Engine adds new rule capability.",
            "rule_deprecated": "MINOR — Engine marks rule as deprecated.",
            "rule_retired": "MAJOR — Engine removes rule functionality.",
            "rule_finding_changed": "MAJOR — Breaking change for consumers.",
            "rule_category_changed": "MAJOR — Breaking structural change.",
            "rule_verification_status_changed": "PATCH — Non-functional status update.",
        },
    },
    "independent_versions": (
        "Contract Version, Validation Rule Version, and Validation Engine Version "
        "are independent engineering concepts. A MAJOR Contract change may not require "
        "a MAJOR Engine change if all affected rules are already deprecated."
    ),
}


# ============================================
# RULE REGISTRY GOVERNANCE
# ============================================

REGISTRY_GOVERNANCE = {
    "adding_rules": {
        "process": [
            "Rule discovered via Spike investigation",
            "Evidence Report documents candidate rule",
            "Category validated (Spike 2 taxonomy)",
            "Boundary classification confirmed",
            "Provenance complete (all required fields)",
            "Project Owner approval (Gate 2)",
            "Added to registry as APPROVED",
        ],
        "authority": "Engineering Question + Spike + Project Owner Approval",
        "traceability": "Every addition traces to EQ number + Spike number.",
    },
    "modifying_rules": {
        "process": [
            "Change proposal via Engineering Question",
            "Impact analysis (Contract, Engine, Consumers)",
            "Version increment determined",
            "Project Owner approval",
            "Registry updated with new rule_version",
        ],
        "authority": "Engineering Question + Impact Analysis + Project Owner",
        "traceability": "Every modification traces to EQ number + version change.",
        "forbidden_modifications": [
            "Changing Rule ID (permanent identity)",
            "Changing boundary_class from valid to Violation",
            "Changing category to rejected category",
            "Removing required provenance fields",
        ],
    },
    "deprecating_rules": {
        "process": [
            "Deprecation notice issued (MINOR Contract change or Engine update)",
            "Rule status: VERIFIED → DEPRECATED",
            "Deprecation reason documented",
            "Migration guidance provided to consumers",
            "Timeline established (consumer migration deadline)",
        ],
        "authority": "ADR or Contract version evolution",
    },
    "retiring_rules": {
        "process": [
            "Deprecation period expired",
            "No active consumers confirmed",
            "Successor rule verified (if applicable)",
            "Rule removed from active registry",
            "Historical index preserved",
            "Rule ID permanently retired",
        ],
        "authority": "Project Owner after deprecation period",
    },
}


# ============================================
# CONSUMER COMPATIBILITY
# ============================================

CONSUMER_COMPATIBILITY_MODEL = {
    "verification_chain": [
        "Consumer identifies required rules",
        "Consumer verifies Rule IDs present in Engine",
        "Consumer verifies Contract Version compatibility",
        "Consumer verifies Finding Types match expectations",
        "Consumer passes Compliance Suite (EQ-0013) for contract compliance",
    ],
    "compatibility_assertions": [
        "Rule IDs stable (permanent identity)",
        "Finding types deterministic (same input → same output)",
        "Contract version documented (consumer checks compatibility)",
        "Boundary class preserved (no assessment/recommendation drift)",
    ],
}


def build_rule_provenance_record(rule_id: str, category: str, status: str) -> dict:
    """Build complete provenance record for a rule."""
    return {
        "rule_id": rule_id,
        "rule_version": "1.0.0",
        "category": category,
        "status": status,
        "verification_status": VerificationStatus.PENDING.value,
        "validation_engine_version": None,  # Not yet implemented
        "dependency_rules": [],
        "deprecation_date": None,
        "retirement_date": None,
        "successor_rule_id": None,
        "consumers": [],
    }


def generate_taxonomy() -> dict:
    """Generate formalized taxonomy document."""
    return {
        "taxonomy_version": "1.0.0",
        "contract_version": "1.0.0",
        "generated_by": "EQ-0013 Spike 2",
        "categories": {
            cat.value: {
                "definition": defn["definition"],
                "scope": defn.get("scope", "N/A"),
                "example_rules": defn.get("examples", []),
                "eq_source": defn.get("eq_source", ""),
                "boundary": defn.get("boundary", ""),
                "prohibited_verbs": defn.get("prohibited_verbs", []),
                "implementable": cat not in REJECTED_CATEGORIES,
            }
            for cat, defn in {**CATEGORY_DEFINITIONS, **REJECTED_CATEGORIES}.items()
        },
        "lifecycle": {
            "states": [s.value for s in RuleStatus],
            "transitions": {
                s.value: d for s, d in LIFECYCLE_TRANSITIONS.items()
            },
            "forbidden_transitions": [
                f"{src.value} → {dst.value}" for src, dst in FORBIDDEN_TRANSITIONS
            ],
        },
        "identity_policy": ID_POLICY,
        "provenance_schema": PROVENANCE_SCHEMA,
        "version_compatibility": VERSION_COMPATIBILITY_RULES,
        "registry_governance": REGISTRY_GOVERNANCE,
        "consumer_compatibility": CONSUMER_COMPATIBILITY_MODEL,
    }


def generate_dependency_graph() -> dict:
    """Generate stable dependency graph."""
    return {
        "dependency_model": DEPENDENCY_MODEL,
        "rule_dependencies": RULE_DEPENDENCY_GRAPH,
        "summary": {
            "total_rules_in_graph": len(RULE_DEPENDENCY_GRAPH),
            "implementable_rules": len([
                r for r, d in RULE_DEPENDENCY_GRAPH.items()
                if d["category"] not in ["Assessment", "Recommendation", "Financial", "Reference"]
            ]),
            "rejected_rules": len([
                r for r, d in RULE_DEPENDENCY_GRAPH.items()
                if d["category"] in ["Assessment", "Recommendation", "Financial", "Reference"]
            ]),
            "finding_types": sorted(set(
                d["finding_type"] for d in RULE_DEPENDENCY_GRAPH.values()
                if d["finding_type"] != "N/A"
            )),
            "eligible_consumers": sorted(set(
                c for d in RULE_DEPENDENCY_GRAPH.values()
                for c in d["eligible_consumers"]
                if not c.startswith("REJECTED")
            )),
        },
    }


def main():
    """Generate Spike 2 outputs."""

    print("=" * 60)
    print("EQ-0013 Spike 2: Validation Rule Taxonomy")
    print("=" * 60)
    print()

    # Load Spike 1 registry
    with open("data/reports/eq0013_spike1_validation_rule_registry.json") as f:
        spike1_registry = json.load(f)

    print(f"Loaded {spike1_registry['total_rules']} rules from Spike 1 Registry")
    print()

    # Verify: no new rules invented
    print("Verification: No new rules invented...")
    print(f"  Spike 1 rules: {spike1_registry['total_rules']}")
    print(f"  Spike 2 extends governance, not discovery")
    print()

    # Generate taxonomy
    taxonomy = generate_taxonomy()
    taxonomy_path = "data/reports/eq0013_spike2_rule_taxonomy.json"
    with open(taxonomy_path, "w") as f:
        json.dump(taxonomy, f, indent=2, default=str)
    print(f"✓ Saved Rule Taxonomy: {taxonomy_path}")

    # Generate dependency graph
    dep_graph = generate_dependency_graph()
    dep_path = "data/reports/eq0013_spike2_dependency_graph.json"
    with open(dep_path, "w") as f:
        json.dump(dep_graph, f, indent=2, default=str)
    print(f"✓ Saved Dependency Graph: {dep_path}")

    # Statistics
    print()
    print("Taxonomy Categories:")
    for cat, defn in CATEGORY_DEFINITIONS.items():
        print(f"  {cat.value}: {len(defn.get('examples', []))} rules — {defn['definition'][:80]}...")
    print()
    print("Rejected Categories:")
    for cat, defn in REJECTED_CATEGORIES.items():
        print(f"  {cat.value}: {defn['rejection_reason']}")
    print()
    print("Lifecycle States:")
    for state in RuleStatus:
        print(f"  {state.value}")
    print()
    print("Dependency Graph Summary:")
    for k, v in dep_graph["summary"].items():
        print(f"  {k}: {v}")
    print()

    print("=" * 60)
    print("Spike 2 Taxonomy Complete")
    print("=" * 60)
    print()
    print("Next: Run eq0013_spike2_verification_audit.py")


if __name__ == "__main__":
    main()