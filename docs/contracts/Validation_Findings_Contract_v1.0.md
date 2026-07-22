# Validation Findings Contract v1.0.0

**Classification:** Public Engineering Contract  
**Authority:** EQ-0013 Spike 4  
**Governance:** Evidence Contract Methodology (EQ-0012)  
**Lifecycle:** Candidate → Review → Approved → Frozen  
**Frozen Date:** TBD (awaiting Spike 4 freeze approval)  
**Supersedes:** None (first version)  
**Contract Type:** Public Output Contract  

---

## 1. Purpose

This contract defines the public output of the Validation Engine.

It is the equivalent of the BOQ Intelligence Public Evidence Contract for validation outputs.

All consumers of the Validation Engine (CheckMate, Formatter, Builder, O&A, Reporting) depend on this contract.

The contract guarantees:

- Finding structure
- Metadata completeness
- Deterministic output
- Immutability
- Provenance traceability
- Consumer compatibility

---

## 2. Contract Version

**Version:** v1.0.0  
**SemVer:** MAJOR.MINOR.PATCH  
**Effective:** Upon freeze approval  

### Versioning Policy

| Change Type | SemVer | Impact |
|---|---|---|
| Add optional finding field | MINOR | Consumers opt-in |
| Add new finding type | MINOR | Consumers opt-in |
| Remove finding field | MAJOR | Consumers must update |
| Rename finding field | MAJOR | Consumers must update |
| Change finding_value semantics | MAJOR | Consumers must update |
| Bug fix (no API change) | PATCH | Transparent |
| Documentation only | PATCH | Transparent |

---

## 3. ValidationFindings — Public Output

### Schema

```python
@dataclass(frozen=True)
class ValidationFinding:
    """A single deterministic finding produced by a validation rule."""
    rule_id: str              # Permanent Rule ID (e.g., "V-007")
    rule_version: str         # Rule version at execution time (e.g., "1.0.0")
    category: str             # Rule category (e.g., "Completeness")
    finding_type: str         # Finding type (e.g., "ratio", "count", "presence")
    finding_value: Any        # Deterministic finding value
    evidence_fields: tuple[str, ...]  # Evidence fields consumed

@dataclass(frozen=True)
class ValidationFindings:
    """Collection of validation findings."""
    findings: tuple[ValidationFinding, ...]
    engine_version: str       # Engine version (e.g., "1.0.0")
    contract_version: str     # This contract version (e.g., "1.0.0")
    execution_timestamp: str  # ISO 8601 timestamp (for audit only)
```

### Example

```python
ValidationFindings(
    findings=(
        ValidationFinding(
            rule_id="V-007",
            rule_version="1.0.0",
            category="Completeness",
            finding_type="ratio",
            finding_value=0.67,
            evidence_fields=("boq_statistics",),
        ),
        ValidationFinding(
            rule_id="V-014",
            rule_version="1.0.0",
            category="Detection",
            finding_type="count",
            finding_value=3,
            evidence_fields=("detected_level_skips",),
        ),
    ),
    engine_version="1.0.0",
    contract_version="1.0.0",
    execution_timestamp="2026-07-15T13:00:00Z",
)
```

---

## 4. Structural Invariants

### SI-FR-01: Findings Field Immutability

**Invariant:** All finding fields are immutable at the dataclass level after construction (field reassignment blocked by `frozen=True`). Mutable objects stored within `finding_value` (dicts, lists) are the engine's deterministic output; consumers that mutate them violate this contract.

**Guarantee:** Consumers cannot reassign finding fields. The finding structure (which fields exist, which findings exist) is immutable. Consumers must not mutate values reachable through finding fields.

**Rationale:** Preserves determinism and consumer trust. Deep immutability of nested containers would require copying engine outputs, adding overhead without benefit given that consumers read findings once.

---

### SI-FR-02: Metadata Completeness

**Invariant:** Every finding must include `rule_id`, `rule_version`, `category`, `finding_type`, `finding_value`, and `evidence_fields`.

**Guarantee:** No finding is produced without complete provenance.

**Rationale:** Consumers need to know which rule produced which finding and what evidence was used.

---

### SI-FR-03: No Null Findings

**Invariant:** `ValidationFindings.findings` is always a tuple (possibly empty), never None.

**Guarantee:** Consumers always receive a valid iterable.

**Rationale:** Eliminates None-checking burden from consumers.

---

### SI-FR-04: Frozen Data Structures

**Invariant:** `ValidationFinding` and `ValidationFindings` are frozen dataclasses (field-level immutability). Field reassignment is blocked. Values stored within fields retain their native Python mutability; consumer mutation of nested containers constitutes a contract violation.

**Guarantee:** Hashable, field-assignment-immutable, thread-safe for structural access.

**Rationale:** Supports caching, comparison, and concurrent access. Full deep immutability is not required for the engine's contract guarantees.

---

### SI-FR-05: Ordered Findings

**Invariant:** Findings are returned in rule_id order (alphanumeric sort).

**Guarantee:** Deterministic ordering across invocations.

**Rationale:** Consumers can rely on stable ordering.

---

### SI-FR-06: Engine Metadata

**Invariant:** `ValidationFindings` includes `engine_version` and `contract_version`.

**Guarantee:** Consumers know exact engine and contract versions that produced findings.

**Rationale:** Audit trail, version compatibility checks.

---

### SI-FR-07: Timestamp for Audit Only

**Invariant:** `execution_timestamp` is informational only — never used in engine logic.

**Guarantee:** Timestamp does not affect determinism.

**Rationale:** Audit trail without compromising determinism.

---

### SI-FR-08: No Recommendations

**Invariant:** No finding may contain recommendation text, severity labels, or action suggestions.

**Guarantee:** EQ-0011 boundary preserved.

**Rationale:** Engine observes/detects. Consumers recommend/decide.

---

### SI-FR-09: No Assessments

**Invariant:** No finding may contain quality assessments (e.g., "good", "bad", "poor").

**Guarantee:** EQ-0011 boundary preserved.

**Rationale:** Engine reports facts. Humans assess.

---

### SI-FR-10: No Consumer-Specific Fields

**Invariant:** No finding may contain fields specific to CheckMate, Formatter, Builder, O&A, or Reporting.

**Guarantee:** Consumer independence.

**Rationale:** Consumers add their own context, not the engine.

---

## 5. Semantic Invariants

### SE-FR-01: Deterministic Output

**Invariant:** Same evidence + same rules → same `ValidationFindings` (all finding fields identical, order identical, finding values identical). The `execution_timestamp` field is excluded from this guarantee per SI-FR-07 (informational only, never used in engine logic).

**Guarantee:** Determinism. Repeatable. Reproducible. Engine findings are deterministic; audit metadata varies per invocation.

**Rationale:** Core engineering requirement. The timestamp serves audit purposes only and does not compromise the determinism contract.

---

### SE-FR-02: Rule ID Traceability

**Invariant:** Every `rule_id` in findings matches a valid Rule ID in the Validation Rule Registry.

**Guarantee:** No orphan findings. Every finding traces to a governed rule.

**Rationale:** Provenance integrity.

---

### SE-FR-03: Evidence Field Traceability

**Invariant:** Every `evidence_field` in findings matches a field in `BOQIntelligenceResult` (Evidence Contract v1.0.0).

**Guarantee:** No invented evidence fields. Every finding traces to frozen evidence.

**Rationale:** Evidence integrity.

---

### SE-FR-04: Finding Type Consistency

**Invariant:** Same `rule_id` always produces same `finding_type`.

**Guarantee:** V-007 always produces "ratio". V-014 always produces "count".

**Rationale:** Consumer type safety.

---

### SE-FR-05: Deprecated Rule Exclusion

**Invariant:** Findings never contain results from rules with status = DEPRECATED or RETIRED.

**Guarantee:** Lifecycle enforcement.

**Rationale:** Only active rules execute.

---

### SE-FR-06: Provenance Completeness

**Invariant:** `rule_version` matches the rule's version at execution time, not a static string.

**Guarantee:** Consumers know which version of a rule produced a finding.

**Rationale:** Rule evolution traceability.

---

### SE-FR-07: Engine Version Stability

**Invariant:** `engine_version` changes only when engine contract changes (MAJOR.MINOR).

**Guarantee:** Consumers can trust engine version as API contract version.

**Rationale:** Consumer compatibility.

---

## 6. Finding Types

| Finding Type | Description | Example Rules |
|---|---|---|
| `presence` | Boolean or presence check result | V-001 (Required Field Presence), V-002 (Expected Key Presence) |
| `count` | Integer count | V-003 (Non-negative Values), V-014 (Level Skip Count) |
| `ratio` | Float ratio (0.0 to 1.0) | V-007 (Code Completeness), V-008 (Description Completeness) |
| `difference` | Numeric difference | V-004 (Total Rows Consistency), V-005 (Section Sum Consistency) |
| `list` | List of detected items | V-010 (Hierarchy Anomalies), V-013 (Detected Level Skips) |
| `value` | Single deterministic value | V-012 (Hierarchy Depth), V-018 (Total Known Anomalies) |

---

## 7. Consumer Guarantees

### What Consumers Can Rely On

- Findings are deterministic (same input → same output)
- Findings are immutable (no mutation possible)
- Findings have complete provenance (rule_id, version, category, evidence_fields)
- Findings are ordered (stable alphanumeric sort)
- Findings never contain recommendations
- Findings never contain assessments
- Findings never contain consumer-specific fields
- Findings trace to governed rules (Rule Registry)
- Findings trace to frozen evidence (Evidence Contract v1.0.0)

### What Consumers Must Handle

- Empty findings (`findings` tuple length = 0) when no rules match
- `finding_value` of `None` for optional evidence fields (e.g., hierarchy not available)
- Future rule additions (new rule_ids appear in findings)
- Future finding_type additions (new types appear)
- Rule version changes (rule_version field changes)

### What Consumers Must Not Expect

- Severity labels (e.g., "error", "warning", "pass")
- Recommendations (e.g., "fix description column")
- Quality assessments (e.g., "BOQ is complete")
- Consumer-specific metadata (e.g., "checkmate_severity")
- Filtered/paginated results
- Sorted-by-severity results
- Real-time streaming results
- Cached/historical results

---

## 8. Contract Evolution

### When This Contract Changes

This contract changes when:

1. A new finding field is required by a new governed rule
2. A finding field is removed because a rule is retired
3. Finding type semantics change
4. Structural invariants change
5. Semantic invariants change

### Change Process

1. Engineering Question raised
2. Spike investigates impact
3. Contract updated with new version
4. Architecture Consistency Gate runs
5. Project Owner approves
6. Contract frozen
7. Consumers migrate

### What Must Not Change

- Immutability guarantee
- Determinism guarantee
- Provenance completeness guarantee
- EQ-0011 boundary
- Consumer independence
- Evidence Contract dependency

---

## 9. Integration Surface

```
Validation Rule Registry (Governed Rules)
        ↓
Evidence Contract v1.0.0 (BOQIntelligenceResult)
        ↓
Validation Engine (validate function)
        ↓
Validation Findings Contract v1.0.0 (this contract)
        ↓
Consumers (CheckMate, Formatter, Builder, O&A, Reporting)
```

This contract is the sole integration surface between the Validation Engine and all consumers.

No consumer may access engine internals.

No consumer may bypass this contract.

---

## 10. Compliance Verification

All consumer compliance must be verified against this contract.

Verification checks:

- Consumers consume `ValidationFindings`, not raw engine output
- Consumers do not mutate findings
- Consumers respect finding_type semantics
- Consumers do not rely on finding ordering beyond alphanumeric
- Consumers handle empty findings
- Consumers handle None finding_value
- Consumers do not expect recommendations/assessments
- Consumers maintain their own interpretation layer

---

## 11. Relationship to Other Contracts

| Contract | Relationship |
|---|---|
| Evidence Contract v1.0.0 | Upstream — engine consumes it |
| Validation Rule Registry | Upstream — engine loads rules from it |
| This Contract | Output — consumers consume it |
| CheckMate Output Contract | Downstream — CheckMate adds interpretation |
| Formatter Output Contract | Downstream — Formatter adds formatting |

---

## 12. Contract Status

**Version:** v1.0.0  
**Status:** Candidate — Awaiting Spike 4 freeze approval  
**Authority:** EQ-0013 Spike 4  
**Next Review:** Upon Spike 4 completion  

---

**End of Validation Findings Contract**