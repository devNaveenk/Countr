"""Unit tests for the Checkout use-case (tax, totals, validation) using fakes."""

import uuid
from decimal import Decimal

import pytest

from app.application.errors import (
    EmptyCart,
    InsufficientStock,
    ProductInactive,
    ProductNotFound,
)
from app.application.use_cases.checkout import CartLine, Checkout, CheckoutCommand
from app.domain.entities.product import Product, ProductUnit
from app.domain.entities.sale import PaymentMethod, Sale, SaleItem
from app.domain.repositories.sale_repository import SaleDraft


def _product(price, *, stock="100", exempt=False, active=True) -> Product:
    return Product(
        id=uuid.uuid4(), name=f"P{price}", barcode=None, category=None,
        unit=ProductUnit.EACH, cost_price=Decimal("0"), price=Decimal(price),
        tax_exempt=exempt, stock_quantity=Decimal(stock), reorder_level=Decimal("0"),
        is_active=active,
    )


class FakeProductRepo:
    def __init__(self, products):
        self._by_id = {p.id: p for p in products}

    def get(self, product_id):
        return self._by_id.get(product_id)


class FakeSaleRepo:
    """Echoes the draft into a Sale so the use-case's computation can be asserted."""

    def __init__(self):
        self.recorded: SaleDraft | None = None

    def record(self, draft: SaleDraft) -> Sale:
        self.recorded = draft
        return Sale(
            id=uuid.uuid4(),
            created_at=__import__("datetime").datetime.now(),
            cashier_id=draft.cashier_id,
            payment_method=draft.payment_method,
            subtotal=draft.subtotal,
            tax_total=draft.tax_total,
            total=draft.total,
            items=tuple(
                SaleItem(
                    id=uuid.uuid4(), product_id=l.product_id, name=l.name,
                    unit_price=l.unit_price, quantity=l.quantity, line_total=l.line_total,
                    tax_exempt=l.tax_exempt,
                )
                for l in draft.lines
            ),
        )

    def get(self, sale_id):  # pragma: no cover - unused here
        return None

    def list_recent(self, *, limit=50):  # pragma: no cover - unused here
        return []


def _checkout(products, rate="0.10"):
    return Checkout(FakeProductRepo(products), FakeSaleRepo(), tax_rate=Decimal(rate))


def test_totals_and_tax_only_on_taxable_lines() -> None:
    soda = _product("2.00")                 # taxable
    milk = _product("3.00", exempt=True)    # exempt
    uc = _checkout([soda, milk])
    sale = uc.execute(
        CheckoutCommand(
            lines=(
                CartLine(soda.id, Decimal("2")),   # 4.00 taxable
                CartLine(milk.id, Decimal("1")),   # 3.00 exempt
            )
        )
    )
    assert sale.subtotal == Decimal("7.00")
    assert sale.tax_total == Decimal("0.40")   # 10% of 4.00
    assert sale.total == Decimal("7.40")
    assert sale.item_count == 2


def test_empty_cart_rejected() -> None:
    with pytest.raises(EmptyCart):
        _checkout([]).execute(CheckoutCommand(lines=()))


def test_insufficient_stock_rejected() -> None:
    soda = _product("2.00", stock="1")
    with pytest.raises(InsufficientStock):
        _checkout([soda]).execute(CheckoutCommand(lines=(CartLine(soda.id, Decimal("5")),)))


def test_inactive_product_rejected() -> None:
    soda = _product("2.00", active=False)
    with pytest.raises(ProductInactive):
        _checkout([soda]).execute(CheckoutCommand(lines=(CartLine(soda.id, Decimal("1")),)))


def test_unknown_product_rejected() -> None:
    with pytest.raises(ProductNotFound):
        _checkout([]).execute(CheckoutCommand(lines=(CartLine(uuid.uuid4(), Decimal("1")),)))


def test_zero_tax_rate() -> None:
    soda = _product("2.00")
    sale = _checkout([soda], rate="0").execute(
        CheckoutCommand(lines=(CartLine(soda.id, Decimal("3")),))
    )
    assert sale.tax_total == Decimal("0.00")
    assert sale.total == Decimal("6.00")
    assert sale.payment_method == PaymentMethod.CASH
