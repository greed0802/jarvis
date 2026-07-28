# Knowledge Validation Rules

## Purpose
This document specifies the validation rules that enforce truth and determinism across the Knowledge Engineering boundary.

Every knowledge asset governed by `knowledge/registry/source_manifest.json` must continuously pass these rules. Any failure immediately disqualifies the asset from consumption capabilities.

## 1. Registry Invariants

### 1.1 Integrity Invariant
- A file matching the `path` recorded in the manifest must physically exist.
- The recalculated `SHA-256` hash of the physical file must perfectly match the `hash_sha256` value stored in the manifest.

### 1.2 Identity Invariant
- No two assets in the manifest may share the same `id`.
- IDs must follow the format `KN-\d{6}` (e.g., `KN-000001`).

### 1.3 Schema Invariant
- The manifest must parse as valid JSON.
- Every asset object must strictly conform to the fields laid out in `knowledge/governance/registry_schema.json`.

## 2. File State Invariants

### 2.1 Immutability Guard
- If a hash verification fails during routine audit, the system must immediately flag the asset as `Corrupted` and halt capability access.
- Assets may only receive a new hash if a deliberate, logged `Version Update` workflow is triggered (producing a new manifest entry or explicitly overwriting a registered version).

### 2.2 Duplication Guard
- If multiple physical paths map to the exact same `SHA-256` digest, the validation suite must emit a `.warning` indicating identical binary blobs exist in storage. The registry allows this physically, but semantic resolution should treat them as aliases of the same source.

## 3. Metadata Completeness

- Required fields (`id`, `title`, `category`, `source_path`, `hash_sha256`, `size_bytes`, `state`) must not be null or empty.
- Allowed values for `state` must equal: `Draft`, `Under Review`, `Approved`, `Archived`, or `Corrupted`.
- Allowed values for `category` must match those set in the `KNOWLEDGE_REGISTER.md`.