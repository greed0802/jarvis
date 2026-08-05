# Document Relationship Model

Defines the structure of the document tracing relationships representation.

## Directional Mappings
* **`supersedes`:** Links document revisions (e.g. `doc-art2` supersedes `doc-art1`). Triggers recommendations for outdated files.
* **`governs`:** A `Specification` governs matching files in the active workspace.
* **`supports`:** A `Drawing` (Architectural/Structural/Civil/Services Layouts) supports a `BOQ` to establish quantity takeoff backing.
* **`validates`:** A QA `Checklist` validates a `BOQ` to verify items calculations.
