"""Read-side SQL implementation of StockMovementRepository."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.entities.stock_movement import MovementReason, StockMovement
from app.domain.repositories.stock_movement_repository import StockMovementRepository
from app.infrastructure.db.models.stock_movement import StockMovementModel


def _to_entity(row: StockMovementModel) -> StockMovement:
    return StockMovement(
        id=row.id,
        product_id=row.product_id,
        delta=row.delta,
        balance_after=row.balance_after,
        reason=MovementReason(row.reason),
        reference_type=row.reference_type,
        reference_id=row.reference_id,
        note=row.note,
        created_at=row.created_at,
    )


class SqlStockMovementRepository(StockMovementRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def list_for_product(self, product_id: UUID, *, limit: int = 50) -> list[StockMovement]:
        rows = self._session.scalars(
            select(StockMovementModel)
            .where(StockMovementModel.product_id == product_id)
            .order_by(StockMovementModel.created_at.desc())
            .limit(limit)
        )
        return [_to_entity(r) for r in rows]
