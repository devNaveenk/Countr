# ADR-0008: Countr is a deliberate new retail vertical under BallotDA

- **Status:** Accepted
- **Date:** 2026-07-26
- **Deciders:** Naveen (BallotDA)

## Context

BallotDA (ballotda.com) is an operating **election-management software** company —
tagline "Your Digital Assistant for Secure, Efficient, and Compliant Elections", with real
county clients (Fulton/Douglas/Whitfield GA, Bay FL, and others). Its products are all
election-focused (Poll Worker Management, Asset Management, Absentee Ballot, FOIA, Voter AI,
etc.).

This raised a real question: **why is an election-software company building a retail ERP
(Countr) for grocery/convenience stores?** The two domains have nothing in common, and a
grocery POS does not fit the election brand. We paused to confirm before writing more code.

## Decision

Confirmed: **Countr is a deliberate new retail vertical** that BallotDA is starting,
**separate from its election business**. The retail-ERP scope (ADR-0002/0003/0004) stands
unchanged. "Stores / shopkeepers / grocery" is the *literal* target market, not an analogy
for election offices.

## Why (rationale)

- Explicit owner confirmation (the decision-maker is inside BallotDA — email
  `naveenk@ballotda.com`).
- BallotDA is treated as a **parent brand / umbrella** that can house multiple products in
  different markets, each with its own product name (see ADR-0007).

## Alternatives considered

- **Product is actually an election-operations platform**, and "stores/shopkeepers" was an
  analogy — **rejected by owner.** (Had this been true, ADR-0002/0003/0004 would have been
  superseded.)

## Deferred / Not doing yet

- **Brand/visual relationship between Countr and BallotDA.** Because Countr's market is
  unrelated to elections, it likely needs its **own product identity** rather than
  inheriting BallotDA's election-trust visual language (blue/red palette, ballot-check
  logo). BallotDA may appear only as a light parent endorsement ("by BallotDA"). Final
  logo, palette, and the exact endorsement wording are deferred to a branding ADR. For now,
  branding values stay centralized (ADR-0007) so this can be set later without rework.

## Consequences

- No rework of the retail scope.
- Countr's UI should not lean on BallotDA's election branding; treat Countr as its own
  identity until the branding ADR is written.
- Anyone confused by "election company → grocery ERP" now has the answer here.
