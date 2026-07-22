"""Validation Rule Registry Validator.

Verifies the embedded rule registry against the Validation Findings Contract v1.0.0.

Checks:
  - Every rule has required fields (rule_id, category, evidence_fields, status, finding_type)
  - Every rule_id is unique
  - Every rule_id matches the expected format (V-XXX)
  - Every status is valid (Approved, Candidate, Deprecated, Retired)
  - Every finding_type is valid (presence, count, ratio, difference, list, value)
  - Every evidence_field matches a field in BOQIntelligenceResult (Evidence Contract v1.0.0)
  - Every rule with status != Candidate has finding_type set
  - Every rule has contract_version set
  - Every rule has rule_version set
  - Every rule has deterministic_finding description
  - Every rule has rationale
  - Every rule has eq_source

Authority: HD-006 — Repository Hardening Sprint (Post EQ-0013)
"""

import json
import sys
from pathlib import Path

# Evidence Contract v1.0.0 fields (from BOQIntelligenceResult)
EVIDENCE_FIELDS = {
    "row_classification",
    "section_statistics",
    "boq_statistics",
    "known_anomalies",
    "hierarchy",
    "hierarchy_statistics",
    "detected_level_skips",
    "zero_quantity_items",
    "structural_containment_findings",
    "completeness_findings",
}

# Valid finding types (from Validation Findings Contract v1.0.0)
VALID_FINDING_TYPES = {
    "presence", "count", "ratio", "difference", "list", "value"
}

# Valid rule statuses
VALID_STATUSES = {
    "Approved", "Candidate", "Deprecated", "Retired"
}

def validate_registry(registry_path: Path) -> tuple[bool, list[str]]:
    """Validate the rule registry JSON file.

    Returns (is_valid, errors)
    """
    errors = []

    try:
        with open(registry_path, encoding="utf-8") as f:
            registry_data = json.load(f)
    except Exception as e:
        return False, [f"Failed to load registry: {e}"]

    # Check top-level structure
    if "registry_version" not in registry_data:
        errors.append("Missing registry_version")
    if "contract_version" not in registry_data:
        errors.append("Missing contract_version")
    if "generated_by" not in registry_data:
        errors.append("Missing generated_by")
    if "total_rules" not in registry_data:
        errors.append("Missing total_rules")
    if "rules" not in registry_data:
        return False, ["Missing rules array"]

    rules = registry_data["rules"]
    if not isinstance(rules, list):
        return False, ["rules must be an array"]

    if len(rules) != registry_data.get("total_rules", 0):
        errors.append(f"total_rules mismatch: expected {len(rules)}, got {registry_data.get('total_rules')}")

    rule_ids = set()
    for i, rule in enumerate(rules):
        rule_prefix = f"Rule {i} ({rule.get('rule_id', 'UNKNOWN')})"

        # Check required fields
        required_fields = ["rule_id", "category", "evidence_fields", "status", "finding_type"]
        for field in required_fields:
            if field not in rule:
                errors.append(f"{rule_prefix}: Missing required field '{field}'")

        # Check rule_id format
        rule_id = rule.get("rule_id", "")
        if not isinstance(rule_id, str) or not rule_id.startswith("V-"):
            errors.append(f"{rule_prefix}: rule_id must start with 'V-'")
        elif not rule_id[2:].isdigit():
            errors.append(f"{rule_prefix}: rule_id must be V- followed by digits")
        elif rule_id in rule_ids:
            errors.append(f"{rule_prefix}: Duplicate rule_id '{rule_id}'")
        else:
            rule_ids.add(rule_id)

        # Check status
        status = rule.get("status", "")
        if status not in VALID_STATUSES:
            errors.append(f"{rule_prefix}: Invalid status '{status}'")

        # Check finding_type
        finding_type = rule.get("finding_type", "")
        if finding_type not in VALID_FINDING_TYPES:
            errors.append(f"{rule_prefix}: Invalid finding_type '{finding_type}'")

        # Check evidence_fields
        evidence_fields = rule.get("evidence_fields", [])
        if not isinstance(evidence_fields, list):
            errors.append(f"{rule_prefix}: evidence_fields must be an array")
        else:
            for field in evidence_fields:
                if field not in EVIDENCE_FIELDS:
                    errors.append(f"{rule_prefix}: Invalid evidence_field '{field}'")

        # Check contract_version
        if "contract_version" not in rule:
            errors.append(f"{rule_prefix}: Missing contract_version")
        elif not isinstance(rule["contract_version"], str):
            errors.append(f"{rule_prefix}: contract_version must be a string")

        # Check rule_version
        if "rule_version" not in rule:
            errors.append(f"{rule_prefix}: Missing rule_version")
        elif not isinstance(rule["rule_version"], str):
            errors.append(f"{rule_prefix}: rule_version must be a string")

        # Check deterministic_finding
        if "deterministic_finding" not in rule:
            errors.append(f"{rule_prefix}: Missing deterministic_finding")
        elif not isinstance(rule["deterministic_finding"], str):
            errors.append(f"{rule_prefix}: deterministic_finding must be a string")

        # Check rationale
        if "rationale" not in rule:
            errors.append(f"{rule_prefix}: Missing rationale")
        elif not isinstance(rule["rationale"], str):
            errors.append(f"{rule_prefix}: rationale must be a string")

        # Check eq_source
        if "eq_source" not in rule:
            errors.append(f"{rule_prefix}: Missing eq_source")
        elif not isinstance(rule["eq_source"], str):
            errors.append(f"{rule_prefix}: eq_source must be a string")

        # Check classification (optional but recommended)
        if "classification" not in rule:
            errors.append(f"{rule_prefix}: Missing classification")
        elif rule.get("classification") not in ("Supported", "Multiple Fields", "Insufficient Evidence", "Boundary Violation"):
            errors.append(f"{rule_prefix}: Invalid classification '{rule.get('classification')}'")

        # Check boundary_class (optional but recommended)
        if "boundary_class" not in rule:
            errors.append(f"{rule_prefix}: Missing boundary_class")
        elif rule.get("boundary_class") not in ("Observation", "Detection"):
            errors.append(f"{rule_prefix}: Invalid boundary_class '{rule.get('boundary_class')}'")

        # Check that non-Candidate rules have finding_type set
        if status != "Candidate" and not finding_type:
            errors.append(f"{rule_prefix}: Non-Candidate rules must have finding_type set")

    return len(errors) == 0, errors

def main():
    """Run the registry validator."""
    registry_path = Path(__file__).parent.parent / "src" / "jarvis" / "engines" / "validation" / "data" / "rule_registry.json"

    print(f"Validating registry: {registry_path}")
    is_valid, errors = validate_registry(registry_path)

    if is_valid:
        print("✓ Registry is valid")
        return 0
    else:
        print("✗ Registry validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

if __name__ == "__main__":
    sys.exit(main())