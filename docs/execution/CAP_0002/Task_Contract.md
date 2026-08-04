# Task Contract

## Purpose
Defines the immutable foundation for the Task domain object.

## Immutable Fields
- `task_id`: Unique persistent identifier.
- `created_at`: UTC timestamp of creation.
- Explicit references to parent owners as per Relationship Model.

## Behavioral Guarantees
- Immutable after initialization.
- Never directly executes business logic (pure data structure).
- State transitions (if any) require returning a new instance.

## Ownership
Strictly adheres to the hierarchical relationship model: Workspace -> Projects -> Knowledge -> Context -> Memory -> Intent -> Workflow -> Task -> Capability.

## Allowed Mutations
None. All domain objects are implemented as `@dataclass(frozen=True)`.

## Cross References
- Maintains ID-based references to parent objects.
- Does not contain full nested instances of parents (avoids circular references).

## Validation Rules
- Required fields must not be None or empty.
- IDs must follow standard Jarvis identification formats.
- Pre/Post conditions asserted in `__post_init__`.

## Additional Architecture Directives
- **Persistence:** Relational or Document storage.
- **Serialization:** Strict JSON compatibility.
- **AI Usage:** Only through explicit injection; AI never mutates this directly.
