"""Product entity — a catalog item in a store.

Plain business object with a couple of real rules (low-stock, margin). Money and
quantities are Decimal, never float — this is a retail/financial domain.

`stock_quantity` is the current on-hand count kept here for the wedge (simple stores).
Stock only changes through the AdjustStock use-case, never via a plain edit, so movement
stays deliberate; a full stock-movement ledger arrives with the Inventory module.
"""

from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum
from uuid import UUID


class ProductUnit(StrEnum):
    EACH = "each"   # sold per item (a can, a bottle)
    LB = "lb"       # sold by weight (pounds) — US grocery
    KG = "kg"


@dataclass(frozen=True)
class Product:
    id: UUID
    name: str
    barcode: str | None
    category: str | None
    unit: ProductUnit
    cost_price: Decimal        # what the store pays
    price: Decimal             # what the customer pays
    tax_exempt: bool           # US grocery food is often sales-tax exempt
    stock_quantity: Decimal
    reorder_level: Decimal
    is_active: bool

    @property
    def is_low_stock(self) -> bool:
        return self.reorder_level > 0 and self.stock_quantity <= self.reorder_level

    @property
    def margin(self) -> Decimal | None:
        """Gross margin as a fraction of price (e.g. 0.25 = 25%)."""
        if self.price > 0:
            return (self.price - self.cost_price) / self.price
        return None
