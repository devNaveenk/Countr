"""PurchaseRepository port.

`record` persists the purchase AND increases each product's stock (and refreshes its cost
price) in a single transaction — the inbound mirror of the sale checkout.
"""

from dataclasses import dataclass
from decimal import Decimal
from typing import Protocol
from uuid import UUID

from app.domain.entities.purchase import Purchase


@dataclass(frozen=True)
class PurchaseLineDraft:
    product_id: UUID
    name: str
    unit_cost: Decimal
    quantity: Decimal
    line_cost: Decimal


@dataclass(frozen=True)
class PurchaseDraft:
    supplier_name: str | None
    received_by: UUID | None
    note: str | None
    total_cost: Decimal
    lines: tuple[PurchaseLineDraft, ...]


class PurchaseRepository(Protocol):
    def record(self, draft: PurchaseDraft) -> Purchase:
        """Persist the purchase + items and increase product stock/cost, atomically."""
        ...

    def get(self, purchase_id: UUID) -> Purchase | None: ...

    def list_recent(self, *, limit: int = 50) -> list[Purchase]: ...
