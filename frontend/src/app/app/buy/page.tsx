"use client";

import { useCallback, useEffect, useState } from "react";

import { listProducts, type Product } from "@/features/products/api";
import { listPurchases, receiveStock, type Purchase } from "@/features/purchases/api";

interface Line {
  product: Product;
  quantity: string;
  unitCost: string;
}

function usd(v: string | number) {
  return `$${Number(v).toFixed(2)}`;
}

export default function BuyPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [search, setSearch] = useState("");
  const [lines, setLines] = useState<Record<string, Line>>({});
  const [supplier, setSupplier] = useState("");
  const [note, setNote] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [done, setDone] = useState<Purchase | null>(null);
  const [recent, setRecent] = useState<Purchase[]>([]);

  const loadProducts = useCallback(async () => {
    setProducts(await listProducts({ search: search || undefined }));
  }, [search]);

  const loadRecent = useCallback(async () => {
    setRecent(await listPurchases(10));
  }, []);

  useEffect(() => {
    const t = setTimeout(loadProducts, 200);
    return () => clearTimeout(t);
  }, [loadProducts]);

  useEffect(() => {
    let active = true;
    listPurchases(10)
      .then((r) => {
        if (active) setRecent(r);
      })
      .catch(() => {});
    return () => {
      active = false;
    };
  }, []);

  const lineList = Object.values(lines);
  const total = lineList.reduce(
    (sum, l) => sum + Number(l.quantity || 0) * Number(l.unitCost || 0),
    0,
  );

  function addLine(p: Product) {
    setError(null);
    setLines((prev) =>
      prev[p.id]
        ? prev
        : { ...prev, [p.id]: { product: p, quantity: "1", unitCost: p.cost_price } },
    );
  }

  function updateLine(id: string, patch: Partial<Line>) {
    setLines((prev) => ({ ...prev, [id]: { ...prev[id], ...patch } }));
  }

  function removeLine(id: string) {
    setLines((prev) => {
      const rest = { ...prev };
      delete rest[id];
      return rest;
    });
  }

  async function submit() {
    if (lineList.length === 0) return;
    setBusy(true);
    setError(null);
    try {
      const purchase = await receiveStock({
        supplier_name: supplier.trim() || null,
        note: note.trim() || null,
        lines: lineList.map((l) => ({
          product_id: l.product.id,
          quantity: l.quantity || "0",
          unit_cost: l.unitCost || "0",
        })),
      });
      setDone(purchase);
      setLines({});
      setSupplier("");
      setNote("");
      loadProducts();
      loadRecent();
    } catch {
      setError("Could not receive stock. Please check the values and try again.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-8 sm:px-6">
      <h1 className="text-2xl font-bold tracking-tight text-slate-900">Buy — receive stock</h1>
      <p className="mt-1 text-sm text-slate-600">
        Record stock coming in. This raises quantities and updates each item&apos;s cost.
      </p>

      {done && (
        <div className="mt-4 flex items-center justify-between rounded-lg border border-green-200 bg-green-50 px-4 py-3 text-sm text-green-800">
          <span>
            Received {done.item_count} item(s) · {usd(done.total_cost)}
            {done.supplier_name ? ` from ${done.supplier_name}` : ""}.
          </span>
          <button onClick={() => setDone(null)} className="font-medium text-green-700">
            Dismiss
          </button>
        </div>
      )}

      <div className="mt-6 grid gap-6 lg:grid-cols-[1fr_380px]">
        {/* Builder */}
        <section>
          <input
            className="input"
            placeholder="Search products to add…"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            aria-label="Search products"
          />
          <div className="mt-3 grid grid-cols-2 gap-2 sm:grid-cols-3">
            {products.map((p) => (
              <button
                key={p.id}
                onClick={() => addLine(p)}
                className="card p-3 text-left text-sm transition hover:border-primary hover:shadow-md"
              >
                <div className="font-medium text-slate-900">{p.name}</div>
                <div className="mt-0.5 text-xs text-slate-500">
                  {Number(p.stock_quantity)} in stock · cost {usd(p.cost_price)}
                </div>
              </button>
            ))}
            {products.length === 0 && (
              <p className="col-span-full py-8 text-center text-sm text-slate-500">
                No products found.
              </p>
            )}
          </div>
        </section>

        {/* Cart / receipt builder */}
        <aside className="card h-fit p-5 lg:sticky lg:top-6">
          <h2 className="font-heading text-lg font-bold text-slate-900">Receiving</h2>

          <div className="mt-4 space-y-3">
            <div>
              <label htmlFor="supplier" className="label">
                Supplier (optional)
              </label>
              <input
                id="supplier"
                className="input mt-1"
                placeholder="e.g. Acme Foods"
                value={supplier}
                onChange={(e) => setSupplier(e.target.value)}
              />
            </div>

            {lineList.length === 0 ? (
              <p className="py-6 text-center text-sm text-slate-500">
                Tap products to add them.
              </p>
            ) : (
              <div className="space-y-3">
                {lineList.map(({ product, quantity, unitCost }) => (
                  <div key={product.id} className="rounded-lg border border-slate-200 p-3">
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium text-slate-900">{product.name}</span>
                      <button
                        onClick={() => removeLine(product.id)}
                        className="text-xs font-medium text-red-600 hover:underline"
                      >
                        Remove
                      </button>
                    </div>
                    <div className="mt-2 grid grid-cols-2 gap-2">
                      <label className="text-xs text-slate-500">
                        Qty
                        <input
                          className="input mt-0.5 py-1.5 text-sm"
                          inputMode="decimal"
                          value={quantity}
                          onChange={(e) => updateLine(product.id, { quantity: e.target.value })}
                        />
                      </label>
                      <label className="text-xs text-slate-500">
                        Unit cost ($)
                        <input
                          className="input mt-0.5 py-1.5 text-sm"
                          inputMode="decimal"
                          value={unitCost}
                          onChange={(e) => updateLine(product.id, { unitCost: e.target.value })}
                        />
                      </label>
                    </div>
                    <div className="mt-1 text-right text-xs text-slate-500">
                      Line: {usd(Number(quantity || 0) * Number(unitCost || 0))}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="mt-4 flex justify-between border-t border-slate-200 pt-4 text-base font-bold text-slate-900">
            <span>Total cost</span>
            <span className="tabular-nums">{usd(total)}</span>
          </div>

          {error && (
            <p role="alert" className="mt-3 text-sm text-red-600">
              {error}
            </p>
          )}

          <button
            onClick={submit}
            disabled={busy || lineList.length === 0}
            className="btn-primary mt-4 w-full py-3 text-base"
          >
            {busy ? "Receiving…" : "Receive stock"}
          </button>
        </aside>
      </div>

      {/* Recent purchases */}
      <div className="card mt-8 p-5">
        <h2 className="font-heading font-bold text-slate-900">Recent purchases</h2>
        {recent.length === 0 ? (
          <p className="mt-4 py-6 text-center text-sm text-slate-500">No purchases yet.</p>
        ) : (
          <ul className="mt-4 divide-y divide-slate-100">
            {recent.map((p) => (
              <li key={p.id} className="flex items-center gap-3 py-3 text-sm">
                <span className="flex-1 truncate">
                  <span className="font-medium text-slate-900">
                    {p.supplier_name ?? "Stock received"}
                  </span>
                  <span className="ml-2 text-slate-500">
                    {p.item_count} item(s) · {new Date(p.created_at).toLocaleDateString()}
                  </span>
                </span>
                <span className="font-medium tabular-nums text-slate-900">
                  {usd(p.total_cost)}
                </span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
