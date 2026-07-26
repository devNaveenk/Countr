"""SQL implementation of ReportRepository — aggregate queries over sales/sale_items."""

from datetime import datetime
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.domain.repositories.report_repository import (
    BestSeller,
    ReportRepository,
    SalesSummary,
)
from app.infrastructure.db.models.sale import SaleItemModel, SaleModel


class SqlReportRepository(ReportRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def sales_summary(self, *, since: datetime) -> SalesSummary:
        totals = self._session.execute(
            select(
                func.count(SaleModel.id),
                func.coalesce(func.sum(SaleModel.total), 0),
                func.coalesce(func.sum(SaleModel.tax_total), 0),
            ).where(SaleModel.created_at >= since)
        ).one()

        items_sold = self._session.execute(
            select(func.coalesce(func.sum(SaleItemModel.quantity), 0))
            .join(SaleModel, SaleItemModel.sale_id == SaleModel.id)
            .where(SaleModel.created_at >= since)
        ).scalar_one()

        return SalesSummary(
            sales_count=int(totals[0]),
            gross_revenue=Decimal(totals[1]),
            tax_collected=Decimal(totals[2]),
            items_sold=Decimal(items_sold),
        )

    def best_sellers(self, *, since: datetime, limit: int = 5) -> list[BestSeller]:
        rows = self._session.execute(
            select(
                SaleItemModel.product_id,
                func.max(SaleItemModel.name),
                func.sum(SaleItemModel.quantity),
                func.sum(SaleItemModel.line_total),
            )
            .join(SaleModel, SaleItemModel.sale_id == SaleModel.id)
            .where(SaleModel.created_at >= since)
            .group_by(SaleItemModel.product_id)
            .order_by(func.sum(SaleItemModel.quantity).desc())
            .limit(limit)
        ).all()

        return [
            BestSeller(
                product_id=r[0], name=r[1], quantity=Decimal(r[2]), revenue=Decimal(r[3])
            )
            for r in rows
        ]
