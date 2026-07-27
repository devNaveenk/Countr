/** Products feature — types + API calls (all go through the authed api client). */

import { api } from "@/lib/api/client";

export type ProductUnit = "each" | "lb" | "kg";

export interface Product {
  id: string;
  name: string;
  barcode: string | null;
  category: string | null;
  unit: ProductUnit;
  cost_price: string; // Decimals arrive as strings — keep exact, don't parseFloat for money
  price: string;
  tax_exempt: boolean;
  stock_quantity: string;
  reorder_level: string;
  is_active: boolean;
  is_low_stock: boolean;
}

export interface ProductWriteInput {
  name: string;
  price: string;
  cost_price: string;
  barcode: string | null;
  category: string | null;
  unit: ProductUnit;
  tax_exempt: boolean;
  reorder_level: string;
}

export interface ProductCreateInput extends ProductWriteInput {
  initial_stock: string;
}

export interface ListParams {
  search?: string;
  lowStockOnly?: boolean;
}

export function listProducts({ search, lowStockOnly }: ListParams = {}): Promise<Product[]> {
  const qs = new URLSearchParams();
  if (search) qs.set("search", search);
  if (lowStockOnly) qs.set("low_stock_only", "true");
  const suffix = qs.toString() ? `?${qs.toString()}` : "";
  return api.get<Product[]>(`/products${suffix}`);
}

export function createProduct(input: ProductCreateInput): Promise<Product> {
  return api.post<Product>("/products", input);
}

export function updateProduct(id: string, input: ProductWriteInput): Promise<Product> {
  return api.put<Product>(`/products/${id}`, input);
}

export function adjustStock(id: string, delta: string, note?: string): Promise<Product> {
  return api.post<Product>(`/products/${id}/stock`, { delta, note: note ?? null });
}

export function archiveProduct(id: string): Promise<Product> {
  return api.del<Product>(`/products/${id}`);
}
