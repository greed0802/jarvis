# Knowledge Engineering

## Purpose

The **Knowledge Engineering (KE)** workstream establishes the governance, organization, and lifecycle of engineering knowledge within the Jarvis repository.

Knowledge Engineering is a permanent engineering discipline alongside Capability Engineering.

- **Capability Engineering** builds production capabilities.
- **Knowledge Engineering** curates the engineering knowledge that future capabilities consume.

This repository area is a first-class repository component equivalent to `src/`, `docs/`, `tests/`, and `tools/`.

This area does **not** contain production code.

---

# Repository Principles

Knowledge Engineering follows these principles:

1. Raw documents remain immutable.
2. Original filenames are preserved.
3. Repository organization is provided by folders and metadata.
4. Knowledge is deterministic.
5. Knowledge is evidence-driven.
6. Knowledge is version controlled.
7. Knowledge acquisition never directly modifies production capabilities.

---

# Knowledge Lifecycle

```
Acquire

↓

Inventory

↓

Normalize

↓

Review

↓

Discovery

↓

Evidence

↓

Knowledge Base

↓

Capability Consumption
```

This lifecycle governs the evolution of repository knowledge while preserving complete traceability from original sources through validated evidence to future capability consumption.

---

# Repository Structure

```
knowledge/
├── README.md
├── registry/
├── sources/
│   ├── standards/
│   ├── councils/
│   ├── specifications/
│   ├── reports/
│   └── projects/
├── evidence/
├── glossary/
├── ontology/
└── governance/
```

## Directory Responsibilities

### sources/

Contains original, immutable source documents.

No document shall be modified or renamed after acquisition.

### registry/

Contains the Knowledge Register and future metadata describing repository knowledge assets.

### evidence/

Contains validated observations and discovery outputs derived from source material.

### glossary/

Contains approved engineering terminology.

### ontology/

Reserved for future structured knowledge representations.

### governance/

Contains Knowledge Engineering policies, lifecycle definitions, and repository governance documentation.

---

# Initial Knowledge Categories

The initial categories are:

- ANZSMM
- Australian Standards
- National Construction Code (NCC)
- Council Specifications
- Engineering Specifications
- Engineering Reports
- Historical Projects
- Glossary
- Future Knowledge

These categories establish repository organization only. They are intentionally unpopulated as part of KE-0001.

---

# Inventory Policy

Knowledge acquisition follows these rules:

- Preserve original filenames.
- Preserve original documents.
- Organize using repository structure.
- Provide discoverability through metadata.
- Never overwrite or edit original source material.
- Maintain deterministic and reviewable provenance for every knowledge asset.

---

# Scope

KE-0001 establishes repository governance only.

The following are explicitly out of scope:

- OCR
- PDF parsing
- AI extraction
- Ontology generation
- Concept extraction
- Embeddings
- Search engines
- Vector databases
- Production capability implementation

These activities are introduced in future Knowledge Engineering work.

---

# Future Roadmap

- KE-0001 — Knowledge Engineering Foundation
- KE-0002 — Knowledge Register
- KE-0003 — ANZSMM Pilot Ingestion
- KE-0004 — Council Specification Pilot
- KE-0005 — Historical Project Corpus
- KE-0006 — Engineering Report Corpus
- KE-0007 — Knowledge Discovery
- KE-0008 — Knowledge Consumption API