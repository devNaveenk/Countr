"""Unit tests for product catalog use-cases using an in-memory fake repository."""

import uuid
from decimal import Decimal

import pytest

from app.application.errors import (
    BarcodeAlreadyExists,
    InvalidStockAdjustment,
    ProductNotFound,
)
from app.application.use_cases.product_catalog import (
    AdjustStock,
    ArchiveProduct,
    CreateProduct,
    ListProducts,
    ProductInput,
    UpdateProduct,
)
from app.domain.entities.product import Product, ProductUnit


class FakeProductRepository:
    def __init__(self) -> None:
        self._items: dict[uuid.UUID, Product] = {}

    def create(
        self, *, name, barcode, category, unit, cost_price, price, tax_exempt,
        stock_quantity, reorder_level,
    ) -> Product:
        product = Product(
            id=uuid.uuid4(), name=name, barcode=barcode, category=category, unit=unit,
            cost_price=cost_price, price=price, tax_exempt=tax_exempt,
            stock_quantity=stock_quantity, reorder_level=reorder_level, is_active=True,
        )
        self._items[product.id] = product
        return product

    def get(self, product_id):
        return self._items.get(product_id)

    def get_by_barcode(self, barcode):
        return next((p for p in self._items.values() if p.barcode == barcode), None)

    def list(self, *, search=None, active_only=True, low_stock_only=False):
        items = list(self._items.values())
        if active_only:
            items = [p for p in items if p.is_active]
        if low_stock_only:
            items = [p for p in items if p.is_low_stock]
        return items

    def update(self, product_id, *, name, barcode, category, unit, cost_price, price,
               tax_exempt, reorder_level):
        cur = self._items.get(product_id)
        if cur is None:
            return None
        import dataclasses
        updated = dataclasses.replace(
            cur, name=name, barcode=barcode, category=category, unit=unit,
            cost_price=cost_price, price=price, tax_exempt=tax_exempt,
            reorder_level=reorder_level,
        )
        self._items[product_id] = updated
        return updated

    def set_active(self, product_id, active):
        cur = self._items.get(product_id)
        if cur is None:
            return None
        import dataclasses
        updated = dataclasses.replace(cur, is_active=active)
        self._items[product_id] = updated
        return updated

    def adjust_stock(self, product_id, delta, *, note=None):
        cur = self._items.get(product_id)
        if cur is None:
            return None
        import dataclasses
        updated = dataclasses.replace(cur, stock_quantity=cur.stock_quantity + delta)
        self._items[product_id] = updated
        return updated


def _input(**kw):
    base = dict(name="Milk 1 gal", price=Decimal("3.99"))
    base.update(kw)
    return ProductInput(**base)


def test_create_product_trims_and_persists() -> None:
    repo = FakeProductRepository()
    product = CreateProduct(repo).execute(_input(name="  Bread  ", barcode=" 012 "))
    assert product.name == "Bread"
    assert product.barcode == "012"


def test_create_rejects_duplicate_barcode() -> None:
    repo = FakeProductRepository()
    uc = CreateProduct(repo)
    uc.execute(_input(barcode="111"))
    with pytest.raises(BarcodeAlreadyExists):
        uc.execute(_input(barcode="111"))


def test_low_stock_flag_and_filter() -> None:
    repo = FakeProductRepository()
    CreateProduct(repo).execute(_input(name="Eggs", reorder_level=Decimal("5")))
    # created with 0 stock, reorder 5 => low stock
    low = ListProducts(repo).execute(low_stock_only=True)
    assert len(low) == 1 and low[0].is_low_stock


def test_adjust_stock_rejects_negative_result() -> None:
    repo = FakeProductRepository()
    p = CreateProduct(repo).execute(_input())
    with pytest.raises(InvalidStockAdjustment):
        AdjustStock(repo).execute(p.id, delta=Decimal("-1"))


def test_adjust_stock_receives_and_removes() -> None:
    repo = FakeProductRepository()
    p = CreateProduct(repo).execute(_input())
    AdjustStock(repo).execute(p.id, delta=Decimal("10"))
    result = AdjustStock(repo).execute(p.id, delta=Decimal("-3"))
    assert result.stock_quantity == Decimal("7")


def test_update_missing_product_raises() -> None:
    with pytest.raises(ProductNotFound):
        UpdateProduct(FakeProductRepository()).execute(uuid.uuid4(), _input())


def test_archive_hides_from_active_list() -> None:
    repo = FakeProductRepository()
    p = CreateProduct(repo).execute(_input(unit=ProductUnit.EACH))
    ArchiveProduct(repo).execute(p.id)
    assert ListProducts(repo).execute(active_only=True) == []
