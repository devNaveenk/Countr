"""Inventory read use-cases — summary totals and per-product movement history."""

from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from app.domain.entities.stock_movement import StockMovement
from app.domain.repositories.product_repository import ProductRepository
from app.domain.repositories.stock_movement_repository import StockMovementRepository


@dataclass(frozen=True)
class InventorySummary:
    total_products: int
    total_units: Decimal
    stock_value: Decimal  # sum(stock_quantity * cost_price)
    low_stock_count: int


class GetInventorySummary:
    def __init__(self, products: ProductRepository) -> None:
        self._products = products

    def execute(self) -> InventorySummary:
        products = self._products.list(active_only=True)
        total_units = sum((p.stock_quantity for p in products), Decimal("0"))
        stock_value = sum(
            (p.stock_quantity * p.cost_price for p in products), Decimal("0")
        )
        low = sum(1 for p in products if p.is_low_stock)
        return InventorySummary(
            total_products=len(products),
            total_units=total_units,
            stock_value=stock_value.quantize(Decimal("0.01")),
            low_stock_count=low,
        )


class ListStockMovements:
    def __init__(self, movements: StockMovementRepository) -> None:
        self._movements = movements

    def execute(self, product_id: UUID, *, limit: int = 50) -> list[StockMovement]:
        return self._movements.list_for_product(product_id, limit=limit)
