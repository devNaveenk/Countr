"use client";

import { useCallback, useEffect, useState } from "react";

import { getOverview, type StoreReport } from "@/features/reports/api";

const PERIODS = [
  { days: 1, label: "Today" },
  { days: 7, label: "7 days" },
  { days: 30, label: "30 days" },
];

function usd(v: string) {
  return `$${Number(v).toFixed(2)}`;
}

function qty(v: string) {
  return String(Number(v));
}

export default function ReportsPage() {
  const [days, setDays] = useState(7);
  const [report, setReport] = useState<StoreReport | null>(null);
  const [loading, setLoading] = useState(true);

  // Note: loading starts true and is cleared in `finally`. We deliberately do not flip it
  // back to true on refetch so no setState runs synchronously inside the effect.
  const load = useCallback(async () => {
    try {
      setReport(await getOverview(days));
    } finally {
      setLoading(false);
    }
  }, [days]);

  useEffect(() => {
    load();
  }, [load]);

  const stats = report
    ? [
        { label: "Revenue", value: usd(report.summary.gross_revenue) },
        { label: "Sales", value: String(report.summary.sales_count) },
        { label: "Items sold", value: qty(report.summary.items_sold) },
        { label: "Tax collected", value: usd(report.summary.tax_collected) },
      ]
    : [];

  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-8 sm:px-6">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900">Reports</h1>
          <p className="mt-1 text-sm text-slate-600">How your store is doing.</p>
        </div>
        <div className="inline-flex rounded-lg border border-slate-300 bg-white p-0.5">
          {PERIODS.map((p) => (
            <button
              key={p.days}
              onClick={() => setDays(p.days)}
              className={`rounded-md px-3 py-1.5 text-sm font-medium transition ${
                days === p.days
                  ? "bg-primary text-white"
                  : "text-slate-600 hover:bg-slate-100"
              }`}
            >
              {p.label}
            </button>
          ))}
        </div>
      </div>

      {/* Stat cards */}
      <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {(loading || !report ? Array.from({ length: 4 }) : stats).map((s, i) => (
          <div key={i} className="card p-5">
            <div className="text-sm text-slate-500">
              {s ? (s as { label: string }).label : <span className="opacity-0">—</span>}
            </div>
            <div className="mt-1 text-2xl font-bold tabular-nums text-slate-900">
              {s ? (s as { value: string }).value : "…"}
            </div>
          </div>
        ))}
      </div>

      <div className="mt-6 grid gap-6 lg:grid-cols-2">
        {/* Best sellers */}
        <div className="card p-5">
          <h2 className="font-heading font-bold text-slate-900">Best sellers</h2>
          {report && report.best_sellers.length > 0 ? (
            <ul className="mt-4 divide-y divide-slate-100">
              {report.best_sellers.map((b, i) => (
                <li key={b.product_id} className="flex items-center gap-3 py-2.5">
                  <span className="grid h-6 w-6 place-items-center rounded-full bg-primary-soft text-xs font-bold text-primary">
                    {i + 1}
                  </span>
                  <span className="flex-1 truncate text-sm font-medium text-slate-900">
                    {b.name}
                  </span>
                  <span className="text-sm tabular-nums text-slate-500">{qty(b.quantity)} sold</span>
                  <span className="w-16 text-right text-sm font-medium tabular-nums text-slate-900">
                    {usd(b.revenue)}
                  </span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="mt-4 py-6 text-center text-sm text-slate-500">
              {loading ? "Loading…" : "No sales in this period yet."}
            </p>
          )}
        </div>

        {/* Low stock */}
        <div className="card p-5">
          <h2 className="font-heading font-bold text-slate-900">Low stock</h2>
          {report && report.low_stock.length > 0 ? (
            <ul className="mt-4 divide-y divide-slate-100">
              {report.low_stock.map((p) => (
                <li key={p.id} className="flex items-center gap-3 py-2.5">
                  <span className="flex-1 truncate text-sm font-medium text-slate-900">
                    {p.name}
                  </span>
                  <span className="rounded-full bg-amber-50 px-2 py-0.5 text-xs font-medium text-amber-700">
                    {qty(p.stock_quantity)} left
                  </span>
                  <span className="text-xs text-slate-400">reorder {qty(p.reorder_level)}</span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="mt-4 py-6 text-center text-sm text-slate-500">
              {loading ? "Loading…" : "Nothing is low on stock. 🎉"}
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
