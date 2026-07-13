> **Historical Reference — ADR-0025**
>
> This design document records the Observation Runtime proposal developed during
> the M6 engineering cycle.
>
> ADR-0025 (2026-07-11) evaluated this proposal and concluded that the Observation
> Runtime would **not be adopted as the active production architecture for the
> current CostX acquisition scope**.
>
> This document is retained as a historical engineering artifact documenting the
> design that was evaluated.
>
> See:
> `docs/decisions/ADR_0025_Observation_Runtime_Architecture.md`

---

# M6 Observation Runtime — Retrospective Summary

> **Not a Contemporaneous Design Record**
>
> No formal design specification was committed for the M6 Observation Runtime
> during its development (`docs/design/M6_Observation_Model.md` was created empty
> in commit `8e944ff` and never populated). This gap was not caught during the M6
> audit, Engineering Spike #1, or the ADR-0025 review — it surfaced only during
> verification of this restoration task.
>
> This document was written afterward, from surviving artifacts, to summarize
> what ADR-0025 evaluated. It is retrospective, not original.

## Purpose

The M6 Observation Model proposed a runtime abstraction layer for acquiring
CostX workbook data. It defined an immutable Observation ontology family
consisting of:

- `Observation` (root, immutable, deterministic)
- `WorkbookObservation`
- `WorksheetObservation`
- `RowObservation`
- `CellObservation`
- `ObservationSet` (container for one acquisition run)
- `Provenance` (source, observer, procedure)

The model was implemented in `src/jarvis/parsers/observation.py` and the
`WorkbookParser.observe()` method was introduced to emit `ObservationSet`
instances.

## Design Intent

The Observation Runtime aimed to establish a trustworthy, reproducible boundary
between information acquisition and internal reasoning. Observations were defined
as raw, interpretation-free records. Downstream subsystems (Memory, Evidence,
Validation, Knowledge) would consume observations without the acquisition layer
performing classification or inference.

## Evaluation Result (ADR-0025)

Engineering Spike #1 demonstrated that the complete BOQ row classification and
sign validation could be achieved in ~80 lines of flat script with no runtime
abstractions. The spike did not naturally produce a need for the Observation
Runtime classes.

Key findings from the spike:

- **Runtime**: < 1 second for 6,350 rows
- **Lines of Code**: ~80 lines for complete classification and sign validation
- **Classes/Abstractions**: None required; a flat script sufficed

Row classification rules observed from the fixture:

- Column D matches `Head\d+` → Section headers (2,011 rows)
- Column D = `'Note'` → Note rows (520 rows)
- Column D = `'noidc'` + Column B = `'OMISSION/ADDITION'` → Section boundaries (15 rows)
- Column A contains `/` and length > 2 → Item rows (3,615 rows) *(disposable heuristic, not a production classifier — see EQ-0001)*

Sign convention validation:

- Section state (single variable) was sufficient for tracking
- OMISSION section: 169 negative, 7 positive (anomalies)
- ADDITION section: 0 negative, 3 positive (correct)
- No font/style/border data was needed for classification

## Disposition

The Observation Runtime is not adopted as part of the active Jarvis
architecture. The supported production interface of `WorkbookParser` remains the
M6.2 scope (load → validate). The `observe()` method is not part of the
supported production parser interface.

The existing Observation implementation and documentation are retained as
historical engineering artifacts until a separate repository cleanup decision
is made.

## Primary Historical Sources

- `docs/ontology/observation/` — Observation ontology family (normative)
- `src/jarvis/parsers/observation.py` — Historical implementation
- `docs/decisions/ADR_0025_Observation_Runtime_Architecture.md` — Evaluation and rejection
- `docs/reference/Engineering_Questions.md` — EQ-0001, EQ-0002, EQ-0004