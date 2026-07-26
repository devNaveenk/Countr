"""GetStoreReport use-case — bundles the sales summary, best-sellers, and low-stock list."""

from dataclasses import dataclass
from datetime import datetime

from app.domain.entities.product import Product
from app.domain.repositories.product_repository import ProductRepository
from app.domain.repositories.report_repository import (
    BestSeller,
    ReportRepository,
    SalesSummary,
)


@dataclass(frozen=True)
class StoreReport:
    summary: SalesSummary
    best_sellers: list[BestSeller]
    low_stock: list[Product]


class GetStoreReport:
    def __init__(self, reports: ReportRepository, products: ProductRepository) -> None:
        self._reports = reports
        self._products = products

    def execute(self, *, since: datetime, best_sellers_limit: int = 5) -> StoreReport:
        return StoreReport(
            summary=self._reports.sales_summary(since=since),
            best_sellers=self._reports.best_sellers(since=since, limit=best_sellers_limit),
            low_stock=self._products.list(active_only=True, low_stock_only=True),
        )
