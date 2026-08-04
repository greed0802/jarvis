# PROD-0002 — Command Reference

**Date:** 2026-08-04

---

## Core Commands

### help
**Description:** Display available commands  
**Usage:** `help`  
**Output:** List of all available commands (hides developer commands in normal mode)

---

### status
**Description:** Platform status summary  
**Usage:** `status`  
**Output:**
```
Jarvis Platform Status
──────────────────────
Version              : 0.0.1-alpha.17
Platform State       : running
Workspace            : (none) or <workspace-name>
Workspaces           : <count>
Knowledge Items      : <count>
Capabilities         : <count>
Memory Entries       : <count>
Artifacts            : <count>
```

---

### version
**Description:** Platform version manifest  
**Usage:** `version`  
**Output:**
```
Version Manifest
────────────────
Platform  : 0.0.1-alpha.17
Kernel    : 1.0
Shell     : 1.0
```

---

### clear
**Description:** Clear terminal screen  
**Usage:** `clear`  
**Notes:** Calls `cls` on Windows, `clear` on Unix

---

### exit
**Description:** Shutdown the platform gracefully  
**Usage:** `exit`  
**Output:** `Shutting down Jarvis Platform...`

---

## Workspace Commands

### create-workspace
**Description:** Create a new workspace  
**Usage:** `create-workspace <name>`  
**Example:** `create-workspace MyProject`  
**Output:** `[OK] Workspace 'MyProject' created and activated. (id: ws-myproject)`  
**Notes:** Auto-activates the new workspace

---

### open-workspace
**Description:** Set the active workspace  
**Usage:** `open-workspace <name>`  
**Example:** `open-workspace MyProject`  
**Output:** `[OK] Workspace 'MyProject' is now active.`  
**Error:** `[Error] Workspace 'X' not found. Use 'list-workspaces' to see available workspaces.`

---

### list-workspaces
**Description:** List all workspaces  
**Usage:** `list-workspaces`  
**Output:** Table with columns: ID, Name, Created  
**Notes:** Active workspace marked with `*`

---

### workspace
**Description:** Show active workspace details  
**Usage:** `workspace`  
**Output:**
```
Active Workspace
────────────────
ID       : ws-myproject
Name     : MyProject
Created  : 2026-08-04T13:00:00
```
**Error:** `No active workspace. Use 'create-workspace <name>' or 'open-workspace <name>' first.`

---

## Knowledge & Artifact Commands

### upload
**Description:** Upload and register a document  
**Usage:** `upload <path>`  
**Example:** `upload /path/to/document.pdf`  
**Output:**
```
Document Registered
───────────────────
artifact_id     : art-1
name            : document.pdf
type            : GENERAL_DOCUMENT
size_bytes      : 12345
content_hash    : abc123...
knowledge_id    : ki-art-1
```
**Errors:**
- `[Error] File not found: /path/to/file`
- `[Error] No active workspace. Open or create a workspace first.`

**Supported Types:**
- `.pdf`, `.doc`, `.docx`, `.txt`, `.md` → GENERAL_DOCUMENT
- `.xlsx`, `.xls`, `.csv` → BOQ
- `.dwg`, `.dxf` → DRAWING
- `.png`, `.jpg`, `.jpeg` → IMAGE

---

### list-documents
**Description:** List knowledge items  
**Usage:** `list-documents`  
**Output:** Table with columns: ID, Resource, Added

---

### artifacts
**Description:** List registered artifacts  
**Usage:** `artifacts`  
**Output:** Table with columns: ID, Name, Type, Versions

---

## Conversation & Execution Commands

### ask
**Description:** Ask the workspace assistant a question  
**Usage:** `ask "<question>"`  
**Example:** `ask "What is Jarvis?"`  
**Output:**
```
Assistant
─────────
<AI-generated response>
```
**Notes:** Uses AIRuntime (mocked response in current implementation)

---

### summarize
**Description:** Summarize workspace context  
**Usage:** `summarize`  
**Output:**
```
Summary
───────
<AI-generated summary>
```

---

### run
**Description:** Execute a registered capability  
**Usage:** `run <capability>`  
**Example:** `run BOQIntelligence`  
**Output:**
```
Capability: BOQIntelligence
───────────────────────────
status  : SUCCESS
output  : {...}
```
**No Args:** Lists available capabilities with descriptions  
**Error:** `[Error] Capability 'X' not discovered.`

---

### memory
**Description:** Show workspace memory entries  
**Usage:** `memory`  
**Output:** Table with columns: ID, Category, Created  
**Notes:** Includes shell history entries

---

## Developer Commands

*(Visible only with `python main.py --developer`)*

### debug runtime
**Description:** Show runtime internal state  
**Usage:** `debug runtime`  
**Output:**
```
Runtime Debug
─────────────
Kernel State  : running
Components    : 11
Services      : 1
```

---

### debug planner
**Description:** Show planner configuration  
**Usage:** `debug planner`  
**Output:** Lists registered capabilities and their descriptions

---

### debug memory
**Description:** Show memory graph details  
**Usage:** `debug memory`  
**Output:**
```
Memory Debug
────────────
Entries      : 5
Graph Nodes  : 5
Graph Edges  : 0
```

---

### debug capabilities
**Description:** Show capability registry  
**Usage:** `debug capabilities`  
**Output:** Table with columns: Name, Description, Input Schema

---

### debug knowledge
**Description:** Show knowledge engine state  
**Usage:** `debug knowledge`  
**Output:**
```
Knowledge Engine Debug
──────────────────────
Source Registry   : SourceRegistry
Parser Registry   : ParserRegistry
Normalizer        : DocumentNormalizer
Validator         : KnowledgeValidator
```
