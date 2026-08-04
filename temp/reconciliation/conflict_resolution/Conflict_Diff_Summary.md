# Conflict Diff Summary

## File: .gitignore

```diff
--- Windows: .gitignore
+++ Fedora: .gitignore
@@ -39,7 +39,4 @@
 
 #Temporary files
 
-knowledge_inbox/
-
-#Others
-.stfolder/
+knowledge_inbox/```

## File: AGENTS.md

```diff
--- Windows: AGENTS.md
+++ Fedora: AGENTS.md
@@ -1,77 +1,1388 @@
-# AGENTS.md — Jarvis Repository Constitution
-
-**Status:** Approved
-**Version:** 2.0.0
-**Authority:** Project Owner
-**Effective Date:** 2026-07-28
-
-This document defines the non-negotiable constitutional laws governing all AI coding agents (Cline, Claude Code, GitHub Copilot, ChatGPT, Gemini, Qoder) contributing to the Jarvis repository.
-
----
-
-## 1. Core Philosophy
-Jarvis is a modular Professional Intelligence Platform, NOT a chatbot, wrapper, or experimental playground.
-- **Documentation First**: Architecture and specifications MUST precede code.
-- **Evidence Driven**: Engineering claims MUST require executable verification.
-- **ADR Governed**: Core commitments are permanently frozen in Architecture Decision Records.
-- **Deterministic Engineering**: Identical inputs MUST yield identical outputs.
-
----
-
-## 2. Mandatory Reading & Operational Pointers
-Before creating files, modifying directory structure, or executing tasks, AI agents **MUST** read and obey the authoritative manual for that operational domain:
-
-1. **Artifact Classification, Folder Ownership & Placement Protocol**:
-   → **MUST READ**: `docs/governance/REPOSITORY_GOVERNANCE_MANUAL.md`
-2. **Workstream Rules & Identifier Policies** (`EQ`, `ADR`, `KE`, `CP`, `CB`):
-   → **MUST READ**: `docs/governance/WORKSTREAM_GOVERNANCE.md`
-3. **Quality Gates & Mechanical Verification**:
-   → **MUST READ**: `docs/engineering/Quality_Assurance_Constitution.md`
-4. **Agent Tactical Workflows & Operating Procedures**:
-   → **MUST READ**: `docs/engineering/AI_Agent_Operating_Manual.md`
-
----
-
-## 3. Constitutional Invariants
-
-### A. The Preservation Rule (MUST)
-Accepted ADRs, frozen Engineering Questions (e.g., `EQ-0017`, `EQ-0019`), public contracts, and release tags are permanently immutable.
-- **STRICTLY PROHIBITED**: Deleting, renumbering, rewriting, merging, or relocating frozen historical artifacts.
-
-### B. Category Boundary Ownership (MUST)
-Every file created **MUST** belong to exactly one domain:
-- `src/` — Production source code only.
-- `tests/` — Automated test suite only.
-- `docs/` — Platform, engineering, governance, and execution documentation.
-- `knowledge/` — Runtime knowledge data (NOT Markdown documentation).
-- `tools/` — Executable quality and tooling only (NO reports or documentation).
-
----
-
-## 4. Mandatory Pre-Creation Protocol (MUST)
-Before creating **ANY** file or directory, the AI agent **MUST**:
-1. Execute the **Pre-Creation Reasoning Protocol** described in `docs/governance/REPOSITORY_GOVERNANCE_MANUAL.md`.
-2. Output a formal **Governance Decision Record (GDR)** block in its response prior to disk creation.
-3. Pass the **Repository Governance Quality Gate**.
-
----
-
-## 5. Constitutional STOP Conditions (MUST)
-An AI agent **MUST IMMEDIATELY STOP** processing and request Project Owner guidance if:
-1. Artifact classification or target folder placement is ambiguous.
-2. A task appears to require creating a new top-level directory or unapproved folder.
-3. A task conflicts with an accepted ADR or permanently frozen architecture.
-4. Repository drift or competing governance structures are detected.
-
-When stopped: Write an **Architecture Conflict Report** or **Repository Drift Report** under `docs/governance/reports/` and await Project Owner instruction.
-
----
-
-## 6. Execution Environment Mandate (MUST)
-Always invoke python directly via the project's virtual environment:
-```bash
-./.venv/bin/python -m pytest
-./.venv/bin/python tools/quality/verify_documentation.py
-```
-
-For Windows environments: `.venv\Scripts\python.exe`.+# AGENTS.md
+
+# Jarvis Repository Instructions
+
+This document defines the mandatory engineering and architectural rules for all AI coding agents contributing to the Jarvis repository.
+
+Examples include:
+
+- Cline
+- Claude Code
+- GitHub Copilot
+- ChatGPT
+- Gemini CLI
+- Qoder
+- Any future coding agent
+
+These instructions apply unless explicitly overridden by the Project Owner.
+
+---
+
+# Repository Purpose
+
+Jarvis is a modular Professional Intelligence Platform.
+
+It is NOT:
+
+- a chatbot
+- an AI wrapper
+- an experimental playground
+
+Jarvis is a long-term engineering platform whose architecture is:
+
+- Documentation First
+- Evidence Driven
+- ADR Governed
+- Capability Oriented
+
+---
+
+# Repository Constitution
+
+The repository architecture is considered a frozen engineering asset.
+
+AI agents SHALL preserve repository structure exactly as defined by the architecture.
+
+Repository organization is NOT an implementation detail.
+
+Repository organization IS architecture.
+
+If an AI agent believes files belong somewhere else, the agent SHALL NOT move them automatically.
+
+Instead the agent shall:
+
+1. identify the conflict
+2. explain why the conflict exists
+3. reference the architecture
+4. propose an Engineering Question or ADR if necessary
+5. wait for Project Owner approval
+
+Repository boundaries shall never evolve implicitly.
+
+---
+
+# Repository Boundary Rules
+
+Every file created by an AI agent SHALL belong to exactly one architectural category.
+
+## Production
+
+Production implementation only.
+
+Examples:
+
+src/
+tests/
+
+Production code SHALL NEVER be written elsewhere.
+
+---
+
+## Documentation
+
+Repository documentation only.
+
+Location:
+
+docs/
+
+Documentation SHALL follow the approved documentation hierarchy.
+
+### Architecture
+
+docs/
+
+Architecture documents.
+
+Examples:
+
+Vision
+
+Principles
+
+Blueprint
+
+Kernel
+
+ADRs
+
+---
+
+### Engineering
+
+docs/engineering/
+
+Engineering Questions
+
+Spike Reports
+
+Capability Discovery
+
+Capability Evaluation
+
+Implementation Reviews
+
+Engineering Evidence
+
+Execution Reports
+
+Temporary engineering documentation
+
+---
+
+### Knowledge Documentation
+
+docs/knowledge/
+
+Knowledge governance only.
+
+Examples:
+
+Knowledge Architecture
+
+Knowledge Governance
+
+Knowledge Lifecycle
+
+Knowledge Storage Policy
+
+Knowledge Consumption
+
+Knowledge Engineering Principles
+
+These documents describe HOW knowledge is managed.
+
+They do NOT describe execution of a milestone.
+
+---
+
+### Execution Documentation
+
+docs/execution/
+
+Execution history only.
+
+Examples:
+
+Migration Reports
+
+Recovery Reports
+
+Temporary execution plans
+
+Validation summaries
+
+Implementation logs
+
+One-off engineering activities
+
+Execution documentation shall never become permanent governance.
+
+---
+
+# Knowledge Boundary
+
+knowledge/
+
+is NOT documentation.
+
+knowledge/
+
+is runtime repository data.
+
+It contains repository knowledge assets.
+
+Only the following belong here:
+
+knowledge/
+
+    registry/
+
+    governance/
+
+    ontology/
+
+    glossary/
+
+    evidence/
+
+Source documents remain immutable.
+
+---
+
+# Tool Boundary
+
+tools/
+
+contains executable tooling only.
+
+Never place:
+
+documentation
+
+reports
+
+architecture
+
+governance
+
+inside tools/.
+
+---
+
+# File Placement Rule
+
+Before creating ANY new file the AI agent SHALL perform this reasoning:
+
+1.
+
+What category is this file?
+
+2.
+
+What architectural boundary owns this category?
+
+3.
+
+Does an approved location already exist?
+
+If yes:
+
+Use the existing location.
+
+Do NOT invent another folder.
+
+---
+
+# Folder Creation Rule
+
+AI agents SHALL NOT create new top-level folders.
+
+AI agents SHALL NOT create new documentation hierarchies.
+
+AI agents SHALL reuse the approved repository structure.
+
+If a new hierarchy appears necessary:
+
+STOP.
+
+Raise an Engineering Question.
+
+---
+
+# Repository Preservation Rule
+
+Every planned operation must be classified before execution.
+
+One of:
+
+Read-Only
+
+Additive
+
+Transformative
+
+Destructive
+
+Definitions
+
+Read-Only
+
+Reads repository assets only.
+
+No modifications.
+
+Additive
+
+Creates new files only.
+
+Never changes existing assets.
+
+Transformative
+
+Modifies repository-managed artefacts only.
+
+Examples:
+
+documentation
+
+registry
+
+metadata
+
+tests
+
+configuration
+
+Destructive
+
+Deletes
+
+Moves
+
+Renames
+
+Overwrites
+
+Restructures
+
+existing assets.
+
+Destructive operations are PROHIBITED unless explicitly approved by the Project Owner in the current conversation.
+
+---
+
+# Architecture Conflict Rule
+
+If implementation conflicts with repository architecture:
+
+STOP.
+
+Do not improvise.
+
+Do not relocate files.
+
+Do not create alternative structures.
+
+Produce an Architecture Conflict Report.
+
+Wait for approval.
+
+---
+
+# Continuous Consistency Rule
+
+Before declaring any milestone complete, verify:
+
+No duplicate documentation exists.
+
+No competing folder structures exist.
+
+No duplicate governance exists.
+
+No architectural drift has occurred.
+
+If drift is detected:
+
+STOP.
+
+Produce a Repository Drift Report.
+
+Do not request milestone freeze until drift is resolved.
+
+---
+
+# Project Authority
+
+The Project Owner is the final engineering authority.
+
+AI agents:
+
+- investigate
+- recommend
+- implement
+- review
+
+AI agents never determine architecture independently.
+
+---
+
+# Source of Truth
+
+Repository decisions are governed by:
+
+1. docs/00_Vision.md
+2. docs/01_Principles.md
+3. docs/02_System_Blueprint.md
+4. docs/03_Core_Ontology_Relationships.md
+5. docs/04_Platform_Kernel.md
+6. Accepted ADRs
+
+These documents define architecture.
+
+Implementation must conform to them.
+
+Never reinterpret architecture during implementation.
+
+---
+
+# Required Repository Reading
+
+Before implementing significant changes, review the documentation relevant to the task.
+
+Examples include:
+
+Architecture
+
+- Vision
+- Principles
+- Blueprint
+- Platform Kernel
+- Accepted ADRs
+
+Engineering
+
+- Engineering Questions
+- Spike Reports
+- Capability Register
+- Capability Roadmap
+
+Operational Guidance
+
+- docs/engineering/AI_Agent_Operating_Manual.md
+- docs/engineering/Quality_Assurance_Constitution.md
+
+Do not ask the Project Owner for information that already exists in repository documentation.
+
+---
+
+# Evidence Hierarchy
+
+When information conflicts, use the following priority.
+
+1. Accepted ADRs
+2. Architecture Documents
+3. Production Code
+4. Engineering Questions
+5. Spike Evidence
+6. Approved Documentation
+7. External References
+8. General AI Knowledge
+
+Higher-priority evidence always overrides lower-priority evidence.
+
+Never replace repository evidence with generic best practices.
+
+---
+
+# Engineering Philosophy
+
+Documentation First.
+
+Evidence Before Promotion.
+
+ADR Driven.
+
+Deterministic Engineering.
+
+Human Authority.
+
+YAGNI.
+
+Small Iterations.
+
+Clarity over Cleverness.
+
+Explicitness over Magic.
+
+Maintainability over Novelty.
+
+---
+
+# Architecture Rules
+
+## Platform Kernel
+
+The Kernel is the Control Plane.
+
+Kernel responsibilities:
+
+- lifecycle
+- configuration
+- registration
+- service management
+
+The Kernel never:
+
+- creates Context
+- creates Plans
+- executes Workflows
+- performs business logic
+- executes Skills
+
+---
+
+## Application
+
+Application is the Composition Root.
+
+Application:
+
+- creates runtime components
+- assembles the runtime
+- wires dependencies
+- registers services
+
+The Kernel never constructs runtime objects.
+
+---
+
+## Runtime Ownership
+
+Ownership is exclusive.
+
+Context Engine owns Context.
+
+Planner Engine owns Plans.
+
+Workflow Engine owns Workflows and Tasks.
+
+Skills perform work.
+
+Validation evaluates outputs.
+
+Learning promotes approved knowledge.
+
+Responsibilities must never overlap.
+
+---
+
+# Engineering Workflow
+
+Before writing production code:
+
+1. Review architecture.
+2. Review applicable ADRs.
+3. Review existing implementation.
+4. Review existing tests.
+5. Determine whether sufficient evidence exists.
+
+If evidence is insufficient:
+
+Do not guess.
+
+Instead:
+
+- propose an Engineering Question
+- propose a Spike
+- gather evidence
+- wait for approval when required
+
+Production implementation must never be assumption-driven.
+
+---
+
+# Capability Lifecycle
+
+Every capability follows:
+
+Capability Discovery
+
+↓
+
+Capability Evaluation
+
+↓
+
+Project Owner Decision
+
+↓
+
+Engineering Question
+
+↓
+
+Spike
+
+↓
+
+Implementation
+
+↓
+
+Validation
+
+↓
+
+Promotion
+
+↓
+
+Release
+
+Do not bypass lifecycle stages without explicit approval.
+
+---
+
+# Implementation Rules
+
+Implement the smallest production-ready solution.
+
+Prefer incremental improvement.
+
+Avoid speculative features.
+
+Avoid unnecessary abstraction.
+
+Prefer explicit typing.
+
+Keep modules focused.
+
+Preserve existing behavior unless requested.
+
+Do not rewrite working modules solely for style.
+
+Avoid architecture expansion unless approved.
+
+---
+
+# Deterministic Engineering
+
+Production code should be:
+
+- deterministic
+- repeatable
+- observable
+- testable
+- maintainable
+
+Identical inputs should produce identical outputs whenever practical.
+
+---
+
+# Multi-Agent Collaboration
+
+Multiple AI agents may contribute.
+
+Agents shall:
+
+- preserve accepted engineering decisions
+- respect frozen investigations
+- respect accepted ADRs
+- avoid unnecessary rewrites
+- clearly identify disagreements
+- justify architectural recommendations with evidence
+
+Never overwrite previous engineering work without justification.
+
+---
+
+# Documentation Responsibilities
+
+If implementation changes architecture:
+
+STOP.
+
+Explain the conflict.
+
+Propose an ADR.
+
+Wait for approval.
+
+Do not silently modify architectural decisions.
+
+If implementation changes behavior:
+
+Review and update documentation as appropriate.
+
+Examples:
+
+- README
+- Architecture Status
+- Capability Register
+- Capability Roadmap
+- ADR references
+- Release Notes
+
+---
+
+# Code Reviews
+
+Every implementation should summarize:
+
+Files created.
+
+Files modified.
+
+Reason for change.
+
+Architecture followed.
+
+Relevant ADRs.
+
+Engineering Question reference (if applicable).
+
+Spike reference (if applicable).
+
+Tests executed.
+
+Remaining risks.
+
+---
+
+## Python Environment
+
+Do not activate the virtual environment.
+
+Always invoke the interpreter directly:
+
+    ./.venv/bin/python
+
+Examples:
+
+    ./.venv/bin/python -m pytest
+    ./.venv/bin/python tools/quality/verify_all.py --json
+    ./.venv/bin/python -m pip install <package>
+
+This avoids shell-specific activation issues (Fish/Bash/Zsh) and ensures deterministic execution.
+
+# Repository Workflow
+
+Every milestone should follow:
+
+1. Review architecture.
+2. Review evidence.
+3. Implement the smallest change.
+4. Execute tests.
+5. Review implementation.
+6. Verify documentation.
+7. Summarize changes.
+8. Commit.
+9. Update release documentation when appropriate.
+
+Avoid implementing multiple architectural milestones in a single change unless explicitly approved.
+
+---
+
+# Prohibited Without Approval
+
+Do not introduce:
+
+- Dependency Injection frameworks
+- Plugin frameworks
+- Service Locators
+- Event Buses
+- Reflection-based discovery
+- Dynamic loading
+- Generic abstractions without production use
+- Architecture rewrites
+- Breaking behavioral changes
+
+---
+
+# Communication Guidelines
+
+When interacting with the Project Owner:
+
+Prefer concise explanations.
+
+Avoid repeating repository context.
+
+Reference existing documentation rather than reproducing it.
+
+Present alternatives when appropriate.
+
+Clearly distinguish:
+
+- observations
+- evidence
+- assumptions
+- recommendations
+
+If uncertain:
+
+State the uncertainty.
+
+Do not fabricate confidence.
+
+---
+
+# Engineering Principles
+
+Prefer evidence over assumptions.
+
+Prefer documentation over memory.
+
+Prefer explicit design over implicit behavior.
+
+Prefer deterministic behavior over convenience.
+
+Prefer small stable improvements over speculative frameworks.
+
+Optimize every contribution for long-term maintainability.
+
+Jarvis is intended to evolve for many years.
+
+Every change should leave the repository clearer, more consistent, and easier to maintain than before.
+
+
+# Engineering Quality Assurance Constitution
+
+This repository follows a Verification Before Freeze philosophy.
+
+No implementation, capability, Engineering Question, or milestone may be declared Complete, Frozen, or Production Ready without passing the mandatory Quality Gates.
+
+These gates exist to ensure objective defects are detected by automation before architectural review.
+
+AI agents shall never substitute narrative summaries for executable verification.
+
+# Quality Gate 1 — Mechanical Verification (Mandatory)
+
+The following SHALL be completed before requesting Freeze.
+
+## Testing
+A committed production test suite SHALL exist under tests/.
+Verification tools under tools/ do not replace regression tests.
+Test count increase SHALL be reported.
+Determinism
+
+## If deterministic behavior is claimed:
+
+identical inputs SHALL produce identical outputs.
+full object equality SHALL be verified where the contract claims deterministic outputs.
+metadata (timestamps, identifiers, runtime state) SHALL not invalidate deterministic contracts unless explicitly excluded from the contract.
+Contract Verification
+
+All public contracts SHALL be verified against production implementation.
+
+Documentation shall never be considered proof of behavior.
+
+Documentation Synchronization
+
+Implementation
+
+↓
+
+Tests
+
+↓
+
+Contracts
+
+↓
+
+Documentation
+
+shall remain synchronized.
+
+Documentation drift shall block Freeze.
+
+Version Consistency
+
+Repository version SHALL be consistent across:
+
+README
+version module
+implementation status
+release documentation
+contracts
+Architecture Integrity
+
+Production code SHALL NOT depend on:
+
+docs/
+tools/
+data/reports/
+
+unless explicitly approved.
+
+Spike artifacts shall never become hidden production dependencies.
+
+# Quality Gate 2 — Architecture Verification
+
+Architecture review SHALL verify:
+
+responsibility boundaries
+hidden coupling
+contract integrity
+consumer independence
+determinism
+YAGNI compliance
+ADR compliance
+Engineering Boundary preservation
+
+This review focuses on engineering judgment rather than mechanical correctness.
+
+# Quality Gate 3 — Consumer Readiness
+
+Before introducing a new consumer:
+
+Verify:
+
+stable public API
+import stability
+package boundaries
+contract maturity
+consumer documentation
+backward compatibility
+Engineering Debt Register
+
+Every Engineering Question SHALL conclude with an Engineering Debt Register.
+
+Each item shall include:
+
+ID
+Finding
+Severity
+Blocks Freeze (Yes/No)
+Planned Resolution
+Status
+
+Known engineering debt shall never be silently ignored.
+
+If debt remains, Freeze approval shall explicitly acknowledge it.
+
+Production Verification Rule
+
+AI agents shall never claim production behavior without executable evidence.
+
+Claims regarding:
+
+determinism
+immutability
+performance
+API behavior
+contract compliance
+
+require executable verification or committed automated tests.
+
+Repository summaries are not evidence.
+
+Execution is evidence.
+
+---
+
+# Repository Boundary Constitution
+
+Repository organization is part of the Jarvis Architecture.
+
+Folder structure is considered a frozen engineering asset.
+
+AI agents SHALL preserve repository organization exactly as defined by the architecture.
+
+Repository layout SHALL NOT evolve through implementation.
+
+Only the Project Owner may approve repository structural changes.
+
+---
+
+# Repository Boundary Verification
+
+Before creating ANY file, every AI agent SHALL perform the following verification.
+
+## Step 1 — Classify the Artifact
+
+Every artifact belongs to exactly one architectural category.
+
+Choose one:
+
+- Production Code
+- Test
+- Architecture Documentation
+- Engineering Documentation
+- Knowledge Documentation
+- Execution Documentation
+- Knowledge Repository Data
+- Tooling
+- Configuration
+- Automation
+- Temporary Investigation
+
+If classification is ambiguous:
+
+STOP.
+
+Request clarification.
+
+---
+
+## Step 2 — Determine Repository Owner
+
+Every category has exactly one repository owner.
+
+| Category | Location |
+|----------|----------|
+| Production Code | src/ |
+| Tests | tests/ |
+| Architecture Documentation | docs/ |
+| Engineering Documentation | docs/engineering/ |
+| Knowledge Documentation | docs/knowledge/ |
+| Execution Documentation | docs/execution/ |
+| Knowledge Repository Data | knowledge/ |
+| Tooling | tools/ |
+| Configuration | repository root |
+
+Never create a second owner.
+
+---
+
+## Step 3 — Check Existing Structure
+
+Before creating a new directory:
+
+Search for an existing location.
+
+If an equivalent location already exists:
+
+Reuse it.
+
+Do not create another folder.
+
+---
+
+# Documentation Placement Rules
+
+Permanent documents belong only in permanent locations.
+
+## Architecture
+
+Contains:
+
+Vision
+
+Principles
+
+Blueprint
+
+Kernel
+
+ADR
+
+Ontology
+
+Architecture Status
+
+Repository Architecture
+
+Never place temporary engineering work here.
+
+---
+
+## Engineering
+
+Contains:
+
+Engineering Questions
+
+Spike Reports
+
+Capability Discovery
+
+Capability Evaluation
+
+Capability Register
+
+Implementation Reviews
+
+Engineering Evidence
+
+Engineering Debt
+
+Only engineering activities belong here.
+
+---
+
+## Knowledge Documentation
+
+Contains permanent governance.
+
+Examples:
+
+Knowledge Architecture
+
+Knowledge Governance
+
+Knowledge Lifecycle
+
+Knowledge Storage Policy
+
+Knowledge Engineering Principles
+
+Knowledge Source Management
+
+Knowledge Consumption
+
+Knowledge Ontology
+
+These documents describe the knowledge system itself.
+
+Never place temporary execution history here.
+
+---
+
+## Execution Documentation
+
+Contains temporary activities.
+
+Examples:
+
+Migration reports
+
+Recovery reports
+
+Execution logs
+
+Validation summaries
+
+One-time implementation reports
+
+Temporary rollout documentation
+
+Execution documents SHALL NOT become permanent governance.
+
+---
+
+# Knowledge Repository Rules
+
+knowledge/
+
+contains repository knowledge.
+
+NOT documentation.
+
+Allowed:
+
+knowledge/
+
+    registry/
+
+    governance/
+
+    ontology/
+
+    glossary/
+
+    evidence/
+
+Never place Markdown documentation here unless it is repository-managed knowledge content.
+
+Never duplicate documentation already living under docs/.
+
+---
+
+# Tooling Rules
+
+tools/
+
+contains executable utilities only.
+
+Never place:
+
+reports
+
+documentation
+
+governance
+
+architecture
+
+inside tools/.
+
+---
+
+# Folder Creation Policy
+
+AI agents SHALL NOT create new top-level folders.
+
+AI agents SHALL NOT introduce alternative documentation hierarchies.
+
+AI agents SHALL reuse approved repository structure.
+
+If a new hierarchy appears necessary:
+
+STOP.
+
+Raise an Engineering Question.
+
+Wait for Project Owner approval.
+
+---
+
+# Repository Preservation Rule
+
+Every repository operation SHALL be classified.
+
+Exactly one classification must be assigned.
+
+## Read-Only
+
+Reads only.
+
+Creates nothing.
+
+Changes nothing.
+
+---
+
+## Additive
+
+Creates new files only.
+
+Never modifies existing assets.
+
+---
+
+## Transformative
+
+Updates approved repository-managed artefacts only.
+
+Examples:
+
+documentation
+
+registry
+
+metadata
+
+configuration
+
+tests
+
+---
+
+## Destructive
+
+Deletes
+
+Moves
+
+Renames
+
+Overwrites
+
+Restructures
+
+existing assets.
+
+Destructive operations are prohibited unless explicitly approved by the Project Owner in the current conversation.
+
+---
+
+# Repository Drift Detection
+
+Before milestone completion the AI agent SHALL verify:
+
+□ No duplicate documentation.
+
+□ No duplicated governance.
+
+□ No duplicated execution reports.
+
+□ No competing folder structures.
+
+□ No conflicting repository hierarchy.
+
+□ No undocumented folder creation.
+
+□ No architecture drift.
+
+If any answer is YES:
+
+STOP.
+
+Produce a Repository Drift Report.
+
+Do not request milestone freeze.
+
+---
+
+# Repository Boundary Checklist
+
+Every completion report SHALL include:
+
+Repository Boundary Verification
+
+Repository Drift Check
+
+Documentation Placement Verification
+
+Knowledge Boundary Verification
+
+Tool Boundary Verification
+
+Architecture Compliance
+
+The checklist SHALL explicitly report:
+
+PASS
+
+or
+
+FAIL
+
+for every category.
+
+---
+
+# Constitutional Stop Conditions
+
+The AI agent SHALL immediately stop if:
+
+- repository architecture becomes ambiguous
+
+- two valid locations appear to exist
+
+- documentation placement cannot be justified
+
+- folder ownership becomes unclear
+
+- architecture conflicts with implementation
+
+- repository organization must change
+
+When stopped:
+
+Produce an Architecture Conflict Report.
+
+Do not continue implementation.
+
+---
+
+# Continuous Engineering Rule
+
+Every completed milestone shall leave the repository:
+
+more deterministic
+
+more consistent
+
+more traceable
+
+more reproducible
+
+more maintainable
+
+than it was before implementation.
+
+No milestone shall increase architectural ambiguity.
+
+====================================================
+REPOSITORY QUALITY GATE
+====================================================
+
+Architecture Compliance
+PASS / FAIL
+
+Repository Boundary Verification
+PASS / FAIL
+
+Documentation Placement Verification
+PASS / FAIL
+
+Knowledge Boundary Verification
+PASS / FAIL
+
+Repository Drift Detection
+PASS / FAIL
+
+Destructive Operations
+NONE / LIST
+
+Files Created
+...
+
+Files Modified
+...
+
+Engineering Debt
+...
+
+Risks Remaining
+...
+
+Recommendation
+
+□ Freeze
+□ Continue
+□ Engineering Question Required
+□ ADR Required```

## File: docs/engineering/Engineering_Register.md

```diff
--- Windows: docs/engineering/Engineering_Register.md
+++ Fedora: docs/engineering/Engineering_Register.md
@@ -6,20 +6,20 @@
 
 | EQ Number | Title | Status | Authority Document | Evidence Package | Outcome | Repository Location |
 |-----------|-------|--------|-------------------|------------------|---------|---------------------|
-| EQ-0010 | Deterministic BOQ Structural Intelligence | Completed | [EQ_0010_Deterministic_BOQ_Structural_Intelligence.md](questions/EQ_0010_Deterministic_BOQ_Structural_Intelligence.md) | [evidence/EQ_0010/](evidence/EQ_0010/) | Approved | docs/engineering/ |
-| EQ-0011 | BOQ Semantic Intelligence Boundary | Completed | [EQ_0011_BOQ_Semantic_Intelligence_Boundary.md](questions/EQ_0011_BOQ_Semantic_Intelligence_Boundary.md) | [evidence/EQ_0011/](evidence/EQ_0011/) | Approved | docs/engineering/ |
-| EQ-0012 | BOQ Intelligence Public Evidence Contract | Completed | [EQ_0012_BOQ_Intelligence_Public_Evidence_Contract.md](questions/EQ_0012_BOQ_Intelligence_Public_Evidence_Contract.md) | [evidence/EQ_0012/](evidence/EQ_0012/) | Approved | docs/engineering/ |
-| EQ-0013 | Validation Engine | Completed | [EQ_0013_Validation_Engine.md](questions/EQ_0013_Validation_Engine.md) | [evidence/EQ_0013/](evidence/EQ_0013/) | Approved | docs/engineering/ |
-| EQ-0014 | Parser Regression Investigation | Completed | [EQ_0014_Parser_Regression_Investigation.md](questions/EQ_0014_Parser_Regression_Investigation.md) | [evidence/EQ_0014/](evidence/EQ_0014/) | Approved | docs/engineering/ |
-| EQ-0015 | Structural Containment Investigation | Completed | [EQ_0015_Structural_Containment_Investigation.md](questions/EQ_0015_Structural_Containment_Investigation.md) | [evidence/EQ_0015/](evidence/EQ_0015/) | Approved | docs/engineering/ |
-| EQ-0016 | Trade Classification Authority | Completed | [EQ_0016_Trade_Classification_Authority.md](questions/EQ_0016_Trade_Classification_Authority.md) | [evidence/EQ_0016/](evidence/EQ_0016/) | Approved | docs/engineering/ |
-| EQ-0017 | Repository Governance Migration | Completed | [EQ_0017_Repository_Governance_Migration.md](questions/EQ_0017_Repository_Governance_Migration.md) | [evidence/EQ_0017/](evidence/EQ_0017/) | Approved | docs/engineering/ |
-| EQ-0018 | BOQ Semantic Intelligence | Completed | [EQ_0018_BOQ_Semantic_Intelligence.md](questions/EQ_0018_BOQ_Semantic_Intelligence.md) | [evidence/EQ_0018/](evidence/EQ_0018/) | Approved | docs/engineering/ |
-| EQ-0019 | BOQ Semantic Intelligence Increment 1 | Completed | [EQ_0019_BOQ_Semantic_Intelligence_Increment_1.md](questions/EQ_0019_BOQ_Semantic_Intelligence_Increment_1.md) | [evidence/EQ_0019/](evidence/EQ_0019/) | PERMANENTLY FROZEN — Increment 4 AUTHORIZED | docs/engineering/ |
-| EQ-0020 | BOQ Consumer Architecture | Completed | Referenced in `docs/design/EQ_0020_Architecture_Recommendation.md` | (see EQ-0019 evidence) | PERMANENTLY FROZEN | docs/engineering/ |
-| EQ-0021 | CheckMate Application Architecture | Completed | Referenced in `docs/design/EQ_0021_Architecture_Recommendation.md` | (see design directory) | PERMANENTLY FROZEN | docs/engineering/ |
-| EQ-0022 | Trade Classification Authority Investigation | OPEN | [EQ_0022_Trade_Classification_Authority_Investigation.md](questions/EQ_0022_Trade_Classification_Authority_Investigation.md) | Pending | Investigation not yet started | docs/engineering/questions/ |
-| EQ-0023 | Execution Runtime Architecture | OPEN | [EQ_0023_Execution_Runtime_Architecture.md](questions/EQ_0023_Execution_Runtime_Architecture.md) | Pending | Investigation complete; ADRs required | docs/engineering/questions/ |
+| EQ-0010 | Deterministic BOQ Structural Intelligence | Completed | [EQ_0010_Deterministic_BOQ_Structural_Intelligence.md](EQ_0010_Deterministic_BOQ_Structural_Intelligence.md) | [EQ_0010/](EQ_0010/) | Approved | docs/engineering/ |
+| EQ-0011 | BOQ Semantic Intelligence Boundary | Completed | [EQ_0011_BOQ_Semantic_Intelligence_Boundary.md](EQ_0011_BOQ_Semantic_Intelligence_Boundary.md) | [EQ_0011/](EQ_0011/) | Approved | docs/engineering/ |
+| EQ-0012 | BOQ Intelligence Public Evidence Contract | Completed | [EQ_0012_BOQ_Intelligence_Public_Evidence_Contract.md](EQ_0012_BOQ_Intelligence_Public_Evidence_Contract.md) | [EQ_0012/](EQ_0012/) | Approved | docs/engineering/ |
+| EQ-0013 | Validation Engine | Completed | [EQ_0013_Validation_Engine.md](EQ_0013_Validation_Engine.md) | [EQ_0013/](EQ_0013/) | Approved | docs/engineering/ |
+| EQ-0014 | Parser Regression Investigation | Completed | [EQ_0014_Parser_Regression_Investigation.md](EQ_0014_Parser_Regression_Investigation.md) | [EQ_0014/](EQ_0014/) | Approved | docs/engineering/ |
+| EQ-0015 | Structural Containment Investigation | Completed | [EQ_0015_Structural_Containment_Investigation.md](EQ_0015_Structural_Containment_Investigation.md) | [EQ_0015/](EQ_0015/) | Approved | docs/engineering/ |
+| EQ-0016 | Trade Classification Authority | Completed | [EQ_0016_Trade_Classification_Authority.md](EQ_0016_Trade_Classification_Authority.md) | [EQ_0016/](EQ_0016/) | Approved | docs/engineering/ |
+| EQ-0017 | Repository Governance Migration | Completed | [EQ_0017_Repository_Governance_Migration.md](EQ_0017_Repository_Governance_Migration.md) | [EQ_0017/](EQ_0017/) | Approved | docs/engineering/ |
+| EQ-0018 | BOQ Semantic Intelligence | Completed | [EQ_0018_BOQ_Semantic_Intelligence.md](EQ_0018_BOQ_Semantic_Intelligence.md) | [EQ_0018/](EQ_0018/) | Approved | docs/engineering/ |
+| EQ-0019 | BOQ Semantic Intelligence Increment 1 | Completed | Approved | docs/engineering/ | EQ_0019_BOQ_Semantic_Intelligence_Increment_1.md | EQ_0019/ |
+| EQ-0020 | BOQ Consumer Architecture | COMPLETE | Referenced in `docs/design/EQ_0020_Architecture_Recommendation.md` | (see EQ-0019 evidence) | PERMANENTLY FROZEN | docs/engineering/ |
+| EQ-0021 | CheckMate Application Architecture | COMPLETE | Referenced in `docs/design/EQ_0021_Architecture_Recommendation.md` | (see design directory) | PERMANENTLY FROZEN | docs/engineering/ |
+| EQ-0022 | Trade Classification Authority Investigation | OPEN | [EQ_0022_Trade_Classification_Authority_Investigation.md](EQ_0022_Trade_Classification_Authority_Investigation.md) | Pending | Investigation not yet started | docs/engineering/questions/ |
+| EQ-0023 | Execution Runtime Architecture | OPEN | [EQ_0023_Execution_Runtime_Architecture.md](EQ_0023_Execution_Runtime_Architecture.md) | Pending | Investigation complete; ADRs required | docs/engineering/questions/ |
 
 ## Archive
 
@@ -31,7 +31,7 @@
 
 | KE Number | Title | Status | Location |
 |-----------|-------|--------|-----------|
-| KE-0001 | Knowledge Engineering Foundation | Completed | `docs/execution/KE-0001-R/` |
+| KE-0001 | Knowledge Engineering Foundation | COMPLETE | `docs/execution/KE-0001-R/` |
 | KE-0002 | Knowledge Source Management | ACTIVE | `docs/knowledge/questions/KE_0002_Knowledge_Source_Management.md` |
 
 ## Governance Model Compliance
```

## File: docs/governance/WORKSTREAM_GOVERNANCE.md

```diff
--- Windows: docs/governance/WORKSTREAM_GOVERNANCE.md
+++ Fedora: docs/governance/WORKSTREAM_GOVERNANCE.md
@@ -134,23 +134,6 @@
 
 ---
 
-## Identifier Continuity Policy
-
-Engineering identifiers are permanent repository identifiers.
-
-Once allocated:
-
-1. Identifiers SHALL NOT be renumbered.
-2. Identifier gaps are permitted.
-3. Identifiers SHALL NEVER be reused.
-4. Cancelled, abandoned, superseded, or deprecated work SHALL retain its allocated identifier.
-5. Repository history takes precedence over sequential numbering.
-6. AI agents SHALL NOT create historical artifacts solely to fill numbering gaps.
-
-**Rationale:** Repository identifiers are stable architectural references rather than contiguous sequence numbers. Historical numbering establishes an immutable audit trail that must not be rewritten for cosmetic purposes. Gaps in numbering are a natural artifact of the development process and shall remain as part of the permanent historical record.
-
----
-
 **Version:** 1.0
 **Date:** 2026-07-28
 **Authority:** Repository Governance Harmonization Sprint```

## File: docs/implementation/IP_0001/README.md

```diff
--- Windows: docs/implementation/IP_0001/README.md
+++ Fedora: docs/implementation/IP_0001/README.md
@@ -10,7 +10,7 @@
 
 ## Source Engineering Question
 
-[EQ-0019 — BOQ Semantic Intelligence Increment 1](../../engineering/questions/EQ_0019_BOQ_Semantic_Intelligence_Increment_1.md)
+[EQ-0019 — BOQ Semantic Intelligence Increment 1](../../engineering/questions/../../engineering/questions/EQ_0019_BOQ_Semantic_Intelligence_Increment_1.md)
 
 **Status:** PERMANENTLY FROZEN
 
@@ -51,7 +51,7 @@
 
 ## Applicable Contracts
 
-- [BOQ Intelligence Public Evidence Contract v1.1.0](../../contracts/BOQ_Intelligence_Public_Evidence_Contract_v1.1.md) — Frozen
+- [BOQ Intelligence Public Evidence Contract v1.1.0](../../contracts/../documentation/contracts/BOQ_Intelligence_Public_Evidence_Contract_v1.1.md) — Frozen
 
 ## Verification Documents
 
```

## File: docs/knowledge/04_Engineering_Governance.md

```diff
--- Windows: docs/knowledge/04_Engineering_Governance.md
+++ Fedora: docs/knowledge/04_Engineering_Governance.md
@@ -12,7 +12,7 @@
 - AI agent operating rules (from AGENTS.md and AI_Agent_Operating_Manual.md)
 - Governance principles that constrain all engineering work
 
-It does NOT cover detailed methodology steps (see `09_Methodology.md`) or individual ADR summaries (see [Appendix B](Appendices/B_ADR_Registry.md)).
+It does NOT cover detailed methodology steps (see `09_Methodology.md`) or individual ADR summaries (see [Appendix B](../decisions/B_ADR_Registry.md)).
 
 ---
 
@@ -215,7 +215,7 @@
 - `docs/engineering/AI_Agent_Operating_Manual.md` — Operating procedures (406 lines)
 - `docs/engineering/Engineering_Governance.md` — Governance rules
 - `docs/decisions/` — All 26 ADRs
-- `docs/knowledge/Appendices/B_ADR_Registry.md` — ADR summary
+- `docs/knowledge/../decisions/B_ADR_Registry.md` — ADR summary
 - `docs/knowledge/09_Methodology.md` — Detailed engineering playbook
 
 ---
```

## File: knowledge/registry/knowledge_inventory.csv

No textual difference or file reading error.

## File: knowledge/registry/source_manifest.json

No textual difference or file reading error.

## File: src/jarvis/application/__init__.py

```diff
--- Windows: src/jarvis/application/__init__.py
+++ Fedora: src/jarvis/application/__init__.py
@@ -1,7 +1,5 @@
-"""Jarvis Application Services."""
+"""Application package - Composition root for Jarvis Platform."""
 
 from jarvis.application.application import Application
-from jarvis.application.contracts import ConversationRequest
-from jarvis.application.conversation import ConversationService
 
-__all__ = ["Application", "ConversationRequest", "ConversationService"]
+__all__ = ["Application"]```

## File: tests/__init__.py

```diff
--- Windows: tests/__init__.py
+++ Fedora: tests/__init__.py
@@ -1 +1 @@
-# Test package+"""Jarvis Platform Tests."""```

## File: tests/validation/test_verify_governance_integration.py

```diff
--- Windows: tests/validation/test_verify_governance_integration.py
+++ Fedora: tests/validation/test_verify_governance_integration.py
@@ -109,7 +109,7 @@
         errors = [f for f in findings if f.startswith("ERROR:")]
         warnings = [f for f in findings if f.startswith("WARN:")]
         # Allow warnings but ensure errors are limited
-        assert len(errors) < 25, f"Too many register errors: {errors}"
+        assert len(errors) < 15, f"Too many register errors: {errors}"
 
 
 class TestVerifyGovernanceIntegration:
```

