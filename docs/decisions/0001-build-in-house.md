# ADR-0001: Build in-house instead of forking NocoBase

- **Status:** Accepted
- **Date:** 2026-07-26
- **Deciders:** Naveen (BallotDA)

## Context

We evaluated building the product on top of a **fork of NocoBase** (an open-source no-code
platform). A fork was even set up (`devNaveenk/nocobase`, branch `ballotda`). NocoBase
provides data modelling, forms, workflow, ACL, audit logs, and mobile out of the box.

However, two things pushed us the other way:

1. **License.** NocoBase ships under its own commercial license (not Apache-2.0). It
   forbids offering a no-code/low-code platform SaaS to the public, requires a paid
   Professional/Enterprise license to remove NocoBase's UI branding, and requires NocoBase
   copyright notices to remain in the source **even after** buying a commercial license.
2. **We don't need a configurable platform.** Our product is a *fixed* retail ERP — we
   (developers) build the features, shopkeepers use them. We need maybe 10–15% of what
   NocoBase does, not its end-user configurability (which is the part that took years to
   build).

## Decision

Build the product **in-house, from scratch**, on a standard stack. Do **not** fork,
embed, or ship NocoBase code.

## Why (rationale)

- **Clean IP and full freedom** — no license constraints, we can sell as SaaS however we
  want, and the codebase is 100% ours (naming and all).
- **A fixed product is a normal web app**, not a platform rebuild. Data storage, screens,
  auth, file upload, notifications are solved problems with mature libraries — building
  only what we need is a months-scale effort, not years.
- **Hireable** — any web developer can work on a standard stack; no NocoBase-specific
  knowledge required.

## Alternatives considered

- **Fork NocoBase + build our product as a plugin on top** — fastest to a demo, gets
  workflow/ACL/audit free. Rejected because of the license constraints above and the
  long-term burden of tracking upstream while carrying 136 packages we mostly don't use.
- **Rebuild a full NocoBase-like configurable platform from scratch** — rejected outright;
  that's a multi-year effort and not what the business needs.

## Deferred / Not doing yet

- **The NocoBase fork is not deleted.** It stays as a reference (see ADR-0006). Revisit
  removing it once we're confident we no longer need to consult its patterns.

## Consequences

- We own everything and can sell freely.
- We must build "boring but necessary" infrastructure (auth, RBAC, audit log, file
  handling, notifications) ourselves — each is days-to-weeks with libraries, and tracked
  in the progress log.
- **Guardrail:** if we ever start letting customers build their own forms/flows, we'd be
  re-inventing NocoBase. We will not go there — the product stays a fixed ERP.
