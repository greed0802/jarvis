#!/usr/bin/env python3
"""EQ-0012 Spike 2: Contract Structure & Versioning Policy

Define the Public Evidence Contract versioning scheme, compatibility rules,
consumer guarantees, and deprecation lifecycle.

Organized around four questions:
1. Version Identity — How is the contract version identified?
2. Compatibility Rules — What constitutes Major/Minor/Patch changes?
3. Consumer Guarantees — What can every consumer permanently rely on?
4. Deprecation Lifecycle — How is an obsolete field retired?

Authority:
- EQ-0012 BOQ Intelligence Public Evidence Contract
- Engineering_Governance.md v1.0
"""

from dataclasses import dataclass, field
from enum import Enum


class ContractVersionScheme(Enum):
    """Possible versioning schemes for the Public Evidence Contract."""
    SEMANTIC = "semantic"  # major.minor.patch (1.0.0, 2.1.0)
    CALENDAR = "calendar"  # year.release (2026.1)
    SEQUENTIAL = "sequential"  # v1, v2, v3


@dataclass(frozen=True)
class ContractFieldRecord:
    """Record of a field in the Evidence Contract."""
    name: str
    increment: int
    is_required: bool
    is_public_api: bool = True  # All contract fields are public API


@dataclass(frozen=True)
class CompatibilityRule:
    """Defines what constitutes a compatibility level change."""
    level: str  # major, minor, patch
    description: str
    examples: list[str]


@dataclass(frozen=True)
class VersioningPolicy:
    """Complete versioning policy specification."""
    scheme: ContractVersionScheme
    initial_version: str
    rules: list[CompatibilityRule]
    guarantees: list[str]
    deprecation_phases: list[str]


# ============================================================
# Question 1: Version Identity
# ============================================================

def evaluate_version_identity() -> dict:
    """Evaluate version identity options."""
    
    schemes = {
        "semantic": {
            "format": "MAJOR.MINOR.PATCH (e.g., 1.0.0, 2.3.1)",
            "strengths": [
                "Industry standard for API contracts",
                "Clear upgrade path for consumers",
                "Published-by-convention meaning of each segment",
                "Tooling and ecosystem support",
            ],
            "weaknesses": [
                "Requires disciplined enforcement",
                "Semantic versioning scope creep risk",
            ],
        },
        "calendar": {
            "format": "YEAR.RELEASE (e.g., 2026.1)",
            "strengths": [
                "Time-based predictability",
                "No ambiguity about release cadence",
            ],
            "weaknesses": [
                "Does not communicate compatibility",
                "Consumers cannot infer breaking changes",
            ],
        },
        "sequential": {
            "format": "v1, v2, v3",
            "strengths": [
                "Simple",
                "Clear major version boundaries",
            ],
            "weaknesses": [
                "No minor/patch granularity",
                "Every change is a major version (discourages small improvements)",
            ],
        },
    }
    
    print("=" * 80)
    print("QUESTION 1: VERSION IDENTITY")
    print("=" * 80)
    print()
    
    for scheme, details in schemes.items():
        print(f"Scheme: {scheme.upper()}")
        print(f"  Format: {details['format']}")
        print("  Strengths:")
        for s in details['strengths']:
            print(f"    + {s}")
        print("  Weaknesses:")
        for w in details['weaknesses']:
            print(f"    - {w}")
        print()
    
    # Recommendation
    print("RECOMMENDATION:")
    print("  Scheme: Semantic Versioning (MAJOR.MINOR.PATCH)")
    print("  Initial version: 1.0.0")
    print("  Reasoning:")
    print("    1. The Evidence Contract is a formal API — semantic versioning is the")
    print("       established standard for API contracts.")
    print("    2. Consumers need to know whether an upgrade is safe (patch/minor)")
    print("       or requires attention (major).")
    print("    3. Industry tooling (packaging, dependency resolution) expects")
    print("       semantic versions.")
    print("    4. The contract will evolve — having three segments provides")
    print("       appropriate granularity for breaking vs. non-breaking changes.")
    print()
    
    return {
        "recommended_scheme": "semantic",
        "initial_version": "1.0.0",
        "schemes_evaluated": list(schemes.keys()),
    }


# ============================================================
# Question 2: Compatibility Rules
# ============================================================

def evaluate_compatibility_rules() -> list[CompatibilityRule]:
    """Evaluate compatibility rules based on evidence field inventory."""
    
    # Based on Spike 1 inventory of 10 evidence fields
    required_fields = ["row_classification", "section_statistics", 
                       "boq_statistics", "known_anomalies"]
    optional_fields = ["hierarchy", "hierarchy_statistics",
                      "detected_level_skips", "zero_quantity_items",
                      "structural_containment_findings", "completeness_findings"]
    
    rules = [
        CompatibilityRule(
            level="MAJOR",
            description="Breaking changes that require consumer attention and migration",
            examples=[
                "Removing a required field",
                "Changing the type of a required field",
                "Renaming a required field",
                "Changing invariants that consumers depend on",
                "Removing an optional field without deprecation period",
                "Breaking existing dictionary key structure (removing keys)",
                "Changing tuple element order or semantics",
            ]
        ),
        CompatibilityRule(
            level="MINOR",
            description="Non-breaking additions that preserve full backward compatibility",
            examples=[
                "Adding a new required field (with default/null for existing consumers)",
                "Adding a new optional field",
                "Adding new keys to existing dictionaries",
                "Adding new fields to the BOQHeaderNode dataclass (with defaults)",
                "Extending tuple contents at the end",
            ]
        ),
        CompatibilityRule(
            level="PATCH",
            description="Internal corrections that do not change the contract surface",
            examples=[
                "Fixing documentation errors",
                "Clarifying semantics of existing fields",
                "Adding new invariant documentation",
                "Correcting type annotation to match actual behavior",
                "Changes that do not affect consumers in any way",
            ]
        ),
    ]
    
    print("=" * 80)
    print("QUESTION 2: COMPATIBILITY RULES")
    print("=" * 80)
    print()
    
    for rule in rules:
        print(f"Level: {rule.level}")
        print(f"  Description: {rule.description}")
        print("  Examples:")
        for ex in rule.examples:
            print(f"    - {ex}")
        print()
    
    print("OBSERVATION:")
    print("  Required vs. Optional distinction is critical:")
    print("    - Changes to REQUIRED fields are ALWAYS breaking (MAJOR)")
    print("    - Changes to OPTIONAL fields may be MINOR if additive")
    print("    - Removing optional fields without deprecation is MAJOR")
    print("  Evidence structures use dicts and tuples:")
    print("    - Adding dict keys is MINOR (consumers should iterate dynamically)")
    print("    - Removing dict keys is MAJOR (breaks consumers expecting keys)")
    print("    - Extending tuples is MINOR at end, MAJOR if reordered")
    print()
    
    return rules


# ============================================================
# Question 3: Consumer Guarantees
# ============================================================

def evaluate_consumer_guarantees() -> list[str]:
    """Evaluate what consumers can permanently rely on."""
    
    guarantees = [
        # Field existence
        "All fields documented in the Evidence Contract will exist for the promised contract version",
        "Required fields will never be None (consumers can use without null checks)",
        "Optional fields will never be removed without formal deprecation",
        
        # Field types
        "Field types as documented will not change within a MAJOR version",
        "Union types (e.g., int | None) will not remove valid variants",
        "Dict key presence: documented keys will remain present",
        "Dict key absence: undocumented keys may appear (non-breaking addition)",
        
        # Field semantics
        "Field semantics as documented will not change within a MAJOR version",
        "Evidence classification (Observation/Hierarchy/Detection) will not change",
        "Engineering boundary (EQ-0011) will be preserved in all evidence",
        
        # Determinism
        "All evidence is deterministic — same input produces same output",
        "All evidence is immutable — consumers cannot modify evidence",
        "All evidence is traceable to frozen engineering evidence",
        
        # Access
        "Consumers may depend on the Evidence Contract directly",
        "Consumers may import evidence types without importing internal implementation",
        "Consumers will not need access to internal BOQ Intelligence functions",
    ]
    
    print("=" * 80)
    print("QUESTION 3: CONSUMER GUARANTEES")
    print("=" * 80)
    print()
    
    print("PERMANENT GUARANTEES (all versions):")
    print()
    for i, g in enumerate(guarantees, 1):
        print(f"  G-{i:02d}: {g}")
    
    print()
    print("GUARANTEE CLASSIFICATION:")
    print("  Structural Guarantees (G-01 to G-03): Field presence and nullability")
    print("  Type Guarantees (G-04 to G-07): Type stability and dict behavior")
    print("  Semantic Guarantees (G-08 to G-10): Meaning and boundary preservation")
    print("  Determinism Guarantees (G-11 to G-13): Immutability and reproducibility")
    print("  Access Guarantees (G-14 to G-16): Consumer dependency model")
    print()
    
    return guarantees


# ============================================================
# Question 4: Deprecation Lifecycle
# ============================================================

def evaluate_deprecation_lifecycle() -> list[str]:
    """Evaluate deprecation lifecycle for obsolete fields."""
    
    phases = [
        # Phase 1: Deprecation Announcement
        """
        PHASE 1: DEPRECATION ANNOUNCEMENT
        Trigger: Engineering Question determines a field is obsolete or harmful
        Action: Field marked as deprecated in evidence contract documentation
        Indicator: @deprecated annotation in field description
        Version: MINOR version bump (not breaking yet)
        Duration: At least one full MAJOR version cycle
        Consumer impact: Field still present and functional
        """,
        
        # Phase 2: Removal Notice
        """
        PHASE 2: REMOVAL NOTICE
        Trigger: Next MAJOR version planning
        Action: Explicit notification that field WILL be removed in next MAJOR
        Indicator: WARNING in deprecation notice with target removal version
        Version: Still present in current MAJOR version
        Duration: Throughout current MAJOR version
        Consumer impact: Field still present but consumers should migrate
        """,
        
        # Phase 3: Removal
        """
        PHASE 3: REMOVAL
        Trigger: MAJOR version bump
        Action: Field removed from Evidence Contract
        Version: MAJOR version bump
        Consumer impact: Breaking change — consumers must migrate
        """,
        
        # Governance Gate
        """
        GOVERNANCE GATE:
        Before any deprecation can begin:
        1. Engineering Question must classify the field as obsolete
        2. Project Owner must approve deprecation
        3. All consumers must be notified
        4. Migration path must be documented
        5. Minimum deprecation period enforced (one full MAJOR version)
        """,
    ]
    
    print("=" * 80)
    print("QUESTION 4: DEPRECATION LIFECYCLE")
    print("=" * 80)
    print()
    
    print("THREE-PHASE DEPRECATION MODEL:")
    print()
    for phase in phases:
        print(phase)
        print("---")
    
    print("MINIMUM DEPRECATION PERIOD:")
    print("  One full MAJOR version cycle")
    print("  Example: Field deprecated in v1.x.x → removed in v2.0.0")
    print("  This ensures consumers have adequate time to migrate")
    print()
    
    print("GOVERNANCE REQUIREMENTS:")
    print("  1. Engineering Question required (cannot deprecate without evidence)")
    print("  2. Project Owner approval required (deprecation is architectural decision)")
    print("  3. Consumer notification required (email, release notes, deprecation doc)")
    print("  4. Migration path required (how to replace deprecated field)")
    print("  5. Minimum deprecation period: one full MAJOR version")
    print()
    
    return phases


# ============================================================
# Policy Specification
# ============================================================

def build_versioning_policy_spec() -> str:
    """Build the formal versioning policy specification."""
    
    spec = """
================================================================================
BOQ INTELLIGENCE PUBLIC EVIDENCE CONTRACT — VERSIONING POLICY v1.0
================================================================================

1. VERSION IDENTITY
   Scheme: Semantic Versioning (MAJOR.MINOR.PATCH)
   Format: X.Y.Z (e.g., 1.0.0)
   Initial version: 1.0.0
   Location: docs/contracts/BOQ_Intelligence_Evidence_Contract.md

2. COMPATIBILITY RULES

   MAJOR (X.0.0):
   - Removing a required field
   - Changing the type of a required field  
   - Renaming a required field
   - Changing invariants consumers depend on
   - Removing an optional field without full deprecation lifecycle
   - Removing documented dictionary keys
   - Changing tuple element order or semantics

   MINOR (0.Y.0):
   - Adding a new required field (with default/null for backward compat)
   - Adding a new optional field
   - Adding new keys to existing dictionaries
   - Adding new fields to dataclass structures (with defaults)
   - Extending tuple contents at the end
   - Marking a field as deprecated (field still present and functional)

   PATCH (0.0.Z):
   - Fixing documentation errors
   - Clarifying field semantics
   - Adding invariant documentation
   - Correcting type annotations to match actual behavior
   - Changes that do not affect consumers

3. CONSUMER GUARANTEES
   G-01: All documented fields will exist for the promised contract version
   G-02: Required fields will never be None
   G-03: Optional fields will not be removed without formal deprecation
   G-04: Documented field types will not change within a MAJOR version
   G-05: Union types will not remove valid variants
   G-06: Documented dictionary keys will remain present
   G-07: Undocumented keys may appear (non-breaking addition)
   G-08: Documented field semantics will not change within a MAJOR version
   G-09: Evidence classification remains stable across versions
   G-10: EQ-0011 engineering boundary preserved in all evidence
   G-11: All evidence is deterministic
   G-12: All evidence is immutable
   G-13: All evidence traceable to frozen engineering evidence
   G-14: Consumers may depend on the Evidence Contract directly
   G-15: Consumers may import without internal implementation details
   G-16: Consumers do not need access to internal BOQ Intelligence functions

4. DEPRECATION LIFECYCLE
   Phase 1: Deprecation Announcement (MINOR version)
     - Field marked @deprecated in contract documentation
     - Field still present and functional
     - Duration: one full MAJOR version cycle minimum

   Phase 2: Removal Notice (during current MAJOR version)
     - Explicit notification of target removal version
     - Consumers should migrate

   Phase 3: Removal (MAJOR version)
     - Field removed from contract
     - Breaking change

   Governance Gate:
   - Engineering Question required
   - Project Owner approval required
   - Consumer notification required
   - Migration path documentation required
   - Minimum deprecation period: one full MAJOR version
"""
    
    return spec


def main():
    """Execute Spike 2: Contract Structure & Versioning Policy."""
    
    print("=" * 80)
    print("EQ-0012 SPIKE 2: CONTRACT STRUCTURE & VERSIONING POLICY")
    print("=" * 80)
    print()
    print("This analysis defines the governance of the Public Evidence Contract")
    print("based on the frozen evidence inventory from Spike 1.")
    print()
    
    # Question 1
    version_identity = evaluate_version_identity()
    
    # Question 2
    compatibility_rules = evaluate_compatibility_rules()
    
    # Question 3
    consumer_guarantees = evaluate_consumer_guarantees()
    
    # Question 4
    deprecation_lifecycle = evaluate_deprecation_lifecycle()
    
    # Build policy specification
    spec = build_versioning_policy_spec()
    
    print("=" * 80)
    print("VERSIONING POLICY SPECIFICATION")
    print("=" * 80)
    print(spec)
    
    print("=" * 80)
    print("SPIKE 2 COMPLETE")
    print("=" * 80)
    print()
    print("Next Steps:")
    print("  1. Review versioning policy specification")
    print("  2. Create Spike 2 Evidence Report")
    print("  3. Proceed to Spike 3: Contract Invariants")


if __name__ == "__main__":
    main()