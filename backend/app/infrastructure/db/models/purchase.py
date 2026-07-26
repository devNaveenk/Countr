"""SQLAlchemy ORM models for purchases (received stock) and their line items."""

import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db.session import Base

MONEY = Numeric(12, 2)
QTY = Numeric(12, 3)


class PurchaseModel(Base):
    __tablename__ = "purchases"

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )
    supplier_name: Mapped[str | None] = mapped_column(String(200))
    received_by: Mapped[uuid.UUID | None] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL")
    )
    note: Mapped[str | None] = mapped_column(String(500))
    total_cost: Mapped[Decimal] = mapped_column(MONEY, nullable=False)

    items: Mapped[list["PurchaseItemModel"]] = relationship(
        back_populates="purchase", cascade="all, delete-orphan", lazy="selectin"
    )


class PurchaseItemModel(Base):
    __tablename__ = "purchase_items"

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    purchase_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("purchases.id", ondelete="CASCADE"), index=True
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("products.id", ondelete="RESTRICT")
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)  # snapshot
    unit_cost: Mapped[Decimal] = mapped_column(MONEY, nullable=False)
    quantity: Mapped[Decimal] = mapped_column(QTY, nullable=False)
    line_cost: Mapped[Decimal] = mapped_column(MONEY, nullable=False)

    purchase: Mapped[PurchaseModel] = relationship(back_populates="items")
