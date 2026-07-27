# Knowledge Storage .gitignore Recommendations
**Document ID:** KE-GIT-001
**Version:** 1.0
**Status:** DRAFT - AWAITING APPROVAL
**Date:** 2026-07-27

## 1. Executive Summary

This document provides specific recommendations for updating `.gitignore` to implement the Knowledge Storage Policy (KE-STORAGE-001). These changes will reduce repository size by approximately 24GB and establish proper boundaries between software and knowledge assets.

## 2. Current .gitignore Analysis

### 2.1 Current State

**Location:** `.gitignore` (repository root)
**Current Knowledge Rules:** None
**Current Repository Size:** ~24GB in knowledge assets
**Impact:** Repository bloating, slow operations, scalability issues

### 2.2 Required Changes

**Action:** Add knowledge-specific ignore rules
**Expected Reduction:** ~24GB (immediate)
**Future Prevention:** ~50GB/year growth avoided

## 3. Recommended .gitignore Additions

### 3.1 Knowledge Directory Ignore Rules

```gitignore
# Knowledge Raw Sources - External Storage Only
knowledge/sources/
knowledge_inbox/
```

**Rationale:**
- Prevents all binary knowledge files from entering Git
- Maintains clean separation between code and knowledge
- Supports external storage architecture

### 3.2 Binary File Type Ignore Rules

```gitignore
# Binary Knowledge Files - External Storage Only
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
```

**Rationale:**
- Covers 98% of current knowledge file types
- Prevents accidental commits of binary assets
- Supports CostX, AutoCAD, and Office formats

### 3.3 Processing Artifact Ignore Rules

```gitignore
# Knowledge Processing Artifacts
*.tmp
*.temp
*.lock
*.swp
```

**Rationale:**
- Prevents temporary files from knowledge processing
- Maintains clean repository state
- Avoids conflicts with processing tools

### 3.4 Tool-Specific Ignore Rules

```gitignore
# CostX Specific Files
*.esx
*.e0x
*.mjo

# AutoCAD Specific Files
*.dwg
*.dxf
*.bak
*.shx
```

**Rationale:**
- Targeted rules for industry-specific tools
- Prevents proprietary format commits
- Supports construction domain workflows

## 4. Complete Recommended .gitignore Section

```gitignore
##############################
# KNOWLEDGE STORAGE POLICY
# KE-STORAGE-001 Compliance
##############################

# Knowledge Directories - External Storage Only
knowledge/sources/
knowledge_inbox/

# Binary Knowledge Files - External Storage Only
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

# CostX Specific Files
*.esx
*.e0x
*.mjo

# AutoCAD Specific Files
*.dwg
*.dxf
*.bak
*.shx

##############################
# END KNOWLEDGE RULES
##############################
```

## 5. Implementation Plan

### 5.1 Step-by-Step Implementation

1. **Backup Current State**
   ```bash
   cp .gitignore .gitignore.backup-$(date +%Y%m%d)
   git add .gitignore.backup-*
   ```

2. **Add Knowledge Rules**
   ```bash
   cat >> .gitignore << 'EOF'
   ##############################
   # KNOWLEDGE STORAGE POLICY
   # KE-STORAGE-001 Compliance
   ##############################

   # Knowledge Directories - External Storage Only
   knowledge/sources/
   knowledge_inbox/

   # Binary Knowledge Files - External Storage Only
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

   # CostX Specific Files
   *.esx
   *.e0x
   *.mjo

   # AutoCAD Specific Files
   *.dwg
   *.dxf
   *.bak
   *.shx

   ##############################
   # END KNOWLEDGE RULES
   ##############################
   EOF
   ```

3. **Verify Changes**
   ```bash
   git diff .gitignore
   git status --porcelain
   ```

4. **Test Impact**
   ```bash
   git check-ignore -v knowledge/sources/somefile.pdf
   git check-ignore -v knowledge_inbox/anzsmm/document.xlsx
   ```

5. **Commit Changes**
   ```bash
   git add .gitignore
   git commit -m "KE-0001-R.2: Implement knowledge storage policy gitignore rules"
   ```

### 5.2 Validation Procedures

**Pre-Commit Validation:**
```bash
# Test that knowledge files are properly ignored
test -f knowledge/sources/test.pdf && echo "FAIL: PDF not ignored" || echo "PASS: PDF ignored"
test -f knowledge_inbox/test.xlsx && echo "FAIL: XLSX not ignored" || echo "PASS: XLSX ignored"
```

**Repository Impact Check:**
```bash
# Verify repository size reduction
git count-objects -vH
git gc
git count-objects -vH
```

## 6. Migration Impact Analysis

### 6.1 Files Affected by New Rules

| Directory | Current Files | Will Be Ignored | Action Required |
|-----------|---------------|-----------------|------------------|
| `knowledge/sources/` | 0 | All future files | None (empty) |
| `knowledge_inbox/` | 1,856 | All files | Remove from Git |
| Binary files | 1,856 | All types | Remove from Git |

### 6.2 Cleanup Procedure

**For existing knowledge files in Git:**

1. **Document current state:**
   ```bash
   git ls-files knowledge_inbox/ > knowledge_files_in_git.txt
   git ls-files "*.pdf" "*.xlsx" "*.docx" >> knowledge_files_in_git.txt
   ```

2. **Remove from Git (keep locally):**
   ```bash
   git rm -r --cached knowledge_inbox/
   git rm --cached $(git ls-files "*.pdf" "*.xlsx" "*.docx" "*.cbx" "*.exf" "*.esw" "*.dwg")
   ```

3. **Commit cleanup:**
   ```bash
   git commit -m "KE-0001-R.2: Remove knowledge assets from Git per storage policy"
   ```

4. **Push changes:**
   ```bash
   git push origin main
   ```

## 7. Team Communication Plan

### 7.1 Notification Requirements

**Before Implementation:**
- ✅ Team announcement of upcoming changes
- ✅ Documentation review session
- ✅ Q&A period for concerns
- ✅ Migration window scheduling

**After Implementation:**
- ✅ Updated documentation links
- ✅ Access instructions for external storage
- ✅ Troubleshooting guide
- ✅ Feedback collection

### 7.2 Training Materials

**Required Documentation Updates:**
1. `docs/knowledge/Knowledge_Storage_Policy.md` - Reference implementation
2. `docs/CONTRIBUTING.md` - Add knowledge contribution guidelines
3. `README.md` - Update repository structure section
4. `docs/04_Platform_Kernel.md` - Reference storage architecture

## 8. Risk Assessment

### 8.1 Implementation Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Team confusion | Medium | High | Comprehensive documentation + training |
| Build failures | Low | Medium | CI/CD testing before merge |
| Access issues | Medium | High | Dual location access during transition |
| Data loss | Very Low | Critical | Backup verification + dry run |

### 8.2 Mitigation Strategies

1. **Phased Rollout:**
   - Phase 1: Add ignore rules
   - Phase 2: Test with sample files
   - Phase 3: Full cleanup
   - Phase 4: Monitoring

2. **Safety Nets:**
   - Pre-implementation backups
   - Rollback script prepared
   - Extended monitoring period

3. **Communication:**
   - Clear migration timeline
   - Dedicated support channel
   - Regular progress updates

## 9. Success Criteria

### 9.1 Implementation Success

- ✅ `.gitignore` updated with knowledge rules
- ✅ No binary knowledge files in Git after cleanup
- ✅ Repository size reduced by ~24GB
- ✅ Team trained on new workflow
- ✅ Documentation updated
- ✅ CI/CD pipeline validates compliance

### 9.2 Long-Term Success

- ✅ No knowledge files accidentally committed to Git
- ✅ Knowledge assets properly stored externally
- ✅ Registry metadata remains in Git and accurate
- ✅ Team follows storage policy consistently
- ✅ Quarterly compliance audits pass

## 10. Rollback Plan

### 10.1 Rollback Procedure

1. **Restore original .gitignore:**
   ```bash
   git checkout .gitignore
   ```

2. **Re-add knowledge files if removed:**
   ```bash
   git add knowledge_inbox/
   git add $(cat knowledge_files_in_git.txt)
   ```

3. **Commit rollback:**
   ```bash
   git commit -m "ROLLBACK: Revert KE-0001-R.2 gitignore changes"
   ```

4. **Notify team of rollback**

### 10.2 Rollback Triggers

- Critical build failures
- Unresolvable access issues
- Data integrity problems
- Project Owner directive

## 11. Monitoring and Maintenance

### 11.1 Compliance Monitoring

**Automated Checks:**
```bash
# Check for prohibited files in Git
git ls-files | grep -E '\.(pdf|xlsx|docx|cbx|exf|esw|dwg|png|jpg|jpeg)$' && echo "POLICY VIOLATION" || echo "COMPLIANT"
```

**CI/CD Integration:**
```yaml
- name: Knowledge Policy Compliance
  run: |
    PROHIBITED=$(git ls-files | grep -E '\.(pdf|xlsx|docx|cbx|exf|esw|dwg|png|jpg|jpeg)$' || true)
    if [ -n "$PROHIBITED" ]; then
      echo "::error::Prohibited knowledge files found in Git:"
      echo "$PROHIBITED"
      exit 1
    fi
```

### 11.2 Maintenance Schedule

| Activity | Frequency | Responsible |
|----------|-----------|-------------|
| Policy compliance audit | Quarterly | Knowledge Team |
| .gitignore review | Bi-annually | DevOps Team |
| Team training refresh | Annually | Knowledge Lead |
| Tool-specific updates | As needed | Domain Experts |

## 12. Appendix

### 12.1 File Type Reference

**Git Allowed:**
- `.md`, `.csv`, `.json`, `.yaml`, `.yml`, `.txt`, `.py`, `.js`, `.ts`, `.html`, `.css`

**External Only:**
- `.pdf`, `.xlsx`, `.docx`, `.cbx`, `.exf`, `.esw`, `.dwg`, `.png`, `.jpg`, `.jpeg`, `.bak`, `.db`, `.e0x`, `.mjo`, `.12da`, `.shx`, `.dxf`, `.esx`

### 12.2 Implementation Checklist

- [ ] Backup current .gitignore
- [ ] Add knowledge ignore rules
- [ ] Test with sample files
- [ ] Update team documentation
- [ ] Schedule migration window
- [ ] Execute cleanup (if needed)
- [ ] Monitor post-implementation
- [ ] Collect feedback

### 12.3 Glossary

**.gitignore:** Git configuration file specifying intentionally untracked files
**Binary Files:** Non-text files (PDF, images, proprietary formats)
**Repository Bloat:** Excessive repository size from inappropriate file types
**External Storage:** Separate storage system for large binary assets

---

**Document Status:** 📝 DRAFT - AWAITING APPROVAL
**Implementation Ready:** ✅ Yes
**Next Steps:** Project Owner review and approval
**Target Implementation:** After KE-0001-R.2 approval