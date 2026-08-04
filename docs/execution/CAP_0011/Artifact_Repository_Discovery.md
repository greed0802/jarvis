# Artifact Repository Discovery

## Structure & Existing Artifacts
- **Evidence Storage:** Physical directories inside `Workspace` path hold basic cost elements.
- **Memory Integration:** `WorkspaceMemoryService` saves logs and status elements, but doesn't have an asset manager tracking binary artifacts, hashes, extensions, and versions.

## Strategy
Create `ArtifactRepository` adjacent to `WorkspaceMemoryService`. Define standard `Artifact` entities. Cascade execution traces directly to automatically register output artifacts dynamically.
