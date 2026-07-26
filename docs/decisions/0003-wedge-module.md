# ADR-0003: First module — Inventory + Billing/POS

- **Status:** Accepted
- **Date:** 2026-07-26
- **Deciders:** Naveen (BallotDA)

## Context

"Complete ERP" is a multi-year scope (ADR-0002). Building it all at once means a long time
before anyone can use — or pay for — anything. We need a **wedge**: the smallest slice a
shopkeeper will open every day and pay for.

## Decision

The first module is **Inventory + Billing/POS + basic reports** — the daily driver of a
store: track stock, scan/lookup products, ring up sales, print a receipt, and see simple
sales/stock reports.

## Why (rationale)

- It is the part of a store's day that *never stops* — highest daily engagement.
- It produces immediate, visible value (a working till + accurate stock).
- It generates the transactional data every later module (purchasing, accounting,
  analytics) will build on.

## Alternatives considered

- **Inventory + Purchasing first** (back-office focus) — valuable but not the daily driver;
  deferred to a later module.
- **Inventory + Reports only** (smallest MVP) — too thin; without billing there's no
  reason for the shopkeeper to open it daily.

## Deferred / Not doing yet

Deferred until after the wedge proves out, each to its own future ADR:
- **Purchasing / suppliers / purchase orders / reorder.**
- **Accounting + QuickBooks sync.**
- **Multi-store.**
- **Employees / payroll / shift management.**
- **CRM / loyalty.**

Reason: none of these earns the first dollar; all depend on transactional data the wedge
creates.

## Consequences

- First build effort concentrates on: product catalog, stock levels, a fast POS/checkout
  screen, receipts, and a few reports.
- US must-haves that touch billing come in early because they block real usage:
  **sales tax** and **payments** (their own ADRs when we implement them).
