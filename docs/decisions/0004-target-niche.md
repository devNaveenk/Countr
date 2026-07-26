# ADR-0004: First niche — grocery / convenience stores

- **Status:** Accepted
- **Date:** 2026-07-26
- **Deciders:** Naveen (BallotDA)

## Context

US retail software is crowded (Square, Shopify POS, Lightspeed, Clover). Competing as a
generic "ERP for everyone" means getting lost. Picking a niche lets us fit one type of
store perfectly and win on depth.

## Decision

Target **grocery / convenience stores** first — with particular attention to small
independent and Indian/Asian-owned stores that find incumbents expensive or a poor fit.

## Why (rationale)

- Very large count of such stores in the US.
- High-volume, fast billing is exactly what the wedge module (ADR-0003) optimizes for.
- Underserved segment: many owners find Square/Clover pricing and generic UX a poor fit.

## Alternatives considered

- **Liquor / smoke shops** — attractive (age verification, compliance, high margin, less
  competition); kept as a strong candidate for a later niche.
- **Auto-parts / hardware** — large catalogs, part numbers, B2B billing; deferred.
- **Stay generic** — rejected; leads to getting lost in the crowd.

## Deferred / Not doing yet

- Expanding to other niches (liquor, auto-parts, etc.) is deferred until the grocery niche
  is working and validated. Revisit after first paying customers.

## Consequences

- Domain modelling, UX, and reports are tuned for grocery/convenience first (e.g. fast
  barcode checkout, weight/units, common category structures).
- Marketing and onboarding language target this segment specifically.
