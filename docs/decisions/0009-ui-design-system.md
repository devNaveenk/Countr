# ADR-0009: UI design system — palette, typography, tokens

- **Status:** Accepted
- **Date:** 2026-07-26
- **Deciders:** Naveen (BallotDA)

## Context

The first UI pass used ad-hoc emerald/slate classes and emoji icons. Two problems surfaced
on review: (1) typed text in form inputs was invisible (the generated `globals.css` flipped
the foreground color under OS dark mode while inputs stayed white → light text on white),
and (2) the overall scheme looked flat and inconsistent. We want a polished, trustworthy
look and a token system so every screen stays consistent.

## Decision

Adopt a single, committed **light** theme with a semantic **design-token** system in
`frontend/src/app/globals.css` (Tailwind v4 `@theme`):

- **Palette** — "pharmacy green + trust blue": primary `#15803D` (green-700), hover
  `#166534`, soft `#F0FDF4`, accent `#0369A1` (used sparingly); neutrals reuse Tailwind's
  slate scale; danger `#DC2626`.
- **Typography** — Rubik (headings) + Nunito Sans (body), loaded via `next/font`.
- **Tokens generate utilities** (`bg-primary`, `text-primary`, …) and reusable component
  classes (`.input`, `.label`, `.btn-primary`, `.btn-secondary`, `.card`, `.chip`).
- **Icons** — inline SVG set (`components/ui/icons.tsx`), no emoji as structural icons.
- Inputs always use dark text on white (`.input`) — fixes the invisibility bug.

Guidance came from the `ui-ux-pro-max` design skill (retail POS SaaS profile).

## Why (rationale)

- Committing to light avoids the dark-mode contrast bug and matches how retail POS tools
  look; full dark mode is deferred, not designed halfway.
- Tokens + component classes keep the growing set of screens visually consistent and make a
  future rebrand a one-file change (aligns with ADR-0007 / ADR-0008).
- Green reads as fresh/grocery + trustworthy; deeper green-700 looks more credible than the
  earlier emerald-600.

## Deferred / Not doing yet

- **Full dark mode** — deferred; would need a second, separately-tested token set.
- A component library beyond the current primitives (inputs, buttons, cards) grows as
  screens need it.

## Consequences

- All auth + marketing screens now share one system; new screens should use the tokens and
  `.input`/`.btn-*`/`.card` classes rather than ad-hoc colors.
- `frontend/src/lib/brand.ts` + these tokens are the single place branding is defined.
