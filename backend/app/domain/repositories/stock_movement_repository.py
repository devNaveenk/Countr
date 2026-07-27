"""Read-side port for the stock-movement ledger."""

from typing import Protocol
from uuid import UUID

from app.domain.entities.stock_movement import StockMovement


class StockMovementRepository(Protocol):
    def list_for_product(self, product_id: UUID, *, limit: int = 50) -> list[StockMovement]: ...
