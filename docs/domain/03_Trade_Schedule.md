# Trade Schedule

**Version:** 1.0  
**Status:** Approved  
**Last Updated:** 2026-07-14  
**Owner:** Project Owner  
**Approvers:** Project Owner

---

## Purpose

This document defines trade schedule rules and standard trade sequences for Bill of Quantities preparation. Trade schedules organize work into logical sections following industry conventions and client preferences.

This is the **Domain Source of Truth** for trade organization.

## Scope

This document covers:

- Office standard trade schedules
- Trade schedule precedence rules
- Commercial vs residential sequences
- Client-specific trade schedule handling
- Extensibility for new requirements

---

## Authority

This document records office standard trade sequences.

**It does not supersede:**

- Contract-Specified Trade Schedules
- Client-Preferred Trade Schedules
- Project-Specific Requirements

**Priority Hierarchy:**

```
Contract-Mandated Trade Schedule
↓
Client-Specific Trade Schedule
↓
Office Standard Trade Schedule (this document)
↓
Default Sequence
```

**Principle:** Client requirements always override office standards.

---

## Capability Consumers

**Current Consumers:**
- Parser (reads any trade sequence)
- BOQ Intelligence (recognizes trade organization patterns)

**Planned Consumers:**
- Formatter (will apply trade sequence during formatting)
- CheckMate (will validate trade completeness)

**Future Consumers:**
- To be determined based on capability development

---

## Definitions

**Trade Schedule**: An ordered list of work sections (trades) defining the standard sequence for organizing BOQ content.

**Hierarchy Level 1 Section**: A top-level BOQ section, typically corresponding to a trade in the trade schedule.

**Office Standard**: The default trade schedule used when no client-specific schedule exists.

**Client Schedule**: A trade schedule specified or preferred by a particular client.

**Elemental Trade Schedule**: An alternative organization grouping by building element rather than construction trade.

---

## Trade Schedule Selection

**Standard:** Trade schedules shall be selected in the following precedence order:

```
1. Client-Specific Trade Schedule (highest priority)
   ↓
2. Project Type Office Standard (Commercial or Residential)
   ↓
3. Generic Office Standard
   ↓
4. Default Sequence (fallback)
```

**Procedure:**

1. Check if client has specified trade schedule
2. If yes, use client trade schedule exactly
3. If no, determine project type (commercial/residential)
4. Use appropriate office standard trade schedule
5. Document which schedule is being used in project files

**Provenance:** Office practice for client management

---

## Office Standard Trade Schedule (Commercial)

**Standard:** The following is the office standard trade schedule for commercial projects.

**Source:** `docs/reference/office_standards/standard_trade_schedule.xlsx`

**Standard Commercial Sequence:**

1. **PRELIMINARIES**
2. **DEMOLITION**
3. **EARTHWORKS**
4. **PILING**
5. **CONCRETE**
6. **FORMWORK**
7. **REINFORCEMENT**
8. **POST TENSIONING**
9. **PRECAST CONCRETE**
10. **STRUCTURAL STEEL & STRUCTURAL TIMBER**
11. **MASONRY & RENDER**
12. **ROOFING**
13. **EXTERNAL CLADDING**
14. **WALLS**
15. **CEILINGS**
16. **ALUMINIUM WINDOWS & DOORS**
17. **DOORS AND HARDWARE**
18. **TILING AND STONE**
19. **CARPET**
20. **RESILIENT FINISH**
21. **PAINTING AND WALL FINISHES**
22. **METALWORK**
23. **CARPENTRY**
24. **JOINERY**
25. **FIXTURES, FITTINGS AND EQUIPMENT**
26. **SIGNAGE**
27. **HYDRAULIC SERVICES**
28. **FIRE SERVICES**
29. **MECHANICAL SERVICES**
30. **ELECTRICAL SERVICES**
31. **LIFTS AND ESCALATORS**
32. **CIVIL WORKS**
33. **LANDSCAPING**

**Notes:**

- This sequence follows typical construction sequence
- Logical progression from demolition through to completion
- Services typically grouped together
- External works and landscaping at end
- Some trades may be combined or split based on project scope

**Provenance:** `docs/reference/office_standards/standard_trade_schedule.xlsx`

---

## Office Standard Trade Schedule (Residential)

**Standard:** The following is the office standard trade schedule for residential projects.

**Source:** `docs/reference/office_standards/standard_trade_schedule_residential.xlsx`

**Standard Residential Sequence:**

1. **PRELIMINARIES**
2. **DEMOLITION**
3. **CIVIL WORKS**
4. **PILING**
5. **CONCRETE**
6. **FORMWORK**
7. **REINFORCEMENT**
8. **POST TENSIONING**
9. **PRECAST CONCRETE**
10. **WATERPROOFING**
11. **STRUCTURAL STEEL**
12. **ALUMINIUM WINDOWS & DOORS**
13. **MASONRY & RENDER**
14. **ROOFING**
15. **EXTERNAL CLADDING**
16. **METALWORK**
17. **CARPENTRY**
18. **WALLS AND CEILINGS**
19. **DOORS AND HARDWARE**
20. **GLAZING**
21. **TILING AND STONE**
22. **JOINERY**
23. **FLOOR COVERINGS**
24. **FIXTURES, FITTINGS AND EQUIPMENT**
25. **PAINTING AND WALL FINISHES**
26. **SIGNAGE**
27. **HYDRAULIC SERVICES**
28. **FIRE SERVICES**
29. **MECHANICAL SERVICES**
30. **ELECTRICAL SERVICES**
31. **LIFTS AND ESCALATORS**
32. **EXTERNAL FINISHES**
33. **LANDSCAPING**

**Notes:**

- Simplified sequence compared to commercial
- Emphasis on domestic construction sequence
- Services less complex
- External works typically smaller scope
- Some trades may not apply to all residential projects

**Provenance:** `docs/reference/office_standards/standard_trade_schedule_residential.xlsx`

---

## Elemental Trade Schedule

**Standard:** Alternative organization grouping by building element.

**Source:** `docs/reference/office_standards/standard_trade_schedule.xlsx` (Elemental Trade Schedule sheet)

**Elemental Sequence:**

1. **MASONRY**
2. **METALWORKS**
3. **WATERPROOFING**
4. **ROOFING**
5. **FAÇADE**
6. **DOORS & INTERNAL WINDOWS**
7. **INTERNAL WALLS**
8. **CEILINGS**
9. **FLOOR FINISHES**
10. **WALL FINISHES**
11. **SIGNAGE**
12. **FFE**
13. **JOINERY**
14. **LANDSCAPING WORKS**

**Use Case:** Typically used for fit-out projects or when client prefers elemental organization.

**Provenance:** `docs/reference/office_standards/standard_trade_schedule.xlsx`

---

## Client-Specific Trade Schedules

**Standard:** Client-specific trade schedules take precedence over office standards.

**Procedure:**

1. **Identify Client Requirements**
   - Check client documentation
   - Review previous projects for same client
   - Confirm with client if unclear

2. **Document Client Schedule**
   - Store in project files
   - Reference in workbook preambles
   - Note deviations from office standard

3. **Apply Client Schedule**
   - Use client sequence exactly as specified
   - Do not "improve" or "standardize" client preferences
   - Maintain client terminology

4. **Validate Against Client Schedule**
   - Ensure all client-required trades included
   - Follow client numbering/naming conventions
   - Verify completeness per client standards

**Provenance:** Office practice for client management

**Severity:**
- Missing client-required trade: **Error**
- Non-standard trade sequence (when client specifies): **Warning**

---

## Trade Schedule Extensibility

**Standard:** New client-specific schedules can be documented without requiring system changes.

**Documentation Pattern:**

When a client requires a specific trade schedule:
1. Document the schedule in project files
2. Note deviations from office standard
3. Apply consistently across all projects for that client
4. Update if client requirements change

This allows:
- Client-specific knowledge to be preserved
- Consistency across client projects
- No system modifications needed

**Provenance:** Platform extensibility principles

---

## Rule Provenance

| Rule ID | Rule | Source | Document |
|---------|------|--------|----------|
| TS-001 | Client schedule precedence | Office Practice | Client management |
| TS-002 | Commercial standard sequence | Office Standard | standard_trade_schedule.xlsx |
| TS-003 | Residential standard sequence | Office Standard | standard_trade_schedule_residential.xlsx |
| TS-004 | Elemental organization | Office Standard | standard_trade_schedule.xlsx |
| TS-005 | Client schedule extensibility | Platform Principle | Extensibility design |

---

## References

### Internal Documents
- `docs/domain/01_QS_Office_Standards.md` - Quality requirements
- `docs/domain/02_BOQ_Structure.md` - BOQ hierarchy (Hierarchy Level 1 corresponds to trades)
- `docs/domain/07_Client_Conventions.md` - Client-specific requirements

### Office Standards
- `docs/reference/office_standards/standard_trade_schedule.xlsx` - Commercial and elemental
- `docs/reference/office_standards/standard_trade_schedule_residential.xlsx` - Residential

---

## Related Documents

- **Upstream:** `docs/domain/07_Client_Conventions.md` - Authority precedence
- **Peer:** `docs/domain/02_BOQ_Structure.md` - Structural organization
- **Downstream:** All BOQ construction and formatting activities

---

## Document Control

**Change History:**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-01-15 | Project Owner | Initial scaffold |
| 1.0 | 2026-07-14 | Project Owner | Expanded with all standard schedules, precedence rules, and evidence-based consumer model |

**Review Schedule:** Annual or upon addition of new client-specific schedules

**Distribution:** All quantity surveying staff, Jarvis Platform

---

## TODO

- [ ] TODO(Project Owner): Document trade schedule for top 3 recurring clients
- [ ] TODO(Project Owner): Define procedure for handling hybrid trade schedules (partial client, partial office)
- [ ] TODO(Project Owner): Establish rules for trade consolidation in small projects
- [ ] TODO(Project Owner): Document when Elemental schedule is preferred over Trade schedule
- [ ] TODO(Project Owner): Create examples of client-specific trade schedule variations