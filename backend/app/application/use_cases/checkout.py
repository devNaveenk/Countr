"""Checkout (CreateSale) use-case.

Validates the cart against the catalog, computes line totals + sales tax, and hands a fully
computed draft to the SaleRepository which persists it and decrements stock atomically.

Tax model (wedge): a single flat rate applied to non-exempt line totals. Real
per-jurisdiction tax comes later behind a TaxCalculator port.
"""

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal
from uuid import UUID

from app.application.errors import (
    EmptyCart,
    InsufficientStock,
    ProductInactive,
    ProductNotFound,
)
from app.domain.entities.sale import PaymentMethod, Sale
from app.domain.repositories.product_repository import ProductRepository
from app.domain.repositories.sale_repository import (
    SaleDraft,
    SaleLineDraft,
    SaleRepository,
)

_CENTS = Decimal("0.01")


def _money(value: Decimal) -> Decimal:
    return value.quantize(_CENTS, rounding=ROUND_HALF_UP)


@dataclass(frozen=True)
class CartLine:
    product_id: UUID
    quantity: Decimal


@dataclass(frozen=True)
class CheckoutCommand:
    lines: tuple[CartLine, ...]
    payment_method: PaymentMethod = PaymentMethod.CASH


class Checkout:
    def __init__(
        self, products: ProductRepository, sales: SaleRepository, *, tax_rate: Decimal
    ) -> None:
        self._products = products
        self._sales = sales
        self._tax_rate = tax_rate

    def execute(self, cmd: CheckoutCommand, *, cashier_id: UUID | None = None) -> Sale:
        if not cmd.lines:
            raise EmptyCart()

        drafts: list[SaleLineDraft] = []
        subtotal = Decimal("0")
        taxable_base = Decimal("0")

        for line in cmd.lines:
            if line.quantity <= 0:
                raise EmptyCart()
            product = self._products.get(line.product_id)
            if product is None:
                raise ProductNotFound(str(line.product_id))
            if not product.is_active:
                raise ProductInactive(product.name)
            if product.stock_quantity < line.quantity:
                raise InsufficientStock(product.name)

            line_total = _money(product.price * line.quantity)
            subtotal += line_total
            if not product.tax_exempt:
                taxable_base += line_total

            drafts.append(
                SaleLineDraft(
                    product_id=product.id,
                    name=product.name,
                    unit_price=product.price,
                    quantity=line.quantity,
                    line_total=line_total,
                    tax_exempt=product.tax_exempt,
                )
            )

        tax_total = _money(taxable_base * self._tax_rate)
        total = _money(subtotal + tax_total)

        return self._sales.record(
            SaleDraft(
                cashier_id=cashier_id,
                payment_method=cmd.payment_method,
                subtotal=_money(subtotal),
                tax_total=tax_total,
                total=total,
                lines=tuple(drafts),
            )
        )
