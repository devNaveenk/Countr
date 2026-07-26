"use client";

import { useState } from "react";

import { ApiError } from "@/lib/api/client";
import {
  createProduct,
  updateProduct,
  type Product,
  type ProductUnit,
} from "@/features/products/api";

interface Props {
  /** When present, the form edits this product; otherwise it creates a new one. */
  product?: Product;
  onClose: () => void;
  onSaved: (product: Product) => void;
}

const units: ProductUnit[] = ["each", "lb", "kg"];

export function ProductForm({ product, onClose, onSaved }: Props) {
  const editing = Boolean(product);
  const [name, setName] = useState(product?.name ?? "");
  const [barcode, setBarcode] = useState(product?.barcode ?? "");
  const [category, setCategory] = useState(product?.category ?? "");
  const [unit, setUnit] = useState<ProductUnit>(product?.unit ?? "each");
  const [price, setPrice] = useState(product?.price ?? "");
  const [cost, setCost] = useState(product?.cost_price ?? "");
  const [reorder, setReorder] = useState(product?.reorder_level ?? "0");
  const [initialStock, setInitialStock] = useState("0");
  const [taxExempt, setTaxExempt] = useState(product?.tax_exempt ?? false);
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setSaving(true);
    const base = {
      name,
      price: price || "0",
      cost_price: cost || "0",
      barcode: barcode.trim() || null,
      category: category.trim() || null,
      unit,
      tax_exempt: taxExempt,
      reorder_level: reorder || "0",
    };
    try {
      const saved = product
        ? await updateProduct(product.id, base)
        : await createProduct({ ...base, initial_stock: initialStock || "0" });
      onSaved(saved);
    } catch (err) {
      setError(
        err instanceof ApiError && err.status === 409
          ? "A product with this barcode already exists."
          : "Could not save the product. Please try again.",
      );
    } finally {
      setSaving(false);
    }
  }

  return (
    <div
      className="fixed inset-0 z-50 flex items-end justify-center bg-slate-900/40 p-0 sm:items-center sm:p-4"
      role="dialog"
      aria-modal="true"
      aria-label={editing ? "Edit product" : "Add product"}
      onClick={onClose}
    >
      <div
        className="max-h-[92vh] w-full max-w-lg overflow-y-auto rounded-t-2xl bg-white p-6 shadow-xl sm:rounded-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <h2 className="text-lg font-bold text-slate-900">
          {editing ? "Edit product" : "Add product"}
        </h2>

        <form onSubmit={onSubmit} className="mt-5 space-y-4" noValidate>
          <div>
            <label htmlFor="p-name" className="label">
              Name
            </label>
            <input
              id="p-name"
              className="input mt-1"
              required
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label htmlFor="p-price" className="label">
                Sell price ($)
              </label>
              <input
                id="p-price"
                className="input mt-1"
                inputMode="decimal"
                required
                value={price}
                onChange={(e) => setPrice(e.target.value)}
              />
            </div>
            <div>
              <label htmlFor="p-cost" className="label">
                Cost price ($)
              </label>
              <input
                id="p-cost"
                className="input mt-1"
                inputMode="decimal"
                value={cost}
                onChange={(e) => setCost(e.target.value)}
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label htmlFor="p-barcode" className="label">
                Barcode (UPC)
              </label>
              <input
                id="p-barcode"
                className="input mt-1"
                inputMode="numeric"
                value={barcode}
                onChange={(e) => setBarcode(e.target.value)}
              />
            </div>
            <div>
              <label htmlFor="p-category" className="label">
                Category
              </label>
              <input
                id="p-category"
                className="input mt-1"
                value={category}
                onChange={(e) => setCategory(e.target.value)}
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label htmlFor="p-unit" className="label">
                Sold by
              </label>
              <select
                id="p-unit"
                className="input mt-1"
                value={unit}
                onChange={(e) => setUnit(e.target.value as ProductUnit)}
              >
                {units.map((u) => (
                  <option key={u} value={u}>
                    {u === "each" ? "Each (per item)" : u === "lb" ? "Pound (lb)" : "Kilogram (kg)"}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label htmlFor="p-reorder" className="label">
                Reorder at
              </label>
              <input
                id="p-reorder"
                className="input mt-1"
                inputMode="decimal"
                value={reorder}
                onChange={(e) => setReorder(e.target.value)}
              />
            </div>
          </div>

          {!editing && (
            <div>
              <label htmlFor="p-stock" className="label">
                Starting stock
              </label>
              <input
                id="p-stock"
                className="input mt-1"
                inputMode="decimal"
                value={initialStock}
                onChange={(e) => setInitialStock(e.target.value)}
              />
            </div>
          )}

          <label className="flex items-center gap-2 text-sm text-slate-700">
            <input
              type="checkbox"
              className="h-4 w-4 rounded border-slate-300 text-primary focus:ring-primary/30"
              checked={taxExempt}
              onChange={(e) => setTaxExempt(e.target.checked)}
            />
            Tax-exempt (e.g. grocery food)
          </label>

          {error && (
            <p role="alert" className="text-sm text-red-600">
              {error}
            </p>
          )}

          <div className="flex justify-end gap-3 pt-2">
            <button type="button" onClick={onClose} className="btn-secondary">
              Cancel
            </button>
            <button type="submit" disabled={saving} className="btn-primary">
              {saving ? "Saving…" : editing ? "Save changes" : "Add product"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
