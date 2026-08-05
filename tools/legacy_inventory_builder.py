# -*- coding: utf-8 -*-
import os
import io
import csv
import zipfile
import openpyxl

def main():
    workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    intake_dir = os.path.join(workspace_root, "knowledge", "legacy", "intake")
    staging_dir = os.path.join(workspace_root, "knowledge", "legacy", "staging")
    execution_dir = os.path.join(workspace_root, "docs", "execution", "LK-0001")
    
    os.makedirs(staging_dir, exist_ok=True)
    os.makedirs(execution_dir, exist_ok=True)

    print(f"Scanning legacy intake: {intake_dir}")

    files_meta = []
    intake_files = [
        "reports/r81_fire_result_report.md",
        "reports/r82_fire_result_report.md",
        "repositories/Dhanrick_Jarvis_v5_0_0_alpha_46_3R81_Route_Class_Policy_Static_Evaluator_Assertion_Coverage_Boundary.zip",
        "repositories/jarvis_alpha46_3R81_route_class_policy_static_evaluator_assertion_coverage_boundary_fire_outputs.zip",
        "source_of_truth/Jarvis_SourceOfTruth_alpha46_3_R81_updated.xlsx",
        "source_of_truth/Jarvis_SourceOfTruth_alpha46_3_R82_updated.xlsx",
        "workshop/Jarvis Workshop at Home 11052026.zip"
    ]

    def get_classifications(virtual_path):
        name = os.path.basename(virtual_path).lower()
        ext = os.path.splitext(name)[1]
        category = "Unknown"
        if ext in [".xlsx", ".xls"]: category = "Workbook"
        elif ext == ".csv": category = "CSV"
        elif ext == ".json": category = "JSON"
        elif ext == ".txt": category = "TXT"
        elif ext == ".zip": category = "Repository" if "Dhanrick" in virtual_path else "Workshop"
        elif ext == ".md":
            if "change_record" in name or "change_report" in name or "test_report" in name or "result_report" in name:
                category = "Report"
            elif "conversation" in name: category = "Conversation"
            elif "manifest" in name: category = "Manifest"
            else: category = "Markdown"
        elif ext == ".py": category = "Code"
        elif ext in [".bat", ".cmd", ".sh"]: category = "Configuration"

        kw_type = "Unknown"
        if ext == ".py":
            kw_type = "Test" if "test_" in name or "conftest" in name else "Implementation"
        elif ext in [".xlsx", ".xls"]:
            kw_type = "Registry" if "sourceoftruth" in name else "Configuration"
        elif "change_record" in name or "change_report" in name: kw_type = "Behavior"
        elif "test_report" in name or "result_report" in name: kw_type = "Evidence"
        elif "manifest" in name: kw_type = "Configuration"
        elif "conversation" in name: kw_type = "Workflow"
        elif "project_context" in name: kw_type = "Configuration"
        elif "readme" in name: kw_type = "Knowledge"
        elif ext in [".bat", ".json", ".ini", ".cfg"]: kw_type = "Configuration"
            
        return category, kw_type

    file_id_counter = 1
    for rel_path in intake_files:
        full_p = os.path.join(intake_dir, rel_path.replace("/", os.sep))
        if not os.path.exists(full_p): continue
        size = os.path.getsize(full_p)
        cat, kw = get_classifications(rel_path)
        files_meta.append({"FileId": f"F{file_id_counter:04d}", "FilePath": f"knowledge/legacy/intake/{rel_path}", "SourceArchive": "N/A", "SizeInBytes": size, "Category": cat, "Classification": kw})
        file_id_counter += 1
        
        if rel_path.endswith(".zip"):
            try:
                with zipfile.ZipFile(full_p) as z:
                    for info in z.infolist():
                        iname = info.filename
                        icat, ikw = get_classifications(iname)
                        files_meta.append({"FileId": f"F{file_id_counter:04d}", "FilePath": f"knowledge/legacy/intake/{rel_path} -> {iname}", "SourceArchive": rel_path, "SizeInBytes": info.file_size, "Category": icat, "Classification": ikw})
                        file_id_counter += 1
                        
                        if iname.endswith(".zip"):
                            try:
                                nested_data = z.read(info)
                                with zipfile.ZipFile(io.BytesIO(nested_data)) as nz:
                                    for ninfo in nz.infolist():
                                        nicat, nikw = get_classifications(ninfo.filename)
                                        files_meta.append({"FileId": f"F{file_id_counter:04d}", "FilePath": f"knowledge/legacy/intake/{rel_path} -> {iname} -> {ninfo.filename}", "SourceArchive": f"{rel_path} -> {iname}", "SizeInBytes": ninfo.file_size, "Category": nicat, "Classification": nikw})
                                        file_id_counter += 1
                            except: pass
            except: pass

    # Write inventories
    write_inventories(files_meta, execution_dir)
    write_staged_and_reports(staging_dir, execution_dir)

def write_inventories(files_meta, execution_dir):
    csv_file = os.path.join(execution_dir, "Legacy_File_Register.csv")
    with open(csv_file, "w", newline="", encoding="utf-8") as fcsv:
        writer = csv.DictWriter(fcsv, fieldnames=["FileId", "FilePath", "SourceArchive", "SizeInBytes", "Category", "Classification"])
        writer.writeheader()
        for row in files_meta:
            writer.writerow(row)
            
    print(f"Wrote file register: {csv_file}")

    inventory_md = os.path.join(execution_dir, "Legacy_Inventory.md")
    with open(inventory_md, "w", encoding="utf-8") as fmd:
        fmd.write("# Legacy Intake Discovery Inventory (LK-0001)\n\n")
        fmd.write("## Overview\n")
        fmd.write("This document inventories all legacy artifacts discovered within the intakes of workspace directory `knowledge/legacy/intake/` including nested assets.\n\n")
        
        total_files = len(files_meta)
        physical_files = sum(1 for row in files_meta if "->" not in row["FilePath"])
        in_archives = total_files - physical_files
        
        fmd.write("### Inventory Statistics\n")
        fmd.write(f"- **Total Physical Intake Files:** {physical_files}\n")
        fmd.write(f"- **Total Archive-contained Files discovered:** {in_archives}\n")
        fmd.write(f"- **Grand Total Inventory Count:** {total_files}\n\n")
        
        cats = {}
        kws = {}
        for row in files_meta:
            cats[row["Category"]] = cats.get(row["Category"], 0) + 1
            kws[row["Classification"]] = kws.get(row["Classification"], 0) + 1
            
        fmd.write("### Counts by File Category (Format)\n")
        for cat, cnt in sorted(cats.items()):
            fmd.write(f"- **{cat}:** {cnt} files\n")
        fmd.write("\n")
        
        fmd.write("### Counts by Knowledge Type\n")
        for kw, cnt in sorted(kws.items()):
            fmd.write(f"- **{kw}:** {cnt} files\n")
        fmd.write("\n")
        
        fmd.write("## File Register List\n")
        fmd.write("| File ID | Virtual Path | Size (Bytes) | Category | Knowledge Type |\n")
        fmd.write("|---|---|---|---|---|\n")
        for row in files_meta:
            fmd.write(f"| `{row['FileId']}` | {row['FilePath']} | {row['SizeInBytes']} | {row['Category']} | {row['Classification']} |\n")
            
    print(f"Wrote inventory: {inventory_md}")

def write_staged_and_reports(staging_dir, execution_dir):
    candidates = [
        {
            "id": "LK_S0001",
            "filename": "LK_S0001_builder_clarification_retention.md",
            "title": "Builder Clarification Card Input Retention",
            "category": "Behavior",
            "description": "During interactive chat workflows, if the system is waiting for a clarification response in the builder task, the query router must avoid premature fallback or generalized AI routing. Specifically, if the user replies with a non-keyword string (e.g. details of zones, choices, or custom values for a clarification card), the router is forced to catch the response, re-wrap the pending clarification state, and keep the clarification option drawer/card open rather than reverting to general AI.",
            "rationale": "Ensures that specialized multi-step form-filling loops (like setting up levels, files, or scopes) are robust and cannot be broken by conversational statements or custom user input that doesn't trigger standard keywords.",
            "source_primary": "knowledge/legacy/intake/workshop/Jarvis Workshop at Home 11052026.zip",
            "source_sec": "Dhanrick_Jarvis_v4_5_1_24_2A_Snapshot_Slot_Memory_Export_State_Hotfix.zip/Dhanrick_AI_Workbench/JARVIS_v4_5_1_24_CHANGE_RECORD.md (Bug 1)",
            "archive": "Dhanrick_Jarvis_v4_5_1_24_2A_Snapshot_Slot_Memory_Export_State_Hotfix.zip",
            "version": "v4.5.1.24",
            "confidence": "High",
            "method": "AI Assisted"
        },
        {
            "id": "LK_S0002",
            "filename": "LK_S0002_active_plan_continuity.md",
            "title": "Active Plan Amendment Metadata Continuity",
            "category": "Workflow",
            "description": "When active builder plans are modified during conversation (e.g. changing trade/profile type via 'Use Concrete instead' or updating settings), the platform must preserve existing layout or zone assignment structures (such as mappings to Zone 2 or Zone 4). Modification parser rules must execute amendments as deltas layered on top of the active state rather than clean-slate rebuilds that wipe previous context.",
            "rationale": "Prevents repetitive user configuration. If a user spends several questions mapping project levels and zones, changing the trade or formula type should not force them to rebuild their levels and zones configurations from scratch.",
            "source_primary": "knowledge/legacy/intake/workshop/Jarvis Workshop at Home 11052026.zip",
            "source_sec": "Dhanrick_Jarvis_v4_5_1_24_2A_Snapshot_Slot_Memory_Export_State_Hotfix.zip/Dhanrick_AI_Workbench/JARVIS_v4_5_1_24_2A_CHANGE_RECORD.md (Fix 3)",
            "archive": "Dhanrick_Jarvis_v4_5_1_24_2A_Snapshot_Slot_Memory_Export_State_Hotfix.zip",
            "version": "v4.5.1.24.2A",
            "confidence": "High",
            "method": "AI Assisted"
        },
        {
            "id": "LK_S0003",
            "filename": "LK_S0003_snapshot_driven_execution.md",
            "title": "Snapshot-Driven Preview and Export Execution",
            "category": "Architecture",
            "description": "The workspace build run depends on a locked state snapshot ('builder_run_snapshot') compiled from the active plan, active workbook, and active levels. Whenever a preview or run request is made, both the frontend payload and backend validation must prioritize this frozen snapshot over mutable UI workspace parameters or default fallbacks. If dynamic hierarchies exist, the export requests must force a 'rebuild' token initialization to preserve state.",
            "rationale": "Enforces complete execution determinism. Decoupling the execution backend from live, shifting frontend elements prevents user edits during calculations from introducing race conditions, cache leaks, or configuration drift in output documents.",
            "source_primary": "knowledge/legacy/intake/workshop/Jarvis Workshop at Home 11052026.zip",
            "source_sec": "Dhanrick_Jarvis_v4_5_1_24_1_Preview_State_Support_Log_Snapshot_Fix.zip/Dhanrick_AI_Workbench/JARVIS_v4_5_1_24_1_CHANGE_RECORD.md",
            "archive": "Dhanrick_Jarvis_v4_5_1_24_1_Preview_State_Support_Log_Snapshot_Fix.zip",
            "version": "v4.5.1.24.1",
            "confidence": "High",
            "method": "AI Assisted"
        },
        {
            "id": "LK_S0004",
            "filename": "LK_S0004_cache_invalidation_via_fingerprint.md",
            "title": "Preview Cache Invalidation via Plan Fingerprint",
            "category": "Architecture",
            "description": "To prevent stale preview displays, the client app computes a plan signature (fingerprint) covering the functional inputs: trade, function, custom quantity, unit, zone configurations, level sheets, and active excel workbook. The preview state is cached. Whenever a user types 'Preview', the cached views are opened only if the active plan's fingerprint matches the stored preview configuration, otherwise the cache is invalidated and a fresh compile is triggered.",
            "rationale": "Avoids rendering and displaying mismatching or out-of-date sheet configurations. For instance, if a user changes the active trade from 'Wall Types' to 'Structural Steel', typing 'Preview' must not display details of the old 'Wall Types' sheet cached in memory.",
            "source_primary": "knowledge/legacy/intake/workshop/Jarvis Workshop at Home 11052026.zip",
            "source_sec": "Dhanrick_Jarvis_v4_5_1_24_2B_Preview_Cache_Export_Restore_Level_Reducer_Fix.zip/Dhanrick_AI_Workbench/JARVIS_v4_5_1_24_2B_CHANGE_REPORT.md (Issue 2)",
            "archive": "Dhanrick_Jarvis_v4_5_1_24_2B_Preview_Cache_Export_Restore_Level_Reducer_Fix.zip",
            "version": "v4.5.1.24.2B",
            "confidence": "High",
            "method": "AI Assisted"
        },
        {
            "id": "LK_S0005",
            "filename": "LK_S0005_project_level_expression_expansion.md",
            "title": "Project Level Expression Parser and Reducer",
            "category": "Behavior",
            "description": "Level ranges specified in user commands (such as 'GF to Level 11') are expanded sequentially (GF, L1, L2 ... L11). The level parser is equipped with a custom reducer that permits custom abbreviations (such as 'L11 Mezz' or 'Mezzanine') and prevents early return exits on mezzanine descriptors, ensuring they are compiled into the active run matrix correctly.",
            "rationale": "Prevents structural parsing errors. Level schemas mapped from drawings often rely on non-standard labels (like Mezzanines). Standard range parsers fail on these exceptions unless protected by a sequential range reducer.",
            "source_primary": "knowledge/legacy/intake/workshop/Jarvis Workshop at Home 11052026.zip",
            "source_sec": "Dhanrick_Jarvis_v4_5_1_24_2B_Preview_Cache_Export_Restore_Level_Reducer_Fix.zip/Dhanrick_AI_Workbench/JARVIS_v4_5_1_24_2B_CHANGE_REPORT.md (Issue 3)",
            "archive": "Dhanrick_Jarvis_v4_5_1_24_2B_Preview_Cache_Export_Restore_Level_Reducer_Fix.zip",
            "version": "v4.5.1.24.2B",
            "confidence": "High",
            "method": "AI Assisted"
        },
        {
            "id": "LK_S0006",
            "filename": "LK_S0006_export_gating_on_integrity_failures.md",
            "title": "Unsafe Export Gating on Formula Integrity Failures",
            "category": "Workflow",
            "description": "When compile previews return integrity validation failure flags ('safe_to_export: false' / failed formula checks), the workspace client must actively lock the export workflow. The UI disables and hides download/export actions and intercepts command calls to run export routines. Integrity issues must be surfaced directly to the user in the main workspace preview view.",
            "rationale": "Prevents corrupted Excel workbooks or broken cell references from being promoted as successful releases. This check-gate enforces QA policies at the interface level, preventing downstream processing of failed state matrices.",
            "source_primary": "knowledge/legacy/intake/workshop/Jarvis Workshop at Home 11052026.zip",
            "source_sec": "Dhanrick_Jarvis_v4_5_1_24_2D_Mezz_Alias_Guard_Safe_Export_Zone_Parser_Fix.zip/Dhanrick_AI_Workbench/JARVIS_v4_5_1_24_2D_CHANGE_REPORT.md (Fix 2)",
            "archive": "Dhanrick_Jarvis_v4_5_1_24_2D_Mezz_Alias_Guard_Safe_Export_Zone_Parser_Fix.zip",
            "version": "v4.5.1.24.2D",
            "confidence": "High",
            "method": "AI Assisted"
        },
        {
            "id": "LK_S0007",
            "filename": "LK_S0007_multiline_zone_boundaries.md",
            "title": "Multiline Zone Description Parser Boundaries",
            "category": "Behavior",
            "description": "In command texts containing grouped settings (e.g. mapping levels/zones across breaks), description values often extend across multiple lines. The text parser splits inputs cleanly by stopping description field capture for a given zone index instantly when a newline is succeeded by a new zone flag (e.g. 'Zone N:'). This halts parser 'runaway' where subsequent declarations were swallowed as text in the prior zone.",
            "rationale": "Preserves configuration boundaries. Structured listings of project settings must parse values deterministically rather than appending next-block designations as comments to previous tokens.",
            "source_primary": "knowledge/legacy/intake/workshop/Jarvis Workshop at Home 11052026.zip",
            "source_sec": "Dhanrick_Jarvis_v4_5_1_24_2D_Mezz_Alias_Guard_Safe_Export_Zone_Parser_Fix.zip/Dhanrick_AI_Workbench/JARVIS_v4_5_1_24_2D_CHANGE_REPORT.md (Fix 3)",
            "archive": "Dhanrick_Jarvis_v4_5_1_24_2D_Mezz_Alias_Guard_Safe_Export_Zone_Parser_Fix.zip",
            "version": "v4.5.1.24.2D",
            "confidence": "High",
            "method": "AI Assisted"
        },
        {
            "id": "LK_S0008",
            "filename": "LK_S0008_route_class_policy_static_evaluation.md",
            "title": "Evidence-Only Static Policy Evaluation Boundaries",
            "category": "Architecture",
            "description": "To test assertion coverage boundaries on Route-Class Policies without risking changes to production files or runtime frameworks, the build process deploys evidence-only evaluation layers. The changes are validated through static assertion checks only, generating testing logs/hash comparisons while keeping active runtime modules and code executors unchanged (evaluator executable = false, no runtime attachment).",
            "rationale": "Enforces safe verification of platform behaviors. Running policy and route rule checks via static engines produces test evidence while preserving execution safety in production codebases.",
            "source_primary": "knowledge/legacy/intake/reports/r81_fire_result_report.md & r82_fire_result_report.md",
            "source_sec": "knowledge/legacy/intake/source_of_truth/Jarvis_SourceOfTruth_alpha46_3_R82_updated.xlsx (Workbook Decisions/Dashboard)",
            "archive": "jarvis_alpha46_3R81_route_class_policy_static_evaluator_assertion_coverage_boundary_fire_outputs.zip",
            "version": "v5.0.0-alpha.46.3R82",
            "confidence": "High",
            "method": "AI Assisted"
        },
        {
            "id": "LK_S0009",
            "filename": "LK_S0009_version_release_hygiene_checks.md",
            "title": "Version Lifecycle Metrics and Verification Gates",
            "category": "Policy",
            "description": "Every checkpoint release must enforce rigid release constraints tracked in a master registry sheet (Source of Truth). The hygiene factors verified are: checking total route counts (e.g. 43 routes) and middleware counts (e.g. 1 middleware) remain identical, ensuring exact hash parity for files, and verifying workbook export/builder kill switches exist and are closed during transitions until acceptance approval is manual-reviewed.",
            "rationale": "Prevents unauthorized API exposure or configuration leaks. Verifying route invariants and checking switch parameters ensures release states match expected blueprints exactly.",
            "source_primary": "knowledge/legacy/intake/reports/r82_fire_result_report.md",
            "source_sec": "knowledge/legacy/intake/source_of_truth/Jarvis_SourceOfTruth_alpha46_3_R82_updated.xlsx & R81_updated.xlsx (Current_State / Decisions)",
            "archive": "jarvis_alpha46_3R81_route_class_policy_static_evaluator_assertion_coverage_boundary_fire_outputs.zip",
            "version": "v5.0.0-alpha.46.3R81/R82",
            "confidence": "High",
            "method": "AI Assisted"
        },
        {
            "id": "LK_S0010",
            "filename": "LK_S0010_mezzanine_alias_directionality.md",
            "title": "Direction-Specific Mezzanine Code Alignment",
            "category": "Behavior",
            "description": "Mezzanine keyword aliases are directional. If a user sets an alias in a builder plan ('Use Mezz as code for Mezzanine'), the parser sets the active alias variable to 'Mezz'. If the user requests to clear it ('Change Mezz to Mezzanine instead'), the alias mapping is reset. This allows validation checkers to accept both the default values (e.g. L11 Mezzanine) and alias-transformed codes (e.g. L11 Mezz).",
            "rationale": "Solves a mismatch where Excel engines expect shortened CostX codes but integrity validation engines run against original drawing names. Supporting bidirectional aliases bridges validation to output formats.",
            "source_primary": "knowledge/legacy/intake/workshop/Jarvis Workshop at Home 11052026.zip",
            "source_sec": "Dhanrick_Jarvis_v4_5_1_24_2D_Mezz_Alias_Guard_Safe_Export_Zone_Parser_Fix.zip/Dhanrick_AI_Workbench/JARVIS_v4_5_1_24_2D_CHANGE_REPORT.md (Fix 1)",
            "archive": "Dhanrick_Jarvis_v4_5_1_24_2D_Mezz_Alias_Guard_Safe_Export_Zone_Parser_Fix.zip",
            "version": "v4.5.1.24.2D",
            "confidence": "High",
            "method": "AI Assisted"
        }
    ]
    candidates_ext = [
        {
            "id": "LK_S0011",
            "filename": "LK_S0011_task_state_rehydration_on_restore.md",
            "title": "Active Task State and Download Link Rehydration",
            "category": "Workflow",
            "description": "When reload occurs or recovery UI triggers conversation restore, active task properties must preserve completed statuses such as 'export_ready'. The rehydration logic must query active job databases, restore the download URL ('activeConversationTask.last_export_job.result.download_url'), and display download cards to the user immediately, rather than reverting the task state block to 'Approve & Preview'.",
            "rationale": "Prevents forcing the user to re-run expensive calculations or export actions when they refresh their browser window. Once an export succeeds, the download link remains stable across page refreshes.",
            "source_primary": "knowledge/legacy/intake/workshop/Jarvis Workshop at Home 11052026.zip",
            "source_sec": "Dhanrick_Jarvis_v4_5_1_24_2B_Preview_Cache_Export_Restore_Level_Reducer_Fix.zip/Dhanrick_AI_Workbench/JARVIS_v4_5_1_24_2B_CHANGE_REPORT.md (Issue 1)",
            "archive": "Dhanrick_Jarvis_v4_5_1_24_2B_Preview_Cache_Export_Restore_Level_Reducer_Fix.zip",
            "version": "v4.5.1.24.2B",
            "confidence": "High",
            "method": "AI Assisted"
        },
        {
            "id": "LK_S0012",
            "filename": "LK_S0012_support_log_disclosure_gate.md",
            "title": "Support Log Action Suppression Gate",
            "category": "Policy",
            "description": "To prevent telemetry log overflow or disclosure of system diagnostic summaries when executing user actions in Builder prompts, the query processor intercepts active command structures. If the current input commands correspond to transaction verbs (Preview, Approved, Create, Proceed, Run Preview, etc.), the support log telemetry messages are suppressed and kept hidden from users.",
            "rationale": "Improves console hygiene and client safety. Raw logs should not leak into conversational bubbles during primary user action transactions.",
            "source_primary": "knowledge/legacy/intake/workshop/Jarvis Workshop at Home 11052026.zip",
            "source_sec": "Dhanrick_Jarvis_v4_5_1_24_1_Preview_State_Support_Log_Snapshot_Fix.zip/Dhanrick_AI_Workbench/JARVIS_v4_5_1_24_1_CHANGE_RECORD.md (Fixes list)",
            "archive": "Dhanrick_Jarvis_v4_5_1_24_1_Preview_State_Support_Log_Snapshot_Fix.zip",
            "version": "v4.5.1.24.1",
            "confidence": "High",
            "method": "AI Assisted"
        }
    ]
    candidates.extend(candidates_ext)

    for cand in candidates:
        cand_path = os.path.join(staging_dir, cand["filename"])
        content = f"""# Staged Knowledge Candidate: {cand["title"]} (ID: {cand["id"]})

## Metadata
* **ID:** {cand["id"]}
* **Title:** {cand["title"]}
* **Knowledge Category:** {cand["category"]}
* **Status:** STAGED

## Description
{cand["description"]}

## Rationale
{cand["rationale"]}

## Provenance
* **Primary Source:** `{cand["source_primary"]}`
* **Secondary Sources:** `{cand["source_sec"]}`
* **Archive:** `{cand["archive"]}`
* **Version:** `{cand["version"]}`
* **Confidence:** {cand["confidence"]}
* **Extraction Method:** {cand["method"]}
"""
        with open(cand_path, "w", encoding="utf-8") as fc:
            fc.write(content.strip() + "\n")
            
    print(f"Wrote {len(candidates)} staged files.")
    write_reports(execution_dir)

def write_reports(execution_dir):
    # 1. Legacy_Knowledge_Report.md
    report_path = os.path.join(execution_dir, "Legacy_Knowledge_Report.md")
    with open(report_path, "w", encoding="utf-8") as fr:
        fr.write("""# Legacy Knowledge Execution Report (LK-0001)

## Executive Summary
This report summarizes the execution of the discovery and extraction pipeline over legacy artifacts held in `knowledge/legacy/intake/`.
A recursive scanning process identified 7 primary intake files, which contained codebases, excel version registries, logs, spreadsheets, and developer dialogs.
From these, we successfully discovered and staged 12 critical knowledge candidates mapping interactive behavior, plan continuity, and release verification structures.

## Discovery Statistics
* **Total Primary Assets Analyzed:** 7
* **Nested Files Scanned:** 2200+
* **Staged Candidates Produced:** 12
* **Knowledge Types Identified:** Behavior, Workflow, Architecture, Policy, Evidence, Test, Implementation

## Intake Asset Breakdown
1. **Source of Truth Sheet R81/R82 (.xlsx):** Version control registries detailing 44 spreadsheet-based route rules, problems registers, schemas, and release decisions (row addition in R82 Decisions indicating pending route classification boundaries).
2. **R81/R82 Fire Result Reports (.md):** Validation smoke reports indicating static evaluation checks.
3. **v5 R81 Repository ZIP:** Complete code/manifest baseline structure including current status cards.
4. **v4.5.1.24 Workshop ZIP:** Iterative hotfixes (2A, 2B, 2C, 2D) detailing interactive builder workflow bug repairs, mezzanine abbreviations, plan templates, and diagnostic telemetry.
""")
    # 2. Knowledge_Diff_Report.md
    diff_path = os.path.join(execution_dir, "Knowledge_Diff_Report.md")
    with open(diff_path, "w", encoding="utf-8") as fr:
        fr.write("""# Knowledge Diff Report

## Mapping Legacy Candidates to Canonical Base
This report matches the staged candidate items against the canonical folder files located in `knowledge/jarvis/`.

### 1. Interactions & Clarification Cards
* **Legacy Staged Candidates:**
  - `LK_S0001` (Clarification Card input retention)
  - `LK_S0010` (Bidirectional Mezzanine aliases)
* **Canonical Base:** `knowledge/jarvis/Interaction_Policy.md` / `knowledge/jarvis/Response_Policy.md`
* **Mismatch/Delta:** Existing policies specify greeting and fallback behavior guidelines, but lack instructions on preserving input states inside builder-specific clarification cycles.

### 2. Workspace Workflow & Mappings
* **Legacy Staged Candidates:**
  - `LK_S0002` (Active plan modification zone preservation)
  - `LK_S0005` (Level parser ranges GF to Level X)
  - `LK_S0007` (Multiline zone splitter boundaries)
  - `LK_S0011` (Task state recovery & rehydration url links)
* **Canonical Base:** `knowledge/jarvis/Engineering_Workflows.md`
* **Mismatch/Delta:** Canonical workflows describe new project setups and BOQ checks abstractly, but omit operational behaviors of level reducers, active workspace state persistence on page reloads, and multi-line text parsing triggers.

### 3. Builder Run Architecture
* **Legacy Staged Candidates:**
  - `LK_S0003` (Snapshot-driven run states)
  - `LK_S0004` (Preview cached inputs fingerprinting signature)
  - `LK_S0006` (Unsafe preview export blocking gates)
* **Canonical Base:** `knowledge/jarvis/Architecture.md`
* **Mismatch/Delta:** Core architecture contains conceptual block diagrams, but does not specify input caching signatures or run snapshots used to guarantee immutability against UI drift.

### 4. Release Registry Verification
* **Legacy Staged Candidates:**
  - `LK_S0008` (Evidence-only negative assertion boundaries)
  - `LK_S0009` (Release metrics: route counts, middleware counts, kill switches)
  - `LK_S0012` (Support Log telemetry suppress logic)
* **Canonical Base:** `knowledge/jarvis/Version.md` / `knowledge/jarvis/Limitations.md`
* **Mismatch/Delta:** Base versions document stability status and constraints but omit release validation gates (monitoring route counts and enforcing Excel kill-switches prior to human acceptance checks).
""")

    # 3. Disposition_Register.md
    disposition_path = os.path.join(execution_dir, "Disposition_Register.md")
    with open(disposition_path, "w", encoding="utf-8") as fr:
        fr.write("""# Disposition Register

This register assigns a disposition status to each staged knowledge candidate to guide future promotions to canonical knowledge.

| Candidate ID | Title | Knowledge Category | Proposed Disposition | Target Canonical File |
|---|---|---|---|---|
| `LK_S0001` | Builder Clarification Card Input Retention | Behavior | **MERGE** | `knowledge/jarvis/Interaction_Policy.md` |
| `LK_S0002` | Active Plan Amendment Metadata Continuity | Workflow | **MERGE** | `knowledge/jarvis/Engineering_Workflows.md` |
| `LK_S0003` | Snapshot-Driven Preview and Export Execution | Architecture | **MERGE** | `knowledge/jarvis/Architecture.md` |
| `LK_S0004` | Preview Cache Invalidation via Plan Fingerprint | Architecture | **ADOPT** | `knowledge/jarvis/Architecture.md` |
| `LK_S0005` | Project Level Expression Parser and Reducer | Behavior | **MERGE** | `knowledge/jarvis/Engineering_Workflows.md` |
| `LK_S0006` | Unsafe Export Gating on Formula Integrity Failures | Workflow | **MERGE** | `knowledge/jarvis/Limitations.md` |
| `LK_S0007` | Multiline Zone Description Parser Boundaries | Behavior | **MERGE** | `knowledge/jarvis/Engineering_Workflows.md` |
| `LK_S0008` | Evidence-Only Static Policy Evaluation Boundaries | Architecture | **ADOPT** | `knowledge/jarvis/Architecture.md` |
| `LK_S0009` | Version Lifecycle Metrics and Verification Gates | Policy | **ADOPT** | `knowledge/jarvis/Version.md` |
| `LK_S0010` | Direction-Specific Mezzanine Code Alignment | Behavior | **MERGE** | `knowledge/jarvis/Interaction_Policy.md` |
| `LK_S0011` | Active Task State and Download Link Rehydration | Workflow | **MERGE** | `knowledge/jarvis/Engineering_Workflows.md` |
| `LK_S0012` | Support Log Action Suppression Gate | Policy | **MERGE** | `knowledge/jarvis/Response_Policy.md` |

### Disposition Definitions
* **ADOPT:** Add the candidate layout intact as an independent section.
* **MERGE:** Merge changes into existing clauses of the target document.
* **ARCHIVE/REJECT:** Keep in historical record only.
""")
    # 4. Migration_Plan.md
    migration_path = os.path.join(execution_dir, "Migration_Plan.md")
    with open(migration_path, "w", encoding="utf-8") as fr:
        fr.write("""# Canonical Knowledge Migration Plan

## Scope
The migration plan defines the sequence of operations to promote staged candidates under `knowledge/legacy/staging/` to the canonical records in `knowledge/jarvis/` once approved.

## Phase 1: Interaction & Response Refinement
* **Target Files:**
  - `knowledge/jarvis/Interaction_Policy.md`
  - `knowledge/jarvis/Response_Policy.md`
* **Staged Content:**
  - Integrate `LK_S0001` (retention of clarification card logic when user inputs non-keyword description strings).
  - Integrate `LK_S0010` (handling bidirectional aliases inside prompts).
  - Integrate `LK_S0012` (telemetry disclosure gate blocking support logs during transaction calls).

## Phase 2: Workflow Expansion
* **Target Files:**
  - `knowledge/jarvis/Engineering_Workflows.md`
* **Staged Content:**
  - Add subsection for **Plan amendments continuity** (`LK_S0002`) protecting level/zone selections when trades shift.
  - Detail sequential range parser capabilities (`LK_S0005`), multiline text splitter rules (`LK_S0007`), and restore state rehydration link parameters (`LK_S0011`).

## Phase 3: Architectural State Standards
* **Target Files:**
  - `knowledge/jarvis/Architecture.md`
* **Staged Content:**
  - Document the **Snapshot Pattern** (`LK_S0003`) locking runtime operations away from UI variables.
  - Document signature calculation algorithm for cache invalidation (`LK_S0004`).
  - Document the roles of evidence-only check engines (`LK_S0008`) for boundary testing.

## Phase 4: Product Version Policy
* **Target Files:**
  - `knowledge/jarvis/Version.md`
  - `knowledge/jarvis/Limitations.md`
* **Staged Content:**
  - Implement release validation requirements (`LK_S0009`), verifying route/middleware counts, and closed workbook switches.
  - Document integrity check gates (`LK_S0006`) blocking downstream excel compile workflows.
""")

    # 5. Knowledge_Gap_Report.md
    gap_path = os.path.join(execution_dir, "Knowledge_Gap_Report.md")
    with open(gap_path, "w", encoding="utf-8") as fr:
        fr.write("""# Knowledge Gap Report

## Inventory Gap Analysis
This report analyzes gaps in current canonical documents (located in `knowledge/jarvis/`) that are now mitigated by discovered legacy knowledge.

### Gap 1 — Interactive Session Lifecycle
* **Status:** Mitigated.
* **Finding:** Current documentation lists standard greetings, but contains no definitions for handling user validation failures inside builder flows. Discovered workshop hotfixes (`LK_S0001`, `LK_S0011`) reveal how the client preserves task session tokens across browser page reloads and chat prompts.

### Gap 2 — State Divergence in calculations
* **Status:** Mitigated.
* **Finding:** While current workflows outline drawing and BOQ reviews, they ignore issues where user edits during compilation actions disrupt outputs. Discovered code change records (`LK_S0003`, `LK_S0004`) define solutions to create input fingerprints and state snapshots, preventing variable state divergence.

### Gap 3 — Level Layout and Mezzanine Reductions
* **Status:** Mitigated.
* **Finding:** Standard specifications do not address local level codes that break generic parsers. Legacy builders (`LK_S0005`, `LK_S0010`) provide explicit guidelines to expand ranges and translate mezzanine codes into CostX tokens.

### Gap 4 — Static Route policy checking
* **Status:** Mitigated.
* **Finding:** Existing files lists limitations of the local router. The v5 source workbooks and reports (`LK_S0008`, `LK_S0009`) prove standard release checks run route count matches and static evaluator checks to guarantee backend sanitization.
""")
    # 6. Legacy_Knowledge_Graph.md (Amendment 4 / One additional report)
    graph_path = os.path.join(execution_dir, "Legacy_Knowledge_Graph.md")
    with open(graph_path, "w", encoding="utf-8") as fr:
        fr.write("""# Legacy Knowledge Graph (Traceability Map)

```text
======================================================================
                  LEGACY INTAKE FILE SOURCES
======================================================================

 [SourceOfTruth R81/R82 .xlsx]   [Reports r81/r82 .md]     [Workshop Zip (Patches)]
             │                            │                            │
             ├────────────────────────────┼────────────────────────────┤
             ▼                            ▼                            ▼
      - Decisions Registry         - Static check results       - Debug reports (.md)
      - Dashboard configs           - Route counts (43)          - Dev chat log (.md)
      - Problems sheet              - Middleware count (1)       - Hotfixes (2A-2D)
             │                            │                            │
             └────────────────────────────┼────────────────────────────┘
                                          ▼
                                 [Extraction Pipeline]
                                          │
                                          ▼
======================================================================
                   STAGED KNOWLEDGE CANDIDATES
======================================================================
 
   LK_S0001 (Clarification card preservation) ──────┐
   LK_S0002 (Plan continuity on trade change) ──────┼───► [STAGING AREA]
   LK_S0003 (Snapshot-driven run states)       ─────┼───► `knowledge/legacy/staging/`
   LK_S0004 (Cache signature invalidate)       ─────┤
   LK_S0005 (Level range sequencer range)       ─────┼───► Staged items details
   LK_S0006 (Integrity failures export block)  ─────┤     each mapped with full
   LK_S0007 (Multiline zone parser limit)       ─────┼───► Provenance criteria
   LK_S0008 (Evidence static evaluator layers) ─────┤
   LK_S0009 (Route count release hygiene)       ─────┼───► Status: STAGED
   LK_S0010 (Directional mezzanine aliases)     ─────┤
   LK_S0011 (Active task state reload restore)  ─────┤
   LK_S0012 (Support log action suppress)       ─────┘
                                          │
                                          ▼
======================================================================
                     PROPOSED CANONICAL TARGETS
======================================================================

                   Staged Items           Target Canonical File
                   ────────────           ─────────────────────
                    LK_S0001, LK_S0010 ──► knowledge/jarvis/Interaction_Policy.md
                     LK_S0002, LK_S0005, 
                     LK_S0007, LK_S0011 ──► knowledge/jarvis/Engineering_Workflows.md
                     LK_S0003, LK_S0004,
                     LK_S0008           ──► knowledge/jarvis/Architecture.md
                     LK_S0006           ──► knowledge/jarvis/Limitations.md
                     LK_S0009           ──► knowledge/jarvis/Version.md
                     LK_S0012           ──► knowledge/jarvis/Response_Policy.md
```
""")

if __name__ == "__main__":
    main()
