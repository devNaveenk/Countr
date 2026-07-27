"use client";

import { useCallback, useEffect, useState } from "react";

import { adjustStock, listProducts, type Product } from "@/features/products/api";
import {
  getInventorySummary,
  listMovements,
  type InventorySummary,
  type MovementReason,
  type StockMovement,
} from "@/features/inventory/api";

function usd(v: string | number) {
  return `$${Number(v).toFixed(2)}`;
}
function num(v: string) {
  return String(Number(v));
}

const reasonLabel: Record<MovementReason, string> = {
  sale: "Sale",
  purchase: "Purchase",
  adjustment: "Adjustment",
  initial: "Opening",
};

export default function InventoryPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [summary, setSummary] = useState<InventorySummary | null>(null);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [historyFor, setHistoryFor] = useState<Product | null>(null);

  const load = useCallback(async () => {
    const [prods, sum] = await Promise.all([
      listProducts({ search: search || undefined }),
      getInventorySummary(),
    ]);
    setProducts(prods);
    setSummary(sum);
    setLoading(false);
  }, [search]);

  useEffect(() => {
    const t = setTimeout(load, 200);
    return () => clearTimeout(t);
  }, [load]);

  async function onAdjust(p: Product) {
    const raw = window.prompt(
      `Adjust stock for "${p.name}" (current ${num(p.stock_quantity)}).\nEnter a change: e.g. 12 to add, -3 to remove.`,
      "",
    );
    if (!raw) return;
    const delta = Number(raw);
    if (!Number.isFinite(delta) || delta === 0) return;
    const note = window.prompt("Reason (optional): e.g. Damaged, Recount, Theft", "") ?? undefined;
    try {
      await adjustStock(p.id, String(delta), note || undefined);
      await load();
    } catch {
      window.alert("Could not adjust (would stock go negative?).");
    }
  }

  const stats = summary
    ? [
        { label: "Products", value: String(summary.total_products) },
        { label: "Units in stock", value: num(summary.total_units) },
        { label: "Stock value", value: usd(summary.stock_value) },
        { label: "Low stock", value: String(summary.low_stock_count) },
      ]
    : [];

  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-8 sm:px-6">
      <h1 className="text-2xl font-bold tracking-tight text-slate-900">Inventory</h1>
      <p className="mt-1 text-sm text-slate-600">What you have on hand, and every change to it.</p>

      {/* Summary */}
      <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {(loading || !summary ? Array.from({ length: 4 }) : stats).map((s, i) => (
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

      <input
        className="input mt-6 max-w-xs"
        placeholder="Search products…"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        aria-label="Search products"
      />

      {/* Table */}
      <div className="card mt-4 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-slate-200 text-left text-xs uppercase tracking-wide text-slate-500">
                <th className="px-4 py-3 font-medium">Product</th>
                <th className="px-4 py-3 text-right font-medium">On hand</th>
                <th className="px-4 py-3 text-right font-medium">Cost</th>
                <th className="px-4 py-3 text-right font-medium">Value</th>
                <th className="px-4 py-3 text-right font-medium">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {products.map((p) => (
                <tr key={p.id} className="hover:bg-slate-50">
                  <td className="px-4 py-3">
                    <div className="font-medium text-slate-900">{p.name}</div>
                    {p.category && <div className="text-xs text-slate-400">{p.category}</div>}
                  </td>
                  <td className="px-4 py-3 text-right">
                    <span
                      className={`tabular-nums ${
                        p.is_low_stock ? "font-semibold text-amber-600" : "text-slate-900"
                      }`}
                    >
                      {num(p.stock_quantity)}
                    </span>
                    {p.is_low_stock && (
                      <span className="ml-2 rounded-full bg-amber-50 px-2 py-0.5 text-xs font-medium text-amber-700">
                        Low
                      </span>
                    )}
                  </td>
                  <td className="px-4 py-3 text-right tabular-nums text-slate-600">
                    {usd(p.cost_price)}
                  </td>
                  <td className="px-4 py-3 text-right tabular-nums text-slate-900">
                    {usd(Number(p.stock_quantity) * Number(p.cost_price))}
                  </td>
                  <td className="px-4 py-3">
                    <div className="flex justify-end gap-1">
                      <button
                        onClick={() => onAdjust(p)}
                        className="rounded px-2 py-1 font-medium text-primary hover:bg-primary-soft"
                      >
                        Adjust
                      </button>
                      <button
                        onClick={() => setHistoryFor(p)}
                        className="rounded px-2 py-1 font-medium text-slate-600 hover:bg-slate-100"
                      >
                        History
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
              {products.length === 0 && (
                <tr>
                  <td colSpan={5} className="px-4 py-10 text-center text-sm text-slate-500">
                    {loading ? "Loading…" : "No products yet."}
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {historyFor && (
        <MovementsModal product={historyFor} onClose={() => setHistoryFor(null)} />
      )}
    </div>
  );
}

function MovementsModal({ product, onClose }: { product: Product; onClose: () => void }) {
  const [movements, setMovements] = useState<StockMovement[] | null>(null);

  useEffect(() => {
    let active = true;
    listMovements(product.id, 100)
      .then((m) => {
        if (active) setMovements(m);
      })
      .catch(() => {
        if (active) setMovements([]);
      });
    return () => {
      active = false;
    };
  }, [product.id]);

  return (
    <div
      className="fixed inset-0 z-50 flex items-end justify-center bg-slate-900/40 p-0 sm:items-center sm:p-4"
      role="dialog"
      aria-modal="true"
      aria-label={`Stock history for ${product.name}`}
      onClick={onClose}
    >
      <div
        className="max-h-[85vh] w-full max-w-md overflow-y-auto rounded-t-2xl bg-white p-6 shadow-xl sm:rounded-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between">
          <h2 className="font-heading text-lg font-bold text-slate-900">Stock history</h2>
          <button onClick={onClose} className="text-sm font-medium text-slate-500 hover:text-slate-700">
            Close
          </button>
        </div>
        <p className="text-sm text-slate-500">{product.name}</p>

        {movements === null ? (
          <p className="py-8 text-center text-sm text-slate-500">Loading…</p>
        ) : movements.length === 0 ? (
          <p className="py-8 text-center text-sm text-slate-500">No movements yet.</p>
        ) : (
          <ul className="mt-4 divide-y divide-slate-100">
            {movements.map((m) => {
              const positive = Number(m.delta) >= 0;
              return (
                <li key={m.id} className="flex items-center gap-3 py-2.5 text-sm">
                  <span
                    className={`w-16 text-right font-semibold tabular-nums ${
                      positive ? "text-green-700" : "text-red-600"
                    }`}
                  >
                    {positive ? "+" : ""}
                    {num(m.delta)}
                  </span>
                  <span className="flex-1">
                    <span className="font-medium text-slate-900">{reasonLabel[m.reason]}</span>
                    {m.note && <span className="ml-1 text-slate-500">· {m.note}</span>}
                    <span className="block text-xs text-slate-400">
                      {new Date(m.created_at).toLocaleString()}
                    </span>
                  </span>
                  <span className="tabular-nums text-slate-500">→ {num(m.balance_after)}</span>
                </li>
              );
            })}
          </ul>
        )}
      </div>
    </div>
  );
}
