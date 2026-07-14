# BOQ Intelligence Increment 1 — Engineering Retrospective

Date: 2026-07-14

---

## What Assumptions Proved Correct

**Pure functions over `list[BOQRow]` was the right scope.** No architectural expansion was needed. The existing extraction pipeline provided everything the intelligence module required. This confirmed that the Capability Evaluation 001 constraint was not just disciplined — it was accurate.

**EQ-0007 evidence was stable and sufficient.** The accepted values from the Production Extraction Report served as a reliable regression target. Every test passed on the first run against the authoritative fixture. The evidence chain (EQ-0007 → EQ-0009 → fixture → test) held without gaps.

**Fixture integrity verification is cheap and valuable.** SHA-256 hashing adds negligible overhead but provides a hard guarantee that the fixture under test is the fixture that was registered. This catches accidental file modifications, editor auto-formatting of binary files, and git merge conflicts in binary assets.

**Deterministic output matters more than it initially appears.** Sorting anomalies by row_number and section statistics by key name seemed like defensive coding, but the acceptance tests depend on exact list equality. Without deterministic ordering, tests would be fragile and non-reproducible.

## What Assumptions Proved Unnecessary

**Quantity range statistics (min/max) were speculative.** They were included in the initial implementation but removed after review — nothing consumes them. YAGNI applied correctly.

**Verbose stat key names (`rows_with_code`) were premature clarity.** Shorter names (`code_rows`) are equally clear in context and reduce visual noise. The longer names added no disambiguation value.

**Deep immutability for the result dataclass was over-engineering.** Frozen dataclass with shallow immutability is sufficient. No consumer has mutated the collections, and if one does in the future, that's when deep immutability should be introduced — not before.

## Were Any Architectural Changes Unexpectedly Needed

No. This was the explicit goal of the constraint, and it held. The implementation required zero changes to:

- Platform Kernel
- Application composition root
- WorkbookParser API
- BOQ extraction logic
- Observation model types

The only structural change was fixture governance (Python dict → JSON registry), which was an improvement to engineering infrastructure, not an architectural change.

## Did Any Governance Step Create Friction

**Fixture metadata evolution required iteration.** The initial per-category metadata design was reconsidered during review. The centralized JSON registry was adopted because it better separated metadata from verification logic and provides a single authoritative registry for fixtures.

**Lesson:** When designing infrastructure, ask "what happens when there are three categories, not one?" even if YAGNI says don't build for it yet. The answer doesn't require building the feature — but it does require leaving a TODO (which was done for the registry key collision case).

**The authority chain documentation was valuable but not obvious.** The initial evidence module header simply referenced EQ-0007. It was strengthened to document the full authority chain (Engineering Question → cross-validation → fixture → identity verification). This is not bureaucratic overhead — it's the difference between "this number came from a report" and "this number is engineering evidence with a verifiable provenance."

## Lessons for BOQ Intelligence Increment 2

1. **The evidence module pattern works.** Centralizing accepted values in `tests/reference/` with an authority chain is reproducible for future increments. Any new intelligence function should add its expected values here, not inline in tests.

2. **The registration tool is the governance boundary.** Tests verify, the tool registers. This separation is clean and should be preserved. If Increment 2 introduces new fixtures, they go through `tools/register_fixture.py`.

3. **Defensive validation at production boundaries is worth the cost.** The `ValueError` for unknown row types cost one `if` statement but transforms an opaque `KeyError` into a diagnostic message. Every production boundary should have this.

4. **The TODO for registry key collisions is real but not urgent.** When Cubit or PDF fixtures arrive, filenames may collide. The fix (promote key from filename to relative path) is small and localized. Don't solve it now — but don't forget it either.

5. **The frozen dataclass with mutable contents is an acceptable trade-off for now.** If Increment 2 introduces consumers that share result objects across threads or cache them, deep immutability should be revisited. Until then, shallow immutability with a documented limitation is honest engineering.

## Reusable Patterns

The following patterns emerged during Increment 1 and are candidates for intentional reuse by future capabilities (Formatter, CheckMate, Cubit Parser):

- **Evidence modules** under `tests/reference/` — centralized accepted values with authority chains, not inline test constants
- **Verification-only APIs** — `FIXTURE_METADATA.verify_fixture()` loads and checks, never mutates
- **Explicit registration tools** — `tools/register_fixture.py` makes fixture governance a deliberate engineering action
- **Production pipeline regression testing** — test the full chain (load → extract → analyze) against authoritative fixtures, not just unit-level mocks
- **Authority chain documentation** — every accepted value traces back to an Engineering Question, a fixture, and a verification method

These are not unique to BOQ Intelligence. They are the engineering infrastructure of the Capability Era.

## Emerging Themes

Nearly every refinement during Increment 1 fell into one of three categories:

- **Determinism** — ordering, fixture identity, atomic writes
- **Explicitness** — registration tool, authority chain, validation
- **YAGNI** — removing speculative stats, avoiding extra models

These three themes are emerging as the practical engineering style of the Capability Era. They are broader than this single capability and should inform how future capabilities are implemented.

---

*This retrospective captures fresh engineering knowledge from the BOQ Intelligence Increment 1 implementation. It is intended to inform Increment 2 planning and future capability work.*