"""
EQ-0013 Spike 3: Validation Engine Scope & Responsibilities

Purpose: Define what belongs inside the Validation Engine and what explicitly
         belongs outside it. Establish engine/consumer boundary.

Question: What belongs inside the Validation Engine, and what explicitly belongs outside it?

Authority: EQ-0013 (Validation Engine Investigation)
Contract: BOQ Intelligence Public Evidence Contract v1.0.0
Registry: Validation Rule Registry (22 rules, 4 categories)
Boundary: EQ-0011 (Observe/Reconstruct/Detect)

This tool determines engineering responsibility only.
No implementation. No CheckMate design. No runtime services.
"""

import json
from dataclasses import dataclass
from typing import List, Dict
from enum import Enum

# ============================================
# VALIDATION ENGINE SCOPE
# ============================================

class ResponsibilityOwner(str, Enum):
    """Who owns each responsibility."""
    ENGINE = "Validation Engine"
    CONSUMER = "Consumer"
    CONTRACT = "Evidence Contract"
    REGISTRY = "Validation Rule Registry"

@dataclass
class Responsibility:
    """A specific engineering responsibility."""
    id: str
    name: str
    owner: ResponsibilityOwner
    description: str
    rationale: str
    examples: List[str]
    forbidden_in: List[ResponsibilityOwner]

# ============================================
# ENGINE RESPONSIBILITIES (Inside Engine)
# ============================================

ENGINE_RESPONSIBILITIES = [
    Responsibility(
        id="E-001",
        name="Load Evidence",
        owner=ResponsibilityOwner.ENGINE,
        description="Accept BOQIntelligenceResult from Evidence Contract as input.",
        rationale="Engine consumes evidence, does not produce it.",
        examples=[
            "analyze_boq() returns BOQIntelligenceResult → Engine accepts it",
            "Engine reads evidence fields: row_classification, hierarchy, detected_level_skips",
        ],
        forbidden_in=[ResponsibilityOwner.CONSUMER],
    ),
    Responsibility(
        id="E-002",
        name="Load Rules",
        owner=ResponsibilityOwner.ENGINE,
        description="Load validation rules from Validation Rule Registry.",
        rationale="Engine evaluates rules against evidence.",
        examples=[
            "Engine loads V-001 (Required Field Presence) from registry",
            "Engine loads V-004 (Total Rows Consistency) from registry",
        ],
        forbidden_in=[ResponsibilityOwner.CONSUMER],
    ),
    Responsibility(
        id="E-003",
        name="Evaluate Rules",
        owner=ResponsibilityOwner.ENGINE,
        description="Execute validation rule logic against evidence.",
        rationale="Engine performs deterministic rule evaluation.",
        examples=[
            "V-003: Check if row_classification values are non-negative",
            "V-007: Calculate code_rows / total_rows ratio",
            "V-014: Count detected_level_skips (or None if unavailable)",
        ],
        forbidden_in=[ResponsibilityOwner.CONSUMER, ResponsibilityOwner.CONTRACT],
    ),
    Responsibility(
        id="E-004",
        name="Produce Findings",
        owner=ResponsibilityOwner.ENGINE,
        description="Generate deterministic validation findings from rule evaluation.",
        rationale="Engine outputs findings, not recommendations.",
        examples=[
            "V-002 finding: [] (all expected keys present)",
            "V-004 finding: 0 (sum matches total_rows)",
            "V-007 finding: 0.67 (code column 67% complete)",
        ],
        forbidden_in=[ResponsibilityOwner.CONSUMER, ResponsibilityOwner.CONTRACT],
    ),
    Responsibility(
        id="E-005",
        name="Handle Optional Evidence",
        owner=ResponsibilityOwner.ENGINE,
        description="Gracefully handle None values for optional evidence fields.",
        rationale="Hierarchy and detection evidence are optional (include_hierarchy, include_detection parameters).",
        examples=[
            "If hierarchy is None, V-010 reports: hierarchy_available = False",
            "If detected_level_skips is None, V-014 reports: None",
        ],
        forbidden_in=[ResponsibilityOwner.CONSUMER],
    ),
    Responsibility(
        id="E-006",
        name="Enforce Rule Lifecycle",
        owner=ResponsibilityOwner.ENGINE,
        description="Only evaluate rules with status = VERIFIED or APPROVED.",
        rationale="Deprecated/Retired rules should not execute.",
        examples=[
            "Skip rules with status = DEPRECATED",
            "Skip rules with status = RETIRED",
        ],
        forbidden_in=[ResponsibilityOwner.CONSUMER],
    ),
    Responsibility(
        id="E-007",
        name="Maintain Determinism",
        owner=ResponsibilityOwner.ENGINE,
        description="Ensure same evidence + same rules = same findings.",
        rationale="Validation must be repeatable and reproducible.",
        examples=[
            "Run engine twice on same evidence → identical findings",
            "No random behavior, no timestamps in findings, no external state",
        ],
        forbidden_in=[ResponsibilityOwner.CONSUMER],
    ),
    Responsibility(
        id="E-008",
        name="Preserve EQ-0011 Boundary",
        owner=ResponsibilityOwner.ENGINE,
        description="Never produce assessments, recommendations, or professional judgments.",
        rationale="Engine observes and detects. Consumers interpret and decide.",
        examples=[
            "Engine reports: '3 level skips detected' (NOT: 'level skips should be fixed')",
            "Engine reports: '0.67 code completeness' (NOT: 'completeness is poor')",
        ],
        forbidden_in=[ResponsibilityOwner.CONSUMER],
    ),
    Responsibility(
        id="E-009",
        name="Report Rule Provenance",
        owner=ResponsibilityOwner.ENGINE,
        description="Include rule_id, rule_version, category in finding metadata.",
        rationale="Consumers need to know which rule produced which finding.",
        examples=[
            "Finding metadata: {rule_id: 'V-007', rule_version: '1.0.0', category: 'Completeness'}",
        ],
        forbidden_in=[ResponsibilityOwner.CONSUMER],
    ),
]

# ============================================
# CONSUMER RESPONSIBILITIES (Outside Engine)
# ============================================

CONSUMER_RESPONSIBILITIES = [
    Responsibility(
        id="C-001",
        name="Interpret Findings",
        owner=ResponsibilityOwner.CONSUMER,
        description="Apply application-specific meaning to validation findings.",
        rationale="Engine produces findings. Consumers decide what findings mean.",
        examples=[
            "CheckMate: 0.67 code completeness → display yellow warning",
            "Formatter: 0.67 code completeness → no formatting change needed",
            "Reporting: 0.67 code completeness → include in summary table",
        ],
        forbidden_in=[ResponsibilityOwner.ENGINE],
    ),
    Responsibility(
        id="C-002",
        name="Display Findings",
        owner=ResponsibilityOwner.CONSUMER,
        description="Present validation findings to users in application-specific UI.",
        rationale="Engine has no UI. Consumers own presentation.",
        examples=[
            "CheckMate: Display findings in validation report table",
            "Reporting: Include findings in PDF export",
        ],
        forbidden_in=[ResponsibilityOwner.ENGINE],
    ),
    Responsibility(
        id="C-003",
        name="Filter Rules",
        owner=ResponsibilityOwner.CONSUMER,
        description="Select which rules to run based on application needs.",
        rationale="Consumers decide which validations are relevant.",
        examples=[
            "CheckMate: Run all 18 implementable rules",
            "Formatter: Run only completeness rules (V-007, V-008, V-009)",
            "Reporting: Run only detection rules (V-013 through V-018)",
        ],
        forbidden_in=[ResponsibilityOwner.ENGINE],
    ),
    Responsibility(
        id="C-004",
        name="Configure Thresholds",
        owner=ResponsibilityOwner.CONSUMER,
        description="Define application-specific thresholds for findings.",
        rationale="Engine reports ratios. Consumers decide what ratios are acceptable.",
        examples=[
            "CheckMate: code_completeness < 0.5 → error, < 0.8 → warning, >= 0.8 → pass",
            "Formatter: No thresholds needed (only uses finding values)",
        ],
        forbidden_in=[ResponsibilityOwner.ENGINE],
    ),
    Responsibility(
        id="C-005",
        name="Make Decisions",
        owner=ResponsibilityOwner.CONSUMER,
        description="Decide what actions to take based on findings.",
        rationale="Engine provides findings. Consumers make decisions.",
        examples=[
            "CheckMate: Block export if critical findings detected",
            "CheckMate: Show recommendations to user based on findings",
            "Reporting: Include findings in automated report",
        ],
        forbidden_in=[ResponsibilityOwner.ENGINE],
    ),
    Responsibility(
        id="C-006",
        name="Manage User Workflow",
        owner=ResponsibilityOwner.CONSUMER,
        description="Control application workflow around validation.",
        rationale="Engine has no workflow. Consumers own UX.",
        examples=[
            "CheckMate: Run validation → Show results → Allow user to accept/reject",
            "Formatter: Run validation → Auto-format based on findings",
        ],
        forbidden_in=[ResponsibilityOwner.ENGINE],
    ),
    Responsibility(
        id="C-007",
        name="Store Validation History",
        owner=ResponsibilityOwner.CONSUMER,
        description="Persist validation findings for audit/history (if needed).",
        rationale="Engine is stateless. Consumers own persistence.",
        examples=[
            "CheckMate: Save validation results to database",
            "Reporting: Include validation timestamp in report metadata",
        ],
        forbidden_in=[ResponsibilityOwner.ENGINE],
    ),
    Responsibility(
        id="C-008",
        name="Verify Contract Compliance",
        owner=ResponsibilityOwner.CONSUMER,
        description="Ensure consumer correctly uses Evidence Contract and Validation Engine APIs.",
        rationale="Consumers must prove compliance.",
        examples=[
            "Run Consumer Compliance Suite (EQ-0013)",
            "Verify Rule IDs exist in Engine",
            "Verify Finding Types match expectations",
        ],
        forbidden_in=[ResponsibilityOwner.ENGINE],
    ),
]

# ============================================
# CONTRACT RESPONSIBILITIES (Evidence Production)
# ============================================

CONTRACT_RESPONSIBILITIES = [
    Responsibility(
        id="K-001",
        name="Produce evidence from BOQRow[] input",
        owner=ResponsibilityOwner.CONTRACT,
        description="Generate deterministic structural evidence from BOQRow[].",
        rationale="Evidence Contract owns evidence production. Engine consumes evidence.",
        examples=[
            "analyze_boq(rows) → BOQIntelligenceResult",
            "Evidence includes: row_classification, hierarchy, detected_level_skips, etc.",
        ],
        forbidden_in=[ResponsibilityOwner.ENGINE, ResponsibilityOwner.CONSUMER],
    ),
    Responsibility(
        id="K-002",
        name="Return BOQIntelligenceResult",
        owner=ResponsibilityOwner.CONTRACT,
        description="Return structured BOQIntelligenceResult as the public evidence surface.",
        rationale="Contract serves as sole integration surface for all consumers.",
        examples=[
            "BOQIntelligenceResult has: row_classification, boq_statistics, hierarchy, detection_summary",
        ],
        forbidden_in=[ResponsibilityOwner.ENGINE, ResponsibilityOwner.CONSUMER],
    ),
    Responsibility(
        id="K-003",
        name="Maintain structural invariants",
        owner=ResponsibilityOwner.CONTRACT,
        description="Enforce structural invariants documented in Contract.",
        rationale="Contract guarantees structural invariants. Engine relies on guarantees.",
        examples=[
            "SI-RC-04: row_classification always has 5 keys",
        ],
        forbidden_in=[ResponsibilityOwner.ENGINE, ResponsibilityOwner.CONSUMER],
    ),
    Responsibility(
        id="K-004",
        name="Maintain semantic invariants",
        owner=ResponsibilityOwner.CONTRACT,
        description="Enforce semantic invariants documented in Contract.",
        rationale="Contract guarantees semantic invariants. Engine relies on guarantees.",
        examples=[
            "SE-RC-01: Same worksheet produces same classifications",
        ],
        forbidden_in=[ResponsibilityOwner.ENGINE, ResponsibilityOwner.CONSUMER],
    ),
    Responsibility(
        id="K-005",
        name="Enforce column detection rules",
        owner=ResponsibilityOwner.CONTRACT,
        description="Apply column detection rules to identify BOQ columns.",
        rationale="Contract owns detection logic. Engine consumes detection results.",
        examples=[
            "Detect item_code, description, quantity, unit columns from worksheet headers",
        ],
        forbidden_in=[ResponsibilityOwner.ENGINE, ResponsibilityOwner.CONSUMER],
    ),
    Responsibility(
        id="K-006",
        name="Manage include_hierarchy option",
        owner=ResponsibilityOwner.CONTRACT,
        description="Control whether hierarchy analysis is performed.",
        rationale="Contract owns output scope. Engine receives optional hierarchy evidence.",
        examples=[
            "include_hierarchy=True → hierarchy field populated",
            "include_hierarchy=False → hierarchy is None",
        ],
        forbidden_in=[ResponsibilityOwner.ENGINE, ResponsibilityOwner.CONSUMER],
    ),
    Responsibility(
        id="K-007",
        name="Manage include_detection option",
        owner=ResponsibilityOwner.CONTRACT,
        description="Control whether detection analysis is performed.",
        rationale="Contract owns output scope. Engine receives optional detection evidence.",
        examples=[
            "include_detection=True → detected_level_skips populated",
            "include_detection=False → detected_level_skips is None",
        ],
        forbidden_in=[ResponsibilityOwner.ENGINE, ResponsibilityOwner.CONSUMER],
    ),
]

# ============================================
# REGISTRY RESPONSIBILITIES (Rule Governance)
# ============================================

REGISTRY_RESPONSIBILITIES = [
    Responsibility(
        id="R-001",
        name="Govern Rules",
        owner=ResponsibilityOwner.REGISTRY,
        description="Manage rule lifecycle (Candidate → Approved → Implemented → Verified → Deprecated → Retired).",
        rationale="Registry owns rule governance. Engine executes rules.",
        examples=[
            "Add new rule via Engineering Question + Spike",
            "Deprecate rule when evidence field removed",
            "Retire rule after deprecation period",
        ],
        forbidden_in=[ResponsibilityOwner.ENGINE, ResponsibilityOwner.CONSUMER],
    ),
    Responsibility(
        id="R-002",
        name="Maintain Provenance",
        owner=ResponsibilityOwner.REGISTRY,
        description="Document complete provenance for every rule (13 required fields).",
        rationale="Registry ensures traceability. Engine relies on provenance.",
        examples=[
            "Rule ID, category, evidence_fields, boundary_class, eq_source, etc.",
        ],
        forbidden_in=[ResponsibilityOwner.ENGINE, ResponsibilityOwner.CONSUMER],
    ),
    Responsibility(
        id="R-003",
        name="Enforce Taxonomy",
        owner=ResponsibilityOwner.REGISTRY,
        description="Ensure rules conform to validated categories (Structural, Consistency, Completeness, Detection).",
        rationale="Registry enforces taxonomy. Engine executes categorized rules.",
        examples=[
            "Reject rules with category = Assessment (crosses EQ-0011)",
            "Reject rules with category = Financial (insufficient evidence)",
        ],
        forbidden_in=[ResponsibilityOwner.ENGINE, ResponsibilityOwner.CONSUMER],
    ),
]

# ============================================
# FORBIDDEN RESPONSIBILITIES (No Owner)
# ============================================

FORBIDDEN_RESPONSIBILITIES = [
    {
        "id": "F-001",
        "name": "Assess BOQ Quality",
        "forbidden": "All components",
        "rationale": "Crosses EQ-0011 boundary (Assess/Judge).",
        "examples": ["Judge whether BOQ is 'good' or 'bad'", "Rate BOQ on quality scale"],
    },
    {
        "id": "F-002",
        "name": "Recommend Actions",
        "forbidden": "All components",
        "rationale": "Crosses EQ-0011 boundary (Recommend).",
        "examples": ["Suggest fixes for level skips", "Advise user to change quantities"],
    },
    {
        "id": "F-003",
        "name": "Perform Professional Judgment",
        "forbidden": "All components",
        "rationale": "Engineering provides findings. Humans make professional decisions.",
        "examples": ["Determine project feasibility", "Assess cost reasonableness"],
    },
    {
        "id": "F-004",
        "name": "Modify Evidence",
        "forbidden": "Engine, Consumer",
        "rationale": "Evidence is immutable. Only Contract produces evidence.",
        "examples": ["Change row_classification counts", "Edit hierarchy structure"],
    },
    {
        "id": "F-005",
        "name": "Modify Rules",
        "forbidden": "Engine, Consumer",
        "rationale": "Rules are governed by Registry. Engine and consumers are read-only.",
        "examples": ["Change rule logic at runtime", "Add rules without governance"],
    },
]

# ============================================
# ENGINE PUBLIC API
# ============================================

ENGINE_API = {
    "input": {
        "evidence": "BOQIntelligenceResult (from Evidence Contract)",
        "rules": "List[RuleID] (from Validation Rule Registry) or 'all'",
        "options": {
            "include_metadata": "bool (default: True) — Include rule provenance in findings",
            "skip_deprecated": "bool (default: True) — Skip rules with status=DEPRECATED",
        },
    },
    "output": {
        "findings": "ValidationFindings (frozen dataclass)",
        "structure": {
            "rule_id": "str — Rule that produced finding",
            "rule_version": "str — Rule version",
            "category": "str — Rule category",
            "finding_type": "str — Type of finding (presence, count, ratio, etc.)",
            "finding_value": "Any — Deterministic finding value",
            "evidence_fields": "List[str] — Evidence fields consumed",
        },
    },
    "example": {
        "input": "validate(evidence=result, rules=['V-007', 'V-014'], options={'include_metadata': True})",
        "output": [
            {
                "rule_id": "V-007",
                "rule_version": "1.0.0",
                "category": "Completeness",
                "finding_type": "ratio",
                "finding_value": 0.67,
                "evidence_fields": ["boq_statistics"],
            },
            {
                "rule_id": "V-014",
                "rule_version": "1.0.0",
                "category": "Detection",
                "finding_type": "count",
                "finding_value": 3,
                "evidence_fields": ["detected_level_skips"],
            },
        ],
    },
}

# ============================================
# ENGINE STATE POLICY
# ============================================

ENGINE_STATE_POLICY = {
    "stateless": "Engine maintains no state between invocations.",
    "deterministic": "Same evidence + same rules = same findings (always).",
    "immutable": "Engine does not modify evidence or rules.",
    "isolated": "Engine does not interact with external systems (no network, no database, no filesystem).",
    "pure_function": "Engine is a pure function: Findings = f(Evidence, Rules).",
}

# ============================================
# ARCHITECTURE CONSISTENCY CHECKS
# ============================================

ARCHITECTURE_CONSISTENCY = {
    "no_duplicate_responsibilities": {
        "check": "Each responsibility has exactly one owner.",
        "violations": [],
    },
    "no_layer_overlap": {
        "check": "Contract produces evidence. Engine evaluates rules. Consumers interpret findings.",
        "violations": [],
    },
    "no_responsibility_migration": {
        "check": "Engine responsibilities remain in Engine. Consumer responsibilities remain in Consumer.",
        "violations": [],
    },
    "no_ontology_drift": {
        "check": "Evidence Contract ontology unchanged. BOQ Intelligence unchanged.",
        "violations": [],
    },
    "no_hidden_coupling": {
        "check": "Engine depends only on Contract (not BOQ Intelligence internals).",
        "violations": [],
    },
    "no_yagni_violations": {
        "check": "Engine implements only what 18 rules require. No speculative features.",
        "violations": [],
    },
    "engine_is_consumer": {
        "check": "Validation Engine is a consumer of Evidence Contract.",
        "violations": [],
    },
}

def generate_scope_document() -> dict:
    """Generate Validation Engine scope document."""
    return {
        "scope_version": "1.0.0",
        "contract_version": "1.0.0",
        "registry_version": "1.0.0",
        "generated_by": "EQ-0013 Spike 3",
        "engine_responsibilities": [
            {
                "id": r.id,
                "name": r.name,
                "owner": r.owner.value,
                "description": r.description,
                "rationale": r.rationale,
                "examples": r.examples,
                "forbidden_in": [o.value for o in r.forbidden_in],
            }
            for r in ENGINE_RESPONSIBILITIES
        ],
        "consumer_responsibilities": [
            {
                "id": r.id,
                "name": r.name,
                "owner": r.owner.value,
                "description": r.description,
                "rationale": r.rationale,
                "examples": r.examples,
                "forbidden_in": [o.value for o in r.forbidden_in],
            }
            for r in CONSUMER_RESPONSIBILITIES
        ],
        "contract_responsibilities": [
            {
                "id": r.id,
                "name": r.name,
                "owner": r.owner.value,
                "description": r.description,
                "rationale": r.rationale,
                "examples": r.examples,
                "forbidden_in": [o.value for o in r.forbidden_in],
            }
            for r in CONTRACT_RESPONSIBILITIES
        ],
        "registry_responsibilities": [
            {
                "id": r.id,
                "name": r.name,
                "owner": r.owner.value,
                "description": r.description,
                "rationale": r.rationale,
                "examples": r.examples,
                "forbidden_in": [o.value for o in r.forbidden_in],
            }
            for r in REGISTRY_RESPONSIBILITIES
        ],
        "forbidden_responsibilities": FORBIDDEN_RESPONSIBILITIES,
        "engine_public_api": ENGINE_API,
        "engine_state_policy": ENGINE_STATE_POLICY,
        "architecture_consistency": ARCHITECTURE_CONSISTENCY,
    }

def main():
    """Generate Spike 3 outputs."""

    print("=" * 60)
    print("EQ-0013 Spike 3: Validation Engine Scope & Responsibilities")
    print("=" * 60)
    print()

    # Generate scope document
    scope = generate_scope_document()

    # Save scope
    scope_path = "data/reports/eq0013_spike3_engine_scope.json"
    with open(scope_path, "w") as f:
        json.dump(scope, f, indent=2)
    print(f"✓ Saved Engine Scope: {scope_path}")

    # Statistics
    print()
    print("Responsibility Distribution:")
    print(f"  Engine: {len(ENGINE_RESPONSIBILITIES)} responsibilities")
    print(f"  Consumer: {len(CONSUMER_RESPONSIBILITIES)} responsibilities")
    print(f"  Contract: {len(CONTRACT_RESPONSIBILITIES)} responsibilities")
    print(f"  Registry: {len(REGISTRY_RESPONSIBILITIES)} responsibilities")
    print(f"  Forbidden: {len(FORBIDDEN_RESPONSIBILITIES)} prohibited activities")
    print()

    print("Engine Responsibilities:")
    for r in ENGINE_RESPONSIBILITIES:
        print(f"  {r.id}: {r.name}")
    print()

    print("Consumer Responsibilities:")
    for r in CONSUMER_RESPONSIBILITIES:
        print(f"  {r.id}: {r.name}")
    print()

    print("Forbidden Responsibilities:")
    for f in FORBIDDEN_RESPONSIBILITIES:
        print(f"  {f['id']}: {f['name']} — {f['rationale']}")
    print()

    print("Engine State Policy:")
    for k, v in ENGINE_STATE_POLICY.items():
        print(f"  {k}: {v}")
    print()

    print("=" * 60)
    print("Spike 3 Scope Definition Complete")
    print("=" * 60)
    print()
    print("Next: Run eq0013_spike3_architecture_consistency_audit.py")

if __name__ == "__main__":
    main()