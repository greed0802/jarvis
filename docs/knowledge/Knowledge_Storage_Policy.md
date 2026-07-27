# Jarvis Knowledge Storage Policy
**Policy ID:** KE-STORAGE-001
**Version:** 1.0
**Status:** DRAFT - AWAITING APPROVAL
**Effective Date:** 2026-07-27
**Last Updated:** 2026-07-27

## 1. Introduction

### 1.1 Purpose

This policy defines the storage governance, version control boundaries, and management approach for Jarvis Knowledge Assets. It establishes clear separation between Software Assets and Knowledge Assets to ensure scalability, maintainability, and operational efficiency.

### 1.2 Scope

This policy applies to all knowledge assets within the Jarvis ecosystem, including but not limited to:

- Construction standards and specifications
- Project documentation and drawings
- Cost estimation files
- Council regulations and guidelines
- Technical reports and evidence
- Domain-specific knowledge artifacts

### 1.3 Definitions

**Software Assets:** Source code, tests, tools, and documentation that comprise the Jarvis platform itself.

**Knowledge Assets:** Domain-specific content, standards, specifications, project documents, and evidence that the Jarvis platform processes and references.

**Raw Sources:** Original, unmodified knowledge documents in their native formats.

**Registry:** Metadata, inventories, and manifests that describe knowledge assets.

**Evidence:** Processed knowledge artifacts, analysis results, and derived content.

## 2. Asset Classification

### 2.1 Knowledge Asset Categories

| Category | Description | Examples | Format Types |
|----------|-------------|----------|--------------|
| **Standards** | Industry and organizational standards | ANZSMM, NCC, Council Standards | PDF, DOCX |
| **Specifications** | Technical specifications and guidelines | Civil Works Specs, Construction Specs | PDF, DOCX |
| **Projects** | Project documentation and deliverables | Drawings, BOQs, Reports, CostX Files | PDF, XLSX, DWG, CBX, EXF |
| **Councils** | Local government regulations | Development Controls, Planning Instruments | PDF, DOCX |
| **Reports** | Analysis reports and findings | Inspection Reports, Audit Reports | PDF, DOCX, XLSX |
| **Evidence** | Processed knowledge artifacts | Inventory CSV, Metadata, Analysis Results | CSV, JSON, MD |
| **Registry** | Knowledge asset tracking | Inventories, Manifests, Catalogs | CSV, MD |

### 2.2 File Type Analysis

Based on current inventory (1,856 files, 24.16 GB):

| File Type | Count | Percentage | Size Profile |
|-----------|-------|------------|--------------|
| PDF | 840 | 45.3% | Large (100KB - 100MB) |
| XLSX | 561 | 30.2% | Medium (50KB - 50MB) |
| DOCX | 153 | 8.2% | Small-Medium (20KB - 10MB) |
| PNG/JPG | 107 | 5.8% | Small-Medium (50KB - 5MB) |
| EXF/CBX | 79 | 4.3% | Medium-Large (1MB - 50MB) |
| ESW/BAK | 67 | 3.6% | Medium (500KB - 20MB) |
| Other | 53 | 2.6% | Varied |

## 3. Storage Architecture Recommendation

### 3.1 Recommended Architecture: Hybrid Storage Model

**Decision:** **Option C - External Knowledge Storage** with Git-controlled metadata

**Rationale:**

| Criteria | Git Only | Git LFS | External Storage |
|----------|----------|---------|------------------|
| Repository Size | ❌ 24GB+ unacceptable | ⚠️ Manageable but grows | ✅ Minimal impact |
| Scalability | ❌ Poor (linear growth) | ⚠️ Limited by LFS quotas | ✅ Excellent |
| Performance | ❌ Slow operations | ⚠️ LFS overhead | ✅ Optimal |
| Cost | ✅ Free | ❌ LFS costs | ✅ Minimal |
| Backup | ✅ Git built-in | ✅ Git built-in | ⚠️ Requires separate |
| Access Control | ✅ Git built-in | ✅ Git built-in | ✅ Flexible |
| Traceability | ✅ Full history | ✅ Full history | ⚠️ Limited history |
| Maintenance | ✅ Simple | ❌ LFS complexity | ✅ Simple |
| **Overall** | ❌ Not viable | ⚠️ Limited suitability | ✅ Recommended |

### 3.2 Proposed Architecture

```
Jarvis Repository (Git)
├── src/                    # Software Assets ✅ Git
├── tests/                  # Software Assets ✅ Git
├── tools/                  # Software Assets ✅ Git
├── docs/                   # Documentation ✅ Git
│   └── knowledge/          # Knowledge Governance ✅ Git
│       ├── Knowledge_Storage_Policy.md
│       ├── knowledge_migration_plan.md
│       └── ...other governance docs
└── knowledge/              # Knowledge Framework ✅ Git
    ├── registry/           # Metadata & Inventories ✅ Git
    │   └── knowledge_inventory.csv
    ├── evidence/           # Processed Evidence ✅ Git
    ├── glossary/           # Controlled Vocabulary ✅ Git
    ├── ontology/           # Domain Models ✅ Git
    └── governance/         # Knowledge Policies ✅ Git

Jarvis Knowledge Repository (External Storage)
└── sources/                # Raw Knowledge Assets ❌ Git
    ├── anzsmm/             # Standards
    ├── standards/          # Industry Standards
    ├── specifications/     # Technical Specifications
    ├── councils/           # Council Regulations
    ├── projects/           # Project Documents
    └── reports/            # Analysis Reports
```

## 4. Storage Location Policy

### 4.1 Git-Controlled Assets

**Must remain in Git:**

| Asset Type | Location | Rationale |
|------------|----------|-----------|
| Knowledge Governance | `docs/knowledge/` | Versioned policy documents |
| Registry Metadata | `knowledge/registry/` | Critical inventory tracking |
| Evidence Artifacts | `knowledge/evidence/` | Processed knowledge results |
| Ontology Definitions | `knowledge/ontology/` | Domain model versioning |
| Glossary | `knowledge/glossary/` | Controlled vocabulary |

**File Types Allowed in Git:**
- `.md` (Markdown documentation)
- `.csv` (Inventory and registry data)
- `.json` (Structured metadata)
- `.yaml`/`.yml` (Configuration)
- `.txt` (Plain text records)

### 4.2 External Storage Assets

**Must NOT be in Git:**

| Asset Type | Location | Rationale |
|------------|----------|-----------|
| Raw PDF Documents | External `sources/` | Large binary files |
| Excel Workbooks | External `sources/` | Binary, frequently updated |
| CostX Files | External `sources/` | Proprietary binary format |
| AutoCAD Files | External `sources/` | Large binary drawings |
| Image Files | External `sources/` | Large binary media |
| Database Files | External `sources/` | Binary, volatile |

**File Types Forbidden in Git:**
- `.pdf` (Portable Document Format)
- `.xlsx` (Excel Workbooks)
- `.docx` (Word Documents)
- `.cbx` (CostX Files)
- `.exf` (CostX Export Files)
- `.esw` (CostX Workbooks)
- `.dwg` (AutoCAD Drawings)
- `.png`, `.jpg`, `.jpeg` (Images)
- `.bak` (Backup Files)
- `.db` (Database Files)
- `.e0x`, `.mjo`, `.12da` (Proprietary formats)

## 5. Versioning Strategy

### 5.1 Git Versioning

**Applies to:** All Git-controlled assets

- Full Git history maintained
- Branching and tagging supported
- Pull requests for governance changes
- Semantic versioning for policy documents

### 5.2 Knowledge Asset Versioning

**Applies to:** External knowledge sources

- **Immutable Snapshots:** Each migration creates a versioned snapshot
- **Timestamp-Based:** `YYYYMMDD-HHMMSS` format
- **Checksum Verification:** SHA256 hashes for integrity
- **Manifest Tracking:** CSV inventories with version metadata

**Example Version Structure:**
```
knowledge_repository/
├── v20260727-194800/      # Initial migration
│   ├── sources/
│   ├── inventory.csv
│   └── checksums.sha256
├── v20260801-093000/      # Quarterly update
│   ├── sources/
│   ├── inventory.csv
│   └── checksums.sha256
└── current/              # Symlink to latest
    ├── sources/ -> ../v20260801-093000/sources/
    ├── inventory.csv -> ../v20260801-093000/inventory.csv
    └── checksums.sha256 -> ../v20260801-093000/checksums.sha256
```

## 6. Backup and Recovery

### 6.1 Backup Responsibility Matrix

| Asset Type | Primary Storage | Backup Location | Frequency | Responsible Party |
|------------|-----------------|-----------------|-----------|-------------------|
| Git Repository | GitHub/GitLab | Git provider | Continuous | DevOps Team |
| Knowledge Repository | External Storage | Cloud Backup | Daily | Knowledge Team |
| Registry Metadata | Git + External | Both locations | Continuous | Both Teams |
| Critical Evidence | Git + External | Both locations | Continuous | Both Teams |

### 6.2 Recovery Procedures

**Git Repository Recovery:**
1. Clone from remote origin
2. Checkout specific tag/commit if needed
3. Verify integrity with `git fsck`

**Knowledge Repository Recovery:**
1. Restore from cloud backup
2. Verify checksums against manifest
3. Update registry metadata
4. Generate recovery report

## 7. Access Control

### 7.1 Git Repository Access

| Role | Read | Write | Admin |
|------|------|-------|-------|
| Project Owner | ✅ | ✅ | ✅ |
| Developers | ✅ | ✅ | ❌ |
| Knowledge Engineers | ✅ | ✅ | ❌ |
| Contributors | ✅ | ❌ | ❌ |
| Viewers | ✅ | ❌ | ❌ |

### 7.2 Knowledge Repository Access

| Role | Read | Write | Admin |
|------|------|-------|-------|
| Project Owner | ✅ | ✅ | ✅ |
| Knowledge Engineers | ✅ | ✅ | ❌ |
| Developers | ✅ | ❌ | ❌ |
| Contributors | ⚠️ | ❌ | ❌ |
| External | ❌ | ❌ | ❌ |

## 8. Migration Rules

### 8.1 Migration Preconditions

Before any knowledge migration:

1. **Storage Policy Approval:** This document must be approved
2. **Destination Confirmation:** External storage location confirmed
3. **Backup Verification:** Source backup confirmed
4. **Checksum Baseline:** Pre-migration checksums captured
5. **Rollback Plan:** Approved rollback procedure in place
6. **Downtime Window:** Maintenance window scheduled

### 8.2 Migration Execution Rules

1. **Copy-Only Operations:** Never move or delete originals
2. **Checksum Verification:** Validate all file integrity post-migration
3. **Manifest Update:** Registry must reflect new locations
4. **Dry Run Required:** Test migration with sample dataset
5. **Progress Tracking:** Real-time logging and monitoring
6. **Error Handling:** Immediate halt on critical errors

### 8.3 Post-Migration Requirements

1. **Verification Report:** Document all validation results
2. **Checksum Archive:** Store pre/post migration hashes
3. **Registry Update:** Commit updated inventory to Git
4. **Access Validation:** Confirm all roles can access assets
5. **Performance Testing:** Validate system functionality
6. **Documentation Update:** Revise all affected documentation

## 9. .gitignore Policy

### 9.1 Recommended .gitignore Additions

```gitignore
# Knowledge Raw Sources - External Storage Only
knowledge/sources/
knowledge_inbox/

# Binary Knowledge Files
*.pdf
*.xlsx
*.docx
*.cbx
*.exf
*.esw
*.dwg
*.png
*.jpg
*.jpeg
*.bak
*.db
*.e0x
*.mjo
*.12da
*.shx
*.dxf

# Knowledge Processing Artifacts
*.tmp
*.temp
*.lock
*.swp

# CostX Specific
*.esx
*.e0x
*.mjo

# AutoCAD Specific
*.dwg
*.dxf
*.bak
*.shx
```

### 9.2 Current .gitignore Analysis

**Current state:** No knowledge-specific ignore rules
**Recommendation:** Add comprehensive knowledge file exclusions
**Impact:** Reduces repository size by ~24GB immediately

## 10. Implementation Roadmap

### 10.1 Immediate Actions (Pre-Migration)

1. ✅ **Policy Approval:** Obtain sign-off on this document
2. ✅ **External Storage Setup:** Configure knowledge repository
3. ✅ **Backup Verification:** Confirm knowledge_inbox backup
4. ✅ **.gitignore Update:** Apply recommended ignore rules
5. ✅ **Migration Script Review:** Approve migration tooling

### 10.2 Migration Phase

1. **Dry Run:** Test with 10% sample dataset
2. **Full Migration:** Execute approved migration plan
3. **Verification:** Comprehensive validation
4. **Rollback Ready:** Prepare cleanup script

### 10.3 Post-Migration

1. **Monitoring:** 72-hour stability period
2. **Documentation:** Update all affected docs
3. **Training:** Team education on new structure
4. **Decommission:** Mark old locations as deprecated

## 11. Compliance and Enforcement

### 11.1 Policy Compliance

**All contributors must:**
- ✅ Follow storage location rules
- ✅ Use approved file types in Git
- ✅ Maintain registry accuracy
- ✅ Respect access control boundaries
- ✅ Participate in backup validation

**Prohibited Actions:**
- ❌ Committing binary knowledge files to Git
- ❌ Modifying knowledge assets without registry update
- ❌ Bypassing versioning procedures
- ❌ Storing sensitive data in unapproved locations

### 11.2 Enforcement Mechanisms

1. **Git Hooks:** Pre-commit checks for forbidden file types
2. **CI/CD Validation:** Build pipeline rejects prohibited files
3. **Automated Scanning:** Regular repository audits
4. **Access Logging:** Monitor knowledge repository access
5. **Policy Reviews:** Quarterly compliance assessments

## 12. Future Considerations

### 12.1 Scalability Planning

- **1 Year:** ~50GB knowledge growth expected
- **3 Years:** ~200GB knowledge growth expected
- **5 Years:** ~500GB+ knowledge growth expected

### 12.2 Technology Evolution

- **Knowledge Graph:** Future integration planned
- **Semantic Search:** Requires metadata enrichment
- **AI Processing:** Will need access to raw sources
- **API Layer:** Potential future interface

### 12.3 Policy Review Schedule

- **Initial Review:** 3 months post-implementation
- **Regular Reviews:** Quarterly
- **Major Revisions:** As needed for architecture changes

## 13. Appendices

### 13.1 File Type Reference

**Git-Allowed Types:**
- `.md`, `.csv`, `.json`, `.yaml`, `.yml`, `.txt`

**External-Only Types:**
- `.pdf`, `.xlsx`, `.docx`, `.cbx`, `.exf`, `.esw`, `.dwg`, `.png`, `.jpg`, `.jpeg`, `.bak`, `.db`, `.e0x`, `.mjo`, `.12da`, `.shx`, `.dxf`, `.esx`

### 13.2 Migration Checklist

- [ ] Storage policy approved
- [ ] External storage configured
- [ ] Backup verified
- [ ] .gitignore updated
- [ ] Migration script tested
- [ ] Rollback plan approved
- [ ] Team notified
- [ ] Monitoring in place

### 13.3 Glossary

**Knowledge Corpus:** Complete body of domain-specific knowledge assets
**Raw Source:** Original, unmodified knowledge document
**Registry:** Comprehensive inventory of knowledge assets
**Evidence:** Processed knowledge artifacts and analysis results
**Governance:** Policies and procedures for knowledge management

## 14. Approval and Change History

### 14.1 Approval Workflow

1. **Draft:** Initial policy creation (Current status)
2. **Review:** Team feedback and revisions
3. **Approval:** Project Owner sign-off
4. **Implementation:** Policy enforcement begins
5. **Monitoring:** Continuous compliance verification

### 14.2 Change History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-07-27 | Knowledge Engineering | Initial draft for KE-0001-R.2 |

## 15. References

- **KE-0001-R:** Knowledge Corpus Foundation Recovery
- **Git Documentation:** https://git-scm.com/doc
- **Git LFS:** https://git-lfs.com/
- **Data Governance Best Practices:** ISO 38505

---

**Policy Status:** 📝 DRAFT - AWAITING APPROVAL
**Do Not Implement Without Explicit Approval**
**Next Review:** 2026-08-27