"""Product catalog use-cases.

Each class is one action and depends only on the ProductRepository port (DIP). Business
rules that belong to the application (unique barcode, no negative stock) live here, not in
the API or the repository.
"""

from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from app.application.errors import (
    BarcodeAlreadyExists,
    InvalidStockAdjustment,
    ProductNotFound,
)
from app.domain.entities.product import Product, ProductUnit
from app.domain.repositories.product_repository import ProductRepository


@dataclass(frozen=True)
class ProductInput:
    name: str
    price: Decimal
    cost_price: Decimal = Decimal("0")
    barcode: str | None = None
    category: str | None = None
    unit: ProductUnit = ProductUnit.EACH
    tax_exempt: bool = False
    reorder_level: Decimal = Decimal("0")


def _clean_barcode(barcode: str | None) -> str | None:
    barcode = (barcode or "").strip()
    return barcode or None


class CreateProduct:
    def __init__(self, products: ProductRepository) -> None:
        self._products = products

    def execute(self, data: ProductInput, *, initial_stock: Decimal = Decimal("0")) -> Product:
        barcode = _clean_barcode(data.barcode)
        if barcode and self._products.get_by_barcode(barcode) is not None:
            raise BarcodeAlreadyExists(barcode)
        return self._products.create(
            name=data.name.strip(),
            barcode=barcode,
            category=(data.category or "").strip() or None,
            unit=data.unit,
            cost_price=data.cost_price,
            price=data.price,
            tax_exempt=data.tax_exempt,
            stock_quantity=initial_stock,
            reorder_level=data.reorder_level,
        )


class ListProducts:
    def __init__(self, products: ProductRepository) -> None:
        self._products = products

    def execute(
        self, *, search: str | None = None, active_only: bool = True, low_stock_only: bool = False
    ) -> list[Product]:
        return self._products.list(
            search=search, active_only=active_only, low_stock_only=low_stock_only
        )


class GetProduct:
    def __init__(self, products: ProductRepository) -> None:
        self._products = products

    def execute(self, product_id: UUID) -> Product:
        product = self._products.get(product_id)
        if product is None:
            raise ProductNotFound(str(product_id))
        return product


class UpdateProduct:
    def __init__(self, products: ProductRepository) -> None:
        self._products = products

    def execute(self, product_id: UUID, data: ProductInput) -> Product:
        existing = self._products.get(product_id)
        if existing is None:
            raise ProductNotFound(str(product_id))

        barcode = _clean_barcode(data.barcode)
        if barcode:
            clash = self._products.get_by_barcode(barcode)
            if clash is not None and clash.id != product_id:
                raise BarcodeAlreadyExists(barcode)

        updated = self._products.update(
            product_id,
            name=data.name.strip(),
            barcode=barcode,
            category=(data.category or "").strip() or None,
            unit=data.unit,
            cost_price=data.cost_price,
            price=data.price,
            tax_exempt=data.tax_exempt,
            reorder_level=data.reorder_level,
        )
        assert updated is not None  # existed a line above
        return updated


class ArchiveProduct:
    """Soft-delete: keep history, just hide from the active catalog."""

    def __init__(self, products: ProductRepository) -> None:
        self._products = products

    def execute(self, product_id: UUID) -> Product:
        product = self._products.set_active(product_id, False)
        if product is None:
            raise ProductNotFound(str(product_id))
        return product


class AdjustStock:
    def __init__(self, products: ProductRepository) -> None:
        self._products = products

    def execute(self, product_id: UUID, *, delta: Decimal) -> Product:
        current = self._products.get(product_id)
        if current is None:
            raise ProductNotFound(str(product_id))
        if current.stock_quantity + delta < 0:
            raise InvalidStockAdjustment(
                f"stock {current.stock_quantity} cannot absorb {delta}"
            )
        adjusted = self._products.adjust_stock(product_id, delta)
        assert adjusted is not None
        return adjusted
