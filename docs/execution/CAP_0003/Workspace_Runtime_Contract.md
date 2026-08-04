# Workspace Runtime Contract

## Responsibilities
- Lifecycle management (Load, Switch, Terminate) for Workspace domain objects.
- Act as the central registry for Projects, Knowledge, and Sessions in-memory.
- Provide a strict facade for the Application to query immutable domain state.

## Ownership
- Belongs to the `Kernel` as a registered `LifecycleAware` component.
- Owns all `Manager` components (ProjectManager, SessionManager, etc.).

## Concurrency
- `asyncio` compatible; State mutations use thread-safe approaches relative to the async event loop.

## AI Independence
- Never imports AI SDKs, Providers, or Planners.
