"""SQLAlchemy ORM model for products. Numeric (not float) for money and quantities."""

import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, Numeric, String, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.session import Base

MONEY = Numeric(12, 2)
QTY = Numeric(12, 3)  # allow weighted items, e.g. 1.250 lb


class ProductModel(Base):
    __tablename__ = "products"

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    barcode: Mapped[str | None] = mapped_column(String(64), unique=True, index=True)
    category: Mapped[str | None] = mapped_column(String(100), index=True)
    unit: Mapped[str] = mapped_column(String(16), nullable=False, default="each")
    cost_price: Mapped[Decimal] = mapped_column(MONEY, nullable=False, default=0)
    price: Mapped[Decimal] = mapped_column(MONEY, nullable=False, default=0)
    tax_exempt: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    stock_quantity: Mapped[Decimal] = mapped_column(QTY, nullable=False, default=0)
    reorder_level: Mapped[Decimal] = mapped_column(QTY, nullable=False, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
