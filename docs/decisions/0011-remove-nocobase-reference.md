# ADR-0011: Remove the NocoBase reference folder

- **Status:** Accepted
- **Date:** 2026-07-26
- **Supersedes:** ADR-0006 (keep NocoBase as a reference)
- **Deciders:** Naveen (BallotDA)

## Context

ADR-0006 kept the `../nocobase/` clone as a read-only architectural reference. By now the
in-house build (Products, Buy, Sell/POS, Inventory + ledger, Reports, Sales history) has its
own established patterns, and the clone (~564 MB) was no longer being consulted. Separately,
the user deleted the `devNaveenk/nocobase` GitHub fork; its local `origin` remote and the
`ballotda` branch were removed, leaving the folder as a bare upstream clone.

## Decision

**Delete the `nocobase/` folder entirely.** Countr no longer keeps any NocoBase code or
clone on disk.

## Why (rationale)

- The reference has served its purpose; our own code is the reference now.
- Removes 564 MB of unused files and any lingering confusion about NocoBase being "part of"
  the product.
- Reinforces the clean-IP position: Countr ships and stores **no** NocoBase code, so its
  commercial license does not bind us (ADR-0001).

## Alternatives considered

- **Keep it (ADR-0006)** — no longer justified; it wasn't being used.

## Deferred / Not doing yet

- Nothing. NocoBase is fully out of the project. If a pattern needs consulting later, browse
  it on GitHub rather than re-cloning into the repo workspace.

## Consequences

- The workspace now contains only `countr/`.
- Any future reference to NocoBase is external (github.com/nocobase/nocobase), never vendored.
