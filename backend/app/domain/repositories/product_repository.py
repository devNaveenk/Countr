"""ProductRepository port — the catalog persistence abstraction (DIP).

Stock is moved only via `adjust_stock`, kept separate from `update` so edits can never
silently change on-hand quantity.
"""

from decimal import Decimal
from typing import Protocol
from uuid import UUID

from app.domain.entities.product import Product, ProductUnit


class ProductRepository(Protocol):
    def create(
        self,
        *,
        name: str,
        barcode: str | None,
        category: str | None,
        unit: ProductUnit,
        cost_price: Decimal,
        price: Decimal,
        tax_exempt: bool,
        stock_quantity: Decimal,
        reorder_level: Decimal,
    ) -> Product: ...

    def get(self, product_id: UUID) -> Product | None: ...

    def get_by_barcode(self, barcode: str) -> Product | None: ...

    def list(
        self, *, search: str | None = None, active_only: bool = True, low_stock_only: bool = False
    ) -> list[Product]: ...

    def update(
        self,
        product_id: UUID,
        *,
        name: str,
        barcode: str | None,
        category: str | None,
        unit: ProductUnit,
        cost_price: Decimal,
        price: Decimal,
        tax_exempt: bool,
        reorder_level: Decimal,
    ) -> Product | None: ...

    def set_active(self, product_id: UUID, active: bool) -> Product | None: ...

    def adjust_stock(self, product_id: UUID, delta: Decimal) -> Product | None: ...
