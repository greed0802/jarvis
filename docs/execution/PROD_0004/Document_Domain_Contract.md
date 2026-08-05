# Document Domain Contract

Defines the core logical properties and types constituting the canonical Document Intelligence Layer.

## Domain Schemas

### 1. Document
* `document_id`: Unique identifier (e.g. `doc-art123`).
* `workspace_id`: Active workspace key.
* `name`: Display path filename.
* `classification`: `DocumentClassification` type.
* `lifecycle`: `DocumentLifecycle` status.
* `metadata`: Nested `DocumentMetadata` properties.
* `relationships`: List of connections.
* `recommendations`: Action items.

### 2. DocumentClassification (Enum)
Target classifications: Architectural Drawing, Structural Drawing, Civil Drawing, Services Drawing, Specification, BOQ, Checklist, Schedule, Image, Photo, Spreadsheet, Calculation, Report, Email, Archive, Unknown.

### 3. DocumentLifecycle (Enum)
Transition lifecycle stages: Uploaded -> Registered -> Classified -> Parsed -> Indexed -> Linked -> Validated -> Ready -> Archived.
