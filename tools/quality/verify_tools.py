"""
verify_tools.py — Tool Classification and Placement Validation

Automated verification of tool organization, classification,
and compliance with governance rules. Ensures tools are
properly categorized as reusable or historical evidence.

Authority: Quality Gate 3 (Consumer Readiness)
Consumers: verify_all.py, CI, Pull Request validation
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Tuple, List, Dict

from shared_governance import (
    PROJECT_ROOT, RepositoryPath, RepositoryModel, FileValidator, ValidationResult,
    generate_validation_report, write_markdown_report
)

EXIT_PASS = 0
EXIT_FAIL = 1
EXIT_ERROR = 2

def validate_tool_classification() -> ValidationResult:
    """Validate that all tools are properly classified."""
    findings = []
    tools_dir = RepositoryPath.TOOLS_ROOT.value
    quality_dir = RepositoryPath.TOOLS_QUALITY.value

    ok_tools_dir, tools_dir_findings = FileValidator.validate_directory_exists(tools_dir, "tools directory not found")
    findings.extend(tools_dir_findings)
    if not ok_tools_dir:
        return ValidationResult(False, findings)

    ok_quality_dir, quality_dir_findings = FileValidator.validate_directory_exists(quality_dir, "tools/quality directory not found")
    findings.extend(quality_dir_findings)
    if not ok_quality_dir:
        return ValidationResult(False, findings)

    root_tools = [f for f in tools_dir.iterdir() if f.is_file() and f.suffix == ".py"]
    quality_tools = [f for f in quality_dir.iterdir() if f.is_file() and f.suffix == ".py"]

    historical_tools = []
    unclassified_tools = []

    for tool in root_tools:
        if tool.name.startswith("eq") and re.match(r"eq\d{4}_", tool.name):
            historical_tools.append(tool.name)
        else:
            unclassified_tools.append(tool.name)

    if unclassified_tools:
        findings.append(f"ERROR: Unclassified tools in tools/ root: {', '.join(unclassified_tools)}")

    if historical_tools:
        findings.append(f"INFO: Found {len(historical_tools)} historical tools preserved in tools/ root")

    for tool in quality_tools:
        if not tool.name.startswith("verify_") or not tool.name.endswith(".py"):
            findings.append(f"ERROR: Quality tool has incorrect naming: {tool.name} (should be verify_*.py)")

    return ValidationResult(len(findings) == 0, findings)

def validate_tool_registry() -> ValidationResult:
    """Validate Tool Registry completeness and accuracy."""
    findings = []
    registry_path = RepositoryPath.TOOLS_QUALITY.value / "Tool_Registry.md"
    quality_dir = RepositoryPath.TOOLS_QUALITY.value

    ok_registry_exists, exists_findings = FileValidator.validate_file_exists(registry_path, "Tool_Registry.md not found")
    findings.extend(exists_findings)
    if not ok_registry_exists:
        return ValidationResult(False, findings)

    ok_quality_dir, dir_findings = FileValidator.validate_directory_exists(quality_dir, "tools/quality directory not found")
    findings.extend(dir_findings)
    if not ok_quality_dir:
        return ValidationResult(False, findings)

    required_sections = [
        "## Purpose",
        "## Active Tools",
        "## Historical Evidence Tools"
    ]
    ok_sections, sections_findings = FileValidator.validate_file_content_contains(registry_path, required_sections, "Tool Registry")
    findings.extend(sections_findings)

    try:
        registry_content = registry_path.read_text(encoding="utf-8")
        active_tools_pattern = r"\| `?verify_(\w+)\.py`?"
        active_tool_names_from_registry = re.findall(active_tools_pattern, registry_content)

        for tool_name_stem in active_tool_names_from_registry:
            tool_path = quality_dir / f"verify_{tool_name_stem}.py"
            if not tool_path.exists():
                findings.append(f"ERROR: Tool registered but not found: verify_{tool_name_stem}.py")

        existing_tool_files_in_quality = [f.stem for f in quality_dir.glob("verify_*.py")]
        registered_tool_files = [f"verify_{name_stem}" for name_stem in active_tool_names_from_registry]

        unregistered_tools = set(existing_tool_files_in_quality) - set(registered_tool_files)
        if unregistered_tools:
            findings.append(f"ERROR: Tools exist in {quality_dir.relative_to(PROJECT_ROOT)} but not registered: {', '.join(sorted(unregistered_tools))}")

    except Exception as e:
        findings.append(f"ERROR: Could not read or parse Tool Registry: {e}")
        return ValidationResult(False, findings)

    return ValidationResult(len(findings) == 0, findings)

def validate_manifest() -> ValidationResult:
    """Validate tools/manifest.json completeness and accuracy."""
    findings = []
    manifest_path = PROJECT_ROOT / "tools" / "manifest.json"
    quality_dir = RepositoryPath.TOOLS_QUALITY.value

    ok_manifest_exists, exists_findings = FileValidator.validate_file_exists(manifest_path, "tools/manifest.json not found")
    findings.extend(exists_findings)
    if not ok_manifest_exists:
        return ValidationResult(False, findings)

    ok_quality_dir, dir_findings = FileValidator.validate_directory_exists(quality_dir, "tools/quality directory not found")
    findings.extend(dir_findings)
    if not ok_quality_dir:
        return ValidationResult(False, findings)

    try:
        manifest_content = manifest_path.read_text(encoding="utf-8")
        manifest = json.loads(manifest_content)

        if not isinstance(manifest, dict):
            findings.append("ERROR: tools/manifest.json is not a valid JSON object")
            return ValidationResult(False, findings)

        required_fields = {"authority", "inputs", "outputs", "description"}

        for tool_name_stem, tool_data in manifest.items():
            tool_path = quality_dir / f"{tool_name_stem}.py"
            ok_tool_exists, tool_exists_findings = FileValidator.validate_file_exists(tool_path, f"Tool in manifest but not found: {tool_name_stem}.py")
            findings.extend(tool_exists_findings)
            if not ok_tool_exists:
                continue

            missing_fields = required_fields - set(tool_data.keys())
            if missing_fields:
                findings.append(f"ERROR: Tool '{tool_name_stem}' missing manifest fields: {', '.join(missing_fields)}")

            if not isinstance(tool_data.get("authority"), str):
                findings.append(f"ERROR: Tool '{tool_name_stem}' has invalid 'authority' field type (expected string)")

            if not isinstance(tool_data.get("inputs"), list):
                findings.append(f"ERROR: Tool '{tool_name_stem}' has invalid 'inputs' field type (expected list)")

            if not isinstance(tool_data.get("outputs"), list):
                findings.append(f"ERROR: Tool '{tool_name_stem}' has invalid 'outputs' field type (expected list)")

    except json.JSONDecodeError:
        findings.append("ERROR: tools/manifest.json is not valid JSON")
        return ValidationResult(False, findings)
    except Exception as e:
        findings.append(f"ERROR: Could not read tools/manifest.json: {e}")
        return ValidationResult(False, findings)

    return ValidationResult(len(findings) == 0, findings)

def validate_historical_tools() -> ValidationResult:
    """Validate historical tools are properly preserved."""
    findings = []
    tools_dir = RepositoryPath.TOOLS_ROOT.value

    ok_tools_dir, tools_dir_findings = FileValidator.validate_directory_exists(tools_dir, "tools directory not found")
    findings.extend(tools_dir_findings)
    if not ok_tools_dir:
        return ValidationResult(False, findings)

    historical_tools = list(tools_dir.glob("eq*.py"))

    if not historical_tools:
        findings.append("INFO: No historical tools found in tools/ root")
        return ValidationResult(True, findings)

    for tool in historical_tools:
        if not re.match(r"eq\d{4}_\w+_\w+\.py", tool.name):
            findings.append(f"WARN: Historical tool has non-standard naming: {tool.name}")

    registry_path = RepositoryPath.TOOLS_QUALITY.value / "Tool_Registry.md"
    if registry_path.exists():
        try:
            registry_content = registry_path.read_text(encoding="utf-8")
            for tool in historical_tools:
                if tool.name not in registry_content:
                    findings.append(f"WARN: Historical tool not documented in Tool Registry: {tool.name}")
        except Exception as e:
            findings.append(f"ERROR: Could not read Tool Registry for historical tool documentation check: {e}")

    findings.append(f"INFO: Found {len(historical_tools)} historical tools preserved as evidence")

    return ValidationResult(len(findings) == 0, findings)

def validate_tool_architectural_justification() -> ValidationResult:
    """Validate that tools have proper architectural justification."""
    findings = []
    registry_path = RepositoryPath.TOOLS_QUALITY.value / "Tool_Registry.md"

    ok_registry_exists, exists_findings = FileValidator.validate_file_exists(registry_path, "Tool_Registry.md not found")
    findings.extend(exists_findings)
    if not ok_registry_exists:
        return ValidationResult(False, findings)

    required_sections = [
        "## Purpose",
        "## Tool Contract"
    ]
    ok_sections, sections_findings = FileValidator.validate_file_content_contains(registry_path, required_sections, "Tool Registry")
    findings.extend(sections_findings)

    try:
        registry_content = registry_path.read_text(encoding="utf-8")
        tool_pattern = r"\| `?verify_(\w+)\.py`?\s*\|\s*([^\|]+)\s*\|\s*([^\|]+)"
        tool_matches = re.findall(tool_pattern, registry_content)

        for tool_name_stem, purpose, authority in tool_matches:
            if not purpose or purpose.strip() == "-":
                findings.append(f"ERROR: Tool verify_{tool_name_stem}.py missing purpose documentation in Tool Registry")

            if not authority or authority.strip() == "-":
                findings.append(f"ERROR: Tool verify_{tool_name_stem}.py missing authority documentation in Tool Registry")

    except Exception as e:
        findings.append(f"ERROR: Could not read or parse Tool Registry for architectural justification: {e}")
        return ValidationResult(False, findings)

    return ValidationResult(len(findings) == 0, findings)

def validate_tool_promotion() -> ValidationResult:
    """Validate that tool promotion follows governance rules."""
    findings = []
    registry_path = RepositoryPath.TOOLS_QUALITY.value / "Tool_Registry.md"
    tools_dir = RepositoryPath.TOOLS_ROOT.value

    ok_registry_exists, exists_findings = FileValidator.validate_file_exists(registry_path, "Tool_Registry.md not found")
    findings.extend(exists_findings)
    if not ok_registry_exists:
        return ValidationResult(False, findings)

    try:
        registry_content = registry_path.read_text(encoding="utf-8")

        if "## Historical Evidence Tools" not in registry_content:
            findings.append("ERROR: Tool Registry missing 'Historical Evidence Tools' section")

        if "## Replacement History" not in registry_content:
            findings.append("WARN: Tool Registry missing 'Replacement History' section")

        historical_tools = list(tools_dir.glob("eq*.py"))

        if "Promoted from" in registry_content: # A simple heuristic for now
            findings.append("INFO: Tool promotions are documented in registry")
        elif historical_tools:
            findings.append("WARN: Historical tools exist but no explicit promotion documentation found in registry")

    except Exception as e:
        findings.append(f"ERROR: Could not read Tool Registry for tool promotion checks: {e}")
        return ValidationResult(False, findings)

    return ValidationResult(len(findings) == 0, findings)

def validate_tool_contract_compliance() -> ValidationResult:
    """Validate that quality tools comply with the tool contract."""
    findings = []
    quality_dir = RepositoryPath.TOOLS_QUALITY.value

    ok_quality_dir, dir_findings = FileValidator.validate_directory_exists(quality_dir, "tools/quality directory not found")
    findings.extend(dir_findings)
    if not ok_quality_dir:
        return ValidationResult(False, findings)

    registry_path = quality_dir / "Tool_Registry.md"
    contract_requirements = []

    ok_registry_exists, registry_exists_findings = FileValidator.validate_file_exists(registry_path, "Tool_Registry.md not found to extract contract requirements")
    findings.extend(registry_exists_findings)
    if ok_registry_exists:
        try:
            registry_content = registry_path.read_text(encoding="utf-8")
            contract_section = re.search(r"## Tool Contract(.*?)(?=## |$)", registry_content, re.DOTALL)
            if contract_section:
                contract_text = contract_section.group(1)
                if "--help" in contract_text: contract_requirements.append("help")
                if "--json" in contract_text: contract_requirements.append("json")
                if "--strict" in contract_text: contract_requirements.append("strict")
                if "--output" in contract_text: contract_requirements.append("output")
        except Exception as e:
            findings.append(f"ERROR: Could not read Tool Registry for contract requirements: {e}")
            # Do not return, continue with what requirements we could gather

    quality_tools = list(quality_dir.glob("verify_*.py"))

    for tool in quality_tools:
        try:
            content = tool.read_text(encoding="utf-8")

            if "help" in contract_requirements and "--help" not in content:
                findings.append(f"ERROR: Tool {tool.name} missing --help argument as per Tool Contract")
            if "json" in contract_requirements and "--json" not in content:
                findings.append(f"ERROR: Tool {tool.name} missing --json argument as per Tool Contract")
            if "strict" in contract_requirements and "--strict" not in content:
                findings.append(f"ERROR: Tool {tool.name} missing --strict argument as per Tool Contract")
            if "output" in contract_requirements and "--output" not in content:
                findings.append(f"ERROR: Tool {tool.name} missing --output argument as per Tool Contract")

            if "EXIT_PASS" not in content or "EXIT_FAIL" not in content:
                findings.append(f"ERROR: Tool {tool.name} missing standard EXIT_PASS/EXIT_FAIL exit codes")

        except Exception as e:
            findings.append(f"ERROR: Could not read tool {tool.name} for contract compliance: {e}")

    return ValidationResult(len(findings) == 0, findings)

def main():
    parser = argparse.ArgumentParser(description="Tool Classification and Placement Validation")
    parser.add_argument("--json", action="store_true", help="Output JSON to stdout")
    parser.add_argument("--strict", action="store_true", help="Exit 1 on any finding")
    parser.add_argument("--output", type=str, help="Write report to file (.json or .md)")
    args = parser.parse_args()

    checks_to_run = [
        ("tool_classification", validate_tool_classification),
        ("tool_registry", validate_tool_registry),
        ("manifest", validate_manifest),
        ("historical_tools", validate_historical_tools),
        ("architectural_justification", validate_tool_architectural_justification),
        ("tool_promotion", validate_tool_promotion),
        ("contract_compliance", validate_tool_contract_compliance),
    ]

    all_check_results = []
    for name, fn in checks_to_run:
        try:
            result = fn()
            all_check_results.append((name, result))
        except Exception as e:
            all_check_results.append((name, ValidationResult(False, [f"ERROR: Validation failed with exception: {e}"])))
            
    report = generate_validation_report("verify_tools", all_check_results)
    all_pass = report["overall_pass"]

    if args.json:
        print(json.dumps(report, indent=2))

    if args.output:
        output_path = Path(args.output)
        if output_path.suffix == ".json":
            output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
        elif output_path.suffix == ".md":
            write_markdown_report(report, output_path)
        print(f"Report written to: {output_path}")

    if not all_pass:
        sys.exit(EXIT_FAIL if args.strict else EXIT_FAIL)
    sys.exit(EXIT_PASS)

if __name__ == "__main__":
    main()
