/** Sales/checkout feature — types + API calls. */

import { api } from "@/lib/api/client";

export type PaymentMethod = "cash" | "card";

export interface SaleItem {
  product_id: string;
  name: string;
  unit_price: string;
  quantity: string;
  line_total: string;
  tax_exempt: boolean;
}

export interface Sale {
  id: string;
  created_at: string;
  payment_method: PaymentMethod;
  subtotal: string;
  tax_total: string;
  total: string;
  item_count: number;
  items: SaleItem[];
}

export interface CheckoutLine {
  product_id: string;
  quantity: string;
}

export function checkout(
  lines: CheckoutLine[],
  paymentMethod: PaymentMethod,
): Promise<Sale> {
  return api.post<Sale>("/sales", { lines, payment_method: paymentMethod });
}

export function listSales(limit = 50): Promise<Sale[]> {
  return api.get<Sale[]>(`/sales?limit=${limit}`);
}

export interface StoreSettings {
  tax_rate: string;
  currency: string;
}

export function getStoreSettings(): Promise<StoreSettings> {
  return api.get<StoreSettings>("/settings");
}
