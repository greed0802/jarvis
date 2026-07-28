# Knowledge Inventory Policy

## Purpose

This policy defines how engineering knowledge is acquired, organized, and governed within the `knowledge/` repository.

KE-0001 establishes repository governance only. No knowledge assets are inventoried as part of this task.

---

# Inventory Principles

Knowledge inventory shall follow these mandatory rules:

1. Original source documents remain immutable.
2. Original filenames shall never be changed.
3. Repository organization is achieved through folders and metadata.
4. Inventory metadata shall never replace or alter the original document.
5. Every knowledge asset shall remain traceable to its original source.
6. Inventory processes shall be deterministic and reviewable.

---

# Source Document Policy

Source documents are stored under:

```
knowledge/sources/
```

The `sources/` hierarchy represents collected material only.

It is not interpreted, modified, or normalized.

Examples include:

- ANZSMM
- Australian Standards
- NCC
- Council Specifications
- Engineering Specifications
- Engineering Reports
- Historical Projects

---

# Metadata Policy

Discoverability is provided through metadata rather than file manipulation.

Knowledge metadata may include:

- Identifier
- Category
- Source
- Authority
- Version
- Status
- Review State
- OCR Requirement
- Notes

Metadata must never alter the original source document.

---

# Provenance

Every knowledge asset shall preserve complete provenance from acquisition through future capability consumption.

The repository distinguishes between:

- **Sources** — Original immutable documents.
- **Evidence** — Validated observations derived from sources.
- **Knowledge Base** — Approved, governed knowledge.
- **Capabilities** — Consumers of approved knowledge.

Each stage shall remain independently reviewable and traceable.

---

# Out of Scope

This policy does not authorize:

- OCR
- PDF parsing
- AI extraction
- Document rewriting
- Automatic classification
- Ontology generation
- Embedding generation
- Production capability implementation

These activities are reserved for future Knowledge Engineering work.