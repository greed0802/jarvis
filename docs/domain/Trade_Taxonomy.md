# Trade Taxonomy

Version: 1.0

---

## Approval Metadata

| Field | Value |
|-------|-------|
| **Status** | Approved |
| **Owner** | Project Owner (QS Authority) |
| **Effective** | 2026-07-22 |
| **Supersedes** | None |
| **Sprint Reference** | CB-0003 |

---

## Purpose

This document defines the trade classification taxonomy for BOQ items in the Jarvis Platform.

A trade is a category of construction work that groups related BOQ items for cost analysis, reporting, and cross-project comparison.

This taxonomy governs how items are classified by trade.

---

## Trade Hierarchy

Trades are organized as a flat list at this level.

Future expansion may introduce sub-trades, but YAGNI applies — no sub-trade structure is defined until multiple consumers require it.

```
Trade
  └── Sub-trade (future, not yet defined)
```

---

## Trade Definitions

### STR — Structural

**Scope:** Load-bearing elements, foundations, framing, concrete works, steelwork, and structural masonry.

**Boundaries:**
- Includes: foundations, columns, beams, slabs, walls (load-bearing), stairs, structural steel, reinforcement, formwork, precast concrete.
- Excludes: finishes applied to structural elements (see FIN), excavation for foundations (see CIV), structural timber (see TIM).
- Excludes: non-load-bearing partitions (see ARC — included in Architectural).

**Examples:**
- RC columns and beams
- Steel roof trusses
- Reinforced concrete slabs
- Foundation excavation and backfill
- Formwork to beams and columns

**Explicit Exclusions:**
- Plaster and rendering on structural walls → FIN
- Waterproofing to foundations → FIN
- Structural timber → TIM

**Authority:** Project Owner / QS practice standard.

---

### ARC — Architectural

**Scope:** Non-load-bearing building elements, finishes, joinery, doors, windows, roofing, cladding, partitions, ceilings, and fixtures.

**Boundaries:**
- Includes: masonry (non-load-bearing), blockwork, brickwork, plasterboard partitions, suspended ceilings, roofing (tiles, metal sheet), cladding, doors, windows, ironmongery, kitchen fittings, sanitaryware, signage, glazing, balustrades, handrails.
- Excludes: structural load-bearing walls (see STR), structural glazing (consult structural engineer), MEP elements (see MEC, ELE, PLU).
- Excludes: external works (see CIV).

**Examples:**
- Internal blockwork partitions
- Suspended ceiling systems
- Metal roof cladding
- Timber doors and ironmongery
- Kitchen joinery and benchtops
- Sanitary fittings and accessories

**Explicit Exclusions:**
- Load-bearing brick walls → STR
- Roof structure (trusses) → STR
- External paving → CIV

**Authority:** Project Owner / QS practice standard.

---

### MEC — Mechanical

**Scope:** HVAC, ventilation, air conditioning, mechanical ventilation, smoke extraction, and building services mechanical systems.

**Boundaries:**
- Includes: ductwork, air handling units, fans, chillers, boilers, radiators, underfloor heating, mechanical ventilation, smoke control systems, insulation of mechanical services.
- Excludes: electrical systems (see ELE), plumbing (see PLU), fire protection (see FIR).
- Excludes: structural supports for mechanical equipment (see STR).

**Examples:**
- Air handling units and ductwork
- Radiators and underfloor heating
- Mechanical ventilation systems
- Chillers and cooling towers
- Insulation of mechanical services

**Explicit Exclusions:**
- Electrical switchboards → ELE
- Fire sprinklers → FIR
- Pipework for plumbing → PLU

**Authority:** Project Owner / QS practice standard.

---

### ELE — Electrical

**Scope:** Power distribution, lighting, switchboards, cabling, containment, earthing, security systems, data/communications, and building automation.

**Boundaries:**
- Includes: main switchboards, sub-distribution boards, cabling, cable trays, conduits, trunking, lighting fixtures, emergency lighting, security alarms, CCTV, intercoms, data cabling, fire alarm systems, building management systems, earthing and bonding.
- Excludes: mechanical systems (see MEC), plumbing (see PLU), fire sprinklers (see FIR).
- Excludes: structural supports for electrical equipment (see STR).

**Examples:**
- Main distribution board and sub-boards
- Lighting and emergency lighting
- Power outlets and switch sockets
- Security alarm and CCTV systems
- Data cabling and network equipment

**Explicit Exclusions:**
- Ductwork → MEC
- Water pipework → PLU
- Fire detection / alarm → FIR (cross-category; may be ELE or FIR depending on office standard)

**Authority:** Project Owner / QS practice standard.

---

### PLU — Plumbing

**Scope:** Water supply, sanitation, drainage, hot water systems, gas supply, and above-ground / below-ground drainage.

**Boundaries:**
- Includes: cold and hot water supply pipework, sanitary pipework, soil and waste pipes, rainwater drainage, gutters and downpipes, water storage tanks, hot water cylinders, gas pipework, pumps, valves, and fittings.
- Excludes: sanitary fixtures (see ARC), mechanical heating systems (see MEC), fire sprinkler systems (see FIR).
- Excludes: external drainage beyond the building line (see CIV).

**Examples:**
- Copper water supply pipework
- PVC soil and waste pipes
- Rainwater downpipes and gutters
- Hot water cylinders
- Gas supply pipework
- Water storage tanks

**Explicit Exclusions:**
- Sanitaryware → ARC
- Boilers and radiators → MEC
- External drainage → CIV

**Authority:** Project Owner / QS practice standard.

---

### FIR — Fire Protection

**Scope:** Fire detection, alarm, suppression, sprinklers, smoke control (mechanical), passive fire protection, and fire-stopping.

**Boundaries:**
- Includes: fire alarm systems, smoke detectors, heat detectors, manual call points, sprinkler systems, fire hydrants, hose reels, fire extinguishers, fire-stopping, cavity barriers, intumescent coatings, passive fire protection.
- Excludes: structural fire resistance (see STR — inherent in structural design), fire-rated glazing (see ARC), mechanical smoke control (see MEC — overlaps; classify by system primary function).
- Note: Fire alarm systems may also fall under ELE depending on office standard. The primary function (fire detection vs. electrical supply) determines classification.

**Examples:**
- Fire alarm control panel and detectors
- Sprinkler system pipework and heads
- Fire extinguishers and hose reels
- Fire-stopping at service penetrations
- Intumescent paint to steelwork

**Explicit Exclusions:**
- Structural fire rating → STR
- Mechanical smoke extract → MEC
- Emergency lighting → ELE

**Authority:** Project Owner / QS practice standard.

---

### CIV — Civil / External Works

**Scope:** Site works, earthworks, external drainage, roads, paths, landscaping, retaining walls, fencing, and external services.

**Boundaries:**
- Includes: site clearance, earthworks, bulk excavation, retaining walls (external), roads, pavements, kerbs, drainage beyond building line, manholes, culverts, fencing, gates, landscaping, planting, irrigation, external lighting, external water and gas supply.
- Excludes: building foundations (see STR), sanitary plumbing within building (see PLU), architectural landscaping features (see ARC when integrated with building).
- Excludes: external finishes to building (see FIN).

**Examples:**
- Site clearance and bulk earthworks
- External drainage and manholes
- Road pavements and kerbs
- Fencing and gates
- Landscaping and planting

**Explicit Exclusions:**
- Building foundations → STR
- Internal drainage → PLU
- External building cladding → ARC

**Authority:** Project Owner / QS practice standard.

---

### FIN — Finishes

**Scope:** Internal and external finishes applied to building elements: plaster, rendering, tiling, painting, flooring, wall coverings, waterproofing, and decorative coatings.

**Boundaries:**
- Includes: plastering, rendering, screeding, tiling (floor and wall), painting, varnishing, wallpaper, vinyl flooring, carpet, timber flooring, waterproofing membranes, sealants, expansion joint covers.
- Excludes: structural finishes (e.g. fair-face concrete — inherent in STR), façade cladding systems (see ARC), sanitary fixtures (see ARC).
- Note: Waterproofing to basements is classified under FIN; waterproofing to roofs falls under ARC (roofing) unless it is a separate applied membrane.

**Examples:**
- Plaster and skim coat to walls
- Ceramic wall and floor tiling
- Paint to walls and ceilings
- Vinyl flooring
- Waterproofing to wet areas

**Explicit Exclusions:**
- Fair-face concrete → STR
- Roof cladding → ARC
- Sanitaryware → ARC

**Authority:** Project Owner / QS practice standard.

---

### TIM — Timber

**Scope:** Structural timber, timber framing, glulam, CLT, timber decking, and timber treatments.

**Boundaries:**
- Includes: structural timber framing, roof timbers, trusses (timber), glulam beams, cross-laminated timber (CLT), timber decking (structural), timber treatment, preservatives, timber connectors.
- Excludes: architectural timber (joinery, doors, window frames — see ARC), timber flooring (see FIN), formwork timber (temporary works — STR or separate).
- Excludes: external timber decking (non-structural — see ARC or CIV based on location).

**Examples:**
- Timber roof trusses
- Glulam columns and beams
- CLT wall and floor panels
- Timber decking (structural)
- Timber treatment and preservative

**Explicit Exclusions:**
- Timber windows → ARC
- Timber flooring → FIN
- Formwork timber → STR (temporary works)

**Authority:** Project Owner / QS practice standard.

---

## Classification Rules

1. Each BOQ Item is assigned to exactly one trade.
2. Classification is based on the item's primary function, not its location or material alone.
3. When an item could belong to multiple trades, use the following priority:
   - **Safety/structural** > **MEP** > **Finishes** > **Architectural**
   - Example: Fire-rated downlight → FIR (safety primary), not ELE.
4. Cross-trade items (e.g. a combined MEP support bracket) are classified by the primary trade of the system they serve.
5. When the trade is ambiguous, classify as ARC (default).

---

## Authority

This taxonomy is approved by the Project Owner based on:

- Standard QS practice conventions
- Office standards documented in `docs/domain/02_BOQ_Structure.md`
- Professional quantity surveying methodology

Changes to this taxonomy require Project Owner approval.

---

## Future Expansion

- Sub-trades may be added when a consumer (e.g. CheckMate, Formatter) requires finer granularity.
- New trades may be added when evidence demonstrates items that cannot be classified under existing trades.

---

## Document History

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-07-22 | Initial trade taxonomy. 9 trades defined. Sprint CB-0003. |