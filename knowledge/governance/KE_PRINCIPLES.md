# Knowledge Engineering Principles

## Purpose

This document defines the governing principles for the Knowledge Engineering (KE) workstream.

Knowledge Engineering is responsible for the deterministic acquisition, organization, governance, and future consumption of engineering knowledge within the Jarvis repository.

These principles apply to all knowledge assets managed under the `knowledge/` repository.

---

# Core Principles

1. **Raw Documents Remain Immutable**

   Original source documents shall never be modified.

2. **Original Filenames Are Preserved**

   Source filenames are retained exactly as acquired to preserve provenance and traceability.

3. **Repository Organization Is Structural**

   Knowledge is organized through repository structure and metadata rather than renaming source material.

4. **Knowledge Is Deterministic**

   Identical inputs shall produce identical repository organization and governance outcomes wherever practical.

5. **Knowledge Is Evidence-Driven**

   Approved knowledge shall be supported by traceable evidence derived from original source material.

6. **Knowledge Is Version Controlled**

   All governance documentation, metadata, and approved knowledge artifacts shall be maintained under version control.

7. **Knowledge Acquisition Is Independent of Capability Engineering**

   Acquiring, organizing, and governing knowledge shall never directly modify production capabilities or architecture.

---

# Separation of Responsibilities

Knowledge Engineering and Capability Engineering are complementary but independent disciplines.

- **Knowledge Engineering** governs engineering knowledge.
- **Capability Engineering** implements production capabilities.

Knowledge Engineering provides curated, reviewable knowledge that future capabilities may consume, but does not implement those capabilities.

---

# Repository Model

The repository distinguishes between:

- **Sources** — Original immutable documents.
- **Evidence** — Validated observations derived from sources.
- **Ontology** — Future structured representations of approved knowledge.

This separation preserves provenance, supports deterministic governance, and enables future capability consumption without altering original source material.