/** Purchases (receive stock) feature — types + API. */

import { api } from "@/lib/api/client";

export interface PurchaseItem {
  product_id: string;
  name: string;
  unit_cost: string;
  quantity: string;
  line_cost: string;
}

export interface Purchase {
  id: string;
  created_at: string;
  supplier_name: string | null;
  note: string | null;
  total_cost: string;
  item_count: number;
  items: PurchaseItem[];
}

export interface ReceiveLine {
  product_id: string;
  quantity: string;
  unit_cost: string;
}

export function receiveStock(input: {
  lines: ReceiveLine[];
  supplier_name?: string | null;
  note?: string | null;
}): Promise<Purchase> {
  return api.post<Purchase>("/purchases", input);
}

export function listPurchases(limit = 20): Promise<Purchase[]> {
  return api.get<Purchase[]>(`/purchases?limit=${limit}`);
}
