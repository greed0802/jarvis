# Knowledge Source Naming Standard

## Purpose
This document defines the naming conventions for directories and files managed under the Jarvis Knowledge Engineering boundary (`knowledge/sources/`).

These rules ensure human-readability, collision resistance, and deterministic programmatic access.

## 1. Zero Modification Principle
**Original filenames are never modified during initial ingestion or storage.**

If a file arrives named `Copy of Copy of report (final)_v2.pdf`, it remains `Copy of Copy of report (final)_v2.pdf` physically on disk. 

Renaming or semantic interpretation happens strictly within the **Knowledge Registry Metadata** mapping, never on the filesystem.

## 2. Directory Naming
Repository directories grouping knowledge sources must adhere to strict conventions.

### 2.1 Allowed Characters
- Lowercase alphanumeric characters (`a-z`, `0-9`)
- Underscores (`_`) for word separation

### 2.2 Prohibited Characters
- Spaces
- Hyphens (`-`)
- Capital letters
- Special symbols (`! @ # $ % ^ & * ( ) + = < > ? / \ | : ; " ' , . ~ \` `)

### 2.3 Structure Conventions
1. **Root Categories:** Must be plural nouns matching `KNOWLEDGE_REGISTER.md` (e.g., `projects/`, `standards/`, `councils/`).
2. **Entity Identifiers:** Must uniquely identify the logical group without spaces (`canberra_theatre/`, `glen_innes_hospital/`).

## 3. Temporary Staging
Staging directories (e.g., `knowledge_inbox/`) represent uncontrolled ingress. The files and folders within staging are not guaranteed to follow this naming standard until evaluated, registered, and promoted (copied) into `knowledge/sources/`.

## 4. Metadata Linking
To connect a cleanly named artifact to a messy physical filename, the Knowledge Registry maps:
- `Source_Path`: `knowledge/sources/projects/canberra_theatre/report 1 final.pdf`
- `Canonical_Title`: `Canberra Theatre Project Report - Final`

The `Canonical_Title` in the JSON registry is used by the system for visual display and LLM contexts, abstracting away the messy original filename while preserving exact physical provenance.