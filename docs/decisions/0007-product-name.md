# ADR-0007: Working product name — "Countr" (provisional)

- **Status:** Accepted
- **Date:** 2026-07-26
- **Deciders:** Naveen (BallotDA)

## Context

The product needs a name to use in code, folders, and branding. BallotDA is the brand;
each product has its own name. A final name (with trademark/domain checks) isn't ready, but
we can't scaffold a repo without *a* name.

## Decision

Use **"Countr"** as the working product name (a BallotDA product). Treat it as
**provisional** and keep it swappable via a single branding/config value so a later rename
is cheap.

## Why (rationale)

- "Countr" evokes both the store **counter** and **counting** inventory — fitting for a
  retail POS/inventory product.
- Short, brandable, easy to say in the US market.
- Picking *something* now unblocks scaffolding; the name is intentionally isolated so it
  isn't wired all over the code.

## Alternatives considered

- **Precinct / Quorum / TallyBoard** — floated earlier when the product was mis-scoped as
  election-related; no longer relevant.
- **Leave unnamed / codename only** — rejected; a real name makes the product feel real and
  guides branding.

## Deferred / Not doing yet

- **Final name + trademark + domain availability** check is deferred. When done, supersede
  this ADR and do the rename through the single branding config.

## Consequences

- Repo folder, package identifiers, and UI use "Countr" for now.
- Branding values are centralized (one place to change on rename) rather than hardcoded.
