"""SQLAlchemy ORM models for sales and their line items."""

import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db.session import Base

MONEY = Numeric(12, 2)
QTY = Numeric(12, 3)


class SaleModel(Base):
    __tablename__ = "sales"

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )
    cashier_id: Mapped[uuid.UUID | None] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL")
    )
    payment_method: Mapped[str] = mapped_column(String(16), nullable=False, default="cash")
    subtotal: Mapped[Decimal] = mapped_column(MONEY, nullable=False)
    tax_total: Mapped[Decimal] = mapped_column(MONEY, nullable=False)
    total: Mapped[Decimal] = mapped_column(MONEY, nullable=False)

    items: Mapped[list["SaleItemModel"]] = relationship(
        back_populates="sale", cascade="all, delete-orphan", lazy="selectin"
    )


class SaleItemModel(Base):
    __tablename__ = "sale_items"

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    sale_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("sales.id", ondelete="CASCADE"), index=True
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("products.id", ondelete="RESTRICT")
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)  # snapshot
    unit_price: Mapped[Decimal] = mapped_column(MONEY, nullable=False)  # snapshot
    quantity: Mapped[Decimal] = mapped_column(QTY, nullable=False)
    line_total: Mapped[Decimal] = mapped_column(MONEY, nullable=False)
    tax_exempt: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    sale: Mapped[SaleModel] = relationship(back_populates="items")
