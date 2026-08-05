# Legacy Knowledge Graph (Traceability Map)

```text
======================================================================
                  LEGACY INTAKE FILE SOURCES
======================================================================

 [SourceOfTruth R81/R82 .xlsx]   [Reports r81/r82 .md]     [Workshop Zip (Patches)]
             │                            │                            │
             ├────────────────────────────┼────────────────────────────┤
             ▼                            ▼                            ▼
      - Decisions Registry         - Static check results       - Debug reports (.md)
      - Dashboard configs           - Route counts (43)          - Dev chat log (.md)
      - Problems sheet              - Middleware count (1)       - Hotfixes (2A-2D)
             │                            │                            │
             └────────────────────────────┼────────────────────────────┘
                                          ▼
                                 [Extraction Pipeline]
                                          │
                                          ▼
======================================================================
                   STAGED KNOWLEDGE CANDIDATES
======================================================================
 
   LK_S0001 (Clarification card preservation) ──────┐
   LK_S0002 (Plan continuity on trade change) ──────┼───► [STAGING AREA]
   LK_S0003 (Snapshot-driven run states)       ─────┼───► `knowledge/legacy/staging/`
   LK_S0004 (Cache signature invalidate)       ─────┤
   LK_S0005 (Level range sequencer range)       ─────┼───► Staged items details
   LK_S0006 (Integrity failures export block)  ─────┤     each mapped with full
   LK_S0007 (Multiline zone parser limit)       ─────┼───► Provenance criteria
   LK_S0008 (Evidence static evaluator layers) ─────┤
   LK_S0009 (Route count release hygiene)       ─────┼───► Status: STAGED
   LK_S0010 (Directional mezzanine aliases)     ─────┤
   LK_S0011 (Active task state reload restore)  ─────┤
   LK_S0012 (Support log action suppress)       ─────┘
                                          │
                                          ▼
======================================================================
                     PROPOSED CANONICAL TARGETS
======================================================================

                   Staged Items           Target Canonical File
                   ────────────           ─────────────────────
                    LK_S0001, LK_S0010 ──► knowledge/jarvis/Interaction_Policy.md
                     LK_S0002, LK_S0005, 
                     LK_S0007, LK_S0011 ──► knowledge/jarvis/Engineering_Workflows.md
                     LK_S0003, LK_S0004,
                     LK_S0008           ──► knowledge/jarvis/Architecture.md
                     LK_S0006           ──► knowledge/jarvis/Limitations.md
                     LK_S0009           ──► knowledge/jarvis/Version.md
                     LK_S0012           ──► knowledge/jarvis/Response_Policy.md
```
