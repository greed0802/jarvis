# Repository Governance Automation

**Authority:** EQ-0017 Repository Governance Migration
**Status:** Active
**Version:** 1.0
**Date:** 2026-07-23

---

## Purpose

This document specifies the automated governance validation framework that prevents repository governance regressions. The framework ensures that repository compliance is automatically verifiable and that future pull requests fail if governance rules are violated.

---

## Architecture Overview

### Quality Gate Integration

Repository governance validation is implemented as **Quality Gate 2 (Architecture Verification)** within the existing repository quality verification process. The governance validators integrate with the `verify_all.py` orchestrator and run automatically in CI pipelines.

### Validator Components

| Validator | Authority | Scope |
|-----------|-----------|-------|
| `verify_governance` | Quality Gate 2 | Comprehensive governance structure validation |
| `verify_links` | Quality Gate 1 | Markdown link integrity verification |
| `verify_evidence` | Quality Gate 2 | Engineering Question evidence validation |
| `verify_tools` | Quality Gate 3 | Tool classification and placement validation |
| `verify_register` | Quality Gate 3 | Engineering Register validation |

### Validation Lifecycle

```
Pull Request → CI Pipeline → verify_all.py → Governance Validators → PASS/FAIL
                          ↓
                    Report Generation → data/reports/
                          ↓
                    Block Merge on FAIL
```

---

## Validation Rules

### Engineering Register Validation (`verify_register`)

**Rules:**
1. **Unique EQ Numbers**: No duplicate EQ registrations
2. **Authority Document Existence**: Every registered EQ must have a corresponding authority document
3. **Evidence Package Existence**: Every registered EQ must have a corresponding evidence package
4. **Valid Repository Paths**: All paths must follow `../questions/` and `../evidence/` patterns
5. **Status Values**: Only valid statuses ("Completed", "Active", "Draft", "Frozen")
6. **Register Completeness**: No empty fields in EQ entries
7. **Proper Naming**: Authority documents must be named `EQ_XXXX.md`, evidence packages `EQ_XXXX/`

**Failure Conditions:**
- Missing authority documents
- Missing evidence packages
- Invalid path formats
- Duplicate EQ numbers
- Invalid status values
- Empty required fields

### Link Validation (`verify_links`)

**Rules:**
1. **Internal Link Integrity**: All markdown links to internal files must resolve
2. **Relative Path Validation**: All relative paths (`../`, `./`) must be resolvable
3. **Engineering Register Links**: All EQ authority document and evidence package links must be functional
4. **Evidence Package README Links**: All authority document references must resolve
5. **Cross-Document References**: All references between governance documents must be valid

**Failure Conditions:**
- Broken internal links
- Invalid relative paths
- Unresolvable authority document links
- Broken cross-references
- Missing linked files

### Evidence Validation (`verify_evidence`)

**Rules:**
1. **Authority Document Presence**: Every EQ must have an authority document in `docs/engineering/questions/`
2. **Evidence Package Presence**: Every EQ must have an evidence package in `docs/engineering/evidence/`
3. **Evidence Completeness**: Evidence packages must contain README.md and relevant reports
4. **No Orphaned Evidence**: All evidence packages must correspond to registered EQs
5. **No Duplicate Evidence**: No duplicate files across evidence packages
6. **Proper Structure**: Evidence packages must follow naming convention `EQ_XXXX/`
7. **README Validation**: Evidence package READMEs must reference correct authority documents

**Failure Conditions:**
- Missing authority documents
- Missing evidence packages
- Orphaned evidence packages
- Duplicate evidence files
- Invalid evidence package structure
- Broken authority document references

### Tool Validation (`verify_tools`)

**Rules:**
1. **Tool Classification**: All tools must be classified as reusable or historical
2. **Registry Completeness**: All quality tools must be registered in Tool Registry
3. **Manifest Accuracy**: All tools in manifest.json must exist
4. **Historical Preservation**: Historical EQ-specific tools must remain in `tools/` root
5. **Architectural Justification**: All tools must have documented purpose and authority
6. **Contract Compliance**: Quality tools must implement required arguments (`--help`, `--json`, `--strict`, `--output`)

**Failure Conditions:**
- Unclassified tools in tools root
- Unregistered quality tools
- Missing tools referenced in manifest
- Historical tools not preserved
- Missing tool documentation
- Contract non-compliance

### Governance Validation (`verify_governance`)

**Rules:**
1. **Repository Organization**: Required directories must exist (`docs/`, `src/`, `tests/`, `tools/`)
2. **Documentation Hierarchy**: Main documentation files must be present
3. **Tool Placement**: Quality tools must be in `tools/quality/`, historical tools in `tools/`
4. **Freeze Checklist**: Engineering Question Freeze Checklist must exist and be complete
5. **No Root Pollution**: Only expected files in repository root
6. **Generated Artifacts**: Reports and archives must be properly placed

**Failure Conditions:**
- Missing required directories
- Missing main documentation
- Improper tool organization
- Missing freeze checklist
- Unexpected files in repository root
- Misplaced generated artifacts

---

## Failure Conditions and Remediation

### Critical Failures (Block Merge)

| Condition | Remediation |
|-----------|-------------|
| Missing authority documents | Create proper authority document in `docs/engineering/questions/` |
| Missing evidence packages | Create proper evidence package in `docs/engineering/evidence/` |
| Broken Engineering Register links | Fix links to use correct `../questions/` and `../evidence/` patterns |
| Duplicate EQ numbers | Remove duplicate registrations |
| Unclassified tools | Move tools to appropriate location or document classification |
| Contract non-compliance | Update tools to implement required arguments |

### Warning Conditions (Documented but Don't Block)

| Condition | Remediation |
|-----------|-------------|
| Orphaned evidence packages | Register EQ or archive evidence |
| Potential duplicate evidence | Review and consolidate if appropriate |
| Missing evidence reports | Document as known gap or add reports |
| Historical tools not documented | Update Tool Registry with historical tool references |

---

## Repository Governance Lifecycle

### Before Commit

1. **Local Validation**: Run `verify_all.py` locally before committing
2. **Fix Issues**: Address any governance validation failures
3. **Document Exceptions**: Add comments for any intentional warnings

### Pull Request Process

1. **Automated CI Validation**: Governance validators run automatically
2. **Failure Notification**: PR author notified of governance violations
3. **Remediation Required**: PR cannot merge until all critical issues resolved
4. **Review Documentation**: Warnings reviewed by Project Owner

### Post-Merge Validation

1. **Automated Report Generation**: Full governance report generated
2. **Archive Reports**: Reports stored in `data/reports/`
3. **Trend Analysis**: Governance compliance tracked over time

---

## Tool Integration

### CI Pipeline Integration

```yaml
# Example CI configuration
- name: Run Governance Validation
  run: |
    python tools/quality/verify_all.py --json --strict
    # Exit 1 on any governance failure

- name: Generate Governance Report
  run: |
    python tools/quality/verify_all.py --output data/reports/Governance_Report.md
    # Store report for documentation
```

### Local Development Usage

```bash
# Run all governance validators
python tools/quality/verify_all.py

# Run specific validator
python tools/quality/verify_governance.py --json

# Generate detailed report
python tools/quality/verify_links.py --output data/reports/Link_Report.md

# Strict mode (exit 1 on any finding)
python tools/quality/verify_evidence.py --strict
```

---

## Governance Validation Matrix

| Validator | Quality Gate | Frequency | Blocking | Scope |
|-----------|--------------|-----------|----------|-------|
| `verify_governance` | 2 | Every PR | Yes | Repository structure |
| `verify_links` | 1 | Every PR | Yes | Link integrity |
| `verify_evidence` | 2 | Every PR | Yes | Evidence packages |
| `verify_tools` | 3 | Every PR | Yes | Tool organization |
| `verify_register` | 3 | Every PR | Yes | Engineering Register |

---

## Promotion Workflow

### New Tool Promotion

1. **Develop Tool**: Implement in `tools/quality/verify_*.py`
2. **Add to Manifest**: Update `tools/manifest.json` with tool metadata
3. **Register Tool**: Add to `tools/quality/Tool_Registry.md`
4. **Document Purpose**: Add architectural justification
5. **Test Integration**: Verify tool runs via `verify_all.py`
6. **Update Documentation**: Add to this document if governance-related

### Historical Tool Preservation

1. **Identify EQ-Specific Tools**: Tools named `eqXXXX_*.py`
2. **Preserve in Root**: Keep in `tools/` directory
3. **Document in Registry**: Add to Historical Evidence Tools section
4. **Do Not Modify**: Historical tools remain unchanged as evidence

---

## Success Criteria

### Automation Success

✅ **Repository governance automatically validated**
- All governance validators integrated and functional
- CI pipeline blocks merges on governance failures
- Comprehensive reports generated automatically

✅ **Broken links automatically detected**
- All markdown links validated systematically
- Engineering Register links verified
- Cross-document references checked

✅ **Engineering packages automatically verified**
- Authority documents validated
- Evidence packages verified
- Orphaned/duplicate evidence detected

✅ **Repository structure regressions automatically reported**
- Directory structure validated
- Tool placement verified
- Documentation hierarchy checked

✅ **Future governance violations detected before merge or release**
- PR validation prevents governance drift
- Automated reporting enables proactive remediation
- Quality gates enforce compliance

✅ **Manual governance audits no longer required except for architectural review**
- Automation handles routine compliance checking
- Human review focused on architectural decisions
- Continuous validation replaces periodic audits

---

## Maintenance and Evolution

### Version Management

- **Validator Versions**: Individual tools maintain version history
- **Registry Versions**: Tool Registry versioned for compatibility
- **Documentation Versions**: This document versioned with repository

### Evolution Process

1. **Identify Gap**: Governance validation gap discovered
2. **Propose Enhancement**: Create Engineering Question if significant
3. **Implement Validator**: Add new validation rule
4. **Update Documentation**: Document new validation
5. **Deploy to CI**: Integrate into automated pipeline

### Deprecation Process

1. **Mark as Planned**: Move to "Planned Tools" section
2. **Preserve Functionality**: Keep existing validation active
3. **Document Replacement**: Specify migration path
4. **Archive**: Move to historical section when replaced

---

## Relationship to Governance

This automation framework implements the validation requirements defined in:

- `docs/engineering/Engineering_Governance.md` § Investigation Approval Gates
- `docs/engineering/Quality_Assurance_Constitution.md` Quality Gate 2
- `AGENTS.md` § Evidence Hierarchy
- `docs/engineering/Engineering_Question_Freeze_Checklist.md`

---

## References

- **Governance Model**: `docs/engineering/Engineering_Governance.md`
- **Quality Constitution**: `docs/engineering/Quality_Assurance_Constitution.md`
- **Freeze Checklist**: `docs/engineering/Engineering_Question_Freeze_Checklist.md`
- **Tool Registry**: `tools/quality/Tool_Registry.md`
- **Manifest**: `tools/manifest.json`

---

## Document Control

**Owner:** Repository Engineering
**Review Schedule:** Upon governance evolution
**Distribution:** All contributors, CI systems, AI agents

**Version History:**

| Version | Date | Changes | Authority |
|---------|------|---------|-----------|
| 1.0 | 2026-07-23 | Initial governance automation framework | EQ-0017 |

---

## Conclusion

The Repository Governance Automation framework establishes a deterministic, automated compliance system that:

1. **Prevents Governance Regression**: Continuous validation catches issues early
2. **Enables Self-Validating Repository**: Repository can verify its own compliance
3. **Reduces Manual Effort**: Automation replaces periodic audits
4. **Improves Quality**: Governance violations blocked before merge
5. **Supports Growth**: Framework scales with repository complexity

**The Jarvis repository now has automated governance enforcement that detects violations before they can cause architectural drift.**