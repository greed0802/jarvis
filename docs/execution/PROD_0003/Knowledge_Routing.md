# Knowledge Routing — PROD-0003

## Deterministic Routing

User queries are classified by `IntentSemantics` and routed through an ordered
`ResolverChain`.

## Routing Table

| User Query | Intent Semantics | Resolver | Deterministic? |
|------------|-----------------|----------|----------------|
| What project am I working on? | QUERY / Project / Describe | WorkspaceResolver | Yes |
| List uploaded files | QUERY / Artifact / List | ArtifactResolver | Yes |
| What documents exist? | QUERY / Artifact / List | ArtifactResolver | Yes |
| What knowledge items exist? | QUERY / Knowledge / List | KnowledgeResolver | Yes |
| What capabilities exist? | QUERY / Capability / List | CapabilityResolver | Yes |
| What is in memory? | QUERY / Memory / List | MemoryResolver | Yes |
| Run BOQ Intelligence | EXECUTE / Capability / Run | CapabilityResolver | Yes (capability) |
| Summarize workspace | SUMMARIZE / Workspace / Describe | AIResolver | No (AI) |

## Fallback

When no keyword/semantic match exists, `AIResolver` (always resolves) activates
with full GroundingEngine context.