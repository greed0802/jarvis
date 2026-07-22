# Engineering Authority

**Authoritative Source:** AGENTS.md (repository root) — the authoritative engineering rules document. See § Project Authority, § Evidence Hierarchy.

**Purpose:** Resolve ambiguity when repository documents disagree.

**Authority:** Project Owner (incorporated into Jarvis governance)
**Version:** 1.0.0
**Status:** Active

---

## Priority of Truth

When two repository documents disagree, the higher-ranked source wins.

1. **Production Source Code** — What the code actually does. Absolute authority.
2. **Frozen Contracts** — Formal evidence contracts (v1.0.0+). Define consumer-facing guarantees.
3. **Frozen Engineering Evidence** — Accepted spike reports, EQ conclusions. Document what was learned.
4. **Engineering Questions** — Active investigations. Define what is being studied.
5. **Knowledge Base** — `docs/knowledge/`. Synthesized documentation from evidence.
6. **Architecture Documents** — Vision (00), Principles (01), Blueprint (02), Kernel (04). Define intent.
7. **Planning Documents** — Capability Register, Roadmap, Implementation Status. Define trajectory.
8. **Historical Documents** — Design docs, early ADRs, pre-freeze artifacts. Historical context only.

---

## Conflict Resolution Rules

### Rule 1: Code Wins Over Documentation
When production code disagrees with documentation, **code is truth**. Documentation must be updated to match code — or an Engineering Question must be filed to determine whether code should change.

### Rule 2: Frozen Over Draft
Frozen artifacts (Contracts, Evidence, EQ conclusions) override draft artifacts (active EQs, planning docs, knowledge base).

### Rule 3: Explicit Over Implicit
An explicit ADR overrides an implicit pattern. If a decision was formally made, it governs.

### Rule 4: Conflicts Must Be Recorded
When a conflict is discovered, it must be recorded in the Engineering Debt Register or a new Engineering Question. Silent resolution is prohibited.

---

## What This Document Does NOT Do

- It does NOT create new authority. Project Owner remains the final engineering authority.
- It does NOT override AGENTS.md rules. AGENTS.md governs agent behavior.
- It does NOT change the Evidence Hierarchy in AGENTS.md. That hierarchy governs investigation.
- It does NOT create a new governance process. It clarifies existing authority.

---

## Consumer Guidance

When uncertain which document governs:

1. Check this Priority of Truth list.
2. If still ambiguous, file an Engineering Question.
3. Project Owner resolves.

---

## References

- AGENTS.md — Evidence Hierarchy section
- docs/01_Principles.md — Engineering principles
- docs/engineering/Quality_Assurance_Constitution.md — Quality Gate framework
- docs/04_Platform_Kernel.md — Kernel authority boundaries