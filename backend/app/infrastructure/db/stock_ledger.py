"""Shared helper that appends a stock-movement row when a product's stock changes.

Called from the sale, purchase, and product repositories inside their existing
transactions, so the ledger and the on-hand quantity are always written together (ADR-0010).
Call this AFTER mutating `product.stock_quantity` so `balance_after` is correct.
"""

from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Session

from app.infrastructure.db.models.product import ProductModel
from app.infrastructure.db.models.stock_movement import StockMovementModel


def record_movement(
    session: Session,
    *,
    product: ProductModel,
    delta: Decimal,
    reason: str,
    reference_type: str | None = None,
    reference_id: UUID | None = None,
    note: str | None = None,
) -> None:
    session.add(
        StockMovementModel(
            product_id=product.id,
            delta=delta,
            balance_after=product.stock_quantity,
            reason=reason,
            reference_type=reference_type,
            reference_id=reference_id,
            note=note,
        )
    )
