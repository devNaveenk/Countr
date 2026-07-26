"""Purchase boundary DTOs (Pydantic v2)."""

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.domain.entities.purchase import Purchase


class ReceiveLineRequest(BaseModel):
    product_id: UUID
    quantity: Decimal = Field(gt=0, max_digits=12, decimal_places=3)
    unit_cost: Decimal = Field(ge=0, max_digits=12, decimal_places=2)


class ReceiveStockRequest(BaseModel):
    lines: list[ReceiveLineRequest] = Field(min_length=1)
    supplier_name: str | None = Field(default=None, max_length=200)
    note: str | None = Field(default=None, max_length=500)


class PurchaseItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: UUID
    name: str
    unit_cost: Decimal
    quantity: Decimal
    line_cost: Decimal


class PurchaseResponse(BaseModel):
    id: UUID
    created_at: datetime
    supplier_name: str | None
    note: str | None
    total_cost: Decimal
    item_count: int
    items: list[PurchaseItemResponse]

    @classmethod
    def from_entity(cls, purchase: Purchase) -> "PurchaseResponse":
        return cls(
            id=purchase.id,
            created_at=purchase.created_at,
            supplier_name=purchase.supplier_name,
            note=purchase.note,
            total_cost=purchase.total_cost,
            item_count=purchase.item_count,
            items=[PurchaseItemResponse.model_validate(i) for i in purchase.items],
        )
