"""Report boundary DTOs."""

from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from app.application.use_cases.store_report import StoreReport
from app.schemas.product import ProductResponse


class SalesSummaryResponse(BaseModel):
    sales_count: int
    gross_revenue: Decimal
    tax_collected: Decimal
    items_sold: Decimal


class BestSellerResponse(BaseModel):
    product_id: UUID
    name: str
    quantity: Decimal
    revenue: Decimal


class StoreReportResponse(BaseModel):
    period_days: int
    summary: SalesSummaryResponse
    best_sellers: list[BestSellerResponse]
    low_stock: list[ProductResponse]

    @classmethod
    def from_report(cls, report: StoreReport, *, period_days: int) -> "StoreReportResponse":
        return cls(
            period_days=period_days,
            summary=SalesSummaryResponse(
                sales_count=report.summary.sales_count,
                gross_revenue=report.summary.gross_revenue,
                tax_collected=report.summary.tax_collected,
                items_sold=report.summary.items_sold,
            ),
            best_sellers=[
                BestSellerResponse(
                    product_id=b.product_id, name=b.name, quantity=b.quantity, revenue=b.revenue
                )
                for b in report.best_sellers
            ],
            low_stock=[ProductResponse.from_entity(p) for p in report.low_stock],
        )
