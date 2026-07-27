"""Inventory boundary DTOs."""

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from app.application.use_cases.inventory import InventorySummary
from app.domain.entities.stock_movement import MovementReason, StockMovement


class InventorySummaryResponse(BaseModel):
    total_products: int
    total_units: Decimal
    stock_value: Decimal
    low_stock_count: int

    @classmethod
    def from_summary(cls, s: InventorySummary) -> "InventorySummaryResponse":
        return cls(
            total_products=s.total_products,
            total_units=s.total_units,
            stock_value=s.stock_value,
            low_stock_count=s.low_stock_count,
        )


class StockMovementResponse(BaseModel):
    id: UUID
    delta: Decimal
    balance_after: Decimal
    reason: MovementReason
    note: str | None
    created_at: datetime

    @classmethod
    def from_entity(cls, m: StockMovement) -> "StockMovementResponse":
        return cls(
            id=m.id,
            delta=m.delta,
            balance_after=m.balance_after,
            reason=m.reason,
            note=m.note,
            created_at=m.created_at,
        )
