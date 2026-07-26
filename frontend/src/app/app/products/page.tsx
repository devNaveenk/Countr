"use client";

import { useCallback, useEffect, useState } from "react";

import { PackageIcon } from "@/components/ui/icons";
import {
  adjustStock,
  archiveProduct,
  listProducts,
  type Product,
} from "@/features/products/api";
import { ProductForm } from "@/features/products/ProductForm";

function money(v: string) {
  return `$${Number(v).toFixed(2)}`;
}

function qty(v: string) {
  // trim trailing zeros for display (14.000 -> 14, 1.250 -> 1.25)
  return String(Number(v));
}

export default function ProductsPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [lowStockOnly, setLowStockOnly] = useState(false);
  const [formOpen, setFormOpen] = useState(false);
  const [editing, setEditing] = useState<Product | undefined>(undefined);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      setProducts(await listProducts({ search: search || undefined, lowStockOnly }));
    } finally {
      setLoading(false);
    }
  }, [search, lowStockOnly]);

  useEffect(() => {
    const t = setTimeout(load, 200); // debounce search
    return () => clearTimeout(t);
  }, [load]);

  function openAdd() {
    setEditing(undefined);
    setFormOpen(true);
  }

  function openEdit(p: Product) {
    setEditing(p);
    setFormOpen(true);
  }

  async function onStock(p: Product, sign: 1 | -1) {
    const raw = window.prompt(
      `${sign > 0 ? "Add to" : "Remove from"} stock for "${p.name}" (current ${qty(p.stock_quantity)}):`,
      "1",
    );
    if (!raw) return;
    const amount = Number(raw);
    if (!Number.isFinite(amount) || amount <= 0) return;
    try {
      await adjustStock(p.id, String(sign * amount));
      await load();
    } catch {
      window.alert("Could not adjust stock (would it go negative?).");
    }
  }

  async function onArchive(p: Product) {
    if (!window.confirm(`Archive "${p.name}"? It will be hidden from the catalog.`)) return;
    await archiveProduct(p.id);
    await load();
  }

  return (
    <>
      <div className="mx-auto w-full max-w-6xl px-4 py-8 sm:px-6">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold tracking-tight text-slate-900">Products</h1>
            <p className="mt-1 text-sm text-slate-600">Your store catalog and stock.</p>
          </div>
          <button onClick={openAdd} className="btn-primary">
            + Add product
          </button>
        </div>

        {/* Filters */}
        <div className="mt-6 flex flex-wrap items-center gap-3">
          <input
            className="input max-w-xs"
            placeholder="Search name, barcode, category…"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            aria-label="Search products"
          />
          <label className="flex items-center gap-2 text-sm text-slate-700">
            <input
              type="checkbox"
              className="h-4 w-4 rounded border-slate-300 text-primary focus:ring-primary/30"
              checked={lowStockOnly}
              onChange={(e) => setLowStockOnly(e.target.checked)}
            />
            Low stock only
          </label>
        </div>

        {/* Table */}
        <div className="card mt-4 overflow-hidden">
          {loading ? (
            <p className="p-8 text-center text-sm text-slate-500">Loading products…</p>
          ) : products.length === 0 ? (
            <div className="p-12 text-center">
              <span className="mx-auto grid h-12 w-12 place-items-center rounded-xl bg-primary-soft text-primary">
                <PackageIcon className="h-6 w-6" />
              </span>
              <h3 className="mt-4 font-semibold text-slate-900">No products yet</h3>
              <p className="mt-1 text-sm text-slate-600">
                Add your first item to start building the catalog.
              </p>
              <button onClick={openAdd} className="btn-primary mt-4">
                + Add product
              </button>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-slate-200 text-left text-xs uppercase tracking-wide text-slate-500">
                    <th className="px-4 py-3 font-medium">Product</th>
                    <th className="px-4 py-3 font-medium">Category</th>
                    <th className="px-4 py-3 text-right font-medium">Price</th>
                    <th className="px-4 py-3 text-right font-medium">Stock</th>
                    <th className="px-4 py-3 font-medium">Tax</th>
                    <th className="px-4 py-3 text-right font-medium">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {products.map((p) => (
                    <tr key={p.id} className="hover:bg-slate-50">
                      <td className="px-4 py-3">
                        <div className="font-medium text-slate-900">{p.name}</div>
                        {p.barcode && (
                          <div className="font-mono text-xs text-slate-400">{p.barcode}</div>
                        )}
                      </td>
                      <td className="px-4 py-3 text-slate-600">{p.category ?? "—"}</td>
                      <td className="px-4 py-3 text-right tabular-nums text-slate-900">
                        {money(p.price)}
                        <span className="text-slate-400">/{p.unit}</span>
                      </td>
                      <td className="px-4 py-3 text-right">
                        <span
                          className={`tabular-nums ${
                            p.is_low_stock ? "font-semibold text-amber-600" : "text-slate-900"
                          }`}
                        >
                          {qty(p.stock_quantity)}
                        </span>
                        {p.is_low_stock && (
                          <span className="ml-2 rounded-full bg-amber-50 px-2 py-0.5 text-xs font-medium text-amber-700">
                            Low
                          </span>
                        )}
                      </td>
                      <td className="px-4 py-3 text-slate-600">
                        {p.tax_exempt ? "Exempt" : "Taxable"}
                      </td>
                      <td className="px-4 py-3">
                        <div className="flex items-center justify-end gap-1 text-sm">
                          <button
                            onClick={() => onStock(p, 1)}
                            className="rounded px-2 py-1 font-medium text-primary hover:bg-primary-soft"
                            aria-label={`Add stock to ${p.name}`}
                          >
                            + Stock
                          </button>
                          <button
                            onClick={() => onStock(p, -1)}
                            className="rounded px-2 py-1 font-medium text-slate-600 hover:bg-slate-100"
                            aria-label={`Remove stock from ${p.name}`}
                          >
                            − Stock
                          </button>
                          <button
                            onClick={() => openEdit(p)}
                            className="rounded px-2 py-1 font-medium text-slate-600 hover:bg-slate-100"
                          >
                            Edit
                          </button>
                          <button
                            onClick={() => onArchive(p)}
                            className="rounded px-2 py-1 font-medium text-red-600 hover:bg-red-50"
                          >
                            Archive
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>

      {formOpen && (
        <ProductForm
          product={editing}
          onClose={() => setFormOpen(false)}
          onSaved={() => {
            setFormOpen(false);
            load();
          }}
        />
      )}
    </>
  );
}
