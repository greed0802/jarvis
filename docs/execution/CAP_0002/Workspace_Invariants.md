# Workspace Invariants

1. No circular module imports.
2. Every entity is `@dataclass(frozen=True)`.
3. AI components (like GenerationPipeline) never define the Domain.
4. Domain models only contain data and validation, never execution or SDK dependencies.
