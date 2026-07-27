"""Concrete SaleRepository over SQLAlchemy.

`record` is the atomic checkout: it re-reads each product row FOR UPDATE, decrements stock,
inserts the sale + items, and commits once. If anything fails, the whole thing rolls back
so stock is never decremented without a corresponding sale.
"""

from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.application.errors import InsufficientStock, ProductNotFound
from app.domain.entities.sale import PaymentMethod, Sale, SaleItem
from app.domain.repositories.sale_repository import SaleDraft, SaleRepository
from app.infrastructure.db.models.product import ProductModel
from app.infrastructure.db.models.sale import SaleItemModel, SaleModel
from app.infrastructure.db.stock_ledger import record_movement


def _to_entity(row: SaleModel) -> Sale:
    items = tuple(
        SaleItem(
            id=i.id,
            product_id=i.product_id,
            name=i.name,
            unit_price=i.unit_price,
            quantity=i.quantity,
            line_total=i.line_total,
            tax_exempt=i.tax_exempt,
        )
        for i in sorted(row.items, key=lambda x: x.name)
    )
    return Sale(
        id=row.id,
        created_at=row.created_at,
        cashier_id=row.cashier_id,
        payment_method=PaymentMethod(row.payment_method),
        subtotal=row.subtotal,
        tax_total=row.tax_total,
        total=row.total,
        items=items,
    )


class SqlSaleRepository(SaleRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def record(self, draft: SaleDraft) -> Sale:
        sale = SaleModel(
            id=uuid4(),
            cashier_id=draft.cashier_id,
            payment_method=draft.payment_method.value,
            subtotal=draft.subtotal,
            tax_total=draft.tax_total,
            total=draft.total,
        )
        touched: list[tuple[ProductModel, Decimal]] = []
        for line in draft.lines:
            # Lock the product row so concurrent checkouts can't oversell.
            product = self._session.execute(
                select(ProductModel).where(ProductModel.id == line.product_id).with_for_update()
            ).scalar_one_or_none()
            if product is None:
                self._session.rollback()
                raise ProductNotFound(str(line.product_id))
            if product.stock_quantity < line.quantity:
                self._session.rollback()
                raise InsufficientStock(product.name)
            product.stock_quantity = product.stock_quantity - line.quantity
            touched.append((product, line.quantity))

            sale.items.append(
                SaleItemModel(
                    product_id=line.product_id,
                    name=line.name,
                    unit_price=line.unit_price,
                    quantity=line.quantity,
                    line_total=line.line_total,
                    tax_exempt=line.tax_exempt,
                )
            )

        # Ledger: one -qty movement per line, referencing this sale (ADR-0010).
        for product, qty in touched:
            record_movement(
                self._session, product=product, delta=-qty, reason="sale",
                reference_type="sale", reference_id=sale.id,
            )

        self._session.add(sale)
        self._session.commit()
        self._session.refresh(sale)
        return _to_entity(sale)

    def get(self, sale_id: UUID) -> Sale | None:
        row = self._session.get(SaleModel, sale_id)
        return _to_entity(row) if row else None

    def list_recent(self, *, limit: int = 50) -> list[Sale]:
        rows = self._session.scalars(
            select(SaleModel).order_by(SaleModel.created_at.desc()).limit(limit)
        )
        return [_to_entity(r) for r in rows]
