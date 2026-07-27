"""Inventory routes — summary totals and per-product stock-movement history. Protected."""

from uuid import UUID

from fastapi import APIRouter, Depends, Query

from app.api.v1.deps import (
    current_user,
    inventory_summary_use_case,
    list_movements_use_case,
)
from app.application.use_cases.inventory import GetInventorySummary, ListStockMovements
from app.schemas.inventory import InventorySummaryResponse, StockMovementResponse

router = APIRouter(prefix="/inventory", tags=["inventory"], dependencies=[Depends(current_user)])


@router.get("/summary", response_model=InventorySummaryResponse, summary="Inventory totals")
def summary(
    use_case: GetInventorySummary = Depends(inventory_summary_use_case),
) -> InventorySummaryResponse:
    return InventorySummaryResponse.from_summary(use_case.execute())


@router.get(
    "/products/{product_id}/movements",
    response_model=list[StockMovementResponse],
    summary="Stock movement history for a product",
)
def movements(
    product_id: UUID,
    limit: int = Query(default=50, ge=1, le=200),
    use_case: ListStockMovements = Depends(list_movements_use_case),
) -> list[StockMovementResponse]:
    return [
        StockMovementResponse.from_entity(m) for m in use_case.execute(product_id, limit=limit)
    ]
