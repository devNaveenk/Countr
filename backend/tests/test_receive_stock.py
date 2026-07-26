"""Unit tests for the ReceiveStock use-case using fakes."""

import uuid
from decimal import Decimal

import pytest

from app.application.errors import EmptyPurchase, ProductNotFound
from app.application.use_cases.receive_stock import (
    ReceiveLine,
    ReceiveStock,
    ReceiveStockCommand,
)
from app.domain.entities.product import Product, ProductUnit
from app.domain.entities.purchase import Purchase, PurchaseItem
from app.domain.repositories.purchase_repository import PurchaseDraft


def _product() -> Product:
    return Product(
        id=uuid.uuid4(), name="Rice", barcode=None, category=None, unit=ProductUnit.EACH,
        cost_price=Decimal("1.00"), price=Decimal("2.00"), tax_exempt=False,
        stock_quantity=Decimal("0"), reorder_level=Decimal("0"), is_active=True,
    )


class FakeProductRepo:
    def __init__(self, products):
        self._by_id = {p.id: p for p in products}

    def get(self, product_id):
        return self._by_id.get(product_id)


class FakePurchaseRepo:
    def __init__(self):
        self.recorded: PurchaseDraft | None = None

    def record(self, draft: PurchaseDraft) -> Purchase:
        self.recorded = draft
        return Purchase(
            id=uuid.uuid4(),
            created_at=__import__("datetime").datetime.now(),
            supplier_name=draft.supplier_name,
            received_by=draft.received_by,
            note=draft.note,
            total_cost=draft.total_cost,
            items=tuple(
                PurchaseItem(
                    id=uuid.uuid4(), product_id=l.product_id, name=l.name,
                    unit_cost=l.unit_cost, quantity=l.quantity, line_cost=l.line_cost,
                )
                for l in draft.lines
            ),
        )

    def get(self, purchase_id):  # pragma: no cover
        return None

    def list_recent(self, *, limit=50):  # pragma: no cover
        return []


def test_receive_computes_costs_and_total() -> None:
    p = _product()
    uc = ReceiveStock(FakeProductRepo([p]), FakePurchaseRepo())
    purchase = uc.execute(
        ReceiveStockCommand(
            lines=(ReceiveLine(p.id, Decimal("10"), Decimal("1.25")),),
            supplier_name="  Acme Foods ",
        )
    )
    assert purchase.total_cost == Decimal("12.50")
    assert purchase.item_count == 1
    assert purchase.supplier_name == "Acme Foods"  # trimmed


def test_empty_purchase_rejected() -> None:
    with pytest.raises(EmptyPurchase):
        ReceiveStock(FakeProductRepo([]), FakePurchaseRepo()).execute(
            ReceiveStockCommand(lines=())
        )


def test_unknown_product_rejected() -> None:
    with pytest.raises(ProductNotFound):
        ReceiveStock(FakeProductRepo([]), FakePurchaseRepo()).execute(
            ReceiveStockCommand(lines=(ReceiveLine(uuid.uuid4(), Decimal("1"), Decimal("1")),))
        )
