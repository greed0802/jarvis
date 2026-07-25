"""EQ-0013 Spike 4: Validation Engine Verification Tool

Generates evidence by executing the Validation Engine against:
1. Minimal BOQ evidence (base case)
2. Evidence with hierarchy
3. Evidence with detection
4. Repeat determinism check (3 runs)

Produces: data/reports/eq0013_spike4_verification_evidence.json

Purpose: Supporting evidence for Spike 4 Evidence Report.
"""

import json
import sys
sys.path.insert(0, "src")

from dataclasses import dataclass

from jarvis.engines.validation.engine import (
    validate,
    ValidationFindings,
    ValidationFinding,
    ENGINE_VERSION,
    CONTRACT_VERSION,
)

@dataclass(frozen=True)
class MockEvidence:
    row_classification: dict
    section_statistics: dict
    boq_statistics: dict
    known_anomalies: list
    hierarchy: tuple | None
    hierarchy_statistics: dict | None
    detected_level_skips: tuple | None
    zero_quantity_items: tuple | None
    structural_containment_findings: tuple | None
    completeness_findings: tuple | None

def build_base_evidence():
    return MockEvidence(
        row_classification={"Head": 3, "Note": 1, "Section": 2, "Item": 10, "Other": 0},
        section_statistics={"S1": {"item_count": 10, "quantity_count": 5},
                           "S2": {"item_count": 5, "quantity_count": 3}},
        boq_statistics={
            "total_rows": 16, "code_rows": 12,
            "description_rows": 7, "quantity_rows": 6,
        },
        known_anomalies=[{"row_number": 5, "type": "missing_code"}],
        hierarchy=None, hierarchy_statistics=None,
        detected_level_skips=None, zero_quantity_items=None,
        structural_containment_findings=None, completeness_findings=None,
    )

def build_full_evidence():
    return MockEvidence(
        row_classification={"Head": 3, "Note": 1, "Section": 2, "Item": 10, "Other": 0},
        section_statistics={"S1": {"item_count": 10, "quantity_count": 5}},
        boq_statistics={
            "total_rows": 16, "code_rows": 12,
            "description_rows": 7, "quantity_rows": 6,
        },
        known_anomalies=[{"row_number": 5, "type": "missing_code"}],
        hierarchy=(),
        hierarchy_statistics={"root_headers": 1, "min_depth": 1, "max_depth": 3,
                              "total_items": 10},
        detected_level_skips=(
            {"from_level": 1, "to_level": 3, "skip_levels": 2},
            {"from_level": 2, "to_level": 4, "skip_levels": 2},
        ),
        zero_quantity_items=(
            {"row_number": 8, "quantity": 0, "description": "Item A"},
        ),
        structural_containment_findings=(
            {"parent_level": 2, "child_level": 3, "type": "inversion"},
        ),
        completeness_findings=(
            {"section": "S3", "item_count": 0},
            {"section": "S5", "item_count": 0},
        ),
    )

def findings_to_dict(findings: ValidationFindings):
    return {
        "engine_version": findings.engine_version,
        "contract_version": findings.contract_version,
        "execution_timestamp": findings.execution_timestamp,
        "total_findings": len(findings.findings),
        "findings": [
            {
                "rule_id": f.rule_id,
                "rule_version": f.rule_version,
                "category": f.category,
                "finding_type": f.finding_type,
                "finding_value": f.finding_value,
                "evidence_fields": list(f.evidence_fields),
            }
            for f in findings.findings
        ],
    }

def main():
    print("Validation Engine Verification Tool")
    print("=" * 50)

    results = {}

    # 1. Base evidence (no optional fields)
    print("\n[1/4] Base evidence (no hierarchy, no detection)...")
    base = build_base_evidence()
    base_findings = validate(base, "all")
    results["base_evidence"] = findings_to_dict(base_findings)
    print(f"  -> {len(base_findings.findings)} findings")

    # 2. Full evidence (with hierarchy + detection)
    print("[2/4] Full evidence (hierarchy + detection)...")
    full = build_full_evidence()
    full_findings = validate(full, "all")
    results["full_evidence"] = findings_to_dict(full_findings)
    print(f"  -> {len(full_findings.findings)} findings")

    # 3. Determinism: 3 runs same input
    print("[3/4] Determinism (3 runs)...")
    runs = []
    for i in range(3):
        ev = build_full_evidence()
        f = validate(ev, "all")
        runs.append(findings_to_dict(f))

    # Compare runs (exclude timestamp)
    run_ids = set()
    for r in runs:
        fingerprint = json.dumps({
            k: v for k, v in r.items()
            if k not in ("execution_timestamp", "total_findings")
        }, sort_keys=True)
        run_ids.add(fingerprint)

    deterministic = len(run_ids) == 1
    results["determinism"] = {
        "total_runs": 3,
        "unique_results": len(run_ids),
        "deterministic": deterministic,
    }
    print(f"  -> Deterministic: {deterministic} ({len(run_ids)} unique among 3 runs)")

    # 4. Specific value checks
    print("[4/4] Specific value verification...")
    checks = []
    fmap = {f.rule_id: f for f in full_findings.findings}

    # V-001: all required fields present
    checks.append({"rule": "V-001", "expected": [], "actual": fmap["V-001"].finding_value,
                   "pass": fmap["V-001"].finding_value == []})

    # V-004: sum=16, total=16 → diff=0
    checks.append({"rule": "V-004", "expected": {"difference": 0},
                   "actual": fmap["V-004"].finding_value,
                   "pass": fmap["V-004"].finding_value["difference"] == 0})

    # V-007: code_rows=12, total=16 → 0.75
    checks.append({"rule": "V-007", "expected": 0.75, "actual": fmap["V-007"].finding_value,
                   "pass": fmap["V-007"].finding_value == 0.75})

    # V-010: hierarchy available
    checks.append({"rule": "V-010", "expected": True, "actual": fmap["V-010"].finding_value,
                   "pass": fmap["V-010"].finding_value is True})

    # V-013: detection available
    checks.append({"rule": "V-013", "expected": True, "actual": fmap["V-013"].finding_value,
                   "pass": fmap["V-013"].finding_value is True})

    # V-014: 2 level skips
    checks.append({"rule": "V-014", "expected": 2, "actual": fmap["V-014"].finding_value,
                   "pass": fmap["V-014"].finding_value == 2})

    # V-016: 1 zero quantity item
    checks.append({"rule": "V-016", "expected": 1, "actual": fmap["V-016"].finding_value,
                   "pass": fmap["V-016"].finding_value == 1})

    # V-017: 1 containment finding
    checks.append({"rule": "V-017", "expected": 1, "actual": fmap["V-017"].finding_value,
                   "pass": fmap["V-017"].finding_value == 1})

    # V-018: 2 empty sections
    checks.append({"rule": "V-018", "expected": 2, "actual": fmap["V-018"].finding_value,
                   "pass": fmap["V-018"].finding_value == 2})

    all_pass = all(c["pass"] for c in checks)
    results["value_checks"] = {"checks": checks, "all_pass": all_pass}
    print(f"  -> All value checks pass: {all_pass}")

    # Write evidence
    output = {
        "title": "EQ-0013 Spike 4: Validation Engine Verification Evidence",
        "engine_version": ENGINE_VERSION,
        "contract_version": CONTRACT_VERSION,
        "evidence_contract": "BOQ Intelligence Public Evidence Contract v1.0.0",
        "output_contract": "Validation Findings Contract v1.0.0",
        "results": results,
        "summary": {
            "base_findings_count": len(results["base_evidence"]["findings"]),
            "full_findings_count": len(results["full_evidence"]["findings"]),
            "deterministic": deterministic,
            "value_checks_all_pass": all_pass,
        },
    }

    output_path = "data/reports/eq0013_spike4_verification_evidence.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, default=str)
    print(f"\nEvidence written to {output_path}")
    print("=" * 50)

    return 0 if (deterministic and all_pass) else 1

if __name__ == "__main__":
    exit(main())