"""
EQ-0013 Spike 2: Taxonomy Verification Audit

Purpose: Verify that the Rule Taxonomy and Dependency Graph are internally
         consistent, complete, and compliant with governance requirements.

Verification Criteria:
- Rule IDs unique
- Provenance complete
- Categories valid
- Lifecycle valid
- Dependency graph complete
- Version metadata complete
- Boundary classification present
- No speculative rules
- Registry internally consistent
- No new rules invented (Spike 1 baseline)

Authority: EQ-0013 Spike 2
Contract: BOQ Intelligence Public Evidence Contract v1.0.0
"""

import json
from typing import List, Dict, Tuple

def load_spike1_registry() -> dict:
    """Load Spike 1 baseline registry."""
    with open("data/reports/eq0013_spike1_validation_rule_registry.json") as f:
        return json.load(f)

def load_spike2_taxonomy() -> dict:
    """Load Spike 2 taxonomy."""
    with open("data/reports/eq0013_spike2_rule_taxonomy.json") as f:
        return json.load(f)

def load_spike2_dependency_graph() -> dict:
    """Load Spike 2 dependency graph."""
    with open("data/reports/eq0013_spike2_dependency_graph.json") as f:
        return json.load(f)

def verify_no_new_rules(spike1: dict, dep_graph: dict) -> Tuple[bool, List[str]]:
    """Verify no new rules invented beyond Spike 1."""
    issues = []
    
    spike1_rule_ids = {rule["rule_id"] for rule in spike1["rules"]}
    spike2_rule_ids = set(dep_graph["rule_dependencies"].keys())
    
    new_rules = spike2_rule_ids - spike1_rule_ids
    missing_rules = spike1_rule_ids - spike2_rule_ids
    
    if new_rules:
        issues.append(f"NEW RULES INVENTED: {sorted(new_rules)} — Spike 2 must not discover new rules")
    
    if missing_rules:
        issues.append(f"RULES MISSING: {sorted(missing_rules)} — All Spike 1 rules must be in dependency graph")
    
    return len(issues) == 0, issues

def verify_rule_id_uniqueness(dep_graph: dict) -> Tuple[bool, List[str]]:
    """Verify all Rule IDs are unique."""
    issues = []
    
    rule_ids = list(dep_graph["rule_dependencies"].keys())
    if len(rule_ids) != len(set(rule_ids)):
        duplicates = [rid for rid in set(rule_ids) if rule_ids.count(rid) > 1]
        issues.append(f"DUPLICATE RULE IDs: {duplicates}")
    
    return len(issues) == 0, issues

def verify_rule_id_format(dep_graph: dict) -> Tuple[bool, List[str]]:
    """Verify Rule ID format: V-NNN."""
    issues = []
    
    for rule_id in dep_graph["rule_dependencies"].keys():
        if not rule_id.startswith("V-"):
            issues.append(f"INVALID FORMAT: {rule_id} — must start with 'V-'")
        elif len(rule_id) != 5:
            issues.append(f"INVALID FORMAT: {rule_id} — must be V-NNN (5 chars)")
        elif not rule_id[2:].isdigit():
            issues.append(f"INVALID FORMAT: {rule_id} — NNN must be numeric")
    
    return len(issues) == 0, issues

def verify_rule_id_reservation(dep_graph: dict) -> Tuple[bool, List[str]]:
    """Verify Rule ID reservation policy (001-899 implementable, 900-999 rejected)."""
    issues = []
    
    implementable_categories = {"Structural", "Consistency", "Completeness", "Detection"}
    rejected_categories = {"Assessment", "Recommendation", "Financial", "Reference"}
    
    for rule_id, rule_data in dep_graph["rule_dependencies"].items():
        num = int(rule_id.split("-")[1])
        category = rule_data["category"]
        
        if category in implementable_categories and num >= 900:
            issues.append(f"ID POLICY VIOLATION: {rule_id} — implementable rule in rejected range (900-999)")
        
        if category in rejected_categories and num < 900:
            issues.append(f"ID POLICY VIOLATION: {rule_id} — rejected rule in implementable range (001-899)")
    
    return len(issues) == 0, issues

def verify_provenance_complete(spike1: dict) -> Tuple[bool, List[str]]:
    """Verify all rules have complete provenance."""
    issues = []
    
    required_fields = [
        "rule_id", "category", "description", "evidence_fields",
        "boundary_class", "contract_version", "eq_source",
        "introduced_by", "deterministic_finding", "rationale", "status"
    ]
    
    for rule in spike1["rules"]:
        for field in required_fields:
            if field not in rule or rule[field] is None:
                issues.append(f"MISSING PROVENANCE: {rule['rule_id']} lacks '{field}'")
    
    return len(issues) == 0, issues

def verify_categories_valid(spike1: dict, taxonomy: dict) -> Tuple[bool, List[str]]:
    """Verify all rules use valid categories from taxonomy."""
    issues = []
    
    valid_categories = set(taxonomy["categories"].keys())
    
    for rule in spike1["rules"]:
        if rule["category"] not in valid_categories:
            issues.append(f"INVALID CATEGORY: {rule['rule_id']} uses '{rule['category']}' (not in taxonomy)")
    
    return len(issues) == 0, issues

def verify_boundary_classification(spike1: dict) -> Tuple[bool, List[str]]:
    """Verify all rules have boundary classification."""
    issues = []
    
    valid_boundaries = {"Observation", "Detection", "Relationship", "Violation"}
    
    for rule in spike1["rules"]:
        if "boundary_class" not in rule:
            issues.append(f"MISSING BOUNDARY: {rule['rule_id']} has no boundary_class")
        elif rule["boundary_class"] not in valid_boundaries:
            issues.append(f"INVALID BOUNDARY: {rule['rule_id']} uses '{rule['boundary_class']}'")
    
    return len(issues) == 0, issues

def verify_lifecycle_valid(spike1: dict, taxonomy: dict) -> Tuple[bool, List[str]]:
    """Verify all rules have valid lifecycle status."""
    issues = []
    
    valid_statuses = set(taxonomy["lifecycle"]["states"])
    
    for rule in spike1["rules"]:
        if rule["status"] not in valid_statuses:
            issues.append(f"INVALID STATUS: {rule['rule_id']} uses '{rule['status']}' (not in lifecycle)")
    
    return len(issues) == 0, issues

def verify_dependency_graph_complete(spike1: dict, dep_graph: dict) -> Tuple[bool, List[str]]:
    """Verify dependency graph has entries for all rules."""
    issues = []
    
    spike1_ids = {rule["rule_id"] for rule in spike1["rules"]}
    graph_ids = set(dep_graph["rule_dependencies"].keys())
    
    missing = spike1_ids - graph_ids
    if missing:
        issues.append(f"INCOMPLETE GRAPH: Missing entries for {sorted(missing)}")
    
    return len(issues) == 0, issues

def verify_dependency_fields_match_registry(spike1: dict, dep_graph: dict) -> Tuple[bool, List[str]]:
    """Verify dependency graph evidence_fields match Spike 1 registry."""
    issues = []
    
    for rule in spike1["rules"]:
        rid = rule["rule_id"]
        if rid not in dep_graph["rule_dependencies"]:
            continue
        
        registry_fields = set(rule["evidence_fields"])
        graph_fields = set(dep_graph["rule_dependencies"][rid]["evidence_fields"])
        
        if registry_fields != graph_fields:
            issues.append(
                f"FIELD MISMATCH: {rid} registry={sorted(registry_fields)} vs graph={sorted(graph_fields)}"
            )
    
    return len(issues) == 0, issues

def verify_no_speculative_rules(spike1: dict) -> Tuple[bool, List[str]]:
    """Verify no rules are classified as Speculative."""
    issues = []
    
    for rule in spike1["rules"]:
        if rule["classification"] == "Speculative":
            issues.append(f"SPECULATIVE RULE: {rule['rule_id']} — all rules must be evidence-backed")
    
    return len(issues) == 0, issues

def verify_rejected_rules_documented(spike1: dict) -> Tuple[bool, List[str]]:
    """Verify rejected rules are documented with rationale."""
    issues = []
    
    rejected_classifications = {"Boundary Violation", "Insufficient Evidence"}
    
    for rule in spike1["rules"]:
        if rule["classification"] in rejected_classifications:
            if "REJECTED" not in rule["rationale"]:
                issues.append(f"REJECTION NOT CLEAR: {rule['rule_id']} is rejected but rationale lacks 'REJECTED' keyword")
    
    return len(issues) == 0, issues

def verify_boundary_preservation(spike1: dict) -> Tuple[bool, List[str]]:
    """Verify EQ-0011 boundary is preserved (no assessment/recommendation in implementable rules)."""
    issues = []
    
    implementable_classifications = {"Supported", "Multiple Fields"}
    prohibited_verbs = ["assess", "judge", "evaluate", "recommend", "suggest", "advise", "should"]
    
    for rule in spike1["rules"]:
        if rule["classification"] in implementable_classifications:
            finding_lower = rule["deterministic_finding"].lower()
            for verb in prohibited_verbs:
                if verb in finding_lower:
                    issues.append(
                        f"BOUNDARY VIOLATION: {rule['rule_id']} uses prohibited verb '{verb}' in finding"
                    )
    
    return len(issues) == 0, issues

def verify_finding_types_valid(dep_graph: dict) -> Tuple[bool, List[str]]:
    """Verify all finding_type values are from taxonomy."""
    issues = []
    
    valid_finding_types = set(dep_graph["dependency_model"]["finding_types"].keys()) | {"N/A"}
    
    for rule_id, rule_data in dep_graph["rule_dependencies"].items():
        finding_type = rule_data["finding_type"]
        if finding_type not in valid_finding_types:
            issues.append(f"INVALID FINDING TYPE: {rule_id} uses '{finding_type}' (not in taxonomy)")
    
    return len(issues) == 0, issues

def verify_contract_version_consistent(spike1: dict) -> Tuple[bool, List[str]]:
    """Verify all rules reference Contract v1.0.0."""
    issues = []
    
    for rule in spike1["rules"]:
        if rule["contract_version"] != "1.0.0":
            issues.append(f"VERSION MISMATCH: {rule['rule_id']} references contract {rule['contract_version']}, expected 1.0.0")
    
    return len(issues) == 0, issues

def run_all_verifications() -> Dict[str, Tuple[bool, List[str]]]:
    """Run all verification checks."""
    
    print("=" * 60)
    print("EQ-0013 Spike 2: Taxonomy Verification Audit")
    print("=" * 60)
    print()
    
    # Load artifacts
    print("Loading artifacts...")
    spike1 = load_spike1_registry()
    taxonomy = load_spike2_taxonomy()
    dep_graph = load_spike2_dependency_graph()
    print(f"  Spike 1 Registry: {spike1['total_rules']} rules")
    print(f"  Spike 2 Taxonomy: {len(taxonomy['categories'])} categories")
    print(f"  Dependency Graph: {len(dep_graph['rule_dependencies'])} entries")
    print()
    
    # Run verifications
    results = {}
    
    print("Running verifications...")
    print()
    
    checks = [
        ("No New Rules Invented", lambda: verify_no_new_rules(spike1, dep_graph)),
        ("Rule ID Uniqueness", lambda: verify_rule_id_uniqueness(dep_graph)),
        ("Rule ID Format", lambda: verify_rule_id_format(dep_graph)),
        ("Rule ID Reservation Policy", lambda: verify_rule_id_reservation(dep_graph)),
        ("Provenance Complete", lambda: verify_provenance_complete(spike1)),
        ("Categories Valid", lambda: verify_categories_valid(spike1, taxonomy)),
        ("Boundary Classification", lambda: verify_boundary_classification(spike1)),
        ("Lifecycle Valid", lambda: verify_lifecycle_valid(spike1, taxonomy)),
        ("Dependency Graph Complete", lambda: verify_dependency_graph_complete(spike1, dep_graph)),
        ("Dependency Fields Match", lambda: verify_dependency_fields_match_registry(spike1, dep_graph)),
        ("No Speculative Rules", lambda: verify_no_speculative_rules(spike1)),
        ("Rejected Rules Documented", lambda: verify_rejected_rules_documented(spike1)),
        ("Boundary Preservation", lambda: verify_boundary_preservation(spike1)),
        ("Finding Types Valid", lambda: verify_finding_types_valid(dep_graph)),
        ("Contract Version Consistent", lambda: verify_contract_version_consistent(spike1)),
    ]
    
    for check_name, check_fn in checks:
        passed, issues = check_fn()
        results[check_name] = (passed, issues)
        
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {check_name}")
        if issues:
            for issue in issues:
                print(f"    {issue}")
    
    print()
    
    # Summary
    total_checks = len(checks)
    passed_checks = sum(1 for p, _ in results.values() if p)
    
    print("=" * 60)
    print(f"Verification Summary: {passed_checks}/{total_checks} checks passed")
    print("=" * 60)
    
    if passed_checks == total_checks:
        print()
        print("✓ ALL VERIFICATIONS PASSED")
        print()
        print("Taxonomy and Dependency Graph are internally consistent,")
        print("complete, and compliant with governance requirements.")
    else:
        print()
        print("✗ VERIFICATION FAILURES DETECTED")
        print()
        print("Fix issues before freezing Spike 2.")
    
    print()
    
    # Save verification report
    report = {
        "verification_version": "1.0.0",
        "spike": "EQ-0013 Spike 2",
        "contract_version": "1.0.0",
        "total_checks": total_checks,
        "passed_checks": passed_checks,
        "failed_checks": total_checks - passed_checks,
        "checks": {
            name: {"passed": passed, "issues": issues}
            for name, (passed, issues) in results.items()
        },
        "conclusion": "PASS" if passed_checks == total_checks else "FAIL",
    }
    
    report_path = "data/reports/eq0013_spike2_verification.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"✓ Saved Verification Report: {report_path}")
    
    return results

if __name__ == "__main__":
    results = run_all_verifications()
    
    # Exit with error code if any check failed
    all_passed = all(passed for passed, _ in results.values())
    exit(0 if all_passed else 1)