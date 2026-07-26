/** Reports feature — types + API. */

import { api } from "@/lib/api/client";
import type { Product } from "@/features/products/api";

export interface SalesSummary {
  sales_count: number;
  gross_revenue: string;
  tax_collected: string;
  items_sold: string;
}

export interface BestSeller {
  product_id: string;
  name: string;
  quantity: string;
  revenue: string;
}

export interface StoreReport {
  period_days: number;
  summary: SalesSummary;
  best_sellers: BestSeller[];
  low_stock: Product[];
}

export function getOverview(days: number): Promise<StoreReport> {
  return api.get<StoreReport>(`/reports/overview?days=${days}`);
}
