"""Domain Rule Registry — deterministic rule catalog for BOQ Intelligence.

This module defines the complete set of currently supported rules,
classified by authority (Engineering vs Domain) and category.

Only rules with existing evidence are implemented.
No rules are invented. No speculative rules.

Authority:
  - CB-0002 — BOQ Intelligence Domain Rule Foundation
  - EQ-0010 — Deterministic BOQ Structural Intelligence
  - EQ-0011 — BOQ Semantic Intelligence Boundary
  - EQ-0012 — BOQ Intelligence Public Evidence Contract
  - EQ-0013 — Validation Engine
  - EQ-0015 — Structural Containment Investigation
  - docs/domain/02_BOQ_Structure.md — BOQ hierarchy rules
  - docs/reference/office_standards/ — Office standards
"""

from __future__ import annotations

from jarvis.domain.models import (
    DomainRule,
    RuleAuthority,
    RuleCategory,
    RuleSeverity,
    RuleStatus,
    RuleRegistry,
)


def _build_rules() -> tuple[DomainRule, ...]:
    """Build the complete set of currently supported rules.

    Returns a tuple sorted by rule_id for deterministic ordering.

    Only rules with existing evidence are included.
    No rules are invented. No speculative rules.
    """
    rules: list[DomainRule] = []

    # ============================================================
    # Engineering-Derived Rules (E-001 through E-018)
    # ============================================================
    # These rules are traced to answered Engineering Questions.
    # They are stable until new evidence contradicts them.

    # --- Evidence Integrity ---

    rules.append(DomainRule(
        rule_id="E-001",
        name="Required Evidence Fields Present",
        description="Verify all required evidence fields are present in BOQIntelligenceResult: "
                    "row_classification, section_statistics, boq_statistics, known_anomalies.",
        authority=RuleAuthority.ENGINEERING,
        category=RuleCategory.EVIDENCE_INTEGRITY,
        severity=RuleSeverity.ERROR,
        status=RuleStatus.VERIFIED,
        eq_reference="EQ-0012",
        evidence_reference="EQ-0012 Spike 3 — Contract Invariants",
        authority_reference="docs/contracts/BOQ_Intelligence_Public_Evidence_Contract_v1.0.md",
        inputs=("row_classification", "section_statistics", "boq_statistics", "known_anomalies"),
        consumers=("Validation Engine",),
        regression_test="tests/domain/test_registry.py",
        notes="Maps to Validation Engine rule V-001.",
        rule_version="1.0.0",
    ))

    # --- Classification ---

    rules.append(DomainRule(
        rule_id="E-002",
        name="Row Classification Keys Complete",
        description="Verify row_classification contains exactly 5 expected keys: "
                    "Head, Note, Section, Item, Other.",
        authority=RuleAuthority.ENGINEERING,
        category=RuleCategory.CLASSIFICATION,
        severity=RuleSeverity.ERROR,
        status=RuleStatus.VERIFIED,
        eq_reference="EQ-0001",
        evidence_reference="EQ-0012 Spike 3 — Contract Invariants (SI-RC-04)",
        authority_reference="docs/contracts/BOQ_Intelligence_Public_Evidence_Contract_v1.0.md",
        inputs=("row_classification",),
        consumers=("Validation Engine",),
        regression_test="tests/domain/test_registry.py",
        notes="Maps to Validation Engine rule V-002. UOM-based classification is deterministic per EQ-0001.",
        rule_version="1.0.0",
    ))

    rules.append(DomainRule(
        rule_id="E-003",
        name="Row Classification Non-Negative",
        description="Verify all row_classification values are >= 0.",
        authority=RuleAuthority.ENGINEERING,
        category=RuleCategory.CLASSIFICATION,
        severity=RuleSeverity.ERROR,
        status=RuleStatus.VERIFIED,
        eq_reference="EQ-0012",
        evidence_reference="EQ-0012 Spike 3 — Contract Invariants (SI-RC-05)",
        authority_reference="docs/contracts/BOQ_Intelligence_Public_Evidence_Contract_v1.0.md",
        inputs=("row_classification",),
        consumers=("Validation Engine",),
        regression_test="tests/domain/test_registry.py",
        notes="Maps to Validation Engine rule V-003.",
        rule_version="1.0.0",
    ))

    rules.append(DomainRule(
        rule_id="E-004",
        name="Row Classification Sum Consistency",
        description="Verify sum of row_classification values equals total_rows in boq_statistics.",
        authority=RuleAuthority.ENGINEERING,
        category=RuleCategory.CLASSIFICATION,
        severity=RuleSeverity.ERROR,
        status=RuleStatus.VERIFIED,
        eq_reference="EQ-0012",
        evidence_reference="EQ-0012 Spike 3 — Contract Invariants (SI-RC-06)",
        authority_reference="docs/contracts/BOQ_Intelligence_Public_Evidence_Contract_v1.0.md",
        inputs=("row_classification", "boq_statistics"),
        consumers=("Validation Engine",),
        regression_test="tests/domain/test_registry.py",
        notes="Maps to Validation Engine rule V-004.",
        rule_version="1.0.0",
    ))

    # --- Sign Convention ---

    rules.append(DomainRule(
        rule_id="E-005",
        name="OMISSION Section Sign Convention",
        description="Detect rows in OMISSION sections with positive quantities. "
                    "OMISSION items should have negative quantities per CostX convention.",
        authority=RuleAuthority.ENGINEERING,
        category=RuleCategory.SIGN_CONVENTION,
        severity=RuleSeverity.WARNING,
        status=RuleStatus.VERIFIED,
        eq_reference="EQ-0002",
        evidence_reference="EQ-0002 — Sign Convention Validation Mechanism (ANSWERED)",
        authority_reference="docs/contracts/BOQ_Intelligence_Public_Evidence_Contract_v1.0.md",
        inputs=("known_anomalies", "section_statistics"),
        consumers=("Validation Engine", "CheckMate"),
        regression_test="tests/domain/test_registry.py",
        notes="Maps to the 7 known OMISSION anomalies. EQ-0006 confirmed these are data-entry errors. "
              "Maps to Validation Engine anomaly detection rules.",
        rule_version="1.0.0",
    ))

    rules.append(DomainRule(
        rule_id="E-006",
        name="Section Quantity Counts Non-Negative",
        description="Verify all section quantity counts are non-negative.",
        authority=RuleAuthority.ENGINEERING,
        category=RuleCategory.SIGN_CONVENTION,
        severity=RuleSeverity.ERROR,
        status=RuleStatus.VERIFIED,
        eq_reference="EQ-0012",
        evidence_reference="EQ-0012 Spike 3 — Contract Invariants (SI-SS-02)",
        authority_reference="docs/contracts/BOQ_Intelligence_Public_Evidence_Contract_v1.0.md",
        inputs=("section_statistics",),
        consumers=("Validation Engine",),
        regression_test="tests/domain/test_registry.py",
        notes="Maps to Validation Engine rule V-005.",
        rule_version="1.0.0",
    ))

    # --- Structural ---

    rules.append(DomainRule(
        rule_id="E-007",
        name="Hierarchy Availability",
        description="Check if hierarchy reconstruction evidence is available (not None).",
        authority=RuleAuthority.ENGINEERING,
        category=RuleCategory.STRUCTURAL,
        severity=RuleSeverity.INFO,
        status=RuleStatus.VERIFIED,
        eq_reference="EQ-0010",
        evidence_reference="EQ-0010 Spike 4 — Hierarchy Reconstruction",
        authority_reference="docs/contracts/BOQ_Intelligence_Public_Evidence_Contract_v1.0.md",
        inputs=("hierarchy",),
        consumers=("Validation Engine", "CheckMate"),
        regression_test="tests/domain/test_registry.py",
        notes="Maps to Validation Engine rule V-010. Hierarchy is optional in analyze_boq().",
        rule_version="1.0.0",
    ))

    rules.append(DomainRule(
        rule_id="E-008",
        name="Level Skip Detection",
        description="Detect level skips in reconstructed hierarchy where a child header "
                    "skips one or more levels relative to its parent.",
        authority=RuleAuthority.ENGINEERING,
        category=RuleCategory.STRUCTURAL,
        severity=RuleSeverity.INFO,
        status=RuleStatus.VERIFIED,
        eq_reference="EQ-0010, EQ-0011",
        evidence_reference="EQ-0010 Spike 4, EQ-0011 Spike 2, EQ-0011 Spike 3",
        authority_reference="docs/contracts/BOQ_Intelligence_Public_Evidence_Contract_v1.0.md",
        inputs=("detected_level_skips",),
        consumers=("Validation Engine",),
        regression_test="tests/domain/test_registry.py",
        notes="Maps to Validation Engine rules V-013, V-014, V-015. "
              "Records observable facts — does not assess legitimacy.",
        rule_version="1.0.0",
    ))

    rules.append(DomainRule(
        rule_id="E-009",
        name="Structural Containment Verification",
        description="Verify structural hierarchy relationships: child level must be > parent level. "
                    "Records structural inversions if they occur.",
        authority=RuleAuthority.ENGINEERING,
        category=RuleCategory.STRUCTURAL,
        severity=RuleSeverity.ERROR,
        status=RuleStatus.VERIFIED,
        eq_reference="EQ-0010, EQ-0011, EQ-0015",
        evidence_reference="EQ-0010 Spike 4, EQ-0011 Spike 3, EQ-0015 Spikes 1-4",
        authority_reference="docs/contracts/BOQ_Intelligence_Public_Evidence_Contract_v1.0.md",
        inputs=("structural_containment_findings",),
        consumers=("Validation Engine",),
        regression_test="tests/domain/test_registry.py",
        notes="Maps to Validation Engine rule V-017. EQ-0015 confirmed the implementation is correct "
              "and the docstring was the only inconsistent artifact.",
        rule_version="1.0.0",
    ))

    # --- Completeness ---

    rules.append(DomainRule(
        rule_id="E-010",
        name="Code Completeness Ratio",
        description="Calculate ratio of rows with codes to total rows.",
        authority=RuleAuthority.ENGINEERING,
        category=RuleCategory.COMPLETENESS,
        severity=RuleSeverity.INFO,
        status=RuleStatus.VERIFIED,
        eq_reference="EQ-0012",
        evidence_reference="EQ-0012 Spike 3 — Contract Invariants (SI-BS-01)",
        authority_reference="docs/contracts/BOQ_Intelligence_Public_Evidence_Contract_v1.0.md",
        inputs=("boq_statistics",),
        consumers=("Validation Engine",),
        regression_test="tests/domain/test_registry.py",
        notes="Maps to Validation Engine rule V-007.",
        rule_version="1.0.0",
    ))

    rules.append(DomainRule(
        rule_id="E-011",
        name="Description Completeness Ratio",
        description="Calculate ratio of rows with descriptions to total rows.",
        authority=RuleAuthority.ENGINEERING,
        category=RuleCategory.COMPLETENESS,
        severity=RuleSeverity.INFO,
        status=RuleStatus.VERIFIED,
        eq_reference="EQ-0012",
        evidence_reference="EQ-0012 Spike 3 — Contract Invariants (SI-BS-02)",
        authority_reference="docs/contracts/BOQ_Intelligence_Public_Evidence_Contract_v1.0.md",
        inputs=("boq_statistics",),
        consumers=("Validation Engine",),
        regression_test="tests/domain/test_registry.py",
        notes="Maps to Validation Engine rule V-008.",
        rule_version="1.0.0",
    ))

    rules.append(DomainRule(
        rule_id="E-012",
        name="Quantity Completeness Ratio",
        description="Calculate ratio of rows with quantities to total rows.",
        authority=RuleAuthority.ENGINEERING,
        category=RuleCategory.COMPLETENESS,
        severity=RuleSeverity.INFO,
        status=RuleStatus.VERIFIED,
        eq_reference="EQ-0012",
        evidence_reference="EQ-0012 Spike 3 — Contract Invariants (SI-BS-03)",
        authority_reference="docs/contracts/BOQ_Intelligence_Public_Evidence_Contract_v1.0.md",
        inputs=("boq_statistics",),
        consumers=("Validation Engine",),
        regression_test="tests/domain/test_registry.py",
        notes="Maps to Validation Engine rule V-009.",
        rule_version="1.0.0",
    ))

    rules.append(DomainRule(
        rule_id="E-013",
        name="Zero Quantity Detection",
        description="Detect Item rows with quantity == 0.0.",
        authority=RuleAuthority.ENGINEERING,
        category=RuleCategory.COMPLETENESS,
        severity=RuleSeverity.INFO,
        status=RuleStatus.VERIFIED,
        eq_reference="EQ-0010, EQ-0011",
        evidence_reference="EQ-0010 Spike 1, EQ-0011 Spike 2, EQ-0011 Spike 3",
        authority_reference="docs/contracts/BOQ_Intelligence_Public_Evidence_Contract_v1.0.md",
        inputs=("zero_quantity_items",),
        consumers=("Validation Engine",),
        regression_test="tests/domain/test_registry.py",
        notes="Maps to Validation Engine rule V-016. Records observable facts — does not assess acceptability.",
        rule_version="1.0.0",
    ))

    rules.append(DomainRule(
        rule_id="E-014",
        name="Empty Section Detection",
        description="Detect sections with zero measurable items.",
        authority=RuleAuthority.ENGINEERING,
        category=RuleCategory.COMPLETENESS,
        severity=RuleSeverity.INFO,
        status=RuleStatus.VERIFIED,
        eq_reference="EQ-0010, EQ-0011",
        evidence_reference="EQ-0010 Spike 3, EQ-0011 Spike 3",
        authority_reference="docs/contracts/BOQ_Intelligence_Public_Evidence_Contract_v1.0.md",
        inputs=("completeness_findings",),
        consumers=("Validation Engine",),
        regression_test="tests/domain/test_registry.py",
        notes="Maps to Validation Engine rule V-018. Records observable facts — does not assess project completeness.",
        rule_version="1.0.0",
    ))

    # --- Anomaly Detection ---

    rules.append(DomainRule(
        rule_id="E-015",
        name="Anomaly Row Range",
        description="Verify known_anomalies row_numbers are within [1, total_rows].",
        authority=RuleAuthority.ENGINEERING,
        category=RuleCategory.ANOMALY_DETECTION,
        severity=RuleSeverity.ERROR,
        status=RuleStatus.VERIFIED,
        eq_reference="EQ-0012",
        evidence_reference="EQ-0012 Spike 3 — Contract Invariants (SI-KA-02)",
        authority_reference="docs/contracts/BOQ_Intelligence_Public_Evidence_Contract_v1.0.md",
        inputs=("known_anomalies", "boq_statistics"),
        consumers=("Validation Engine",),
        regression_test="tests/domain/test_registry.py",
        notes="Maps to Validation Engine rule V-006.",
        rule_version="1.0.0",
    ))

    rules.append(DomainRule(
        rule_id="E-016",
        name="Root Header Count",
        description="Report number of root headers in reconstructed hierarchy.",
        authority=RuleAuthority.ENGINEERING,
        category=RuleCategory.STRUCTURAL,
        severity=RuleSeverity.INFO,
        status=RuleStatus.VERIFIED,
        eq_reference="EQ-0010",
        evidence_reference="EQ-0010 Spike 4 — Hierarchy Reconstruction",
        authority_reference="docs/contracts/BOQ_Intelligence_Public_Evidence_Contract_v1.0.md",
        inputs=("hierarchy_statistics",),
        consumers=("Validation Engine",),
        regression_test="tests/domain/test_registry.py",
        notes="Maps to Validation Engine rule V-011.",
        rule_version="1.0.0",
    ))

    rules.append(DomainRule(
        rule_id="E-017",
        name="Hierarchy Depth Distribution",
        description="Report min/max depth of reconstructed hierarchy.",
        authority=RuleAuthority.ENGINEERING,
        category=RuleCategory.STRUCTURAL,
        severity=RuleSeverity.INFO,
        status=RuleStatus.VERIFIED,
        eq_reference="EQ-0010",
        evidence_reference="EQ-0010 Spike 4 — Hierarchy Reconstruction",
        authority_reference="docs/contracts/BOQ_Intelligence_Public_Evidence_Contract_v1.0.md",
        inputs=("hierarchy_statistics",),
        consumers=("Validation Engine",),
        regression_test="tests/domain/test_registry.py",
        notes="Maps to Validation Engine rule V-012.",
        rule_version="1.0.0",
    ))

    rules.append(DomainRule(
        rule_id="E-018",
        name="Level Skip Magnitude",
        description="Report min/max skip magnitude for detected level skips.",
        authority=RuleAuthority.ENGINEERING,
        category=RuleCategory.STRUCTURAL,
        severity=RuleSeverity.INFO,
        status=RuleStatus.VERIFIED,
        eq_reference="EQ-0010, EQ-0011",
        evidence_reference="EQ-0010 Spike 4, EQ-0011 Spike 2, EQ-0011 Spike 3",
        authority_reference="docs/contracts/BOQ_Intelligence_Public_Evidence_Contract_v1.0.md",
        inputs=("detected_level_skips",),
        consumers=("Validation Engine",),
        regression_test="tests/domain/test_registry.py",
        notes="Maps to Validation Engine rule V-015.",
        rule_version="1.0.0",
    ))

    # ============================================================
    # Domain-Derived Rules (D-001 through D-004)
    # ============================================================
    # These rules are sourced from office standards, professional
    # conventions, or QS authority. They require Project Owner or
    # QS authority to change.

    rules.append(DomainRule(
        rule_id="D-001",
        name="Duplicate Item Code Detection",
        description="Detect duplicate item codes within the same BOQ. "
                    "Duplicate codes indicate data-entry errors per office standards.",
        authority=RuleAuthority.DOMAIN,
        category=RuleCategory.DOMAIN_QUALITY,
        severity=RuleSeverity.WARNING,
        status=RuleStatus.IMPLEMENTED,
        eq_reference=None,
        evidence_reference="docs/domain/Duplicate_Code_Policy.md",
        authority_reference="docs/domain/Duplicate_Code_Policy.md",
        inputs=("row_classification",),
        consumers=("CheckMate",),
        regression_test="tests/domain/test_executor.py",
        notes="Implemented per CB-0004. Policy documented in Duplicate_Code_Policy.md v1.0. "
              "10 regression tests passing. "
              "Rule logic: group Item rows by code (case-sensitive, trimmed), detect groups with count > 1.",
        rule_version="1.0.0",
    ))

    rules.append(DomainRule(
        rule_id="D-002",
        name="Missing Description Detection",
        description="Detect Item rows with missing (None) descriptions.",
        authority=RuleAuthority.DOMAIN,
        category=RuleCategory.DOMAIN_QUALITY,
        severity=RuleSeverity.WARNING,
        status=RuleStatus.IMPLEMENTED,
        eq_reference=None,
        evidence_reference="docs/domain/Missing_Description_Policy.md",
        authority_reference="docs/domain/Missing_Description_Policy.md",
        inputs=("boq_statistics",),
        consumers=("CheckMate",),
        regression_test="tests/domain/test_executor.py",
        notes="Implemented per CB-0004. Policy documented in Missing_Description_Policy.md v1.0. "
              "9 regression tests passing. "
              "Rule logic: iterate over Item rows, flag rows where description is None or empty/whitespace.",
        rule_version="1.0.0",
    ))

    rules.append(DomainRule(
        rule_id="D-003",
        name="Missing UOM Detection",
        description="Detect Item rows with missing (None) UOMs.",
        authority=RuleAuthority.DOMAIN,
        category=RuleCategory.DOMAIN_QUALITY,
        severity=RuleSeverity.WARNING,
        status=RuleStatus.IMPLEMENTED,
        eq_reference=None,
        evidence_reference="docs/domain/Missing_UOM_Policy.md",
        authority_reference="docs/domain/Missing_UOM_Policy.md",
        inputs=("boq_statistics",),
        consumers=("CheckMate",),
        regression_test="tests/domain/test_executor.py",
        notes="Implemented per CB-0004. Policy documented in Missing_UOM_Policy.md v1.0. "
              "9 regression tests passing. "
              "Rule logic: iterate over Item rows with non-zero quantity, flag rows where UOM is None or empty.",
        rule_version="1.0.0",
    ))

    rules.append(DomainRule(
        rule_id="D-004",
        name="Trade Classification",
        description="Classify BOQ items by trade category (structural, architectural, "
                    "mechanical, electrical, etc.) based on item code patterns or descriptions.",
        authority=RuleAuthority.DOMAIN,
        category=RuleCategory.TRADE,
        severity=RuleSeverity.INFO,
        status=RuleStatus.IMPLEMENTED,
        eq_reference=None,
        evidence_reference="data/reports/eq0016_trade_classification_evidence.md",
        authority_reference="docs/domain/Trade_Taxonomy.md",
        inputs=("row_classification",),
        consumers=("CheckMate", "Formatter"),
        regression_test="tests/domain/test_executor.py",
        notes="Implemented per CB-0005. Evidence documented in EQ-0016 report. "
              "Deterministic prefix-based classification. "
              "26 CostX trade sections mapped to 9 Jarvis trades. "
              "Unknown items return 'UNKNOWN' rather than guessing.",
        rule_version="1.0.0",
    ))

    # Sort by rule_id for deterministic ordering
    rules.sort(key=lambda r: r.rule_id)
    return tuple(rules)


# Singleton registry — built once at module load time
_REGISTRY: RuleRegistry | None = None


def load_registry() -> RuleRegistry:
    """Load the domain rule registry.

    Returns the singleton RuleRegistry instance.
    Immutable after loading. Deterministic ordering.
    """
    global _REGISTRY
    if _REGISTRY is None:
        _REGISTRY = RuleRegistry(rules=_build_rules())
    return _REGISTRY


def get_registry() -> RuleRegistry:
    """Get the loaded registry. Must call load_registry() first."""
    if _REGISTRY is None:
        raise RuntimeError(
            "Registry not loaded. Call load_registry() first."
        )
    return _REGISTRY