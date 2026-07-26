"""Concrete ProductRepository over SQLAlchemy. Maps ORM rows <-> domain entities."""

from decimal import Decimal
from uuid import UUID

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.domain.entities.product import Product, ProductUnit
from app.domain.repositories.product_repository import ProductRepository
from app.infrastructure.db.models.product import ProductModel


def _to_entity(row: ProductModel) -> Product:
    return Product(
        id=row.id,
        name=row.name,
        barcode=row.barcode,
        category=row.category,
        unit=ProductUnit(row.unit),
        cost_price=row.cost_price,
        price=row.price,
        tax_exempt=row.tax_exempt,
        stock_quantity=row.stock_quantity,
        reorder_level=row.reorder_level,
        is_active=row.is_active,
    )


class SqlProductRepository(ProductRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(
        self,
        *,
        name: str,
        barcode: str | None,
        category: str | None,
        unit: ProductUnit,
        cost_price: Decimal,
        price: Decimal,
        tax_exempt: bool,
        stock_quantity: Decimal,
        reorder_level: Decimal,
    ) -> Product:
        row = ProductModel(
            name=name,
            barcode=barcode,
            category=category,
            unit=unit.value,
            cost_price=cost_price,
            price=price,
            tax_exempt=tax_exempt,
            stock_quantity=stock_quantity,
            reorder_level=reorder_level,
        )
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return _to_entity(row)

    def get(self, product_id: UUID) -> Product | None:
        row = self._session.get(ProductModel, product_id)
        return _to_entity(row) if row else None

    def get_by_barcode(self, barcode: str) -> Product | None:
        row = self._session.scalar(select(ProductModel).where(ProductModel.barcode == barcode))
        return _to_entity(row) if row else None

    def list(
        self, *, search: str | None = None, active_only: bool = True, low_stock_only: bool = False
    ) -> list[Product]:
        stmt = select(ProductModel)
        if active_only:
            stmt = stmt.where(ProductModel.is_active.is_(True))
        if search:
            like = f"%{search.strip()}%"
            stmt = stmt.where(
                or_(
                    ProductModel.name.ilike(like),
                    ProductModel.barcode.ilike(like),
                    ProductModel.category.ilike(like),
                )
            )
        if low_stock_only:
            stmt = stmt.where(
                ProductModel.reorder_level > 0,
                ProductModel.stock_quantity <= ProductModel.reorder_level,
            )
        stmt = stmt.order_by(ProductModel.name.asc())
        return [_to_entity(r) for r in self._session.scalars(stmt)]

    def update(
        self,
        product_id: UUID,
        *,
        name: str,
        barcode: str | None,
        category: str | None,
        unit: ProductUnit,
        cost_price: Decimal,
        price: Decimal,
        tax_exempt: bool,
        reorder_level: Decimal,
    ) -> Product | None:
        row = self._session.get(ProductModel, product_id)
        if row is None:
            return None
        row.name = name
        row.barcode = barcode
        row.category = category
        row.unit = unit.value
        row.cost_price = cost_price
        row.price = price
        row.tax_exempt = tax_exempt
        row.reorder_level = reorder_level
        self._session.commit()
        self._session.refresh(row)
        return _to_entity(row)

    def set_active(self, product_id: UUID, active: bool) -> Product | None:
        row = self._session.get(ProductModel, product_id)
        if row is None:
            return None
        row.is_active = active
        self._session.commit()
        self._session.refresh(row)
        return _to_entity(row)

    def adjust_stock(self, product_id: UUID, delta: Decimal) -> Product | None:
        row = self._session.get(ProductModel, product_id)
        if row is None:
            return None
        row.stock_quantity = row.stock_quantity + delta
        self._session.commit()
        self._session.refresh(row)
        return _to_entity(row)
