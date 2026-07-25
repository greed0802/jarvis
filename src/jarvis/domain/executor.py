"""Domain Rule Executor — pure functions for executing domain rules.

Implements the APPROVED Domain Rules (D-001, D-002, D-003) as
deterministic, pure functions with immutable outputs.

No global state. No mutation. No runtime registration. No reflection.

Authority:
  - CB-0004 — Domain Rule Execution
  - docs/domain/Duplicate_Code_Policy.md
  - docs/domain/Missing_Description_Policy.md
  - docs/domain/Missing_UOM_Policy.md
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Callable

from jarvis.domain.models import DomainRule, RuleSeverity, RuleStatus
from jarvis.domain.registry import get_registry, load_registry
from jarvis.domain.results import DomainRuleExecutionResult, DomainRuleFinding, DomainRuleFindingType

# Mock BOQRow for type hinting purposes
@dataclass(frozen=True)
class BOQRow:
    """Mock BOQRow structure based on typical parser output."""
    row_number: int
    row_type: str  # e.g., "Head", "Note", "Section", "Item", "Other"
    item_code: str | None = None
    description: str | None = None
    quantity: float | None = None
    uom: str | None = None
    section: str | None = None
    trade: str | None = None  # Trade classification (D-004)
    # Add other fields as needed for future rules

# --- D-001: Duplicate Item Code Detection ---
def _detect_duplicate_item_codes(
    boq_rows: list[BOQRow], rule: DomainRule
) -> list[DomainRuleFinding]:
    """Detect duplicate item codes based on the Duplicate Code Policy.

    Args:
        boq_rows: A list of BOQRow objects from a single extraction.
        rule: The D-001 DomainRule instance.

    Returns:
        A list of DomainRuleFinding objects for detected duplicates.
    """
    findings: list[DomainRuleFinding] = []
    item_codes_by_normalized_code: dict[str, list[BOQRow]] = defaultdict(list)

    for row in boq_rows:
        if row.row_type == "Item" and row.item_code is not None:
            normalized_code = row.item_code.strip()
            item_codes_by_normalized_code[normalized_code].append(row)

    for normalized_code, rows_with_code in item_codes_by_normalized_code.items():
        if len(rows_with_code) > 1:
            # Check for OMISSION/ADDITION exception
            omission_addition_exception_applies = False
            if all(row.section in ("OMISSION", "ADDITION") for row in rows_with_code):
                omission_rows = [r for r in rows_with_code if r.section == "OMISSION" and (r.quantity is None or r.quantity < 0)]
                addition_rows = [r for r in rows_with_code if r.section == "ADDITION" and (r.quantity is None or r.quantity >= 0)]

                # Simple check: if there's one omission row and one addition row, with opposite sign quantities,
                # and matching descriptions (case-insensitive)
                if len(omission_rows) == 1 and len(addition_rows) == 1:
                    omission_row = omission_rows[0]
                    addition_row = addition_rows[0]
                    if (omission_row.quantity is None or omission_row.quantity < 0) and \
                       (addition_row.quantity is None or addition_row.quantity >= 0) and \
                       (omission_row.description or "").strip().lower() == (addition_row.description or "").strip().lower():
                        omission_addition_exception_applies = True

            if not omission_addition_exception_applies:
                # Flag all rows with this duplicate code as findings
                for duplicate_row in rows_with_code:
                    findings.append(
                        DomainRuleFinding(
                            rule_id=rule.rule_id,
                            finding_type=DomainRuleFindingType.DUPLICATE_ITEM_CODE,
                            severity=rule.severity,
                            message=f"Duplicate item code '{duplicate_row.item_code}' detected. "
                                    f"Original at row {rows_with_code[0].row_number}, duplicate at row {duplicate_row.row_number}.",
                            row_number=duplicate_row.row_number,
                            field_name="item_code",
                            context={
                                "duplicate_code": duplicate_row.item_code,
                                "all_row_numbers": sorted([r.row_number for r in rows_with_code]),
                            },
                        )
                    )
    return findings

# --- D-002: Missing Description Detection ---
def _detect_missing_descriptions(
    boq_rows: list[BOQRow], rule: DomainRule
) -> list[DomainRuleFinding]:
    """Detect missing descriptions based on the Missing Description Policy.

    Args:
        boq_rows: A list of BOQRow objects.
        rule: The D-002 DomainRule instance.

    Returns:
        A list of DomainRuleFinding objects for missing descriptions.
    """
    findings: list[DomainRuleFinding] = []

    for row in boq_rows:
        description_is_missing = row.description is None or not str(row.description).strip()

        if description_is_missing:
            severity = None
            if row.row_type == "Item":
                # Check for zero-quantity provisional sum exception (INFO, not WARNING)
                if row.quantity is not None and row.quantity == 0.0:
                    severity = RuleSeverity.INFO
                    message = f"Item row {row.row_number} has zero quantity and missing description (provisional sum/placeholder)."
                else:
                    severity = rule.severity # WARNING
                    message = f"Item row {row.row_number} has a missing description."
            elif row.row_type == "Head":
                # Head rows ideally have descriptions, but not critical
                severity = RuleSeverity.INFO
                message = f"Header row {row.row_number} has a missing description."
            else:
                # Notes, Sections, Other types are permitted to have missing descriptions
                continue

            if severity:
                findings.append(
                    DomainRuleFinding(
                        rule_id=rule.rule_id,
                        finding_type=DomainRuleFindingType.MISSING_DESCRIPTION,
                        severity=severity,
                        message=message,
                        row_number=row.row_number,
                        field_name="description",
                        context={"original_description": row.description},
                    )
                )
    return findings

# --- D-003: Missing UOM Detection ---
def _detect_missing_uoms(
    boq_rows: list[BOQRow], rule: DomainRule
) -> list[DomainRuleFinding]:
    """Detect missing UOMs based on the Missing UOM Policy.

    Args:
        boq_rows: A list of BOQRow objects.
        rule: The D-003 DomainRule instance.

    Returns:
        A list of DomainRuleFinding objects for missing UOMs.
    """
    findings: list[DomainRuleFinding] = []

    for row in boq_rows:
        uom_is_missing = row.uom is None or not str(row.uom).strip()

        if uom_is_missing:
            severity = None
            if row.row_type == "Item":
                # Check for zero-quantity provisional sum exception (INFO, not WARNING)
                if row.quantity is not None and row.quantity == 0.0:
                    severity = RuleSeverity.INFO
                    message = f"Item row {row.row_number} has zero quantity and missing UOM (provisional sum/placeholder)."
                else:
                    severity = rule.severity # WARNING
                    message = f"Item row {row.row_number} has a measured quantity but a missing UOM."
            else:
                # Head, Note, Section, Other types are permitted to have missing UOMs
                continue

            if severity:
                findings.append(
                    DomainRuleFinding(
                        rule_id=rule.rule_id,
                        finding_type=DomainRuleFindingType.MISSING_UOM,
                        severity=severity,
                        message=message,
                        row_number=row.row_number,
                        field_name="uom",
                        context={"original_uom": row.uom},
                    )
                )
    return findings

# --- D-004: Trade Classification ---
def classify_trade(item_code: str | None) -> str:
    """Classify BOQ items by trade based on item code prefixes.

    Deterministic classification using evidence-based patterns from CostX fixtures.
    No ML, no fuzzy matching, no heuristics — only exact prefix matching.

    Args:
        item_code: The item code to classify (e.g., "F/1", "AA/5", "CONC-001").

    Returns:
        The trade code (A-Z) for known patterns, "UNKNOWN" for unmatched items.

    Authority:
        - EQ-0016 — Trade Classification Evidence Report
        - docs/domain/Trade_Taxonomy.md
        - data/reports/eq0016_trade_classification_evidence.md
    """
    if item_code is None:
        return "UNKNOWN"

    # Extract prefix (part before first separator)
    prefix = item_code.split('/')[0].split('-')[0].strip().upper()

    # Evidence-based prefix mappings from CostX fixture analysis
    # Single-letter prefixes (A-Z) map directly to their trade
    if len(prefix) == 1 and prefix in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        return prefix

    # Trade Z (SIGNAGE) has multiple prefixes: AA-AZ, BA-BH
    if len(prefix) == 2:
        first_char = prefix[0]
        second_char = prefix[1]

        # AA-AZ pattern (includes AA)
        if first_char == 'A' and second_char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            return "Z"

        # BA-BH pattern
        if first_char == 'B' and second_char in "ABCDEFGH":
            return "Z"

    # Unknown patterns return UNKNOWN (no guessing)
    return "UNKNOWN"

def _classify_trades(
    boq_rows: list[BOQRow], rule: DomainRule
) -> list[DomainRuleFinding]:
    """Classify BOQ items by trade and return findings.

    Args:
        boq_rows: A list of BOQRow objects.
        rule: The D-004 DomainRule instance.

    Returns:
        A list of DomainRuleFinding objects for trade classifications.
    """
    findings: list[DomainRuleFinding] = []

    for row in boq_rows:
        if row.row_type == "Item" and row.item_code is not None:
            trade = classify_trade(row.item_code)

            # Create a finding for each classified item
            findings.append(
                DomainRuleFinding(
                    rule_id=rule.rule_id,
                    finding_type=DomainRuleFindingType.TRADE_CLASSIFICATION,
                    severity=rule.severity,
                    message=f"Item '{row.item_code}' classified as trade '{trade}'.",
                    row_number=row.row_number,
                    field_name="trade",
                    context={
                        "item_code": row.item_code,
                        "classified_trade": trade,
                        "description": row.description,
                    },
                )
            )

    return findings

# --- Main Executor Function ---
def execute_domain_rules(
    boq_rows: list[BOQRow], rules_to_execute: list[DomainRule] | None = None,
    metadata: dict[str, Any] | None = None
) -> DomainRuleExecutionResult:
    """Executes a set of domain rules against BOQ data.

    Args:
        boq_rows: The BOQ data as a list of BOQRow objects.
        rules_to_execute: A list of specific DomainRule objects to execute. If None,
                          all APPROVED domain rules from the registry will be executed.
        metadata: Optional dictionary of metadata to include in the result.

    Returns:
        An immutable DomainRuleExecutionResult containing all findings.
    """
    all_findings: list[DomainRuleFinding] = []
    executed_rules: list[DomainRule] = []

    if rules_to_execute is None:
        registry = load_registry()
        # Get all executable rules (APPROVED and IMPLEMENTED)
        rules_to_execute = list(registry.by_status(RuleStatus.APPROVED))
        rules_to_execute.extend(list(registry.by_status(RuleStatus.IMPLEMENTED)))

    # Ensure it's a mutable list for deterministic sorting
    if not isinstance(rules_to_execute, list):
        rules_to_execute = list(rules_to_execute)

    # Sort rules for deterministic execution order
    rules_to_execute.sort(key=lambda r: r.rule_id)

    for rule in rules_to_execute:
        # Execute only APPROVED or IMPLEMENTED rules
        if rule.status not in (RuleStatus.APPROVED, RuleStatus.IMPLEMENTED):
            continue

        executed_rules.append(rule)

        if rule.rule_id == "D-001":
            all_findings.extend(_detect_duplicate_item_codes(boq_rows, rule))
        elif rule.rule_id == "D-002":
            all_findings.extend(_detect_missing_descriptions(boq_rows, rule))
        elif rule.rule_id == "D-003":
            all_findings.extend(_detect_missing_uoms(boq_rows, rule))
        elif rule.rule_id == "D-004":
            all_findings.extend(_classify_trades(boq_rows, rule))
        # Add other rule executors here as they are implemented.

    # Sort findings for deterministic output
    all_findings.sort(key=lambda f: (f.rule_id, f.row_number or 0, f.message))

    return DomainRuleExecutionResult(
        executed_rules=tuple(executed_rules),
        findings=tuple(all_findings),
        metadata=metadata if metadata is not None else {},
    )