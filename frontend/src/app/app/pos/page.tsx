"use client";

import { useCallback, useEffect, useMemo, useState } from "react";

import { listProducts, type Product } from "@/features/products/api";
import {
  checkout,
  getStoreSettings,
  type PaymentMethod,
  type Sale,
} from "@/features/sales/api";
import { ApiError } from "@/lib/api/client";

interface CartLine {
  product: Product;
  quantity: number;
}

function fmt(n: number) {
  return `$${n.toFixed(2)}`;
}

export default function PosPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [search, setSearch] = useState("");
  const [cart, setCart] = useState<Record<string, CartLine>>({});
  const [taxRate, setTaxRate] = useState(0);
  const [payment, setPayment] = useState<PaymentMethod>("cash");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [receipt, setReceipt] = useState<Sale | null>(null);

  const loadProducts = useCallback(async () => {
    setProducts(await listProducts({ search: search || undefined }));
  }, [search]);

  useEffect(() => {
    getStoreSettings().then((s) => setTaxRate(Number(s.tax_rate))).catch(() => setTaxRate(0));
  }, []);

  useEffect(() => {
    const t = setTimeout(loadProducts, 200);
    return () => clearTimeout(t);
  }, [loadProducts]);

  const lines = Object.values(cart);

  const totals = useMemo(() => {
    let subtotal = 0;
    let taxable = 0;
    for (const { product, quantity } of lines) {
      const lineTotal = Number(product.price) * quantity;
      subtotal += lineTotal;
      if (!product.tax_exempt) taxable += lineTotal;
    }
    const tax = Math.round(taxable * taxRate * 100) / 100;
    return { subtotal, tax, total: subtotal + tax };
  }, [lines, taxRate]);

  function addToCart(p: Product) {
    setError(null);
    setCart((c) => {
      const existing = c[p.id];
      const nextQty = (existing?.quantity ?? 0) + 1;
      if (nextQty > Number(p.stock_quantity)) return c; // don't exceed stock
      return { ...c, [p.id]: { product: p, quantity: nextQty } };
    });
  }

  function setQty(id: string, quantity: number) {
    setCart((c) => {
      if (quantity <= 0) {
        const rest = { ...c };
        delete rest[id];
        return rest;
      }
      const line = c[id];
      if (!line || quantity > Number(line.product.stock_quantity)) return c;
      return { ...c, [id]: { ...line, quantity } };
    });
  }

  async function completeSale() {
    if (lines.length === 0) return;
    setBusy(true);
    setError(null);
    try {
      const sale = await checkout(
        lines.map((l) => ({ product_id: l.product.id, quantity: String(l.quantity) })),
        payment,
      );
      setReceipt(sale);
      setCart({});
      loadProducts(); // refresh stock
    } catch (err) {
      setError(
        err instanceof ApiError && err.status === 409
          ? "Not enough stock for one of the items. Refresh and try again."
          : "Checkout failed. Please try again.",
      );
    } finally {
      setBusy(false);
    }
  }

  return (
    <>
      <main className="mx-auto grid w-full max-w-6xl gap-6 px-4 py-6 sm:px-6 lg:grid-cols-[1fr_380px]">
        {/* Product picker */}
        <section>
          <input
            className="input"
            placeholder="Search products to add…"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            aria-label="Search products"
          />
          <div className="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-3">
            {products.map((p) => {
              const out = Number(p.stock_quantity) <= 0;
              return (
                <button
                  key={p.id}
                  onClick={() => addToCart(p)}
                  disabled={out}
                  className="card p-4 text-left transition hover:border-primary hover:shadow-md disabled:cursor-not-allowed disabled:opacity-50"
                >
                  <div className="font-medium text-slate-900">{p.name}</div>
                  <div className="mt-1 tabular-nums text-primary">
                    {fmt(Number(p.price))}
                    <span className="text-slate-400">/{p.unit}</span>
                  </div>
                  <div className="mt-1 text-xs text-slate-500">
                    {out ? "Out of stock" : `${Number(p.stock_quantity)} in stock`}
                  </div>
                </button>
              );
            })}
            {products.length === 0 && (
              <p className="col-span-full py-10 text-center text-sm text-slate-500">
                No products found. Add some under Products first.
              </p>
            )}
          </div>
        </section>

        {/* Cart */}
        <aside className="card flex h-fit flex-col p-5 lg:sticky lg:top-6">
          <h2 className="font-heading text-lg font-bold text-slate-900">Current sale</h2>

          <div className="mt-4 flex-1 space-y-3">
            {lines.length === 0 ? (
              <p className="py-8 text-center text-sm text-slate-500">
                Tap products to add them to the sale.
              </p>
            ) : (
              lines.map(({ product, quantity }) => (
                <div key={product.id} className="flex items-center gap-2">
                  <div className="min-w-0 flex-1">
                    <div className="truncate text-sm font-medium text-slate-900">
                      {product.name}
                    </div>
                    <div className="text-xs text-slate-500">
                      {fmt(Number(product.price))} × {quantity}
                    </div>
                  </div>
                  <div className="flex items-center gap-1">
                    <button
                      onClick={() => setQty(product.id, quantity - 1)}
                      className="grid h-7 w-7 place-items-center rounded-md border border-slate-300 text-slate-600 hover:bg-slate-50"
                      aria-label={`Decrease ${product.name}`}
                    >
                      −
                    </button>
                    <span className="w-6 text-center text-sm tabular-nums">{quantity}</span>
                    <button
                      onClick={() => setQty(product.id, quantity + 1)}
                      className="grid h-7 w-7 place-items-center rounded-md border border-slate-300 text-slate-600 hover:bg-slate-50"
                      aria-label={`Increase ${product.name}`}
                    >
                      +
                    </button>
                  </div>
                  <div className="w-16 text-right text-sm font-medium tabular-nums text-slate-900">
                    {fmt(Number(product.price) * quantity)}
                  </div>
                </div>
              ))
            )}
          </div>

          <div className="mt-4 space-y-1 border-t border-slate-200 pt-4 text-sm">
            <div className="flex justify-between text-slate-600">
              <span>Subtotal</span>
              <span className="tabular-nums">{fmt(totals.subtotal)}</span>
            </div>
            <div className="flex justify-between text-slate-600">
              <span>Tax{taxRate > 0 ? ` (${(taxRate * 100).toFixed(2)}%)` : ""}</span>
              <span className="tabular-nums">{fmt(totals.tax)}</span>
            </div>
            <div className="flex justify-between pt-1 text-base font-bold text-slate-900">
              <span>Total</span>
              <span className="tabular-nums">{fmt(totals.total)}</span>
            </div>
          </div>

          <div className="mt-4 grid grid-cols-2 gap-2">
            {(["cash", "card"] as PaymentMethod[]).map((m) => (
              <button
                key={m}
                onClick={() => setPayment(m)}
                className={`rounded-lg border px-3 py-2 text-sm font-medium capitalize transition ${
                  payment === m
                    ? "border-primary bg-primary-soft text-primary"
                    : "border-slate-300 text-slate-600 hover:bg-slate-50"
                }`}
              >
                {m}
              </button>
            ))}
          </div>

          {error && (
            <p role="alert" className="mt-3 text-sm text-red-600">
              {error}
            </p>
          )}

          <button
            onClick={completeSale}
            disabled={busy || lines.length === 0}
            className="btn-primary mt-4 w-full py-3 text-base"
          >
            {busy ? "Completing…" : `Complete sale · ${fmt(totals.total)}`}
          </button>
        </aside>
      </main>

      {receipt && <ReceiptModal sale={receipt} onClose={() => setReceipt(null)} />}
    </>
  );
}

function ReceiptModal({ sale, onClose }: { sale: Sale; onClose: () => void }) {
  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 p-4"
      role="dialog"
      aria-modal="true"
      aria-label="Receipt"
      onClick={onClose}
    >
      <div
        className="w-full max-w-sm rounded-2xl bg-white p-6 shadow-xl"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="text-center">
          <div className="mx-auto grid h-12 w-12 place-items-center rounded-full bg-green-100 text-2xl text-green-700">
            ✓
          </div>
          <h2 className="mt-3 font-heading text-lg font-bold text-slate-900">Sale complete</h2>
          <p className="text-sm text-slate-500">
            {new Date(sale.created_at).toLocaleString()} · {sale.payment_method}
          </p>
        </div>

        <div className="mt-5 space-y-2 border-y border-slate-200 py-4 text-sm">
          {sale.items.map((i) => (
            <div key={i.product_id} className="flex justify-between">
              <span className="text-slate-700">
                {i.name} × {Number(i.quantity)}
              </span>
              <span className="tabular-nums text-slate-900">${Number(i.line_total).toFixed(2)}</span>
            </div>
          ))}
        </div>

        <div className="mt-4 space-y-1 text-sm">
          <div className="flex justify-between text-slate-600">
            <span>Subtotal</span>
            <span className="tabular-nums">${Number(sale.subtotal).toFixed(2)}</span>
          </div>
          <div className="flex justify-between text-slate-600">
            <span>Tax</span>
            <span className="tabular-nums">${Number(sale.tax_total).toFixed(2)}</span>
          </div>
          <div className="flex justify-between text-base font-bold text-slate-900">
            <span>Total</span>
            <span className="tabular-nums">${Number(sale.total).toFixed(2)}</span>
          </div>
        </div>

        <button onClick={onClose} className="btn-primary mt-6 w-full">
          New sale
        </button>
      </div>
    </div>
  );
}
