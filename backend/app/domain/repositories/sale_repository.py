"""SaleRepository port.

`record` persists a fully-computed sale AND decrements product stock in a single
transaction (atomic checkout), so stock and sales can never disagree.
"""

from dataclasses import dataclass
from decimal import Decimal
from typing import Protocol
from uuid import UUID

from app.domain.entities.sale import PaymentMethod, Sale


@dataclass(frozen=True)
class SaleLineDraft:
    product_id: UUID
    name: str
    unit_price: Decimal
    quantity: Decimal
    line_total: Decimal
    tax_exempt: bool


@dataclass(frozen=True)
class SaleDraft:
    cashier_id: UUID | None
    payment_method: PaymentMethod
    subtotal: Decimal
    tax_total: Decimal
    total: Decimal
    lines: tuple[SaleLineDraft, ...]


class SaleRepository(Protocol):
    def record(self, draft: SaleDraft) -> Sale:
        """Persist the sale + items and decrement each product's stock, atomically."""
        ...

    def get(self, sale_id: UUID) -> Sale | None: ...

    def list_recent(self, *, limit: int = 50) -> list[Sale]: ...
