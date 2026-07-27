/** Inventory feature — summary totals + stock-movement history. */

import { api } from "@/lib/api/client";

export interface InventorySummary {
  total_products: number;
  total_units: string;
  stock_value: string;
  low_stock_count: number;
}

export type MovementReason = "sale" | "purchase" | "adjustment" | "initial";

export interface StockMovement {
  id: string;
  delta: string;
  balance_after: string;
  reason: MovementReason;
  note: string | null;
  created_at: string;
}

export function getInventorySummary(): Promise<InventorySummary> {
  return api.get<InventorySummary>("/inventory/summary");
}

export function listMovements(productId: string, limit = 50): Promise<StockMovement[]> {
  return api.get<StockMovement[]>(`/inventory/products/${productId}/movements?limit=${limit}`);
}
