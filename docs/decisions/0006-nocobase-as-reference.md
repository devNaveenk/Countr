# ADR-0006: Keep NocoBase as a reference only

- **Status:** Accepted
- **Date:** 2026-07-26
- **Deciders:** Naveen (BallotDA)

## Context

Having chosen to build in-house (ADR-0001), the question was what to do with the existing
NocoBase clone at `../nocobase/`. Options: delete it, or keep it.

## Decision

**Keep** the `../nocobase/` folder as a **read-only architectural reference** — a knowledge
base for how a mature system structures data modelling, workflow, permissions (ACL), and
audit logging. Do **not** copy its code, and keep it outside Countr's own git repository.

## Why (rationale)

- Deleting is irreversible and the reference has real value while we design our own
  equivalents.
- Studying a battle-tested system's *patterns* (not its code) speeds up good design
  decisions.

## Alternatives considered

- **Delete it now** — rejected; premature, loses a useful reference.
- **Fork/embed it** — rejected in ADR-0001 (license + platform baggage).

## Deferred / Not doing yet

- **Removing the folder** is deferred until we're confident we no longer consult it.
- Its own git remotes (the `devNaveenk/nocobase` fork) are left intact for now; cleaning
  them up is a later chore.

## Consequences

- **Legal guardrail:** because we only *read patterns* and never ship NocoBase code, its
  commercial license does not bind Countr. If any NocoBase code is ever copied in, that
  changes — so we don't copy code.
- Countr's git repo must exclude `../nocobase/` (it's a sibling folder, naturally outside).
