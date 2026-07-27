"""ORM model for the append-only stock-movement ledger (see ADR-0010)."""

import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.session import Base

QTY = Numeric(12, 3)


class StockMovementModel(Base):
    __tablename__ = "stock_movements"

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("products.id", ondelete="CASCADE"), index=True
    )
    delta: Mapped[Decimal] = mapped_column(QTY, nullable=False)          # +in / -out
    balance_after: Mapped[Decimal] = mapped_column(QTY, nullable=False)  # on-hand after
    # sale / purchase / adjustment / initial
    reason: Mapped[str] = mapped_column(String(16), nullable=False)
    reference_type: Mapped[str | None] = mapped_column(String(16))
    reference_id: Mapped[uuid.UUID | None] = mapped_column(PGUUID(as_uuid=True))
    note: Mapped[str | None] = mapped_column(String(300))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )
