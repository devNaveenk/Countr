"""ReportRepository port — read-side aggregates over sales for the dashboard."""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Protocol
from uuid import UUID


@dataclass(frozen=True)
class SalesSummary:
    sales_count: int
    gross_revenue: Decimal
    tax_collected: Decimal
    items_sold: Decimal


@dataclass(frozen=True)
class BestSeller:
    product_id: UUID
    name: str
    quantity: Decimal
    revenue: Decimal


class ReportRepository(Protocol):
    def sales_summary(self, *, since: datetime) -> SalesSummary: ...

    def best_sellers(self, *, since: datetime, limit: int = 5) -> list[BestSeller]: ...
