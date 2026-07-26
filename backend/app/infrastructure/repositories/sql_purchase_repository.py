"""Concrete PurchaseRepository over SQLAlchemy.

`record` is the atomic receive: it locks each product row, raises its stock, refreshes its
cost price to the latest unit cost, inserts the purchase + items, and commits once.
"""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.application.errors import ProductNotFound
from app.domain.entities.purchase import Purchase, PurchaseItem
from app.domain.repositories.purchase_repository import PurchaseDraft, PurchaseRepository
from app.infrastructure.db.models.product import ProductModel
from app.infrastructure.db.models.purchase import PurchaseItemModel, PurchaseModel


def _to_entity(row: PurchaseModel) -> Purchase:
    items = tuple(
        PurchaseItem(
            id=i.id,
            product_id=i.product_id,
            name=i.name,
            unit_cost=i.unit_cost,
            quantity=i.quantity,
            line_cost=i.line_cost,
        )
        for i in sorted(row.items, key=lambda x: x.name)
    )
    return Purchase(
        id=row.id,
        created_at=row.created_at,
        supplier_name=row.supplier_name,
        received_by=row.received_by,
        note=row.note,
        total_cost=row.total_cost,
        items=items,
    )


class SqlPurchaseRepository(PurchaseRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def record(self, draft: PurchaseDraft) -> Purchase:
        purchase = PurchaseModel(
            supplier_name=draft.supplier_name,
            received_by=draft.received_by,
            note=draft.note,
            total_cost=draft.total_cost,
        )
        for line in draft.lines:
            product = self._session.execute(
                select(ProductModel).where(ProductModel.id == line.product_id).with_for_update()
            ).scalar_one_or_none()
            if product is None:
                self._session.rollback()
                raise ProductNotFound(str(line.product_id))
            product.stock_quantity = product.stock_quantity + line.quantity
            product.cost_price = line.unit_cost  # keep cost current

            purchase.items.append(
                PurchaseItemModel(
                    product_id=line.product_id,
                    name=line.name,
                    unit_cost=line.unit_cost,
                    quantity=line.quantity,
                    line_cost=line.line_cost,
                )
            )

        self._session.add(purchase)
        self._session.commit()
        self._session.refresh(purchase)
        return _to_entity(purchase)

    def get(self, purchase_id: UUID) -> Purchase | None:
        row = self._session.get(PurchaseModel, purchase_id)
        return _to_entity(row) if row else None

    def list_recent(self, *, limit: int = 50) -> list[Purchase]:
        rows = self._session.scalars(
            select(PurchaseModel).order_by(PurchaseModel.created_at.desc()).limit(limit)
        )
        return [_to_entity(r) for r in rows]
