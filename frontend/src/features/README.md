# Feature modules

Each user-facing capability lives in its own folder here (feature-based, not layer-based),
so everything for one feature stays together and can change independently.

Planned for Phase 1 (wedge — Inventory + Billing/POS, see `docs/decisions/0003-wedge-module.md`):

```
features/
├── catalog/     # products, categories, barcodes, prices, units
├── inventory/   # stock levels & adjustments
├── pos/         # checkout screen: scan, cart, tender, receipt
└── reports/     # basic sales & stock reports
```

Inside a feature, keep its own `components/`, `hooks/`, and `api.ts` (calls via
`@/lib/api/client`). Shared, generic UI goes in `@/components/ui`; app shells/nav in
`@/components/layout`.
