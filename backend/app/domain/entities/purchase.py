"""Purchase entities — stock received into the store (the inbound counterpart of a Sale).

Line items snapshot the product name and the unit cost paid. Receiving a purchase increases
stock and refreshes the product's cost price. Supplier is a free-text name for the first
layer; a managed Supplier entity can come later.
"""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True)
class PurchaseItem:
    id: UUID
    product_id: UUID
    name: str            # snapshot
    unit_cost: Decimal
    quantity: Decimal
    line_cost: Decimal


@dataclass(frozen=True)
class Purchase:
    id: UUID
    created_at: datetime
    supplier_name: str | None
    received_by: UUID | None
    note: str | None
    total_cost: Decimal
    items: tuple[PurchaseItem, ...]

    @property
    def item_count(self) -> int:
        return len(self.items)
