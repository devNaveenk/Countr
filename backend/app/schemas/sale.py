"""Sale boundary DTOs (Pydantic v2)."""

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.domain.entities.sale import PaymentMethod, Sale


class CartLineRequest(BaseModel):
    product_id: UUID
    quantity: Decimal = Field(gt=0, max_digits=12, decimal_places=3)


class CheckoutRequest(BaseModel):
    lines: list[CartLineRequest] = Field(min_length=1)
    payment_method: PaymentMethod = PaymentMethod.CASH


class SaleItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: UUID
    name: str
    unit_price: Decimal
    quantity: Decimal
    line_total: Decimal
    tax_exempt: bool


class SaleResponse(BaseModel):
    id: UUID
    created_at: datetime
    payment_method: PaymentMethod
    subtotal: Decimal
    tax_total: Decimal
    total: Decimal
    item_count: int
    items: list[SaleItemResponse]

    @classmethod
    def from_entity(cls, sale: Sale) -> "SaleResponse":
        return cls(
            id=sale.id,
            created_at=sale.created_at,
            payment_method=sale.payment_method,
            subtotal=sale.subtotal,
            tax_total=sale.tax_total,
            total=sale.total,
            item_count=sale.item_count,
            items=[SaleItemResponse.model_validate(i) for i in sale.items],
        )
