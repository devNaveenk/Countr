"""Product boundary DTOs (Pydantic v2)."""

from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.domain.entities.product import Product, ProductUnit


class ProductWriteRequest(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    price: Decimal = Field(ge=0, max_digits=12, decimal_places=2)
    cost_price: Decimal = Field(default=Decimal("0"), ge=0, max_digits=12, decimal_places=2)
    barcode: str | None = Field(default=None, max_length=64)
    category: str | None = Field(default=None, max_length=100)
    unit: ProductUnit = ProductUnit.EACH
    tax_exempt: bool = False
    reorder_level: Decimal = Field(default=Decimal("0"), ge=0, max_digits=12, decimal_places=3)


class ProductCreateRequest(ProductWriteRequest):
    initial_stock: Decimal = Field(default=Decimal("0"), ge=0, max_digits=12, decimal_places=3)


class StockAdjustmentRequest(BaseModel):
    # positive to receive stock, negative to remove; not zero
    delta: Decimal = Field(max_digits=12, decimal_places=3)


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    barcode: str | None
    category: str | None
    unit: ProductUnit
    cost_price: Decimal
    price: Decimal
    tax_exempt: bool
    stock_quantity: Decimal
    reorder_level: Decimal
    is_active: bool
    is_low_stock: bool

    @classmethod
    def from_entity(cls, product: Product) -> "ProductResponse":
        return cls(
            id=product.id,
            name=product.name,
            barcode=product.barcode,
            category=product.category,
            unit=product.unit,
            cost_price=product.cost_price,
            price=product.price,
            tax_exempt=product.tax_exempt,
            stock_quantity=product.stock_quantity,
            reorder_level=product.reorder_level,
            is_active=product.is_active,
            is_low_stock=product.is_low_stock,
        )
