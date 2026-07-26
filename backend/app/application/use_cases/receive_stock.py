"""ReceiveStock (create Purchase) use-case — the inbound counterpart of Checkout.

Validates the received lines against the catalog, computes costs, and hands a fully
computed draft to the PurchaseRepository which persists it and raises stock atomically.
"""

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal
from uuid import UUID

from app.application.errors import EmptyPurchase, ProductNotFound
from app.domain.entities.purchase import Purchase
from app.domain.repositories.product_repository import ProductRepository
from app.domain.repositories.purchase_repository import (
    PurchaseDraft,
    PurchaseLineDraft,
    PurchaseRepository,
)

_CENTS = Decimal("0.01")


def _money(value: Decimal) -> Decimal:
    return value.quantize(_CENTS, rounding=ROUND_HALF_UP)


@dataclass(frozen=True)
class ReceiveLine:
    product_id: UUID
    quantity: Decimal
    unit_cost: Decimal


@dataclass(frozen=True)
class ReceiveStockCommand:
    lines: tuple[ReceiveLine, ...]
    supplier_name: str | None = None
    note: str | None = None


class ReceiveStock:
    def __init__(self, products: ProductRepository, purchases: PurchaseRepository) -> None:
        self._products = products
        self._purchases = purchases

    def execute(self, cmd: ReceiveStockCommand, *, received_by: UUID | None = None) -> Purchase:
        if not cmd.lines:
            raise EmptyPurchase()

        drafts: list[PurchaseLineDraft] = []
        total = Decimal("0")

        for line in cmd.lines:
            if line.quantity <= 0 or line.unit_cost < 0:
                raise EmptyPurchase()
            product = self._products.get(line.product_id)
            if product is None:
                raise ProductNotFound(str(line.product_id))

            line_cost = _money(line.unit_cost * line.quantity)
            total += line_cost
            drafts.append(
                PurchaseLineDraft(
                    product_id=product.id,
                    name=product.name,
                    unit_cost=line.unit_cost,
                    quantity=line.quantity,
                    line_cost=line_cost,
                )
            )

        supplier = (cmd.supplier_name or "").strip() or None
        note = (cmd.note or "").strip() or None

        return self._purchases.record(
            PurchaseDraft(
                supplier_name=supplier,
                received_by=received_by,
                note=note,
                total_cost=_money(total),
                lines=tuple(drafts),
            )
        )
