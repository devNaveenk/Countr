"use client";

import { useEffect, useMemo, useState } from "react";

import { listSales, type Sale } from "@/features/sales/api";

function usd(v: string | number) {
  return `$${Number(v).toFixed(2)}`;
}
function num(v: string) {
  return String(Number(v));
}

export default function SalesHistoryPage() {
  const [sales, setSales] = useState<Sale[] | null>(null);
  const [selected, setSelected] = useState<Sale | null>(null);

  useEffect(() => {
    let active = true;
    listSales(100)
      .then((s) => {
        if (active) setSales(s);
      })
      .catch(() => {
        if (active) setSales([]);
      });
    return () => {
      active = false;
    };
  }, []);

  const dayTotal = useMemo(() => {
    if (!sales) return 0;
    const today = new Date().toDateString();
    return sales
      .filter((s) => new Date(s.created_at).toDateString() === today)
      .reduce((sum, s) => sum + Number(s.total), 0);
  }, [sales]);

  return (
    <div className="mx-auto w-full max-w-4xl px-4 py-8 sm:px-6">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900">Sales history</h1>
          <p className="mt-1 text-sm text-slate-600">Every completed sale. Tap one for its receipt.</p>
        </div>
        {sales && sales.length > 0 && (
          <div className="text-right">
            <div className="text-xs uppercase tracking-wide text-slate-500">Today</div>
            <div className="text-xl font-bold tabular-nums text-slate-900">{usd(dayTotal)}</div>
          </div>
        )}
      </div>

      <div className="card mt-6 overflow-hidden">
        {sales === null ? (
          <p className="py-12 text-center text-sm text-slate-500">Loading…</p>
        ) : sales.length === 0 ? (
          <p className="py-12 text-center text-sm text-slate-500">
            No sales yet. Ring one up under <span className="font-medium">Sell</span>.
          </p>
        ) : (
          <ul className="divide-y divide-slate-100">
            {sales.map((s) => (
              <li key={s.id}>
                <button
                  onClick={() => setSelected(s)}
                  className="flex w-full items-center gap-4 px-4 py-3 text-left hover:bg-slate-50"
                >
                  <div className="min-w-0 flex-1">
                    <div className="text-sm font-medium text-slate-900">
                      {new Date(s.created_at).toLocaleString()}
                    </div>
                    <div className="text-xs text-slate-500">
                      {s.item_count} item{s.item_count === 1 ? "" : "s"}
                    </div>
                  </div>
                  <span className="rounded-full bg-slate-100 px-2 py-0.5 text-xs font-medium capitalize text-slate-600">
                    {s.payment_method}
                  </span>
                  <span className="w-20 text-right text-sm font-bold tabular-nums text-slate-900">
                    {usd(s.total)}
                  </span>
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>

      {selected && <ReceiptModal sale={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}

function ReceiptModal({ sale, onClose }: { sale: Sale; onClose: () => void }) {
  return (
    <div
      className="fixed inset-0 z-50 flex items-end justify-center bg-slate-900/40 p-0 sm:items-center sm:p-4"
      role="dialog"
      aria-modal="true"
      aria-label="Receipt"
      onClick={onClose}
    >
      <div
        className="max-h-[85vh] w-full max-w-sm overflow-y-auto rounded-t-2xl bg-white p-6 shadow-xl sm:rounded-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between">
          <h2 className="font-heading text-lg font-bold text-slate-900">Receipt</h2>
          <button onClick={onClose} className="text-sm font-medium text-slate-500 hover:text-slate-700">
            Close
          </button>
        </div>
        <p className="text-sm text-slate-500">
          {new Date(sale.created_at).toLocaleString()} · {sale.payment_method}
        </p>

        <div className="mt-4 space-y-2 border-y border-slate-200 py-4 text-sm">
          {sale.items.map((i) => (
            <div key={i.product_id} className="flex justify-between">
              <span className="text-slate-700">
                {i.name} × {num(i.quantity)}
              </span>
              <span className="tabular-nums text-slate-900">{usd(i.line_total)}</span>
            </div>
          ))}
        </div>

        <div className="mt-4 space-y-1 text-sm">
          <div className="flex justify-between text-slate-600">
            <span>Subtotal</span>
            <span className="tabular-nums">{usd(sale.subtotal)}</span>
          </div>
          <div className="flex justify-between text-slate-600">
            <span>Tax</span>
            <span className="tabular-nums">{usd(sale.tax_total)}</span>
          </div>
          <div className="flex justify-between text-base font-bold text-slate-900">
            <span>Total</span>
            <span className="tabular-nums">{usd(sale.total)}</span>
          </div>
        </div>

        <button onClick={onClose} className="btn-primary mt-6 w-full">
          Done
        </button>
      </div>
    </div>
  );
}
