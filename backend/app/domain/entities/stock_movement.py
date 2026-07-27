"""StockMovement entity — one row in the stock ledger (read model)."""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from uuid import UUID


class MovementReason(StrEnum):
    SALE = "sale"
    PURCHASE = "purchase"
    ADJUSTMENT = "adjustment"
    INITIAL = "initial"


@dataclass(frozen=True)
class StockMovement:
    id: UUID
    product_id: UUID
    delta: Decimal
    balance_after: Decimal
    reason: MovementReason
    reference_type: str | None
    reference_id: UUID | None
    note: str | None
    created_at: datetime
