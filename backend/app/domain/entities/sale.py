"""Sale entities — a completed checkout and its line items.

Line items snapshot the product's name and unit price at the time of sale, so later edits
to the catalog never change historical receipts. Money is Decimal throughout.
"""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
from uuid import UUID


class PaymentMethod(str, Enum):
    CASH = "cash"
    CARD = "card"


@dataclass(frozen=True)
class SaleItem:
    id: UUID
    product_id: UUID
    name: str            # snapshot
    unit_price: Decimal  # snapshot
    quantity: Decimal
    line_total: Decimal
    tax_exempt: bool


@dataclass(frozen=True)
class Sale:
    id: UUID
    created_at: datetime
    cashier_id: UUID | None
    payment_method: PaymentMethod
    subtotal: Decimal
    tax_total: Decimal
    total: Decimal
    items: tuple[SaleItem, ...]

    @property
    def item_count(self) -> int:
        return len(self.items)
